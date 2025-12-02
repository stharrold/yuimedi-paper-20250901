"""Tests for DOI value object."""

import pytest

from lit_review.domain.exceptions import ValidationError
from lit_review.domain.values.doi import DOI


class TestDOICreation:
    """Tests for DOI creation and validation."""

    def test_valid_doi_standard_format(self) -> None:
        """Valid DOI with standard format is accepted."""
        doi = DOI("10.1234/sample-article")
        assert doi.value == "10.1234/sample-article"

    def test_valid_doi_with_long_registrant(self) -> None:
        """Valid DOI with long registrant code is accepted."""
        doi = DOI("10.12345678/article")
        assert doi.value == "10.12345678/article"

    def test_valid_doi_with_complex_suffix(self) -> None:
        """Valid DOI with complex suffix characters is accepted."""
        doi = DOI("10.1234/test.article_2024-01;part(1)/sub:section")
        assert doi.value == "10.1234/test.article_2024-01;part(1)/sub:section"

    def test_invalid_doi_empty_string_raises_error(self) -> None:
        """Empty string DOI raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            DOI("")
        assert "cannot be empty" in str(exc_info.value.message)

    def test_invalid_doi_missing_prefix_raises_error(self) -> None:
        """DOI without '10.' prefix raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            DOI("11.1234/article")
        assert "Invalid DOI format" in str(exc_info.value.message)

    def test_invalid_doi_short_registrant_raises_error(self) -> None:
        """DOI with registrant code < 4 digits raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            DOI("10.123/article")
        assert "Invalid DOI format" in str(exc_info.value.message)

    def test_invalid_doi_missing_suffix_raises_error(self) -> None:
        """DOI without suffix raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            DOI("10.1234/")
        assert "Invalid DOI format" in str(exc_info.value.message)

    def test_invalid_doi_no_slash_raises_error(self) -> None:
        """DOI without slash separator raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            DOI("10.1234article")
        assert "Invalid DOI format" in str(exc_info.value.message)


class TestDOIImmutability:
    """Tests for DOI immutability."""

    def test_doi_is_immutable(self) -> None:
        """DOI value cannot be modified after creation."""
        doi = DOI("10.1234/test")
        with pytest.raises(AttributeError):
            doi.value = "10.5678/new"  # type: ignore[misc]


class TestDOIEquality:
    """Tests for DOI equality and hashing."""

    def test_equal_dois_are_equal(self) -> None:
        """Two DOIs with same value are equal."""
        doi1 = DOI("10.1234/test")
        doi2 = DOI("10.1234/test")
        assert doi1 == doi2

    def test_different_dois_are_not_equal(self) -> None:
        """Two DOIs with different values are not equal."""
        doi1 = DOI("10.1234/test1")
        doi2 = DOI("10.1234/test2")
        assert doi1 != doi2

    def test_doi_hash_equality(self) -> None:
        """Equal DOIs have equal hashes."""
        doi1 = DOI("10.1234/test")
        doi2 = DOI("10.1234/test")
        assert hash(doi1) == hash(doi2)

    def test_doi_can_be_used_in_set(self) -> None:
        """DOIs can be used in sets for deduplication."""
        doi1 = DOI("10.1234/test")
        doi2 = DOI("10.1234/test")
        doi3 = DOI("10.1234/other")
        doi_set = {doi1, doi2, doi3}
        assert len(doi_set) == 2


class TestDOIMethods:
    """Tests for DOI methods."""

    def test_str_returns_value(self) -> None:
        """str() returns the DOI value."""
        doi = DOI("10.1234/test")
        assert str(doi) == "10.1234/test"

    def test_to_url_returns_doi_org_url(self) -> None:
        """to_url() returns the doi.org URL."""
        doi = DOI("10.1234/test")
        assert doi.to_url() == "https://doi.org/10.1234/test"
