#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""
File: validate_references.py
Project: YuiQuery Healthcare Analytics Research
Type: Academic research documentation project

Reference Validation Script
Validates citations in paper.md to ensure:
1. All references are properly formatted
2. All citations in the body have corresponding references
3. All reference URLs are accessible
4. Generates a validation report

Uses Python stdlib only - no external dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Configuration
PAPER_PATH = Path(__file__).parent.parent / "paper.md"
BIBTEX_PATH = Path(__file__).parent.parent / "references.bib"
MAPPING_PATH = Path(__file__).parent / "citation_key_mapping.json"
ALLOWLIST_PATH = Path(__file__).parent / "url_allowlist.json"
REPORT_PATH = Path(__file__).parent.parent / "docs" / "validation_report.md"
URL_TIMEOUT = 10  # seconds
MAX_RETRIES = 2

# Citation patterns - support both old [A#]/[I#] and new [@key] formats
ACADEMIC_PATTERN = re.compile(r"\[A(\d+)\]")
INDUSTRY_PATTERN = re.compile(r"\[I(\d+)\]")
CITATION_PATTERN = re.compile(r"\[(A|I)(\d+)\]")
# New pandoc-citeproc citation pattern: [@key] or [@key1; @key2]
# Uses \w with Unicode flag to match international characters (e.g., š, ć)
CITEPROC_CITATION_PATTERN = re.compile(r"\[@([\w]+(?:;\s*@[\w]+)*)\]", re.UNICODE)
URL_PATTERN = re.compile(r'https?://[^\s<>"]+')
REFERENCE_LINE_PATTERN = re.compile(r"^\[(A|I)(\d+)\]\s+(.+)$", re.MULTILINE)
# Pattern to detect LaTeX commands in URLs (e.g., \break, \textit, \href)
LATEX_IN_URL_PATTERN = re.compile(r"(https?://[^\s<>\"]*)(\\[a-zA-Z]+)([^\s<>\"]*)")


@dataclass
class Reference:
    """Represents a reference entry."""

    marker: str  # e.g., "A1", "I5"
    ref_type: str  # "academic" or "industry"
    number: int
    full_text: str
    url: str | None = None
    url_status: int | None = None
    url_error: str | None = None


@dataclass
class Citation:
    """Represents a citation in the paper body."""

    marker: str  # e.g., "A1", "I5"
    line_number: int
    context: str  # surrounding text


@dataclass
class ValidationResult:
    """Holds all validation results."""

    references: dict[str, Reference] = field(default_factory=dict)
    citations: list[Citation] = field(default_factory=list)
    orphaned_citations: list[Citation] = field(default_factory=list)
    unused_references: list[str] = field(default_factory=list)
    broken_urls: list[Reference] = field(default_factory=list)
    accessible_urls: list[Reference] = field(default_factory=list)
    missing_urls: list[Reference] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON output."""
        return {
            "summary": {
                "total_references": len(self.references),
                "academic_references": sum(
                    1 for r in self.references.values() if r.ref_type == "academic"
                ),
                "industry_references": sum(
                    1 for r in self.references.values() if r.ref_type == "industry"
                ),
                "total_citations": len(self.citations),
                "orphaned_citations": len(self.orphaned_citations),
                "unused_references": len(self.unused_references),
                "accessible_urls": len(self.accessible_urls),
                "broken_urls": len(self.broken_urls),
                "missing_urls": len(self.missing_urls),
            },
            "issues": {
                "orphaned_citations": [
                    {"marker": c.marker, "line": c.line_number, "context": c.context}
                    for c in self.orphaned_citations
                ],
                "unused_references": self.unused_references,
                "broken_urls": [
                    {
                        "marker": r.marker,
                        "url": r.url,
                        "status": r.url_status,
                        "error": r.url_error,
                    }
                    for r in self.broken_urls
                ],
                "missing_urls": [r.marker for r in self.missing_urls],
            },
        }


def parse_bibtex_references(bibtex_path: Path) -> dict[str, Reference]:
    """Parse references from a BibTeX file."""
    references: dict[str, Reference] = {}

    if not bibtex_path.exists():
        return references

    content = bibtex_path.read_text()

    # Simple BibTeX parser (stdlib only - no external dependencies)
    # Pattern to match BibTeX entries: @type{key, ... }
    entry_pattern = re.compile(r"@(\w+)\{([^,]+),([^@]*?)^\}", re.MULTILINE | re.DOTALL)

    for match in entry_pattern.finditer(content):
        _entry_type = match.group(1).lower()  # noqa: F841 - kept for future use
        key = match.group(2).strip()
        fields_text = match.group(3)

        # Parse fields
        fields: dict[str, str] = {}
        # Match field = {value} or field = "value"
        field_pattern = re.compile(r'(\w+)\s*=\s*[{"]([^}"]*)[}"]')
        for field_match in field_pattern.finditer(fields_text):
            field_name = field_match.group(1).lower()
            field_value = field_match.group(2).strip()
            fields[field_name] = field_value

        # Extract URL
        url = fields.get("url")

        # Try to determine type from original note
        note = fields.get("note", "")
        original_match = re.search(r"\[([AI])(\d+)\]", note)
        if original_match:
            ref_type = "academic" if original_match.group(1) == "A" else "industry"
            number = int(original_match.group(2))
        else:
            # Default to academic, use hash as number
            ref_type = "academic"
            number = hash(key) % 1000

        # Build full text from available fields
        author = fields.get("author", "Unknown")
        title = fields.get("title", "").strip("{}")
        year = fields.get("year", "n.d.")
        journal = fields.get("journal", fields.get("booktitle", ""))
        full_text = f"{author}. ({year}). {title}. {journal}"

        references[key] = Reference(
            marker=key,
            ref_type=ref_type,
            number=number,
            full_text=full_text,
            url=url,
        )

    return references


def parse_references(paper_content: str, bibtex_path: Path | None = None) -> dict[str, Reference]:
    """Parse references from paper.md or BibTeX file.

    Supports both:
    - Old format: Manual [A#]/[I#] references in paper.md
    - New format: BibTeX file with [@key] citations
    """
    # Try BibTeX first if available
    if bibtex_path and bibtex_path.exists():
        refs = parse_bibtex_references(bibtex_path)
        if refs:
            return refs

    # Fall back to old format in paper.md
    references: dict[str, Reference] = {}

    # Find the References section
    ref_section_match = re.search(r"^# References\s*$", paper_content, re.MULTILINE)
    if not ref_section_match:
        print("WARNING: No References section found in paper.md", file=sys.stderr)
        return references

    # Get content from References section onwards
    ref_content = paper_content[ref_section_match.end() :]

    # Find the next major section (if any) to limit our search
    next_section_match = re.search(r"^# [^#]", ref_content, re.MULTILINE)
    if next_section_match:
        ref_content = ref_content[: next_section_match.start()]

    # Parse each reference line
    for match in REFERENCE_LINE_PATTERN.finditer(ref_content):
        ref_type_char = match.group(1)
        number = int(match.group(2))
        full_text = match.group(3).strip()

        marker = f"{ref_type_char}{number}"
        ref_type = "academic" if ref_type_char == "A" else "industry"

        # Extract URL from the reference text
        url_match = URL_PATTERN.search(full_text)
        url = url_match.group(0).rstrip(".,;:") if url_match else None

        references[marker] = Reference(
            marker=marker,
            ref_type=ref_type,
            number=number,
            full_text=full_text,
            url=url,
        )

    return references


def extract_citations(paper_content: str, use_citeproc: bool = False) -> list[Citation]:
    """Extract all citations from the paper body.

    Args:
        paper_content: The markdown content
        use_citeproc: If True, use [@key] format; if False, use [A#]/[I#] format

    Returns:
        List of Citation objects
    """
    citations: list[Citation] = []

    # For old format, exclude References section
    if not use_citeproc:
        ref_section_match = re.search(r"^# References\s*$", paper_content, re.MULTILINE)
        body_content = (
            paper_content[: ref_section_match.start()] if ref_section_match else paper_content
        )
    else:
        # For citeproc format, use entire content (no manual References section)
        body_content = paper_content

    # Split into lines for context
    lines = body_content.split("\n")

    for line_num, line in enumerate(lines, start=1):
        if use_citeproc:
            # New format: [@key] or [@key1; @key2]
            for match in CITEPROC_CITATION_PATTERN.finditer(line):
                # Extract all citation keys from the match (each prefixed with @)
                keys = re.findall(r"@([\w]+)", match.group(0))

                # Get context
                start = max(0, match.start() - 50)
                end = min(len(line), match.end() + 50)
                context = line[start:end].strip()
                if start > 0:
                    context = "..." + context
                if end < len(line):
                    context = context + "..."

                for key in keys:
                    citations.append(Citation(marker=key, line_number=line_num, context=context))
        else:
            # Old format: [A#] or [I#]
            for match in CITATION_PATTERN.finditer(line):
                ref_type = match.group(1)
                number = match.group(2)
                marker = f"{ref_type}{number}"

                # Get context (the sentence or surrounding text)
                start = max(0, match.start() - 50)
                end = min(len(line), match.end() + 50)
                context = line[start:end].strip()
                if start > 0:
                    context = "..." + context
                if end < len(line):
                    context = context + "..."

                citations.append(Citation(marker=marker, line_number=line_num, context=context))

    return citations


def check_url(url: str, timeout: int = URL_TIMEOUT) -> tuple[int | None, str | None]:
    """Check if a URL is accessible. Returns (status_code, error_message)."""
    # Use default SSL context with certificate verification enabled
    ssl_context = ssl.create_default_context()

    for attempt in range(MAX_RETRIES):
        try:
            # Create request with a common user agent
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                },
                method="HEAD",  # Just check if accessible, don't download
            )

            with urllib.request.urlopen(request, timeout=timeout, context=ssl_context) as response:
                return response.status, None

        except urllib.error.HTTPError as e:
            # Try GET if HEAD fails (some servers don't support HEAD)
            if e.code == 405 and attempt == 0:  # Method Not Allowed
                try:
                    request = urllib.request.Request(
                        url,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                        },
                        method="GET",
                    )
                    with urllib.request.urlopen(
                        request, timeout=timeout, context=ssl_context
                    ) as response:
                        return response.status, None
                except Exception:
                    pass
            return e.code, f"HTTP {e.code}: {e.reason}"

        except urllib.error.URLError as e:
            return None, f"URL Error: {e.reason}"

        except TimeoutError:
            if attempt < MAX_RETRIES - 1:
                continue
            return None, "Timeout"

        except Exception as e:
            return None, f"Error: {type(e).__name__}: {e}"

    return None, "Max retries exceeded"


def validate_urls(
    references: dict[str, Reference], allowlist: dict[str, str] | None = None, verbose: bool = False
) -> tuple[list[Reference], list[Reference], list[Reference]]:
    """Validate all reference URLs."""
    accessible: list[Reference] = []
    broken: list[Reference] = []
    missing: list[Reference] = []

    allowlist = allowlist or {}
    total = len(references)
    for i, (marker, ref) in enumerate(references.items(), start=1):
        if ref.url is None:
            missing.append(ref)
            if verbose:
                print(f"  [{i}/{total}] {marker}: No URL")
            continue

        if verbose:
            print(f"  [{i}/{total}] {marker}: Checking {ref.url[:50]}...")

        # Check allowlist
        if marker in allowlist and allowlist[marker] == ref.url:
            status, error = 200, "Confirmed-as-good (allowlisted)"
        else:
            status, error = check_url(ref.url)

        ref.url_status = status
        ref.url_error = error

        if status is not None and 200 <= status < 400:
            accessible.append(ref)
            if verbose:
                print(f"    -> OK ({status})")
        else:
            broken.append(ref)
            if verbose:
                print(f"    -> FAILED: {error}")

    return accessible, broken, missing


def find_orphaned_and_unused(
    references: dict[str, Reference], citations: list[Citation]
) -> tuple[list[Citation], list[str]]:
    """Find orphaned citations (no matching reference) and unused references."""
    cited_markers = {c.marker for c in citations}
    defined_markers = set(references.keys())

    orphaned_citations = [c for c in citations if c.marker not in defined_markers]
    unused_references = sorted(defined_markers - cited_markers)

    if unused_references:
        print("UNUSED REFERENCES:")
        for ref in unused_references:
            print(ref)

    return orphaned_citations, unused_references


@dataclass
class LatexViolation:
    """Represents a LaTeX command found in a URL."""

    line_number: int
    url_fragment: str
    latex_command: str
    full_match: str


def check_latex_in_urls(content: str) -> list[LatexViolation]:
    """
    Check for LaTeX commands embedded in URLs.

    This detects issues like URLs split by \\break commands, which cause
    hyperlinks to break in generated PDF/HTML/DOCX outputs.

    Args:
        content: The markdown content to check

    Returns:
        List of LatexViolation objects with line numbers and matched patterns
    """
    violations: list[LatexViolation] = []

    for line_num, line in enumerate(content.split("\n"), start=1):
        for match in LATEX_IN_URL_PATTERN.finditer(line):
            url_before = match.group(1)
            latex_cmd = match.group(2)
            full_match = match.group(0)

            violations.append(
                LatexViolation(
                    line_number=line_num,
                    url_fragment=url_before,
                    latex_command=latex_cmd,
                    full_match=full_match,
                )
            )

    return violations


def generate_report(result: ValidationResult, output_path: Path | None = None) -> str:
    """Generate a markdown validation report."""
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# Reference Validation Report",
        "",
        f"**Generated:** {timestamp}",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Total References | {len(result.references)} |",
        f"| Academic [A*] | {sum(1 for r in result.references.values() if r.ref_type == 'academic')} |",
        f"| Industry [I*] | {sum(1 for r in result.references.values() if r.ref_type == 'industry')} |",
        f"| Total Citations | {len(result.citations)} |",
        f"| Accessible URLs | {len(result.accessible_urls)} |",
        f"| Broken URLs | {len(result.broken_urls)} |",
        f"| Missing URLs | {len(result.missing_urls)} |",
        f"| Orphaned Citations | {len(result.orphaned_citations)} |",
        f"| Unused References | {len(result.unused_references)} |",
        "",
    ]

    # Issues section
    has_issues = (
        result.orphaned_citations
        or result.unused_references
        or result.broken_urls
        or result.missing_urls
    )

    if has_issues:
        lines.extend(["## Issues", ""])

        if result.orphaned_citations:
            lines.extend(
                [
                    "### Orphaned Citations",
                    "",
                    "Citations in the paper body with no matching reference:",
                    "",
                    "| Citation | Line | Context |",
                    "|----------|------|---------|",
                ]
            )
            for c in result.orphaned_citations:
                context = c.context.replace("|", "\\|")
                lines.append(f"| [{c.marker}] | {c.line_number} | {context} |")
            lines.append("")

        if result.unused_references:
            lines.extend(
                [
                    "### Unused References",
                    "",
                    "References defined but never cited in the paper body:",
                    "",
                ]
            )
            for marker in result.unused_references:
                lines.append(f"- [{marker}]")
            lines.append("")

        if result.broken_urls:
            lines.extend(
                [
                    "### Broken URLs",
                    "",
                    "References with inaccessible URLs:",
                    "",
                    "| Reference | URL | Error |",
                    "|-----------|-----|-------|",
                ]
            )
            for r in result.broken_urls:
                url = r.url[:60] + "..." if r.url and len(r.url) > 60 else r.url
                error = r.url_error or "Unknown error"
                lines.append(f"| [{r.marker}] | {url} | {error} |")
            lines.append("")

        if result.missing_urls:
            lines.extend(
                [
                    "### References Without URLs",
                    "",
                    "References that don't have a URL:",
                    "",
                ]
            )
            for r in result.missing_urls:
                lines.append(f"- [{r.marker}]")
            lines.append("")
    else:
        lines.extend(["## Status", "", "All validations passed.", ""])

    # All references section (collapsed)
    lines.extend(
        [
            "## All References",
            "",
            "<details>",
            "<summary>Click to expand full reference list</summary>",
            "",
            "| Marker | Type | URL Status |",
            "|--------|------|------------|",
        ]
    )

    for marker in sorted(
        result.references.keys(),
        key=lambda x: (x[0], int(x[1:])) if re.match(r"^[AI]\d+$", x) else (x.lower(), 0),
    ):
        ref = result.references[marker]
        if ref.url is None:
            status = "No URL"
        elif ref.url_status and 200 <= ref.url_status < 400:
            status = f"OK ({ref.url_status})"
        else:
            status = f"Failed: {ref.url_error}"
        lines.append(f"| [{marker}] | {ref.ref_type} | {status} |")

    lines.extend(["", "</details>", ""])

    report = "\n".join(lines)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report)
        print(f"Report written to: {output_path}")

    return report


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate references in paper.md",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/validate_references.py --parse-only
  python scripts/validate_references.py --check-citations
  python scripts/validate_references.py --check-urls
  python scripts/validate_references.py --check-latex
  python scripts/validate_references.py --report
  python scripts/validate_references.py --all
        """,
    )

    parser.add_argument(
        "--parse-only",
        action="store_true",
        help="Only parse references, don't validate",
    )
    parser.add_argument(
        "--check-citations",
        action="store_true",
        help="Check for orphaned/unused citations",
    )
    parser.add_argument(
        "--check-urls",
        action="store_true",
        help="Validate reference URLs",
    )
    parser.add_argument(
        "--check-latex",
        action="store_true",
        help="Check for LaTeX commands in URLs (e.g., \\break)",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate validation report",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all validations and generate report",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output",
    )
    parser.add_argument(
        "--paper",
        type=Path,
        default=PAPER_PATH,
        help=f"Path to paper.md (default: {PAPER_PATH})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPORT_PATH,
        help=f"Path for output report (default: {REPORT_PATH})",
    )
    parser.add_argument(
        "--bibtex",
        type=Path,
        default=BIBTEX_PATH,
        help=f"Path to BibTeX file (default: {BIBTEX_PATH})",
    )

    args = parser.parse_args()

    # Default to --all if no specific action specified
    if not any(
        [args.parse_only, args.check_citations, args.check_urls, args.check_latex, args.report]
    ):
        args.all = True

    # Read paper content
    if not args.paper.exists():
        print(f"ERROR: Paper not found: {args.paper}", file=sys.stderr)
        return 1

    paper_content = args.paper.read_text()

    # Detect citation format
    # Check for citeproc format ([@key]) vs old format ([A#])
    has_citeproc = bool(CITEPROC_CITATION_PATTERN.search(paper_content))
    has_old_format = bool(CITATION_PATTERN.search(paper_content))
    use_citeproc = has_citeproc and not has_old_format

    if use_citeproc:
        print("Detected pandoc-citeproc format ([@key] citations)")
    else:
        print("Detected legacy format ([A#]/[I#] citations)")

    # Initialize result
    result = ValidationResult()

    # Parse references
    print("Parsing references...")
    if use_citeproc and args.bibtex.exists():
        result.references = parse_references(paper_content, args.bibtex)
    else:
        result.references = parse_references(paper_content)

    academic_count = sum(1 for r in result.references.values() if r.ref_type == "academic")
    industry_count = sum(1 for r in result.references.values() if r.ref_type == "industry")
    print(
        f"Found {len(result.references)} references ({academic_count} academic, {industry_count} industry)"
    )

    if args.parse_only:
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        return 0

    # Extract citations and check for orphaned/unused
    if args.check_citations or args.all:
        print("\nExtracting citations...")
        result.citations = extract_citations(paper_content, use_citeproc=use_citeproc)
        print(f"Found {len(result.citations)} citations in paper body")

        result.orphaned_citations, result.unused_references = find_orphaned_and_unused(
            result.references, result.citations
        )

        if result.orphaned_citations:
            print(f"WARNING: {len(result.orphaned_citations)} orphaned citations found")
            for c in result.orphaned_citations:
                print(f"  - [{c.marker}] at line {c.line_number}")

        if result.unused_references:
            print(f"INFO: {len(result.unused_references)} unused references")
            if args.verbose:
                for marker in result.unused_references:
                    print(f"  - [{marker}]")

    # Validate URLs
    if args.check_urls or args.all:
        print("\nValidating URLs...")
        # Load allowlist if it exists
        allowlist = {}
        if ALLOWLIST_PATH.exists():
            try:
                allowlist = json.loads(ALLOWLIST_PATH.read_text())
                print(f"Loaded {len(allowlist)} allowlisted URLs from {ALLOWLIST_PATH}")
            except Exception as e:
                print(f"WARNING: Failed to load allowlist from {ALLOWLIST_PATH}: {e}")

        result.accessible_urls, result.broken_urls, result.missing_urls = validate_urls(
            result.references, allowlist=allowlist, verbose=args.verbose
        )
        print(
            f"Checked {len(result.references)} URLs: "
            f"{len(result.accessible_urls)} accessible, "
            f"{len(result.broken_urls)} broken, "
            f"{len(result.missing_urls)} missing"
        )

    # Check for LaTeX commands in URLs
    latex_violations: list[LatexViolation] = []
    if args.check_latex or args.all:
        print("\nChecking for LaTeX commands in URLs...")
        latex_violations = check_latex_in_urls(paper_content)
        if latex_violations:
            print(f"ERROR: Found {len(latex_violations)} LaTeX commands in URLs:")
            for v in latex_violations:
                print(f"  Line {v.line_number}: {v.latex_command} in URL")
                if args.verbose:
                    print(f"    Full match: {v.full_match}")
            print("\n  FIX: Remove LaTeX commands from URLs. Common issues:")
            print("    - \\break in long URLs: Remove line breaks, use continuous URL")
            print("    - \\textit or \\textbf: Remove formatting commands from URLs")
            print("    - Escaped characters: Use raw URL without LaTeX escaping")
        else:
            print("OK: No LaTeX commands found in URLs")

    # Generate report
    if args.report or args.all:
        print("\nGenerating report...")
        generate_report(result, args.output if not args.json else None)

    # JSON output
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))

    # Return exit code based on critical issues only
    # Orphaned citations are critical (missing references)
    # LaTeX in URLs is critical (breaks hyperlinks in output)
    # Broken URLs are warnings (many are paywalls/access restrictions)
    has_critical_issues = bool(result.orphaned_citations) or bool(latex_violations)
    if result.broken_urls:
        print(f"\nWARNING: {len(result.broken_urls)} broken URLs (non-critical, likely paywalls)")
    if latex_violations:
        print(
            f"\nERROR: {len(latex_violations)} LaTeX commands in URLs (critical, breaks hyperlinks)"
        )
        print("  Run with --verbose to see affected URLs, then edit paper.md to fix.")
    return 1 if has_critical_issues else 0


if __name__ == "__main__":
    sys.exit(main())
