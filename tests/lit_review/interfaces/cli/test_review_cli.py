# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for review CLI."""

import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from lit_review.domain.entities.paper import Paper
from lit_review.domain.entities.review import Review, ReviewStage
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI
from lit_review.infrastructure.persistence.json_repository import JSONReviewRepository
from lit_review.interfaces.cli.review_cli import review


@pytest.fixture
def runner() -> CliRunner:
    """Create CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_data_dir(monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create temp data directory and set env var."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setenv("LIT_REVIEW_DATA_DIR", tmpdir)
        yield Path(tmpdir)


class TestInitCommand:
    """Tests for init command."""

    def test_init_creates_review(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """init creates a new review."""
        result = runner.invoke(
            review,
            ["init", "Test Review", "-q", "What is the impact?"],
        )

        assert result.exit_code == 0
        assert "Created review: Test Review" in result.output

    def test_init_with_criteria(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """init accepts multiple criteria."""
        result = runner.invoke(
            review,
            [
                "init",
                "Test Review",
                "-q",
                "Question",
                "-i",
                "Peer-reviewed",
                "-i",
                "English",
                "-e",
                "Conference papers",
            ],
        )

        assert result.exit_code == 0

        # Verify saved review
        repo = JSONReviewRepository(temp_data_dir)
        loaded = repo.load("Test Review")
        assert "Peer-reviewed" in loaded.inclusion_criteria
        assert "English" in loaded.inclusion_criteria
        assert "Conference papers" in loaded.exclusion_criteria

    def test_init_fails_if_exists(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """init fails if review already exists."""
        # Create first
        runner.invoke(review, ["init", "Test Review", "-q", "Question"])

        # Try to create again
        result = runner.invoke(review, ["init", "Test Review", "-q", "Different question"])

        assert result.exit_code == 1
        assert "already exists" in result.output


class TestStatusCommand:
    """Tests for status command."""

    def test_status_shows_review_info(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """status shows review information."""
        # Create review
        runner.invoke(review, ["init", "Test Review", "-q", "What is the impact?"])

        result = runner.invoke(review, ["status", "Test Review"])

        assert result.exit_code == 0
        assert "Test Review" in result.output
        assert "What is the impact?" in result.output
        assert "PLANNING" in result.output

    def test_status_shows_paper_counts(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """status shows paper statistics."""
        # Create review with papers
        repo = JSONReviewRepository(temp_data_dir)
        test_review = Review(
            title="Test Review",
            research_question="Question",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        test_review.advance_stage()

        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )
        test_review.add_paper(paper)
        repo.save(test_review)

        result = runner.invoke(review, ["status", "Test Review"])

        assert result.exit_code == 0
        assert "Total: 1" in result.output

    def test_status_fails_if_not_found(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """status fails for nonexistent review."""
        result = runner.invoke(review, ["status", "Nonexistent"])

        assert result.exit_code == 1
        assert "not found" in result.output


class TestAdvanceCommand:
    """Tests for advance command."""

    def test_advance_moves_to_next_stage(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """advance moves review to next stage."""
        runner.invoke(review, ["init", "Test Review", "-q", "Question"])

        result = runner.invoke(review, ["advance", "Test Review"])

        assert result.exit_code == 0
        assert "PLANNING" in result.output
        assert "SEARCH" in result.output

        # Verify stage changed
        repo = JSONReviewRepository(temp_data_dir)
        loaded = repo.load("Test Review")
        assert loaded.stage == ReviewStage.SEARCH


class TestExportCommand:
    """Tests for export command."""

    def test_export_creates_file(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """export creates output file."""
        # Create review with paper
        repo = JSONReviewRepository(temp_data_dir)
        test_review = Review(
            title="Test Review",
            research_question="Question",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        test_review.advance_stage()

        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )
        paper.assess(8.0, include=True)
        test_review.add_paper(paper)
        repo.save(test_review)

        output_file = temp_data_dir / "output.bib"
        result = runner.invoke(
            review, ["export", "Test Review", "-f", "bibtex", "-o", str(output_file)]
        )

        assert result.exit_code == 0
        assert output_file.exists()
        assert "Export complete" in result.output
        assert "1 papers" in result.output


class TestListCommand:
    """Tests for list command."""

    def test_list_shows_reviews(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """list shows all reviews."""
        runner.invoke(review, ["init", "Review One", "-q", "Question 1"])
        runner.invoke(review, ["init", "Review Two", "-q", "Question 2"])

        result = runner.invoke(review, ["list"])

        assert result.exit_code == 0
        assert "Review_One" in result.output
        assert "Review_Two" in result.output

    def test_list_empty(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """list handles empty directory."""
        result = runner.invoke(review, ["list"])

        assert result.exit_code == 0
        assert "No reviews found" in result.output


class TestDeleteCommand:
    """Tests for delete command."""

    def test_delete_removes_review(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """delete removes review."""
        runner.invoke(review, ["init", "Test Review", "-q", "Question"])

        result = runner.invoke(review, ["delete", "Test Review", "--yes"])

        assert result.exit_code == 0
        assert "Deleted review" in result.output

        # Verify deleted
        repo = JSONReviewRepository(temp_data_dir)
        assert not repo.exists("Test Review")


class TestAssessCommand:
    """Tests for assess command."""

    def test_assess_single_paper(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """assess evaluates a single paper."""
        # Create review with paper
        repo = JSONReviewRepository(temp_data_dir)
        test_review = Review(
            title="Test Review",
            research_question="Question",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        test_review.advance_stage()

        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
            abstract="This is a test abstract.",
        )
        test_review.add_paper(paper)
        repo.save(test_review)

        result = runner.invoke(
            review,
            [
                "assess",
                "Test Review",
                "--doi",
                "10.1234/test",
                "--score",
                "8.5",
                "--include",
            ],
        )

        assert result.exit_code == 0
        assert "INCLUDED" in result.output
        assert "8.5/10" in result.output

        # Verify assessment saved
        loaded = repo.load("Test Review")
        assessed_paper = loaded.get_paper_by_doi(DOI("10.1234/test"))
        assert assessed_paper is not None
        assert assessed_paper.quality_score == 8.5
        assert assessed_paper.included is True

    def test_assess_batch(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """assess handles batch assessment from CSV."""
        # Create review with papers
        repo = JSONReviewRepository(temp_data_dir)
        test_review = Review(
            title="Test Review",
            research_question="Question",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        test_review.advance_stage()

        paper1 = Paper(
            doi=DOI("10.1234/test1"),
            title="Test Paper 1",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )
        paper2 = Paper(
            doi=DOI("10.1234/test2"),
            title="Test Paper 2",
            authors=[Author("Jones", "Jane", "J.")],
            publication_year=2024,
            journal="Journal",
        )
        test_review.add_paper(paper1)
        test_review.add_paper(paper2)
        repo.save(test_review)

        # Create CSV file
        csv_file = temp_data_dir / "batch.csv"
        csv_file.write_text(
            "doi,score,include,notes\n10.1234/test1,8.0,yes,Good\n10.1234/test2,6.0,no,Limited"
        )

        result = runner.invoke(
            review,
            ["assess", "Test Review", "--batch", str(csv_file)],
        )

        assert result.exit_code == 0
        assert "2 papers assessed" in result.output

    def test_assess_fails_without_doi(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """assess fails if DOI not specified."""
        runner.invoke(review, ["init", "Test Review", "-q", "Question"])

        result = runner.invoke(
            review,
            ["assess", "Test Review", "--score", "8.0", "--include"],
        )

        assert result.exit_code == 1
        assert "Must specify --doi" in result.output


class TestAnalyzeCommand:
    """Tests for analyze command."""

    def test_analyze_extracts_themes(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """analyze extracts themes from papers."""
        # Create review with included papers
        repo = JSONReviewRepository(temp_data_dir)
        test_review = Review(
            title="Test Review",
            research_question="Question",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        test_review.advance_stage()

        for i in range(5):
            paper = Paper(
                doi=DOI(f"10.1234/test{i}"),
                title=f"Machine Learning Paper {i}",
                authors=[Author("Smith", "John", "J.")],
                publication_year=2024,
                journal="Journal",
                abstract="Machine learning and artificial intelligence in healthcare diagnosis.",
            )
            paper.assess(8.0, True)
            test_review.add_paper(paper)
        repo.save(test_review)

        result = runner.invoke(
            review,
            ["analyze", "Test Review", "--clusters", "3"],
        )

        assert result.exit_code == 0
        assert "Theme Analysis Results" in result.output
        assert "Theme" in result.output

    def test_analyze_fails_without_included_papers(
        self, runner: CliRunner, temp_data_dir: Path
    ) -> None:
        """analyze fails if no included papers."""
        runner.invoke(review, ["init", "Test Review", "-q", "Question"])

        result = runner.invoke(review, ["analyze", "Test Review"])

        assert result.exit_code == 1
        assert "No included papers" in result.output


class TestSynthesizeCommand:
    """Tests for synthesize command."""

    def test_synthesize_creates_markdown(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """synthesize generates markdown synthesis."""
        # Create review with included papers
        repo = JSONReviewRepository(temp_data_dir)
        test_review = Review(
            title="Test Review",
            research_question="What is the impact of ML?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        test_review.advance_stage()

        for i in range(3):
            paper = Paper(
                doi=DOI(f"10.1234/test{i}"),
                title=f"Test Paper {i}",
                authors=[Author("Smith", "John", "J.")],
                publication_year=2024,
                journal="Journal",
                abstract="This is a test abstract about machine learning.",
            )
            paper.assess(8.0, True)
            test_review.add_paper(paper)
        repo.save(test_review)

        output_file = temp_data_dir / "synthesis.md"
        result = runner.invoke(
            review,
            ["synthesize", "Test Review", "-o", str(output_file)],
        )

        assert result.exit_code == 0
        assert "Synthesis complete" in result.output
        assert output_file.exists()

        # Check content
        content = output_file.read_text()
        assert "Literature Review Synthesis" in content
        assert "What is the impact of ML?" in content

    def test_synthesize_fails_without_papers(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """synthesize fails if no included papers."""
        runner.invoke(review, ["init", "Test Review", "-q", "Question"])

        output_file = temp_data_dir / "synthesis.md"
        result = runner.invoke(
            review,
            ["synthesize", "Test Review", "-o", str(output_file)],
        )

        assert result.exit_code == 1
        assert "No included papers" in result.output


class TestExportCommandEnhanced:
    """Tests for enhanced export command."""

    def test_export_multiple_formats(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """export creates multiple format files."""
        # Create review with paper
        repo = JSONReviewRepository(temp_data_dir)
        test_review = Review(
            title="Test Review",
            research_question="Question",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        test_review.advance_stage()

        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )
        paper.assess(8.0, True)
        test_review.add_paper(paper)
        repo.save(test_review)

        outdir = temp_data_dir / "exports"
        result = runner.invoke(
            review,
            [
                "export",
                "Test Review",
                "-f",
                "bibtex",
                "-f",
                "json",
                "-f",
                "html",
                "--outdir",
                str(outdir),
            ],
        )

        assert result.exit_code == 0
        assert "Export complete" in result.output
        assert (outdir / "Test_Review.bib").exists()
        assert (outdir / "Test_Review.json").exists()
        assert (outdir / "Test_Review.html").exists()

    def test_export_html_format(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """export creates HTML file."""
        # Create review with paper
        repo = JSONReviewRepository(temp_data_dir)
        test_review = Review(
            title="Test Review",
            research_question="Question",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        test_review.advance_stage()

        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )
        paper.assess(8.0, True)
        test_review.add_paper(paper)
        repo.save(test_review)

        output_file = temp_data_dir / "output.html"
        result = runner.invoke(
            review, ["export", "Test Review", "-f", "html", "-o", str(output_file)]
        )

        assert result.exit_code == 0
        assert output_file.exists()

        # Check HTML content
        content = output_file.read_text()
        assert "<!DOCTYPE html>" in content
        assert "Test Paper" in content


class TestSearchCommandEnhanced:
    """Tests for enhanced search command with progress."""

    def test_search_shows_progress(self, runner: CliRunner, temp_data_dir: Path) -> None:
        """search shows progress indicators."""
        runner.invoke(review, ["init", "Test Review", "-q", "Question"])

        result = runner.invoke(
            review,
            ["search", "Test Review", "-d", "crossref", "-k", "machine learning", "-l", "5"],
        )

        # Should show progress indicators
        assert "Searching Academic Databases" in result.output
        assert "crossref" in result.output
        assert "Search Results" in result.output
