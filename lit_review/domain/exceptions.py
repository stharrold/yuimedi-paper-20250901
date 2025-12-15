# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Domain exceptions for lit_review.

These exceptions represent business rule violations and domain errors.
"""


class DomainError(Exception):
    """Base exception for all domain errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class ValidationError(DomainError):
    """Raised when domain data validation fails.

    Examples:
        - Invalid DOI format
        - Missing required fields
        - Value out of allowed range
    """

    pass


class WorkflowError(DomainError):
    """Raised when workflow rules are violated.

    Examples:
        - Adding papers during PLANNING stage
        - Skipping workflow stages
        - Invalid state transitions
    """

    pass


class EntityNotFoundError(DomainError):
    """Raised when a requested entity is not found.

    Examples:
        - Paper not found by DOI
        - Review not found by ID
    """

    pass
