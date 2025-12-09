"""Claude AI analyzer with graceful fallback to keyword-based analysis.

Implements the AIAnalyzer port using Anthropic's Claude API with
automatic fallback to simpler methods when API is unavailable.
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from lit_review.application.ports.ai_analyzer import AIAnalyzer, ThemeHierarchy
from lit_review.domain.entities.paper import Paper


class ClaudeAnalyzer(AIAnalyzer):
    """Claude-powered analyzer with keyword fallback.

    Uses Claude API for theme extraction and synthesis when available.
    Falls back to keyword-based analysis when API is unavailable or
    API key is not provided.

    Attributes:
        api_key: Anthropic API key (from ANTHROPIC_API_KEY env var).
        model: Claude model to use (default: claude-sonnet-4-5-20250929).
        cache_dir: Directory for caching responses (7-day TTL).
        cache_ttl_days: Cache time-to-live in days (default: 7).
        use_api: Whether to use Claude API (False for fallback mode).

    Example:
        >>> analyzer = ClaudeAnalyzer()
        >>> themes = analyzer.extract_themes(papers)
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-sonnet-4-5-20250929",
        cache_dir: Path | None = None,
        cache_ttl_days: int = 7,
    ) -> None:
        """Initialize Claude analyzer.

        Args:
            api_key: Anthropic API key (uses ANTHROPIC_API_KEY env if not provided).
            model: Claude model identifier.
            cache_dir: Cache directory (default: ~/.lit_review/cache).
            cache_ttl_days: Cache TTL in days.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model
        self.cache_ttl_days = cache_ttl_days

        # Set up cache directory
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path.home() / ".lit_review" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Determine if we can use API
        self.use_api = self.api_key is not None

        # Import anthropic only if API key available
        self._client = None
        if self.use_api:
            try:
                from anthropic import Anthropic  # type: ignore[import-not-found]

                self._client = Anthropic(api_key=self.api_key)
            except ImportError:
                self.use_api = False

    def extract_themes(
        self,
        papers: list[Paper],
        max_themes: int = 10,
    ) -> ThemeHierarchy:
        """Extract hierarchical themes from papers.

        Args:
            papers: List of papers to analyze.
            max_themes: Maximum number of themes to extract.

        Returns:
            ThemeHierarchy containing themes, relationships, and summary.

        Raises:
            ValueError: If papers list is empty or max_themes is invalid.
        """
        if not papers:
            raise ValueError("Papers list cannot be empty")

        if max_themes < 1:
            raise ValueError("max_themes must be at least 1")

        # Try Claude API first, fall back to keyword extraction
        if self.use_api and self._client:
            try:
                return self._extract_themes_with_claude(papers, max_themes)
            except Exception:
                # Fall back to keyword method
                pass

        return self._extract_themes_keyword_based(papers, max_themes)

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
        if not papers:
            raise ValueError("Papers list cannot be empty")

        if not research_question:
            raise ValueError("Research question cannot be empty")

        # Try Claude API first, fall back to simple synthesis
        if self.use_api and self._client:
            try:
                return self._generate_synthesis_with_claude(papers, themes, research_question)
            except Exception:
                # Fall back to simple method
                pass

        return self._generate_synthesis_simple(papers, themes, research_question)

    def _extract_themes_with_claude(self, papers: list[Paper], max_themes: int) -> ThemeHierarchy:
        """Extract themes using Claude API.

        Args:
            papers: List of papers.
            max_themes: Maximum themes.

        Returns:
            ThemeHierarchy from Claude analysis.
        """
        # Check cache first
        cache_key = self._get_cache_key("themes", papers, max_themes)
        cached = self._load_from_cache(cache_key)
        if cached:
            return ThemeHierarchy(**cached)

        # Prepare prompt
        papers_text = self._papers_to_text(papers)
        prompt = f"""Analyze these {len(papers)} academic papers and extract up to {max_themes} major themes.

For each theme, provide:
1. Theme name
2. Related keywords
3. Relationships to other themes (with similarity scores 0-1)

Papers:
{papers_text}

Return JSON with this structure:
{{
    "themes": {{"Theme Name": ["keyword1", "keyword2", ...], ...}},
    "relationships": {{"Theme1": {{"Theme2": 0.8, ...}}, ...}},
    "summary": "High-level summary of thematic structure"
}}
"""

        # Call Claude API
        if not self._client:
            raise RuntimeError("Claude API client not initialized")

        response = self._client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse response
        content = response.content[0].text
        data = json.loads(content)

        result = ThemeHierarchy(
            themes=data["themes"],
            relationships=data["relationships"],
            summary=data["summary"],
        )

        # Cache result
        self._save_to_cache(
            cache_key,
            {
                "themes": result.themes,
                "relationships": result.relationships,
                "summary": result.summary,
            },
        )

        return result

    def _generate_synthesis_with_claude(
        self,
        papers: list[Paper],
        themes: ThemeHierarchy,
        research_question: str,
    ) -> str:
        """Generate synthesis using Claude API.

        Args:
            papers: List of papers.
            themes: ThemeHierarchy.
            research_question: Research question.

        Returns:
            Markdown synthesis.
        """
        # Check cache
        cache_key = self._get_cache_key("synthesis", papers, research_question)
        cached = self._load_from_cache(cache_key)
        if cached:
            return str(cached)

        papers_text = self._papers_to_text(papers)
        themes_text = json.dumps(themes.themes, indent=2)

        prompt = f"""Generate a narrative synthesis for this systematic review.

Research Question: {research_question}

Identified Themes:
{themes_text}

Papers:
{papers_text}

Generate a markdown-formatted synthesis that:
1. Addresses the research question
2. Organizes findings by themes
3. Uses proper citations [Author et al., Year]
4. Synthesizes across studies rather than summarizing each
5. Identifies patterns, gaps, and contradictions
"""

        if not self._client:
            raise RuntimeError("Claude API client not initialized")

        response = self._client.messages.create(
            model=self.model,
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}],
        )

        synthesis: str = str(response.content[0].text)

        # Cache result
        self._save_to_cache(cache_key, synthesis)

        return synthesis

    def _extract_themes_keyword_based(self, papers: list[Paper], max_themes: int) -> ThemeHierarchy:
        """Fallback: Extract themes using keyword frequency.

        Args:
            papers: List of papers.
            max_themes: Maximum themes.

        Returns:
            ThemeHierarchy from keyword analysis.
        """
        from collections import Counter

        # Collect all keywords
        all_keywords: list[str] = []
        for paper in papers:
            all_keywords.extend(paper.keywords)

        # Count frequency
        keyword_counts = Counter(all_keywords)
        top_keywords = keyword_counts.most_common(max_themes)

        # Create themes from top keywords
        themes: dict[str, list[str]] = {}
        for keyword, _ in top_keywords:
            # Group related keywords (simple approach: same keyword is the theme)
            related = [
                kw for kw, _ in keyword_counts.most_common(20) if keyword.lower() in kw.lower()
            ]
            themes[keyword] = related[:5]

        # Simple relationships (keywords that co-occur)
        relationships: dict[str, dict[str, float]] = {}
        for theme1 in themes:
            relationships[theme1] = {}
            for theme2 in themes:
                if theme1 != theme2:
                    # Calculate co-occurrence
                    cooccur = sum(
                        1 for p in papers if theme1 in p.keywords and theme2 in p.keywords
                    )
                    if cooccur > 0:
                        relationships[theme1][theme2] = min(cooccur / len(papers), 1.0)

        summary = (
            f"Identified {len(themes)} themes from {len(papers)} papers using keyword analysis."
        )

        return ThemeHierarchy(
            themes=themes,
            relationships=relationships,
            summary=summary,
        )

    def _generate_synthesis_simple(
        self,
        papers: list[Paper],
        themes: ThemeHierarchy,
        research_question: str,
    ) -> str:
        """Fallback: Generate simple synthesis.

        Args:
            papers: List of papers.
            themes: ThemeHierarchy.
            research_question: Research question.

        Returns:
            Simple markdown synthesis.
        """
        synthesis = f"# Synthesis\n\n## Research Question\n\n{research_question}\n\n"
        synthesis += f"## Overview\n\n{themes.summary}\n\n"
        synthesis += f"This synthesis is based on {len(papers)} papers.\n\n"

        synthesis += "## Themes\n\n"
        for theme, keywords in themes.themes.items():
            synthesis += f"### {theme}\n\n"
            synthesis += f"Keywords: {', '.join(keywords)}\n\n"

            # Find papers related to this theme
            related_papers = [p for p in papers if any(kw in p.keywords for kw in keywords)]
            if related_papers:
                synthesis += "Relevant papers:\n"
                for paper in related_papers[:5]:  # Limit to 5
                    citation_key = paper.get_citation_key()
                    synthesis += f"- {paper.title} [{citation_key}]\n"
            synthesis += "\n"

        return synthesis

    def _papers_to_text(self, papers: list[Paper]) -> str:
        """Convert papers to text for prompts.

        Args:
            papers: List of papers.

        Returns:
            Formatted text string.
        """
        text = ""
        for i, paper in enumerate(papers[:50], 1):  # Limit to 50 papers
            authors_str = ", ".join(a.last_name for a in paper.authors[:3])
            if len(paper.authors) > 3:
                authors_str += " et al."

            text += f"{i}. {authors_str} ({paper.publication_year}). {paper.title}\n"
            if paper.abstract:
                text += f"   Abstract: {paper.abstract[:500]}...\n"
            if paper.keywords:
                text += f"   Keywords: {', '.join(paper.keywords[:10])}\n"
            text += "\n"

        return text

    def _get_cache_key(self, operation: str, papers: list[Paper], *args: Any) -> str:
        """Generate cache key for operation.

        Args:
            operation: Operation type (themes/synthesis).
            papers: List of papers.
            args: Additional args to include in hash.

        Returns:
            Cache key string.
        """
        # Create hash from paper DOIs and args
        hash_input = operation + "||"
        hash_input += "||".join(p.doi.value for p in papers)
        hash_input += "||".join(str(arg) for arg in args)

        return hashlib.sha256(hash_input.encode()).hexdigest()

    def _load_from_cache(self, cache_key: str) -> Any:
        """Load result from cache if not expired.

        Args:
            cache_key: Cache key.

        Returns:
            Cached result or None if not found/expired.
        """
        cache_file = self.cache_dir / f"{cache_key}.json"

        if not cache_file.exists():
            return None

        # Check if expired
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        if datetime.now() - mtime > timedelta(days=self.cache_ttl_days):
            cache_file.unlink()
            return None

        try:
            return json.loads(cache_file.read_text())
        except Exception:
            return None

    def _save_to_cache(self, cache_key: str, data: Any) -> None:
        """Save result to cache.

        Args:
            cache_key: Cache key.
            data: Data to cache (must be JSON serializable).
        """
        cache_file = self.cache_dir / f"{cache_key}.json"

        try:
            cache_file.write_text(json.dumps(data, indent=2))
        except Exception:
            # Silently fail on cache write errors
            pass
