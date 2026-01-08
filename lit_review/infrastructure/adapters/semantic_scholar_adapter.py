# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Semantic Scholar API adapter for searching academic papers.

Implements the SearchService port for Semantic Scholar with rate limiting,
citation count metadata, and JSON parsing.
"""

import time
from typing import Any

import httpx

from lit_review.application.ports.search_service import SearchService
from lit_review.domain.entities.paper import Paper
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


class SemanticScholarAdapter(SearchService):
    """Semantic Scholar API adapter with rate limiting.

    Implements rate-limited Semantic Scholar searches using the public API.
    Respects rate limits: 100 requests per 5 minutes (1 request per 3 seconds).

    Attributes:
        base_url: Semantic Scholar API base URL.
        rate_limit: Minimum seconds between requests.
        timeout: Request timeout in seconds.
        max_retries: Maximum retry attempts.
        api_key: Optional API key for higher rate limits.

    Example:
        >>> adapter = SemanticScholarAdapter()
        >>> papers = adapter.search("machine learning", limit=10)
    """

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit: float = 3.0,
        api_key: str | None = None,
    ) -> None:
        """Initialize Semantic Scholar adapter.

        Args:
            timeout: Request timeout in seconds.
            max_retries: Maximum retry attempts.
            rate_limit: Minimum seconds between requests (default 3.0).
            api_key: Optional API key for higher rate limits.
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limit = rate_limit
        self.api_key = api_key
        self._last_request_time = 0.0

    def _rate_limit_sleep(self) -> None:
        """Sleep to respect rate limits."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self._last_request_time = time.time()

    def search(self, query: str, limit: int = 100) -> list[Paper]:
        """Search Semantic Scholar for papers matching query.

        Args:
            query: Search query string.
            limit: Maximum number of results.

        Returns:
            List of Paper entities from search results.

        Raises:
            ConnectionError: If unable to connect to Semantic Scholar.
            TimeoutError: If request times out.
        """
        # Semantic Scholar search endpoint
        url = f"{self.BASE_URL}/paper/search"

        params = {
            "query": query,
            "limit": min(limit, 100),  # API max is 100 per request
            "fields": "paperId,externalIds,title,authors,year,venue,abstract,citationCount",
        }

        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        # Retry with exponential backoff
        for attempt in range(self.max_retries):
            try:
                self._rate_limit_sleep()

                with httpx.Client(timeout=self.timeout) as client:
                    response = client.get(url, params=params, headers=headers)
                    response.raise_for_status()

                return self._parse_response(response.json())

            except httpx.TimeoutException:
                if attempt == self.max_retries - 1:
                    raise TimeoutError(
                        f"Semantic Scholar request timed out after {self.max_retries} attempts"
                    )
                time.sleep(2**attempt)
            except httpx.HTTPError as e:
                if attempt == self.max_retries - 1:
                    raise ConnectionError(f"Semantic Scholar request failed: {e}") from e
                time.sleep(2**attempt)

        return []

    def _parse_response(self, data: dict[str, Any]) -> list[Paper]:
        """Parse Semantic Scholar API response to Paper entities.

        Args:
            data: JSON response from Semantic Scholar API.

        Returns:
            List of Paper entities.
        """
        papers: list[Paper] = []
        items = data.get("data", [])

        for item in items:
            try:
                paper = self._item_to_paper(item)
                if paper:
                    papers.append(paper)
            except Exception:
                # Skip malformed entries
                continue

        return papers

    def _item_to_paper(self, item: dict[str, Any]) -> Paper | None:
        """Convert Semantic Scholar item to Paper entity.

        Args:
            item: Single Semantic Scholar result item.

        Returns:
            Paper entity or None if required fields missing.
        """
        # Title (required)
        title = item.get("title")
        if not title:
            return None

        # DOI (try multiple sources, fallback to S2 paper ID)
        doi_value = self._extract_doi(item)
        if not doi_value:
            return None

        # Authors
        authors = self._parse_authors(item.get("authors", []))
        if not authors:
            authors = [Author("Unknown", "Author", "U.")]

        # Publication year
        year = item.get("year")
        if not year or not isinstance(year, int):
            year = 2024

        # Venue (journal/conference)
        venue = item.get("venue")
        journal = venue if venue else "Unknown Journal"

        # Abstract
        abstract = item.get("abstract", "")

        # Citation count as metadata (stored in keywords for now)
        keywords: list[str] = []
        citation_count = item.get("citationCount")
        if citation_count is not None:
            keywords.append(f"citations:{citation_count}")

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

    def _extract_doi(self, item: dict[str, Any]) -> str | None:
        """Extract DOI from item, with Semantic Scholar ID fallback.

        Args:
            item: Semantic Scholar result item.

        Returns:
            DOI string or S2 paper ID as fallback, or None if neither found.
        """
        # Try DOI from externalIds
        external_ids = item.get("externalIds", {})
        if external_ids and isinstance(external_ids, dict):
            doi = external_ids.get("DOI")
            if doi:
                return doi

            # Try ArXiv ID
            arxiv_id = external_ids.get("ArXiv")
            if arxiv_id:
                return f"10.48550/arXiv.{arxiv_id}"

        # Fallback to Semantic Scholar paper ID
        paper_id = item.get("paperId")
        if paper_id:
            return f"10.58121/S2.{paper_id}"

        return None

    def _parse_authors(self, author_list: list[dict[str, Any]]) -> list[Author]:
        """Parse Semantic Scholar author list to Author value objects.

        Args:
            author_list: List of author dicts from Semantic Scholar.

        Returns:
            List of Author value objects.
        """
        authors: list[Author] = []

        for author_data in author_list:
            name = author_data.get("name")
            if not name:
                continue

            # Parse "First Last" or "Last, First" format
            if "," in name:
                # "Last, First" format
                parts = name.split(",", 1)
                last_name = parts[0].strip()
                first_name = parts[1].strip() if len(parts) > 1 else "Unknown"
            else:
                # "First Last" format
                name_parts = name.strip().split()
                if len(name_parts) == 0:
                    continue
                elif len(name_parts) == 1:
                    last_name = name_parts[0]
                    first_name = "Unknown"
                else:
                    last_name = name_parts[-1]
                    first_name = " ".join(name_parts[:-1])

            # Generate initials
            if first_name and first_name != "Unknown":
                initials = ".".join(p[0].upper() for p in first_name.split() if p) + "."
            else:
                initials = "U."

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

    def get_service_name(self) -> str:
        """Return service name."""
        return "Semantic Scholar"
