#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Convert inline citations in paper.md from [A#]/[I#] to [@key] format.

This script reads the citation key mapping and converts all inline citations
in paper.md to pandoc-citeproc format. It also removes the manual References
section (pandoc will generate it automatically).

Usage:
    python scripts/convert_inline_citations.py
    python scripts/convert_inline_citations.py --dry-run
    python scripts/convert_inline_citations.py --backup
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load_citation_mapping(mapping_path: Path) -> dict[str, str]:
    """Load the citation key mapping from JSON file."""
    with mapping_path.open() as f:
        data = json.load(f)
    return data["mapping"]


def convert_citation(match: re.Match, mapping: dict[str, str]) -> str:
    """Convert a single citation or citation group to pandoc format.

    Handles:
    - [A1] -> [@wu2024]
    - [A1, A2] -> [@wu2024; @ren2024]
    - [A1]-[A3] -> [@wu2024; @ren2024; @chen2024] (expanded range)
    - [A1, A2, I1] -> [@wu2024; @ren2024; @himss2024]
    """
    full_match = match.group(0)

    # Check if this is a range like [A1]-[A3]
    range_match = re.match(r"\[([AI])(\d+)\]-\[([AI])(\d+)\]", full_match)
    if range_match:
        prefix1, start, prefix2, end = range_match.groups()
        if prefix1 != prefix2:
            # Different prefixes, just convert both individually
            key1 = f"{prefix1}{start}"
            key2 = f"{prefix2}{end}"
            new_key1 = mapping.get(key1, key1.lower())
            new_key2 = mapping.get(key2, key2.lower())
            return f"[@{new_key1}; @{new_key2}]"

        # Same prefix, expand the range
        keys = []
        for i in range(int(start), int(end) + 1):
            old_key = f"{prefix1}{i}"
            new_key = mapping.get(old_key, old_key.lower())
            keys.append(f"@{new_key}")
        return "[" + "; ".join(keys) + "]"

    # Single citation or comma-separated list like [A1, A2, I1]
    inner = match.group(1)

    # Split by comma and process each
    parts = [p.strip() for p in inner.split(",")]
    new_keys = []

    for part in parts:
        # Match individual citation like A1, A2, I1
        key_match = re.match(r"([AI])(\d+)", part)
        if key_match:
            old_key = key_match.group(0)
            new_key = mapping.get(old_key, old_key.lower())
            new_keys.append(f"@{new_key}")
        else:
            # Not a recognized citation format, keep as-is
            new_keys.append(part)

    if len(new_keys) == 1:
        return f"[@{new_keys[0].lstrip('@')}]"
    return "[" + "; ".join(new_keys) + "]"


def convert_inline_citations(content: str, mapping: dict[str, str]) -> str:
    """Convert all inline citations in content from [A#]/[I#] to [@key] format."""
    # Pattern to match citation ranges like [A1]-[A3]
    range_pattern = r"\[[AI]\d+\]-\[[AI]\d+\]"

    # Pattern to match single citations or comma-separated lists like [A1] or [A1, A2, I1]
    single_pattern = r"\[([AI]\d+(?:\s*,\s*[AI]\d+)*)\]"

    # First, convert ranges (do this first as they're more specific)
    def convert_range(match: re.Match) -> str:
        return convert_citation(match, mapping)

    content = re.sub(range_pattern, convert_range, content)

    # Then convert single/grouped citations
    def convert_single(match: re.Match) -> str:
        return convert_citation(match, mapping)

    content = re.sub(single_pattern, convert_single, content)

    return content


def remove_references_section(content: str) -> str:
    """Remove the manual References section (pandoc will generate it).

    We keep the Appendices section if present.
    """
    # Find the References section
    ref_match = re.search(r"^# References\s*$", content, re.MULTILINE)
    if not ref_match:
        return content

    ref_start = ref_match.start()

    # Find where References ends (at Appendices or end of file)
    appendix_match = re.search(r"^# Appendices?\s*$", content[ref_match.end() :], re.MULTILINE)

    if appendix_match:
        # Keep everything before References + Appendices onwards
        ref_end = ref_match.end() + appendix_match.start()
        return content[:ref_start] + content[ref_end:]
    else:
        # No Appendices, remove everything from References to end
        return content[:ref_start].rstrip() + "\n"


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert inline citations to pandoc-citeproc format"
    )
    parser.add_argument("--paper", type=Path, default=Path("paper.md"), help="Path to paper.md")
    parser.add_argument(
        "--mapping",
        type=Path,
        default=Path("scripts/citation_key_mapping.json"),
        help="Citation mapping file",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print changes without modifying files"
    )
    parser.add_argument(
        "--backup", action="store_true", help="Create backup of paper.md before modifying"
    )
    parser.add_argument(
        "--keep-references", action="store_true", help="Don't remove the References section"
    )
    args = parser.parse_args()

    # Find project root
    if not args.paper.exists():
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        args.paper = project_root / "paper.md"
        args.mapping = project_root / "scripts" / "citation_key_mapping.json"

    if not args.paper.exists():
        print(f"Error: Could not find paper.md at {args.paper}", file=sys.stderr)
        return 1

    if not args.mapping.exists():
        print(f"Error: Could not find mapping file at {args.mapping}", file=sys.stderr)
        print("Run scripts/convert_references_to_bibtex.py first to generate it.")
        return 1

    # Load mapping
    print(f"Loading citation mapping from {args.mapping}...")
    mapping = load_citation_mapping(args.mapping)
    print(f"Loaded {len(mapping)} citation mappings")

    # Read paper
    print(f"Reading {args.paper}...")
    original_content = args.paper.read_text()

    # Count original citations
    original_citations = len(re.findall(r"\[[AI]\d+\]", original_content))
    print(f"Found {original_citations} citation references in paper.md")

    # Convert citations
    converted_content = convert_inline_citations(original_content, mapping)

    # Count new citations
    new_citations = len(re.findall(r"\[@[a-z0-9]+\]", converted_content))
    print(f"Converted to {new_citations} pandoc citations")

    # Remove References section unless --keep-references
    if not args.keep_references:
        final_content = remove_references_section(converted_content)
        print("Removed manual References section (pandoc will generate it)")
    else:
        final_content = converted_content

    if args.dry_run:
        print("\n--- Sample conversion (first 50 citations) ---")
        # Show some example conversions
        original_lines = original_content.split("\n")
        converted_lines = final_content.split("\n")

        shown = 0
        for i, (orig, conv) in enumerate(zip(original_lines, converted_lines)):
            if orig != conv and "[A" in orig or "[I" in orig:
                print(f"Line {i + 1}:")
                print(f"  - {orig[:100]}...")
                print(f"  + {conv[:100]}...")
                shown += 1
                if shown >= 5:
                    break

        print("\n... (dry-run: no files modified)")
    else:
        # Create backup if requested
        if args.backup:
            backup_path = args.paper.with_suffix(".md.bak")
            backup_path.write_text(original_content)
            print(f"Backup saved to {backup_path}")

        # Write converted content
        args.paper.write_text(final_content)
        print(f"Updated {args.paper}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
