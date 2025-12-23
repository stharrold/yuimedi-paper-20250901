# SPDX-FileCopyrightText: 2025 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
"""Tests for the JMIR compliance validation script.

Tests cover:
- Abstract structure validation (5-section format)
- Abstract word count validation (450 limit)
- Required section detection
- CSL configuration validation
- Legacy citation format detection
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate_jmir_compliance import (  # noqa: E402
    validate_abstract_structure,
    validate_csl_configuration,
    validate_no_old_citations,
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
