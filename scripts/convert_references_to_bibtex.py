#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Convert paper.md References section to BibTeX format.

This script parses the manual [A#]/[I#] citation format from paper.md and
generates a references.bib file with proper BibTeX entries. It also creates
a citation_key_mapping.json file mapping old citation keys to new ones.

Usage:
    python scripts/convert_references_to_bibtex.py
    python scripts/convert_references_to_bibtex.py --dry-run
    python scripts/convert_references_to_bibtex.py --output references.bib
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Unicode to ASCII transliteration map for citation keys
UNICODE_TO_ASCII = {
    "á": "a",
    "à": "a",
    "â": "a",
    "ä": "a",
    "ã": "a",
    "å": "a",
    "ą": "a",
    "ć": "c",
    "č": "c",
    "ç": "c",
    "đ": "d",
    "ď": "d",
    "é": "e",
    "è": "e",
    "ê": "e",
    "ë": "e",
    "ě": "e",
    "ę": "e",
    "í": "i",
    "ì": "i",
    "î": "i",
    "ï": "i",
    "ł": "l",
    "ń": "n",
    "ň": "n",
    "ñ": "n",
    "ó": "o",
    "ò": "o",
    "ô": "o",
    "ö": "o",
    "õ": "o",
    "ø": "o",
    "ř": "r",
    "ś": "s",
    "š": "s",
    "ş": "s",
    "ť": "t",
    "ú": "u",
    "ù": "u",
    "û": "u",
    "ü": "u",
    "ů": "u",
    "ý": "y",
    "ÿ": "y",
    "ź": "z",
    "ž": "z",
    "ż": "z",
    "ß": "ss",
    "æ": "ae",
    "œ": "oe",
}


def transliterate_to_ascii(text: str) -> str:
    """Transliterate Unicode characters to ASCII for citation keys.

    This ensures citation keys are compatible with all tools and avoid
    encoding issues in BibTeX processing.
    """
    result = []
    for char in text:
        if char in UNICODE_TO_ASCII:
            result.append(UNICODE_TO_ASCII[char])
        elif ord(char) < 128:  # ASCII range
            result.append(char)
        # Skip non-ASCII characters not in map
    return "".join(result)


@dataclass
class Reference:
    """Parsed reference entry."""

    original_key: str  # e.g., "A1" or "I1"
    authors: str
    year: str
    title: str
    journal: str | None = None
    volume: str | None = None
    issue: str | None = None
    pages: str | None = None
    doi: str | None = None
    url: str | None = None
    entry_type: str = "article"  # article, inproceedings, techreport, misc, mastersthesis
    publisher: str | None = None
    institution: str | None = None
    booktitle: str | None = None
    note: str | None = None


def extract_first_author_lastname(authors: str) -> str:
    """Extract first author's last name for citation key generation.

    Examples:
        "Wu, Y., Li, X., Zhang, Y., et al." -> "wu"
        "HIMSS Analytics" -> "himss"
        "Health Catalyst" -> "healthcatalyst"
        "Snowdon, A." -> "snowdon"
    """
    # Handle organizational authors (no comma before first word)
    words = authors.split()
    if not words or "," not in words[0]:
        # Likely organizational author - use first significant word
        org_name = authors.split(".")[0].split(",")[0].strip()
        # Remove common prefixes/suffixes
        org_name = org_name.replace("The ", "").replace("&", "").strip()
        # Take first word or combine if short
        words = org_name.split()
        if len(words) == 1:
            return words[0].lower()
        if len(words) == 2 and len(words[0]) <= 4:
            return "".join(words).lower()
        return words[0].lower()

    # Standard author format: "LastName, F., ..."
    first_author = authors.split(",")[0].strip()
    return transliterate_to_ascii(first_author.lower().replace(" ", "").replace("-", ""))


def parse_reference_line(line: str) -> Reference | None:
    """Parse a single reference line into a Reference object."""
    # Match citation key pattern [A#] or [I#]
    key_match = re.match(r"^\[([AI]\d+)\]\s*(.+)$", line.strip())
    if not key_match:
        return None

    original_key = key_match.group(1)
    content = key_match.group(2)

    # Extract URL (at end of line)
    url_match = re.search(r"(https?://[^\s]+)$", content)
    url = url_match.group(1) if url_match else None
    if url:
        content = content[: url_match.start()].strip().rstrip(".")

    # Extract DOI
    doi_match = re.search(r"DOI:\s*([^\s.]+(?:\.[^\s.]+)*)", content, re.IGNORECASE)
    doi = doi_match.group(1).rstrip(".") if doi_match else None
    if doi_match:
        content = content[: doi_match.start()].strip()

    # Extract year (typically in parentheses after authors)
    year_match = re.search(r"\((\d{4})\)", content)
    year = year_match.group(1) if year_match else "n.d."

    # Split into authors and rest
    if year_match:
        authors = content[: year_match.start()].strip().rstrip(".")
        rest = content[year_match.end() :].strip().lstrip(".")
    else:
        # Try to find authors before first period
        first_period = content.find(".")
        if first_period > 0:
            authors = content[:first_period].strip()
            rest = content[first_period + 1 :].strip()
        else:
            authors = "Unknown"
            rest = content

    # Clean up authors
    authors = authors.strip().rstrip(",").strip()

    # Parse rest for title and publication info
    # Title is typically in italics (*Title*) or before the journal
    title = ""
    journal = None
    volume = None
    issue = None
    pages = None
    # Default to 'article'; may be overridden below if a more specific type is detected
    entry_type = "article"
    booktitle = None
    publisher = None
    institution = None

    # Try to extract title (before first italicized section or after first sentence)
    # Format: "Title. *Journal*, vol(issue), pages"
    parts = rest.split("*")

    if len(parts) >= 2:
        # Title before italics, journal in italics
        title = parts[0].strip().rstrip(".")
        journal = parts[1].strip().rstrip(",").rstrip(".")

        # Get remaining info after journal
        if len(parts) > 2:
            remainder = parts[2].strip()
            # Parse volume(issue), pages
            vol_match = re.match(r"(\d+)\(([^)]+)\)", remainder)
            if vol_match:
                volume = vol_match.group(1)
                issue = vol_match.group(2)
                remainder = remainder[vol_match.end() :].strip().lstrip(",").strip()

            # Parse pages
            pages_match = re.match(r"([\d\-–]+)", remainder)
            if pages_match:
                pages = pages_match.group(1).replace("–", "-")
    else:
        # No italics - likely a report, thesis, or web page
        title = rest.strip().rstrip(".")
        entry_type = "misc"

    # Detect entry type based on content
    content_lower = content.lower()
    if "thesis" in content_lower or "dissertation" in content_lower:
        entry_type = "mastersthesis"
        # Try to extract institution
        inst_match = re.search(r"(?:Master's\s+[Tt]hesis|[Dd]issertation),?\s+([^.]+)", rest)
        if inst_match:
            institution = inst_match.group(1).strip()
    elif "proceedings" in content_lower or "conference" in content_lower:
        entry_type = "inproceedings"
        booktitle = journal
        journal = None
    elif any(x in content_lower for x in ["report", "white paper", "whitepaper"]):
        entry_type = "techreport"
        institution = journal if journal else authors
        journal = None
    elif journal is None:
        entry_type = "misc"

    # Clean up title (remove trailing periods, fix quotes)
    title = title.strip().rstrip(".")

    return Reference(
        original_key=original_key,
        authors=authors,
        year=year,
        title=title,
        journal=journal,
        volume=volume,
        issue=issue,
        pages=pages,
        doi=doi,
        url=url,
        entry_type=entry_type,
        publisher=publisher,
        institution=institution,
        booktitle=booktitle,
    )


def generate_citation_key(ref: Reference, existing_keys: dict[str, int]) -> str:
    """Generate a unique citation key in format: firstauthor{year}{suffix}.

    Args:
        ref: The reference to generate a key for
        existing_keys: Dict tracking count of base keys (author+year) used

    Returns:
        Unique citation key like "wu2024" or "wu2024a" if duplicate
    """
    lastname = extract_first_author_lastname(ref.authors)
    base_key = f"{lastname}{ref.year}"

    # Track how many times this base key has been used
    count = existing_keys.get(base_key, 0)
    existing_keys[base_key] = count + 1

    if count == 0:
        return base_key
    # Use a, b, c, ... z for duplicates 1-26, then numeric suffixes
    suffix = chr(ord("a") + count - 1) if count <= 26 else f"{count}"
    return f"{base_key}{suffix}"


# Unicode to LaTeX encoding map for proper rendering in BibTeX
UNICODE_TO_LATEX = {
    "á": r"\'a",
    "à": r"\`a",
    "â": r"\^a",
    "ä": r"\"a",
    "ã": r"\~a",
    "å": r"\aa",
    "ą": r"\k{a}",
    "Á": r"\'A",
    "À": r"\`A",
    "Â": r"\^A",
    "Ä": r"\"A",
    "Ã": r"\~A",
    "Å": r"\AA",
    "Ą": r"\k{A}",
    "ć": r"\'c",
    "č": r"\v{c}",
    "ç": r"\c{c}",
    "Ć": r"\'C",
    "Č": r"\v{C}",
    "Ç": r"\c{C}",
    "đ": r"\dj",
    "ď": r"\v{d}",
    "Đ": r"\DJ",
    "Ď": r"\v{D}",
    "é": r"\'e",
    "è": r"\`e",
    "ê": r"\^e",
    "ë": r"\"e",
    "ě": r"\v{e}",
    "ę": r"\k{e}",
    "É": r"\'E",
    "È": r"\`E",
    "Ê": r"\^E",
    "Ë": r"\"E",
    "Ě": r"\v{E}",
    "Ę": r"\k{E}",
    "í": r"\'i",
    "ì": r"\`i",
    "î": r"\^i",
    "ï": r"\"i",
    "Í": r"\'I",
    "Ì": r"\`I",
    "Î": r"\^I",
    "Ï": r"\"I",
    "ł": r"\l",
    "Ł": r"\L",
    "ń": r"\'n",
    "ň": r"\v{n}",
    "ñ": r"\~n",
    "Ń": r"\'N",
    "Ň": r"\v{N}",
    "Ñ": r"\~N",
    "ó": r"\'o",
    "ò": r"\`o",
    "ô": r"\^o",
    "ö": r"\"o",
    "õ": r"\~o",
    "ø": r"\o",
    "Ó": r"\'O",
    "Ò": r"\`O",
    "Ô": r"\^O",
    "Ö": r"\"O",
    "Õ": r"\~O",
    "Ø": r"\O",
    "ř": r"\v{r}",
    "Ř": r"\v{R}",
    "ś": r"\'s",
    "š": r"\v{s}",
    "ş": r"\c{s}",
    "Ś": r"\'S",
    "Š": r"\v{S}",
    "Ş": r"\c{S}",
    "ť": r"\v{t}",
    "Ť": r"\v{T}",
    "ú": r"\'u",
    "ù": r"\`u",
    "û": r"\^u",
    "ü": r"\"u",
    "ů": r"\r{u}",
    "Ú": r"\'U",
    "Ù": r"\`U",
    "Û": r"\^U",
    "Ü": r"\"U",
    "Ů": r"\r{U}",
    "ý": r"\'y",
    "ÿ": r"\"y",
    "Ý": r"\'Y",
    "Ÿ": r"\"Y",
    "ź": r"\'z",
    "ž": r"\v{z}",
    "ż": r"\.z",
    "Ź": r"\'Z",
    "Ž": r"\v{Z}",
    "Ż": r"\.Z",
    "ß": r"\ss",
    "æ": r"\ae",
    "œ": r"\oe",
    "Æ": r"\AE",
    "Œ": r"\OE",
}


def escape_bibtex(text: str) -> str:
    """Escape special characters for BibTeX, including Unicode to LaTeX."""
    if not text:
        return ""
    # First, escape special LaTeX chars (before Unicode conversion)
    text = text.replace("&", r"\&")
    text = text.replace("%", r"\%")
    text = text.replace("_", r"\_")
    text = text.replace("#", r"\#")
    text = text.replace("$", r"\$")

    # Convert Unicode characters to LaTeX equivalents
    result = []
    for char in text:
        if char in UNICODE_TO_LATEX:
            result.append(UNICODE_TO_LATEX[char])
        else:
            result.append(char)
    text = "".join(result)

    # Protect uppercase letters in titles
    # (BibTeX lowercases titles by default in some styles)
    # Only protect isolated uppercase words
    words = text.split()
    protected_words = []
    for word in words:
        # Protect acronyms (2+ uppercase letters)
        if re.match(r"^[A-Z]{2,}$", word):
            protected_words.append("{" + word + "}")
        else:
            protected_words.append(word)
    return " ".join(protected_words)


def format_bibtex_entry(ref: Reference, citation_key: str) -> str:
    """Format a Reference as a BibTeX entry string."""
    lines = [f"@{ref.entry_type}{{{citation_key},"]

    # Author(s)
    authors = escape_bibtex(ref.authors)
    lines.append(f"  author = {{{authors}}},")

    # Title
    title = escape_bibtex(ref.title)
    lines.append(f"  title = {{{{{title}}}}},")  # Double braces preserve case

    # Year
    lines.append(f"  year = {{{ref.year}}},")

    # Entry-type specific fields
    if ref.entry_type == "article":
        if ref.journal:
            lines.append(f"  journal = {{{escape_bibtex(ref.journal)}}},")
        if ref.volume:
            lines.append(f"  volume = {{{ref.volume}}},")
        if ref.issue:
            lines.append(f"  number = {{{ref.issue}}},")
        if ref.pages:
            lines.append(f"  pages = {{{ref.pages}}},")
    elif ref.entry_type == "inproceedings":
        if ref.booktitle:
            lines.append(f"  booktitle = {{{escape_bibtex(ref.booktitle)}}},")
        if ref.pages:
            lines.append(f"  pages = {{{ref.pages}}},")
    elif ref.entry_type == "techreport":
        if ref.institution:
            lines.append(f"  institution = {{{escape_bibtex(ref.institution)}}},")
    elif ref.entry_type == "mastersthesis":
        if ref.institution:
            lines.append(f"  school = {{{escape_bibtex(ref.institution)}}},")

    # DOI
    if ref.doi:
        lines.append(f"  doi = {{{ref.doi}}},")

    # URL
    if ref.url:
        lines.append(f"  url = {{{ref.url}}},")

    # Note for original key (helpful for verification)
    lines.append(f"  note = {{Original citation: [{ref.original_key}]}},")

    lines.append("}")

    return "\n".join(lines)


def parse_references_from_paper(paper_path: Path) -> list[Reference]:
    """Parse all references from paper.md."""
    content = paper_path.read_text()

    # Find the References section
    ref_section_match = re.search(r"^# References\s*$", content, re.MULTILINE)
    if not ref_section_match:
        print("Error: Could not find '# References' section in paper.md", file=sys.stderr)
        sys.exit(1)

    # Get content after References header, before Appendices
    ref_start = ref_section_match.end()
    appendix_match = re.search(r"^# Appendices?\s*$", content[ref_start:], re.MULTILINE)
    if appendix_match:
        ref_content = content[ref_start : ref_start + appendix_match.start()]
    else:
        ref_content = content[ref_start:]

    # Parse each reference line
    references = []
    for line in ref_content.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        ref = parse_reference_line(line)
        if ref:
            references.append(ref)

    return references


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Convert paper.md references to BibTeX format")
    parser.add_argument("--paper", type=Path, default=Path("paper.md"), help="Path to paper.md")
    parser.add_argument(
        "--output", type=Path, default=Path("references.bib"), help="Output BibTeX file"
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        default=Path("scripts/citation_key_mapping.json"),
        help="Output mapping file",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print output without writing files")
    args = parser.parse_args()

    # Find project root (where paper.md is)
    if not args.paper.exists():
        # Try relative to script location
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        args.paper = project_root / "paper.md"
        args.output = project_root / args.output.name
        args.mapping = project_root / "scripts" / args.mapping.name

    if not args.paper.exists():
        print(f"Error: Could not find paper.md at {args.paper}", file=sys.stderr)
        return 1

    print(f"Parsing references from {args.paper}...")
    references = parse_references_from_paper(args.paper)
    print(f"Found {len(references)} references")

    # Count by type
    academic = sum(1 for r in references if r.original_key.startswith("A"))
    industry = sum(1 for r in references if r.original_key.startswith("I"))
    print(f"  Academic: {academic}, Industry: {industry}")

    # Generate citation keys and mapping
    existing_keys: dict[str, int] = {}
    key_mapping: dict[str, str] = {}
    bibtex_entries: list[str] = []

    for ref in references:
        citation_key = generate_citation_key(ref, existing_keys)
        key_mapping[ref.original_key] = citation_key
        bibtex_entry = format_bibtex_entry(ref, citation_key)
        bibtex_entries.append(bibtex_entry)

    # Generate output
    bibtex_content = "% BibTeX bibliography for YuiQuery Healthcare Analytics Paper\n"
    bibtex_content += f"% Auto-generated from paper.md - {len(references)} entries\n"
    bibtex_content += "% DO NOT EDIT MANUALLY - regenerate with:\n"
    bibtex_content += "%   python scripts/convert_references_to_bibtex.py\n\n"
    bibtex_content += "\n\n".join(bibtex_entries)
    bibtex_content += "\n"

    if args.dry_run:
        print("\n--- BibTeX Output (dry-run) ---")
        print(bibtex_content[:2000])
        print(f"\n... ({len(bibtex_content)} characters total)")
        print("\n--- Key Mapping (dry-run) ---")
        for old_key, new_key in list(key_mapping.items())[:10]:
            print(f"  {old_key} -> {new_key}")
        print(f"  ... ({len(key_mapping)} mappings total)")
    else:
        # Write BibTeX file
        args.output.write_text(bibtex_content)
        print(f"Wrote {args.output}")

        # Write mapping file
        args.mapping.parent.mkdir(parents=True, exist_ok=True)
        mapping_json = {
            "description": "Maps original [A#]/[I#] citations to new BibTeX keys",
            "generated_from": str(args.paper),
            "total_references": len(references),
            "mapping": key_mapping,
        }
        args.mapping.write_text(json.dumps(mapping_json, indent=2) + "\n")
        print(f"Wrote {args.mapping}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
