"""Crossref API adapter for searching academic papers.

Implements the SearchService port for the Crossref API with
rate limiting and response parsing.
"""

import os
from time import sleep

import httpx

from lit_review.application.ports.search_service import SearchService
from lit_review.domain.entities.paper import Paper
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


class CrossrefAdapter(SearchService):
    """Crossref API adapter with rate limiting.

    Searches the Crossref API for academic papers and converts
    results to Paper entities.

    Attributes:
        base_url: Crossref API base URL.
        timeout: Request timeout in seconds.
        max_retries: Maximum retry attempts on failure.

    Example:
        >>> adapter = CrossrefAdapter()
        >>> papers = adapter.search("machine learning healthcare", limit=10)
    """

    BASE_URL = "https://api.crossref.org/works"

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        email: str | None = None,
    ) -> None:
        """Initialize Crossref adapter.

        Args:
            timeout: Request timeout in seconds.
            max_retries: Maximum retry attempts.
            email: Email for polite API access (recommended).
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.email = email or os.environ.get("CROSSREF_EMAIL")

    def search(self, query: str, limit: int = 100) -> list[Paper]:
        """Search Crossref for papers matching query.

        Args:
            query: Search query string.
            limit: Maximum number of results.

        Returns:
            List of Paper entities from search results.

        Raises:
            ConnectionError: If unable to connect after retries.
            TimeoutError: If all requests timeout.
        """
        params: dict[str, str | int] = {
            "query": query,
            "rows": min(limit, 100),  # Crossref max is 100 per request
            "select": "DOI,title,author,published,container-title,abstract",
        }

        headers = {"Accept": "application/json"}
        if self.email:
            headers["User-Agent"] = f"LitReview/1.0 (mailto:{self.email})"

        # Retry with exponential backoff
        for attempt in range(self.max_retries):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.get(
                        self.BASE_URL,
                        params=params,
                        headers=headers,
                    )
                    response.raise_for_status()
                    return self._parse_response(response.json())
            except httpx.TimeoutException:
                if attempt == self.max_retries - 1:
                    raise TimeoutError(
                        f"Crossref request timed out after {self.max_retries} attempts"
                    )
                sleep(2**attempt)
            except httpx.HTTPError as e:
                if attempt == self.max_retries - 1:
                    raise ConnectionError(f"Crossref request failed: {e}") from e
                sleep(2**attempt)

        return []

    def _parse_response(self, data: dict[str, object]) -> list[Paper]:
        """Parse Crossref API response to Paper entities.

        Args:
            data: Crossref API response JSON.

        Returns:
            List of Paper entities.
        """
        papers: list[Paper] = []
        items = data.get("message", {}).get("items", [])

        for item in items:
            try:
                paper = self._item_to_paper(item)
                if paper:
                    papers.append(paper)
            except Exception:
                # Skip malformed entries
                continue

        return papers

    def _item_to_paper(self, item: dict[str, object]) -> Paper | None:
        """Convert Crossref item to Paper entity.

        Args:
            item: Single Crossref result item.

        Returns:
            Paper entity or None if required fields missing.
        """
        # Required fields
        doi_value = item.get("DOI")
        title_list = item.get("title", [])
        if not doi_value or not title_list:
            return None

        title = title_list[0] if title_list else ""

        # Authors
        authors = self._parse_authors(item.get("author", []))
        if not authors:
            # Create placeholder author if none found
            authors = [Author("Unknown", "Author", "U.")]

        # Publication year
        published = item.get("published", {})
        date_parts = published.get("date-parts", [[]])
        year = date_parts[0][0] if date_parts and date_parts[0] else 2024

        # Journal
        container = item.get("container-title", [])
        journal = container[0] if container else "Unknown Journal"

        # Optional: abstract
        abstract = item.get("abstract", "")
        # Clean HTML from abstract
        if abstract:
            abstract = self._clean_html(abstract)

        try:
            return Paper(
                doi=DOI(doi_value),
                title=title,
                authors=authors,
                publication_year=year,
                journal=journal,
                abstract=abstract,
            )
        except Exception:
            return None

    def _parse_authors(self, author_list: list[dict[str, object]]) -> list[Author]:
        """Parse Crossref author list to Author value objects.

        Args:
            author_list: List of author dicts from Crossref.

        Returns:
            List of Author value objects.
        """
        authors: list[Author] = []

        for author_data in author_list:
            family = author_data.get("family", "")
            given = author_data.get("given", "")

            if not family:
                continue

            # Generate initials from given name
            initials = ""
            if given:
                parts = given.split()
                initials = ".".join(p[0].upper() for p in parts if p) + "."

            try:
                authors.append(
                    Author(
                        last_name=family,
                        first_name=given or "Unknown",
                        initials=initials or "U.",
                        orcid=author_data.get("ORCID"),
                    )
                )
            except Exception:
                continue

        return authors

    def _clean_html(self, text: str) -> str:
        """Remove HTML tags from text.

        Args:
            text: Text potentially containing HTML.

        Returns:
            Clean text without HTML tags.
        """
        import re

        clean = re.sub(r"<[^>]+>", "", text)
        return clean.strip()

    def get_service_name(self) -> str:
        """Return service name."""
        return "Crossref"
