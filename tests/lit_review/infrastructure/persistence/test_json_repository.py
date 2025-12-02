"""Tests for JSONReviewRepository."""

import json
import tempfile
from pathlib import Path

import pytest

from lit_review.domain.entities.paper import Paper
from lit_review.domain.entities.review import Review, ReviewStage
from lit_review.domain.exceptions import EntityNotFoundError
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI
from lit_review.infrastructure.persistence.json_repository import JSONReviewRepository


@pytest.fixture
def temp_data_dir() -> Path:
    """Create temporary data directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def repository(temp_data_dir: Path) -> JSONReviewRepository:
    """Create repository with temp directory."""
    return JSONReviewRepository(temp_data_dir)


@pytest.fixture
def sample_review() -> Review:
    """Create sample review."""
    return Review(
        title="Test Review",
        research_question="What is the impact?",
        inclusion_criteria=["Peer-reviewed"],
        exclusion_criteria=["Conference abstracts"],
    )


@pytest.fixture
def sample_paper() -> Paper:
    """Create sample paper."""
    return Paper(
        doi=DOI("10.1234/test"),
        title="Test Paper",
        authors=[Author("Smith", "John", "J.")],
        publication_year=2024,
        journal="Test Journal",
        abstract="Test abstract",
        keywords=["test", "paper"],
    )


class TestJSONReviewRepository:
    """Tests for JSONReviewRepository."""

    def test_save_creates_file(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """save creates JSON file."""
        repository.save(sample_review)

        path = repository._get_review_path(sample_review.title)
        assert path.exists()

    def test_save_creates_valid_json(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """save creates valid JSON content."""
        repository.save(sample_review)

        path = repository._get_review_path(sample_review.title)
        data = json.loads(path.read_text())

        assert data["title"] == "Test Review"
        assert data["research_question"] == "What is the impact?"
        assert data["inclusion_criteria"] == ["Peer-reviewed"]

    def test_save_creates_backup_on_overwrite(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """save creates backup before overwriting."""
        # Save twice
        repository.save(sample_review)
        sample_review.advance_stage()  # Modify review
        repository.save(sample_review)

        path = repository._get_review_path(sample_review.title)
        backup_path = path.with_suffix(".json.bak")

        assert backup_path.exists()

    def test_load_returns_review(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """load returns saved review."""
        repository.save(sample_review)
        loaded = repository.load(sample_review.title)

        assert loaded.title == sample_review.title
        assert loaded.research_question == sample_review.research_question
        assert loaded.inclusion_criteria == sample_review.inclusion_criteria

    def test_load_preserves_stage(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """load preserves review stage."""
        sample_review.advance_stage()  # Move to SEARCH
        repository.save(sample_review)
        loaded = repository.load(sample_review.title)

        assert loaded.stage == ReviewStage.SEARCH

    def test_load_preserves_papers(
        self,
        repository: JSONReviewRepository,
        sample_review: Review,
        sample_paper: Paper,
    ) -> None:
        """load preserves papers."""
        sample_review.advance_stage()  # Move to SEARCH
        sample_review.add_paper(sample_paper)
        repository.save(sample_review)

        loaded = repository.load(sample_review.title)

        assert len(loaded.papers) == 1
        paper = list(loaded.papers)[0]
        assert paper.doi.value == "10.1234/test"
        assert paper.title == "Test Paper"
        assert len(paper.authors) == 1
        assert paper.authors[0].last_name == "Smith"

    def test_load_raises_not_found(self, repository: JSONReviewRepository) -> None:
        """load raises EntityNotFoundError for missing review."""
        with pytest.raises(EntityNotFoundError) as exc_info:
            repository.load("nonexistent")

        assert "not found" in str(exc_info.value.message)

    def test_delete_removes_file(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """delete removes review file."""
        repository.save(sample_review)
        repository.delete(sample_review.title)

        assert not repository.exists(sample_review.title)

    def test_delete_raises_not_found(self, repository: JSONReviewRepository) -> None:
        """delete raises EntityNotFoundError for missing review."""
        with pytest.raises(EntityNotFoundError):
            repository.delete("nonexistent")

    def test_list_reviews_empty(self, repository: JSONReviewRepository) -> None:
        """list_reviews returns empty list for empty directory."""
        reviews = repository.list_reviews()
        assert reviews == []

    def test_list_reviews_returns_ids(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """list_reviews returns review IDs."""
        repository.save(sample_review)
        reviews = repository.list_reviews()

        assert len(reviews) == 1
        assert "Test_Review" in reviews

    def test_list_reviews_excludes_backups(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """list_reviews excludes backup files."""
        repository.save(sample_review)
        sample_review.advance_stage()
        repository.save(sample_review)  # Creates backup

        reviews = repository.list_reviews()
        assert len(reviews) == 1  # No backup in list

    def test_exists_true_when_exists(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """exists returns True when review exists."""
        repository.save(sample_review)
        assert repository.exists(sample_review.title)

    def test_exists_false_when_missing(self, repository: JSONReviewRepository) -> None:
        """exists returns False when review missing."""
        assert not repository.exists("nonexistent")


class TestJSONReviewRepositoryPaperSerialization:
    """Tests for paper serialization/deserialization."""

    def test_paper_assessment_preserved(
        self,
        repository: JSONReviewRepository,
        sample_review: Review,
        sample_paper: Paper,
    ) -> None:
        """Paper assessment is preserved through save/load."""
        sample_review.advance_stage()
        sample_paper.assess(8.5, include=True, notes="Good paper")
        sample_review.add_paper(sample_paper)
        repository.save(sample_review)

        loaded = repository.load(sample_review.title)
        paper = list(loaded.papers)[0]

        assert paper.quality_score == 8.5
        assert paper.included is True
        assert paper.assessment_notes == "Good paper"

    def test_paper_keywords_preserved(
        self,
        repository: JSONReviewRepository,
        sample_review: Review,
        sample_paper: Paper,
    ) -> None:
        """Paper keywords are preserved through save/load."""
        sample_review.advance_stage()
        sample_review.add_paper(sample_paper)
        repository.save(sample_review)

        loaded = repository.load(sample_review.title)
        paper = list(loaded.papers)[0]

        assert paper.keywords == ["test", "paper"]

    def test_author_orcid_preserved(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """Author ORCID is preserved through save/load."""
        paper = Paper(
            doi=DOI("10.1234/orcid"),
            title="ORCID Paper",
            authors=[Author("Smith", "John", "J.", "0000-0001-2345-6789")],
            publication_year=2024,
            journal="Journal",
        )

        sample_review.advance_stage()
        sample_review.add_paper(paper)
        repository.save(sample_review)

        loaded = repository.load(sample_review.title)
        loaded_paper = list(loaded.papers)[0]

        assert loaded_paper.authors[0].orcid == "0000-0001-2345-6789"
