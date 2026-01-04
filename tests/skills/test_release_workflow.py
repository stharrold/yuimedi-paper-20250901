# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for release_workflow.py functionality.

Tests the release workflow script that creates release branches,
runs quality gates, creates PRs, and tags releases.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add skills path to import the module
sys.path.insert(
    0,
    str(
        Path(__file__).parent.parent.parent
        / ".gemini"
        / "skills"
        / "git-workflow-manager"
        / "scripts"
    ),
)

from release_workflow import (
    calculate_next_version,
    get_contrib_branch,
    get_current_branch,
    get_latest_version,
    return_to_editable_branch,
    run_quality_gates,
    show_status,
    step_create_release,
    step_pr_main,
    step_run_gates,
    step_tag_release,
)


class TestGetCurrentBranch:
    """Test get_current_branch function."""

    def test_returns_branch_name(self):
        """Test that branch name is returned."""
        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="feature/test-branch\n", returncode=0)
            result = get_current_branch()
            assert result == "feature/test-branch"

    def test_strips_whitespace(self):
        """Test that whitespace is stripped from branch name."""
        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="  main  \n", returncode=0)
            result = get_current_branch()
            assert result == "main"

    def test_handles_empty_output(self):
        """Test handling of empty output (detached HEAD)."""
        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=0)
            result = get_current_branch()
            assert result == ""


class TestGetContribBranch:
    """Test get_contrib_branch function."""

    def test_returns_contrib_branch_format(self):
        """Test that contrib/username format is returned."""
        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="testuser\n", returncode=0)
            result = get_contrib_branch()
            assert result == "contrib/testuser"

    def test_raises_on_empty_username(self):
        """Test that RuntimeError is raised when username is empty."""
        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=0)
            with pytest.raises(RuntimeError, match="Failed to get GitHub username"):
                get_contrib_branch()

    def test_raises_on_whitespace_only_username(self):
        """Test that RuntimeError is raised when username is whitespace."""
        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="   \n", returncode=0)
            with pytest.raises(RuntimeError, match="Failed to get GitHub username"):
                get_contrib_branch()


class TestReturnToEditableBranch:
    """Test return_to_editable_branch function."""

    def test_returns_true_when_already_on_contrib(self):
        """Test that True is returned when already on contrib branch."""
        with patch("release_workflow.get_contrib_branch", return_value="contrib/testuser"):
            with patch("release_workflow.get_current_branch", return_value="contrib/testuser"):
                result = return_to_editable_branch()
                assert result is True

    def test_returns_true_on_successful_checkout(self):
        """Test that True is returned when checkout succeeds."""
        with patch("release_workflow.get_contrib_branch", return_value="contrib/testuser"):
            with patch("release_workflow.get_current_branch", return_value="main"):
                with patch("release_workflow.run_cmd") as mock_run:
                    mock_run.return_value = MagicMock(returncode=0, stderr="")
                    result = return_to_editable_branch()
                    assert result is True

    def test_returns_false_on_checkout_failure(self):
        """Test that False is returned when checkout fails."""
        with patch("release_workflow.get_contrib_branch", return_value="contrib/testuser"):
            with patch("release_workflow.get_current_branch", return_value="main"):
                with patch("release_workflow.run_cmd") as mock_run:
                    mock_run.return_value = MagicMock(returncode=1, stderr="error: checkout failed")
                    result = return_to_editable_branch()
                    assert result is False


class TestGetLatestVersion:
    """Test get_latest_version function."""

    def test_returns_tag_from_main(self):
        """Test that version tag is returned from main."""
        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="v1.5.0\n", returncode=0)
            result = get_latest_version()
            assert result == "v1.5.0"

    def test_returns_default_on_failure(self):
        """Test that v0.0.0 is returned when no tags exist."""
        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=128)
            result = get_latest_version()
            assert result == "v0.0.0"

    def test_strips_whitespace_from_tag(self):
        """Test that whitespace is stripped from tag."""
        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="  v2.0.0  \n", returncode=0)
            result = get_latest_version()
            assert result == "v2.0.0"


class TestCalculateNextVersion:
    """Test calculate_next_version function."""

    def test_bumps_minor_version(self):
        """Test that minor version is bumped."""
        result = calculate_next_version("v1.5.0")
        assert result == "v1.6.0"

    def test_handles_version_without_v_prefix(self):
        """Test handling of version without v prefix."""
        result = calculate_next_version("1.5.0")
        assert result == "v1.6.0"

    def test_resets_patch_version(self):
        """Test that patch version is reset to 0."""
        result = calculate_next_version("v1.5.3")
        assert result == "v1.6.0"

    def test_returns_default_for_invalid_version(self):
        """Test that v1.0.0 is returned for invalid versions."""
        result = calculate_next_version("invalid")
        assert result == "v1.0.0"

    def test_returns_default_for_single_number(self):
        """Test that v1.0.0 is returned for single number."""
        result = calculate_next_version("5")
        assert result == "v1.0.0"

    def test_handles_high_version_numbers(self):
        """Test handling of high version numbers."""
        result = calculate_next_version("v10.99.5")
        assert result == "v10.100.0"


class TestRunQualityGates:
    """Test run_quality_gates function."""

    def test_returns_true_on_success(self):
        """Test that True is returned when quality gates pass."""
        with patch("release_workflow.Path.exists", return_value=True):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                result = run_quality_gates()
                assert result is True

    def test_returns_false_on_failure(self):
        """Test that False is returned when quality gates fail."""
        with patch("release_workflow.Path.exists", return_value=True):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=1)
                result = run_quality_gates()
                assert result is False

    def test_returns_true_when_script_not_found(self):
        """Test that True is returned when quality gates script doesn't exist."""
        with patch("release_workflow.Path.exists", return_value=False):
            result = run_quality_gates()
            assert result is True


class TestStepCreateRelease:
    """Test step_create_release function."""

    def test_creates_release_branch(self):
        """Test that release branch is created."""
        with patch("release_workflow.get_latest_version", return_value="v1.5.0"):
            with patch("release_workflow.run_cmd") as mock_run:
                # Simulate: fetch succeeds, no existing branch, create succeeds, push succeeds
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout="", stderr=""),  # fetch
                    MagicMock(returncode=0, stdout="", stderr=""),  # check existing
                    MagicMock(returncode=0, stdout="", stderr=""),  # create branch
                    MagicMock(returncode=0, stdout="", stderr=""),  # push
                ]
                result = step_create_release()
                assert result is True

    def test_uses_provided_version(self):
        """Test that provided version is used."""
        with patch("release_workflow.run_cmd") as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),  # fetch
                MagicMock(returncode=0, stdout="", stderr=""),  # check existing
                MagicMock(returncode=0, stdout="", stderr=""),  # create branch
                MagicMock(returncode=0, stdout="", stderr=""),  # push
            ]
            result = step_create_release(version="v2.0.0")
            assert result is True
            # Verify branch name contains provided version
            create_call = mock_run.call_args_list[2]
            assert "release/v2.0.0" in create_call[0][0]

    def test_returns_true_when_branch_exists(self):
        """Test that True is returned when release branch already exists."""
        with patch("release_workflow.get_latest_version", return_value="v1.5.0"):
            with patch("release_workflow.run_cmd") as mock_run:
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout="", stderr=""),  # fetch
                    MagicMock(
                        returncode=0, stdout="origin/release/v1.6.0\n", stderr=""
                    ),  # check existing
                ]
                result = step_create_release()
                assert result is True

    def test_returns_false_on_branch_creation_failure(self):
        """Test that False is returned when branch creation fails."""
        with patch("release_workflow.get_latest_version", return_value="v1.5.0"):
            with patch("release_workflow.run_cmd") as mock_run:
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout="", stderr=""),  # fetch
                    MagicMock(returncode=0, stdout="", stderr=""),  # check existing
                    MagicMock(
                        returncode=1, stdout="", stderr="error: branch creation failed"
                    ),  # create branch
                ]
                result = step_create_release()
                assert result is False

    def test_returns_false_on_push_failure(self):
        """Test that False is returned when push fails."""
        with patch("release_workflow.get_latest_version", return_value="v1.5.0"):
            with patch("release_workflow.run_cmd") as mock_run:
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout="", stderr=""),  # fetch
                    MagicMock(returncode=0, stdout="", stderr=""),  # check existing
                    MagicMock(returncode=0, stdout="", stderr=""),  # create branch
                    MagicMock(returncode=1, stdout="", stderr="error: push failed"),  # push
                ]
                result = step_create_release()
                assert result is False


class TestStepRunGates:
    """Test step_run_gates function."""

    def test_returns_true_on_success(self):
        """Test that True is returned when gates pass."""
        with patch("release_workflow.run_quality_gates", return_value=True):
            result = step_run_gates()
            assert result is True

    def test_returns_false_on_failure(self):
        """Test that False is returned when gates fail."""
        with patch("release_workflow.run_quality_gates", return_value=False):
            result = step_run_gates()
            assert result is False


class TestStepPrMain:
    """Test step_pr_main function."""

    def test_returns_false_when_not_on_release_branch(self):
        """Test that False is returned when not on release branch."""
        with patch("release_workflow.get_current_branch", return_value="main"):
            result = step_pr_main()
            assert result is False

    def test_returns_false_on_develop_branch(self):
        """Test that False is returned when on develop branch."""
        with patch("release_workflow.get_current_branch", return_value="develop"):
            result = step_pr_main()
            assert result is False

    def test_creates_pr_successfully(self):
        """Test that PR is created successfully."""
        with patch("release_workflow.get_current_branch", return_value="release/v1.6.0"):
            with patch("release_workflow.run_cmd") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                result = step_pr_main()
                assert result is True

    def test_returns_true_when_pr_exists(self):
        """Test that True is returned when PR already exists."""
        with patch("release_workflow.get_current_branch", return_value="release/v1.6.0"):
            with patch("release_workflow.run_cmd") as mock_run:
                mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="already exists")
                result = step_pr_main()
                assert result is True

    def test_returns_false_on_pr_creation_failure(self):
        """Test that False is returned when PR creation fails."""
        with patch("release_workflow.get_current_branch", return_value="release/v1.6.0"):
            with patch("release_workflow.run_cmd") as mock_run:
                mock_run.return_value = MagicMock(
                    returncode=1, stdout="", stderr="error: permission denied"
                )
                result = step_pr_main()
                assert result is False


class TestStepTagRelease:
    """Test step_tag_release function."""

    def test_extracts_version_from_release_branch(self):
        """Test that version is extracted from release branch name."""
        with patch("release_workflow.get_current_branch", return_value="release/v1.6.0"):
            with patch("release_workflow.run_cmd") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                with patch("release_workflow.return_to_editable_branch", return_value=True):
                    step_tag_release()
                    # Verify tag command was called with correct version
                    tag_calls = [c for c in mock_run.call_args_list if "tag" in str(c)]
                    assert len(tag_calls) > 0

    def test_finds_release_branch_when_not_on_release(self):
        """Test that release branch is found when on different branch."""
        with patch("release_workflow.get_current_branch", return_value="main"):
            with patch("release_workflow.run_cmd") as mock_run:
                mock_run.side_effect = [
                    MagicMock(
                        returncode=0, stdout="origin/release/v1.6.0\n", stderr=""
                    ),  # find release
                    MagicMock(returncode=0, stdout="", stderr=""),  # checkout
                    MagicMock(returncode=0, stdout="", stderr=""),  # pull
                    MagicMock(returncode=0, stdout="", stderr=""),  # tag
                    MagicMock(returncode=0, stdout="", stderr=""),  # push tag
                ]
                with patch("release_workflow.return_to_editable_branch", return_value=True):
                    result = step_tag_release()
                    assert result is True

    def test_returns_false_when_no_version_found(self):
        """Test that False is returned when no version can be determined."""
        with patch("release_workflow.get_current_branch", return_value="main"):
            with patch("release_workflow.run_cmd") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                result = step_tag_release()
                assert result is False

    def test_returns_true_when_tag_exists(self):
        """Test that True is returned when tag already exists."""
        with patch("release_workflow.get_current_branch", return_value="release/v1.6.0"):
            with patch("release_workflow.run_cmd") as mock_run:
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout="", stderr=""),  # checkout
                    MagicMock(returncode=0, stdout="", stderr=""),  # pull
                    MagicMock(returncode=1, stdout="", stderr="already exists"),  # tag
                    MagicMock(returncode=0, stdout="", stderr=""),  # push tag (warning)
                ]
                with patch("release_workflow.return_to_editable_branch", return_value=True):
                    result = step_tag_release()
                    assert result is True

    def test_returns_false_on_tag_creation_failure(self):
        """Test that False is returned when tag creation fails."""
        with patch("release_workflow.get_current_branch", return_value="release/v1.6.0"):
            with patch("release_workflow.run_cmd") as mock_run:
                mock_run.side_effect = [
                    MagicMock(returncode=0, stdout="", stderr=""),  # checkout
                    MagicMock(returncode=0, stdout="", stderr=""),  # pull
                    MagicMock(returncode=1, stdout="", stderr="error: tag failed"),  # tag
                ]
                result = step_tag_release()
                assert result is False


class TestShowStatus:
    """Test show_status function."""

    def test_returns_none(self):
        """Test that show_status returns None (display only)."""
        with patch("release_workflow.get_current_branch", return_value="develop"):
            with patch("release_workflow.get_latest_version", return_value="v1.5.0"):
                with patch("release_workflow.run_cmd") as mock_run:
                    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                    result = show_status()
                    assert result is None

    def test_displays_release_branches(self):
        """Test that release branches are displayed."""
        with patch("release_workflow.get_current_branch", return_value="develop"):
            with patch("release_workflow.get_latest_version", return_value="v1.5.0"):
                with patch("release_workflow.run_cmd") as mock_run:
                    mock_run.return_value = MagicMock(
                        returncode=0,
                        stdout="origin/release/v1.5.0\norigin/release/v1.6.0\n",
                        stderr="",
                    )
                    result = show_status()
                    # Should run without error
                    assert result is None


class TestVersionCalculation:
    """Test version calculation edge cases."""

    def test_major_version_zero(self):
        """Test bumping minor when major is 0."""
        result = calculate_next_version("v0.5.0")
        assert result == "v0.6.0"

    def test_minor_version_rollover(self):
        """Test that minor version can exceed 9."""
        result = calculate_next_version("v1.9.0")
        assert result == "v1.10.0"

    def test_preserves_major_version(self):
        """Test that major version is preserved."""
        result = calculate_next_version("v5.3.2")
        assert result.startswith("v5.")

    def test_two_digit_minor(self):
        """Test handling of two-digit minor version."""
        result = calculate_next_version("v1.15.3")
        assert result == "v1.16.0"


class TestRunCmd:
    """Test run_cmd function."""

    def test_calls_subprocess_run(self):
        """Test that subprocess.run is called with correct args."""
        # Import run_cmd separately to test it
        from release_workflow import run_cmd

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="output", stderr="")
            run_cmd(["git", "status"], check=False)
            mock_run.assert_called_once()
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "status"]
            assert call_args[1]["capture_output"] is True
            assert call_args[1]["text"] is True

    def test_check_parameter_passed(self):
        """Test that check parameter is passed to subprocess."""
        from release_workflow import run_cmd

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            run_cmd(["git", "status"], check=True)
            assert mock_run.call_args[1]["check"] is True
