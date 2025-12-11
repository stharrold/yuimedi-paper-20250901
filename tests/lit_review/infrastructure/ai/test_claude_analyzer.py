"""Tests for ClaudeAnalyzer."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from lit_review.domain.entities.paper import Paper
from lit_review.domain.values.author import Author
from lit_review.domain.values.doi import DOI
from lit_review.infrastructure.ai.claude_analyzer import ClaudeAnalyzer


@pytest.fixture
def sample_papers() -> list[Paper]:
    """Create sample papers for testing."""
    return [
        Paper(
            doi=DOI("10.1234/ml1"),
            title="Machine Learning in Healthcare",
            authors=[Author("Smith", "John", "J.")],
            publication_year=2024,
            journal="AI Journal",
            abstract="This paper explores machine learning applications in healthcare.",
            keywords=["machine learning", "healthcare", "diagnosis"],
        ),
        Paper(
            doi=DOI("10.1234/ml2"),
            title="Deep Learning for Medical Imaging",
            authors=[Author("Jones", "Jane", "J.")],
            publication_year=2023,
            journal="Medical AI",
            abstract="Deep learning methods for medical image analysis.",
            keywords=["deep learning", "medical imaging", "machine learning"],
        ),
        Paper(
            doi=DOI("10.1234/ml3"),
            title="Clinical Decision Support Systems",
            authors=[Author("Wilson", "Bob", "B.")],
            publication_year=2024,
            journal="Healthcare Tech",
            abstract="AI-powered clinical decision support.",
            keywords=["clinical decision support", "AI", "healthcare"],
        ),
    ]


@pytest.fixture
def temp_cache_dir() -> Path:
    """Create temporary cache directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.mark.integration
class TestClaudeAnalyzerInit:
    """Tests for ClaudeAnalyzer initialization (integration - optional dependencies)."""

    def test_init_without_api_key_uses_fallback(self, temp_cache_dir: Path) -> None:
        """__init__ sets use_api=False when no API key provided."""
        with patch.dict("os.environ", {}, clear=True):
            analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)
            assert analyzer.use_api is False

    def test_init_with_api_key_enables_api(self, temp_cache_dir: Path) -> None:
        """__init__ sets use_api=True when API key provided."""
        with patch("lit_review.infrastructure.ai.claude_analyzer.Anthropic"):
            analyzer = ClaudeAnalyzer(api_key="test_key", cache_dir=temp_cache_dir)
            assert analyzer.use_api is True

    def test_init_creates_cache_directory(self, temp_cache_dir: Path) -> None:
        """__init__ creates cache directory."""
        cache_dir = temp_cache_dir / "custom_cache"
        analyzer = ClaudeAnalyzer(cache_dir=cache_dir)

        assert cache_dir.exists()
        assert analyzer.cache_dir == cache_dir

    def test_init_uses_default_model(self, temp_cache_dir: Path) -> None:
        """__init__ sets default model."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)
        assert analyzer.model == "claude-sonnet-4-5-20250929"

    def test_init_accepts_custom_model(self, temp_cache_dir: Path) -> None:
        """__init__ accepts custom model."""
        analyzer = ClaudeAnalyzer(model="claude-opus-4", cache_dir=temp_cache_dir)
        assert analyzer.model == "claude-opus-4"


class TestClaudeAnalyzerFallback:
    """Tests for fallback keyword-based analysis."""

    def test_extract_themes_fallback_returns_themes(
        self, temp_cache_dir: Path, sample_papers: list[Paper]
    ) -> None:
        """extract_themes uses keyword fallback when API unavailable."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)  # No API key

        themes = analyzer.extract_themes(sample_papers, max_themes=5)

        assert len(themes.themes) > 0
        assert "machine learning" in themes.themes or "healthcare" in themes.themes
        assert themes.summary
        assert isinstance(themes.relationships, dict)

    def test_extract_themes_fallback_respects_max_themes(
        self, temp_cache_dir: Path, sample_papers: list[Paper]
    ) -> None:
        """extract_themes respects max_themes in fallback mode."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)

        themes = analyzer.extract_themes(sample_papers, max_themes=2)

        assert len(themes.themes) <= 2

    def test_extract_themes_raises_error_for_empty_list(self, temp_cache_dir: Path) -> None:
        """extract_themes raises ValueError for empty papers list."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)

        with pytest.raises(ValueError) as exc_info:
            analyzer.extract_themes([], max_themes=5)

        assert "cannot be empty" in str(exc_info.value)

    def test_extract_themes_raises_error_for_invalid_max(
        self, temp_cache_dir: Path, sample_papers: list[Paper]
    ) -> None:
        """extract_themes raises ValueError for invalid max_themes."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)

        with pytest.raises(ValueError) as exc_info:
            analyzer.extract_themes(sample_papers, max_themes=0)

        assert "at least 1" in str(exc_info.value)

    def test_generate_synthesis_fallback_returns_markdown(
        self, temp_cache_dir: Path, sample_papers: list[Paper]
    ) -> None:
        """generate_synthesis uses simple fallback when API unavailable."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)
        themes = analyzer.extract_themes(sample_papers, max_themes=3)

        synthesis = analyzer.generate_synthesis(
            sample_papers,
            themes,
            "What is the impact of AI in healthcare?",
        )

        assert "# Synthesis" in synthesis
        assert "Research Question" in synthesis
        assert "AI in healthcare" in synthesis

    def test_generate_synthesis_raises_error_for_empty_papers(self, temp_cache_dir: Path) -> None:
        """generate_synthesis raises ValueError for empty papers."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)

        from lit_review.application.ports.ai_analyzer import ThemeHierarchy

        themes = ThemeHierarchy(themes={}, relationships={}, summary="")

        with pytest.raises(ValueError) as exc_info:
            analyzer.generate_synthesis([], themes, "Question?")

        assert "cannot be empty" in str(exc_info.value)

    def test_generate_synthesis_raises_error_for_empty_question(
        self, temp_cache_dir: Path, sample_papers: list[Paper]
    ) -> None:
        """generate_synthesis raises ValueError for empty question."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)

        from lit_review.application.ports.ai_analyzer import ThemeHierarchy

        themes = ThemeHierarchy(themes={}, relationships={}, summary="")

        with pytest.raises(ValueError) as exc_info:
            analyzer.generate_synthesis(sample_papers, themes, "")

        assert "cannot be empty" in str(exc_info.value)


class TestClaudeAnalyzerCaching:
    """Tests for response caching."""

    def test_cache_key_generation_deterministic(
        self, temp_cache_dir: Path, sample_papers: list[Paper]
    ) -> None:
        """_get_cache_key generates same key for same inputs."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)

        key1 = analyzer._get_cache_key("themes", sample_papers, 5)
        key2 = analyzer._get_cache_key("themes", sample_papers, 5)

        assert key1 == key2

    def test_cache_key_differs_for_different_inputs(
        self, temp_cache_dir: Path, sample_papers: list[Paper]
    ) -> None:
        """_get_cache_key generates different keys for different inputs."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)

        key1 = analyzer._get_cache_key("themes", sample_papers, 5)
        key2 = analyzer._get_cache_key("themes", sample_papers, 10)

        assert key1 != key2

    def test_save_and_load_cache(self, temp_cache_dir: Path) -> None:
        """_save_to_cache and _load_from_cache work correctly."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)

        test_data = {"result": "test", "count": 42}
        cache_key = "test_key_123"

        analyzer._save_to_cache(cache_key, test_data)
        loaded = analyzer._load_from_cache(cache_key)

        assert loaded == test_data

    def test_load_cache_returns_none_for_missing(self, temp_cache_dir: Path) -> None:
        """_load_from_cache returns None for missing cache."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)

        loaded = analyzer._load_from_cache("nonexistent_key")

        assert loaded is None

    def test_cache_expires_after_ttl(self, temp_cache_dir: Path) -> None:
        """Cache expires after TTL days."""
        from datetime import datetime, timedelta

        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir, cache_ttl_days=7)

        test_data = {"result": "old"}
        cache_key = "expire_test"

        analyzer._save_to_cache(cache_key, test_data)
        cache_file = temp_cache_dir / f"{cache_key}.json"

        # Set mtime to 8 days ago
        old_time = (datetime.now() - timedelta(days=8)).timestamp()
        import os

        os.utime(cache_file, (old_time, old_time))

        # Should return None (expired)
        loaded = analyzer._load_from_cache(cache_key)
        assert loaded is None

        # Cache file should be deleted
        assert not cache_file.exists()


class TestClaudeAnalyzerHelpers:
    """Tests for helper methods."""

    def test_papers_to_text_formats_correctly(
        self, temp_cache_dir: Path, sample_papers: list[Paper]
    ) -> None:
        """_papers_to_text formats papers as text."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)

        text = analyzer._papers_to_text(sample_papers)

        assert "Smith (2024)" in text
        assert "Machine Learning in Healthcare" in text
        assert "Keywords:" in text

    def test_papers_to_text_limits_to_50(self, temp_cache_dir: Path) -> None:
        """_papers_to_text limits to 50 papers."""
        analyzer = ClaudeAnalyzer(cache_dir=temp_cache_dir)

        # Create 60 papers
        many_papers = [
            Paper(
                doi=DOI(f"10.1234/test{i}"),
                title=f"Paper {i}",
                authors=[Author("Author", f"Name{i}", "A.")],
                publication_year=2024,
                journal="Journal",
            )
            for i in range(60)
        ]

        text = analyzer._papers_to_text(many_papers)

        # Should contain only first 50
        assert "Paper 0" in text
        assert "Paper 49" in text
        assert "Paper 50" not in text


@pytest.mark.integration
class TestClaudeAnalyzerIntegration:
    """Integration tests for Claude API (requires API key)."""

    def test_real_claude_theme_extraction(
        self, temp_cache_dir: Path, sample_papers: list[Paper]
    ) -> None:
        """extract_themes uses real Claude API (integration test)."""
        import os

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            pytest.skip("ANTHROPIC_API_KEY not set")

        analyzer = ClaudeAnalyzer(api_key=api_key, cache_dir=temp_cache_dir)
        themes = analyzer.extract_themes(sample_papers, max_themes=3)

        assert len(themes.themes) > 0
        assert themes.summary
        assert isinstance(themes.relationships, dict)

    def test_real_claude_synthesis(self, temp_cache_dir: Path, sample_papers: list[Paper]) -> None:
        """generate_synthesis uses real Claude API (integration test)."""
        import os

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            pytest.skip("ANTHROPIC_API_KEY not set")

        analyzer = ClaudeAnalyzer(api_key=api_key, cache_dir=temp_cache_dir)
        themes = analyzer.extract_themes(sample_papers, max_themes=3)

        synthesis = analyzer.generate_synthesis(
            sample_papers,
            themes,
            "What role does AI play in healthcare?",
        )

        assert len(synthesis) > 100
        assert "#" in synthesis  # Markdown headers
