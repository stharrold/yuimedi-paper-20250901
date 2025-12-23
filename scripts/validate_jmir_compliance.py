#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
"""
Validate JMIR Medical Informatics compliance for paper.md with pandoc-citeproc system.

Checks:
- Abstract structure (5 sections: Background, Objective, Methods, Results, Conclusions)
- Abstract word count (max 450 words)
- Required end sections (Funding, Conflicts of Interest, Data Availability, etc.)
- CSL configuration in metadata.yaml
- Abbreviations section

Uses Python stdlib only - no external dependencies.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def validate_abstract_structure(content: str) -> dict:
    """
    Check for 5-section abstract with JMIR headers.

    Args:
        content: Full paper.md content including YAML frontmatter.

    Returns:
        dict with keys:
            - valid (bool): True if all 5 sections present
            - missing_headers (list[str]): List of missing section headers
            - word_count (int): Total words in abstract (excluding formatting)
            - within_limit (bool): True if word_count <= 450
            - error (str, optional): Error message if abstract not found
    """
    # More robust pattern: match abstract until next YAML field or end of frontmatter
    abstract_match = re.search(
        r"^abstract:\s*\|\s*(.+?)^(?=\w+:|---)",
        content,
        re.DOTALL | re.MULTILINE,
    )
    if not abstract_match:
        return {"valid": False, "error": "No abstract found", "word_count": 0}

    abstract = abstract_match.group(1)

    # Check for required headers (bold markdown format)
    required = [
        "**Background:**",
        "**Objective:**",
        "**Methods:**",
        "**Results:**",
        "**Conclusions:**",
    ]

    missing = [h for h in required if h not in abstract]

    # Count words (excluding markdown formatting)
    clean_text = re.sub(r"\*\*[^*]+\*\*:?", "", abstract)
    word_count = len(clean_text.split())

    return {
        "valid": len(missing) == 0,
        "missing_headers": missing,
        "word_count": word_count,
        "within_limit": word_count <= 450,
    }


def validate_required_sections(content: str) -> dict:
    """
    Check for required JMIR end sections.

    Args:
        content: Full paper.md content.

    Returns:
        dict mapping section name to bool indicating presence.
        Keys: "Funding", "Conflicts of Interest", "Data Availability",
              "Author Contributions", "Abbreviations"
    """
    required = {
        "Funding": r"^# Funding\s*$",
        "Conflicts of Interest": r"^# Conflicts of Interest\s*$",
        "Data Availability": r"^# Data Availability\s*$",
        "Author Contributions": r"^# Author Contributions?\s*$",
        "Abbreviations": r"^# Abbreviations\s*$",
    }

    results = {}
    for section, pattern in required.items():
        results[section] = bool(re.search(pattern, content, re.MULTILINE))

    return results


def validate_csl_configuration(metadata_content: str) -> dict:
    """
    Check metadata.yaml CSL configuration for JMIR compliance.

    Args:
        metadata_content: Content of metadata.yaml file.

    Returns:
        dict with keys:
            - bibliography_configured (bool): True if references.bib configured
            - csl_configured (bool): True if any CSL file configured
            - ama_style (bool): True if AMA 11th edition CSL configured
    """
    has_bib = bool(re.search(r"bibliography:\s*references\.bib", metadata_content))
    has_csl = bool(re.search(r"csl:\s*citation-style", metadata_content))
    is_ama = bool(re.search(r"csl:\s*citation-style-ama\.csl", metadata_content))

    return {
        "bibliography_configured": has_bib,
        "csl_configured": has_csl,
        "ama_style": is_ama,
    }


def validate_no_old_citations(content: str) -> dict:
    """
    Check that old [A#] and [I#] citation format is not present.

    Args:
        content: Full paper.md content.

    Returns:
        dict with keys:
            - clean (bool): True if no legacy citations found
            - old_academic_count (int): Number of [A#] citations found
            - old_industry_count (int): Number of [I#] citations found
    """
    old_academic = re.findall(r"\[A\d+\]", content)
    old_industry = re.findall(r"\[I\d+\]", content)

    return {
        "clean": len(old_academic) == 0 and len(old_industry) == 0,
        "old_academic_count": len(old_academic),
        "old_industry_count": len(old_industry),
    }


def main() -> int:
    """Main entry point. Returns 0 if compliant, 1 otherwise."""
    paper_path = Path("paper.md")
    metadata_path = Path("metadata.yaml")

    if not paper_path.exists():
        print(f"Error: {paper_path} not found")
        return 1

    if not metadata_path.exists():
        print(f"Error: {metadata_path} not found")
        return 1

    paper_content = paper_path.read_text()
    metadata_content = metadata_path.read_text()

    print("# JMIR Medical Informatics Compliance Report")
    print("# (Pandoc-Citeproc Edition)")
    print()

    all_valid = True

    # Abstract validation
    abstract = validate_abstract_structure(paper_content)
    print("## Abstract")
    if abstract.get("error"):
        print(f"  ✗ Error: {abstract['error']}")
        all_valid = False
    else:
        valid_str = "✓" if abstract["valid"] else "✗"
        print(
            f"  {valid_str} Structure: {'5 sections present' if abstract['valid'] else 'missing headers'}"
        )
        if not abstract["valid"]:
            print(f"      Missing: {', '.join(abstract['missing_headers'])}")
            all_valid = False

        limit_str = "✓" if abstract["within_limit"] else "✗"
        print(f"  {limit_str} Word count: {abstract['word_count']}/450")
        if not abstract["within_limit"]:
            all_valid = False
    print()

    # Required sections
    sections = validate_required_sections(paper_content)
    print("## Required Sections")
    for section, present in sections.items():
        status = "✓" if present else "✗"
        print(f"  {status} {section}")
        if not present:
            all_valid = False
    print()

    # CSL Configuration
    csl = validate_csl_configuration(metadata_content)
    print("## Citation Configuration")
    bib_str = "✓" if csl["bibliography_configured"] else "✗"
    csl_str = "✓" if csl["csl_configured"] else "✗"
    ama_str = "✓" if csl["ama_style"] else "✗"
    print(f"  {bib_str} Bibliography (references.bib)")
    print(f"  {csl_str} CSL configured")
    print(f"  {ama_str} AMA style (11th edition)")
    if not csl["bibliography_configured"] or not csl["csl_configured"]:
        all_valid = False
    print()

    # Old citation format check
    old_citations = validate_no_old_citations(paper_content)
    print("## Citation Format Migration")
    clean_str = "✓" if old_citations["clean"] else "✗"
    print(
        f"  {clean_str} No old [A#]/[I#] citations: {'clean' if old_citations['clean'] else 'found legacy citations'}"
    )
    if not old_citations["clean"]:
        print(f"      Old academic: {old_citations['old_academic_count']}")
        print(f"      Old industry: {old_citations['old_industry_count']}")
        all_valid = False
    print()

    # Overall compliance
    print("## Overall Compliance")
    if all_valid:
        print("  ✓ COMPLIANT - Ready for JMIR submission")
        return 0
    else:
        print("  ✗ NON-COMPLIANT - See issues above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
