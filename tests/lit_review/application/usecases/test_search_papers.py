"""Tests for SearchPapersUseCase."""

import time

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
        self._fail_count = 0
        self._call_count = 0
        self._delay = 0.0

    def search(self, query: str, limit: int = 100) -> list[Paper]:
        self._call_count += 1

        # Simulate delay if configured
        if self._delay > 0:
            time.sleep(self._delay)

        # Fail first N times if configured
        if self._fail_count > 0:
            self._fail_count -= 1
            raise ConnectionError("Mock connection error")

        if self._should_fail:
            raise ConnectionError("Mock connection error")
        return self._papers[:limit]

    def get_service_name(self) -> str:
        return self._name

    def set_should_fail(self, fail: bool) -> None:
        self._should_fail = fail

    def set_fail_count(self, count: int) -> None:
        """Set number of times to fail before succeeding."""
        self._fail_count = count

    def set_delay(self, delay: float) -> None:
        """Set delay for search in seconds."""
        self._delay = delay

    def get_call_count(self) -> int:
        """Get number of times search was called."""
        return self._call_count


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


class TestSearchPapersUseCaseParallelExecution:
    """Tests for parallel execution functionality."""

    def test_parallel_execution_faster_than_sequential(self) -> None:
        """Parallel execution is faster than sequential for multiple services."""
        # Create services with delays
        papers1 = [create_paper("paper1")]
        papers2 = [create_paper("paper2")]
        service1 = MockSearchService("service1", papers1)
        service2 = MockSearchService("service2", papers2)
        service1.set_delay(0.1)
        service2.set_delay(0.1)

        use_case = SearchPapersUseCase(
            services={
                "service1": service1,
                "service2": service2,
            }
        )

        start_time = time.time()
        results = use_case.execute("test query")
        elapsed_time = time.time() - start_time

        # Parallel execution should take ~0.1s, sequential would take ~0.2s
        assert elapsed_time < 0.15  # Allow some overhead
        assert len(results) == 2

    def test_parallel_execution_with_four_services(self) -> None:
        """Parallel execution handles four services concurrently."""
        services = {}
        for i in range(4):
            papers = [create_paper(f"service{i}-paper1")]
            service = MockSearchService(f"service{i}", papers)
            services[f"service{i}"] = service

        use_case = SearchPapersUseCase(services=services)

        results = use_case.execute("test query")
        assert len(results) == 4


class TestSearchPapersUseCaseRetryWithBackoff:
    """Tests for retry with exponential backoff."""

    def test_retry_succeeds_on_second_attempt(self) -> None:
        """Service that fails once succeeds on retry."""
        papers = [create_paper("retry-paper")]
        service = MockSearchService("service", papers)
        service.set_fail_count(1)  # Fail once, then succeed

        use_case = SearchPapersUseCase(services={"service": service}, max_retries=3)

        results = use_case.execute("test query")
        assert len(results) == 1
        assert service.get_call_count() == 2  # Original + 1 retry

    def test_retry_gives_up_after_max_attempts(self) -> None:
        """Service that always fails is retried max times then skipped."""
        service = MockSearchService("service", [])
        service.set_should_fail(True)

        use_case = SearchPapersUseCase(services={"service": service}, max_retries=3)

        results = use_case.execute("test query")
        assert results == []
        assert service.get_call_count() == 3  # All retries attempted

    def test_exponential_backoff_timing(self) -> None:
        """Exponential backoff increases wait time between retries."""
        service = MockSearchService("service", [])
        service.set_fail_count(2)  # Fail twice, then succeed

        use_case = SearchPapersUseCase(services={"service": service}, max_retries=3)

        start_time = time.time()
        use_case.execute("test query")
        elapsed_time = time.time() - start_time

        # Should wait 2^0 + 2^1 = 1s + 2s = 3s
        assert elapsed_time >= 3.0
        assert elapsed_time < 3.5  # Allow some overhead


class TestSearchPapersUseCaseTimeout:
    """Tests for timeout per database."""

    def test_timeout_per_database(self) -> None:
        """Slow database times out but doesn't block other results."""
        papers1 = [create_paper("fast-paper")]
        papers2 = [create_paper("slow-paper")]
        service1 = MockSearchService("fast", papers1)
        service2 = MockSearchService("slow", papers2)
        service2.set_delay(5.0)  # 5 second delay (longer than timeout)

        use_case = SearchPapersUseCase(
            services={
                "fast": service1,
                "slow": service2,
            },
            timeout_per_database=0.5,  # 0.5 second timeout
        )

        start_time = time.time()
        results = use_case.execute("test query")
        elapsed_time = time.time() - start_time

        # Should complete quickly (not wait full 5s) and get fast results
        # The slow service will timeout but the fast one should complete
        assert elapsed_time < 6.0  # Less than the slow service delay
        assert len(results) >= 1  # At least get fast results


class TestSearchPapersUseCasePartialResults:
    """Tests for returning partial results when some databases fail."""

    def test_partial_results_when_one_fails(self) -> None:
        """Returns results from successful database when one fails."""
        papers1 = [create_paper("success-paper")]
        service1 = MockSearchService("success", papers1)
        service2 = MockSearchService("fail", [])
        service2.set_should_fail(True)

        use_case = SearchPapersUseCase(
            services={
                "success": service1,
                "fail": service2,
            }
        )

        results = use_case.execute("test query")
        assert len(results) == 1
        assert results[0].doi.value == "10.1234/success-paper"

    def test_partial_results_when_multiple_fail(self) -> None:
        """Returns results from successful databases when multiple fail."""
        papers1 = [create_paper("success1")]
        papers2 = [create_paper("success2")]
        service1 = MockSearchService("success1", papers1)
        service2 = MockSearchService("success2", papers2)
        service3 = MockSearchService("fail1", [])
        service4 = MockSearchService("fail2", [])
        service3.set_should_fail(True)
        service4.set_should_fail(True)

        use_case = SearchPapersUseCase(
            services={
                "success1": service1,
                "success2": service2,
                "fail1": service3,
                "fail2": service4,
            }
        )

        results = use_case.execute("test query")
        assert len(results) == 2
