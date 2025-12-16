# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Paper entity representing an academic publication.

The Paper entity is the core domain object representing a scholarly article
with metadata, quality assessment, and citation generation capabilities.
"""

from dataclasses import dataclass, field
from datetime import datetime

from lit_review.domain.exceptions import ValidationError
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


@dataclass
class Paper:
    """Academic paper entity with business logic.

    Represents a scholarly publication with full metadata. Papers are uniquely
    identified by their DOI and can be assessed for quality during review.

    Attributes:
        doi: Digital Object Identifier (unique identifier).
        title: Paper title.
        authors: List of paper authors (at least one required).
        publication_year: Year of publication.
        journal: Journal or venue name.
        abstract: Paper abstract (optional).
        keywords: List of keywords (optional).
        quality_score: Assessment score 0-10 (optional).
        included: Whether paper is included in review (optional).
        assessment_notes: Notes from quality assessment (optional).

    Example:
        >>> paper = Paper(
        ...     doi=DOI("10.1234/test"),
        ...     title="Test Paper",
        ...     authors=[Author("Smith", "John", "J.")],
        ...     publication_year=2024,
        ...     journal="Test Journal"
        ... )
    """

    doi: DOI
    title: str
    authors: list[Author]
    publication_year: int
    journal: str
    abstract: str = ""
    keywords: list[str] = field(default_factory=list)
    quality_score: float | None = None
    included: bool | None = None
    assessment_notes: str = ""

    def __post_init__(self) -> None:
        """Validate paper fields on creation."""
        if not self.title or not self.title.strip():
            raise ValidationError("Paper title cannot be empty")

        if not self.authors:
            raise ValidationError("Paper must have at least one author")

        if not self.journal or not self.journal.strip():
            raise ValidationError("Paper journal cannot be empty")

        current_year = datetime.now().year
        if self.publication_year < 1900 or self.publication_year > current_year:
            raise ValidationError(
                f"Publication year must be between 1900 and {current_year}, "
                f"got {self.publication_year}"
            )

        if self.quality_score is not None:
            self._validate_quality_score(self.quality_score)

    def _validate_quality_score(self, score: float) -> None:
        """Validate quality score is in valid range."""
        if score < 0 or score > 10:
            raise ValidationError(f"Quality score must be between 0 and 10, got {score}")

    def set_quality_score(self, score: float) -> None:
        """Set the quality assessment score.

        Args:
            score: Quality score between 0 and 10.

        Raises:
            ValidationError: If score is out of range.
        """
        self._validate_quality_score(score)
        self.quality_score = score

    def assess(self, score: float, include: bool, notes: str = "") -> None:
        """Assess paper for quality and inclusion.

        Args:
            score: Quality score between 0 and 10.
            include: Whether to include paper in review.
            notes: Optional assessment notes.

        Raises:
            ValidationError: If score is out of range.
        """
        self._validate_quality_score(score)
        self.quality_score = score
        self.included = include
        self.assessment_notes = notes

    def get_citation_key(self) -> str:
        """Generate citation key for BibTeX.

        Format: AuthorYear for single author, Author1Author2Year for two authors,
        AuthorEtAlYear for three or more authors.

        Returns:
            Citation key string.

        Example:
            >>> paper.get_citation_key()
            'SmithEtAl2024'
        """
        if not self.authors:
            return f"Unknown{self.publication_year}"

        if len(self.authors) == 1:
            return f"{self.authors[0].last_name}{self.publication_year}"
        elif len(self.authors) == 2:
            return f"{self.authors[0].last_name}{self.authors[1].last_name}{self.publication_year}"
        else:
            return f"{self.authors[0].last_name}EtAl{self.publication_year}"

    def is_assessed(self) -> bool:
        """Check if paper has been assessed.

        Returns:
            True if paper has a quality score and inclusion decision.
        """
        return self.quality_score is not None and self.included is not None

    def __eq__(self, other: object) -> bool:
        """Papers are equal if they have the same DOI."""
        if not isinstance(other, Paper):
            return NotImplemented
        return self.doi == other.doi

    def __hash__(self) -> int:
        """Hash based on DOI for use in sets."""
        return hash(self.doi)
