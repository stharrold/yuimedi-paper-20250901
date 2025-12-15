# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Author value object for academic papers.

Represents an author with name components and optional ORCID identifier.
"""

import re
from dataclasses import dataclass

from lit_review.domain.exceptions import ValidationError

# ORCID pattern: 0000-0000-0000-000X (X can be digit or X for checksum)
ORCID_PATTERN = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")


@dataclass(frozen=True)
class Author:
    """Immutable author value object.

    Represents an author with structured name components for proper citation
    formatting and an optional ORCID identifier for disambiguation.

    Attributes:
        last_name: Author's family name (required).
        first_name: Author's given name (required).
        initials: Author's initials, e.g., "J." or "J.A." (required).
        orcid: Optional ORCID identifier for author disambiguation.

    Raises:
        ValidationError: If required fields are empty or ORCID format is invalid.

    Example:
        >>> author = Author(
        ...     last_name="Smith",
        ...     first_name="John",
        ...     initials="J.",
        ...     orcid="0000-0001-2345-6789"
        ... )
    """

    last_name: str
    first_name: str
    initials: str
    orcid: str | None = None

    def __post_init__(self) -> None:
        """Validate author fields on creation."""
        if not self.last_name or not self.last_name.strip():
            raise ValidationError("Author last_name cannot be empty")

        if not self.first_name or not self.first_name.strip():
            raise ValidationError("Author first_name cannot be empty")

        if not self.initials or not self.initials.strip():
            raise ValidationError("Author initials cannot be empty")

        if self.orcid is not None and not ORCID_PATTERN.match(self.orcid):
            raise ValidationError(
                f"Invalid ORCID format: '{self.orcid}'. "
                "ORCID must match pattern: 0000-0000-0000-000X"
            )

    def __str__(self) -> str:
        """Return author in 'Last, First' format."""
        return f"{self.last_name}, {self.first_name}"

    def format_citation(self) -> str:
        """Format author name for citation (Last, Initials).

        Returns:
            Author name in citation format.

        Example:
            >>> Author("Smith", "John", "J.").format_citation()
            'Smith, J.'
        """
        return f"{self.last_name}, {self.initials}"

    def format_full(self) -> str:
        """Format author with full name.

        Returns:
            Author's full name in 'First Last' format.

        Example:
            >>> Author("Smith", "John", "J.").format_full()
            'John Smith'
        """
        return f"{self.first_name} {self.last_name}"

    def orcid_url(self) -> str | None:
        """Return ORCID as URL if present.

        Returns:
            ORCID URL or None if no ORCID is set.

        Example:
            >>> Author("Smith", "John", "J.", "0000-0001-2345-6789").orcid_url()
            'https://orcid.org/0000-0001-2345-6789'
        """
        if self.orcid:
            return f"https://orcid.org/{self.orcid}"
        return None
