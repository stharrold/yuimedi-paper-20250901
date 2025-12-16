# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for CitationFormatter service."""

import pytest

from lit_review.domain.entities.paper import Paper
from lit_review.domain.services.citation_formatter import CitationFormatter
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


@pytest.fixture
def formatter() -> CitationFormatter:
    """Return a CitationFormatter instance."""
    return CitationFormatter()


@pytest.fixture
def single_author_paper() -> Paper:
    """Return a paper with a single author."""
    return Paper(
        doi=DOI("10.1234/single"),
        title="Single Author Paper",
        authors=[Author("Smith", "John", "J.")],
        publication_year=2024,
        journal="Test Journal",
    )


@pytest.fixture
def two_author_paper() -> Paper:
    """Return a paper with two authors."""
    return Paper(
        doi=DOI("10.1234/two"),
        title="Two Author Paper",
        authors=[
            Author("Smith", "John", "J."),
            Author("Jones", "Jane", "J."),
        ],
        publication_year=2024,
        journal="Test Journal",
    )


@pytest.fixture
def multi_author_paper() -> Paper:
    """Return a paper with three authors."""
    return Paper(
        doi=DOI("10.1234/multi"),
        title="Multi Author Paper",
        authors=[
            Author("Smith", "John", "J."),
            Author("Jones", "Jane", "J."),
            Author("Wilson", "Bob", "B."),
        ],
        publication_year=2024,
        journal="Test Journal",
        abstract="This is a test abstract.",
        keywords=["test", "paper"],
    )


class TestBibTeXFormat:
    """Tests for BibTeX formatting."""

    def test_bibtex_single_author(
        self, formatter: CitationFormatter, single_author_paper: Paper
    ) -> None:
        """BibTeX format for single author paper."""
        bibtex = formatter.format_bibtex(single_author_paper)
        assert "@article{Smith2024," in bibtex
        assert "author = {Smith, J.}" in bibtex
        assert "title = {Single Author Paper}" in bibtex
        assert "journal = {Test Journal}" in bibtex
        assert "year = {2024}" in bibtex
        assert "doi = {10.1234/single}" in bibtex

    def test_bibtex_two_authors(
        self, formatter: CitationFormatter, two_author_paper: Paper
    ) -> None:
        """BibTeX format for two author paper."""
        bibtex = formatter.format_bibtex(two_author_paper)
        assert "@article{SmithJones2024," in bibtex
        assert "author = {Smith, J. and Jones, J.}" in bibtex

    def test_bibtex_multi_authors(
        self, formatter: CitationFormatter, multi_author_paper: Paper
    ) -> None:
        """BibTeX format for multi-author paper."""
        bibtex = formatter.format_bibtex(multi_author_paper)
        assert "@article{SmithEtAl2024," in bibtex
        assert "author = {Smith, J. and Jones, J. and Wilson, B.}" in bibtex

    def test_bibtex_includes_keywords(
        self, formatter: CitationFormatter, multi_author_paper: Paper
    ) -> None:
        """BibTeX includes keywords when present."""
        bibtex = formatter.format_bibtex(multi_author_paper)
        assert "keywords = {test, paper}" in bibtex

    def test_bibtex_includes_abstract(
        self, formatter: CitationFormatter, multi_author_paper: Paper
    ) -> None:
        """BibTeX includes abstract when present."""
        bibtex = formatter.format_bibtex(multi_author_paper)
        assert "abstract = {This is a test abstract.}" in bibtex


class TestAPAFormat:
    """Tests for APA formatting."""

    def test_apa_single_author(
        self, formatter: CitationFormatter, single_author_paper: Paper
    ) -> None:
        """APA format for single author paper."""
        apa = formatter.format_apa(single_author_paper)
        assert "Smith, J." in apa
        assert "(2024)" in apa
        assert "Single Author Paper" in apa
        assert "Test Journal" in apa
        assert "https://doi.org/10.1234/single" in apa

    def test_apa_two_authors(self, formatter: CitationFormatter, two_author_paper: Paper) -> None:
        """APA format for two author paper."""
        apa = formatter.format_apa(two_author_paper)
        assert "Smith, J., & Jones, J." in apa

    def test_apa_multi_authors_uses_et_al(
        self, formatter: CitationFormatter, multi_author_paper: Paper
    ) -> None:
        """APA format uses 'et al.' for 3+ authors."""
        apa = formatter.format_apa(multi_author_paper)
        assert "Smith, J., et al." in apa


class TestChicagoFormat:
    """Tests for Chicago formatting."""

    def test_chicago_single_author(
        self, formatter: CitationFormatter, single_author_paper: Paper
    ) -> None:
        """Chicago format for single author paper."""
        chicago = formatter.format_chicago(single_author_paper)
        assert "Smith, John." in chicago
        assert "2024." in chicago
        assert '"Single Author Paper."' in chicago
        assert "Test Journal." in chicago
        assert "https://doi.org/10.1234/single." in chicago

    def test_chicago_two_authors(
        self, formatter: CitationFormatter, two_author_paper: Paper
    ) -> None:
        """Chicago format for two author paper."""
        chicago = formatter.format_chicago(two_author_paper)
        assert "Smith, John, and Jane Jones." in chicago

    def test_chicago_multi_authors_uses_et_al(
        self, formatter: CitationFormatter, multi_author_paper: Paper
    ) -> None:
        """Chicago format uses 'et al.' for 3+ authors."""
        chicago = formatter.format_chicago(multi_author_paper)
        assert "Smith, John, et al." in chicago


class TestVancouverFormat:
    """Tests for Vancouver formatting."""

    def test_vancouver_single_author(
        self, formatter: CitationFormatter, single_author_paper: Paper
    ) -> None:
        """Vancouver format for single author paper."""
        vancouver = formatter.format_vancouver(single_author_paper)
        assert "Smith J." in vancouver
        assert "Single Author Paper." in vancouver
        assert "Test Journal." in vancouver
        assert "2024;" in vancouver
        assert "doi:10.1234/single" in vancouver

    def test_vancouver_two_authors(
        self, formatter: CitationFormatter, two_author_paper: Paper
    ) -> None:
        """Vancouver format for two author paper."""
        vancouver = formatter.format_vancouver(two_author_paper)
        assert "Smith J, Jones J." in vancouver

    def test_vancouver_multi_authors(
        self, formatter: CitationFormatter, multi_author_paper: Paper
    ) -> None:
        """Vancouver format for multi-author paper."""
        vancouver = formatter.format_vancouver(multi_author_paper)
        assert "Smith J, Jones J, Wilson B." in vancouver
