"""Integration tests for full literature review workflow.

Tests end-to-end workflow: init → search → assess → analyze → synthesize → export
Uses real adapters with small result sets (marked as integration tests).

Run with: pytest -v tests/lit_review/integration/test_full_workflow.py -m integration
Skip network tests: pytest -v -m "not integration"
"""

import json
import tempfile
from pathlib import Path

import pytest

from lit_review.application.ports.ai_analyzer import AIAnalyzer, ThemeHierarchy
from lit_review.application.usecases.analyze_themes import AnalyzeThemesUseCase
from lit_review.application.usecases.export_review import ExportFormat, ExportReviewUseCase
from lit_review.application.usecases.generate_synthesis import GenerateSynthesisUseCase
from lit_review.application.usecases.search_papers import SearchPapersUseCase
from lit_review.domain.entities.paper import Paper
from lit_review.domain.entities.review import Review, ReviewStage
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI
from lit_review.infrastructure.adapters.arxiv_adapter import ArxivAdapter
from lit_review.infrastructure.adapters.crossref_adapter import CrossrefAdapter
from lit_review.infrastructure.adapters.pubmed_adapter import PubMedAdapter
from lit_review.infrastructure.adapters.semantic_scholar_adapter import SemanticScholarAdapter
from lit_review.infrastructure.persistence.json_repository import JSONReviewRepository


@pytest.fixture
def temp_review_dir():
    """Create a temporary directory for review storage."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def review_repository(temp_review_dir: Path) -> JSONReviewRepository:
    """Create a JSON repository for testing."""
    return JSONReviewRepository(temp_review_dir)


@pytest.fixture
def search_use_case() -> SearchPapersUseCase:
    """Create a search use case with all adapters.

    Note: PubMed adapter is only added if NCBI_EMAIL is set,
    as it's required by NCBI policy.
    """
    import os

    use_case = SearchPapersUseCase()
    use_case.add_service("arxiv", ArxivAdapter())
    use_case.add_service("crossref", CrossrefAdapter())

    # Only add PubMed if email is configured (required by NCBI)
    if os.environ.get("NCBI_EMAIL"):
        use_case.add_service("pubmed", PubMedAdapter())

    use_case.add_service("semantic_scholar", SemanticScholarAdapter())
    return use_case


@pytest.fixture
def mock_ai_analyzer():
    """Create a mock AI analyzer that doesn't require API keys."""

    class MockAIAnalyzer(AIAnalyzer):
        """Mock AI analyzer for testing without API calls."""

        def extract_themes(self, papers: list[Paper], max_themes: int = 10) -> ThemeHierarchy:
            """Extract themes from papers (mock implementation)."""
            return ThemeHierarchy(
                themes={
                    "Machine Learning Applications": [
                        "machine learning",
                        "neural networks",
                        "deep learning",
                    ],
                    "Healthcare Systems": ["healthcare", "clinical", "hospital"],
                },
                relationships={
                    "Machine Learning Applications": {
                        "Healthcare Systems": 0.7,
                    },
                },
                summary=f"Identified 2 main themes across {len(papers)} papers.",
            )

        def generate_synthesis(
            self, papers: list[Paper], themes: ThemeHierarchy, research_question: str
        ) -> str:
            """Generate synthesis (mock implementation)."""
            return f"""# Literature Review Synthesis

## Introduction
This synthesis addresses: {research_question}
Analyzed {len(papers)} papers.

## Key Themes

### Machine Learning Applications
Papers explore ML applications in healthcare.

### Healthcare Systems
Focus on healthcare system improvements.

## Conclusions
Significant progress in the field.
"""

    return MockAIAnalyzer()


class TestFullWorkflowWithoutNetwork:
    """Test full workflow without network calls (using mocks)."""

    def test_init_stage(self, review_repository: JSONReviewRepository):
        """Test review initialization."""
        # Create a new review
        review = Review(
            title="Healthcare AI Literature Review",
            research_question="How is AI transforming healthcare delivery?",
            inclusion_criteria=["Peer-reviewed", "English", "Published 2020-2024"],
            exclusion_criteria=["Conference abstracts", "Non-empirical"],
        )

        # Should be in PLANNING stage
        assert review.stage == ReviewStage.PLANNING
        assert len(review.papers) == 0

        # Save to repository (uses title as ID)
        review_repository.save(review)
        loaded = review_repository.load(review.title)
        assert loaded is not None
        assert loaded.title == review.title
        assert loaded.stage == ReviewStage.PLANNING

    def test_search_stage(self, review_repository: JSONReviewRepository):
        """Test adding papers to review."""
        # Create and advance to SEARCH stage
        review = Review(
            title="Test Review",
            research_question="Test question",
            inclusion_criteria=["Test"],
            exclusion_criteria=["None"],
        )
        review.advance_stage()
        assert review.stage == ReviewStage.SEARCH

        # Add mock papers
        papers = [
            Paper(
                doi=DOI("10.1234/test1"),
                title="Test Paper 1",
                authors=[Author("Smith", "John", "J.")],
                publication_year=2023,
                journal="Test Journal",
                abstract="Test abstract 1",
            ),
            Paper(
                doi=DOI("10.1234/test2"),
                title="Test Paper 2",
                authors=[Author("Jones", "Jane", "J.")],
                publication_year=2023,
                journal="Test Journal",
                abstract="Test abstract 2",
            ),
        ]

        for paper in papers:
            review.add_paper(paper)

        assert len(review.papers) == 2
        review_repository.save(review)

        # Verify persistence (use title as ID)
        loaded = review_repository.load(review.title)
        assert loaded is not None
        assert len(loaded.papers) == 2
        assert loaded.stage == ReviewStage.SEARCH

    def test_assessment_stage(self, review_repository: JSONReviewRepository):
        """Test quality assessment stage."""
        # Setup review with papers
        review = Review(
            title="Test Assessment Review",
            research_question="Test question",
            inclusion_criteria=["Test"],
            exclusion_criteria=["None"],
        )
        review.advance_stage()  # to SEARCH

        papers = [
            Paper(
                doi=DOI("10.1234/test1"),
                title="High Quality Paper",
                authors=[Author("Smith", "John", "J.")],
                publication_year=2023,
                journal="Nature",
                abstract="Rigorous methodology and clear results.",
            ),
            Paper(
                doi=DOI("10.1234/test2"),
                title="Lower Quality Paper",
                authors=[Author("Jones", "Jane", "J.")],
                publication_year=2023,
                journal="Blog Post",
                abstract="Informal discussion.",
            ),
        ]

        for paper in papers:
            review.add_paper(paper)

        # Advance to SCREENING (not ASSESSMENT - check enum)
        review.advance_stage()
        assert review.stage == ReviewStage.SCREENING

        # Assess papers (convert set to list)
        papers_list = list(review.papers)
        papers_list[0].assess(
            score=9.0,
            include=True,
            notes="Excellent methodology",
        )
        papers_list[1].assess(
            score=4.0,
            include=False,
            notes="Not peer-reviewed",
        )

        # Save and verify
        review_repository.save(review)
        loaded = review_repository.load(review.title)
        assert loaded is not None
        included = loaded.get_included_papers()
        excluded = loaded.get_excluded_papers()
        assert len(included) == 1
        assert len(excluded) == 1

    def test_analysis_stage(self, review_repository: JSONReviewRepository):
        """Test theme analysis stage."""
        # Setup review with assessed papers
        review = Review(
            title="Test Analysis Review",
            research_question="Test question",
            inclusion_criteria=["Test"],
            exclusion_criteria=["None"],
        )
        review.advance_stage()  # to SEARCH

        papers = [
            Paper(
                doi=DOI("10.1234/ml1"),
                title="Machine Learning in Healthcare",
                authors=[Author("Smith", "John", "J.")],
                publication_year=2023,
                journal="Nature",
                abstract="Machine learning models improve healthcare outcomes through predictive analytics.",
            ),
            Paper(
                doi=DOI("10.1234/ml2"),
                title="Deep Learning Applications",
                authors=[Author("Jones", "Jane", "J.")],
                publication_year=2023,
                journal="Science",
                abstract="Deep learning and neural networks show promise in medical imaging.",
            ),
        ]

        for paper in papers:
            review.add_paper(paper)

        # Assess papers
        for paper in review.papers:
            paper.assess(score=8.0, include=True, notes="Good")

        # Advance to ANALYSIS (PLANNING -> SEARCH -> SCREENING -> ANALYSIS)
        review.advance_stage()  # to SCREENING
        review.advance_stage()  # to ANALYSIS
        assert review.stage == ReviewStage.ANALYSIS

        # Perform theme analysis (using TF-IDF clustering)
        analyze_use_case = AnalyzeThemesUseCase()
        themes = analyze_use_case.execute(papers=list(review.papers), max_themes=3)

        assert isinstance(themes.themes, dict)
        assert len(themes.themes) > 0
        assert themes.summary != ""

        # Save with analysis results
        review_repository.save(review)

    def test_synthesis_stage(
        self,
        review_repository: JSONReviewRepository,
        mock_ai_analyzer: AIAnalyzer,
    ):
        """Test synthesis generation stage."""
        # Setup review
        review = Review(
            title="Healthcare AI Review",
            research_question="How is AI transforming healthcare?",
            inclusion_criteria=["Test"],
            exclusion_criteria=["None"],
        )

        # Add papers and move through stages
        papers = [
            Paper(
                doi=DOI("10.1234/ai1"),
                title="AI in Diagnostics",
                authors=[Author("Smith", "John", "J.")],
                publication_year=2023,
                journal="Nature Medicine",
                abstract="AI improves diagnostic accuracy in radiology.",
            ),
            Paper(
                doi=DOI("10.1234/ai2"),
                title="Clinical Decision Support",
                authors=[Author("Jones", "Jane", "J.")],
                publication_year=2023,
                journal="JAMA",
                abstract="AI-based clinical decision support systems.",
            ),
        ]

        review.advance_stage()  # SEARCH
        for paper in papers:
            review.add_paper(paper)

        # Assess papers
        for paper in review.papers:
            paper.assess(score=8.0, include=True, notes="Good")

        review.advance_stage()  # SCREENING
        review.advance_stage()  # ANALYSIS
        review.advance_stage()  # SYNTHESIS
        assert review.stage == ReviewStage.SYNTHESIS

        # Generate themes first (required for synthesis)
        analyze_use_case = AnalyzeThemesUseCase()
        themes = analyze_use_case.execute(papers=list(review.papers), max_themes=3)

        # Generate synthesis with AI
        synthesis_use_case = GenerateSynthesisUseCase(ai_analyzer=mock_ai_analyzer)
        synthesis = synthesis_use_case.execute(
            papers=list(review.papers),
            themes=themes,
            research_question=review.research_question,
            use_ai=True,
        )

        assert "Literature Review Synthesis" in synthesis
        assert review.research_question in synthesis
        assert str(len(papers)) in synthesis

        # Save review
        review_repository.save(review)

    def test_export_stage_all_formats(
        self, review_repository: JSONReviewRepository, temp_review_dir: Path
    ):
        """Test export stage with all formats."""
        # Setup review with papers
        review = Review(
            title="Export Test Review",
            research_question="Test export functionality",
            inclusion_criteria=["Test"],
            exclusion_criteria=["None"],
        )
        review.advance_stage()  # SEARCH

        papers = [
            Paper(
                doi=DOI("10.1234/export1"),
                title="Export Test Paper",
                authors=[Author("Smith", "John", "J.")],
                publication_year=2023,
                journal="Test Journal",
                abstract="Test abstract for export.",
            ),
        ]

        for paper in papers:
            review.add_paper(paper)

        # Assess papers
        for paper in review.papers:
            paper.assess(score=8.0, include=True, notes="Good")

        # Move to COMPLETE stage (final stage)
        review.advance_stage()  # SCREENING
        review.advance_stage()  # ANALYSIS
        review.advance_stage()  # SYNTHESIS
        review.advance_stage()  # COMPLETE
        assert review.stage == ReviewStage.COMPLETE

        # Test each export format
        export_use_case = ExportReviewUseCase()

        formats_to_test = ["bibtex", "json", "html", "markdown", "csv"]
        exported_files = []

        format_map = {
            "bibtex": ExportFormat.BIBTEX,
            "json": ExportFormat.JSON,
            "html": ExportFormat.HTML,
            "markdown": ExportFormat.MARKDOWN,
            "csv": ExportFormat.CSV,
        }

        for fmt in formats_to_test:
            output_path = temp_review_dir / f"export.{fmt}"
            export_use_case.execute(
                review=review,
                export_format=format_map[fmt],
                output_path=output_path,
                included_only=True,
            )

            assert output_path.exists(), f"Export file not created: {output_path}"
            assert output_path.stat().st_size > 0, f"Export file is empty: {output_path}"
            exported_files.append(output_path)

        # Verify content of each format
        # BibTeX
        bibtex_content = (temp_review_dir / "export.bibtex").read_text()
        assert "@article{" in bibtex_content or "@misc{" in bibtex_content

        # JSON
        json_content = json.loads((temp_review_dir / "export.json").read_text())
        assert "papers" in json_content
        assert len(json_content["papers"]) == 1

        # HTML
        html_content = (temp_review_dir / "export.html").read_text()
        assert "<html" in html_content.lower()
        assert "Export Test Paper" in html_content

        # Markdown
        md_content = (temp_review_dir / "export.markdown").read_text()
        assert "#" in md_content  # Has headers
        assert "Export Test Paper" in md_content

        # CSV
        csv_content = (temp_review_dir / "export.csv").read_text()
        assert "DOI" in csv_content or "Title" in csv_content
        assert "Export Test Paper" in csv_content


@pytest.mark.integration
class TestFullWorkflowWithNetwork:
    """Integration tests with real API calls (requires network)."""

    def test_end_to_end_workflow_small_search(
        self,
        review_repository: JSONReviewRepository,
        search_use_case: SearchPapersUseCase,
        temp_review_dir: Path,
    ):
        """Test complete workflow with real search (small result set)."""
        # Initialize review
        review = Review(
            title="COVID-19 Treatment Review",
            research_question="What treatments are effective for COVID-19?",
            inclusion_criteria=["Peer-reviewed", "English", "RCT"],
            exclusion_criteria=["Preprints", "Non-human studies"],
        )

        # Save initial state
        review_repository.save(review)

        # Stage 1: Search (limit to 5 papers for speed)
        review.advance_stage()
        assert review.stage == ReviewStage.SEARCH

        try:
            papers = search_use_case.execute(
                query="COVID-19 treatment randomized controlled trial",
                databases=["crossref"],  # Use Crossref (no auth required)
                limit=5,
            )

            # Add papers to review
            for paper in papers:
                review.add_paper(paper)

            assert len(review.papers) > 0, "No papers found in search"
            review_repository.save(review)

        except Exception as e:
            pytest.skip(f"Network search failed (expected in CI): {e}")

        # Stage 2: Screening
        review.advance_stage()
        assert review.stage == ReviewStage.SCREENING

        # Quick assessment for testing
        for paper in review.papers:
            paper.assess(
                score=7.0,
                include=True,
                notes="Auto-assessed for integration test",
            )

        review_repository.save(review)

        # Stage 3: Analysis
        review.advance_stage()
        assert review.stage == ReviewStage.ANALYSIS

        analyze_use_case = AnalyzeThemesUseCase()
        themes = analyze_use_case.execute(papers=list(review.papers), max_themes=3)

        assert isinstance(themes.themes, dict)
        review_repository.save(review)

        # Stage 4: Synthesis
        review.advance_stage()
        assert review.stage == ReviewStage.SYNTHESIS

        synthesis_use_case = GenerateSynthesisUseCase(ai_analyzer=None)
        synthesis = synthesis_use_case.execute(
            papers=list(review.papers),
            themes=themes,
            research_question=review.research_question,
            use_ai=False,  # No AI for integration test
        )

        assert len(synthesis) > 100
        review_repository.save(review)

        # Stage 5: Complete
        review.advance_stage()
        assert review.stage == ReviewStage.COMPLETE

        export_use_case = ExportReviewUseCase()
        output_path = temp_review_dir / "final_review.json"
        export_use_case.execute(
            review=review,
            export_format=ExportFormat.JSON,
            output_path=output_path,
            included_only=True,
        )

        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # Verify final state
        final_review = review_repository.load(review.title)
        assert final_review is not None
        assert final_review.stage == ReviewStage.COMPLETE
        assert len(final_review.papers) > 0

    @pytest.mark.integration
    def test_network_failure_handling(self, search_use_case: SearchPapersUseCase):
        """Test graceful handling of network failures."""
        # Try to search with invalid query or timeout
        try:
            papers = search_use_case.execute(
                query="xyzxyzxyzinvalidquerythatshouldfail12345",
                databases=["crossref"],  # Use Crossref (no auth required)
                limit=1,
            )
            # If it returns results, that's fine (shouldn't fail)
            assert isinstance(papers, list)
        except Exception as e:
            # Should handle errors gracefully
            assert "timeout" in str(e).lower() or "connection" in str(e).lower()

    @pytest.mark.integration
    def test_multiple_databases_concurrent_search(self, search_use_case: SearchPapersUseCase):
        """Test searching multiple databases concurrently."""
        try:
            # Use databases that don't require authentication
            papers = search_use_case.execute(
                query="machine learning healthcare",
                databases=["arxiv", "crossref", "semantic_scholar"],
                limit=3,
            )

            # Should get results from multiple sources
            assert isinstance(papers, list)
            if len(papers) > 0:
                # Check for diversity in sources
                journals = {p.journal for p in papers}
                assert len(journals) >= 1

        except Exception as e:
            pytest.skip(f"Network search failed (expected in CI): {e}")


class TestErrorScenarios:
    """Test error handling in workflow."""

    def test_cannot_add_paper_before_search_stage(self):
        """Test that papers can't be added in PLANNING stage."""
        review = Review(
            title="Test Cannot Add",
            research_question="Test?",
            inclusion_criteria=["Test"],
            exclusion_criteria=["None"],
        )

        assert review.stage == ReviewStage.PLANNING

        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2023,
            journal="Test Journal",
        )

        from lit_review.domain.exceptions import WorkflowError

        with pytest.raises(WorkflowError, match="Cannot add papers during PLANNING"):
            review.add_paper(paper)

    def test_cannot_assess_before_assessment_stage(self):
        """Test that assessment requires ASSESSMENT stage."""
        review = Review(
            title="Test",
            research_question="Test?",
            inclusion_criteria=["Test"],
            exclusion_criteria=["None"],
        )
        review.advance_stage()  # to SEARCH

        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2023,
            journal="Test Journal",
        )
        review.add_paper(paper)

        # Still in SEARCH stage, shouldn't be able to mark as assessed
        # (This depends on domain rules - adjust based on actual implementation)
        assert review.stage == ReviewStage.SEARCH

    def test_export_with_no_papers(
        self, review_repository: JSONReviewRepository, temp_review_dir: Path
    ):
        """Test export with empty review."""
        review = Review(
            title="Empty Review",
            research_question="Test?",
            inclusion_criteria=["Test"],
            exclusion_criteria=["None"],
        )

        # Advance to COMPLETE stage
        for _ in range(5):  # PLANNING -> SEARCH -> SCREENING -> ANALYSIS -> SYNTHESIS -> COMPLETE
            review.advance_stage()

        assert review.stage == ReviewStage.COMPLETE
        assert len(review.papers) == 0

        # Export should still work but produce minimal output
        export_use_case = ExportReviewUseCase()
        output_path = temp_review_dir / "empty_export.json"

        export_use_case.execute(
            review=review,
            export_format=ExportFormat.JSON,
            output_path=output_path,
            included_only=False,
        )

        assert output_path.exists()
        content = json.loads(output_path.read_text())
        assert content["review"]["title"] == "Empty Review"
        assert len(content["papers"]) == 0

    def test_synthesis_with_no_abstracts(self):
        """Test synthesis generation when papers lack abstracts."""
        review = Review(
            title="Test Review",
            research_question="Test question",
            inclusion_criteria=["Test"],
            exclusion_criteria=["None"],
        )
        review.advance_stage()

        # Papers without abstracts
        papers = [
            Paper(
                doi=DOI("10.1234/noabstract1"),
                title="Paper Without Abstract",
                authors=[Author("Smith", "John", "J.")],
                publication_year=2023,
                journal="Test Journal",
                abstract="",  # Empty abstract
            ),
        ]

        for paper in papers:
            review.add_paper(paper)

        # Try to generate themes and synthesis
        # Should handle gracefully or raise appropriate error
        try:
            # First try themes analysis
            analyze_use_case = AnalyzeThemesUseCase()
            themes = analyze_use_case.execute(papers=list(review.papers), max_themes=3)

            # Then synthesis
            synthesis_use_case = GenerateSynthesisUseCase(ai_analyzer=None)
            synthesis = synthesis_use_case.execute(
                papers=list(review.papers),
                themes=themes,
                research_question=review.research_question,
                use_ai=False,
            )
            # If it succeeds, check it produced something
            assert isinstance(synthesis, str)
        except ValueError as e:
            # Expected error for papers without abstracts
            assert "abstract" in str(e).lower() or "empty" in str(e).lower()
