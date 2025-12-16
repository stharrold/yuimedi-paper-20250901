# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for Review entity."""

import pytest

from lit_review.domain.entities.paper import Paper
from lit_review.domain.entities.review import Review, ReviewStage
from lit_review.domain.exceptions import ValidationError, WorkflowError
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


def create_paper(doi_suffix: str = "test") -> Paper:
    """Helper to create a test paper."""
    return Paper(
        doi=DOI(f"10.1234/{doi_suffix}"),
        title=f"Test Paper {doi_suffix}",
        authors=[Author("Smith", "John", "J.")],
        publication_year=2024,
        journal="Test Journal",
    )


class TestReviewCreation:
    """Tests for Review creation and validation."""

    def test_valid_review_minimal_fields(self) -> None:
        """Review with minimal required fields is created successfully."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        assert review.title == "Test Review"
        assert review.research_question == "What is the impact?"
        assert review.inclusion_criteria == ["Peer-reviewed"]
        assert review.exclusion_criteria == []
        assert review.stage == ReviewStage.PLANNING
        assert len(review.papers) == 0

    def test_empty_title_raises_error(self) -> None:
        """Empty title raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Review(
                title="",
                research_question="What is the impact?",
                inclusion_criteria=["Peer-reviewed"],
                exclusion_criteria=[],
            )
        assert "title cannot be empty" in str(exc_info.value.message)

    def test_empty_research_question_raises_error(self) -> None:
        """Empty research question raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Review(
                title="Test Review",
                research_question="",
                inclusion_criteria=["Peer-reviewed"],
                exclusion_criteria=[],
            )
        assert "Research question cannot be empty" in str(exc_info.value.message)

    def test_no_inclusion_criteria_raises_error(self) -> None:
        """Empty inclusion criteria raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Review(
                title="Test Review",
                research_question="What is the impact?",
                inclusion_criteria=[],
                exclusion_criteria=[],
            )
        assert "inclusion criterion is required" in str(exc_info.value.message)


class TestReviewWorkflowStages:
    """Tests for Review workflow stage transitions."""

    def test_initial_stage_is_planning(self) -> None:
        """Review starts in PLANNING stage."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        assert review.stage == ReviewStage.PLANNING

    def test_advance_stage_from_planning_to_search(self) -> None:
        """advance_stage() moves from PLANNING to SEARCH."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        review.advance_stage()
        assert review.stage == ReviewStage.SEARCH

    def test_advance_through_all_stages(self) -> None:
        """Can advance through all stages in order."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        expected_stages = [
            ReviewStage.SEARCH,
            ReviewStage.SCREENING,
            ReviewStage.ANALYSIS,
            ReviewStage.SYNTHESIS,
            ReviewStage.COMPLETE,
        ]
        for expected in expected_stages:
            review.advance_stage()
            assert review.stage == expected

    def test_cannot_advance_beyond_complete(self) -> None:
        """Cannot advance beyond COMPLETE stage."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        # Advance to COMPLETE
        for _ in range(5):
            review.advance_stage()
        assert review.stage == ReviewStage.COMPLETE

        # Try to advance again
        with pytest.raises(WorkflowError) as exc_info:
            review.advance_stage()
        assert "Cannot advance beyond" in str(exc_info.value.message)


class TestReviewPaperManagement:
    """Tests for Review paper management."""

    def test_cannot_add_papers_during_planning(self) -> None:
        """Cannot add papers during PLANNING stage."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        paper = create_paper()

        with pytest.raises(WorkflowError) as exc_info:
            review.add_paper(paper)
        assert "PLANNING stage" in str(exc_info.value.message)

    def test_can_add_papers_during_search(self) -> None:
        """Can add papers during SEARCH stage."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        review.advance_stage()  # Move to SEARCH
        paper = create_paper()

        review.add_paper(paper)
        assert len(review.papers) == 1

    def test_add_papers_returns_count_of_added(self) -> None:
        """add_papers() returns count of newly added papers."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        review.advance_stage()  # Move to SEARCH

        papers = [create_paper("test1"), create_paper("test2")]
        added = review.add_papers(papers)
        assert added == 2

    def test_add_papers_deduplicates_by_doi(self) -> None:
        """add_papers() deduplicates papers by DOI."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        review.advance_stage()  # Move to SEARCH

        paper1 = create_paper("same")
        paper2 = create_paper("same")  # Same DOI
        paper3 = create_paper("different")

        added = review.add_papers([paper1, paper2, paper3])
        assert added == 2  # paper1 and paper2 have same DOI
        assert len(review.papers) == 2

    def test_get_paper_by_doi_found(self) -> None:
        """get_paper_by_doi() returns paper when found."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        review.advance_stage()
        paper = create_paper("findme")
        review.add_paper(paper)

        found = review.get_paper_by_doi(DOI("10.1234/findme"))
        assert found is not None
        assert found.doi.value == "10.1234/findme"

    def test_get_paper_by_doi_not_found(self) -> None:
        """get_paper_by_doi() returns None when not found."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        review.advance_stage()

        found = review.get_paper_by_doi(DOI("10.1234/notfound"))
        assert found is None


class TestReviewPaperFiltering:
    """Tests for Review paper filtering methods."""

    def test_get_unassessed_papers(self) -> None:
        """get_unassessed_papers() returns papers without assessment."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        review.advance_stage()

        paper1 = create_paper("assessed")
        paper1.assess(8.0, include=True)
        paper2 = create_paper("unassessed")

        review.add_papers([paper1, paper2])
        unassessed = review.get_unassessed_papers()
        assert len(unassessed) == 1
        assert unassessed[0].doi.value == "10.1234/unassessed"

    def test_get_included_papers(self) -> None:
        """get_included_papers() returns papers marked for inclusion."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        review.advance_stage()

        paper1 = create_paper("included")
        paper1.assess(8.0, include=True)
        paper2 = create_paper("excluded")
        paper2.assess(3.0, include=False)

        review.add_papers([paper1, paper2])
        included = review.get_included_papers()
        assert len(included) == 1
        assert included[0].doi.value == "10.1234/included"

    def test_get_excluded_papers(self) -> None:
        """get_excluded_papers() returns papers marked for exclusion."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        review.advance_stage()

        paper1 = create_paper("included")
        paper1.assess(8.0, include=True)
        paper2 = create_paper("excluded")
        paper2.assess(3.0, include=False)

        review.add_papers([paper1, paper2])
        excluded = review.get_excluded_papers()
        assert len(excluded) == 1
        assert excluded[0].doi.value == "10.1234/excluded"


class TestReviewStatistics:
    """Tests for Review statistics generation."""

    def test_generate_statistics_empty_review(self) -> None:
        """generate_statistics() works for empty review."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        stats = review.generate_statistics()
        assert stats["total_papers"] == 0
        assert stats["assessed_papers"] == 0
        assert stats["unassessed_papers"] == 0
        assert stats["included_papers"] == 0
        assert stats["excluded_papers"] == 0
        assert stats["inclusion_rate"] == 0.0
        assert stats["current_stage"] == "planning"

    def test_generate_statistics_with_papers(self) -> None:
        """generate_statistics() calculates correct values."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        review.advance_stage()

        # Add papers with different states
        paper1 = create_paper("included1")
        paper1.assess(8.0, include=True)
        paper2 = create_paper("included2")
        paper2.assess(7.0, include=True)
        paper3 = create_paper("excluded")
        paper3.assess(3.0, include=False)
        paper4 = create_paper("unassessed")

        review.add_papers([paper1, paper2, paper3, paper4])
        stats = review.generate_statistics()

        assert stats["total_papers"] == 4
        assert stats["assessed_papers"] == 3
        assert stats["unassessed_papers"] == 1
        assert stats["included_papers"] == 2
        assert stats["excluded_papers"] == 1
        assert stats["inclusion_rate"] == pytest.approx(2 / 3, rel=0.01)
        assert stats["current_stage"] == "search"


class TestReviewCompletion:
    """Tests for Review completion status."""

    def test_is_complete_false_when_not_complete(self) -> None:
        """is_complete() returns False when not in COMPLETE stage."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        assert review.is_complete() is False

    def test_is_complete_true_when_complete(self) -> None:
        """is_complete() returns True when in COMPLETE stage."""
        review = Review(
            title="Test Review",
            research_question="What is the impact?",
            inclusion_criteria=["Peer-reviewed"],
            exclusion_criteria=[],
        )
        # Advance to COMPLETE
        for _ in range(5):
            review.advance_stage()
        assert review.is_complete() is True
