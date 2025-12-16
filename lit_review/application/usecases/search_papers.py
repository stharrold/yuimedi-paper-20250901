# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Search papers use case for querying academic databases.

Orchestrates searching across multiple academic databases and
deduplicates results by DOI with parallel execution.
"""

import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
from dataclasses import dataclass, field
from typing import Any

from lit_review.application.ports.search_service import SearchService
from lit_review.domain.entities.paper import Paper


@dataclass
class SearchPapersUseCase:
    """Use case for searching papers across multiple databases.

    Coordinates searches across configured search services with parallel execution,
    deduplicates results by DOI to prevent duplicate papers, and handles errors
    with exponential backoff.

    Attributes:
        services: Dictionary mapping service names to SearchService instances.
        max_workers: Maximum number of parallel search threads.
        timeout_per_database: Timeout in seconds for each database search.
        max_retries: Maximum number of retry attempts for failed searches.

    Example:
        >>> use_case = SearchPapersUseCase(services={
        ...     "crossref": CrossrefAdapter(),
        ...     "pubmed": PubMedAdapter(),
        ... })
        >>> papers = use_case.execute("machine learning healthcare")
    """

    services: dict[str, SearchService] = field(default_factory=dict)
    max_workers: int = 4
    timeout_per_database: float = 30.0
    max_retries: int = 3

    def add_service(self, name: str, service: SearchService) -> None:
        """Add a search service.

        Args:
            name: Service identifier.
            service: SearchService implementation.
        """
        self.services[name] = service

    def execute(
        self,
        query: str,
        databases: list[str] | None = None,
        limit: int = 100,
    ) -> list[Paper]:
        """Execute search across databases with parallel execution and deduplication.

        Searches multiple databases in parallel using ThreadPoolExecutor.
        Implements timeout per database and exponential backoff for retries.
        Returns partial results if some databases fail.

        Args:
            query: Search query string.
            databases: List of database names to search. If None, searches all.
            limit: Maximum results per database.

        Returns:
            List of unique Paper entities (deduplicated by DOI).
        """
        if not self.services:
            return []

        # Determine which services to use
        if databases is None:
            service_names = list(self.services.keys())
        else:
            service_names = [name for name in databases if name in self.services]

        if not service_names:
            return []

        # Execute searches in parallel
        all_papers: list[Paper] = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all search tasks
            future_to_service: dict[Any, str] = {
                executor.submit(self._search_with_retry, self.services[name], query, limit): name
                for name in service_names
            }

            # Collect results as they complete
            try:
                for future in as_completed(
                    future_to_service, timeout=self.timeout_per_database * len(service_names)
                ):
                    try:
                        papers = future.result(timeout=self.timeout_per_database)
                        all_papers.extend(papers)
                    except TimeoutError:
                        # Database search timed out, continue with other databases
                        continue
                    except Exception:
                        # Other errors, continue with partial results
                        continue
            except TimeoutError:
                # Overall timeout reached, return whatever we have
                pass

        # Deduplicate by DOI
        unique_papers = self._deduplicate_by_doi(all_papers)
        return unique_papers

    def _search_with_retry(self, service: SearchService, query: str, limit: int) -> list[Paper]:
        """Search a service with exponential backoff retry.

        Args:
            service: SearchService to query.
            query: Search query string.
            limit: Maximum results.

        Returns:
            List of papers from this service.

        Raises:
            Exception: If all retries fail.
        """
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                return service.search(query, limit=limit)
            except (ConnectionError, TimeoutError, OSError) as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    # Exponential backoff: 1s, 2s, 4s
                    wait_time = 2**attempt
                    time.sleep(wait_time)
                continue
            except Exception as e:
                # Non-retryable error
                raise e

        # All retries failed
        if last_exception:
            raise last_exception
        return []

    def _deduplicate_by_doi(self, papers: list[Paper]) -> list[Paper]:
        """Remove duplicate papers by DOI.

        Args:
            papers: List of papers (may contain duplicates).

        Returns:
            List of unique papers (first occurrence kept).
        """
        seen_dois: set[str] = set()
        unique: list[Paper] = []

        for paper in papers:
            doi_value = paper.doi.value
            if doi_value not in seen_dois:
                seen_dois.add(doi_value)
                unique.append(paper)

        return unique

    def get_available_databases(self) -> list[str]:
        """Get list of available database names.

        Returns:
            List of configured database names.
        """
        return list(self.services.keys())
