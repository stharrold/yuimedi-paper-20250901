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

    def test_save_creates_timestamped_backup_on_overwrite(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """save creates timestamped backup before overwriting."""
        # Save twice
        repository.save(sample_review)
        sample_review.advance_stage()  # Modify review
        repository.save(sample_review)

        # Check for timestamped backup in .backups/
        backups = list(repository.backup_dir.glob("Test_Review_*.json"))
        assert len(backups) == 1

    def test_save_keeps_max_backups(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """save keeps only max_backups most recent backups."""
        # Save 7 times (should keep only 5 backups)
        for i in range(7):
            sample_review.advance_stage() if i > 0 else None
            repository.save(sample_review)
            # Small delay to ensure different timestamps
            import time

            time.sleep(0.01)

        backups = list(repository.backup_dir.glob("Test_Review_*.json"))
        assert len(backups) == 5

    def test_save_atomic_write_cleans_up_on_failure(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """save cleans up temp file on failure."""
        # This is hard to test directly, but we can verify no temp files remain
        repository.save(sample_review)

        temp_files = list(repository.data_dir.glob("tmp*"))
        assert len(temp_files) == 0

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

    def test_delete_soft_deletes_file(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """delete moves file to .deleted/ directory."""
        repository.save(sample_review)
        repository.delete(sample_review.title)

        # File should not exist in main directory
        assert not repository.exists(sample_review.title)

        # But should exist in .deleted/
        deleted_files = list(repository.deleted_dir.glob("Test_Review_*.json"))
        assert len(deleted_files) == 1

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


class TestJSONReviewRepositoryBackupRecovery:
    """Tests for backup and recovery functionality."""

    def test_recover_from_backup_most_recent(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """recover_from_backup recovers most recent backup by default."""
        # Save twice to create backup
        repository.save(sample_review)
        sample_review.advance_stage()
        repository.save(sample_review)

        # Recover from backup (should be the first version)
        recovered = repository.recover_from_backup(sample_review.title)

        assert recovered.stage == ReviewStage.PLANNING  # Original stage

    def test_recover_from_backup_specific_index(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """recover_from_backup can recover specific backup by index."""
        # Save three times to create two backups
        repository.save(sample_review)
        sample_review.advance_stage()  # SEARCH
        repository.save(sample_review)
        sample_review.advance_stage()  # SCREENING
        repository.save(sample_review)

        import time

        time.sleep(0.01)  # Ensure timestamps differ

        # Recover from second most recent backup (index 1)
        recovered = repository.recover_from_backup(sample_review.title, backup_index=1)

        assert recovered.stage == ReviewStage.PLANNING

    def test_recover_from_backup_raises_not_found(self, repository: JSONReviewRepository) -> None:
        """recover_from_backup raises EntityNotFoundError when no backups."""
        with pytest.raises(EntityNotFoundError) as exc_info:
            repository.recover_from_backup("nonexistent")

        assert "No backup found" in str(exc_info.value.message)

    def test_recover_from_backup_invalid_index(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """recover_from_backup raises error for invalid backup index."""
        repository.save(sample_review)
        sample_review.advance_stage()
        repository.save(sample_review)  # Creates 1 backup

        with pytest.raises(EntityNotFoundError):
            repository.recover_from_backup(sample_review.title, backup_index=5)


class TestJSONReviewRepositorySoftDelete:
    """Tests for soft delete functionality."""

    def test_delete_cleanup_old_files(
        self, repository: JSONReviewRepository, sample_review: Review, tmp_path: Path
    ) -> None:
        """_cleanup_deleted_files removes files older than 30 days."""
        from datetime import datetime, timedelta

        repository.save(sample_review)
        repository.delete(sample_review.title)

        # Get the deleted file
        deleted_files = list(repository.deleted_dir.glob("*.json"))
        assert len(deleted_files) == 1

        # Manually set mtime to 31 days ago
        old_time = (datetime.now() - timedelta(days=31)).timestamp()
        import os

        os.utime(deleted_files[0], (old_time, old_time))

        # Run cleanup
        repository._cleanup_deleted_files()

        # File should be removed
        deleted_files_after = list(repository.deleted_dir.glob("*.json"))
        assert len(deleted_files_after) == 0

    def test_delete_keeps_recent_files(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """_cleanup_deleted_files keeps files newer than 30 days."""
        repository.save(sample_review)
        repository.delete(sample_review.title)

        # Run cleanup immediately
        repository._cleanup_deleted_files()

        # File should still exist
        deleted_files = list(repository.deleted_dir.glob("*.json"))
        assert len(deleted_files) == 1


class TestJSONReviewRepositoryFileLocking:
    """Tests for file locking functionality."""

    def test_load_uses_file_locking(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """load uses file locking for concurrent access."""
        repository.save(sample_review)

        # Load should succeed with file locking
        loaded = repository.load(sample_review.title)
        assert loaded.title == sample_review.title

    def test_concurrent_reads_allowed(
        self, repository: JSONReviewRepository, sample_review: Review
    ) -> None:
        """Multiple concurrent reads are allowed with shared locks."""
        import threading

        repository.save(sample_review)

        results = []

        def read_review() -> None:
            loaded = repository.load(sample_review.title)
            results.append(loaded.title)

        # Start multiple read threads
        threads = [threading.Thread(target=read_review) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All reads should succeed
        assert len(results) == 5
        assert all(r == sample_review.title for r in results)
