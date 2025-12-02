"""Search service port for academic database searches.

Defines the abstract interface for search service adapters that query
academic databases like Crossref, PubMed, and ArXiv.
"""

from abc import ABC, abstractmethod

from lit_review.domain.entities.paper import Paper


class SearchService(ABC):
    """Abstract base class for academic database search services.

    Implementations should handle API communication, rate limiting,
    and conversion of search results to Paper entities.

    Example:
        >>> class CrossrefAdapter(SearchService):
        ...     def search(self, query: str, limit: int = 100) -> list[Paper]:
        ...         # Implementation
        ...         pass
    """

    @abstractmethod
    def search(self, query: str, limit: int = 100) -> list[Paper]:
        """Search for papers matching the query.

        Args:
            query: Search query string (keywords, title fragments, etc.).
            limit: Maximum number of results to return (default 100).

        Returns:
            List of Paper entities matching the query.

        Raises:
            ConnectionError: If unable to connect to the service.
            TimeoutError: If the request times out.
        """
        pass

    @abstractmethod
    def get_service_name(self) -> str:
        """Return the name of this search service.

        Returns:
            Human-readable name of the service (e.g., "Crossref", "PubMed").
        """
        pass
