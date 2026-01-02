# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for ArxivAdapter."""

from unittest.mock import MagicMock, patch
from xml.etree import ElementTree

import httpx
import pytest

from lit_review.infrastructure.adapters.arxiv_adapter import ArxivAdapter


@pytest.fixture
def mock_arxiv_atom() -> bytes:
    """Return mock ArXiv ATOM response."""
    atom = """<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
        <entry>
            <id>http://arxiv.org/abs/2401.12345v1</id>
            <title>Machine Learning for Healthcare Diagnosis</title>
            <author>
                <name>John Smith</name>
            </author>
            <author>
                <name>Jane A. Jones</name>
            </author>
            <published>2024-01-15T10:00:00Z</published>
            <summary>This paper explores machine learning applications in healthcare diagnosis.</summary>
            <arxiv:primary_category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
            <category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
            <category term="cs.AI" scheme="http://arxiv.org/schemas/atom"/>
            <link href="http://dx.doi.org/10.1234/arxiv.2024.001" title="doi"/>
        </entry>
        <entry>
            <id>http://arxiv.org/abs/2401.67890v2</id>
            <title>Another ML Paper</title>
            <author>
                <name>Bob Wilson</name>
            </author>
            <published>2023-12-01T15:30:00Z</published>
            <summary>Another abstract.</summary>
            <arxiv:primary_category term="stat.ML" scheme="http://arxiv.org/schemas/atom"/>
            <category term="stat.ML" scheme="http://arxiv.org/schemas/atom"/>
        </entry>
    </feed>
    """
    return atom.encode("utf-8")


@pytest.mark.integration
class TestArxivAdapter:
    """Tests for ArxivAdapter (integration - mocked HTTP)."""

    def test_get_service_name(self) -> None:
        """get_service_name returns 'ArXiv'."""
        adapter = ArxivAdapter()
        assert adapter.get_service_name() == "ArXiv"

    def test_init_sets_default_rate_limit(self) -> None:
        """__init__ sets default rate limit to 3 seconds."""
        adapter = ArxivAdapter()
        assert adapter.rate_limit == 3.0

    def test_init_accepts_custom_rate_limit(self) -> None:
        """__init__ accepts custom rate limit."""
        adapter = ArxivAdapter(rate_limit=5.0)
        assert adapter.rate_limit == 5.0

    @patch("lit_review.infrastructure.adapters.arxiv_adapter.httpx.Client")
    def test_search_returns_papers(
        self,
        mock_client_class: MagicMock,
        mock_arxiv_atom: bytes,
    ) -> None:
        """search returns list of Paper entities."""
        mock_response = MagicMock()
        mock_response.content = mock_arxiv_atom
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=None)
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = ArxivAdapter()
        papers = adapter.search("machine learning", limit=10)

        assert len(papers) == 2
        assert papers[0].title == "Machine Learning for Healthcare Diagnosis"
        assert papers[0].doi.value == "10.1234/arxiv.2024.001"
        assert len(papers[0].authors) == 2
        assert papers[0].authors[0].last_name == "Smith"

    @patch("lit_review.infrastructure.adapters.arxiv_adapter.httpx.Client")
    def test_search_parses_authors_correctly(
        self,
        mock_client_class: MagicMock,
        mock_arxiv_atom: bytes,
    ) -> None:
        """search correctly parses author information."""
        mock_response = MagicMock()
        mock_response.content = mock_arxiv_atom
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=None)
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = ArxivAdapter()
        papers = adapter.search("test")

        first_author = papers[0].authors[0]
        assert first_author.last_name == "Smith"
        assert first_author.first_name == "John"
        assert first_author.initials == "J."

        second_author = papers[0].authors[1]
        assert second_author.last_name == "Jones"
        assert second_author.first_name == "Jane A."
        assert second_author.initials == "J.A."

    @patch("lit_review.infrastructure.adapters.arxiv_adapter.httpx.Client")
    def test_search_extracts_categories_as_keywords(
        self,
        mock_client_class: MagicMock,
        mock_arxiv_atom: bytes,
    ) -> None:
        """search extracts categories as keywords."""
        mock_response = MagicMock()
        mock_response.content = mock_arxiv_atom
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=None)
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = ArxivAdapter()
        papers = adapter.search("test")

        assert "cs.LG" in papers[0].keywords
        assert "cs.AI" in papers[0].keywords

    @patch("lit_review.infrastructure.adapters.arxiv_adapter.httpx.Client")
    def test_search_uses_arxiv_id_as_doi_fallback(
        self,
        mock_client_class: MagicMock,
    ) -> None:
        """search uses ArXiv ID as DOI when no DOI present."""
        atom = """<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
            <entry>
                <id>http://arxiv.org/abs/2401.12345v1</id>
                <title>Paper Without DOI</title>
                <author><name>Bob Wilson</name></author>
                <published>2024-01-15T10:00:00Z</published>
                <summary>Abstract text.</summary>
                <arxiv:primary_category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
            </entry>
        </feed>
        """
        mock_response = MagicMock()
        mock_response.content = atom.encode("utf-8")
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=None)
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = ArxivAdapter()
        papers = adapter.search("test")

        assert len(papers) == 1
        assert papers[0].doi.value == "arXiv:2401.12345v1"

    @patch("lit_review.infrastructure.adapters.arxiv_adapter.httpx.Client")
    def test_search_extracts_publication_year(
        self,
        mock_client_class: MagicMock,
        mock_arxiv_atom: bytes,
    ) -> None:
        """search extracts publication year from published date."""
        mock_response = MagicMock()
        mock_response.content = mock_arxiv_atom
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=None)
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = ArxivAdapter()
        papers = adapter.search("test")

        assert papers[0].publication_year == 2024
        assert papers[1].publication_year == 2023

    @patch("lit_review.infrastructure.adapters.arxiv_adapter.httpx.Client")
    def test_search_sets_journal_from_category(
        self,
        mock_client_class: MagicMock,
        mock_arxiv_atom: bytes,
    ) -> None:
        """search sets journal from primary category."""
        mock_response = MagicMock()
        mock_response.content = mock_arxiv_atom
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=None)
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = ArxivAdapter()
        papers = adapter.search("test")

        assert papers[0].journal == "arXiv:cs.LG"
        assert papers[1].journal == "arXiv:stat.ML"

    @patch("lit_review.infrastructure.adapters.arxiv_adapter.httpx.Client")
    def test_search_handles_empty_response(self, mock_client_class: MagicMock) -> None:
        """search handles empty response gracefully."""
        atom = """<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom"></feed>
        """
        mock_response = MagicMock()
        mock_response.content = atom.encode("utf-8")
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=None)
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        adapter = ArxivAdapter()
        papers = adapter.search("nonexistent query")

        assert papers == []

    @patch("lit_review.infrastructure.adapters.arxiv_adapter.httpx.Client")
    def test_search_retries_on_timeout(self, mock_client_class: MagicMock) -> None:
        """search retries on timeout."""
        atom = """<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
            <entry>
                <id>http://arxiv.org/abs/2401.12345v1</id>
                <title>Test Paper</title>
                <author><name>John Smith</name></author>
                <published>2024-01-15T10:00:00Z</published>
                <summary>Abstract.</summary>
                <arxiv:primary_category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
            </entry>
        </feed>
        """
        mock_response = MagicMock()
        mock_response.content = atom.encode("utf-8")
        mock_response.raise_for_status.return_value = None

        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=None)
        # First two calls timeout, third succeeds
        mock_client.get.side_effect = [
            httpx.TimeoutException("Timeout"),
            httpx.TimeoutException("Timeout"),
            mock_response,
        ]
        mock_client_class.return_value = mock_client

        adapter = ArxivAdapter(max_retries=3)
        papers = adapter.search("test")

        assert len(papers) == 1
        assert mock_client.get.call_count == 3

    @patch("lit_review.infrastructure.adapters.arxiv_adapter.httpx.Client")
    def test_search_raises_timeout_after_retries(self, mock_client_class: MagicMock) -> None:
        """search raises TimeoutError after max retries."""
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=None)
        mock_client.get.side_effect = httpx.TimeoutException("Timeout")
        mock_client_class.return_value = mock_client

        adapter = ArxivAdapter(max_retries=2)

        with pytest.raises(TimeoutError) as exc_info:
            adapter.search("test")

        assert "timed out" in str(exc_info.value)

    @patch("lit_review.infrastructure.adapters.arxiv_adapter.httpx.Client")
    def test_search_raises_connection_error_on_failure(self, mock_client_class: MagicMock) -> None:
        """search raises ConnectionError on persistent failure."""
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=None)
        mock_client.get.side_effect = httpx.HTTPError("Network error")
        mock_client_class.return_value = mock_client

        adapter = ArxivAdapter(max_retries=2)

        with pytest.raises(ConnectionError) as exc_info:
            adapter.search("test")

        assert "failed" in str(exc_info.value)

    @patch("lit_review.infrastructure.adapters.arxiv_adapter.time.sleep")
    def test_rate_limiting(self, mock_sleep: MagicMock) -> None:
        """_rate_limit_sleep respects rate limits."""
        adapter = ArxivAdapter(rate_limit=3.0)

        # First call should not sleep
        adapter._rate_limit_sleep()
        mock_sleep.assert_not_called()

        # Immediate second call should sleep for 3 seconds
        adapter._last_request_time = adapter._last_request_time - 1.0  # 1 second ago
        adapter._rate_limit_sleep()
        # Should sleep for ~2 seconds (3 seconds - 1 second elapsed)
        assert mock_sleep.call_count == 1


@pytest.mark.integration
class TestArxivAdapterParsing:
    """Tests for ArXiv ATOM parsing (integration - DOI validation)."""

    def test_parse_atom_with_valid_data(self, mock_arxiv_atom: bytes) -> None:
        """_parse_atom correctly parses valid ATOM."""
        adapter = ArxivAdapter()
        papers = adapter._parse_atom(mock_arxiv_atom)

        assert len(papers) == 2
        assert papers[0].title == "Machine Learning for Healthcare Diagnosis"

    def test_extract_arxiv_id_from_url(self) -> None:
        """_extract_arxiv_id extracts ID from URL."""
        atom = """<?xml version="1.0" encoding="UTF-8"?>
        <entry xmlns="http://www.w3.org/2005/Atom">
            <id>http://arxiv.org/abs/2401.12345v1</id>
        </entry>
        """
        entry = ElementTree.fromstring(atom.encode("utf-8"))
        adapter = ArxivAdapter()

        arxiv_id = adapter._extract_arxiv_id(entry)

        assert arxiv_id == "2401.12345v1"

    def test_extract_doi_from_link(self) -> None:
        """_extract_doi extracts DOI from link."""
        atom = """<?xml version="1.0" encoding="UTF-8"?>
        <entry xmlns="http://www.w3.org/2005/Atom">
            <link href="http://dx.doi.org/10.1234/test" title="doi"/>
        </entry>
        """
        entry = ElementTree.fromstring(atom.encode("utf-8"))
        adapter = ArxivAdapter()

        doi = adapter._extract_doi(entry)

        assert doi == "10.1234/test"

    def test_parse_authors_handles_various_formats(self) -> None:
        """_parse_authors handles various name formats."""
        atom = """<?xml version="1.0" encoding="UTF-8"?>
        <entry xmlns="http://www.w3.org/2005/Atom">
            <author><name>John Smith</name></author>
            <author><name>Jane A. Jones</name></author>
            <author><name>SingleName</name></author>
        </entry>
        """
        entry = ElementTree.fromstring(atom.encode("utf-8"))
        adapter = ArxivAdapter()

        authors = adapter._parse_authors(entry)

        assert len(authors) == 3
        assert authors[0].last_name == "Smith"
        assert authors[0].first_name == "John"
        assert authors[1].last_name == "Jones"
        assert authors[1].first_name == "Jane A."
        assert authors[2].last_name == "SingleName"
        assert authors[2].first_name == "Unknown"

    def test_extract_year_from_published(self) -> None:
        """_extract_year extracts year from published date."""
        atom = """<published xmlns="http://www.w3.org/2005/Atom">2023-12-01T15:30:00Z</published>"""
        published_elem = ElementTree.fromstring(atom.encode("utf-8"))
        adapter = ArxivAdapter()

        year = adapter._extract_year(published_elem)

        assert year == 2023

    def test_extract_year_handles_malformed_date(self) -> None:
        """_extract_year handles malformed dates."""
        atom = """<published xmlns="http://www.w3.org/2005/Atom">invalid</published>"""
        published_elem = ElementTree.fromstring(atom.encode("utf-8"))
        adapter = ArxivAdapter()

        year = adapter._extract_year(published_elem)

        assert year == 2024

    def test_extract_primary_category(self) -> None:
        """_extract_primary_category extracts primary category."""
        atom = """<?xml version="1.0" encoding="UTF-8"?>
        <entry xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
            <arxiv:primary_category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
        </entry>
        """
        entry = ElementTree.fromstring(atom.encode("utf-8"))
        adapter = ArxivAdapter()

        journal = adapter._extract_primary_category(entry)

        assert journal == "arXiv:cs.LG"

    def test_extract_categories_limits_to_ten(self) -> None:
        """_extract_categories limits result to 10 categories."""
        categories = "".join(
            [
                f'<category term="cat{i}" scheme="http://arxiv.org/schemas/atom" xmlns="http://www.w3.org/2005/Atom"/>'
                for i in range(15)
            ]
        )
        atom = f"""<?xml version="1.0" encoding="UTF-8"?>
        <entry xmlns="http://www.w3.org/2005/Atom">
            {categories}
        </entry>
        """
        entry = ElementTree.fromstring(atom.encode("utf-8"))
        adapter = ArxivAdapter()

        keywords = adapter._extract_categories(entry)

        assert len(keywords) == 10


@pytest.mark.integration
class TestArxivAdapterIntegration:
    """Integration tests for ArXiv API (requires network)."""

    def test_real_arxiv_search(self) -> None:
        """search performs real ArXiv query (integration test)."""
        adapter = ArxivAdapter()
        papers = adapter.search("machine learning", limit=5)

        assert len(papers) > 0
        assert all(paper.title for paper in papers)
        assert all(paper.authors for paper in papers)
        assert all(paper.doi.value for paper in papers)
        # Check for ArXiv ID format or DOI
        assert all(
            paper.doi.value.startswith("arXiv:") or "." in paper.doi.value for paper in papers
        )
