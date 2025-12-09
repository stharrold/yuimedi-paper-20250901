"""PubMed API adapter using Biopython's Entrez module.

Implements the SearchService port for PubMed with proper rate limiting,
XML parsing, and DOI fallback handling.
"""

import os
import time
from xml.etree import ElementTree

from Bio import Entrez

from lit_review.application.ports.search_service import SearchService
from lit_review.domain.entities.paper import Paper
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


class PubMedAdapter(SearchService):
    """PubMed API adapter with Entrez E-utilities.

    Implements rate-limited PubMed searches using Biopython's Entrez module.
    Respects NCBI rate limits: 3 requests/sec (10/sec with API key).

    Attributes:
        email: Email address for NCBI API (required).
        api_key: Optional NCBI API key for higher rate limits.
        rate_limit: Request rate limit (requests per second).
        timeout: Request timeout in seconds.

    Example:
        >>> adapter = PubMedAdapter(email="researcher@example.com")
        >>> papers = adapter.search("machine learning healthcare", limit=10)
    """

    def __init__(
        self,
        email: str | None = None,
        api_key: str | None = None,
        timeout: int = 30,
    ) -> None:
        """Initialize PubMed adapter.

        Args:
            email: Email address for NCBI (required by NCBI policy).
            api_key: Optional NCBI API key for higher rate limits.
            timeout: Request timeout in seconds.

        Raises:
            ValueError: If email is not provided.
        """
        self.email = email or os.environ.get("NCBI_EMAIL")
        if not self.email:
            raise ValueError(
                "Email is required for PubMed API. Set NCBI_EMAIL environment "
                "variable or pass email parameter."
            )

        self.api_key = api_key or os.environ.get("NCBI_API_KEY")
        self.timeout = timeout

        # Set rate limit based on API key presence
        self.rate_limit = 10 if self.api_key else 3  # requests per second
        self._last_request_time = 0.0

        # Configure Entrez
        Entrez.email = self.email
        if self.api_key:
            Entrez.api_key = self.api_key

    def _rate_limit_sleep(self) -> None:
        """Sleep to respect rate limits."""
        elapsed = time.time() - self._last_request_time
        min_interval = 1.0 / self.rate_limit
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self._last_request_time = time.time()

    def search(self, query: str, limit: int = 100) -> list[Paper]:
        """Search PubMed for papers matching query.

        Args:
            query: Search query string (PubMed query syntax).
            limit: Maximum number of results.

        Returns:
            List of Paper entities from search results.

        Raises:
            ConnectionError: If unable to connect to PubMed.
            TimeoutError: If request times out.
        """
        try:
            # Step 1: Search for PMIDs
            self._rate_limit_sleep()
            search_handle = Entrez.esearch(
                db="pubmed",
                term=query,
                retmax=limit,
                sort="relevance",
            )
            search_results = Entrez.read(search_handle)
            search_handle.close()

            pmids = search_results["IdList"]
            if not pmids:
                return []

            # Step 2: Fetch full records
            self._rate_limit_sleep()
            fetch_handle = Entrez.efetch(
                db="pubmed",
                id=",".join(pmids),
                retmode="xml",
            )
            records = fetch_handle.read()
            fetch_handle.close()

            # Step 3: Parse XML to Paper entities
            return self._parse_xml(records)

        except Exception as e:
            if "timeout" in str(e).lower():
                raise TimeoutError(f"PubMed request timed out: {e}") from e
            raise ConnectionError(f"PubMed request failed: {e}") from e

    def _parse_xml(self, xml_data: bytes) -> list[Paper]:
        """Parse PubMed XML response to Paper entities.

        Args:
            xml_data: XML response from Entrez.efetch.

        Returns:
            List of Paper entities.
        """
        papers: list[Paper] = []
        root = ElementTree.fromstring(xml_data)

        for article in root.findall(".//PubmedArticle"):
            try:
                paper = self._article_to_paper(article)
                if paper:
                    papers.append(paper)
            except Exception:
                # Skip malformed articles
                continue

        return papers

    def _article_to_paper(self, article: ElementTree.Element) -> Paper | None:
        """Convert PubMed article XML to Paper entity.

        Args:
            article: PubmedArticle XML element.

        Returns:
            Paper entity or None if required fields missing.
        """
        medline_citation = article.find(".//MedlineCitation")
        if medline_citation is None:
            return None

        article_elem = medline_citation.find(".//Article")
        if article_elem is None:
            return None

        # Title (required)
        title_elem = article_elem.find(".//ArticleTitle")
        if title_elem is None or not title_elem.text:
            return None
        title = title_elem.text

        # DOI (try multiple sources, fallback to PMID)
        doi_value = self._extract_doi(article, medline_citation)
        if not doi_value:
            return None

        # Authors
        authors = self._parse_authors(article_elem)
        if not authors:
            authors = [Author("Unknown", "Author", "U.")]

        # Publication year
        pub_date = article_elem.find(".//PubDate")
        year = self._extract_year(pub_date) if pub_date is not None else 2024

        # Journal
        journal_elem = article_elem.find(".//Journal/Title")
        journal = (
            journal_elem.text
            if journal_elem is not None and journal_elem.text
            else "Unknown Journal"
        )

        # Abstract
        abstract_elem = article_elem.find(".//Abstract/AbstractText")
        abstract = abstract_elem.text if abstract_elem is not None and abstract_elem.text else ""

        # Keywords (MeSH terms)
        keywords = self._extract_keywords(medline_citation)

        try:
            return Paper(
                doi=DOI(doi_value),
                title=title,
                authors=authors,
                publication_year=year,
                journal=journal,
                abstract=abstract,
                keywords=keywords,
            )
        except Exception:
            return None

    def _extract_doi(
        self,
        article: ElementTree.Element,
        medline_citation: ElementTree.Element,
    ) -> str | None:
        """Extract DOI from article, with PMID fallback.

        Args:
            article: PubmedArticle XML element.
            medline_citation: MedlineCitation XML element.

        Returns:
            DOI string or PMID as fallback, or None if neither found.
        """
        # Try ArticleIdList first (most reliable)
        article_ids = article.findall(".//ArticleId")
        for article_id in article_ids:
            if article_id.get("IdType") == "doi" and article_id.text:
                return article_id.text

        # Try ELocationID with DOI type
        elocation_ids = article.findall(".//ELocationID")
        for eloc in elocation_ids:
            if eloc.get("EIdType") == "doi" and eloc.text:
                return eloc.text

        # Fallback to PMID (PubMed ID)
        pmid_elem = medline_citation.find(".//PMID")
        if pmid_elem is not None and pmid_elem.text:
            return f"PMID:{pmid_elem.text}"

        return None

    def _parse_authors(self, article_elem: ElementTree.Element) -> list[Author]:
        """Parse PubMed author list to Author value objects.

        Args:
            article_elem: Article XML element.

        Returns:
            List of Author value objects.
        """
        authors: list[Author] = []
        author_list = article_elem.find(".//AuthorList")

        if author_list is None:
            return authors

        for author_elem in author_list.findall(".//Author"):
            try:
                last_name_elem = author_elem.find("LastName")
                fore_name_elem = author_elem.find("ForeName")
                initials_elem = author_elem.find("Initials")

                if last_name_elem is None or not last_name_elem.text:
                    continue

                last_name = last_name_elem.text
                first_name = (
                    fore_name_elem.text
                    if fore_name_elem is not None and fore_name_elem.text
                    else "Unknown"
                )
                initials = (
                    initials_elem.text if initials_elem is not None and initials_elem.text else "U."
                )

                # Ensure initials have periods
                if not initials.endswith("."):
                    initials += "."

                authors.append(
                    Author(
                        last_name=last_name,
                        first_name=first_name,
                        initials=initials,
                    )
                )
            except Exception:
                continue

        return authors

    def _extract_year(self, pub_date: ElementTree.Element) -> int:
        """Extract publication year from PubDate element.

        Args:
            pub_date: PubDate XML element.

        Returns:
            Publication year as integer.
        """
        year_elem = pub_date.find("Year")
        if year_elem is not None and year_elem.text:
            try:
                return int(year_elem.text)
            except ValueError:
                pass

        # Fallback to MedlineDate
        medline_date_elem = pub_date.find("MedlineDate")
        if medline_date_elem is not None and medline_date_elem.text:
            # Extract first 4 digits from date like "2024 Jan-Feb"
            import re

            match = re.search(r"\d{4}", medline_date_elem.text)
            if match:
                return int(match.group())

        return 2024

    def _extract_keywords(self, medline_citation: ElementTree.Element) -> list[str]:
        """Extract MeSH keywords from article.

        Args:
            medline_citation: MedlineCitation XML element.

        Returns:
            List of keyword strings.
        """
        keywords: list[str] = []

        # Extract MeSH headings
        mesh_list = medline_citation.find(".//MeshHeadingList")
        if mesh_list is not None:
            for mesh_heading in mesh_list.findall(".//MeshHeading"):
                descriptor = mesh_heading.find("DescriptorName")
                if descriptor is not None and descriptor.text:
                    keywords.append(descriptor.text)

        # Also check KeywordList
        keyword_list = medline_citation.find(".//KeywordList")
        if keyword_list is not None:
            for keyword in keyword_list.findall(".//Keyword"):
                if keyword.text and keyword.text not in keywords:
                    keywords.append(keyword.text)

        return keywords[:10]  # Limit to 10 keywords

    def get_service_name(self) -> str:
        """Return service name."""
        return "PubMed"
