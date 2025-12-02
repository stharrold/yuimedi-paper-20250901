"""Tests for ExportReviewUseCase."""

import json
import tempfile
from pathlib import Path

from lit_review.application.usecases.export_review import (
    ExportFormat,
    ExportReviewUseCase,
)
from lit_review.domain.entities.paper import Paper
from lit_review.domain.entities.review import Review
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


def create_paper(doi_suffix: str, included: bool | None = None) -> Paper:
    """Helper to create a test paper."""
    paper = Paper(
        doi=DOI(f"10.1234/{doi_suffix}"),
        title=f"Paper {doi_suffix}",
        authors=[Author("Smith", "John", "J.")],
        publication_year=2024,
        journal="Test Journal",
    )
    if included is not None:
        paper.assess(7.0, include=included)
    return paper


def create_review_with_papers() -> Review:
    """Create a review with sample papers."""
    review = Review(
        title="Test Review",
        research_question="What is the impact?",
        inclusion_criteria=["Peer-reviewed"],
        exclusion_criteria=[],
    )
    review.advance_stage()  # Move to SEARCH

    # Add papers
    paper1 = create_paper("included1", included=True)
    paper2 = create_paper("included2", included=True)
    paper3 = create_paper("excluded", included=False)

    review.add_papers([paper1, paper2, paper3])
    return review


class TestExportReviewUseCase:
    """Tests for ExportReviewUseCase."""

    def test_execute_bibtex_creates_file(self) -> None:
        """Execute creates BibTeX file."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        with tempfile.NamedTemporaryFile(suffix=".bib", delete=False) as f:
            output_path = Path(f.name)

        try:
            count = use_case.execute(review, ExportFormat.BIBTEX, output_path)
            assert count == 2  # Only included papers
            assert output_path.exists()

            content = output_path.read_text()
            assert "@article{Smith2024," in content
        finally:
            output_path.unlink()

    def test_execute_json_creates_file(self) -> None:
        """Execute creates JSON file."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            output_path = Path(f.name)

        try:
            count = use_case.execute(review, ExportFormat.JSON, output_path)
            assert count == 2  # Only included papers
            assert output_path.exists()

            content = output_path.read_text()
            data = json.loads(content)
            assert "review" in data
            assert "papers" in data
            assert len(data["papers"]) == 2
        finally:
            output_path.unlink()

    def test_execute_all_papers_when_included_only_false(self) -> None:
        """Execute exports all papers when included_only=False."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            output_path = Path(f.name)

        try:
            count = use_case.execute(review, ExportFormat.JSON, output_path, included_only=False)
            assert count == 3  # All papers

            content = output_path.read_text()
            data = json.loads(content)
            assert len(data["papers"]) == 3
        finally:
            output_path.unlink()


class TestExportToString:
    """Tests for export_to_string method."""

    def test_export_to_string_bibtex(self) -> None:
        """export_to_string returns BibTeX content."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.BIBTEX)
        assert "@article{" in content
        assert "doi = {10.1234/" in content

    def test_export_to_string_json(self) -> None:
        """export_to_string returns JSON content."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.JSON)
        data = json.loads(content)

        assert data["review"]["title"] == "Test Review"
        assert data["review"]["research_question"] == "What is the impact?"
        assert len(data["papers"]) == 2


class TestJSONExport:
    """Tests for JSON export format."""

    def test_json_includes_review_metadata(self) -> None:
        """JSON export includes review metadata."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.JSON)
        data = json.loads(content)

        assert data["review"]["title"] == "Test Review"
        assert data["review"]["inclusion_criteria"] == ["Peer-reviewed"]
        assert data["review"]["exclusion_criteria"] == []
        assert "statistics" in data["review"]

    def test_json_includes_paper_details(self) -> None:
        """JSON export includes full paper details."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.JSON)
        data = json.loads(content)

        paper = data["papers"][0]
        assert "doi" in paper
        assert "title" in paper
        assert "authors" in paper
        assert "publication_year" in paper
        assert "journal" in paper
        assert "quality_score" in paper
        assert "included" in paper


class TestBibTeXExport:
    """Tests for BibTeX export format."""

    def test_bibtex_separates_entries(self) -> None:
        """BibTeX export separates entries with blank lines."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.BIBTEX)

        # Should have 2 entries separated by blank line
        entries = content.split("\n\n")
        assert len(entries) == 2

    def test_bibtex_entries_are_valid(self) -> None:
        """BibTeX entries have required fields."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.BIBTEX)

        # Check for required BibTeX fields
        assert "author = " in content
        assert "title = " in content
        assert "journal = " in content
        assert "year = " in content
        assert "doi = " in content
