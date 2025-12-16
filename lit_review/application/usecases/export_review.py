# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
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
    HTML = "html"
    MARKDOWN = "markdown"
    CSV = "csv"


@dataclass
class ExportReviewUseCase:
    """Use case for exporting reviews to various formats.

    Supports exporting to multiple formats:
    - BibTeX: For citation managers
    - JSON: For data interchange
    - HTML: Interactive web view with search/filtering
    - Markdown: Human-readable format
    - CSV: Spreadsheet import

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
            export_format: Target format.
            output_path: Path to write output file.
            included_only: If True, only export included papers.

        Returns:
            Number of papers exported.

        Raises:
            IOError: If unable to write to output path.
            ValueError: If format is unsupported.
        """
        papers = review.get_included_papers() if included_only else list(review.papers)

        if export_format == ExportFormat.BIBTEX:
            content = self._format_bibtex(papers)
        elif export_format == ExportFormat.JSON:
            content = self._format_json(review, papers)
        elif export_format == ExportFormat.HTML:
            content = self._format_html(review, papers)
        elif export_format == ExportFormat.MARKDOWN:
            content = self._format_markdown(review, papers)
        elif export_format == ExportFormat.CSV:
            content = self._format_csv(papers)
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
            export_format: Target format.
            included_only: If True, only export included papers.

        Returns:
            Formatted string content.

        Raises:
            ValueError: If format is unsupported.
        """
        papers = review.get_included_papers() if included_only else list(review.papers)

        if export_format == ExportFormat.BIBTEX:
            return self._format_bibtex(papers)
        elif export_format == ExportFormat.JSON:
            return self._format_json(review, papers)
        elif export_format == ExportFormat.HTML:
            return self._format_html(review, papers)
        elif export_format == ExportFormat.MARKDOWN:
            return self._format_markdown(review, papers)
        elif export_format == ExportFormat.CSV:
            return self._format_csv(papers)
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

    def _format_html(self, review: Review, papers: list[Paper]) -> str:
        """Format review and papers as interactive HTML.

        Args:
            review: Review metadata.
            papers: Papers to include.

        Returns:
            HTML formatted string with search/filtering capabilities.
        """
        papers_html = []
        for i, paper in enumerate(papers, 1):
            authors_str = ", ".join(f"{a.last_name}, {a.first_name[0]}." for a in paper.authors[:3])
            if len(paper.authors) > 3:
                authors_str += " et al."

            quality_badge = ""
            if paper.quality_score is not None:
                quality_badge = f'<span class="badge">Quality: {paper.quality_score}/10</span>'

            papers_html.append(
                f"""
        <div class="paper" data-year="{paper.publication_year}" data-doi="{paper.doi.value}">
            <h3>{i}. {paper.title}</h3>
            <p class="authors">{authors_str}</p>
            <p class="meta">
                <em>{paper.journal}</em> ({paper.publication_year})
                {quality_badge}
            </p>
            <p class="doi">DOI: <a href="https://doi.org/{paper.doi.value}">{paper.doi.value}</a></p>
            {f'<p class="abstract">{paper.abstract}</p>' if paper.abstract else ""}
        </div>
        """
            )

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{review.title} - Literature Review</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        header {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{ margin: 0 0 10px 0; color: #333; }}
        .search-box {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        #searchInput {{
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 4px;
        }}
        .paper {{
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .paper h3 {{ margin-top: 0; color: #2c3e50; }}
        .authors {{ color: #555; font-weight: 500; }}
        .meta {{ color: #777; font-size: 14px; }}
        .doi {{ font-size: 13px; font-family: monospace; }}
        .abstract {{ color: #666; font-size: 14px; margin-top: 10px; }}
        .badge {{
            background: #3498db;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 10px;
        }}
        .stats {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 4px;
            margin-top: 15px;
        }}
        .hidden {{ display: none; }}
    </style>
</head>
<body>
    <header>
        <h1>{review.title}</h1>
        <p><strong>Research Question:</strong> {review.research_question}</p>
        <p><strong>Stage:</strong> {review.stage.value.title()}</p>
        <div class="stats">
            <strong>Statistics:</strong> {len(papers)} papers |
            Stage: {review.stage.value}
        </div>
    </header>

    <div class="search-box">
        <input type="text" id="searchInput" placeholder="Search papers by title, author, DOI...">
    </div>

    <div id="papers">
        {"".join(papers_html)}
    </div>

    <script>
        const searchInput = document.getElementById('searchInput');
        const papers = document.querySelectorAll('.paper');

        searchInput.addEventListener('input', function() {{
            const searchTerm = this.value.toLowerCase();

            papers.forEach(paper => {{
                const text = paper.textContent.toLowerCase();
                if (text.includes(searchTerm)) {{
                    paper.classList.remove('hidden');
                }} else {{
                    paper.classList.add('hidden');
                }}
            }});
        }});
    </script>
</body>
</html>"""
        return html

    def _format_markdown(self, review: Review, papers: list[Paper]) -> str:
        """Format review and papers as Markdown.

        Args:
            review: Review metadata.
            papers: Papers to include.

        Returns:
            Markdown formatted string.
        """
        lines = [
            f"# {review.title}",
            "",
            f"**Research Question:** {review.research_question}",
            f"**Stage:** {review.stage.value.title()}",
            "",
            "## Statistics",
            "",
            f"- Total Papers: {len(papers)}",
            f"- Review Stage: {review.stage.value}",
            "",
            "## Papers",
            "",
        ]

        for i, paper in enumerate(papers, 1):
            authors_str = ", ".join(f"{a.last_name}, {a.first_name[0]}." for a in paper.authors[:3])
            if len(paper.authors) > 3:
                authors_str += " et al."

            lines.append(f"### {i}. {paper.title}")
            lines.append("")
            lines.append(f"**Authors:** {authors_str}")
            lines.append(f"**Journal:** {paper.journal} ({paper.publication_year})")
            lines.append(f"**DOI:** [{paper.doi.value}](https://doi.org/{paper.doi.value})")

            if paper.quality_score is not None:
                lines.append(f"**Quality Score:** {paper.quality_score}/10")

            if paper.abstract:
                lines.append("")
                lines.append(f"**Abstract:** {paper.abstract}")

            lines.append("")

        return "\n".join(lines)

    def _format_csv(self, papers: list[Paper]) -> str:
        """Format papers as CSV.

        Args:
            papers: Papers to format.

        Returns:
            CSV formatted string.
        """
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(
            [
                "DOI",
                "Title",
                "Authors",
                "Year",
                "Journal",
                "Quality Score",
                "Included",
                "Keywords",
            ]
        )

        # Data rows
        for paper in papers:
            authors_str = "; ".join(f"{a.last_name}, {a.first_name}" for a in paper.authors)
            keywords_str = "; ".join(paper.keywords) if paper.keywords else ""

            writer.writerow(
                [
                    paper.doi.value,
                    paper.title,
                    authors_str,
                    paper.publication_year,
                    paper.journal,
                    paper.quality_score if paper.quality_score is not None else "",
                    "Yes" if paper.included else "No" if paper.included is False else "",
                    keywords_str,
                ]
            )

        return output.getvalue()
