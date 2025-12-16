# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Review entity with workflow stage enforcement.

The Review entity manages a systematic literature review, enforcing workflow
stages and tracking papers through the review process.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from lit_review.domain.entities.paper import Paper
from lit_review.domain.exceptions import ValidationError, WorkflowError
from lit_review.domain.values.doi import DOI


class ReviewStage(Enum):
    """Workflow stages for a literature review.

    Stages must be followed in order:
    PLANNING -> SEARCH -> SCREENING -> ANALYSIS -> SYNTHESIS -> COMPLETE
    """

    PLANNING = "planning"
    SEARCH = "search"
    SCREENING = "screening"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    COMPLETE = "complete"


# Define valid stage transitions
STAGE_ORDER = [
    ReviewStage.PLANNING,
    ReviewStage.SEARCH,
    ReviewStage.SCREENING,
    ReviewStage.ANALYSIS,
    ReviewStage.SYNTHESIS,
    ReviewStage.COMPLETE,
]


@dataclass
class Review:
    """Literature review entity with workflow stage enforcement.

    Manages a systematic literature review with research question, inclusion/
    exclusion criteria, and a collection of papers. Enforces workflow stages
    to ensure proper review methodology.

    Attributes:
        title: Review title.
        research_question: The main research question.
        inclusion_criteria: List of inclusion criteria.
        exclusion_criteria: List of exclusion criteria.
        stage: Current workflow stage.
        papers: Set of papers in the review.

    Example:
        >>> review = Review(
        ...     title="ML in Healthcare",
        ...     research_question="What is the impact of ML on diagnosis?",
        ...     inclusion_criteria=["Peer-reviewed", "English"],
        ...     exclusion_criteria=["Conference abstracts"],
        ... )
    """

    title: str
    research_question: str
    inclusion_criteria: list[str]
    exclusion_criteria: list[str]
    stage: ReviewStage = ReviewStage.PLANNING
    papers: set[Paper] = field(default_factory=set)

    def __post_init__(self) -> None:
        """Validate review fields on creation."""
        if not self.title or not self.title.strip():
            raise ValidationError("Review title cannot be empty")

        if not self.research_question or not self.research_question.strip():
            raise ValidationError("Research question cannot be empty")

        if not self.inclusion_criteria:
            raise ValidationError("At least one inclusion criterion is required")

    def advance_stage(self) -> None:
        """Advance to the next workflow stage.

        Raises:
            WorkflowError: If already at the final stage.
        """
        current_idx = STAGE_ORDER.index(self.stage)
        if current_idx >= len(STAGE_ORDER) - 1:
            raise WorkflowError(f"Cannot advance beyond {self.stage.value} stage")
        self.stage = STAGE_ORDER[current_idx + 1]

    def can_add_papers(self) -> bool:
        """Check if papers can be added at current stage.

        Returns:
            True if current stage allows adding papers.
        """
        return self.stage != ReviewStage.PLANNING

    def add_paper(self, paper: Paper) -> None:
        """Add a paper to the review.

        Args:
            paper: Paper to add.

        Raises:
            WorkflowError: If in PLANNING stage.
        """
        if self.stage == ReviewStage.PLANNING:
            raise WorkflowError(
                "Cannot add papers during PLANNING stage. Advance to SEARCH stage first."
            )
        self.papers.add(paper)

    def add_papers(self, papers: list[Paper]) -> int:
        """Add multiple papers to the review.

        Args:
            papers: List of papers to add.

        Returns:
            Number of papers actually added (excluding duplicates).

        Raises:
            WorkflowError: If in PLANNING stage.
        """
        if self.stage == ReviewStage.PLANNING:
            raise WorkflowError(
                "Cannot add papers during PLANNING stage. Advance to SEARCH stage first."
            )
        initial_count = len(self.papers)
        for paper in papers:
            self.papers.add(paper)
        return len(self.papers) - initial_count

    def get_paper_by_doi(self, doi: DOI) -> Paper | None:
        """Find a paper by its DOI.

        Args:
            doi: DOI to search for.

        Returns:
            Paper if found, None otherwise.
        """
        for paper in self.papers:
            if paper.doi == doi:
                return paper
        return None

    def get_unassessed_papers(self) -> list[Paper]:
        """Get papers that haven't been assessed yet.

        Returns:
            List of unassessed papers.
        """
        return [p for p in self.papers if not p.is_assessed()]

    def get_included_papers(self) -> list[Paper]:
        """Get papers marked for inclusion.

        Returns:
            List of included papers.
        """
        return [p for p in self.papers if p.included is True]

    def get_excluded_papers(self) -> list[Paper]:
        """Get papers marked for exclusion.

        Returns:
            List of excluded papers.
        """
        return [p for p in self.papers if p.included is False]

    def generate_statistics(self) -> dict[str, Any]:
        """Generate review statistics.

        Returns:
            Dictionary with review statistics.
        """
        total = len(self.papers)
        assessed = sum(1 for p in self.papers if p.is_assessed())
        included = len(self.get_included_papers())
        excluded = len(self.get_excluded_papers())

        return {
            "total_papers": total,
            "assessed_papers": assessed,
            "unassessed_papers": total - assessed,
            "included_papers": included,
            "excluded_papers": excluded,
            "inclusion_rate": included / assessed if assessed > 0 else 0.0,
            "current_stage": self.stage.value,
        }

    def is_complete(self) -> bool:
        """Check if review is complete.

        Returns:
            True if review is in COMPLETE stage.
        """
        return self.stage == ReviewStage.COMPLETE
