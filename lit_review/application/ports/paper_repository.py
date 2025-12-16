# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Paper repository port for persistence operations.

Defines the abstract interface for storing and retrieving Review entities.
"""

from abc import ABC, abstractmethod

from lit_review.domain.entities.review import Review


class PaperRepository(ABC):
    """Abstract base class for review persistence.

    Implementations should handle serialization, file I/O, and
    provide atomic write operations for data integrity.

    Example:
        >>> class JSONRepository(PaperRepository):
        ...     def save(self, review: Review) -> None:
        ...         # Implementation
        ...         pass
    """

    @abstractmethod
    def save(self, review: Review) -> None:
        """Persist a review to storage.

        Args:
            review: Review entity to save.

        Raises:
            IOError: If unable to write to storage.
        """
        pass

    @abstractmethod
    def load(self, review_id: str) -> Review:
        """Load a review from storage.

        Args:
            review_id: Identifier of the review to load.

        Returns:
            The loaded Review entity.

        Raises:
            EntityNotFoundError: If review is not found.
            IOError: If unable to read from storage.
        """
        pass

    @abstractmethod
    def delete(self, review_id: str) -> None:
        """Delete a review from storage.

        Args:
            review_id: Identifier of the review to delete.

        Raises:
            EntityNotFoundError: If review is not found.
            IOError: If unable to delete from storage.
        """
        pass

    @abstractmethod
    def list_reviews(self) -> list[str]:
        """List all review IDs in storage.

        Returns:
            List of review identifiers.

        Raises:
            IOError: If unable to read from storage.
        """
        pass

    @abstractmethod
    def exists(self, review_id: str) -> bool:
        """Check if a review exists in storage.

        Args:
            review_id: Identifier of the review to check.

        Returns:
            True if review exists, False otherwise.
        """
        pass
