"""JSON file-based repository for review persistence.

Implements the PaperRepository port with JSON file storage,
atomic writes, and automatic backups.
"""

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

from lit_review.application.ports.paper_repository import PaperRepository
from lit_review.domain.entities.paper import Paper
from lit_review.domain.entities.review import Review, ReviewStage
from lit_review.domain.exceptions import EntityNotFoundError
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


class JSONReviewRepository(PaperRepository):
    """JSON file-based repository with atomic writes.

    Stores reviews as JSON files with automatic backup on overwrite.
    Uses atomic write pattern (temp file + rename) for data integrity.

    Attributes:
        data_dir: Directory for storing review JSON files.

    Example:
        >>> repo = JSONReviewRepository(Path("./data"))
        >>> repo.save(review)
        >>> loaded = repo.load("my-review")
    """

    def __init__(self, data_dir: Path) -> None:
        """Initialize repository.

        Args:
            data_dir: Directory for storing review files.
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

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
        """Persist review to JSON file with atomic write.

        Args:
            review: Review to save.

        Raises:
            IOError: If unable to write file.
        """
        path = self._get_review_path(review.title)

        # Create backup if file exists
        if path.exists():
            backup_path = path.with_suffix(".json.bak")
            shutil.copy(path, backup_path)

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

    def load(self, review_id: str) -> Review:
        """Load review from JSON file.

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
            data = json.loads(path.read_text(encoding="utf-8"))
            return self._deserialize_review(data)
        except json.JSONDecodeError as e:
            raise OSError(f"Invalid JSON in review file: {e}") from e

    def delete(self, review_id: str) -> None:
        """Delete review file.

        Args:
            review_id: Review identifier.

        Raises:
            EntityNotFoundError: If review not found.
        """
        path = self._get_review_path(review_id)

        if not path.exists():
            raise EntityNotFoundError(f"Review '{review_id}' not found")

        path.unlink()

        # Also delete backup if exists
        backup_path = path.with_suffix(".json.bak")
        if backup_path.exists():
            backup_path.unlink()

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
