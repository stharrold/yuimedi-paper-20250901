# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for Paper entity."""

import pytest

from lit_review.domain.entities.paper import Paper
from lit_review.domain.exceptions import ValidationError
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


class TestPaperCreation:
    """Tests for Paper creation and validation."""

    def test_valid_paper_minimal_fields(self) -> None:
        """Paper with minimal required fields is created successfully."""
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Test Journal",
        )
        assert paper.doi.value == "10.1234/test"
        assert paper.title == "Test Paper"
        assert len(paper.authors) == 1
        assert paper.publication_year == 2024
        assert paper.journal == "Test Journal"
        assert paper.abstract == ""
        assert paper.keywords == []
        assert paper.quality_score is None

    def test_valid_paper_all_fields(self) -> None:
        """Paper with all fields is created successfully."""
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Test Journal",
            abstract="Test abstract",
            keywords=["test", "paper"],
            quality_score=8.5,
        )
        assert paper.abstract == "Test abstract"
        assert paper.keywords == ["test", "paper"]
        assert paper.quality_score == 8.5

    def test_empty_title_raises_error(self) -> None:
        """Empty title raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Paper(
                doi=DOI("10.1234/test"),
                title="",
                authors=[Author("Smith", "John", "J.")],
                publication_year=2024,
                journal="Test Journal",
            )
        assert "title cannot be empty" in str(exc_info.value.message)

    def test_no_authors_raises_error(self) -> None:
        """Empty authors list raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Paper(
                doi=DOI("10.1234/test"),
                title="Test Paper",
                authors=[],
                publication_year=2024,
                journal="Test Journal",
            )
        assert "at least one author" in str(exc_info.value.message)

    def test_empty_journal_raises_error(self) -> None:
        """Empty journal raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Paper(
                doi=DOI("10.1234/test"),
                title="Test Paper",
                authors=[Author("Smith", "John", "J.")],
                publication_year=2024,
                journal="",
            )
        assert "journal cannot be empty" in str(exc_info.value.message)

    def test_year_before_1900_raises_error(self) -> None:
        """Publication year before 1900 raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Paper(
                doi=DOI("10.1234/test"),
                title="Test Paper",
                authors=[Author("Smith", "John", "J.")],
                publication_year=1899,
                journal="Test Journal",
            )
        assert "between 1900" in str(exc_info.value.message)

    def test_future_year_raises_error(self) -> None:
        """Publication year in far future raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Paper(
                doi=DOI("10.1234/test"),
                title="Test Paper",
                authors=[Author("Smith", "John", "J.")],
                publication_year=3000,
                journal="Test Journal",
            )
        assert "between 1900" in str(exc_info.value.message)

    def test_invalid_quality_score_raises_error(self) -> None:
        """Quality score outside 0-10 range raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Paper(
                doi=DOI("10.1234/test"),
                title="Test Paper",
                authors=[Author("Smith", "John", "J.")],
                publication_year=2024,
                journal="Test Journal",
                quality_score=11.0,
            )
        assert "between 0 and 10" in str(exc_info.value.message)


class TestPaperQualityAssessment:
    """Tests for Paper quality assessment."""

    def test_set_quality_score_valid(self) -> None:
        """Valid quality score is set successfully."""
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Test Journal",
        )
        paper.set_quality_score(7.5)
        assert paper.quality_score == 7.5

    def test_set_quality_score_invalid_raises_error(self) -> None:
        """Invalid quality score raises ValidationError."""
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Test Journal",
        )
        with pytest.raises(ValidationError):
            paper.set_quality_score(-1.0)

    def test_assess_sets_all_fields(self) -> None:
        """assess() sets score, inclusion, and notes."""
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Test Journal",
        )
        paper.assess(8.0, include=True, notes="High quality paper")
        assert paper.quality_score == 8.0
        assert paper.included is True
        assert paper.assessment_notes == "High quality paper"

    def test_is_assessed_false_when_not_assessed(self) -> None:
        """is_assessed() returns False for unassessed paper."""
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Test Journal",
        )
        assert paper.is_assessed() is False

    def test_is_assessed_true_when_assessed(self) -> None:
        """is_assessed() returns True after assessment."""
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Test Journal",
        )
        paper.assess(7.0, include=True)
        assert paper.is_assessed() is True


class TestPaperCitationKey:
    """Tests for Paper citation key generation."""

    def test_citation_key_single_author(self) -> None:
        """Citation key for single author: AuthorYear."""
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Test Journal",
        )
        assert paper.get_citation_key() == "Smith2024"

    def test_citation_key_two_authors(self) -> None:
        """Citation key for two authors: Author1Author2Year."""
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[
                Author("Smith", "John", "J."),
                Author("Jones", "Jane", "J."),
            ],
            publication_year=2024,
            journal="Test Journal",
        )
        assert paper.get_citation_key() == "SmithJones2024"

    def test_citation_key_three_or_more_authors(self) -> None:
        """Citation key for 3+ authors: AuthorEtAlYear."""
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[
                Author("Smith", "John", "J."),
                Author("Jones", "Jane", "J."),
                Author("Wilson", "Bob", "B."),
            ],
            publication_year=2024,
            journal="Test Journal",
        )
        assert paper.get_citation_key() == "SmithEtAl2024"


class TestPaperEquality:
    """Tests for Paper equality (based on DOI)."""

    def test_papers_with_same_doi_are_equal(self) -> None:
        """Papers with same DOI are equal regardless of other fields."""
        paper1 = Paper(
            doi=DOI("10.1234/test"),
            title="Title 1",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal 1",
        )
        paper2 = Paper(
            doi=DOI("10.1234/test"),
            title="Title 2",
            authors=[Author("Jones", "Jane", "J.")],
            publication_year=2023,
            journal="Journal 2",
        )
        assert paper1 == paper2

    def test_papers_with_different_dois_are_not_equal(self) -> None:
        """Papers with different DOIs are not equal."""
        paper1 = Paper(
            doi=DOI("10.1234/test1"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Test Journal",
        )
        paper2 = Paper(
            doi=DOI("10.1234/test2"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Test Journal",
        )
        assert paper1 != paper2

    def test_papers_can_be_used_in_set(self) -> None:
        """Papers can be used in sets for deduplication."""
        paper1 = Paper(
            doi=DOI("10.1234/test1"),
            title="Paper 1",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )
        paper2 = Paper(
            doi=DOI("10.1234/test1"),  # Same DOI
            title="Paper 2",
            authors=[Author("Jones", "Jane", "J.")],
            publication_year=2024,
            journal="Journal",
        )
        paper3 = Paper(
            doi=DOI("10.1234/test3"),  # Different DOI
            title="Paper 3",
            authors=[Author("Wilson", "Bob", "B.")],
            publication_year=2024,
            journal="Journal",
        )
        paper_set = {paper1, paper2, paper3}
        assert len(paper_set) == 2  # paper1 and paper2 are same (same DOI)

    def test_paper_not_equal_to_non_paper_object(self) -> None:
        """Paper compared to non-Paper returns NotImplemented."""
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )
        # Comparing with different types should work
        assert paper != "not a paper"
        assert paper != 123
        assert paper is not None
