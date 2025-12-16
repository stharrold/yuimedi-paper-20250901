# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for GenerateSynthesisUseCase."""

import pytest

from lit_review.application.ports.ai_analyzer import AIAnalyzer, ThemeHierarchy
from lit_review.application.usecases.generate_synthesis import GenerateSynthesisUseCase
from lit_review.domain.entities.paper import Paper
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


class MockAIAnalyzer(AIAnalyzer):
    """Mock AI analyzer for testing."""

    def __init__(self, should_fail: bool = False) -> None:
        """Initialize mock analyzer.

        Args:
            should_fail: If True, raise exception on generate_synthesis.
        """
        self.should_fail = should_fail
        self.called = False

    def extract_themes(self, papers: list[Paper], max_themes: int = 10) -> ThemeHierarchy:
        """Mock extract_themes."""
        return ThemeHierarchy(
            themes={"Theme 1": ["keyword1", "keyword2"]},
            relationships={},
            summary="Mock summary",
        )

    def generate_synthesis(
        self, papers: list[Paper], themes: ThemeHierarchy, research_question: str
    ) -> str:
        """Mock generate_synthesis."""
        self.called = True
        if self.should_fail:
            raise RuntimeError("Mock AI failure")
        return "# AI-Generated Synthesis\n\nThis is AI-generated content."


@pytest.fixture
def sample_papers() -> list[Paper]:
    """Create sample papers for testing."""
    return [
        Paper(
            doi=DOI("10.1001/paper1"),
            title="Machine Learning in Healthcare",
            authors=[Author("Smith", "John", "J"), Author("Doe", "Jane", "J")],
            publication_year=2023,
            journal="AI Medicine",
            abstract=(
                "This study explores machine learning algorithms for clinical "
                "decision support systems."
            ),
        ),
        Paper(
            doi=DOI("10.1002/paper2"),
            title="Deep Learning for Medical Imaging",
            authors=[Author("Jones", "Mary", "M")],
            publication_year=2022,
            journal="Medical AI",
            abstract="Deep learning techniques for radiology image analysis.",
        ),
        Paper(
            doi=DOI("10.1003/paper3"),
            title="Natural Language Processing in EHR",
            authors=[Author("Brown", "David", "D")],
            publication_year=2021,
            journal="Health Informatics",
            abstract="NLP methods for electronic health records.",
        ),
    ]


@pytest.fixture
def sample_themes() -> ThemeHierarchy:
    """Create sample themes for testing."""
    return ThemeHierarchy(
        themes={
            "Theme 1": ["machine learning", "algorithms", "clinical"],
            "Theme 2": ["deep learning", "imaging", "radiology"],
            "Theme 3": ["natural language", "processing", "ehr"],
        },
        relationships={
            "Theme 1": {"Theme 2": 0.5, "Theme 3": 0.3},
            "Theme 2": {"Theme 1": 0.5, "Theme 3": 0.2},
            "Theme 3": {"Theme 1": 0.3, "Theme 2": 0.2},
        },
        summary="Three major themes identified",
    )


class TestGenerateSynthesisUseCaseExecution:
    """Tests for main execute method."""

    def test_execute_with_valid_inputs(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test synthesis generation with valid inputs."""
        use_case = GenerateSynthesisUseCase()

        result = use_case.execute(
            sample_papers, sample_themes, "What is the impact of AI in healthcare?"
        )

        assert result
        assert "Literature Review Synthesis" in result
        assert "Thematic Analysis" in result
        assert "Research Gaps" in result
        assert "Conclusions" in result
        assert "References" in result

    def test_execute_with_empty_papers_raises_error(self, sample_themes: ThemeHierarchy) -> None:
        """Test that empty papers list raises ValueError."""
        use_case = GenerateSynthesisUseCase()

        with pytest.raises(ValueError, match="empty paper list"):
            use_case.execute([], sample_themes, "Research question?")

    def test_execute_with_empty_research_question_raises_error(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that empty research question raises ValueError."""
        use_case = GenerateSynthesisUseCase()

        with pytest.raises(ValueError, match="cannot be empty"):
            use_case.execute(sample_papers, sample_themes, "")

    def test_execute_with_whitespace_research_question_raises_error(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that whitespace-only research question raises ValueError."""
        use_case = GenerateSynthesisUseCase()

        with pytest.raises(ValueError, match="cannot be empty"):
            use_case.execute(sample_papers, sample_themes, "   ")

    def test_execute_uses_ai_when_requested(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that AI analyzer is used when use_ai=True."""
        mock_ai = MockAIAnalyzer()
        use_case = GenerateSynthesisUseCase(ai_analyzer=mock_ai)

        result = use_case.execute(sample_papers, sample_themes, "Research question?", use_ai=True)

        assert mock_ai.called
        assert "AI-Generated" in result

    def test_execute_falls_back_to_keyword_when_ai_fails(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test fallback to keyword synthesis when AI fails."""
        mock_ai = MockAIAnalyzer(should_fail=True)
        use_case = GenerateSynthesisUseCase(ai_analyzer=mock_ai)

        result = use_case.execute(sample_papers, sample_themes, "Research question?", use_ai=True)

        assert mock_ai.called
        assert "Literature Review Synthesis" in result  # Keyword-based format

    def test_execute_without_ai_analyzer(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that synthesis works without AI analyzer."""
        use_case = GenerateSynthesisUseCase(ai_analyzer=None)

        result = use_case.execute(sample_papers, sample_themes, "Research question?", use_ai=True)

        assert "Literature Review Synthesis" in result


class TestGenerateSynthesisUseCaseIntroduction:
    """Tests for introduction generation."""

    def test_introduction_contains_paper_count(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that introduction includes paper count."""
        use_case = GenerateSynthesisUseCase()

        result = use_case.execute(sample_papers, sample_themes, "Research question?")

        assert str(len(sample_papers)) in result

    def test_introduction_contains_research_question(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that introduction includes research question."""
        question = "What is the impact of machine learning in healthcare?"
        use_case = GenerateSynthesisUseCase()

        result = use_case.execute(sample_papers, sample_themes, question)

        assert question in result

    def test_introduction_contains_year_range(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that introduction includes year range."""
        use_case = GenerateSynthesisUseCase()

        result = use_case.execute(sample_papers, sample_themes, "Research question?")

        assert "2021-2023" in result or "2021" in result


class TestGenerateSynthesisUseCaseThemes:
    """Tests for theme section generation."""

    def test_theme_sections_generated(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that theme sections are generated."""
        use_case = GenerateSynthesisUseCase()

        result = use_case.execute(sample_papers, sample_themes, "Research question?")

        for theme_name in sample_themes.themes.keys():
            assert theme_name in result

    def test_theme_sections_include_keywords(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that theme sections include keywords."""
        use_case = GenerateSynthesisUseCase()

        result = use_case.execute(sample_papers, sample_themes, "Research question?")

        # Check for some keywords from themes
        assert "machine learning" in result.lower()


class TestGenerateSynthesisUseCaseResearchGaps:
    """Tests for research gap identification."""

    def test_research_gaps_section_present(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that research gaps section is present."""
        use_case = GenerateSynthesisUseCase()

        result = use_case.execute(sample_papers, sample_themes, "Research question?")

        assert "Research Gaps" in result

    def test_identifies_temporal_gap_for_old_papers(self, sample_themes: ThemeHierarchy) -> None:
        """Test that temporal gaps are identified for old papers."""
        old_papers = [
            Paper(
                doi=DOI(f"10.100{i}/paper{i}"),
                title=f"Paper {i}",
                authors=[Author("Author", "Test", "T")],
                publication_year=2015,
                journal="Old Journal",
                abstract="Old research.",
            )
            for i in range(3)
        ]

        use_case = GenerateSynthesisUseCase()
        result = use_case.execute(old_papers, sample_themes, "Research question?")

        assert "recent research" in result.lower() or "updated studies" in result.lower()


class TestGenerateSynthesisUseCaseConclusion:
    """Tests for conclusion generation."""

    def test_conclusion_section_present(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that conclusion section is present."""
        use_case = GenerateSynthesisUseCase()

        result = use_case.execute(sample_papers, sample_themes, "Research question?")

        assert "Conclusions" in result

    def test_conclusion_contains_paper_count(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that conclusion includes paper count."""
        use_case = GenerateSynthesisUseCase()

        result = use_case.execute(sample_papers, sample_themes, "Research question?")

        conclusion_section = result.split("## Conclusions")[1].split("##")[0]
        assert str(len(sample_papers)) in conclusion_section


class TestGenerateSynthesisUseCaseReferences:
    """Tests for reference generation."""

    def test_references_section_present(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that references section is present."""
        use_case = GenerateSynthesisUseCase()

        result = use_case.execute(sample_papers, sample_themes, "Research question?")

        assert "References" in result

    def test_all_papers_referenced(
        self, sample_papers: list[Paper], sample_themes: ThemeHierarchy
    ) -> None:
        """Test that all papers appear in references."""
        use_case = GenerateSynthesisUseCase()

        result = use_case.execute(sample_papers, sample_themes, "Research question?")

        references_section = result.split("## References")[1]

        for paper in sample_papers:
            assert paper.doi.value in references_section


class TestGenerateSynthesisUseCaseCitations:
    """Tests for citation formatting."""

    def test_format_single_citation(self, sample_papers: list[Paper]) -> None:
        """Test formatting of single citation."""
        use_case = GenerateSynthesisUseCase()

        citation = use_case._format_citations([sample_papers[0]])

        assert "[" in citation
        assert "]" in citation
        assert sample_papers[0].get_citation_key() in citation

    def test_format_two_citations(self, sample_papers: list[Paper]) -> None:
        """Test formatting of two citations."""
        use_case = GenerateSynthesisUseCase()

        citation = use_case._format_citations(sample_papers[:2])

        assert ";" in citation
        assert sample_papers[0].get_citation_key() in citation
        assert sample_papers[1].get_citation_key() in citation

    def test_format_many_citations(self, sample_papers: list[Paper]) -> None:
        """Test formatting of many citations."""
        use_case = GenerateSynthesisUseCase()

        # Add more papers
        many_papers = sample_papers + [
            Paper(
                doi=DOI(f"10.100{i}/paper{i}"),
                title=f"Paper {i}",
                authors=[Author("Author", "Test", "T")],
                publication_year=2023,
                journal="Journal",
                abstract="Abstract",
            )
            for i in range(4, 10)
        ]

        citation = use_case._format_citations(many_papers)

        assert "and others" in citation

    def test_format_empty_citations(self) -> None:
        """Test formatting of empty citation list."""
        use_case = GenerateSynthesisUseCase()

        citation = use_case._format_citations([])

        assert citation == ""
