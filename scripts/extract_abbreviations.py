#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
"""
Extract abbreviations from paper.md.
Output: Markdown abbreviations section for JMIR compliance.

Uses Python stdlib only - no external dependencies.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# Path to abbreviations configuration file
ABBREVIATIONS_JSON = Path(__file__).parent / "abbreviations.json"


def load_known_abbreviations(config_path: Path | None = None) -> dict[str, str]:
    """
    Load known abbreviations from JSON configuration file.

    Args:
        config_path: Path to JSON file. Defaults to scripts/abbreviations.json.

    Returns:
        dict mapping abbreviation to full term (e.g., {"AI": "Artificial Intelligence"})
    """
    path = config_path or ABBREVIATIONS_JSON
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def extract_abbreviations(
    paper_path: Path, min_count: int = 1, config_path: Path | None = None
) -> dict[str, tuple[str, int]]:
    """
    Find abbreviations in paper content and count occurrences.

    Args:
        paper_path: Path to paper.md
        min_count: Minimum number of times abbreviation must appear (default: 1)
        config_path: Path to abbreviations JSON config. Defaults to scripts/abbreviations.json.

    Returns:
        dict mapping abbreviation to tuple of (full_term, count).
        Example: {"AI": ("Artificial Intelligence", 15)}
    """
    content = paper_path.read_text()

    # Load known abbreviations from configuration file
    known_abbrevs = load_known_abbreviations(config_path)

    # Count occurrences of each abbreviation in the content
    abbrev_dict: dict[str, tuple[str, int]] = {}
    for abbrev, full_term in known_abbrevs.items():
        # Count both standalone uses and parenthetical uses
        count = len(re.findall(rf"\b{abbrev}\b", content))
        if count >= min_count:
            abbrev_dict[abbrev] = (full_term, count)

    return abbrev_dict


def format_abbreviations_section(abbrevs: dict[str, tuple[str, int]]) -> str:
    """
    Generate markdown abbreviations section for JMIR compliance.

    Args:
        abbrevs: dict mapping abbreviation to (full_term, count) tuple.

    Returns:
        Markdown-formatted string with header and alphabetically sorted abbreviations.
        Example:
            # Abbreviations

            AI: Artificial Intelligence
            EHR: Electronic Health Record
    """
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
