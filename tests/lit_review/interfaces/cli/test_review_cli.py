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
        assert "Exported 1 papers" in result.output


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
