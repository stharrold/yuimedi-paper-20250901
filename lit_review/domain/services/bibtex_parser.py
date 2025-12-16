# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""BibTeX parser domain service.

Converts Paper entities to BibTeX format for bibliography management.
"""

from lit_review.domain.entities.paper import Paper


class BibtexParser:
    """Service for converting Papers to BibTeX format.

    Generates properly formatted BibTeX entries for @article, @inproceedings,
    and @book types with proper escaping of special characters.

    Example:
        >>> parser = BibtexParser()
        >>> bibtex = parser.parse_to_bibtex(paper)
        >>> print(bibtex)
        @article{Smith2024,
            author = {Smith, J.},
            title = {Machine Learning in Healthcare},
            journal = {Journal of Medical AI},
            year = {2024},
            doi = {10.1234/test-2024}
        }
    """

    def parse_to_bibtex(self, paper: Paper, entry_type: str = "article") -> str:
        """Convert Paper entity to BibTeX format.

        Args:
            paper: Paper entity to convert.
            entry_type: BibTeX entry type (article, inproceedings, book).
                Defaults to "article".

        Returns:
            Formatted BibTeX entry string.

        Example:
            >>> parser = BibtexParser()
            >>> bibtex = parser.parse_to_bibtex(paper)
        """
        citation_key = paper.get_citation_key()

        # Build author string
        author_list = [author.format_citation() for author in paper.authors]
        authors_str = " and ".join(author_list)

        # Build BibTeX entry
        lines = [
            f"@{entry_type}{{{citation_key},",
            f"    author = {{{authors_str}}},",
            f"    title = {{{self._escape_special_chars(paper.title)}}},",
            f"    journal = {{{self._escape_special_chars(paper.journal)}}},",
            f"    year = {{{paper.publication_year}}},",
            f"    doi = {{{paper.doi.value}}},",
        ]

        # Add optional abstract
        if paper.abstract and paper.abstract.strip():
            abstract_escaped = self._escape_special_chars(paper.abstract)
            lines.append(f"    abstract = {{{abstract_escaped}}},")

        # Remove trailing comma from last field and add closing brace
        lines[-1] = lines[-1].rstrip(",")
        lines.append("}")

        return "\n".join(lines)

    def _escape_special_chars(self, text: str) -> str:
        """Escape special LaTeX/BibTeX characters in text.

        Args:
            text: Text to escape.

        Returns:
            Text with special characters escaped.

        Note:
            Common special characters in LaTeX: & % $ # _ { } ~ ^ \\
            We preserve braces {} for BibTeX formatting, escape the rest.
        """
        # For BibTeX, we need to be careful with escaping
        # Most special chars can stay as-is in modern BibTeX processors
        # We'll do minimal escaping to preserve readability

        # Escape backslash first (before other escapes)
        text = text.replace("\\", "\\textbackslash{}")

        # Escape special LaTeX chars that aren't used in BibTeX formatting
        # Note: We preserve {}, they're part of BibTeX syntax
        replacements = {
            "&": "\\&",
            "%": "\\%",
            "$": "\\$",
            "#": "\\#",
            "_": "\\_",
            "~": "\\textasciitilde{}",
            "^": "\\textasciicircum{}",
        }

        for char, escaped in replacements.items():
            text = text.replace(char, escaped)

        return text
