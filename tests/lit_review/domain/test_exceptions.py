"""Tests for domain exceptions."""

import pytest

from lit_review.domain.exceptions import (
    DomainError,
    EntityNotFoundError,
    ValidationError,
    WorkflowError,
)


class TestDomainError:
    """Tests for DomainError base class."""

    def test_domain_error_stores_message(self) -> None:
        """DomainError stores the message parameter."""
        error = DomainError("Test error message")
        assert error.message == "Test error message"

    def test_domain_error_string_representation(self) -> None:
        """DomainError has correct string representation."""
        error = DomainError("Test error")
        assert str(error) == "Test error"


class TestValidationError:
    """Tests for ValidationError."""

    def test_validation_error_is_domain_error(self) -> None:
        """ValidationError is a DomainError subclass."""
        error = ValidationError("Invalid data")
        assert isinstance(error, DomainError)

    def test_validation_error_can_be_raised_and_caught(self) -> None:
        """ValidationError can be raised and caught."""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Invalid DOI format")
        assert exc_info.value.message == "Invalid DOI format"


class TestWorkflowError:
    """Tests for WorkflowError."""

    def test_workflow_error_is_domain_error(self) -> None:
        """WorkflowError is a DomainError subclass."""
        error = WorkflowError("Invalid transition")
        assert isinstance(error, DomainError)

    def test_workflow_error_can_be_raised_and_caught(self) -> None:
        """WorkflowError can be raised and caught."""
        with pytest.raises(WorkflowError) as exc_info:
            raise WorkflowError("Cannot add papers during PLANNING")
        assert "PLANNING" in exc_info.value.message


class TestEntityNotFoundError:
    """Tests for EntityNotFoundError."""

    def test_entity_not_found_error_is_domain_error(self) -> None:
        """EntityNotFoundError is a DomainError subclass."""
        error = EntityNotFoundError("Paper not found")
        assert isinstance(error, DomainError)

    def test_entity_not_found_error_can_be_raised_and_caught(self) -> None:
        """EntityNotFoundError can be raised and caught."""
        with pytest.raises(EntityNotFoundError) as exc_info:
            raise EntityNotFoundError("Review with ID 'test' not found")
        assert "not found" in exc_info.value.message
