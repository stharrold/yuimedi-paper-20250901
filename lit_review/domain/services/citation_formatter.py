# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Citation formatter service for generating formatted citations.

Provides methods to format Paper entities into various citation formats
including BibTeX, APA, and other academic citation styles.
"""

from lit_review.domain.entities.paper import Paper


class CitationFormatter:
    """Service for formatting paper citations.

    Provides methods to convert Paper entities into standard citation formats
    for academic writing and bibliography generation.

    Example:
        >>> formatter = CitationFormatter()
        >>> bibtex = formatter.format_bibtex(paper)
    """

    def format_bibtex(self, paper: Paper) -> str:
        """Format paper as BibTeX entry.

        Args:
            paper: Paper to format.

        Returns:
            BibTeX formatted string.

        Example:
            @article{Smith2024,
                author = {Smith, J. and Jones, J.},
                title = {Test Paper},
                journal = {Test Journal},
                year = {2024},
                doi = {10.1234/test}
            }
        """
        citation_key = paper.get_citation_key()

        # Format authors: Last1, I1. and Last2, I2.
        authors = " and ".join(author.format_citation() for author in paper.authors)

        # Format keywords if present
        keywords_line = ""
        if paper.keywords:
            keywords_line = f",\n    keywords = {{{', '.join(paper.keywords)}}}"

        # Format abstract if present
        abstract_line = ""
        if paper.abstract:
            # Escape special characters in abstract
            escaped_abstract = (
                paper.abstract.replace("{", "\\{")
                .replace("}", "\\}")
                .replace("&", "\\&")
                .replace("%", "\\%")
            )
            abstract_line = f",\n    abstract = {{{escaped_abstract}}}"

        return f"""@article{{{citation_key},
    author = {{{authors}}},
    title = {{{paper.title}}},
    journal = {{{paper.journal}}},
    year = {{{paper.publication_year}}},
    doi = {{{paper.doi.value}}}{keywords_line}{abstract_line}
}}"""

    def format_apa(self, paper: Paper) -> str:
        """Format paper in APA 7th edition style.

        Args:
            paper: Paper to format.

        Returns:
            APA formatted citation string.

        Example:
            Smith, J., & Jones, J. (2024). Test Paper. Test Journal.
            https://doi.org/10.1234/test
        """
        # Format authors
        if len(paper.authors) == 1:
            authors_str = paper.authors[0].format_citation()
        elif len(paper.authors) == 2:
            authors_str = (
                f"{paper.authors[0].format_citation()}, & {paper.authors[1].format_citation()}"
            )
        else:
            # More than 2 authors: First author, et al.
            authors_str = f"{paper.authors[0].format_citation()}, et al."

        return (
            f"{authors_str} ({paper.publication_year}). {paper.title}. "
            f"{paper.journal}. {paper.doi.to_url()}"
        )

    def format_chicago(self, paper: Paper) -> str:
        """Format paper in Chicago author-date style.

        Args:
            paper: Paper to format.

        Returns:
            Chicago formatted citation string.

        Example:
            Smith, John, and Jane Jones. 2024. "Test Paper."
            Test Journal. https://doi.org/10.1234/test.
        """
        # Format authors with full first names
        if len(paper.authors) == 1:
            authors_str = f"{paper.authors[0].last_name}, {paper.authors[0].first_name}"
        elif len(paper.authors) == 2:
            authors_str = (
                f"{paper.authors[0].last_name}, {paper.authors[0].first_name}, "
                f"and {paper.authors[1].first_name} {paper.authors[1].last_name}"
            )
        else:
            # More than 2 authors
            first = paper.authors[0]
            authors_str = f"{first.last_name}, {first.first_name}, et al."

        return (
            f'{authors_str}. {paper.publication_year}. "{paper.title}." '
            f"{paper.journal}. {paper.doi.to_url()}."
        )

    def format_vancouver(self, paper: Paper) -> str:
        """Format paper in Vancouver style (common in medical journals).

        Args:
            paper: Paper to format.

        Returns:
            Vancouver formatted citation string.

        Example:
            Smith J, Jones J. Test Paper. Test Journal. 2024;
            doi:10.1234/test
        """
        # Format authors: Last I
        authors = ", ".join(
            f"{a.last_name} {a.initials.replace('.', '')}"
            for a in paper.authors[:6]  # Vancouver limits to 6 authors
        )
        if len(paper.authors) > 6:
            authors += ", et al"

        return (
            f"{authors}. {paper.title}. {paper.journal}. "
            f"{paper.publication_year}; doi:{paper.doi.value}"
        )
