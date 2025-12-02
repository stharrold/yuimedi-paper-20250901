"""Tests for CrossrefAdapter."""

from unittest.mock import MagicMock, patch

import pytest

from lit_review.infrastructure.adapters.crossref_adapter import CrossrefAdapter


@pytest.fixture
def mock_crossref_response() -> dict:
    """Return mock Crossref API response."""
    return {
        "message": {
            "items": [
                {
                    "DOI": "10.1234/test1",
                    "title": ["Test Paper One"],
                    "author": [
                        {"family": "Smith", "given": "John"},
                        {"family": "Jones", "given": "Jane"},
                    ],
                    "published": {"date-parts": [[2024]]},
                    "container-title": ["Test Journal"],
                    "abstract": "<p>This is the abstract.</p>",
                },
                {
                    "DOI": "10.1234/test2",
                    "title": ["Test Paper Two"],
                    "author": [{"family": "Wilson", "given": "Bob"}],
                    "published": {"date-parts": [[2023]]},
                    "container-title": ["Another Journal"],
                },
            ]
        }
    }


class TestCrossrefAdapter:
    """Tests for CrossrefAdapter."""

    def test_get_service_name(self) -> None:
        """get_service_name returns 'Crossref'."""
        adapter = CrossrefAdapter()
        assert adapter.get_service_name() == "Crossref"

    @patch("lit_review.infrastructure.adapters.crossref_adapter.requests.get")
    def test_search_returns_papers(self, mock_get: MagicMock, mock_crossref_response: dict) -> None:
        """search returns list of Paper entities."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_crossref_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        adapter = CrossrefAdapter()
        papers = adapter.search("test query", limit=10)

        assert len(papers) == 2
        assert papers[0].doi.value == "10.1234/test1"
        assert papers[0].title == "Test Paper One"
        assert len(papers[0].authors) == 2
        assert papers[0].authors[0].last_name == "Smith"

    @patch("lit_review.infrastructure.adapters.crossref_adapter.requests.get")
    def test_search_parses_authors_correctly(
        self, mock_get: MagicMock, mock_crossref_response: dict
    ) -> None:
        """search correctly parses author information."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_crossref_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        adapter = CrossrefAdapter()
        papers = adapter.search("test query")

        first_author = papers[0].authors[0]
        assert first_author.last_name == "Smith"
        assert first_author.first_name == "John"
        assert first_author.initials == "J."

    @patch("lit_review.infrastructure.adapters.crossref_adapter.requests.get")
    def test_search_cleans_html_from_abstract(
        self, mock_get: MagicMock, mock_crossref_response: dict
    ) -> None:
        """search removes HTML tags from abstract."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_crossref_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        adapter = CrossrefAdapter()
        papers = adapter.search("test query")

        assert papers[0].abstract == "This is the abstract."
        assert "<p>" not in papers[0].abstract

    @patch("lit_review.infrastructure.adapters.crossref_adapter.requests.get")
    def test_search_handles_empty_response(self, mock_get: MagicMock) -> None:
        """search handles empty response gracefully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"message": {"items": []}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        adapter = CrossrefAdapter()
        papers = adapter.search("test query")

        assert papers == []

    @patch("lit_review.infrastructure.adapters.crossref_adapter.requests.get")
    def test_search_skips_items_without_doi(self, mock_get: MagicMock) -> None:
        """search skips items missing DOI."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "message": {
                "items": [
                    {
                        "title": ["No DOI Paper"],
                        "author": [{"family": "Smith", "given": "John"}],
                    }
                ]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        adapter = CrossrefAdapter()
        papers = adapter.search("test query")

        assert papers == []

    @patch("lit_review.infrastructure.adapters.crossref_adapter.requests.get")
    def test_search_retries_on_timeout(self, mock_get: MagicMock) -> None:
        """search retries on timeout."""
        import requests

        # First two calls timeout, third succeeds
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "message": {
                "items": [
                    {
                        "DOI": "10.1234/test",
                        "title": ["Test Paper"],
                        "author": [{"family": "Smith", "given": "John"}],
                        "published": {"date-parts": [[2024]]},
                        "container-title": ["Journal"],
                    }
                ]
            }
        }
        mock_response.raise_for_status.return_value = None

        mock_get.side_effect = [
            requests.Timeout(),
            requests.Timeout(),
            mock_response,
        ]

        adapter = CrossrefAdapter(max_retries=3)
        papers = adapter.search("test query")

        assert len(papers) == 1
        assert mock_get.call_count == 3

    @patch("lit_review.infrastructure.adapters.crossref_adapter.requests.get")
    def test_search_raises_timeout_after_retries(self, mock_get: MagicMock) -> None:
        """search raises TimeoutError after max retries."""
        import requests

        mock_get.side_effect = requests.Timeout()

        adapter = CrossrefAdapter(max_retries=2)

        with pytest.raises(TimeoutError) as exc_info:
            adapter.search("test query")

        assert "timed out" in str(exc_info.value)

    @patch("lit_review.infrastructure.adapters.crossref_adapter.requests.get")
    def test_search_raises_connection_error_on_failure(self, mock_get: MagicMock) -> None:
        """search raises ConnectionError on persistent failure."""
        import requests

        mock_get.side_effect = requests.RequestException("Network error")

        adapter = CrossrefAdapter(max_retries=2)

        with pytest.raises(ConnectionError) as exc_info:
            adapter.search("test query")

        assert "failed" in str(exc_info.value)


class TestCrossrefAdapterParsing:
    """Tests for Crossref response parsing."""

    def test_parse_authors_handles_missing_given_name(self) -> None:
        """_parse_authors handles authors without given name."""
        adapter = CrossrefAdapter()
        authors = adapter._parse_authors([{"family": "Smith"}])

        assert len(authors) == 1
        assert authors[0].last_name == "Smith"
        assert authors[0].first_name == "Unknown"

    def test_parse_authors_handles_orcid(self) -> None:
        """_parse_authors includes ORCID when present."""
        adapter = CrossrefAdapter()
        authors = adapter._parse_authors(
            [
                {
                    "family": "Smith",
                    "given": "John",
                    "ORCID": "0000-0001-2345-6789",
                }
            ]
        )

        assert authors[0].orcid == "0000-0001-2345-6789"

    def test_clean_html_removes_tags(self) -> None:
        """_clean_html removes HTML tags."""
        adapter = CrossrefAdapter()

        html = "<p>This is <strong>bold</strong> text.</p>"
        clean = adapter._clean_html(html)

        assert clean == "This is bold text."
