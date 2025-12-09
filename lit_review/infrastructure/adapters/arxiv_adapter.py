"""ArXiv API adapter for searching preprints.

Implements the SearchService port for ArXiv with rate limiting
and ATOM feed parsing.
"""

import time
from xml.etree import ElementTree

import httpx

from lit_review.application.ports.search_service import SearchService
from lit_review.domain.entities.paper import Paper
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


class ArxivAdapter(SearchService):
    """ArXiv API adapter with rate limiting.

    Implements rate-limited ArXiv searches using the ArXiv API v2.
    Respects ArXiv rate limits: 1 request per 3 seconds.

    Attributes:
        base_url: ArXiv API base URL.
        rate_limit: Minimum seconds between requests.
        timeout: Request timeout in seconds.
        max_retries: Maximum retry attempts.

    Example:
        >>> adapter = ArxivAdapter()
        >>> papers = adapter.search("machine learning", limit=10)
    """

    BASE_URL = "http://export.arxiv.org/api/query"
    NAMESPACE = {"atom": "http://www.w3.org/2005/Atom"}

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit: float = 3.0,
    ) -> None:
        """Initialize ArXiv adapter.

        Args:
            timeout: Request timeout in seconds.
            max_retries: Maximum retry attempts.
            rate_limit: Minimum seconds between requests (default 3.0).
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limit = rate_limit
        self._last_request_time = 0.0

    def _rate_limit_sleep(self) -> None:
        """Sleep to respect rate limits."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self._last_request_time = time.time()

    def search(self, query: str, limit: int = 100) -> list[Paper]:
        """Search ArXiv for papers matching query.

        Args:
            query: Search query string (ArXiv query syntax).
            limit: Maximum number of results.

        Returns:
            List of Paper entities from search results.

        Raises:
            ConnectionError: If unable to connect to ArXiv.
            TimeoutError: If request times out.
        """
        params = {
            "search_query": query,
            "start": 0,
            "max_results": min(limit, 100),  # ArXiv recommends max 100
            "sortBy": "relevance",
            "sortOrder": "descending",
        }

        # Retry with exponential backoff
        for attempt in range(self.max_retries):
            try:
                self._rate_limit_sleep()

                with httpx.Client(timeout=self.timeout) as client:
                    response = client.get(self.BASE_URL, params=params)
                    response.raise_for_status()

                return self._parse_atom(response.content)

            except httpx.TimeoutException:
                if attempt == self.max_retries - 1:
                    raise TimeoutError(f"ArXiv request timed out after {self.max_retries} attempts")
                time.sleep(2**attempt)
            except httpx.HTTPError as e:
                if attempt == self.max_retries - 1:
                    raise ConnectionError(f"ArXiv request failed: {e}") from e
                time.sleep(2**attempt)

        return []

    def _parse_atom(self, atom_data: bytes) -> list[Paper]:
        """Parse ArXiv ATOM feed to Paper entities.

        Args:
            atom_data: ATOM XML response from ArXiv API.

        Returns:
            List of Paper entities.
        """
        papers: list[Paper] = []
        root = ElementTree.fromstring(atom_data)

        for entry in root.findall("atom:entry", self.NAMESPACE):
            try:
                paper = self._entry_to_paper(entry)
                if paper:
                    papers.append(paper)
            except Exception:
                # Skip malformed entries
                continue

        return papers

    def _entry_to_paper(self, entry: ElementTree.Element) -> Paper | None:
        """Convert ArXiv entry to Paper entity.

        Args:
            entry: ATOM entry element.

        Returns:
            Paper entity or None if required fields missing.
        """
        # Title (required)
        title_elem = entry.find("atom:title", self.NAMESPACE)
        if title_elem is None or not title_elem.text:
            return None
        title = title_elem.text.strip().replace("\n", " ")

        # ArXiv ID (used as DOI fallback)
        arxiv_id = self._extract_arxiv_id(entry)
        if not arxiv_id:
            return None

        # Try to get DOI first, fallback to ArXiv ID
        doi_value = self._extract_doi(entry) or f"arXiv:{arxiv_id}"

        # Authors
        authors = self._parse_authors(entry)
        if not authors:
            authors = [Author("Unknown", "Author", "U.")]

        # Publication year (use published date)
        published_elem = entry.find("atom:published", self.NAMESPACE)
        year = self._extract_year(published_elem) if published_elem is not None else 2024

        # Journal (use primary category)
        journal = self._extract_primary_category(entry)

        # Abstract
        summary_elem = entry.find("atom:summary", self.NAMESPACE)
        abstract = (
            summary_elem.text.strip() if summary_elem is not None and summary_elem.text else ""
        )

        # Keywords (categories)
        keywords = self._extract_categories(entry)

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

    def _extract_arxiv_id(self, entry: ElementTree.Element) -> str | None:
        """Extract ArXiv ID from entry.

        Args:
            entry: ATOM entry element.

        Returns:
            ArXiv ID or None if not found.
        """
        id_elem = entry.find("atom:id", self.NAMESPACE)
        if id_elem is None or not id_elem.text:
            return None

        # Extract ID from URL like http://arxiv.org/abs/1234.5678v1
        arxiv_id = id_elem.text.split("/abs/")[-1]
        return arxiv_id

    def _extract_doi(self, entry: ElementTree.Element) -> str | None:
        """Extract DOI from entry if present.

        Args:
            entry: ATOM entry element.

        Returns:
            DOI string or None if not found.
        """
        # Look for DOI in links
        for link in entry.findall("atom:link", self.NAMESPACE):
            title = link.get("title")
            if title == "doi":
                href = link.get("href")
                if href and "doi.org/" in href:
                    return href.split("doi.org/")[-1]
        return None

    def _parse_authors(self, entry: ElementTree.Element) -> list[Author]:
        """Parse ArXiv author list to Author value objects.

        Args:
            entry: ATOM entry element.

        Returns:
            List of Author value objects.
        """
        authors: list[Author] = []

        for author_elem in entry.findall("atom:author", self.NAMESPACE):
            name_elem = author_elem.find("atom:name", self.NAMESPACE)
            if name_elem is None or not name_elem.text:
                continue

            full_name = name_elem.text.strip()
            # Parse "First Last" or "First Middle Last"
            name_parts = full_name.split()

            if len(name_parts) == 0:
                continue
            elif len(name_parts) == 1:
                last_name = name_parts[0]
                first_name = "Unknown"
                initials = "U."
            else:
                # Last part is last name, rest is first name
                last_name = name_parts[-1]
                first_name = " ".join(name_parts[:-1])
                # Generate initials
                initials = ".".join(p[0].upper() for p in name_parts[:-1] if p) + "."

            try:
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

    def _extract_year(self, published_elem: ElementTree.Element) -> int:
        """Extract publication year from published date.

        Args:
            published_elem: Published date element.

        Returns:
            Publication year as integer.
        """
        if published_elem.text:
            # Date format: YYYY-MM-DDTHH:MM:SSZ
            try:
                year_str = published_elem.text[:4]
                return int(year_str)
            except (ValueError, IndexError):
                pass
        return 2024

    def _extract_primary_category(self, entry: ElementTree.Element) -> str:
        """Extract primary category as journal name.

        Args:
            entry: ATOM entry element.

        Returns:
            Primary category string.
        """
        primary_cat = entry.find(
            "arxiv:primary_category", {"arxiv": "http://arxiv.org/schemas/atom"}
        )
        if primary_cat is not None:
            term = primary_cat.get("term")
            if term:
                return f"arXiv:{term}"

        # Fallback to first category
        category = entry.find("atom:category", self.NAMESPACE)
        if category is not None:
            term = category.get("term")
            if term:
                return f"arXiv:{term}"

        return "arXiv"

    def _extract_categories(self, entry: ElementTree.Element) -> list[str]:
        """Extract categories as keywords.

        Args:
            entry: ATOM entry element.

        Returns:
            List of category strings.
        """
        keywords: list[str] = []

        for category in entry.findall("atom:category", self.NAMESPACE):
            term = category.get("term")
            if term and term not in keywords:
                keywords.append(term)

        return keywords[:10]  # Limit to 10 categories

    def get_service_name(self) -> str:
        """Return service name."""
        return "ArXiv"
