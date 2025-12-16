# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""AI analyzer port interface for theme extraction and synthesis.

This port defines the contract for AI-powered analysis services that can
extract themes from papers and generate research synthesis.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from lit_review.domain.entities.paper import Paper


@dataclass(frozen=True)
class ThemeHierarchy:
    """Hierarchical representation of research themes.

    Attributes:
        themes: Dictionary mapping theme names to lists of related keywords.
        relationships: Dictionary mapping themes to related themes with similarity scores.
        summary: High-level summary of the thematic structure.
    """

    themes: dict[str, list[str]]
    relationships: dict[str, dict[str, float]]
    summary: str


class AIAnalyzer(ABC):
    """Abstract interface for AI-powered analysis services.

    Implementations of this interface can use various AI services (Claude, GPT, etc.)
    or fall back to keyword-based analysis when AI is unavailable.
    """

    @abstractmethod
    def extract_themes(
        self,
        papers: list[Paper],
        max_themes: int = 10,
    ) -> ThemeHierarchy:
        """Extract hierarchical themes from a collection of papers.

        Args:
            papers: List of papers to analyze.
            max_themes: Maximum number of themes to extract.

        Returns:
            ThemeHierarchy containing themes, relationships, and summary.

        Raises:
            ValueError: If papers list is empty or max_themes is invalid.
        """

    @abstractmethod
    def generate_synthesis(
        self,
        papers: list[Paper],
        themes: ThemeHierarchy,
        research_question: str,
    ) -> str:
        """Generate narrative synthesis from papers and themes.

        Args:
            papers: List of papers to synthesize.
            themes: ThemeHierarchy from extract_themes.
            research_question: Research question guiding the synthesis.

        Returns:
            Markdown-formatted synthesis with proper citations.

        Raises:
            ValueError: If inputs are invalid.
        """
