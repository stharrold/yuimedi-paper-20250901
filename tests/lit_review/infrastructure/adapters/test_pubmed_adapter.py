# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for PubMedAdapter."""

from unittest.mock import MagicMock, patch
from xml.etree import ElementTree

import pytest

from lit_review.infrastructure.adapters.pubmed_adapter import PubMedAdapter


@pytest.fixture
def mock_pubmed_xml() -> bytes:
    """Return mock PubMed XML response."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <PubmedArticleSet>
        <PubmedArticle>
            <MedlineCitation>
                <PMID>12345678</PMID>
                <Article>
                    <ArticleTitle>Machine Learning in Healthcare Diagnosis</ArticleTitle>
                    <AuthorList>
                        <Author>
                            <LastName>Smith</LastName>
                            <ForeName>John</ForeName>
                            <Initials>J</Initials>
                        </Author>
                        <Author>
                            <LastName>Jones</LastName>
                            <ForeName>Jane</ForeName>
                            <Initials>JA</Initials>
                        </Author>
                    </AuthorList>
                    <Journal>
                        <Title>Journal of Medical AI</Title>
                    </Journal>
                    <PubDate>
                        <Year>2024</Year>
                    </PubDate>
                    <Abstract>
                        <AbstractText>This paper explores machine learning applications.</AbstractText>
                    </Abstract>
                    <ELocationID EIdType="doi">10.1234/jmai.2024.001</ELocationID>
                </Article>
                <MeshHeadingList>
                    <MeshHeading>
                        <DescriptorName>Machine Learning</DescriptorName>
                    </MeshHeading>
                    <MeshHeading>
                        <DescriptorName>Healthcare</DescriptorName>
                    </MeshHeading>
                </MeshHeadingList>
            </MedlineCitation>
            <PubmedData>
                <ArticleIdList>
                    <ArticleId IdType="doi">10.1234/jmai.2024.001</ArticleId>
                    <ArticleId IdType="pubmed">12345678</ArticleId>
                </ArticleIdList>
            </PubmedData>
        </PubmedArticle>
    </PubmedArticleSet>
    """
    return xml.encode("utf-8")


@pytest.fixture
def mock_pubmed_xml_no_doi() -> bytes:
    """Return mock PubMed XML response without DOI (PMID fallback)."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <PubmedArticleSet>
        <PubmedArticle>
            <MedlineCitation>
                <PMID>87654321</PMID>
                <Article>
                    <ArticleTitle>Paper Without DOI</ArticleTitle>
                    <AuthorList>
                        <Author>
                            <LastName>Wilson</LastName>
                            <ForeName>Bob</ForeName>
                            <Initials>B</Initials>
                        </Author>
                    </AuthorList>
                    <Journal>
                        <Title>Old Journal</Title>
                    </Journal>
                    <PubDate>
                        <Year>2020</Year>
                    </PubDate>
                </Article>
            </MedlineCitation>
        </PubmedArticle>
    </PubmedArticleSet>
    """
    return xml.encode("utf-8")


@pytest.mark.integration
class TestPubMedAdapter:
    """Tests for PubMedAdapter (integration - mocked HTTP)."""

    def test_init_requires_email(self) -> None:
        """__init__ raises ValueError if no email provided."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                PubMedAdapter()
            assert "Email is required" in str(exc_info.value)

    def test_init_uses_env_email(self) -> None:
        """__init__ uses NCBI_EMAIL from environment."""
        with patch.dict("os.environ", {"NCBI_EMAIL": "test@example.com"}):
            adapter = PubMedAdapter()
            assert adapter.email == "test@example.com"

    def test_init_sets_rate_limit_with_api_key(self) -> None:
        """__init__ sets higher rate limit when API key present."""
        adapter = PubMedAdapter(email="test@example.com", api_key="test_key")
        assert adapter.rate_limit == 10

    def test_init_sets_rate_limit_without_api_key(self) -> None:
        """__init__ sets default rate limit without API key."""
        adapter = PubMedAdapter(email="test@example.com")
        assert adapter.rate_limit == 3

    def test_get_service_name(self) -> None:
        """get_service_name returns 'PubMed'."""
        adapter = PubMedAdapter(email="test@example.com")
        assert adapter.get_service_name() == "PubMed"

    @patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.esearch")
    @patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.efetch")
    def test_search_returns_papers(
        self,
        mock_efetch: MagicMock,
        mock_esearch: MagicMock,
        mock_pubmed_xml: bytes,
    ) -> None:
        """search returns list of Paper entities."""
        # Mock search response
        mock_search_handle = MagicMock()
        mock_search_handle.__enter__ = MagicMock(return_value=mock_search_handle)
        mock_search_handle.__exit__ = MagicMock()
        mock_esearch.return_value = mock_search_handle

        mock_search_result = {"IdList": ["12345678"]}
        with patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.read") as mock_read:
            mock_read.return_value = mock_search_result

            # Mock fetch response
            mock_fetch_handle = MagicMock()
            mock_fetch_handle.read.return_value = mock_pubmed_xml
            mock_fetch_handle.close.return_value = None
            mock_efetch.return_value = mock_fetch_handle

            adapter = PubMedAdapter(email="test@example.com")
            papers = adapter.search("machine learning", limit=10)

            assert len(papers) == 1
            assert papers[0].title == "Machine Learning in Healthcare Diagnosis"
            assert papers[0].doi.value == "10.1234/jmai.2024.001"
            assert len(papers[0].authors) == 2
            assert papers[0].authors[0].last_name == "Smith"

    @patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.esearch")
    @patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.efetch")
    def test_search_parses_authors_correctly(
        self,
        mock_efetch: MagicMock,
        mock_esearch: MagicMock,
        mock_pubmed_xml: bytes,
    ) -> None:
        """search correctly parses author information."""
        mock_search_handle = MagicMock()
        mock_esearch.return_value = mock_search_handle

        mock_search_result = {"IdList": ["12345678"]}
        with patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.read") as mock_read:
            mock_read.return_value = mock_search_result

            mock_fetch_handle = MagicMock()
            mock_fetch_handle.read.return_value = mock_pubmed_xml
            mock_fetch_handle.close.return_value = None
            mock_efetch.return_value = mock_fetch_handle

            adapter = PubMedAdapter(email="test@example.com")
            papers = adapter.search("test")

            first_author = papers[0].authors[0]
            assert first_author.last_name == "Smith"
            assert first_author.first_name == "John"
            assert first_author.initials == "J."

            second_author = papers[0].authors[1]
            assert second_author.initials == "JA."

    @patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.esearch")
    @patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.efetch")
    def test_search_extracts_keywords(
        self,
        mock_efetch: MagicMock,
        mock_esearch: MagicMock,
        mock_pubmed_xml: bytes,
    ) -> None:
        """search extracts MeSH keywords."""
        mock_search_handle = MagicMock()
        mock_esearch.return_value = mock_search_handle

        mock_search_result = {"IdList": ["12345678"]}
        with patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.read") as mock_read:
            mock_read.return_value = mock_search_result

            mock_fetch_handle = MagicMock()
            mock_fetch_handle.read.return_value = mock_pubmed_xml
            mock_fetch_handle.close.return_value = None
            mock_efetch.return_value = mock_fetch_handle

            adapter = PubMedAdapter(email="test@example.com")
            papers = adapter.search("test")

            assert "Machine Learning" in papers[0].keywords
            assert "Healthcare" in papers[0].keywords

    @patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.esearch")
    @patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.efetch")
    def test_search_handles_missing_doi_with_pmid_fallback(
        self,
        mock_efetch: MagicMock,
        mock_esearch: MagicMock,
        mock_pubmed_xml_no_doi: bytes,
    ) -> None:
        """search uses PMID as fallback when DOI missing."""
        mock_search_handle = MagicMock()
        mock_esearch.return_value = mock_search_handle

        mock_search_result = {"IdList": ["87654321"]}
        with patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.read") as mock_read:
            mock_read.return_value = mock_search_result

            mock_fetch_handle = MagicMock()
            mock_fetch_handle.read.return_value = mock_pubmed_xml_no_doi
            mock_fetch_handle.close.return_value = None
            mock_efetch.return_value = mock_fetch_handle

            adapter = PubMedAdapter(email="test@example.com")
            papers = adapter.search("test")

            assert len(papers) == 1
            assert papers[0].doi.value == "10.9999/pubmed.87654321"

    @patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.esearch")
    def test_search_handles_empty_results(self, mock_esearch: MagicMock) -> None:
        """search handles empty results gracefully."""
        mock_search_handle = MagicMock()
        mock_esearch.return_value = mock_search_handle

        mock_search_result = {"IdList": []}
        with patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.read") as mock_read:
            mock_read.return_value = mock_search_result

            adapter = PubMedAdapter(email="test@example.com")
            papers = adapter.search("nonexistent query")

            assert papers == []

    @patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.esearch")
    def test_search_raises_connection_error_on_failure(self, mock_esearch: MagicMock) -> None:
        """search raises ConnectionError on failure."""
        mock_esearch.side_effect = Exception("Network error")

        adapter = PubMedAdapter(email="test@example.com")

        with pytest.raises(ConnectionError) as exc_info:
            adapter.search("test")

        assert "failed" in str(exc_info.value)

    @patch("lit_review.infrastructure.adapters.pubmed_adapter.Entrez.esearch")
    def test_search_raises_timeout_error(self, mock_esearch: MagicMock) -> None:
        """search raises TimeoutError on timeout."""
        mock_esearch.side_effect = Exception("timeout occurred")

        adapter = PubMedAdapter(email="test@example.com")

        with pytest.raises(TimeoutError) as exc_info:
            adapter.search("test")

        assert "timed out" in str(exc_info.value)

    @patch("lit_review.infrastructure.adapters.pubmed_adapter.time.sleep")
    def test_rate_limiting_with_api_key(self, mock_sleep: MagicMock) -> None:
        """_rate_limit_sleep respects higher rate with API key."""
        adapter = PubMedAdapter(email="test@example.com", api_key="test_key")

        # First call should not sleep
        adapter._rate_limit_sleep()
        mock_sleep.assert_not_called()

        # Immediate second call should sleep
        adapter._last_request_time = adapter._last_request_time - 0.05  # 50ms ago
        adapter._rate_limit_sleep()
        # Should sleep for ~50ms (100ms interval - 50ms elapsed)
        assert mock_sleep.call_count == 1

    @patch("lit_review.infrastructure.adapters.pubmed_adapter.time.sleep")
    def test_rate_limiting_without_api_key(self, mock_sleep: MagicMock) -> None:
        """_rate_limit_sleep respects standard rate without API key."""
        adapter = PubMedAdapter(email="test@example.com")
        assert adapter.rate_limit == 3

        # First call should not sleep
        adapter._rate_limit_sleep()
        mock_sleep.assert_not_called()


class TestPubMedAdapterParsing:
    """Tests for PubMed XML parsing."""

    def test_parse_xml_with_valid_data(self, mock_pubmed_xml: bytes) -> None:
        """_parse_xml correctly parses valid XML."""
        adapter = PubMedAdapter(email="test@example.com")
        papers = adapter._parse_xml(mock_pubmed_xml)

        assert len(papers) == 1
        assert papers[0].title == "Machine Learning in Healthcare Diagnosis"

    def test_extract_doi_from_article_id_list(self) -> None:
        """_extract_doi extracts DOI from ArticleIdList."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <PubmedArticle>
            <MedlineCitation>
                <PMID>12345678</PMID>
            </MedlineCitation>
            <PubmedData>
                <ArticleIdList>
                    <ArticleId IdType="doi">10.1234/test</ArticleId>
                </ArticleIdList>
            </PubmedData>
        </PubmedArticle>
        """
        article = ElementTree.fromstring(xml.encode("utf-8"))
        adapter = PubMedAdapter(email="test@example.com")

        medline_citation = article.find(".//MedlineCitation")
        assert medline_citation is not None
        doi = adapter._extract_doi(article, medline_citation)

        assert doi == "10.1234/test"

    def test_extract_doi_from_elocation_id(self) -> None:
        """_extract_doi extracts DOI from ELocationID."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <PubmedArticle>
            <MedlineCitation>
                <PMID>12345678</PMID>
                <Article>
                    <ELocationID EIdType="doi">10.1234/eloc</ELocationID>
                </Article>
            </MedlineCitation>
        </PubmedArticle>
        """
        article = ElementTree.fromstring(xml.encode("utf-8"))
        adapter = PubMedAdapter(email="test@example.com")

        medline_citation = article.find(".//MedlineCitation")
        assert medline_citation is not None
        doi = adapter._extract_doi(article, medline_citation)

        assert doi == "10.1234/eloc"

    def test_extract_doi_falls_back_to_pmid(self) -> None:
        """_extract_doi uses PMID when no DOI available."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <PubmedArticle>
            <MedlineCitation>
                <PMID>12345678</PMID>
            </MedlineCitation>
        </PubmedArticle>
        """
        article = ElementTree.fromstring(xml.encode("utf-8"))
        adapter = PubMedAdapter(email="test@example.com")

        medline_citation = article.find(".//MedlineCitation")
        assert medline_citation is not None
        doi = adapter._extract_doi(article, medline_citation)

        assert doi == "10.9999/pubmed.12345678"

    def test_parse_authors_handles_missing_elements(self) -> None:
        """_parse_authors handles missing name elements."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <Article>
            <AuthorList>
                <Author>
                    <LastName>Smith</LastName>
                </Author>
            </AuthorList>
        </Article>
        """
        article_elem = ElementTree.fromstring(xml.encode("utf-8"))
        adapter = PubMedAdapter(email="test@example.com")

        authors = adapter._parse_authors(article_elem)

        assert len(authors) == 1
        assert authors[0].last_name == "Smith"
        assert authors[0].first_name == "Unknown"
        assert authors[0].initials == "U."

    def test_extract_year_from_pub_date(self) -> None:
        """_extract_year extracts year from PubDate."""
        xml = """<PubDate><Year>2023</Year></PubDate>"""
        pub_date = ElementTree.fromstring(xml.encode("utf-8"))
        adapter = PubMedAdapter(email="test@example.com")

        year = adapter._extract_year(pub_date)

        assert year == 2023

    def test_extract_year_from_medline_date(self) -> None:
        """_extract_year extracts year from MedlineDate."""
        xml = """<PubDate><MedlineDate>2023 Jan-Feb</MedlineDate></PubDate>"""
        pub_date = ElementTree.fromstring(xml.encode("utf-8"))
        adapter = PubMedAdapter(email="test@example.com")

        year = adapter._extract_year(pub_date)

        assert year == 2023

    def test_extract_year_defaults_to_current(self) -> None:
        """_extract_year defaults to 2024 when no date found."""
        xml = """<PubDate></PubDate>"""
        pub_date = ElementTree.fromstring(xml.encode("utf-8"))
        adapter = PubMedAdapter(email="test@example.com")

        year = adapter._extract_year(pub_date)

        assert year == 2024

    def test_extract_keywords_from_mesh(self) -> None:
        """_extract_keywords extracts MeSH headings."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <MedlineCitation>
            <MeshHeadingList>
                <MeshHeading>
                    <DescriptorName>Keyword One</DescriptorName>
                </MeshHeading>
                <MeshHeading>
                    <DescriptorName>Keyword Two</DescriptorName>
                </MeshHeading>
            </MeshHeadingList>
        </MedlineCitation>
        """
        medline_citation = ElementTree.fromstring(xml.encode("utf-8"))
        adapter = PubMedAdapter(email="test@example.com")

        keywords = adapter._extract_keywords(medline_citation)

        assert "Keyword One" in keywords
        assert "Keyword Two" in keywords

    def test_extract_keywords_from_keyword_list(self) -> None:
        """_extract_keywords extracts from KeywordList."""
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <MedlineCitation>
            <KeywordList>
                <Keyword>Custom Keyword</Keyword>
            </KeywordList>
        </MedlineCitation>
        """
        medline_citation = ElementTree.fromstring(xml.encode("utf-8"))
        adapter = PubMedAdapter(email="test@example.com")

        keywords = adapter._extract_keywords(medline_citation)

        assert "Custom Keyword" in keywords

    def test_extract_keywords_limits_to_ten(self) -> None:
        """_extract_keywords limits result to 10 keywords."""
        mesh_headings = "".join(
            [
                f"<MeshHeading><DescriptorName>Keyword {i}</DescriptorName></MeshHeading>"
                for i in range(15)
            ]
        )
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <MedlineCitation>
            <MeshHeadingList>{mesh_headings}</MeshHeadingList>
        </MedlineCitation>
        """
        medline_citation = ElementTree.fromstring(xml.encode("utf-8"))
        adapter = PubMedAdapter(email="test@example.com")

        keywords = adapter._extract_keywords(medline_citation)

        assert len(keywords) == 10


@pytest.mark.integration
class TestPubMedAdapterIntegration:
    """Integration tests for PubMed API (requires network and credentials)."""

    def test_real_pubmed_search(self) -> None:
        """search performs real PubMed query (integration test)."""
        import os

        # Skip if credentials not available
        email = os.environ.get("NCBI_EMAIL")
        if not email:
            pytest.skip("NCBI_EMAIL not set")

        adapter = PubMedAdapter(email=email)
        papers = adapter.search("machine learning healthcare[Title]", limit=5)

        assert len(papers) > 0
        assert all(paper.title for paper in papers)
        assert all(paper.authors for paper in papers)
        # Note: Some papers may use PMID fallback
        assert all(paper.doi.value for paper in papers)
