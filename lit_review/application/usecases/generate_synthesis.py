"""Generate synthesis use case for creating narrative literature reviews.

This use case generates structured synthesis from papers and themes,
with optional AI enhancement.
"""

from dataclasses import dataclass

from lit_review.application.ports.ai_analyzer import AIAnalyzer, ThemeHierarchy
from lit_review.domain.entities.paper import Paper


@dataclass
class GenerateSynthesisUseCase:
    """Use case for generating narrative synthesis from papers and themes.

    Creates structured synthesis with introduction, themes, gaps, and conclusions.
    Uses keyword-based approach by default, with optional AI enhancement.

    Attributes:
        ai_analyzer: Optional AI analyzer for enhanced synthesis.
    """

    ai_analyzer: AIAnalyzer | None = None

    def execute(
        self,
        papers: list[Paper],
        themes: ThemeHierarchy,
        research_question: str,
        use_ai: bool = False,
    ) -> str:
        """Generate narrative synthesis from papers and themes.

        Args:
            papers: List of papers to synthesize (should be included papers).
            themes: ThemeHierarchy from AnalyzeThemesUseCase.
            research_question: Research question guiding the synthesis.
            use_ai: If True and ai_analyzer available, use AI enhancement.

        Returns:
            Markdown-formatted synthesis with proper citations.

        Raises:
            ValueError: If inputs are invalid.
        """
        if not papers:
            raise ValueError("Cannot generate synthesis from empty paper list")

        if not research_question.strip():
            raise ValueError("Research question cannot be empty")

        # Try AI synthesis if requested and available
        if use_ai and self.ai_analyzer is not None:
            try:
                return self.ai_analyzer.generate_synthesis(papers, themes, research_question)
            except Exception:
                # Fall back to keyword-based synthesis on error
                pass

        # Keyword-based synthesis
        return self._generate_keyword_synthesis(papers, themes, research_question)

    def _generate_keyword_synthesis(
        self,
        papers: list[Paper],
        themes: ThemeHierarchy,
        research_question: str,
    ) -> str:
        """Generate synthesis using keyword-based approach.

        Args:
            papers: Papers to synthesize.
            themes: Theme hierarchy.
            research_question: Research question.

        Returns:
            Markdown-formatted synthesis.
        """
        # Build synthesis sections
        intro = self._generate_introduction(papers, research_question)
        theme_sections = self._generate_theme_sections(papers, themes)
        gaps = self._identify_research_gaps(papers, themes)
        conclusion = self._generate_conclusion(papers, themes, research_question)

        # Combine into full synthesis
        synthesis = f"""# Literature Review Synthesis

{intro}

## Thematic Analysis

{theme_sections}

## Research Gaps

{gaps}

## Conclusions

{conclusion}

## References

{self._generate_references(papers)}
"""

        return synthesis

    def _generate_introduction(self, papers: list[Paper], research_question: str) -> str:
        """Generate introduction section.

        Args:
            papers: Papers in the review.
            research_question: Research question.

        Returns:
            Introduction text.
        """
        num_papers = len(papers)
        year_range = self._get_year_range(papers)

        intro = f"""This systematic literature review examines the research question: "{research_question}"

The review synthesizes findings from {num_papers} peer-reviewed papers published between \
{year_range}. The analysis identifies major themes, methodological approaches, and research gaps \
in the current literature."""

        return intro

    def _generate_theme_sections(self, papers: list[Paper], themes: ThemeHierarchy) -> str:
        """Generate sections for each theme.

        Args:
            papers: Papers in the review.
            themes: Theme hierarchy.

        Returns:
            Theme sections text.
        """
        sections = []

        for theme_name, keywords in themes.themes.items():
            # Find papers relevant to this theme
            relevant_papers = self._find_papers_for_theme(papers, keywords)

            if relevant_papers:
                section = self._create_theme_section(theme_name, keywords, relevant_papers)
                sections.append(section)

        return "\n\n".join(sections)

    def _create_theme_section(
        self,
        theme_name: str,
        keywords: list[str],
        papers: list[Paper],
    ) -> str:
        """Create a single theme section.

        Args:
            theme_name: Name of the theme.
            keywords: Keywords defining the theme.
            papers: Papers relevant to this theme.

        Returns:
            Theme section text.
        """
        keyword_list = ", ".join(keywords[:5])
        citations = self._format_citations(papers[:10])  # Limit citations

        section = f"""### {theme_name}

Key concepts: {keyword_list}

{len(papers)} papers address this theme, including {citations}. \
These studies explore {keywords[0]} and related concepts, \
contributing to our understanding of the research question."""

        return section

    def _identify_research_gaps(self, papers: list[Paper], themes: ThemeHierarchy) -> str:
        """Identify research gaps based on themes and papers.

        Args:
            papers: Papers in the review.
            themes: Theme hierarchy.

        Returns:
            Research gaps text.
        """
        gaps = []

        # Look for weak theme relationships (potential gaps)
        weak_connections = []
        for theme_name, relationships in themes.relationships.items():
            if not relationships or all(score < 0.2 for score in relationships.values()):
                weak_connections.append(theme_name)

        if weak_connections:
            gaps.append(f"Limited integration between themes: {', '.join(weak_connections[:3])}")

        # Check for temporal gaps
        recent_papers = [p for p in papers if p.publication_year >= 2020]
        if len(recent_papers) < len(papers) * 0.3:
            gaps.append(
                "Limited recent research (past 3 years), suggesting need for updated studies"
            )

        # Default gap if none identified
        if not gaps:
            gaps.append(
                "Further research needed to validate and extend findings across different contexts"
            )

        return "\n\n".join(f"- {gap}" for gap in gaps)

    def _generate_conclusion(
        self,
        papers: list[Paper],
        themes: ThemeHierarchy,
        research_question: str,
    ) -> str:
        """Generate conclusion section.

        Args:
            papers: Papers in the review.
            themes: Theme hierarchy.
            research_question: Research question.

        Returns:
            Conclusion text.
        """
        num_themes = len(themes.themes)

        conclusion = f"""This systematic review of {len(papers)} papers identified {num_themes} major \
themes related to the research question: "{research_question}"

The synthesis reveals a diverse body of literature with varying methodological approaches \
and findings. Future research should address the identified gaps and build upon the \
established theoretical foundations."""

        return conclusion

    def _generate_references(self, papers: list[Paper]) -> str:
        """Generate reference list.

        Args:
            papers: Papers to reference.

        Returns:
            Reference list text.
        """
        references = []

        for i, paper in enumerate(papers, 1):
            authors = paper.get_citation_key().split("EtAl")[0].split("And")[0]
            ref = (
                f"{i}. {authors} et al. ({paper.publication_year}). {paper.title}. "
                f"*{paper.journal}*. DOI: {paper.doi.value}"
            )
            references.append(ref)

        return "\n\n".join(references)

    def _find_papers_for_theme(self, papers: list[Paper], keywords: list[str]) -> list[Paper]:
        """Find papers relevant to a theme based on keywords.

        Args:
            papers: All papers.
            keywords: Theme keywords.

        Returns:
            Papers relevant to the theme.
        """
        relevant = []

        for paper in papers:
            # Check if any keyword appears in title or abstract
            text = f"{paper.title} {paper.abstract or ''}".lower()
            if any(keyword.lower() in text for keyword in keywords):
                relevant.append(paper)

        return relevant

    def _format_citations(self, papers: list[Paper]) -> str:
        """Format paper citations for inline use.

        Args:
            papers: Papers to cite.

        Returns:
            Formatted citations string.
        """
        if not papers:
            return ""

        if len(papers) == 1:
            return f"[{papers[0].get_citation_key()}]"

        if len(papers) == 2:
            return f"[{papers[0].get_citation_key()}; {papers[1].get_citation_key()}]"

        # More than 2 papers
        citations = [p.get_citation_key() for p in papers[:3]]
        if len(papers) > 3:
            return f"[{'; '.join(citations)}; and others]"
        return f"[{'; '.join(citations)}]"

    def _get_year_range(self, papers: list[Paper]) -> str:
        """Get the year range of papers.

        Args:
            papers: Papers to analyze.

        Returns:
            Year range string (e.g., "2018-2023").
        """
        if not papers:
            return "N/A"

        years = [p.publication_year for p in papers]
        min_year = min(years)
        max_year = max(years)

        if min_year == max_year:
            return str(min_year)

        return f"{min_year}-{max_year}"
