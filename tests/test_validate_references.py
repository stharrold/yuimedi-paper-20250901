# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for the reference validation script.

Tests cover:
- Reference parsing from paper.md
- Citation extraction from paper body
- Orphaned/unused reference detection
- Report generation
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate_references import (  # noqa: E402
    Citation,
    Reference,
    ValidationResult,
    check_latex_in_urls,
    extract_citations,
    find_orphaned_and_unused,
    generate_report,
    parse_references,
)


@pytest.fixture
def repo_root() -> Path:
    """Return the repository root directory."""
    return Path(__file__).parent.parent


# Sample paper content for testing
SAMPLE_PAPER_CONTENT = """# Sample Paper

## Introduction

Healthcare analytics has transformed patient care [A1]. The HIMSS model [I1] shows
maturity stages. Studies show 91% success rates [A2][I2].

## Methods

We used natural language processing [A3].

# References

## Academic Sources

[A1] Smith, J. (2023). Healthcare analytics. *Journal*. https://example.com/a1

[A2] Jones, K. (2024). NLP in medicine. *JAMIA*. DOI: 10.1234. https://example.com/a2

[A3] Brown, L. (2022). Deep learning. *Nature*. https://example.com/a3

[A4] White, M. (2021). Unused reference. *Book*. https://example.com/a4

## Industry Sources

[I1] HIMSS. (2024). AMAM Report. https://himss.org/amam

[I2] Health Catalyst. (2023). Analytics guide. https://healthcatalyst.com/guide
"""

SAMPLE_PAPER_NO_REFS = """# Sample Paper

## Introduction

This paper has no references section.

## Methods

We used some methods.
"""

SAMPLE_PAPER_ORPHANED = """# Sample Paper

## Introduction

This references a non-existent citation [A99].

# References

## Academic Sources

[A1] Real reference. https://example.com
"""


class TestParseReferences:
    """Tests for parse_references function."""

    def test_parses_academic_references(self):
        """Should correctly parse academic [A*] references."""
        refs = parse_references(SAMPLE_PAPER_CONTENT)

        assert "A1" in refs
        assert refs["A1"].ref_type == "academic"
        assert refs["A1"].number == 1
        assert "Smith" in refs["A1"].full_text

    def test_parses_industry_references(self):
        """Should correctly parse industry [I*] references."""
        refs = parse_references(SAMPLE_PAPER_CONTENT)

        assert "I1" in refs
        assert refs["I1"].ref_type == "industry"
        assert refs["I1"].number == 1
        assert "HIMSS" in refs["I1"].full_text

    def test_extracts_urls(self):
        """Should extract URLs from reference text."""
        refs = parse_references(SAMPLE_PAPER_CONTENT)

        assert refs["A1"].url == "https://example.com/a1"
        assert refs["I1"].url == "https://himss.org/amam"

    def test_counts_references_correctly(self):
        """Should count all references."""
        refs = parse_references(SAMPLE_PAPER_CONTENT)

        academic_count = sum(1 for r in refs.values() if r.ref_type == "academic")
        industry_count = sum(1 for r in refs.values() if r.ref_type == "industry")

        assert academic_count == 4
        assert industry_count == 2
        assert len(refs) == 6

    def test_handles_missing_references_section(self):
        """Should return empty dict if no References section."""
        refs = parse_references(SAMPLE_PAPER_NO_REFS)
        assert refs == {}


class TestExtractCitations:
    """Tests for extract_citations function."""

    def test_extracts_academic_citations(self):
        """Should extract [A*] citations from paper body."""
        citations = extract_citations(SAMPLE_PAPER_CONTENT)

        academic = [c for c in citations if c.marker.startswith("A")]
        assert len(academic) >= 1
        assert any(c.marker == "A1" for c in academic)

    def test_extracts_industry_citations(self):
        """Should extract [I*] citations from paper body."""
        citations = extract_citations(SAMPLE_PAPER_CONTENT)

        industry = [c for c in citations if c.marker.startswith("I")]
        assert len(industry) >= 1
        assert any(c.marker == "I1" for c in industry)

    def test_captures_context(self):
        """Should capture surrounding context for each citation."""
        citations = extract_citations(SAMPLE_PAPER_CONTENT)

        a1_citations = [c for c in citations if c.marker == "A1"]
        assert len(a1_citations) > 0
        assert "Healthcare" in a1_citations[0].context or "analytics" in a1_citations[0].context

    def test_excludes_references_section(self):
        """Should not extract citations from References section."""
        citations = extract_citations(SAMPLE_PAPER_CONTENT)

        # A4 is only in References section, not cited in body
        assert not any(c.marker == "A4" for c in citations)


class TestFindOrphanedAndUnused:
    """Tests for find_orphaned_and_unused function."""

    def test_finds_unused_references(self):
        """Should identify references that are never cited."""
        refs = parse_references(SAMPLE_PAPER_CONTENT)
        citations = extract_citations(SAMPLE_PAPER_CONTENT)

        _, unused = find_orphaned_and_unused(refs, citations)

        # A4 is defined but never cited
        assert "A4" in unused

    def test_finds_orphaned_citations(self):
        """Should identify citations with no matching reference."""
        refs = parse_references(SAMPLE_PAPER_ORPHANED)
        citations = extract_citations(SAMPLE_PAPER_ORPHANED)

        orphaned, _ = find_orphaned_and_unused(refs, citations)

        # A99 is cited but not defined
        assert len(orphaned) > 0
        assert any(c.marker == "A99" for c in orphaned)

    def test_no_false_positives(self):
        """Should not mark properly linked refs as orphaned/unused."""
        refs = parse_references(SAMPLE_PAPER_CONTENT)
        citations = extract_citations(SAMPLE_PAPER_CONTENT)

        orphaned, unused = find_orphaned_and_unused(refs, citations)

        # A1, A2, A3, I1, I2 are properly linked
        assert "A1" not in unused
        assert "I1" not in unused
        assert not any(c.marker == "A1" for c in orphaned)


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_to_dict_structure(self):
        """Should produce correct dictionary structure."""
        result = ValidationResult()
        result.references = {"A1": Reference("A1", "academic", 1, "Test ref")}
        result.citations = [Citation("A1", 10, "Test context")]

        data = result.to_dict()

        assert "summary" in data
        assert "issues" in data
        assert data["summary"]["total_references"] == 1
        assert data["summary"]["total_citations"] == 1


class TestGenerateReport:
    """Tests for generate_report function."""

    def test_generates_markdown(self):
        """Should generate valid markdown report."""
        result = ValidationResult()
        result.references = {"A1": Reference("A1", "academic", 1, "Test ref")}

        report = generate_report(result, output_path=None)

        assert "# Reference Validation Report" in report
        assert "## Summary" in report
        assert "| Total References | 1 |" in report

    def test_includes_issues(self):
        """Should include issues section when problems exist."""
        result = ValidationResult()
        result.unused_references = ["A99"]

        report = generate_report(result, output_path=None)

        assert "## Issues" in report
        assert "Unused References" in report
        assert "[A99]" in report

    def test_writes_to_file(self, tmp_path: Path):
        """Should write report to file when path provided."""
        result = ValidationResult()
        output = tmp_path / "report.md"

        generate_report(result, output_path=output)

        assert output.exists()
        content = output.read_text()
        assert "# Reference Validation Report" in content


class TestCheckLatexInUrls:
    """Tests for check_latex_in_urls function."""

    def test_detects_break_command(self):
        """Should detect \\break LaTeX command in URLs."""
        content = "Reference: https://example.com/\\break/path/to/resource"
        violations = check_latex_in_urls(content)

        assert len(violations) == 1
        assert violations[0].latex_command == "\\break"
        assert violations[0].line_number == 1

    def test_detects_textit_command(self):
        """Should detect other LaTeX commands like \\textit."""
        content = "Reference: https://example.com/\\textit/path"
        violations = check_latex_in_urls(content)

        assert len(violations) == 1
        assert violations[0].latex_command == "\\textit"

    def test_clean_urls_pass(self):
        """Should return empty list for clean URLs without LaTeX."""
        content = """
[A1] Smith, J. (2023). Title. https://example.com/path/to/resource

[I1] Company. (2024). Report. https://company.org/reports/2024
"""
        violations = check_latex_in_urls(content)

        assert len(violations) == 0

    def test_detects_multiple_violations(self):
        """Should detect multiple LaTeX violations across lines."""
        content = """
[A1] Reference with bad URL: https://example.com/\\break/path1

[A2] Another bad URL: https://other.org/\\textit/path2

[A3] Clean URL: https://clean.com/path
"""
        violations = check_latex_in_urls(content)

        assert len(violations) == 2
        assert any(v.latex_command == "\\break" for v in violations)
        assert any(v.latex_command == "\\textit" for v in violations)

    def test_captures_line_number(self):
        """Should capture correct line numbers for violations."""
        content = """Line 1 no URL
Line 2 no URL
https://example.com/\\break/path on line 3
Line 4 no URL
https://example.com/\\href/path on line 5
"""
        violations = check_latex_in_urls(content)

        assert len(violations) == 2
        line_numbers = {v.line_number for v in violations}
        assert 3 in line_numbers
        assert 5 in line_numbers

    def test_captures_url_fragment(self):
        """Should capture the URL fragment before the LaTeX command."""
        content = "https://pmc.ncbi.nlm.nih.gov/\\break/articles/PMC123"
        violations = check_latex_in_urls(content)

        assert len(violations) == 1
        assert violations[0].url_fragment == "https://pmc.ncbi.nlm.nih.gov/"

    def test_ignores_non_url_latex(self):
        """Should not flag LaTeX commands outside of URLs."""
        content = """
This is \\textbf{bold} text in the paper body.

Reference: https://example.com/clean/path
"""
        violations = check_latex_in_urls(content)

        assert len(violations) == 0


class TestWithRealPaper:
    """Integration tests using the actual paper.md."""

    @pytest.fixture
    def paper_content(self, repo_root: Path) -> str:
        """Load the actual paper content."""
        paper_path = repo_root / "paper.md"
        if not paper_path.exists():
            pytest.skip("paper.md not found")
        return paper_path.read_text()

    def test_parses_real_paper(self, paper_content: str):
        """Should successfully parse references from real paper."""
        refs = parse_references(paper_content)

        # Paper should have references
        assert len(refs) > 0

        # Should have both academic and industry
        academic = sum(1 for r in refs.values() if r.ref_type == "academic")
        industry = sum(1 for r in refs.values() if r.ref_type == "industry")

        assert academic > 0, "Should have academic references"
        assert industry > 0, "Should have industry references"

    def test_extracts_real_citations(self, paper_content: str):
        """Should extract citations from real paper body."""
        citations = extract_citations(paper_content)

        # Paper should have citations in body
        assert len(citations) > 0

    def test_no_orphaned_citations(self, paper_content: str):
        """Real paper should have no orphaned citations."""
        refs = parse_references(paper_content)
        citations = extract_citations(paper_content)

        orphaned, _ = find_orphaned_and_unused(refs, citations)

        # All citations should have matching references
        assert len(orphaned) == 0, f"Found orphaned citations: {[c.marker for c in orphaned]}"

    def test_no_latex_in_urls(self, paper_content: str):
        """Real paper should have no LaTeX commands in URLs after fix."""
        violations = check_latex_in_urls(paper_content)

        assert len(violations) == 0, (
            f"Found {len(violations)} LaTeX commands in URLs: "
            f"{[(v.line_number, v.latex_command) for v in violations]}"
        )
