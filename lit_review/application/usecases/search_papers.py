"""Search papers use case for querying academic databases.

Orchestrates searching across multiple academic databases and
deduplicates results by DOI.
"""

from dataclasses import dataclass, field

from lit_review.application.ports.search_service import SearchService
from lit_review.domain.entities.paper import Paper


@dataclass
class SearchPapersUseCase:
    """Use case for searching papers across multiple databases.

    Coordinates searches across configured search services and
    deduplicates results by DOI to prevent duplicate papers.

    Attributes:
        services: Dictionary mapping service names to SearchService instances.

    Example:
        >>> use_case = SearchPapersUseCase(services={
        ...     "crossref": CrossrefAdapter(),
        ...     "pubmed": PubMedAdapter(),
        ... })
        >>> papers = use_case.execute("machine learning healthcare")
    """

    services: dict[str, SearchService] = field(default_factory=dict)

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
        """Execute search across databases with deduplication.

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
            services_to_use = list(self.services.values())
        else:
            services_to_use = [self.services[name] for name in databases if name in self.services]

        if not services_to_use:
            return []

        # Collect results from all services
        all_papers: list[Paper] = []
        for service in services_to_use:
            try:
                papers = service.search(query, limit=limit)
                all_papers.extend(papers)
            except (ConnectionError, TimeoutError):
                # Log and continue with other services
                continue

        # Deduplicate by DOI
        unique_papers = self._deduplicate_by_doi(all_papers)
        return unique_papers

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
