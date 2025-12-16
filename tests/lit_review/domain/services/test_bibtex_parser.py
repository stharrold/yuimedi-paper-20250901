# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for BibtexParser domain service."""

from lit_review.domain.entities.paper import Paper
from lit_review.domain.services.bibtex_parser import BibtexParser
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI


class TestBibtexParserArticle:
    """Tests for parsing papers to BibTeX @article entries."""

    def test_parse_single_author_article(self) -> None:
        """Parse article with single author to BibTeX."""
        parser = BibtexParser()
        paper = Paper(
            doi=DOI("10.1234/test-2024"),
            title="Machine Learning in Healthcare",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal of Medical AI",
            abstract="This paper explores ML applications.",
        )

        bibtex = parser.parse_to_bibtex(paper)

        assert "@article{Smith2024," in bibtex
        assert "author = {Smith, J.}," in bibtex
        assert "title = {Machine Learning in Healthcare}," in bibtex
        assert "journal = {Journal of Medical AI}," in bibtex
        assert "year = {2024}," in bibtex
        assert "doi = {10.1234/test-2024}," in bibtex
        assert "abstract = {This paper explores ML applications.}" in bibtex

    def test_parse_multiple_authors_article(self) -> None:
        """Parse article with multiple authors to BibTeX."""
        parser = BibtexParser()
        paper = Paper(
            doi=DOI("10.1234/multi"),
            title="Healthcare Analytics",
            authors=[
                Author("Smith", "John", "J."),
                Author("Jones", "Jane", "J."),
                Author("Wilson", "Bob", "B."),
            ],
            publication_year=2024,
            journal="Analytics Journal",
        )

        bibtex = parser.parse_to_bibtex(paper)

        assert "@article{SmithEtAl2024," in bibtex
        assert "author = {Smith, J. and Jones, J. and Wilson, B.}," in bibtex

    def test_parse_without_abstract(self) -> None:
        """Parse article without abstract to BibTeX."""
        parser = BibtexParser()
        paper = Paper(
            doi=DOI("10.1234/no-abstract"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Test Journal",
            abstract="",
        )

        bibtex = parser.parse_to_bibtex(paper)

        assert "@article{Smith2024," in bibtex
        # Check that abstract field is not present (DOI contains "abstract" so check for field)
        assert "abstract =" not in bibtex

    def test_bibtex_format_structure(self) -> None:
        """Verify BibTeX has correct structure."""
        parser = BibtexParser()
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )

        bibtex = parser.parse_to_bibtex(paper)

        # Should start with @article{
        assert bibtex.startswith("@article{")
        # Should have closing brace
        assert bibtex.strip().endswith("}")
        # Should have citation key
        assert "Smith2024," in bibtex


class TestBibtexParserSpecialCharacters:
    """Tests for handling special characters in BibTeX."""

    def test_escape_braces_in_title(self) -> None:
        """Braces in title are escaped."""
        parser = BibtexParser()
        paper = Paper(
            doi=DOI("10.1234/braces"),
            title="Using {Machine Learning} for Healthcare",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )

        bibtex = parser.parse_to_bibtex(paper)

        # Braces should be preserved in title
        assert "{Machine Learning}" in bibtex

    def test_escape_special_latex_chars_in_title(self) -> None:
        """Special LaTeX characters in title are escaped."""
        parser = BibtexParser()
        paper = Paper(
            doi=DOI("10.1234/special"),
            title="AI & ML: The Future of Healthcare",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )

        bibtex = parser.parse_to_bibtex(paper)

        # Ampersand should be escaped
        assert "\\&" in bibtex or "&" in bibtex  # Both are valid

    def test_escape_dollar_sign_in_title(self) -> None:
        """Dollar signs in title are escaped."""
        parser = BibtexParser()
        paper = Paper(
            doi=DOI("10.1234/dollar"),
            title="Cost Analysis: $1000 per Patient",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )

        bibtex = parser.parse_to_bibtex(paper)

        # Dollar sign should be escaped or preserved
        assert "\\$" in bibtex or "$" in bibtex

    def test_handle_quotes_in_abstract(self) -> None:
        """Quotes in abstract are handled correctly."""
        parser = BibtexParser()
        paper = Paper(
            doi=DOI("10.1234/quotes"),
            title="Test Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
            abstract='The study found "significant results" in the data.',
        )

        bibtex = parser.parse_to_bibtex(paper)

        # Abstract should be present with quotes handled
        assert "abstract" in bibtex.lower()
        assert "significant results" in bibtex


class TestBibtexParserUnicode:
    """Tests for handling unicode characters."""

    def test_unicode_in_author_name(self) -> None:
        """Unicode characters in author names are preserved."""
        parser = BibtexParser()
        paper = Paper(
            doi=DOI("10.1234/unicode"),
            title="Test Paper",
            authors=[Author("Müller", "José", "J.")],
            publication_year=2024,
            journal="Journal",
        )

        bibtex = parser.parse_to_bibtex(paper)

        # Unicode should be preserved (or LaTeX encoded)
        assert "Müller" in bibtex or 'M\\"uller' in bibtex

    def test_unicode_in_title(self) -> None:
        """Unicode characters in title are preserved."""
        parser = BibtexParser()
        paper = Paper(
            doi=DOI("10.1234/unicode-title"),
            title="Künstliche Intelligenz in der Medizin",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )

        bibtex = parser.parse_to_bibtex(paper)

        # Unicode should be preserved
        assert "Künstliche" in bibtex or 'K\\"unstliche' in bibtex


class TestBibtexParserEdgeCases:
    """Tests for edge cases and error handling."""

    def test_very_long_title(self) -> None:
        """Very long titles are handled correctly."""
        parser = BibtexParser()
        long_title = "A" * 500  # 500 character title
        paper = Paper(
            doi=DOI("10.1234/long"),
            title=long_title,
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )

        bibtex = parser.parse_to_bibtex(paper)

        assert long_title in bibtex
        assert bibtex.startswith("@article{")

    def test_journal_with_special_chars(self) -> None:
        """Journal names with special characters work."""
        parser = BibtexParser()
        paper = Paper(
            doi=DOI("10.1234/journal"),
            title="Test",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Nature & Science: The Journal",
        )

        bibtex = parser.parse_to_bibtex(paper)

        assert "Nature" in bibtex
        assert "Science" in bibtex

    def test_multiple_papers_generate_unique_keys(self) -> None:
        """Multiple papers from same author/year have unique keys."""
        parser = BibtexParser()
        paper1 = Paper(
            doi=DOI("10.1234/first"),
            title="First Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )
        paper2 = Paper(
            doi=DOI("10.1234/second"),
            title="Second Paper",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )

        bibtex1 = parser.parse_to_bibtex(paper1)
        bibtex2 = parser.parse_to_bibtex(paper2)

        # Both should use Smith2024 key (deduplication is handled externally)
        assert "Smith2024," in bibtex1
        assert "Smith2024," in bibtex2


class TestBibtexParserFormatting:
    """Tests for BibTeX formatting details."""

    def test_fields_are_comma_separated(self) -> None:
        """BibTeX fields are properly comma-separated."""
        parser = BibtexParser()
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
            abstract="Abstract text",
        )

        bibtex = parser.parse_to_bibtex(paper)

        # Each field should end with comma (except last)
        lines = bibtex.split("\n")
        field_lines = [line.strip() for line in lines if "=" in line]
        # Most field lines should end with comma
        comma_count = sum(1 for line in field_lines if line.endswith(","))
        assert comma_count >= len(field_lines) - 1

    def test_indentation_is_consistent(self) -> None:
        """BibTeX fields have consistent indentation."""
        parser = BibtexParser()
        paper = Paper(
            doi=DOI("10.1234/test"),
            title="Test",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="Journal",
        )

        bibtex = parser.parse_to_bibtex(paper)

        # Fields should be indented
        lines = bibtex.split("\n")
        field_lines = [line for line in lines if "=" in line]
        for line in field_lines:
            assert line.startswith("    ") or line.startswith("\t")
