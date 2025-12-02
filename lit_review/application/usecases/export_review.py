"""Export review use case for generating formatted output.

Handles exporting reviews to various formats including BibTeX and JSON.
"""

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from lit_review.domain.entities.paper import Paper
from lit_review.domain.entities.review import Review
from lit_review.domain.services.citation_formatter import CitationFormatter


class ExportFormat(Enum):
    """Supported export formats."""

    BIBTEX = "bibtex"
    JSON = "json"


@dataclass
class ExportReviewUseCase:
    """Use case for exporting reviews to various formats.

    Supports exporting to BibTeX for citation managers and JSON
    for data interchange.

    Example:
        >>> use_case = ExportReviewUseCase()
        >>> use_case.execute(review, ExportFormat.BIBTEX, Path("refs.bib"))
    """

    formatter: CitationFormatter | None = None

    def __post_init__(self) -> None:
        """Initialize formatter if not provided."""
        if self.formatter is None:
            self.formatter = CitationFormatter()

    def execute(
        self,
        review: Review,
        export_format: ExportFormat,
        output_path: Path,
        included_only: bool = True,
    ) -> int:
        """Export review to specified format.

        Args:
            review: Review to export.
            export_format: Target format (BIBTEX or JSON).
            output_path: Path to write output file.
            included_only: If True, only export included papers.

        Returns:
            Number of papers exported.

        Raises:
            IOError: If unable to write to output path.
        """
        papers = review.get_included_papers() if included_only else list(review.papers)

        if export_format == ExportFormat.BIBTEX:
            content = self._format_bibtex(papers)
        elif export_format == ExportFormat.JSON:
            content = self._format_json(review, papers)
        else:
            raise ValueError(f"Unsupported format: {export_format}")

        output_path.write_text(content, encoding="utf-8")
        return len(papers)

    def export_to_string(
        self,
        review: Review,
        export_format: ExportFormat,
        included_only: bool = True,
    ) -> str:
        """Export review to string in specified format.

        Args:
            review: Review to export.
            export_format: Target format (BIBTEX or JSON).
            included_only: If True, only export included papers.

        Returns:
            Formatted string content.
        """
        papers = review.get_included_papers() if included_only else list(review.papers)

        if export_format == ExportFormat.BIBTEX:
            return self._format_bibtex(papers)
        elif export_format == ExportFormat.JSON:
            return self._format_json(review, papers)
        else:
            raise ValueError(f"Unsupported format: {export_format}")

    def _format_bibtex(self, papers: list[Paper]) -> str:
        """Format papers as BibTeX entries.

        Args:
            papers: Papers to format.

        Returns:
            BibTeX formatted string with all papers.
        """
        assert self.formatter is not None
        entries = [self.formatter.format_bibtex(paper) for paper in papers]
        return "\n\n".join(entries)

    def _format_json(self, review: Review, papers: list[Paper]) -> str:
        """Format review and papers as JSON.

        Args:
            review: Review metadata.
            papers: Papers to include.

        Returns:
            JSON formatted string.
        """
        data = {
            "review": {
                "title": review.title,
                "research_question": review.research_question,
                "inclusion_criteria": review.inclusion_criteria,
                "exclusion_criteria": review.exclusion_criteria,
                "stage": review.stage.value,
                "statistics": review.generate_statistics(),
            },
            "papers": [self._paper_to_dict(paper) for paper in papers],
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

    def _paper_to_dict(self, paper: Paper) -> dict[str, Any]:
        """Convert Paper entity to dictionary.

        Args:
            paper: Paper to convert.

        Returns:
            Dictionary representation of paper.
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
