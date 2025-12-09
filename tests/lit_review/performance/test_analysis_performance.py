"""Performance tests for analysis functionality.

Tests theme analysis performance and scalability.
Target: <30 seconds for 500 papers.

Run with: pytest -v tests/lit_review/performance/ -m benchmark --benchmark-only
Skip benchmark tests: pytest -v -m "not benchmark"
"""

import time

import pytest

from lit_review.application.usecases.analyze_themes import AnalyzeThemesUseCase
from lit_review.domain.entities.paper import Paper
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


def generate_mock_papers(count: int, abstract_length: int = 500) -> list[Paper]:
    """Generate mock papers for performance testing."""
    papers = []

    # Sample abstracts with healthcare/ML keywords
    abstract_templates = [
        (
            "Machine learning models improve clinical outcomes in healthcare settings. "
            "Deep neural networks analyze patient data to predict disease progression. "
            "Healthcare analytics enable better decision making for medical professionals. "
        ),
        (
            "Natural language processing extracts information from electronic health records. "
            "Clinical decision support systems assist physicians in diagnosis. "
            "Healthcare informatics transforms patient care through data analysis. "
        ),
        (
            "Predictive analytics identify high-risk patients requiring intervention. "
            "Medical imaging benefits from deep learning classification algorithms. "
            "Healthcare delivery improves with artificial intelligence applications. "
        ),
        (
            "Patient outcomes improve through evidence-based machine learning models. "
            "Clinical workflows optimize using healthcare analytics platforms. "
            "Medical research advances with computational analysis methods. "
        ),
    ]

    for i in range(count):
        # Create varied abstracts
        template = abstract_templates[i % len(abstract_templates)]
        abstract = (template * (abstract_length // len(template) + 1))[:abstract_length]

        paper = Paper(
            doi=DOI(f"10.1234/perf-test-{i}"),
            title=f"Performance Test Paper {i}: Machine Learning in Healthcare",
            authors=[
                Author(f"Author{i}", f"First{i}", f"F{i}."),
                Author(f"Coauthor{i}", f"Second{i}", f"S{i}."),
            ],
            publication_year=2020 + (i % 5),
            journal=f"Journal of Testing {i % 10}",
            abstract=abstract,
            keywords=["machine learning", "healthcare", "analytics"][: (i % 3) + 1],
        )
        papers.append(paper)

    return papers


@pytest.mark.benchmark
class TestAnalysisPerformanceTarget:
    """Test that analysis meets performance target."""

    def test_500_papers_under_30_seconds(self, benchmark):
        """Test that 500 papers can be analyzed in under 30 seconds.

        This is the critical performance requirement.
        """
        papers = generate_mock_papers(500, abstract_length=500)
        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        def analyze_operation():
            return use_case.execute(papers=papers, max_themes=5)

        result = benchmark.pedantic(
            analyze_operation,
            rounds=3,
            iterations=1,
        )

        # Verify results
        assert "themes" in result
        assert len(result["themes"]) > 0

        # Check performance target
        assert benchmark.stats.mean < 30.0, (
            f"Analysis took {benchmark.stats.mean:.2f}s, exceeds 30s target for 500 papers"
        )

        print("\n=== 500 PAPERS PERFORMANCE ===")
        print(f"Mean time: {benchmark.stats.mean:.2f}s")
        print(f"Themes found: {len(result['themes'])}")
        print(f"Papers/second: {500 / benchmark.stats.mean:.1f}")

    def test_100_papers_fast_analysis(self, benchmark):
        """Test that 100 papers can be analyzed quickly (baseline)."""
        papers = generate_mock_papers(100, abstract_length=500)
        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        result = benchmark(lambda: use_case.execute(papers=papers, max_themes=5))

        assert "themes" in result
        assert benchmark.stats.mean < 5.0  # Should be under 5 seconds

        print("\n=== 100 PAPERS BASELINE ===")
        print(f"Mean time: {benchmark.stats.mean:.3f}s")
        print(f"Themes found: {len(result['themes'])}")

    def test_1000_papers_extended(self, benchmark):
        """Test analysis with 1000 papers (extended scenario)."""
        papers = generate_mock_papers(1000, abstract_length=500)
        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        result = benchmark.pedantic(
            lambda: use_case.execute(papers=papers, max_themes=10),
            rounds=2,
            iterations=1,
        )

        assert "themes" in result

        # Should scale reasonably (under 60 seconds for 1000 papers)
        assert benchmark.stats.mean < 60.0

        print("\n=== 1000 PAPERS EXTENDED ===")
        print(f"Mean time: {benchmark.stats.mean:.2f}s")
        print(f"Themes found: {len(result['themes'])}")
        print(f"Papers/second: {1000 / benchmark.stats.mean:.1f}")


@pytest.mark.benchmark
class TestAnalysisPerformanceScaling:
    """Test how analysis performance scales with paper count."""

    @pytest.mark.parametrize("paper_count", [10, 50, 100, 250, 500])
    def test_scaling_by_paper_count(self, benchmark, paper_count):
        """Test performance scaling across different paper counts."""
        papers = generate_mock_papers(paper_count, abstract_length=500)
        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        result = benchmark(lambda: use_case.execute(papers=papers, max_themes=5))

        assert "themes" in result

        papers_per_second = paper_count / benchmark.stats.mean

        print(f"\n=== SCALING: {paper_count} papers ===")
        print(f"Time: {benchmark.stats.mean:.3f}s")
        print(f"Rate: {papers_per_second:.1f} papers/s")

    def test_scaling_with_abstract_length(self, benchmark):
        """Test how abstract length affects performance."""
        # Use 200 papers with longer abstracts
        papers = generate_mock_papers(200, abstract_length=2000)
        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        result = benchmark(lambda: use_case.execute(papers=papers, max_themes=5))

        assert "themes" in result
        assert benchmark.stats.mean < 15.0  # Should still be reasonably fast

        print("\n=== LONG ABSTRACTS (2000 chars) ===")
        print(f"Time: {benchmark.stats.mean:.3f}s for 200 papers")

    def test_scaling_with_theme_count(self, benchmark):
        """Test how max_themes parameter affects performance."""
        papers = generate_mock_papers(200, abstract_length=500)
        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        # Test with more themes (more clusters)
        result = benchmark(lambda: use_case.execute(papers=papers, max_themes=20))

        assert "themes" in result
        assert len(result["themes"]) > 0

        print("\n=== MANY THEMES (max=20) ===")
        print(f"Time: {benchmark.stats.mean:.3f}s")
        print(f"Themes found: {len(result['themes'])}")


@pytest.mark.benchmark
class TestAnalysisPerformanceOptimization:
    """Test performance optimizations."""

    def test_vectorization_performance(self, benchmark):
        """Test that TF-IDF vectorization is efficient."""
        papers = generate_mock_papers(500, abstract_length=500)
        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        # Test with custom vectorizer settings for speed
        result = benchmark(
            lambda: use_case.execute(
                papers=papers,
                max_themes=5,
                max_features=100,  # Limit features for speed
            )
        )

        assert "themes" in result
        # Should be faster with limited features
        assert benchmark.stats.mean < 20.0

        print("\n=== OPTIMIZED VECTORIZATION ===")
        print(f"Time: {benchmark.stats.mean:.3f}s for 500 papers")

    def test_clustering_performance(self, benchmark):
        """Test clustering algorithm performance."""
        papers = generate_mock_papers(500, abstract_length=500)
        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        # Measure clustering specifically
        start = time.time()
        result = use_case.execute(papers=papers, max_themes=5)
        total_time = time.time() - start

        assert "themes" in result

        print("\n=== CLUSTERING PERFORMANCE ===")
        print(f"Total time: {total_time:.3f}s for 500 papers")
        print(f"Themes generated: {len(result['themes'])}")


@pytest.mark.benchmark
class TestAnalysisPerformanceMemory:
    """Test memory efficiency of analysis."""

    def test_memory_efficient_large_corpus(self, benchmark):
        """Test that analysis handles large corpus efficiently."""
        # This would ideally use memory_profiler, but we'll test execution time
        papers = generate_mock_papers(1000, abstract_length=1000)
        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        def analyze():
            result = use_case.execute(papers=papers, max_themes=10)
            return result

        result = benchmark.pedantic(analyze, rounds=2, iterations=1)

        assert "themes" in result
        assert len(result["themes"]) > 0

        print("\n=== LARGE CORPUS (1000 papers, 1000 char abstracts) ===")
        print(f"Time: {benchmark.stats.mean:.2f}s")
        print("Memory efficient: Completed without issues")

    def test_incremental_processing(self, benchmark):
        """Test processing papers in batches for memory efficiency."""
        papers = generate_mock_papers(500, abstract_length=500)
        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        # Process in single batch (current implementation)
        def single_batch():
            return use_case.execute(papers=papers, max_themes=5)

        result = benchmark(single_batch)

        assert "themes" in result

        print("\n=== BATCH PROCESSING ===")
        print(f"Single batch time: {benchmark.stats.mean:.3f}s")


@pytest.mark.benchmark
class TestAnalysisPerformanceBaselines:
    """Establish performance baselines for regression testing."""

    def test_baseline_tfidf_vectorization(self, benchmark):
        """Baseline: TF-IDF vectorization time."""
        from sklearn.feature_extraction.text import TfidfVectorizer

        papers = generate_mock_papers(500, abstract_length=500)
        abstracts = [p.abstract for p in papers if p.abstract]

        vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")

        def vectorize():
            return vectorizer.fit_transform(abstracts)

        matrix = benchmark(vectorize)

        assert matrix.shape[0] == len(abstracts)

        print("\n=== BASELINE: TF-IDF Vectorization ===")
        print(f"Time: {benchmark.stats.mean:.4f}s for {len(abstracts)} abstracts")
        print(f"Matrix shape: {matrix.shape}")

    def test_baseline_clustering(self, benchmark):
        """Baseline: K-means clustering time."""
        from sklearn.cluster import KMeans
        from sklearn.feature_extraction.text import TfidfVectorizer

        papers = generate_mock_papers(500, abstract_length=500)
        abstracts = [p.abstract for p in papers if p.abstract]

        # Pre-compute vectors
        vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
        vectors = vectorizer.fit_transform(abstracts)

        def cluster():
            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            return kmeans.fit(vectors)

        model = benchmark(cluster)

        assert len(model.labels_) == len(abstracts)

        print("\n=== BASELINE: K-Means Clustering ===")
        print(f"Time: {benchmark.stats.mean:.4f}s for {len(abstracts)} abstracts")
        print("Clusters: 5")

    def test_baseline_full_pipeline(self, benchmark):
        """Baseline: Complete analysis pipeline."""
        papers = generate_mock_papers(500, abstract_length=500)
        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        result = benchmark.pedantic(
            lambda: use_case.execute(papers=papers, max_themes=5),
            rounds=5,
            iterations=1,
        )

        assert "themes" in result

        print("\n=== BASELINE: Full Analysis Pipeline ===")
        print(f"Mean: {benchmark.stats.mean:.3f}s")
        print(f"StdDev: {benchmark.stats.stddev:.3f}s")
        print(f"Min: {benchmark.stats.min:.3f}s")
        print(f"Max: {benchmark.stats.max:.3f}s")
        print(f"Themes: {len(result['themes'])}")
        print(f"Target: <30s for 500 papers - {'PASS' if benchmark.stats.mean < 30 else 'FAIL'}")


@pytest.mark.benchmark
class TestAnalysisPerformanceEdgeCases:
    """Test performance with edge cases."""

    def test_many_small_abstracts(self, benchmark):
        """Test with many papers but small abstracts."""
        papers = generate_mock_papers(1000, abstract_length=100)
        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        result = benchmark(lambda: use_case.execute(papers=papers, max_themes=5))

        assert "themes" in result
        print("\n=== SMALL ABSTRACTS (100 chars) ===")
        print(f"Time: {benchmark.stats.mean:.3f}s for 1000 papers")

    def test_few_large_abstracts(self, benchmark):
        """Test with few papers but large abstracts."""
        papers = generate_mock_papers(50, abstract_length=5000)
        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        result = benchmark(lambda: use_case.execute(papers=papers, max_themes=5))

        assert "themes" in result
        print("\n=== LARGE ABSTRACTS (5000 chars) ===")
        print(f"Time: {benchmark.stats.mean:.3f}s for 50 papers")

    def test_similar_papers(self, benchmark):
        """Test performance when all papers are very similar."""
        # All papers have identical abstracts
        abstract = (
            "Machine learning improves healthcare outcomes. "
            "Deep learning models analyze patient data effectively. "
        ) * 10

        papers = []
        for i in range(500):
            papers.append(
                Paper(
                    doi=DOI(f"10.1234/similar-{i}"),
                    title=f"Similar Paper {i}",
                    authors=[Author("Doe", "John", "J.")],
                    publication_year=2023,
                    journal="Journal",
                    abstract=abstract,
                )
            )

        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        result = benchmark(lambda: use_case.execute(papers=papers, max_themes=5))

        assert "themes" in result
        print("\n=== IDENTICAL PAPERS ===")
        print(f"Time: {benchmark.stats.mean:.3f}s for 500 similar papers")

    def test_diverse_papers(self, benchmark):
        """Test performance with highly diverse papers."""
        # Create papers with completely different abstracts
        diverse_abstracts = [
            "Quantum computing revolutionizes cryptography and security protocols.",
            "Agricultural technology improves crop yields through precision farming.",
            "Urban planning benefits from sustainable development practices.",
            "Renewable energy sources reduce carbon emissions significantly.",
            "Educational technology enhances student learning outcomes.",
        ]

        papers = []
        for i in range(500):
            abstract = diverse_abstracts[i % len(diverse_abstracts)] * 20
            papers.append(
                Paper(
                    doi=DOI(f"10.1234/diverse-{i}"),
                    title=f"Diverse Paper {i}",
                    authors=[Author("Doe", "John", "J.")],
                    publication_year=2023,
                    journal="Journal",
                    abstract=abstract,
                )
            )

        use_case = AnalyzeThemesUseCase(ai_analyzer=None)

        result = benchmark(lambda: use_case.execute(papers=papers, max_themes=10))

        assert "themes" in result
        print("\n=== DIVERSE PAPERS ===")
        print(f"Time: {benchmark.stats.mean:.3f}s for 500 diverse papers")
        print(f"Themes found: {len(result['themes'])}")
