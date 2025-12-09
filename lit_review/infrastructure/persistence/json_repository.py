"""JSON file-based repository for review persistence.

Implements the PaperRepository port with JSON file storage,
atomic writes, automatic backups, file locking, and soft delete.
"""

import fcntl
import json
import shutil
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from lit_review.application.ports.paper_repository import PaperRepository
from lit_review.domain.entities.paper import Paper
from lit_review.domain.entities.review import Review, ReviewStage
from lit_review.domain.exceptions import EntityNotFoundError
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


class JSONReviewRepository(PaperRepository):
    """JSON file-based repository with atomic writes and backups.

    Stores reviews as JSON files with:
    - Atomic writes (temp file + rename pattern)
    - Automatic backups (keeps last 5 in .backups/)
    - File locking for concurrent access
    - Soft delete with 30-day retention in .deleted/

    Attributes:
        data_dir: Directory for storing review JSON files.
        backup_dir: Directory for backup files.
        deleted_dir: Directory for soft-deleted files.
        max_backups: Maximum number of backups to retain (default 5).

    Example:
        >>> repo = JSONReviewRepository(Path("./data"))
        >>> repo.save(review)
        >>> loaded = repo.load("my-review")
    """

    def __init__(self, data_dir: Path, max_backups: int = 5) -> None:
        """Initialize repository.

        Args:
            data_dir: Directory for storing review files.
            max_backups: Maximum number of backups to retain per file.
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.backup_dir = self.data_dir / ".backups"
        self.backup_dir.mkdir(exist_ok=True)

        self.deleted_dir = self.data_dir / ".deleted"
        self.deleted_dir.mkdir(exist_ok=True)

        self.max_backups = max_backups

    def _get_review_path(self, review_id: str) -> Path:
        """Get path to review JSON file.

        Args:
            review_id: Review identifier.

        Returns:
            Path to review JSON file.
        """
        # Sanitize review_id for filename
        safe_id = review_id.replace(" ", "_").replace("/", "_")
        return self.data_dir / f"{safe_id}.json"

    def save(self, review: Review) -> None:
        """Persist review to JSON file with atomic write and backup.

        Args:
            review: Review to save.

        Raises:
            IOError: If unable to write file.
        """
        path = self._get_review_path(review.title)

        # Create backup if file exists
        if path.exists():
            self._create_backup(path)

        # Serialize review
        data = self._serialize_review(review)

        # Atomic write: write to temp file, then rename
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".json",
                dir=self.data_dir,
                delete=False,
            ) as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                temp_path = Path(f.name)

            temp_path.rename(path)
        except Exception as e:
            # Clean up temp file if rename failed
            if "temp_path" in locals() and temp_path.exists():
                temp_path.unlink()
            raise OSError(f"Failed to save review: {e}") from e

    def _create_backup(self, path: Path) -> None:
        """Create timestamped backup of file.

        Args:
            path: Path to file to backup.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{path.stem}_{timestamp}.json"
        backup_path = self.backup_dir / backup_name

        shutil.copy(path, backup_path)

        # Clean up old backups
        self._cleanup_old_backups(path.stem)

    def _cleanup_old_backups(self, review_id: str) -> None:
        """Remove old backups, keeping only max_backups most recent.

        Args:
            review_id: Review identifier (stem of filename).
        """
        # Find all backups for this review
        backups = sorted(
            self.backup_dir.glob(f"{review_id}_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        # Remove excess backups
        for backup in backups[self.max_backups :]:
            backup.unlink()

    def load(self, review_id: str) -> Review:
        """Load review from JSON file with file locking.

        Args:
            review_id: Review identifier (title).

        Returns:
            Loaded Review entity.

        Raises:
            EntityNotFoundError: If review not found.
            IOError: If unable to read file.
        """
        path = self._get_review_path(review_id)

        if not path.exists():
            raise EntityNotFoundError(f"Review '{review_id}' not found")

        try:
            with open(path, encoding="utf-8") as f:
                # Acquire shared lock for reading
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                try:
                    data = json.load(f)
                    return self._deserialize_review(data)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except json.JSONDecodeError as e:
            raise OSError(f"Invalid JSON in review file: {e}") from e

    def delete(self, review_id: str) -> None:
        """Soft delete review file (move to .deleted/ with 30-day retention).

        Args:
            review_id: Review identifier.

        Raises:
            EntityNotFoundError: If review not found.
        """
        path = self._get_review_path(review_id)

        if not path.exists():
            raise EntityNotFoundError(f"Review '{review_id}' not found")

        # Move to deleted directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        deleted_name = f"{path.stem}_{timestamp}.json"
        deleted_path = self.deleted_dir / deleted_name

        shutil.move(str(path), str(deleted_path))

        # Clean up old deleted files (30 days)
        self._cleanup_deleted_files()

    def _cleanup_deleted_files(self) -> None:
        """Remove deleted files older than 30 days."""
        cutoff = datetime.now() - timedelta(days=30)

        for deleted_file in self.deleted_dir.glob("*.json"):
            if datetime.fromtimestamp(deleted_file.stat().st_mtime) < cutoff:
                deleted_file.unlink()

    def list_reviews(self) -> list[str]:
        """List all review IDs.

        Returns:
            List of review identifiers.
        """
        return [p.stem for p in self.data_dir.glob("*.json") if not p.name.endswith(".bak")]

    def exists(self, review_id: str) -> bool:
        """Check if review exists.

        Args:
            review_id: Review identifier.

        Returns:
            True if review exists.
        """
        return self._get_review_path(review_id).exists()

    def _serialize_review(self, review: Review) -> dict[str, Any]:
        """Serialize Review to dictionary.

        Args:
            review: Review to serialize.

        Returns:
            Dictionary representation.
        """
        return {
            "title": review.title,
            "research_question": review.research_question,
            "inclusion_criteria": review.inclusion_criteria,
            "exclusion_criteria": review.exclusion_criteria,
            "stage": review.stage.value,
            "papers": [self._serialize_paper(p) for p in review.papers],
        }

    def _serialize_paper(self, paper: Paper) -> dict[str, Any]:
        """Serialize Paper to dictionary.

        Args:
            paper: Paper to serialize.

        Returns:
            Dictionary representation.
        """
        return {
            "doi": paper.doi.value,
            "title": paper.title,
            "authors": [
                {
                    "last_name": a.last_name,
                    "first_name": a.first_name,
                    "initials": a.initials,
                    "orcid": a.orcid,
                }
                for a in paper.authors
            ],
            "publication_year": paper.publication_year,
            "journal": paper.journal,
            "abstract": paper.abstract,
            "keywords": paper.keywords,
            "quality_score": paper.quality_score,
            "included": paper.included,
            "assessment_notes": paper.assessment_notes,
        }

    def _deserialize_review(self, data: dict[str, Any]) -> Review:
        """Deserialize dictionary to Review.

        Args:
            data: Dictionary representation.

        Returns:
            Review entity.
        """
        review = Review(
            title=data["title"],
            research_question=data["research_question"],
            inclusion_criteria=data["inclusion_criteria"],
            exclusion_criteria=data.get("exclusion_criteria", []),
            stage=ReviewStage(data.get("stage", "planning")),
        )

        # Add papers
        for paper_data in data.get("papers", []):
            paper = self._deserialize_paper(paper_data)
            # Bypass stage check by directly adding to set
            review.papers.add(paper)

        return review

    def _deserialize_paper(self, data: dict[str, Any]) -> Paper:
        """Deserialize dictionary to Paper.

        Args:
            data: Dictionary representation.

        Returns:
            Paper entity.
        """
        authors = [
            Author(
                last_name=a["last_name"],
                first_name=a["first_name"],
                initials=a["initials"],
                orcid=a.get("orcid"),
            )
            for a in data["authors"]
        ]

        paper = Paper(
            doi=DOI(data["doi"]),
            title=data["title"],
            authors=authors,
            publication_year=data["publication_year"],
            journal=data["journal"],
            abstract=data.get("abstract", ""),
            keywords=data.get("keywords", []),
            quality_score=data.get("quality_score"),
            included=data.get("included"),
            assessment_notes=data.get("assessment_notes", ""),
        )

        return paper

    def recover_from_backup(self, review_id: str, backup_index: int = 0) -> Review:
        """Recover review from backup.

        Args:
            review_id: Review identifier.
            backup_index: Index of backup to recover (0 = most recent).

        Returns:
            Recovered Review entity.

        Raises:
            EntityNotFoundError: If no backups found.
            IOError: If unable to read backup.
        """
        # Find backups for this review
        safe_id = review_id.replace(" ", "_").replace("/", "_")
        backups = sorted(
            self.backup_dir.glob(f"{safe_id}_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        if not backups or backup_index >= len(backups):
            raise EntityNotFoundError(
                f"No backup found for review '{review_id}' at index {backup_index}"
            )

        backup_path = backups[backup_index]

        try:
            data = json.loads(backup_path.read_text(encoding="utf-8"))
            return self._deserialize_review(data)
        except json.JSONDecodeError as e:
            raise OSError(f"Invalid JSON in backup file: {e}") from e
