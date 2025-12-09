"""Tests for Keywords value object."""

import pytest

from lit_review.domain.exceptions import ValidationError
from lit_review.domain.values.keywords import Keywords


class TestKeywordsCreation:
    """Tests for Keywords creation and validation."""

    def test_valid_keywords_single_word(self) -> None:
        """Keywords with single word is accepted."""
        keywords = Keywords(["machine"])
        assert keywords.terms == ("machine",)

    def test_valid_keywords_multiple_words(self) -> None:
        """Keywords with multiple words is accepted."""
        keywords = Keywords(["machine learning", "healthcare", "diagnosis"])
        assert keywords.terms == ("machine learning", "healthcare", "diagnosis")

    def test_keywords_lowercase_normalization(self) -> None:
        """Keywords are normalized to lowercase."""
        keywords = Keywords(["Machine Learning", "HEALTHCARE", "DiAgNoSiS"])
        assert keywords.terms == ("machine learning", "healthcare", "diagnosis")

    def test_keywords_strip_whitespace(self) -> None:
        """Leading/trailing whitespace is stripped from keywords."""
        keywords = Keywords(["  machine learning  ", " healthcare ", "diagnosis"])
        assert keywords.terms == ("machine learning", "healthcare", "diagnosis")

    def test_keywords_deduplication(self) -> None:
        """Duplicate keywords are removed."""
        keywords = Keywords(["machine", "learning", "machine", "learning"])
        assert keywords.terms == ("machine", "learning")
        assert len(keywords.terms) == 2

    def test_keywords_deduplication_case_insensitive(self) -> None:
        """Case-insensitive deduplication works."""
        keywords = Keywords(["Machine", "MACHINE", "machine"])
        assert keywords.terms == ("machine",)
        assert len(keywords.terms) == 1

    def test_keywords_order_preserved_after_deduplication(self) -> None:
        """Order of first occurrence is preserved after deduplication."""
        keywords = Keywords(["zebra", "apple", "zebra", "banana", "apple"])
        assert keywords.terms == ("zebra", "apple", "banana")

    def test_empty_keywords_raises_error(self) -> None:
        """Empty keywords list raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Keywords([])
        assert "cannot be empty" in str(exc_info.value.message)

    def test_keywords_with_empty_strings_raises_error(self) -> None:
        """Keywords containing empty strings raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Keywords(["machine", "", "learning"])
        assert "cannot be empty" in str(exc_info.value.message)

    def test_keywords_with_only_whitespace_raises_error(self) -> None:
        """Keywords with only whitespace raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Keywords(["machine", "   ", "learning"])
        assert "cannot be empty" in str(exc_info.value.message)

    def test_keywords_all_empty_after_strip_raises_error(self) -> None:
        """All keywords empty after stripping raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Keywords(["  ", "   ", "    "])
        assert "cannot be empty" in str(exc_info.value.message)


class TestKeywordsImmutability:
    """Tests for Keywords immutability."""

    def test_keywords_is_immutable(self) -> None:
        """Keywords terms cannot be modified after creation."""
        keywords = Keywords(["machine", "learning"])
        with pytest.raises(AttributeError):
            keywords.terms = ["new", "terms"]  # type: ignore[misc]

    def test_keywords_terms_list_is_immutable(self) -> None:
        """Keywords terms list cannot be modified."""
        keywords = Keywords(["machine", "learning"])
        # The tuple is immutable, so this should raise an error
        with pytest.raises(AttributeError):
            keywords.terms.append("new")  # type: ignore[attr-defined]


class TestKeywordsEquality:
    """Tests for Keywords equality and hashing."""

    def test_equal_keywords_are_equal(self) -> None:
        """Two Keywords with same terms are equal."""
        keywords1 = Keywords(["machine", "learning"])
        keywords2 = Keywords(["machine", "learning"])
        assert keywords1 == keywords2

    def test_equal_keywords_different_case_are_equal(self) -> None:
        """Keywords are equal regardless of case."""
        keywords1 = Keywords(["Machine", "Learning"])
        keywords2 = Keywords(["machine", "learning"])
        assert keywords1 == keywords2

    def test_equal_keywords_different_order_are_not_equal(self) -> None:
        """Keywords with same terms but different order are not equal."""
        keywords1 = Keywords(["machine", "learning"])
        keywords2 = Keywords(["learning", "machine"])
        assert keywords1 != keywords2

    def test_different_keywords_are_not_equal(self) -> None:
        """Two Keywords with different terms are not equal."""
        keywords1 = Keywords(["machine", "learning"])
        keywords2 = Keywords(["deep", "learning"])
        assert keywords1 != keywords2

    def test_keywords_hash_equality(self) -> None:
        """Equal Keywords have equal hashes."""
        keywords1 = Keywords(["machine", "learning"])
        keywords2 = Keywords(["machine", "learning"])
        assert hash(keywords1) == hash(keywords2)

    def test_keywords_can_be_used_in_set(self) -> None:
        """Keywords can be used in sets for deduplication."""
        keywords1 = Keywords(["machine", "learning"])
        keywords2 = Keywords(["machine", "learning"])
        keywords3 = Keywords(["deep", "learning"])
        keyword_set = {keywords1, keywords2, keywords3}
        assert len(keyword_set) == 2


class TestKeywordsMethods:
    """Tests for Keywords methods."""

    def test_str_returns_comma_separated(self) -> None:
        """str() returns comma-separated keywords."""
        keywords = Keywords(["machine learning", "healthcare", "diagnosis"])
        assert str(keywords) == "machine learning, healthcare, diagnosis"

    def test_str_single_keyword(self) -> None:
        """str() works with single keyword."""
        keywords = Keywords(["machine"])
        assert str(keywords) == "machine"

    def test_len_returns_count(self) -> None:
        """len() returns number of keywords."""
        keywords = Keywords(["machine", "learning", "healthcare"])
        assert len(keywords) == 3

    def test_contains_finds_keyword(self) -> None:
        """'in' operator finds keyword in Keywords."""
        keywords = Keywords(["machine", "learning", "healthcare"])
        assert "machine" in keywords
        assert "learning" in keywords

    def test_contains_case_insensitive(self) -> None:
        """'in' operator is case-insensitive."""
        keywords = Keywords(["Machine Learning"])
        assert "machine learning" in keywords
        assert "MACHINE LEARNING" in keywords

    def test_contains_not_found(self) -> None:
        """'in' operator returns False for missing keyword."""
        keywords = Keywords(["machine", "learning"])
        assert "deep" not in keywords

    def test_iter_returns_iterator(self) -> None:
        """Keywords is iterable."""
        keywords = Keywords(["machine", "learning", "healthcare"])
        terms_list = list(keywords)
        assert terms_list == ["machine", "learning", "healthcare"]

    def test_getitem_by_index(self) -> None:
        """Keywords supports indexing."""
        keywords = Keywords(["machine", "learning", "healthcare"])
        assert keywords[0] == "machine"
        assert keywords[1] == "learning"
        assert keywords[2] == "healthcare"
        assert keywords[-1] == "healthcare"

    def test_to_list_returns_copy(self) -> None:
        """to_list() returns a mutable copy of terms."""
        keywords = Keywords(["machine", "learning"])
        terms = keywords.to_list()
        assert terms == ["machine", "learning"]
        # Verify it's a copy by modifying it
        terms.append("new")
        assert "new" not in keywords


class TestKeywordsEdgeCases:
    """Tests for Keywords edge cases."""

    def test_keywords_with_special_characters(self) -> None:
        """Keywords with special characters are preserved."""
        keywords = Keywords(["C++", "machine-learning", "AI/ML"])
        assert keywords.terms == ("c++", "machine-learning", "ai/ml")

    def test_keywords_with_unicode(self) -> None:
        """Keywords with unicode characters are supported."""
        keywords = Keywords(["Künstliche Intelligenz", "Машинное обучение"])
        assert len(keywords) == 2
        assert "künstliche intelligenz" in keywords

    def test_keywords_dedupe_with_mixed_case_and_whitespace(self) -> None:
        """Complex deduplication scenario works correctly."""
        keywords = Keywords(
            [
                "Machine Learning",
                "  machine learning  ",
                "MACHINE LEARNING",
                "machine learning",
            ]
        )
        assert keywords.terms == ("machine learning",)
        assert len(keywords) == 1
