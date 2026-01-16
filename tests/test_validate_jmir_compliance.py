# SPDX-FileCopyrightText: 2025 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Tests for the JMIR compliance validation script.

Tests cover:
- Abstract structure validation (5-section format)
- Abstract word count validation (450 limit)
- Keywords validation (5-10 required)
- IMRD structure validation
- Required section detection
- AI disclosure validation
- CSL configuration validation
- Pandoc citation format validation
- Figure format validation
- Abbreviations usage validation
- Legacy citation format detection
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate_jmir_compliance import (  # noqa: E402
    validate_abbreviations_usage,
    validate_abstract_structure,
    validate_ai_disclosure,
    validate_csl_configuration,
    validate_figure_format,
    validate_imrd_structure,
    validate_keywords,
    validate_no_old_citations,
    validate_pandoc_citations,
    validate_required_sections,
)

# Sample content for testing
VALID_ABSTRACT_CONTENT = """---
title: "Test Paper"
abstract: |
  **Background:** Healthcare organizations face challenges.

  **Objective:** This research examines the evidence.

  **Methods:** We conducted a narrative literature review.

  **Results:** Healthcare-specific benchmarks show progress.

  **Conclusions:** The convergence of technical advances.
keywords: test, jmir
---

# Introduction
"""

MISSING_SECTIONS_ABSTRACT = """---
title: "Test Paper"
abstract: |
  **Background:** Healthcare organizations face challenges.

  **Methods:** We conducted a review.

  **Conclusions:** Results are promising.
keywords: test
---

# Introduction
"""

LONG_ABSTRACT_CONTENT = (
    """---
title: "Test Paper"
abstract: |
  **Background:** """
    + " ".join(["word"] * 100)
    + """

  **Objective:** """
    + " ".join(["word"] * 100)
    + """

  **Methods:** """
    + " ".join(["word"] * 100)
    + """

  **Results:** """
    + " ".join(["word"] * 100)
    + """

  **Conclusions:** """
    + " ".join(["word"] * 100)
    + """
keywords: test
---

# Introduction
"""
)

NO_ABSTRACT_CONTENT = """---
title: "Test Paper"
keywords: test
---

# Introduction

This paper has no abstract.
"""

VALID_SECTIONS_CONTENT = """
# Introduction

Some content here.

# Funding

This research was supported by grants.

# Conflicts of Interest

None declared.

# Data Availability

Data available on request.

# Author Contributions

STH wrote the paper.

# Abbreviations

AI: Artificial Intelligence
"""

MISSING_SECTIONS_CONTENT = """
# Introduction

Some content here.

# Funding

This research was supported by grants.

# Competing Interests

None declared.
"""

VALID_METADATA = """
bibliography: references.bib
csl: citation-style-ama.csl
link-citations: true
"""

INVALID_METADATA = """
bibliography: refs.bib
csl: other-style.csl
"""

OLD_CITATIONS_CONTENT = """
Healthcare analytics has transformed patient care [A1]. The HIMSS model [I1] shows
maturity stages. Studies show 91% success rates [A2][I2].
"""

CLEAN_CITATIONS_CONTENT = """
Healthcare analytics has transformed patient care [@smith2023]. The HIMSS model [@himss2024]
shows maturity stages. Studies show 91% success rates [@jones2024; @catalyst2023].
"""

# Keywords test content
VALID_KEYWORDS_ARRAY = """---
title: "Test Paper"
keywords: [healthcare analytics, NLP, SQL generation, machine learning, AI]
---
"""

VALID_KEYWORDS_TEN = """---
title: "Test Paper"
keywords: [one, two, three, four, five, six, seven, eight, nine, ten]
---
"""

TOO_FEW_KEYWORDS = """---
title: "Test Paper"
keywords: [healthcare, NLP]
---
"""

TOO_MANY_KEYWORDS = """---
title: "Test Paper"
keywords: [one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve]
---
"""

NO_KEYWORDS = """---
title: "Test Paper"
---
"""

# IMRD structure test content
VALID_IMRD_CONTENT = """
# Introduction

Background content.

# Methodology

Methods content.

# Literature Review: Evidence Synthesis

Results content.

# Discussion

Discussion content.
"""

MISSING_METHODS_CONTENT = """
# Introduction

Background content.

# Results

Findings here.

# Discussion

Discussion content.
"""

# AI disclosure test content
VALID_AI_DISCLOSURE = """
# Acknowledgments

The author thanks the reviewers. Gemini assisted with manuscript editing.

# Funding

Grant support.
"""

NO_AI_DISCLOSURE = """
# Acknowledgments

The author thanks the reviewers and colleagues.

# Funding

Grant support.
"""

NO_ACKNOWLEDGMENTS = """
# Funding

Grant support.
"""

# Pandoc citations test content
PANDOC_CITATIONS = """
Healthcare analytics [@smith2023] shows promise. Multiple studies [@jones2024; @doe2024]
confirm this. The HIMSS model [@himss2024] provides guidance.
"""

NO_PANDOC_CITATIONS = """
Healthcare analytics shows promise. Multiple studies confirm this.
The HIMSS model provides guidance.
"""

# Abbreviations usage test content
ABBREV_CONTENT_WITH_SECTION = """
AI systems use SQL queries. AI is transforming healthcare. AI tools are advancing.
SQL databases are common. SQL queries help analysis. SQL is essential.
The IT department manages systems. IT staff turnover is high. IT skills are needed.

# Abbreviations

AI: Artificial Intelligence
SQL: Structured Query Language
IT: Information Technology
"""

ABBREV_CONTENT_MISSING = """
AI systems use SQL queries. AI is transforming healthcare. AI tools are advancing.
HIMSS models are used. HIMSS standards apply. HIMSS maturity helps.

# Abbreviations

AI: Artificial Intelligence
"""


class TestValidateKeywords:
    """Tests for validate_keywords function."""

    def test_valid_array_keywords(self):
        """Should accept 5-10 keywords in array format."""
        result = validate_keywords(VALID_KEYWORDS_ARRAY)

        assert result["valid"] is True
        assert result["count"] == 5
        assert len(result["keywords"]) == 5

    def test_valid_ten_keywords(self):
        """Should accept exactly 10 keywords."""
        result = validate_keywords(VALID_KEYWORDS_TEN)

        assert result["valid"] is True
        assert result["count"] == 10

    def test_too_few_keywords(self):
        """Should reject fewer than 5 keywords."""
        result = validate_keywords(TOO_FEW_KEYWORDS)

        assert result["valid"] is False
        assert result["count"] == 2

    def test_too_many_keywords(self):
        """Should reject more than 10 keywords."""
        result = validate_keywords(TOO_MANY_KEYWORDS)

        assert result["valid"] is False
        assert result["count"] == 12

    def test_no_keywords(self):
        """Should return error when no keywords found."""
        result = validate_keywords(NO_KEYWORDS)

        assert result["valid"] is False
        assert "error" in result


class TestValidateImrdStructure:
    """Tests for validate_imrd_structure function."""

    def test_valid_imrd_structure(self):
        """Should accept valid IMRD structure."""
        result = validate_imrd_structure(VALID_IMRD_CONTENT)

        assert result["valid"] is True
        assert len(result["sections_found"]) == 4
        assert len(result["missing_sections"]) == 0

    def test_missing_methods_detected(self):
        """Should detect missing Methods section."""
        result = validate_imrd_structure(MISSING_METHODS_CONTENT)

        assert result["valid"] is False
        assert "Methods" in result["missing_sections"]

    def test_accepts_methodology_variant(self):
        """Should accept 'Methodology' as Methods."""
        content = """
# Introduction
Intro.
# Methodology
Methods.
# Results
Results.
# Discussion
Discussion.
"""
        result = validate_imrd_structure(content)

        assert result["valid"] is True
        assert "Methods" in result["sections_found"]


class TestValidateAiDisclosure:
    """Tests for validate_ai_disclosure function."""

    def test_valid_ai_disclosure(self):
        """Should detect AI disclosure in Acknowledgments."""
        result = validate_ai_disclosure(VALID_AI_DISCLOSURE)

        assert result["has_acknowledgments"] is True
        assert result["has_ai_disclosure"] is True
        assert len(result["ai_tools_mentioned"]) > 0

    def test_no_ai_disclosure(self):
        """Should detect absence of AI disclosure."""
        result = validate_ai_disclosure(NO_AI_DISCLOSURE)

        assert result["has_acknowledgments"] is True
        assert result["has_ai_disclosure"] is False

    def test_no_acknowledgments(self):
        """Should detect missing Acknowledgments section."""
        result = validate_ai_disclosure(NO_ACKNOWLEDGMENTS)

        assert result["has_acknowledgments"] is False
        assert result["has_ai_disclosure"] is False

    def test_detects_chatgpt(self):
        """Should detect ChatGPT mentions."""
        content = """
# Acknowledgments

ChatGPT was used for initial drafts.
"""
        result = validate_ai_disclosure(content)

        assert result["has_ai_disclosure"] is True


class TestValidatePandocCitations:
    """Tests for validate_pandoc_citations function."""

    def test_finds_pandoc_citations(self):
        """Should find pandoc-style citations."""
        result = validate_pandoc_citations(PANDOC_CITATIONS)

        assert result["has_citations"] is True
        assert result["citation_count"] >= 3
        assert result["unique_keys"] >= 4

    def test_no_citations(self):
        """Should detect absence of citations."""
        result = validate_pandoc_citations(NO_PANDOC_CITATIONS)

        assert result["has_citations"] is False
        assert result["citation_count"] == 0

    def test_multi_citations(self):
        """Should handle multiple citations in one bracket."""
        content = "Studies [@a2023; @b2023; @c2023] show results."
        result = validate_pandoc_citations(content)

        assert result["has_citations"] is True
        assert result["unique_keys"] == 3


class TestValidateFigureFormat:
    """Tests for validate_figure_format function."""

    def test_no_figures_dir(self, tmp_path: Path):
        """Should handle missing figures directory."""
        result = validate_figure_format(tmp_path)

        assert result["valid"] is True
        assert "note" in result

    def test_all_png_figures(self, tmp_path: Path):
        """Should accept all PNG figures."""
        figures_dir = tmp_path / "figures"
        figures_dir.mkdir()
        (figures_dir / "fig1.png").touch()
        (figures_dir / "fig2.png").touch()

        result = validate_figure_format(tmp_path)

        assert result["valid"] is True
        assert result["png_count"] == 2

    def test_non_png_figures(self, tmp_path: Path):
        """Should detect non-PNG figures."""
        figures_dir = tmp_path / "figures"
        figures_dir.mkdir()
        (figures_dir / "fig1.jpg").touch()
        (figures_dir / "fig2.png").touch()

        result = validate_figure_format(tmp_path)

        assert result["valid"] is False
        assert "fig1.jpg" in result["non_png_figures"]

    def test_allows_mmd_source_files(self, tmp_path: Path):
        """Should allow .mmd source file derivatives."""
        figures_dir = tmp_path / "figures"
        figures_dir.mkdir()
        (figures_dir / "diagram.mmd.png").touch()
        (figures_dir / "diagram.mmd.svg").touch()

        result = validate_figure_format(tmp_path)

        assert result["valid"] is True


class TestValidateAbbreviationsUsage:
    """Tests for validate_abbreviations_usage function."""

    def test_all_abbreviations_listed(self, tmp_path: Path):
        """Should pass when all frequent abbreviations are listed."""
        # Create temp config
        config = tmp_path / "abbreviations.json"
        config.write_text(
            '{"AI": "Artificial Intelligence", "SQL": "Structured Query Language", "IT": "Information Technology"}'
        )

        result = validate_abbreviations_usage(ABBREV_CONTENT_WITH_SECTION, config)

        assert result["valid"] is True
        assert len(result["missing_abbrevs"]) == 0

    def test_missing_abbreviation_detected(self, tmp_path: Path):
        """Should detect abbreviations used >=3 times but not listed."""
        config = tmp_path / "abbreviations.json"
        config.write_text('{"AI": "Artificial Intelligence", "HIMSS": "HIMSS", "SQL": "SQL"}')

        result = validate_abbreviations_usage(ABBREV_CONTENT_MISSING, config)

        assert result["valid"] is False
        # HIMSS appears 3 times in ABBREV_CONTENT_MISSING but is not listed
        # AI appears 3 times and IS listed, so should not be in missing
        # SQL appears 0 times in ABBREV_CONTENT_MISSING
        assert "HIMSS" in result["missing_abbrevs"]
        assert "AI" not in result["missing_abbrevs"]  # AI is listed in the section

    def test_no_abbreviations_section(self):
        """Should return error when no Abbreviations section."""
        content = "AI is used. AI helps. AI transforms."

        result = validate_abbreviations_usage(content)

        assert result["valid"] is False
        assert "error" in result


class TestValidateAbstractStructure:
    """Tests for validate_abstract_structure function."""

    def test_valid_abstract_passes(self):
        """Should pass when all 5 sections are present."""
        result = validate_abstract_structure(VALID_ABSTRACT_CONTENT)

        assert result["valid"] is True
        assert result["missing_headers"] == []
        assert result["within_limit"] is True

    def test_missing_sections_detected(self):
        """Should detect missing abstract sections."""
        result = validate_abstract_structure(MISSING_SECTIONS_ABSTRACT)

        assert result["valid"] is False
        assert "**Objective:**" in result["missing_headers"]
        assert "**Results:**" in result["missing_headers"]

    def test_word_count_calculated(self):
        """Should calculate word count correctly."""
        result = validate_abstract_structure(VALID_ABSTRACT_CONTENT)

        assert result["word_count"] > 0
        assert result["word_count"] < 450

    def test_long_abstract_detected(self):
        """Should detect abstracts exceeding 450 words."""
        result = validate_abstract_structure(LONG_ABSTRACT_CONTENT)

        assert result["word_count"] > 450
        assert result["within_limit"] is False

    def test_no_abstract_returns_error(self):
        """Should return error when no abstract found."""
        result = validate_abstract_structure(NO_ABSTRACT_CONTENT)

        assert result["valid"] is False
        assert "error" in result
        assert result["word_count"] == 0


class TestValidateRequiredSections:
    """Tests for validate_required_sections function."""

    def test_all_sections_present(self):
        """Should detect when all required sections are present."""
        result = validate_required_sections(VALID_SECTIONS_CONTENT)

        assert result["Funding"] is True
        assert result["Conflicts of Interest"] is True
        assert result["Data Availability"] is True
        assert result["Author Contributions"] is True
        assert result["Abbreviations"] is True

    def test_missing_sections_detected(self):
        """Should detect missing required sections."""
        result = validate_required_sections(MISSING_SECTIONS_CONTENT)

        assert result["Funding"] is True
        assert result["Conflicts of Interest"] is False  # Has "Competing Interests" instead
        assert result["Data Availability"] is False
        assert result["Author Contributions"] is False
        assert result["Abbreviations"] is False

    def test_competing_interests_not_accepted(self):
        """Should require 'Conflicts of Interest' not 'Competing Interests'."""
        content = """
# Funding
Grant support.

# Competing Interests
None.
"""
        result = validate_required_sections(content)

        assert result["Conflicts of Interest"] is False


class TestValidateCslConfiguration:
    """Tests for validate_csl_configuration function."""

    def test_valid_configuration(self):
        """Should detect valid CSL configuration."""
        result = validate_csl_configuration(VALID_METADATA)

        assert result["bibliography_configured"] is True
        assert result["csl_configured"] is True
        assert result["ama_style"] is True

    def test_invalid_configuration(self):
        """Should detect invalid CSL configuration."""
        result = validate_csl_configuration(INVALID_METADATA)

        assert result["bibliography_configured"] is False
        assert result["csl_configured"] is False
        assert result["ama_style"] is False

    def test_partial_configuration(self):
        """Should detect partial configuration."""
        partial_metadata = """
bibliography: references.bib
csl: citation-style.csl
"""
        result = validate_csl_configuration(partial_metadata)

        assert result["bibliography_configured"] is True
        assert result["csl_configured"] is True
        assert result["ama_style"] is False


class TestValidateNoOldCitations:
    """Tests for validate_no_old_citations function."""

    def test_detects_old_academic_citations(self):
        """Should detect old [A#] citation format."""
        result = validate_no_old_citations(OLD_CITATIONS_CONTENT)

        assert result["clean"] is False
        assert result["old_academic_count"] == 2

    def test_detects_old_industry_citations(self):
        """Should detect old [I#] citation format."""
        result = validate_no_old_citations(OLD_CITATIONS_CONTENT)

        assert result["clean"] is False
        assert result["old_industry_count"] == 2

    def test_clean_content_passes(self):
        """Should pass when no old citations present."""
        result = validate_no_old_citations(CLEAN_CITATIONS_CONTENT)

        assert result["clean"] is True
        assert result["old_academic_count"] == 0
        assert result["old_industry_count"] == 0


class TestWithRealPaper:
    """Integration tests using actual paper.md."""

    @pytest.fixture
    def repo_root(self) -> Path:
        """Return the repository root directory."""
        return Path(__file__).parent.parent

    @pytest.fixture
    def paper_content(self, repo_root: Path) -> str:
        """Load the actual paper content."""
        paper_path = repo_root / "paper.md"
        if not paper_path.exists():
            pytest.skip("paper.md not found")
        return paper_path.read_text()

    @pytest.fixture
    def metadata_content(self, repo_root: Path) -> str:
        """Load the actual metadata content."""
        metadata_path = repo_root / "metadata.yaml"
        if not metadata_path.exists():
            pytest.skip("metadata.yaml not found")
        return metadata_path.read_text()

    def test_real_paper_abstract_valid(self, paper_content: str):
        """Real paper should have valid 5-section abstract."""
        result = validate_abstract_structure(paper_content)

        assert result["valid"] is True, f"Missing headers: {result.get('missing_headers', [])}"
        assert result["within_limit"] is True, f"Word count: {result['word_count']}/450"

    def test_real_paper_sections_present(self, paper_content: str):
        """Real paper should have all required sections."""
        result = validate_required_sections(paper_content)

        for section, present in result.items():
            assert present is True, f"Missing section: {section}"

    def test_real_paper_csl_configured(self, metadata_content: str):
        """Real paper should have proper CSL configuration."""
        result = validate_csl_configuration(metadata_content)

        assert result["bibliography_configured"] is True
        assert result["csl_configured"] is True
        assert result["ama_style"] is True

    def test_real_paper_no_old_citations(self, paper_content: str):
        """Real paper should have no legacy [A#]/[I#] citations."""
        result = validate_no_old_citations(paper_content)

        assert result["clean"] is True, (
            f"Found {result['old_academic_count']} old academic citations, "
            f"{result['old_industry_count']} old industry citations"
        )

    def test_real_paper_keywords_valid(self, paper_content: str):
        """Real paper should have 5-10 keywords."""
        result = validate_keywords(paper_content)

        assert result["valid"] is True, f"Keywords count: {result['count']}/5-10"
        assert 5 <= result["count"] <= 10

    def test_real_paper_imrd_structure(self, paper_content: str):
        """Real paper should have IMRD structure."""
        result = validate_imrd_structure(paper_content)

        assert result["valid"] is True, f"Missing sections: {result['missing_sections']}"
        assert len(result["sections_found"]) == 4

    def test_real_paper_ai_disclosure(self, paper_content: str):
        """Real paper should have AI disclosure in Acknowledgments."""
        result = validate_ai_disclosure(paper_content)

        assert result["has_acknowledgments"] is True
        assert result["has_ai_disclosure"] is True

    def test_real_paper_pandoc_citations(self, paper_content: str):
        """Real paper should use pandoc citation format."""
        result = validate_pandoc_citations(paper_content)

        assert result["has_citations"] is True
        assert result["citation_count"] > 0
        assert result["unique_keys"] > 0

    def test_real_paper_figure_format(self, repo_root: Path):
        """Real paper figures should be PNG format."""
        result = validate_figure_format(repo_root)

        assert result["valid"] is True, f"Non-PNG figures: {result['non_png_figures']}"

    def test_real_paper_abbreviations_usage(self, paper_content: str):
        """Real paper should list all frequently used abbreviations."""
        result = validate_abbreviations_usage(paper_content)

        assert result["valid"] is True, (
            f"Missing abbreviations: {result.get('missing_abbrevs', [])}"
        )
