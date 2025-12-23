#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
"""
Extract abbreviations from paper.md.
Output: Markdown abbreviations section for JMIR compliance.

Uses Python stdlib only - no external dependencies.
"""

from __future__ import annotations

import re
from pathlib import Path


def extract_abbreviations(paper_path: Path, min_count: int = 1) -> dict[str, tuple[str, int]]:
    """
    Find abbreviations in format: "full term (ABBREV)"
    Return: {abbrev: (full_term, count)}

    Args:
        paper_path: Path to paper.md
        min_count: Minimum number of times abbreviation must appear (default: 1)
    """
    content = paper_path.read_text()

    # Known abbreviation definitions (manually curated for accuracy)
    # Format: ABBREV -> full term
    known_abbrevs = {
        "AACODS": "Authority, Accuracy, Coverage, Objectivity, Date, Significance",
        "ACO": "Accountable Care Organization",
        "AI": "Artificial Intelligence",
        "AMAM": "Analytics Maturity Assessment Model",
        "API": "Application Programming Interface",
        "CPT": "Current Procedural Terminology",
        "DAMAF": "Data Analytics Maturity Assessment Framework",
        "DIKW": "Data-Information-Knowledge-Wisdom",
        "EHR": "Electronic Health Record",
        "EMRAM": "Electronic Medical Record Adoption Model",
        "HDQM2": "Healthcare Data Quality Maturity Model",
        "HIMSS": "Healthcare Information Management Systems Society",
        "ICD": "International Classification of Diseases",
        "IT": "Information Technology",
        "LLM": "Large Language Model",
        "NL2SQL": "Natural Language to SQL",
        "RAG": "Retrieval-Augmented Generation",
        "SQL": "Structured Query Language",
    }

    # Count occurrences of each abbreviation in the content
    abbrev_dict: dict[str, tuple[str, int]] = {}
    for abbrev, full_term in known_abbrevs.items():
        # Count both standalone uses and parenthetical uses
        count = len(re.findall(rf"\b{abbrev}\b", content))
        if count >= min_count:
            abbrev_dict[abbrev] = (full_term, count)

    return abbrev_dict


def format_abbreviations_section(abbrevs: dict[str, tuple[str, int]]) -> str:
    """Generate markdown section."""
    lines = ["# Abbreviations", ""]

    # Sort alphabetically
    for abbrev in sorted(abbrevs.keys()):
        full_term, _count = abbrevs[abbrev]
        lines.append(f"{abbrev}: {full_term}")

    return "\n".join(lines)


def main() -> None:
    """Main entry point."""
    paper_path = Path(__file__).parent.parent / "paper.md"

    if not paper_path.exists():
        print(f"Error: {paper_path} not found")
        return

    abbrevs = extract_abbreviations(paper_path)
    section = format_abbreviations_section(abbrevs)

    print(section)
    print(f"\n# Found {len(abbrevs)} abbreviations")

    # Also show all abbreviations with counts for reference
    print("\n# All abbreviations found (with counts):")
    for abbrev in sorted(abbrevs.keys()):
        full_term, count = abbrevs[abbrev]
        print(f"#   {abbrev}: {full_term} ({count} occurrences)")


if __name__ == "__main__":
    main()
