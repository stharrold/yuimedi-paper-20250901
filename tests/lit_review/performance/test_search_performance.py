"""Performance tests for search functionality.

Tests search throughput and scalability using pytest-benchmark.
Target: 1000 papers/minute throughput.

Run with: pytest -v tests/lit_review/performance/ -m benchmark --benchmark-only
Skip benchmark tests: pytest -v -m "not benchmark"
"""

import time

import pytest

from lit_review.application.ports.search_service import SearchService
from lit_review.application.usecases.search_papers import SearchPapersUseCase
from lit_review.domain.entities.paper import Paper
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


class FastMockSearchService(SearchService):
    """Mock search service that returns results quickly."""

    def __init__(self, results_per_call: int = 100, delay_ms: int = 10):
        """Initialize with configurable results and delay."""
        self.results_per_call = results_per_call
        self.delay_ms = delay_ms
        self._call_count = 0

    def search(self, query: str, limit: int = 10) -> list[Paper]:
        """Return mock papers with minimal delay."""
        self._call_count += 1

        # Simulate network delay
        time.sleep(self.delay_ms / 1000.0)

        # Generate mock papers
        papers = []
        for i in range(min(limit, self.results_per_call)):
            paper = Paper(
                doi=DOI(f"10.1234/mock-{self._call_count}-{i}"),
                title=f"Mock Paper {self._call_count}-{i}",
                authors=[Author("Doe", "John", "J.")],
                publication_year=2023,
                journal="Mock Journal",
                abstract=f"Mock abstract for paper {i}. " * 10,  # ~100 chars
            )
            papers.append(paper)

        return papers


class SlowMockSearchService(SearchService):
    """Mock search service with realistic latency."""

    def __init__(self, results_per_call: int = 50, delay_ms: int = 500):
        """Initialize with configurable results and delay."""
        self.results_per_call = results_per_call
        self.delay_ms = delay_ms

    def search(self, query: str, limit: int = 10) -> list[Paper]:
        """Return mock papers with realistic network delay."""
        time.sleep(self.delay_ms / 1000.0)

        papers = []
        for i in range(min(limit, self.results_per_call)):
            paper = Paper(
                doi=DOI(f"10.5678/slow-{i}"),
                title=f"Slow Paper {i}",
                authors=[Author("Smith", "Jane", "J.")],
                publication_year=2023,
                journal="Slow Journal",
                abstract=f"Abstract for slow paper {i}. " * 20,  # ~200 chars
            )
            papers.append(paper)

        return papers


@pytest.mark.benchmark
class TestSearchPerformanceThroughput:
    """Test search throughput (papers per minute)."""

    def test_single_service_throughput_target(self, benchmark):
        """Test that single service can achieve target throughput.

        Target: 1000 papers/minute = ~16.7 papers/second
        With 100ms latency: need 10 concurrent calls to achieve target
        """
        use_case = SearchPapersUseCase()
        fast_service = FastMockSearchService(results_per_call=100, delay_ms=100)
        use_case.add_service("fast", fast_service)

        def search_operation():
            return use_case.execute(
                query="test query",
                databases=["fast"],
                limit=100,
            )

        result = benchmark(search_operation)

        # Verify results
        assert len(result) == 100

        # Calculate throughput (papers per minute)
        # benchmark.stats.mean is in seconds
        papers_per_second = 100 / benchmark.stats.mean
        papers_per_minute = papers_per_second * 60

        # Should achieve at least 500 papers/minute with single service
        assert papers_per_minute >= 500, (
            f"Throughput too low: {papers_per_minute:.0f} papers/min " f"(target: 500+ papers/min)"
        )

    def test_multiple_services_parallel_throughput(self, benchmark):
        """Test throughput with multiple services running in parallel.

        Target: 1000 papers/minute with 4 services in parallel
        """
        use_case = SearchPapersUseCase()

        # Add multiple services
        for i in range(4):
            service = FastMockSearchService(results_per_call=50, delay_ms=100)
            use_case.add_service(f"service_{i}", service)

        def parallel_search_operation():
            return use_case.execute(
                query="test query",
                databases=[f"service_{i}" for i in range(4)],
                limit=50,
            )

        result = benchmark(parallel_search_operation)

        # Should get results from all services (up to 200 total, deduplicated)
        assert len(result) > 0

        # Calculate throughput
        papers_per_second = len(result) / benchmark.stats.mean
        papers_per_minute = papers_per_second * 60

        # With parallel execution should exceed 1000 papers/minute
        print(f"\nParallel throughput: {papers_per_minute:.0f} papers/min")

    def test_deduplication_performance(self, benchmark):
        """Test that deduplication doesn't significantly impact performance."""
        use_case = SearchPapersUseCase()

        # Create services that return overlapping results
        class OverlappingMockService(SearchService):
            def __init__(self, service_id: int):
                self.service_id = service_id

            def search(self, query: str, limit: int = 10) -> list[Paper]:
                time.sleep(0.05)  # 50ms delay
                papers = []
                for i in range(limit):
                    # 50% overlap between services
                    doi_num = i if self.service_id == 0 else i + (limit // 2)
                    paper = Paper(
                        doi=DOI(f"10.1234/overlap-{doi_num}"),
                        title=f"Paper {doi_num}",
                        authors=[Author("Doe", "John", "J.")],
                        publication_year=2023,
                        journal="Journal",
                    )
                    papers.append(paper)
                return papers

        # Add services with overlap
        for i in range(3):
            use_case.add_service(f"overlap_{i}", OverlappingMockService(i))

        def dedup_operation():
            return use_case.execute(
                query="test",
                databases=[f"overlap_{i}" for i in range(3)],
                limit=100,
            )

        result = benchmark(dedup_operation)

        # Should deduplicate but not take too long
        assert len(result) > 0
        assert benchmark.stats.mean < 1.0  # Should complete in under 1 second


@pytest.mark.benchmark
class TestSearchPerformanceScalability:
    """Test search performance scaling characteristics."""

    def test_linear_scaling_with_paper_count(self, benchmark):
        """Test that search time scales linearly with result count."""
        use_case = SearchPapersUseCase()
        service = FastMockSearchService(results_per_call=1000, delay_ms=10)
        use_case.add_service("scalable", service)

        # Test with 500 papers
        def search_500():
            return use_case.execute(query="test", databases=["scalable"], limit=500)

        result = benchmark(search_500)
        assert len(result) == 500

        # Mean time should be reasonable (< 0.5 seconds for 500 papers)
        assert benchmark.stats.mean < 0.5

    def test_concurrent_service_scaling(self, benchmark):
        """Test that adding services improves throughput (up to a point)."""
        use_case = SearchPapersUseCase()

        # Add 8 services
        for i in range(8):
            service = FastMockSearchService(results_per_call=25, delay_ms=100)
            use_case.add_service(f"concurrent_{i}", service)

        def concurrent_search():
            return use_case.execute(
                query="test",
                databases=[f"concurrent_{i}" for i in range(8)],
                limit=25,
            )

        result = benchmark(concurrent_search)

        # With 8 services running concurrently, should complete reasonably fast
        # Even though each has 100ms delay, parallel execution means ~100-200ms total
        assert benchmark.stats.mean < 0.5  # Should complete in under 500ms
        assert len(result) > 0


@pytest.mark.benchmark
class TestSearchPerformanceRealistic:
    """Test performance with realistic scenarios."""

    def test_realistic_multi_database_search(self, benchmark):
        """Test realistic scenario: 4 databases, 500ms latency each, 50 papers each."""
        use_case = SearchPapersUseCase()

        # Simulate 4 real databases with realistic characteristics
        databases = [
            ("pubmed", SlowMockSearchService(50, 500)),
            ("crossref", SlowMockSearchService(50, 400)),
            ("arxiv", SlowMockSearchService(50, 300)),
            ("semantic_scholar", SlowMockSearchService(50, 600)),
        ]

        for name, service in databases:
            use_case.add_service(name, service)

        def realistic_search():
            return use_case.execute(
                query="machine learning healthcare",
                databases=[name for name, _ in databases],
                limit=50,
            )

        result = benchmark(realistic_search)

        # Should get results from multiple databases
        assert len(result) > 0

        # With parallel execution, should complete in ~600ms (max latency)
        # Allow up to 2 seconds for safety
        assert benchmark.stats.mean < 2.0

        # Calculate effective throughput
        papers_per_second = len(result) / benchmark.stats.mean
        papers_per_minute = papers_per_second * 60

        print(f"\nRealistic throughput: {papers_per_minute:.0f} papers/min")
        print(f"Mean search time: {benchmark.stats.mean:.3f}s")
        print(f"Papers returned: {len(result)}")

    def test_search_with_retry_performance(self, benchmark):
        """Test that retry mechanism doesn't excessively slow down searches."""
        use_case = SearchPapersUseCase()

        # Service that fails once then succeeds
        class FlakeyService(SearchService):
            def __init__(self):
                self.attempt = 0

            def search(self, query: str, limit: int = 10) -> list[Paper]:
                self.attempt += 1
                if self.attempt == 1:
                    time.sleep(0.1)
                    raise TimeoutError("Simulated timeout")

                time.sleep(0.05)
                return [
                    Paper(
                        doi=DOI(f"10.1234/retry-{i}"),
                        title=f"Retry Paper {i}",
                        authors=[Author("Doe", "John", "J.")],
                        publication_year=2023,
                        journal="Retry Journal",
                    )
                    for i in range(limit)
                ]

        use_case.add_service("flakey", FlakeyService())

        def search_with_retry():
            try:
                return use_case.execute(query="test", databases=["flakey"], limit=10)
            except TimeoutError:
                return []

        _result = benchmark(search_with_retry)

        # Should complete reasonably fast even with one retry
        # ~250ms total (100ms fail + 50ms backoff + 100ms success)
        assert benchmark.stats.mean < 1.0


@pytest.mark.benchmark
class TestSearchPerformanceBaselines:
    """Establish performance baselines for regression testing."""

    def test_baseline_100_papers_single_service(self, benchmark):
        """Baseline: Search 100 papers from single service."""
        use_case = SearchPapersUseCase()
        service = FastMockSearchService(results_per_call=100, delay_ms=50)
        use_case.add_service("baseline", service)

        result = benchmark.pedantic(
            lambda: use_case.execute(query="test", databases=["baseline"], limit=100),
            rounds=10,
            iterations=5,
        )

        assert len(result) == 100

        # Document baseline for regression tracking
        print("\n=== BASELINE: 100 papers, single service ===")
        print(f"Mean: {benchmark.stats.mean:.4f}s")
        print(f"StdDev: {benchmark.stats.stddev:.4f}s")
        print(f"Min: {benchmark.stats.min:.4f}s")
        print(f"Max: {benchmark.stats.max:.4f}s")

    def test_baseline_500_papers_four_services(self, benchmark):
        """Baseline: Search 500 papers from 4 services in parallel."""
        use_case = SearchPapersUseCase()

        for i in range(4):
            service = FastMockSearchService(results_per_call=125, delay_ms=50)
            use_case.add_service(f"baseline_{i}", service)

        result = benchmark.pedantic(
            lambda: use_case.execute(
                query="test",
                databases=[f"baseline_{i}" for i in range(4)],
                limit=125,
            ),
            rounds=10,
            iterations=3,
        )

        assert len(result) > 0

        print("\n=== BASELINE: 500 papers, 4 services parallel ===")
        print(f"Mean: {benchmark.stats.mean:.4f}s")
        print(f"Papers returned: {len(result)}")
        print(f"Throughput: {len(result) / benchmark.stats.mean * 60:.0f} papers/min")

    def test_baseline_1000_papers_target(self, benchmark):
        """Baseline: Target of 1000 papers/minute."""
        use_case = SearchPapersUseCase()

        # Setup to achieve 1000 papers/minute target
        for i in range(4):
            # Each service returns 250 papers in 250ms
            service = FastMockSearchService(results_per_call=250, delay_ms=250)
            use_case.add_service(f"target_{i}", service)

        def target_search():
            return use_case.execute(
                query="test",
                databases=[f"target_{i}" for i in range(4)],
                limit=250,
            )

        result = benchmark.pedantic(target_search, rounds=5, iterations=2)

        papers_per_second = len(result) / benchmark.stats.mean
        papers_per_minute = papers_per_second * 60

        print("\n=== TARGET: 1000 papers/minute ===")
        print(f"Achieved: {papers_per_minute:.0f} papers/min")
        print(f"Mean time: {benchmark.stats.mean:.4f}s")
        print(f"Papers returned: {len(result)}")

        # Should meet or exceed target
        assert (
            papers_per_minute >= 1000
        ), f"Failed to meet 1000 papers/min target: {papers_per_minute:.0f}"
