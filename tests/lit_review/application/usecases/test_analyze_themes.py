"""Tests for AnalyzeThemesUseCase."""

import time

import pytest

from lit_review.application.usecases.analyze_themes import AnalyzeThemesUseCase
from lit_review.domain.entities.paper import Paper
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


@pytest.fixture
def sample_papers() -> list[Paper]:
    """Create sample papers with varied abstracts for testing."""
    papers = []

    # Healthcare AI papers
    papers.append(
        Paper(
            doi=DOI("10.1001/ai-healthcare-1"),
            title="Machine Learning in Clinical Decision Support",
            authors=[Author("Smith", "John", "J")],
            publication_year=2023,
            journal="AI Medicine",
            abstract=(
                "This study explores machine learning algorithms for clinical decision "
                "support systems. We evaluate deep learning models for diagnosis prediction "
                "and treatment recommendation in healthcare settings."
            ),
            keywords=["machine learning", "clinical decision support", "healthcare AI"],
        )
    )

    papers.append(
        Paper(
            doi=DOI("10.1001/ai-healthcare-2"),
            title="Deep Learning for Medical Image Analysis",
            authors=[Author("Jones", "Mary", "M")],
            publication_year=2023,
            journal="Medical AI",
            abstract=(
                "Deep learning techniques have revolutionized medical image analysis. "
                "Convolutional neural networks show promising results in radiology imaging "
                "and diagnostic accuracy for various medical conditions."
            ),
            keywords=["deep learning", "medical imaging", "neural networks"],
        )
    )

    # Natural language processing papers
    papers.append(
        Paper(
            doi=DOI("10.1002/nlp-ehr-1"),
            title="Natural Language Processing of Electronic Health Records",
            authors=[Author("Brown", "David", "D")],
            publication_year=2023,
            journal="Health Informatics",
            abstract=(
                "Natural language processing methods extract structured information from "
                "unstructured clinical notes in electronic health records. Named entity "
                "recognition and relation extraction improve data quality."
            ),
            keywords=["natural language processing", "EHR", "clinical notes"],
        )
    )

    papers.append(
        Paper(
            doi=DOI("10.1002/nlp-ehr-2"),
            title="Text Mining for Clinical Research",
            authors=[Author("Wilson", "Sarah", "S")],
            publication_year=2023,
            journal="Clinical Informatics",
            abstract=(
                "Text mining techniques analyze large volumes of clinical text data. "
                "Information extraction and text classification enable automated coding "
                "and clinical research applications."
            ),
            keywords=["text mining", "clinical research", "information extraction"],
        )
    )

    # Data privacy papers
    papers.append(
        Paper(
            doi=DOI("10.1003/privacy-1"),
            title="Privacy-Preserving Machine Learning in Healthcare",
            authors=[Author("Lee", "Kevin", "K")],
            publication_year=2023,
            journal="Privacy Journal",
            abstract=(
                "Privacy-preserving techniques like federated learning and differential "
                "privacy enable machine learning on sensitive healthcare data without "
                "compromising patient confidentiality."
            ),
            keywords=["privacy", "federated learning", "differential privacy"],
        )
    )

    return papers


class TestAnalyzeThemesUseCaseExecution:
    """Tests for main execute method."""

    def test_execute_with_valid_papers(self, sample_papers: list[Paper]) -> None:
        """Test theme analysis with valid papers."""
        use_case = AnalyzeThemesUseCase()

        result = use_case.execute(sample_papers, max_themes=3)

        assert result is not None
        assert len(result.themes) > 0
        assert len(result.themes) <= 3
        assert result.summary
        assert "papers" in result.summary.lower()

    def test_execute_with_empty_papers_raises_error(self) -> None:
        """Test that empty papers list raises ValueError."""
        use_case = AnalyzeThemesUseCase()

        with pytest.raises(ValueError, match="empty paper list"):
            use_case.execute([], max_themes=3)

    def test_execute_with_invalid_max_themes_raises_error(self, sample_papers: list[Paper]) -> None:
        """Test that invalid max_themes raises ValueError."""
        use_case = AnalyzeThemesUseCase()

        with pytest.raises(ValueError, match="max_themes must be at least 1"):
            use_case.execute(sample_papers, max_themes=0)

    def test_execute_with_no_abstracts_raises_error(self) -> None:
        """Test that papers without abstracts raise ValueError."""
        papers = [
            Paper(
                doi=DOI("10.1001/no-abstract"),
                title="Paper Without Abstract",
                authors=[Author("Test", "User", "T")],
                publication_year=2023,
                journal="Test Journal",
                abstract=None,
            )
        ]

        use_case = AnalyzeThemesUseCase()

        with pytest.raises(ValueError, match="No papers with abstracts"):
            use_case.execute(papers, max_themes=3)

    def test_execute_themes_contain_keywords(self, sample_papers: list[Paper]) -> None:
        """Test that extracted themes contain relevant keywords."""
        use_case = AnalyzeThemesUseCase()

        result = use_case.execute(sample_papers, max_themes=3)

        # Check that themes have keywords
        for theme_name, keywords in result.themes.items():
            assert len(keywords) > 0
            assert all(isinstance(kw, str) for kw in keywords)

    def test_execute_with_single_paper(self) -> None:
        """Test theme analysis with single paper."""
        paper = Paper(
            doi=DOI("10.1001/single"),
            title="Single Paper Study",
            authors=[Author("Single", "Author", "S")],
            publication_year=2023,
            journal="Single Journal",
            abstract=(
                "This paper discusses machine learning algorithms for healthcare "
                "applications including diagnosis and treatment recommendations."
            ),
        )

        use_case = AnalyzeThemesUseCase()
        result = use_case.execute([paper], max_themes=2)

        assert len(result.themes) > 0
        assert result.summary


class TestAnalyzeThemesUseCaseRelationships:
    """Tests for theme relationship calculations."""

    def test_relationships_calculated(self, sample_papers: list[Paper]) -> None:
        """Test that theme relationships are calculated."""
        use_case = AnalyzeThemesUseCase()

        result = use_case.execute(sample_papers, max_themes=3)

        assert isinstance(result.relationships, dict)

        # Each theme should have relationships to other themes
        for theme_name, related_themes in result.relationships.items():
            assert theme_name in result.themes
            assert isinstance(related_themes, dict)

            # Check relationship scores
            for related_theme, score in related_themes.items():
                assert related_theme in result.themes
                assert 0.0 <= score <= 1.0

    def test_no_self_relationships(self, sample_papers: list[Paper]) -> None:
        """Test that themes don't have relationships to themselves."""
        use_case = AnalyzeThemesUseCase()

        result = use_case.execute(sample_papers, max_themes=3)

        for theme_name, related_themes in result.relationships.items():
            assert theme_name not in related_themes


class TestAnalyzeThemesUseCasePerformance:
    """Performance tests for theme analysis."""

    def test_performance_under_30_seconds_for_500_papers(self) -> None:
        """Test that analysis completes in <30s for 500 papers."""
        # Generate 500 papers with varied abstracts
        papers = []
        abstracts = [
            (
                "Machine learning algorithms improve clinical decision support "
                "systems for healthcare diagnosis and treatment recommendations."
            ),
            (
                "Natural language processing extracts structured information from "
                "electronic health records and clinical documentation."
            ),
            (
                "Deep learning models analyze medical images for radiology "
                "and diagnostic applications in healthcare settings."
            ),
            (
                "Privacy-preserving techniques like federated learning enable "
                "secure machine learning on sensitive patient data."
            ),
            (
                "Text mining and information extraction analyze large volumes "
                "of clinical research literature and publications."
            ),
        ]

        for i in range(500):
            papers.append(
                Paper(
                    doi=DOI(f"10.{1000 + i // 1000}/paper-{i}"),
                    title=f"Research Paper {i}",
                    authors=[Author(f"Author{i}", "First", "F")],
                    publication_year=2023,
                    journal="Test Journal",
                    abstract=abstracts[i % len(abstracts)],
                )
            )

        use_case = AnalyzeThemesUseCase()

        start_time = time.time()
        result = use_case.execute(papers, max_themes=10)
        elapsed_time = time.time() - start_time

        assert elapsed_time < 30.0, f"Analysis took {elapsed_time:.2f}s (should be <30s)"
        assert len(result.themes) > 0

    def test_performance_scales_with_paper_count(self) -> None:
        """Test that performance scales reasonably with paper count."""
        abstract = (
            "This paper discusses machine learning applications in healthcare "
            "including diagnosis prediction and treatment recommendations."
        )

        times = []
        paper_counts = [10, 50, 100]

        for count in paper_counts:
            papers = [
                Paper(
                    doi=DOI(f"10.1000/paper-{i}"),
                    title=f"Paper {i}",
                    authors=[Author(f"Author{i}", "First", "F")],
                    publication_year=2023,
                    journal="Journal",
                    abstract=abstract,
                )
                for i in range(count)
            ]

            use_case = AnalyzeThemesUseCase()

            start_time = time.time()
            use_case.execute(papers, max_themes=5)
            elapsed_time = time.time() - start_time

            times.append(elapsed_time)

        # Check that time increases reasonably (not exponentially)
        # 10x papers should take less than 20x time
        if len(times) >= 2:
            ratio = times[-1] / times[0]
            count_ratio = paper_counts[-1] / paper_counts[0]
            assert ratio < count_ratio * 2


class TestAnalyzeThemesUseCaseConfiguration:
    """Tests for configuration parameters."""

    def test_custom_max_features(self, sample_papers: list[Paper]) -> None:
        """Test custom max_features parameter."""
        use_case = AnalyzeThemesUseCase(max_features=50)

        result = use_case.execute(sample_papers, max_themes=3)

        assert len(result.themes) > 0

    def test_custom_min_df(self, sample_papers: list[Paper]) -> None:
        """Test custom min_df parameter."""
        use_case = AnalyzeThemesUseCase(min_df=1)

        result = use_case.execute(sample_papers, max_themes=3)

        assert len(result.themes) > 0

    def test_custom_max_df(self, sample_papers: list[Paper]) -> None:
        """Test custom max_df parameter."""
        use_case = AnalyzeThemesUseCase(max_df=0.9)

        result = use_case.execute(sample_papers, max_themes=3)

        assert len(result.themes) > 0


class TestAnalyzeThemesUseCaseSummary:
    """Tests for summary generation."""

    def test_summary_contains_paper_count(self, sample_papers: list[Paper]) -> None:
        """Test that summary includes paper count."""
        use_case = AnalyzeThemesUseCase()

        result = use_case.execute(sample_papers, max_themes=3)

        assert str(len(sample_papers)) in result.summary

    def test_summary_contains_theme_count(self, sample_papers: list[Paper]) -> None:
        """Test that summary includes theme count."""
        use_case = AnalyzeThemesUseCase()

        result = use_case.execute(sample_papers, max_themes=3)

        assert str(len(result.themes)) in result.summary

    def test_summary_lists_themes(self, sample_papers: list[Paper]) -> None:
        """Test that summary lists theme names."""
        use_case = AnalyzeThemesUseCase()

        result = use_case.execute(sample_papers, max_themes=3)

        for theme_name in result.themes.keys():
            assert theme_name in result.summary
