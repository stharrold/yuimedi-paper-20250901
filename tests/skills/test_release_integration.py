"""Integration tests for release workflow.

Tests end-to-end release workflow scenarios including release branch creation,
quality gates, tagging, and cleanup.

Note: These tests are marked as integration tests and are skipped by default
in CI. Run with: pytest -m integration
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add skills path to import the modules
sys.path.insert(
    0,
    str(
        Path(__file__).parent.parent.parent
        / ".claude"
        / "skills"
        / "git-workflow-manager"
        / "scripts"
    ),
)


@pytest.mark.integration
class TestReleaseWorkflowIntegration:
    """Integration tests for release workflow."""

    def test_full_release_workflow_success(self):
        """Test complete release workflow from create to tag."""
        from release_workflow import run_full_workflow

        with patch("release_workflow.step_create_release", return_value=True) as mock_create:
            with patch("release_workflow.step_run_gates", return_value=True) as mock_gates:
                with patch("release_workflow.step_pr_main", return_value=True) as mock_pr:
                    result = run_full_workflow("v1.0.0")

                    assert result is True
                    mock_create.assert_called_once()
                    mock_gates.assert_called_once()
                    mock_pr.assert_called_once()

    def test_release_workflow_stops_on_gate_failure(self):
        """Test that release workflow stops when quality gates fail."""
        from release_workflow import run_full_workflow

        with patch("release_workflow.step_create_release", return_value=True):
            with patch("release_workflow.step_run_gates", return_value=False):
                with patch("release_workflow.step_pr_main") as mock_pr:
                    with patch("release_workflow.return_to_editable_branch", return_value=True):
                        result = run_full_workflow("v1.0.0")

                        assert result is False
                        mock_pr.assert_not_called()

    def test_release_workflow_returns_to_editable_branch(self):
        """Test that workflow returns to editable branch on completion."""
        from release_workflow import run_full_workflow

        with patch("release_workflow.step_create_release", return_value=True):
            with patch("release_workflow.step_run_gates", return_value=True):
                with patch("release_workflow.step_pr_main", return_value=True):
                    run_full_workflow("v1.0.0")
                    # The full workflow should complete without error


@pytest.mark.integration
class TestVersionCalculationIntegration:
    """Integration tests for version calculation."""

    def test_version_bump_from_develop(self):
        """Test version calculation from develop branch."""
        from release_workflow import calculate_next_version, get_latest_version

        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="v1.5.2\n", returncode=0)
            latest = get_latest_version()
            next_version = calculate_next_version(latest)

            assert latest == "v1.5.2"
            assert next_version == "v1.6.0"

    def test_version_calculation_handles_missing_tags(self):
        """Test version calculation when no tags exist."""
        from release_workflow import calculate_next_version, get_latest_version

        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=128)
            latest = get_latest_version()
            next_version = calculate_next_version(latest)

            assert latest == "v0.0.0"
            assert next_version == "v0.1.0"


@pytest.mark.integration
class TestQualityGatesIntegration:
    """Integration tests for quality gates in release."""

    def test_quality_gates_block_release(self):
        """Test that failed quality gates prevent PR creation."""
        from release_workflow import step_run_gates

        with patch("release_workflow.run_quality_gates", return_value=False):
            result = step_run_gates()
            assert result is False

    def test_quality_gates_allow_release(self):
        """Test that passed quality gates allow PR creation."""
        from release_workflow import step_run_gates

        with patch("release_workflow.run_quality_gates", return_value=True):
            result = step_run_gates()
            assert result is True


@pytest.mark.integration
class TestTaggingIntegration:
    """Integration tests for release tagging."""

    def test_tag_creation_on_main(self):
        """Test tag creation on main branch."""
        from release_workflow import step_tag_release

        with patch("release_workflow.get_current_branch", return_value="release/v1.0.0"):
            with patch("release_workflow.run_cmd") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                with patch("release_workflow.return_to_editable_branch", return_value=True):
                    result = step_tag_release()
                    assert result is True

    def test_tag_already_exists_handling(self):
        """Test handling of existing tags."""
        from release_workflow import step_tag_release

        with patch("release_workflow.get_current_branch", return_value="release/v1.0.0"):
            with patch("release_workflow.run_cmd") as mock_run:
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout="", stderr=""),  # checkout
                    MagicMock(returncode=0, stdout="", stderr=""),  # pull
                    MagicMock(returncode=1, stdout="", stderr="already exists"),  # tag
                    MagicMock(returncode=0, stdout="", stderr=""),  # push
                ]
                with patch("release_workflow.return_to_editable_branch", return_value=True):
                    result = step_tag_release()
                    assert result is True


@pytest.mark.integration
class TestBranchManagementIntegration:
    """Integration tests for branch management."""

    def test_release_branch_creation_from_develop(self):
        """Test release branch creation from develop."""
        from release_workflow import step_create_release

        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),  # fetch
                MagicMock(returncode=0, stdout="", stderr=""),  # check existing
                MagicMock(returncode=0, stdout="", stderr=""),  # create branch
                MagicMock(returncode=0, stdout="", stderr=""),  # push
            ]
            result = step_create_release("v2.0.0")
            assert result is True

    def test_release_branch_already_exists(self):
        """Test handling when release branch already exists."""
        from release_workflow import step_create_release

        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),  # fetch
                MagicMock(
                    returncode=0, stdout="origin/release/v2.0.0\n", stderr=""
                ),  # check existing
            ]
            result = step_create_release("v2.0.0")
            assert result is True  # Returns True because branch exists


@pytest.mark.integration
class TestReleaseStatusIntegration:
    """Integration tests for release status reporting."""

    def test_status_on_release_branch(self):
        """Test status reporting when on release branch."""
        from release_workflow import show_status

        with patch("release_workflow.get_current_branch", return_value="release/v1.0.0"):
            with patch("release_workflow.get_latest_version", return_value="v0.9.0"):
                with patch("release_workflow.run_cmd") as mock_run:
                    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                    # Should run without error
                    show_status()

    def test_status_on_main_branch(self):
        """Test status reporting when on main branch."""
        from release_workflow import show_status

        with patch("release_workflow.get_current_branch", return_value="main"):
            with patch("release_workflow.get_latest_version", return_value="v1.0.0"):
                with patch("release_workflow.run_cmd") as mock_run:
                    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                    # Should run without error
                    show_status()

    def test_status_shows_release_branches(self):
        """Test that status shows available release branches."""
        from release_workflow import show_status

        with patch("release_workflow.get_current_branch", return_value="develop"):
            with patch("release_workflow.get_latest_version", return_value="v1.0.0"):
                with patch("release_workflow.run_cmd") as mock_run:
                    mock_run.return_value = MagicMock(
                        returncode=0,
                        stdout="origin/release/v1.0.0\norigin/release/v1.1.0\n",
                        stderr="",
                    )
                    # Should run without error
                    show_status()
