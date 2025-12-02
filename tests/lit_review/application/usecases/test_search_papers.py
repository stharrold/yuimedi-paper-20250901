"""Tests for SearchPapersUseCase."""


from lit_review.application.ports.search_service import SearchService
from lit_review.application.usecases.search_papers import SearchPapersUseCase
from lit_review.domain.entities.paper import Paper
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


class MockSearchService(SearchService):
    """Mock search service for testing."""

    def __init__(self, name: str, papers: list[Paper] | None = None) -> None:
        self._name = name
        self._papers = papers or []
        self._should_fail = False

    def search(self, query: str, limit: int = 100) -> list[Paper]:
        if self._should_fail:
            raise ConnectionError("Mock connection error")
        return self._papers[:limit]

    def get_service_name(self) -> str:
        return self._name

    def set_should_fail(self, fail: bool) -> None:
        self._should_fail = fail


def create_paper(doi_suffix: str) -> Paper:
    """Helper to create a test paper."""
    return Paper(
        doi=DOI(f"10.1234/{doi_suffix}"),
        title=f"Paper {doi_suffix}",
        authors=[Author("Smith", "John", "J.")],
        publication_year=2024,
        journal="Test Journal",
    )


class TestSearchPapersUseCase:
    """Tests for SearchPapersUseCase."""

    def test_execute_with_no_services_returns_empty(self) -> None:
        """Execute with no services returns empty list."""
        use_case = SearchPapersUseCase()
        results = use_case.execute("test query")
        assert results == []

    def test_execute_with_single_service(self) -> None:
        """Execute with single service returns its results."""
        papers = [create_paper("test1"), create_paper("test2")]
        service = MockSearchService("crossref", papers)
        use_case = SearchPapersUseCase(services={"crossref": service})

        results = use_case.execute("test query")
        assert len(results) == 2

    def test_execute_with_multiple_services(self) -> None:
        """Execute with multiple services combines results."""
        papers1 = [create_paper("service1-paper1")]
        papers2 = [create_paper("service2-paper1")]
        service1 = MockSearchService("crossref", papers1)
        service2 = MockSearchService("pubmed", papers2)

        use_case = SearchPapersUseCase(
            services={
                "crossref": service1,
                "pubmed": service2,
            }
        )

        results = use_case.execute("test query")
        assert len(results) == 2

    def test_execute_deduplicates_by_doi(self) -> None:
        """Execute deduplicates papers with same DOI from different services."""
        paper1 = create_paper("duplicate")
        paper2 = create_paper("duplicate")  # Same DOI
        paper3 = create_paper("unique")

        service1 = MockSearchService("crossref", [paper1, paper3])
        service2 = MockSearchService("pubmed", [paper2])

        use_case = SearchPapersUseCase(
            services={
                "crossref": service1,
                "pubmed": service2,
            }
        )

        results = use_case.execute("test query")
        assert len(results) == 2  # duplicate removed

    def test_execute_with_specific_databases(self) -> None:
        """Execute with specific databases only searches those."""
        papers1 = [create_paper("crossref-paper")]
        papers2 = [create_paper("pubmed-paper")]
        service1 = MockSearchService("crossref", papers1)
        service2 = MockSearchService("pubmed", papers2)

        use_case = SearchPapersUseCase(
            services={
                "crossref": service1,
                "pubmed": service2,
            }
        )

        results = use_case.execute("test query", databases=["crossref"])
        assert len(results) == 1
        assert results[0].doi.value == "10.1234/crossref-paper"

    def test_execute_with_unknown_database_ignores_it(self) -> None:
        """Execute with unknown database name ignores it gracefully."""
        papers = [create_paper("test")]
        service = MockSearchService("crossref", papers)
        use_case = SearchPapersUseCase(services={"crossref": service})

        results = use_case.execute("test query", databases=["unknown"])
        assert results == []

    def test_execute_continues_on_service_failure(self) -> None:
        """Execute continues if one service fails."""
        papers1 = [create_paper("success")]
        service1 = MockSearchService("crossref", papers1)
        service2 = MockSearchService("pubmed", [])
        service2.set_should_fail(True)

        use_case = SearchPapersUseCase(
            services={
                "crossref": service1,
                "pubmed": service2,
            }
        )

        results = use_case.execute("test query")
        assert len(results) == 1  # Only crossref results

    def test_execute_respects_limit(self) -> None:
        """Execute respects the limit parameter."""
        papers = [create_paper(f"paper{i}") for i in range(10)]
        service = MockSearchService("crossref", papers)
        use_case = SearchPapersUseCase(services={"crossref": service})

        results = use_case.execute("test query", limit=5)
        assert len(results) == 5

    def test_add_service(self) -> None:
        """add_service adds a service to the use case."""
        use_case = SearchPapersUseCase()
        service = MockSearchService("crossref", [])
        use_case.add_service("crossref", service)

        assert "crossref" in use_case.get_available_databases()

    def test_get_available_databases(self) -> None:
        """get_available_databases returns configured service names."""
        service1 = MockSearchService("crossref", [])
        service2 = MockSearchService("pubmed", [])

        use_case = SearchPapersUseCase(
            services={
                "crossref": service1,
                "pubmed": service2,
            }
        )

        databases = use_case.get_available_databases()
        assert set(databases) == {"crossref", "pubmed"}
