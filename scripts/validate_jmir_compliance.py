#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
"""
Validate JMIR Medical Informatics compliance for paper.md with pandoc-citeproc system.

Checks:
- Abstract structure (5 sections: Background, Objective, Methods, Results, Conclusions)
- Abstract word count (max 450 words)
- Keywords (5-10 required)
- Main body structure (IMRD for Review articles)
- Required end sections (Funding, Conflicts of Interest, Data Availability, etc.)
- Generative AI disclosure in Acknowledgments
- CSL configuration in metadata.yaml
- Pandoc citation format ([@key])
- Figure format (PNG files)
- Abbreviations section

Uses Python stdlib only - no external dependencies.
"""

from __future__ import annotations

import json
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


def validate_keywords(content: str) -> dict:
    """
    Check for 5-10 keywords in YAML frontmatter.

    JMIR requires 5-10 semicolon-separated keywords. MeSH terms preferred.

    Args:
        content: Full paper.md content including YAML frontmatter.

    Returns:
        dict with keys:
            - valid (bool): True if 5-10 keywords present
            - count (int): Number of keywords found
            - keywords (list[str]): List of keywords found
            - error (str, optional): Error message if keywords not found
    """
    # Match keywords in YAML array format: keywords: [keyword1, keyword2, ...]
    array_match = re.search(r"^keywords:\s*\[([^\]]+)\]", content, re.MULTILINE)
    if array_match:
        keywords_str = array_match.group(1)
        # Split by comma and strip quotes/whitespace
        keywords = [k.strip().strip('"').strip("'") for k in keywords_str.split(",")]
        keywords = [k for k in keywords if k]  # Remove empty
        return {
            "valid": 5 <= len(keywords) <= 10,
            "count": len(keywords),
            "keywords": keywords,
        }

    # Match keywords in semicolon format: keywords: "keyword1; keyword2; ..."
    semicolon_match = re.search(r'^keywords:\s*["\']?([^"\'\n]+)["\']?', content, re.MULTILINE)
    if semicolon_match:
        keywords_str = semicolon_match.group(1)
        keywords = [k.strip() for k in keywords_str.split(";")]
        keywords = [k for k in keywords if k]
        return {
            "valid": 5 <= len(keywords) <= 10,
            "count": len(keywords),
            "keywords": keywords,
        }

    return {"valid": False, "count": 0, "keywords": [], "error": "No keywords found"}


def validate_imrd_structure(content: str) -> dict:
    """
    Check for IMRD main body structure (Introduction, Methods, Results, Discussion).

    JMIR requires IMRD structure for Review articles. The specific section names
    may vary (e.g., "Methodology" instead of "Methods", "Literature Review" as Results).

    Args:
        content: Full paper.md content.

    Returns:
        dict with keys:
            - valid (bool): True if all 4 main sections present
            - sections_found (list[str]): List of IMRD sections found
            - missing_sections (list[str]): List of missing IMRD sections
    """
    # Pattern matches level-1 headers (# Section Name)
    imrd_patterns = {
        "Introduction": r"^# Introduction\s*$",
        "Methods": r"^# (Methods?|Methodology)\s*$",
        "Results": r"^# (Results?|Literature Review[^\n]*|Framework Development[^\n]*)\s*$",
        "Discussion": r"^# Discussion\s*$",
    }

    found = []
    missing = []

    for section, pattern in imrd_patterns.items():
        if re.search(pattern, content, re.MULTILINE):
            found.append(section)
        else:
            missing.append(section)

    return {
        "valid": len(missing) == 0,
        "sections_found": found,
        "missing_sections": missing,
    }


def validate_ai_disclosure(content: str) -> dict:
    """
    Check for generative AI disclosure in Acknowledgments section.

    JMIR requires disclosure of any generative AI use in manuscript creation.

    Args:
        content: Full paper.md content.

    Returns:
        dict with keys:
            - has_acknowledgments (bool): True if Acknowledgments section exists
            - has_ai_disclosure (bool): True if AI tool disclosure found
            - ai_tools_mentioned (list[str]): List of AI tools mentioned
    """
    # Find Acknowledgments section
    ack_match = re.search(
        r"^# Acknowledgments?\s*\n(.*?)(?=^# |\Z)", content, re.MULTILINE | re.DOTALL
    )

    if not ack_match:
        return {
            "has_acknowledgments": False,
            "has_ai_disclosure": False,
            "ai_tools_mentioned": [],
        }

    ack_content = ack_match.group(1)

    # Check for AI tool mentions
    ai_patterns = [
        r"Claude",
        r"ChatGPT",
        r"GPT-\d",
        r"Gemini",
        r"Copilot",
        r"generative AI",
        r"language model",
        r"LLM",
        r"AI assist",
    ]

    tools_found = []
    for pattern in ai_patterns:
        if re.search(pattern, ack_content, re.IGNORECASE):
            tools_found.append(pattern)

    return {
        "has_acknowledgments": True,
        "has_ai_disclosure": len(tools_found) > 0,
        "ai_tools_mentioned": tools_found,
    }


def validate_pandoc_citations(content: str) -> dict:
    """
    Check for pandoc-style citations [@key] format.

    Pandoc-citeproc uses [@citationkey] format which gets converted to [1], [2], etc.

    Args:
        content: Full paper.md content.

    Returns:
        dict with keys:
            - has_citations (bool): True if pandoc citations found
            - citation_count (int): Number of citations found
            - sample_citations (list[str]): Sample of citation keys found
    """
    # Match pandoc citation format: [@key] or [@key1; @key2]
    citations = re.findall(r"\[@[a-zA-Z0-9_-]+(?:;\s*@[a-zA-Z0-9_-]+)*\]", content)

    # Extract individual citation keys
    all_keys = []
    for cite in citations:
        keys = re.findall(r"@([a-zA-Z0-9_-]+)", cite)
        all_keys.extend(keys)

    unique_keys = list(set(all_keys))

    return {
        "has_citations": len(citations) > 0,
        "citation_count": len(citations),
        "unique_keys": len(unique_keys),
        "sample_citations": unique_keys[:5] if unique_keys else [],
    }


def validate_figure_format(base_path: Path) -> dict:
    """
    Check that figures are in PNG format as required by JMIR.

    JMIR requires figures as high-resolution PNG files.

    Args:
        base_path: Base path for the repository (to find figures/).

    Returns:
        dict with keys:
            - valid (bool): True if all figures are PNG
            - png_count (int): Number of PNG figures
            - non_png_figures (list[str]): List of non-PNG figure files
            - all_figures (list[str]): List of all figure files
    """
    figures_dir = base_path / "figures"

    if not figures_dir.exists():
        return {
            "valid": True,
            "png_count": 0,
            "non_png_figures": [],
            "all_figures": [],
            "note": "No figures directory found",
        }

    # Find all image files
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".tiff"}
    all_figures = []
    non_png = []

    for file in figures_dir.iterdir():
        if file.suffix.lower() in image_extensions:
            all_figures.append(file.name)
            if file.suffix.lower() != ".png":
                non_png.append(file.name)

    return {
        "valid": len(non_png) == 0
        or all(
            # Allow source files (.mmd, .dot) to have non-PNG derivatives
            ".mmd" in f or ".dot" in f
            for f in non_png
        ),
        "png_count": len([f for f in all_figures if f.endswith(".png")]),
        "non_png_figures": non_png,
        "all_figures": all_figures,
    }


def validate_abbreviations_usage(content: str, config_path: Path | None = None) -> dict:
    """
    Check that abbreviations used ≥3 times in paper are listed in Abbreviations section.

    JMIR requires abbreviations used 3+ times to be listed alphabetically.

    Args:
        content: Full paper.md content.
        config_path: Path to abbreviations.json config file.

    Returns:
        dict with keys:
            - valid (bool): True if all frequent abbreviations are listed
            - listed_abbrevs (list[str]): Abbreviations in the section
            - missing_abbrevs (list[str]): Abbreviations used ≥3 times but not listed
            - usage_counts (dict[str, int]): Count of each abbreviation's usage
    """
    # Find Abbreviations section
    abbrev_match = re.search(
        r"^# Abbreviations\s*\n(.*?)(?=^# |\Z)", content, re.MULTILINE | re.DOTALL
    )

    if not abbrev_match:
        return {
            "valid": False,
            "listed_abbrevs": [],
            "missing_abbrevs": [],
            "usage_counts": {},
            "error": "No Abbreviations section found",
        }

    abbrev_section = abbrev_match.group(1)

    # Extract listed abbreviations (format: "ABBREV: Full Term")
    listed = re.findall(r"^([A-Z][A-Z0-9]+):", abbrev_section, re.MULTILINE)

    # Load known abbreviations from config
    default_config = Path(__file__).parent / "abbreviations.json"
    config = config_path or default_config

    known_abbrevs = {}
    if config.exists():
        known_abbrevs = json.loads(config.read_text())

    # Count abbreviation usage in paper (excluding the Abbreviations section itself)
    paper_without_abbrev_section = content.replace(abbrev_section, "")

    usage_counts = {}
    missing = []

    for abbrev in known_abbrevs:
        count = len(re.findall(rf"\b{abbrev}\b", paper_without_abbrev_section))
        if count >= 3:
            usage_counts[abbrev] = count
            if abbrev not in listed:
                missing.append(abbrev)

    return {
        "valid": len(missing) == 0,
        "listed_abbrevs": listed,
        "missing_abbrevs": missing,
        "usage_counts": usage_counts,
    }


def main() -> int:
    """Main entry point. Returns 0 if compliant, 1 otherwise."""
    paper_path = Path("paper.md")
    metadata_path = Path("metadata.yaml")
    base_path = Path(".")

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

    # Keywords validation
    keywords = validate_keywords(paper_content)
    print("## Keywords")
    if keywords.get("error"):
        print(f"  ✗ Error: {keywords['error']}")
        all_valid = False
    else:
        kw_str = "✓" if keywords["valid"] else "✗"
        print(f"  {kw_str} Count: {keywords['count']}/5-10")
        if not keywords["valid"]:
            if keywords["count"] < 5:
                print("      Need at least 5 keywords")
            elif keywords["count"] > 10:
                print("      Maximum 10 keywords allowed")
            all_valid = False
    print()

    # IMRD Structure validation
    imrd = validate_imrd_structure(paper_content)
    print("## Main Body Structure (IMRD)")
    imrd_str = "✓" if imrd["valid"] else "✗"
    print(f"  {imrd_str} Structure: {'IMRD complete' if imrd['valid'] else 'incomplete'}")
    if imrd["sections_found"]:
        print(f"      Found: {', '.join(imrd['sections_found'])}")
    if imrd["missing_sections"]:
        print(f"      Missing: {', '.join(imrd['missing_sections'])}")
        all_valid = False
    print()

    # Required end sections
    sections = validate_required_sections(paper_content)
    print("## Required End Sections")
    for section, present in sections.items():
        status = "✓" if present else "✗"
        print(f"  {status} {section}")
        if not present:
            all_valid = False
    print()

    # AI Disclosure validation
    ai_disclosure = validate_ai_disclosure(paper_content)
    print("## Generative AI Disclosure")
    if not ai_disclosure["has_acknowledgments"]:
        print("  ✗ No Acknowledgments section found")
        # Not marking as invalid - Acknowledgments is recommended, not required
    else:
        ai_str = "✓" if ai_disclosure["has_ai_disclosure"] else "ℹ"
        status = "disclosed" if ai_disclosure["has_ai_disclosure"] else "no AI tools mentioned"
        print(f"  {ai_str} AI tools: {status}")
        if ai_disclosure["ai_tools_mentioned"]:
            print(f"      Mentioned: {', '.join(ai_disclosure['ai_tools_mentioned'])}")
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

    # Pandoc citations check
    pandoc_cites = validate_pandoc_citations(paper_content)
    print("## Pandoc Citations")
    cite_str = "✓" if pandoc_cites["has_citations"] else "✗"
    print(f"  {cite_str} Citations found: {pandoc_cites['citation_count']} instances")
    print(f"      Unique references: {pandoc_cites['unique_keys']}")
    if pandoc_cites["sample_citations"]:
        print(f"      Sample: {', '.join(pandoc_cites['sample_citations'])}")
    if not pandoc_cites["has_citations"]:
        all_valid = False
    print()

    # Old citation format check
    old_citations = validate_no_old_citations(paper_content)
    print("## Legacy Citation Check")
    clean_str = "✓" if old_citations["clean"] else "✗"
    print(
        f"  {clean_str} No old [A#]/[I#] citations: {'clean' if old_citations['clean'] else 'found legacy citations'}"
    )
    if not old_citations["clean"]:
        print(f"      Old academic: {old_citations['old_academic_count']}")
        print(f"      Old industry: {old_citations['old_industry_count']}")
        all_valid = False
    print()

    # Figure format validation
    figures = validate_figure_format(base_path)
    print("## Figure Format")
    fig_str = "✓" if figures["valid"] else "✗"
    print(f"  {fig_str} PNG format: {figures['png_count']} PNG files")
    if figures.get("note"):
        print(f"      Note: {figures['note']}")
    if figures["non_png_figures"]:
        print(f"      Non-PNG (source files OK): {', '.join(figures['non_png_figures'][:5])}")
        if len(figures["non_png_figures"]) > 5:
            print(f"      ... and {len(figures['non_png_figures']) - 5} more")
    if not figures["valid"]:
        all_valid = False
    print()

    # Abbreviations usage validation
    abbrevs = validate_abbreviations_usage(paper_content)
    print("## Abbreviations Usage")
    if abbrevs.get("error"):
        print(f"  ✗ Error: {abbrevs['error']}")
        all_valid = False
    else:
        abbr_str = "✓" if abbrevs["valid"] else "✗"
        print(
            f"  {abbr_str} All frequent abbreviations listed: {len(abbrevs['listed_abbrevs'])} abbreviations"
        )
        if abbrevs["missing_abbrevs"]:
            print(f"      Missing (used ≥3 times): {', '.join(abbrevs['missing_abbrevs'])}")
            all_valid = False
        if abbrevs["usage_counts"]:
            high_usage = sorted(abbrevs["usage_counts"].items(), key=lambda x: -x[1])[:5]
            usage_str = ", ".join(f"{k}({v})" for k, v in high_usage)
            print(f"      Top usage: {usage_str}")
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
