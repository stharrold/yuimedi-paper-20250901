# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
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


class TestHTMLExport:
    """Tests for HTML export format."""

    def test_html_export_creates_valid_html(self) -> None:
        """HTML export creates valid HTML document."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.HTML)

        assert "<!DOCTYPE html>" in content
        assert "<html" in content
        assert "</html>" in content
        assert review.title in content

    def test_html_export_includes_papers(self) -> None:
        """HTML export includes all paper details."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.HTML)

        # Check papers are included
        assert "Paper included1" in content
        assert "Paper included2" in content

    def test_html_export_includes_search_functionality(self) -> None:
        """HTML export includes search box."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.HTML)

        assert "searchInput" in content
        assert "Search papers" in content


class TestMarkdownExport:
    """Tests for Markdown export format."""

    def test_markdown_export_has_title(self) -> None:
        """Markdown export includes review title."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.MARKDOWN)

        assert f"# {review.title}" in content

    def test_markdown_export_includes_papers(self) -> None:
        """Markdown export includes all papers."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.MARKDOWN)

        assert "Paper included1" in content
        assert "Paper included2" in content
        assert "10.1234/included1" in content

    def test_markdown_export_has_proper_structure(self) -> None:
        """Markdown export has proper heading structure."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.MARKDOWN)

        assert "## Statistics" in content
        assert "## Papers" in content
        assert "###" in content  # Paper headings


class TestCSVExport:
    """Tests for CSV export format."""

    def test_csv_export_has_header(self) -> None:
        """CSV export includes header row."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.CSV)

        lines = content.split("\n")
        header = lines[0]
        assert "DOI" in header
        assert "Title" in header
        assert "Authors" in header

    def test_csv_export_includes_all_papers(self) -> None:
        """CSV export includes all papers."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.CSV)

        assert "10.1234/included1" in content
        assert "10.1234/included2" in content
        assert "Paper included1" in content

    def test_csv_export_is_parseable(self) -> None:
        """CSV export can be parsed."""
        import csv
        from io import StringIO

        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        content = use_case.export_to_string(review, ExportFormat.CSV)

        reader = csv.reader(StringIO(content))
        rows = list(reader)

        assert len(rows) > 1  # Header + data rows
        assert len(rows[0]) == 8  # 8 columns


class TestMultipleFormats:
    """Tests for multiple format support."""

    def test_execute_with_html_format(self) -> None:
        """Execute can export to HTML format."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        try:
            count = use_case.execute(review, ExportFormat.HTML, tmp_path)
            assert count == 2  # Only included papers
            assert tmp_path.exists()

            content = tmp_path.read_text()
            assert "<!DOCTYPE html>" in content
        finally:
            tmp_path.unlink()

    def test_execute_with_markdown_format(self) -> None:
        """Execute can export to Markdown format."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        try:
            count = use_case.execute(review, ExportFormat.MARKDOWN, tmp_path)
            assert count == 2
            assert tmp_path.exists()
        finally:
            tmp_path.unlink()

    def test_execute_with_csv_format(self) -> None:
        """Execute can export to CSV format."""
        use_case = ExportReviewUseCase()
        review = create_review_with_papers()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        try:
            count = use_case.execute(review, ExportFormat.CSV, tmp_path)
            assert count == 2
            assert tmp_path.exists()
        finally:
            tmp_path.unlink()
