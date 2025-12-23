# SPDX-FileCopyrightText: 2025 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Tests for the abbreviation extraction script.

Tests cover:
- Abbreviation extraction from paper content
- Minimum count filtering
- Markdown section formatting
- Known abbreviations dictionary coverage
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from extract_abbreviations import (  # noqa: E402
    extract_abbreviations,
    format_abbreviations_section,
)

# Sample content for testing
SAMPLE_PAPER_CONTENT = """
# Introduction

Healthcare organizations using Electronic Health Records (EHR) face challenges.
The Healthcare Information Management Systems Society (HIMSS) developed the
Analytics Maturity Assessment Model (AMAM) to measure progress.

Natural Language to SQL (NL2SQL) systems powered by Large Language Models (LLM)
and Retrieval-Augmented Generation (RAG) offer solutions.

## Methods

We used Artificial Intelligence (AI) techniques with Structured Query Language (SQL)
queries. The Electronic Medical Record Adoption Model (EMRAM) from HIMSS was used
as reference. EHR systems were analyzed using HIMSS AMAM stages.

## Results

AI and LLM approaches showed promise. EHR adoption via EMRAM increased.
NL2SQL accuracy improved. HIMSS AMAM stages were assessed.
"""

MINIMAL_CONTENT = """
Just mentioning EHR once.
"""

CONTENT_WITH_ALL_ABBREVS = """
AACODS is used for grey literature assessment.
ACO organizations participate.
AI is transforming healthcare.
AMAM measures analytics maturity.
API connections are standard.
CPT codes are used for billing.
DAMAF provides assessment.
DIKW hierarchy applies.
EHR systems are widespread.
EMRAM tracks EMR adoption.
HDQM2 addresses data quality.
HIMSS sets standards.
ICD codes classify diseases.
IT departments manage systems.
LLM models assist.
NL2SQL converts queries.
RAG retrieves context.
SQL is the query language.
"""


@pytest.fixture
def temp_paper_file(tmp_path: Path) -> Path:
    """Create a temporary paper file with sample content."""
    paper_path = tmp_path / "paper.md"
    paper_path.write_text(SAMPLE_PAPER_CONTENT)
    return paper_path


@pytest.fixture
def minimal_paper_file(tmp_path: Path) -> Path:
    """Create a temporary paper file with minimal content."""
    paper_path = tmp_path / "paper.md"
    paper_path.write_text(MINIMAL_CONTENT)
    return paper_path


@pytest.fixture
def all_abbrevs_file(tmp_path: Path) -> Path:
    """Create a temporary paper file with all abbreviations."""
    paper_path = tmp_path / "paper.md"
    paper_path.write_text(CONTENT_WITH_ALL_ABBREVS)
    return paper_path


class TestExtractAbbreviations:
    """Tests for extract_abbreviations function."""

    def test_extracts_known_abbreviations(self, temp_paper_file: Path):
        """Should extract known abbreviations from content."""
        result = extract_abbreviations(temp_paper_file)

        assert "EHR" in result
        assert "HIMSS" in result
        assert "AI" in result
        assert "NL2SQL" in result

    def test_returns_full_term_and_count(self, temp_paper_file: Path):
        """Should return tuple of (full_term, count) for each abbreviation."""
        result = extract_abbreviations(temp_paper_file)

        full_term, count = result["EHR"]
        assert full_term == "Electronic Health Record"
        assert count >= 1

    def test_counts_abbreviations_correctly(self, temp_paper_file: Path):
        """Should count occurrences correctly."""
        result = extract_abbreviations(temp_paper_file)

        # HIMSS appears multiple times in sample content
        _, himss_count = result["HIMSS"]
        assert himss_count >= 3

        # EHR appears multiple times
        _, ehr_count = result["EHR"]
        assert ehr_count >= 2

    def test_min_count_filter_default(self, temp_paper_file: Path):
        """Should include abbreviations with count >= 1 by default."""
        result = extract_abbreviations(temp_paper_file)

        # All found abbreviations should have count >= 1
        for abbrev, (_, count) in result.items():
            assert count >= 1, f"{abbrev} has count {count} < 1"

    def test_min_count_filter_custom(self, temp_paper_file: Path):
        """Should respect custom min_count parameter."""
        result = extract_abbreviations(temp_paper_file, min_count=3)

        # Only abbreviations with count >= 3 should be included
        for abbrev, (_, count) in result.items():
            assert count >= 3, f"{abbrev} has count {count} < 3"

    def test_min_count_filter_excludes_low_count(self, minimal_paper_file: Path):
        """Should exclude abbreviations below min_count threshold."""
        result_default = extract_abbreviations(minimal_paper_file, min_count=1)
        result_high = extract_abbreviations(minimal_paper_file, min_count=5)

        # With min_count=1, EHR should be found
        assert "EHR" in result_default

        # With min_count=5, EHR should not be found (only appears once)
        assert "EHR" not in result_high

    def test_all_known_abbreviations_can_be_found(self, all_abbrevs_file: Path):
        """Should be able to find all known abbreviations when present."""
        result = extract_abbreviations(all_abbrevs_file)

        expected_abbrevs = [
            "AACODS",
            "ACO",
            "AI",
            "AMAM",
            "API",
            "CPT",
            "DAMAF",
            "DIKW",
            "EHR",
            "EMRAM",
            "HDQM2",
            "HIMSS",
            "ICD",
            "IT",
            "LLM",
            "NL2SQL",
            "RAG",
            "SQL",
        ]

        for abbrev in expected_abbrevs:
            assert abbrev in result, f"Known abbreviation {abbrev} not found"


class TestFormatAbbreviationsSection:
    """Tests for format_abbreviations_section function."""

    def test_generates_markdown_header(self):
        """Should generate markdown with # Abbreviations header."""
        abbrevs = {"AI": ("Artificial Intelligence", 5)}
        result = format_abbreviations_section(abbrevs)

        assert result.startswith("# Abbreviations")

    def test_formats_abbreviation_correctly(self):
        """Should format as 'ABBREV: Full Term'."""
        abbrevs = {"AI": ("Artificial Intelligence", 5)}
        result = format_abbreviations_section(abbrevs)

        assert "AI: Artificial Intelligence" in result

    def test_sorts_alphabetically(self):
        """Should sort abbreviations alphabetically."""
        abbrevs = {
            "SQL": ("Structured Query Language", 3),
            "AI": ("Artificial Intelligence", 5),
            "EHR": ("Electronic Health Record", 4),
        }
        result = format_abbreviations_section(abbrevs)

        lines = result.split("\n")
        abbrev_lines = [line for line in lines if ": " in line and not line.startswith("#")]

        # AI should come before EHR, EHR before SQL
        ai_idx = next(i for i, line in enumerate(abbrev_lines) if line.startswith("AI:"))
        ehr_idx = next(i for i, line in enumerate(abbrev_lines) if line.startswith("EHR:"))
        sql_idx = next(i for i, line in enumerate(abbrev_lines) if line.startswith("SQL:"))

        assert ai_idx < ehr_idx < sql_idx

    def test_handles_empty_dict(self):
        """Should handle empty abbreviations dict."""
        result = format_abbreviations_section({})

        assert "# Abbreviations" in result
        # Should only have header and blank line
        lines = [line for line in result.split("\n") if line.strip()]
        assert len(lines) == 1

    def test_multiple_abbreviations(self):
        """Should format multiple abbreviations correctly."""
        abbrevs = {
            "AI": ("Artificial Intelligence", 5),
            "EHR": ("Electronic Health Record", 4),
            "SQL": ("Structured Query Language", 3),
        }
        result = format_abbreviations_section(abbrevs)

        assert "AI: Artificial Intelligence" in result
        assert "EHR: Electronic Health Record" in result
        assert "SQL: Structured Query Language" in result


class TestWithRealPaper:
    """Integration tests using actual paper.md."""

    @pytest.fixture
    def repo_root(self) -> Path:
        """Return the repository root directory."""
        return Path(__file__).parent.parent

    @pytest.fixture
    def paper_path(self, repo_root: Path) -> Path:
        """Get the actual paper path."""
        path = repo_root / "paper.md"
        if not path.exists():
            pytest.skip("paper.md not found")
        return path

    def test_extracts_from_real_paper(self, paper_path: Path):
        """Should extract abbreviations from real paper."""
        result = extract_abbreviations(paper_path)

        # Paper should have multiple abbreviations
        assert len(result) > 5

        # Key abbreviations should be present
        assert "HIMSS" in result
        assert "EHR" in result
        assert "NL2SQL" in result

    def test_real_paper_abbreviations_have_definitions(self, paper_path: Path):
        """All extracted abbreviations should have full term definitions."""
        result = extract_abbreviations(paper_path)

        for abbrev, (full_term, count) in result.items():
            assert full_term, f"{abbrev} has empty full term"
            assert len(full_term) > len(abbrev), f"{abbrev} full term shorter than abbreviation"
            assert count >= 1, f"{abbrev} has invalid count"

    def test_real_paper_section_is_valid_markdown(self, paper_path: Path):
        """Generated section should be valid markdown."""
        abbrevs = extract_abbreviations(paper_path)
        section = format_abbreviations_section(abbrevs)

        # Should start with header
        assert section.startswith("# Abbreviations")

        # Each non-empty, non-header line should have colon separator
        lines = section.split("\n")
        for line in lines[2:]:  # Skip header and blank line
            if line.strip():
                assert ": " in line, f"Invalid line format: {line}"
