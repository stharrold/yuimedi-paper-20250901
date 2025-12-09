"""Tests for SemanticScholarAdapter."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from lit_review.infrastructure.adapters.semantic_scholar_adapter import (
    SemanticScholarAdapter,
)


@pytest.fixture
def mock_s2_response() -> dict:
    """Return mock Semantic Scholar API response."""
    return {
        "total": 2,
        "offset": 0,
        "data": [
            {
                "paperId": "abc123def456",
                "externalIds": {
                    "DOI": "10.1234/test1",
                    "ArXiv": "2401.12345",
                },
                "title": "Machine Learning in Healthcare",
                "authors": [
                    {"authorId": "1", "name": "John Smith"},
                    {"authorId": "2", "name": "Jones, Jane A."},
                ],
                "year": 2024,
                "venue": "Journal of AI in Medicine",
                "abstract": "This paper explores ML applications.",
                "citationCount": 42,
            },
            {
                "paperId": "xyz789ghi012",
                "externalIds": {"ArXiv": "2401.67890"},
                "title": "Deep Learning for Diagnosis",
                "authors": [{"authorId": "3", "name": "Wilson, Bob"}],
                "year": 2023,
                "venue": "Medical AI Conference",
                "abstract": "Deep learning methods.",
                "citationCount": 15,
            },
        ],
    }


class TestSemanticScholarAdapter:
    """Tests for SemanticScholarAdapter."""

    def test_get_service_name(self) -> None:
        """get_service_name returns 'Semantic Scholar'."""
        adapter = SemanticScholarAdapter()
        assert adapter.get_service_name() == "Semantic Scholar"

    def test_init_sets_default_rate_limit(self) -> None:
        """__init__ sets default rate limit to 3 seconds."""
        adapter = SemanticScholarAdapter()
        assert adapter.rate_limit == 3.0

    def test_init_accepts_api_key(self) -> None:
        """__init__ accepts API key."""
        adapter = SemanticScholarAdapter(api_key="test_key")
        assert adapter.api_key == "test_key"

    @patch("lit_review.infrastructure.adapters.semantic_scholar_adapter.httpx.Client")
    def test_search_returns_papers(
        self,
        mock_client_class: MagicMock,
        mock_s2_response: dict,
    ) -> None:
        """search returns list of Paper entities."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_s2_response
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = SemanticScholarAdapter()
        papers = adapter.search("machine learning", limit=10)

        assert len(papers) == 2
        assert papers[0].title == "Machine Learning in Healthcare"
        assert papers[0].doi.value == "10.1234/test1"
        assert len(papers[0].authors) == 2
        assert papers[0].authors[0].last_name == "Smith"

    @patch("lit_review.infrastructure.adapters.semantic_scholar_adapter.httpx.Client")
    def test_search_parses_authors_correctly(
        self,
        mock_client_class: MagicMock,
        mock_s2_response: dict,
    ) -> None:
        """search correctly parses author information."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_s2_response
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = SemanticScholarAdapter()
        papers = adapter.search("test")

        # First paper, first author (First Last format)
        first_author = papers[0].authors[0]
        assert first_author.last_name == "Smith"
        assert first_author.first_name == "John"
        assert first_author.initials == "J."

        # First paper, second author (Last, First format)
        second_author = papers[0].authors[1]
        assert second_author.last_name == "Jones"
        assert second_author.first_name == "Jane A."

        # Second paper, author (Last, First format)
        third_author = papers[1].authors[0]
        assert third_author.last_name == "Wilson"
        assert third_author.first_name == "Bob"

    @patch("lit_review.infrastructure.adapters.semantic_scholar_adapter.httpx.Client")
    def test_search_includes_citation_count(
        self,
        mock_client_class: MagicMock,
        mock_s2_response: dict,
    ) -> None:
        """search includes citation count in keywords."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_s2_response
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = SemanticScholarAdapter()
        papers = adapter.search("test")

        assert "citations:42" in papers[0].keywords
        assert "citations:15" in papers[1].keywords

    @patch("lit_review.infrastructure.adapters.semantic_scholar_adapter.httpx.Client")
    def test_search_uses_arxiv_id_when_no_doi(
        self,
        mock_client_class: MagicMock,
        mock_s2_response: dict,
    ) -> None:
        """search uses ArXiv ID when DOI not present."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_s2_response
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = SemanticScholarAdapter()
        papers = adapter.search("test")

        # Second paper has no DOI, should use ArXiv ID
        assert papers[1].doi.value == "arXiv:2401.67890"

    @patch("lit_review.infrastructure.adapters.semantic_scholar_adapter.httpx.Client")
    def test_search_uses_s2_id_as_fallback(self, mock_client_class: MagicMock) -> None:
        """search uses S2 paper ID when no DOI or ArXiv ID."""
        response_data = {
            "data": [
                {
                    "paperId": "s2paper123",
                    "externalIds": {},
                    "title": "Paper Without DOI",
                    "authors": [{"name": "John Smith"}],
                    "year": 2024,
                    "venue": "Test Venue",
                }
            ]
        }

        mock_response = MagicMock()
        mock_response.json.return_value = response_data
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = SemanticScholarAdapter()
        papers = adapter.search("test")

        assert len(papers) == 1
        assert papers[0].doi.value == "S2:s2paper123"

    @patch("lit_review.infrastructure.adapters.semantic_scholar_adapter.httpx.Client")
    def test_search_handles_missing_year(self, mock_client_class: MagicMock) -> None:
        """search defaults to 2024 when year missing."""
        response_data = {
            "data": [
                {
                    "paperId": "test123",
                    "externalIds": {"DOI": "10.1234/test"},
                    "title": "Paper Without Year",
                    "authors": [{"name": "John Smith"}],
                    "venue": "Test Venue",
                }
            ]
        }

        mock_response = MagicMock()
        mock_response.json.return_value = response_data
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = SemanticScholarAdapter()
        papers = adapter.search("test")

        assert papers[0].publication_year == 2024

    @patch("lit_review.infrastructure.adapters.semantic_scholar_adapter.httpx.Client")
    def test_search_handles_empty_response(self, mock_client_class: MagicMock) -> None:
        """search handles empty response gracefully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = SemanticScholarAdapter()
        papers = adapter.search("nonexistent query")

        assert papers == []

    @patch("lit_review.infrastructure.adapters.semantic_scholar_adapter.httpx.Client")
    def test_search_sends_api_key_when_provided(
        self,
        mock_client_class: MagicMock,
        mock_s2_response: dict,
    ) -> None:
        """search includes API key in headers when provided."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_s2_response
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = SemanticScholarAdapter(api_key="test_key")
        adapter.search("test")

        # Check that API key was sent in headers
        call_kwargs = mock_client.get.call_args[1]
        assert "headers" in call_kwargs
        assert call_kwargs["headers"]["x-api-key"] == "test_key"

    @patch("lit_review.infrastructure.adapters.semantic_scholar_adapter.httpx.Client")
    def test_search_retries_on_timeout(self, mock_client_class: MagicMock) -> None:
        """search retries on timeout."""
        response_data = {
            "data": [
                {
                    "paperId": "test123",
                    "externalIds": {"DOI": "10.1234/test"},
                    "title": "Test Paper",
                    "authors": [{"name": "John Smith"}],
                    "year": 2024,
                    "venue": "Test Venue",
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = response_data
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock()
        # First two calls timeout, third succeeds
        mock_client.get.side_effect = [
            httpx.TimeoutException("Timeout"),
            httpx.TimeoutException("Timeout"),
            mock_response,
        ]
        mock_client_class.return_value = mock_client

        adapter = SemanticScholarAdapter(max_retries=3)
        papers = adapter.search("test")

        assert len(papers) == 1
        assert mock_client.get.call_count == 3

    @patch("lit_review.infrastructure.adapters.semantic_scholar_adapter.httpx.Client")
    def test_search_raises_timeout_after_retries(self, mock_client_class: MagicMock) -> None:
        """search raises TimeoutError after max retries."""
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock()
        mock_client.get.side_effect = httpx.TimeoutException("Timeout")
        mock_client_class.return_value = mock_client

        adapter = SemanticScholarAdapter(max_retries=2)

        with pytest.raises(TimeoutError) as exc_info:
            adapter.search("test")

        assert "timed out" in str(exc_info.value)

    @patch("lit_review.infrastructure.adapters.semantic_scholar_adapter.httpx.Client")
    def test_search_raises_connection_error_on_failure(self, mock_client_class: MagicMock) -> None:
        """search raises ConnectionError on persistent failure."""
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock()
        mock_client.get.side_effect = httpx.HTTPError("Network error")
        mock_client_class.return_value = mock_client

        adapter = SemanticScholarAdapter(max_retries=2)

        with pytest.raises(ConnectionError) as exc_info:
            adapter.search("test")

        assert "failed" in str(exc_info.value)

    @patch("lit_review.infrastructure.adapters.semantic_scholar_adapter.time.sleep")
    def test_rate_limiting(self, mock_sleep: MagicMock) -> None:
        """_rate_limit_sleep respects rate limits."""
        adapter = SemanticScholarAdapter(rate_limit=3.0)

        # First call should not sleep
        adapter._rate_limit_sleep()
        mock_sleep.assert_not_called()

        # Immediate second call should sleep
        adapter._last_request_time = adapter._last_request_time - 1.0  # 1 second ago
        adapter._rate_limit_sleep()
        # Should sleep for ~2 seconds
        assert mock_sleep.call_count == 1


class TestSemanticScholarAdapterParsing:
    """Tests for Semantic Scholar response parsing."""

    def test_parse_response_with_valid_data(self, mock_s2_response: dict) -> None:
        """_parse_response correctly parses valid response."""
        adapter = SemanticScholarAdapter()
        papers = adapter._parse_response(mock_s2_response)

        assert len(papers) == 2
        assert papers[0].title == "Machine Learning in Healthcare"

    def test_extract_doi_prefers_doi_over_arxiv(self) -> None:
        """_extract_doi prefers DOI over ArXiv ID."""
        item = {
            "paperId": "test123",
            "externalIds": {
                "DOI": "10.1234/test",
                "ArXiv": "2401.12345",
            },
        }

        adapter = SemanticScholarAdapter()
        doi = adapter._extract_doi(item)

        assert doi == "10.1234/test"

    def test_extract_doi_uses_arxiv_when_no_doi(self) -> None:
        """_extract_doi uses ArXiv ID when no DOI."""
        item = {
            "paperId": "test123",
            "externalIds": {"ArXiv": "2401.12345"},
        }

        adapter = SemanticScholarAdapter()
        doi = adapter._extract_doi(item)

        assert doi == "arXiv:2401.12345"

    def test_extract_doi_falls_back_to_paper_id(self) -> None:
        """_extract_doi uses paper ID when no external IDs."""
        item = {
            "paperId": "s2paper123",
            "externalIds": {},
        }

        adapter = SemanticScholarAdapter()
        doi = adapter._extract_doi(item)

        assert doi == "S2:s2paper123"

    def test_parse_authors_handles_first_last_format(self) -> None:
        """_parse_authors handles 'First Last' format."""
        adapter = SemanticScholarAdapter()
        authors = adapter._parse_authors([{"name": "John Smith"}])

        assert len(authors) == 1
        assert authors[0].last_name == "Smith"
        assert authors[0].first_name == "John"
        assert authors[0].initials == "J."

    def test_parse_authors_handles_last_first_format(self) -> None:
        """_parse_authors handles 'Last, First' format."""
        adapter = SemanticScholarAdapter()
        authors = adapter._parse_authors([{"name": "Smith, John A."}])

        assert len(authors) == 1
        assert authors[0].last_name == "Smith"
        assert authors[0].first_name == "John A."

    def test_parse_authors_handles_single_name(self) -> None:
        """_parse_authors handles single name."""
        adapter = SemanticScholarAdapter()
        authors = adapter._parse_authors([{"name": "Madonna"}])

        assert len(authors) == 1
        assert authors[0].last_name == "Madonna"
        assert authors[0].first_name == "Unknown"
        assert authors[0].initials == "U."

    def test_parse_authors_skips_empty_names(self) -> None:
        """_parse_authors skips entries without names."""
        adapter = SemanticScholarAdapter()
        authors = adapter._parse_authors([{"authorId": "1"}])

        assert len(authors) == 0


@pytest.mark.integration
class TestSemanticScholarAdapterIntegration:
    """Integration tests for Semantic Scholar API (requires network)."""

    def test_real_semantic_scholar_search(self) -> None:
        """search performs real Semantic Scholar query (integration test)."""
        adapter = SemanticScholarAdapter()
        papers = adapter.search("machine learning healthcare", limit=5)

        assert len(papers) > 0
        assert all(paper.title for paper in papers)
        assert all(paper.authors for paper in papers)
        assert all(paper.doi.value for paper in papers)
        # Check citation count is present
        assert any("citations:" in kw for paper in papers for kw in paper.keywords)
