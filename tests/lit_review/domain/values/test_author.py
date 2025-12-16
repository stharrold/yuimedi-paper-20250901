# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for Author value object."""

import pytest

from lit_review.domain.exceptions import ValidationError
from lit_review.domain.values.author import Author


class TestAuthorCreation:
    """Tests for Author creation and validation."""

    def test_valid_author_without_orcid(self) -> None:
        """Valid author without ORCID is created successfully."""
        author = Author(last_name="Smith", first_name="John", initials="J.")
        assert author.last_name == "Smith"
        assert author.first_name == "John"
        assert author.initials == "J."
        assert author.orcid is None

    def test_valid_author_with_orcid(self) -> None:
        """Valid author with ORCID is created successfully."""
        author = Author(
            last_name="Smith",
            first_name="John",
            initials="J.",
            orcid="0000-0001-2345-6789",
        )
        assert author.orcid == "0000-0001-2345-6789"

    def test_valid_author_with_orcid_checksum_x(self) -> None:
        """Valid author with ORCID ending in X is accepted."""
        author = Author(
            last_name="Smith",
            first_name="John",
            initials="J.",
            orcid="0000-0001-2345-678X",
        )
        assert author.orcid == "0000-0001-2345-678X"

    def test_empty_last_name_raises_error(self) -> None:
        """Empty last_name raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Author(last_name="", first_name="John", initials="J.")
        assert "last_name cannot be empty" in str(exc_info.value.message)

    def test_whitespace_last_name_raises_error(self) -> None:
        """Whitespace-only last_name raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Author(last_name="   ", first_name="John", initials="J.")
        assert "last_name cannot be empty" in str(exc_info.value.message)

    def test_empty_first_name_raises_error(self) -> None:
        """Empty first_name raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Author(last_name="Smith", first_name="", initials="J.")
        assert "first_name cannot be empty" in str(exc_info.value.message)

    def test_empty_initials_raises_error(self) -> None:
        """Empty initials raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Author(last_name="Smith", first_name="John", initials="")
        assert "initials cannot be empty" in str(exc_info.value.message)

    def test_invalid_orcid_format_raises_error(self) -> None:
        """Invalid ORCID format raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Author(
                last_name="Smith",
                first_name="John",
                initials="J.",
                orcid="invalid-orcid",
            )
        assert "Invalid ORCID format" in str(exc_info.value.message)


class TestAuthorImmutability:
    """Tests for Author immutability."""

    def test_author_is_immutable(self) -> None:
        """Author attributes cannot be modified after creation."""
        author = Author(last_name="Smith", first_name="John", initials="J.")
        with pytest.raises(AttributeError):
            author.last_name = "Jones"  # type: ignore[misc]


class TestAuthorEquality:
    """Tests for Author equality."""

    def test_equal_authors_are_equal(self) -> None:
        """Two authors with same values are equal."""
        author1 = Author(last_name="Smith", first_name="John", initials="J.")
        author2 = Author(last_name="Smith", first_name="John", initials="J.")
        assert author1 == author2

    def test_different_authors_are_not_equal(self) -> None:
        """Two authors with different values are not equal."""
        author1 = Author(last_name="Smith", first_name="John", initials="J.")
        author2 = Author(last_name="Jones", first_name="Jane", initials="J.")
        assert author1 != author2


class TestAuthorFormatting:
    """Tests for Author formatting methods."""

    def test_str_returns_last_first_format(self) -> None:
        """str() returns 'Last, First' format."""
        author = Author(last_name="Smith", first_name="John", initials="J.")
        assert str(author) == "Smith, John"

    def test_format_citation_returns_last_initials(self) -> None:
        """format_citation() returns 'Last, Initials' format."""
        author = Author(last_name="Smith", first_name="John", initials="J.A.")
        assert author.format_citation() == "Smith, J.A."

    def test_format_full_returns_first_last(self) -> None:
        """format_full() returns 'First Last' format."""
        author = Author(last_name="Smith", first_name="John", initials="J.")
        assert author.format_full() == "John Smith"

    def test_orcid_url_returns_url_when_set(self) -> None:
        """orcid_url() returns URL when ORCID is set."""
        author = Author(
            last_name="Smith",
            first_name="John",
            initials="J.",
            orcid="0000-0001-2345-6789",
        )
        assert author.orcid_url() == "https://orcid.org/0000-0001-2345-6789"

    def test_orcid_url_returns_none_when_not_set(self) -> None:
        """orcid_url() returns None when ORCID is not set."""
        author = Author(last_name="Smith", first_name="John", initials="J.")
        assert author.orcid_url() is None
