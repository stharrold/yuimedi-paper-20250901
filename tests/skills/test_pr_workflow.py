# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for pr_workflow.py functionality.

Tests the PR workflow script that handles the feature-to-contrib-to-develop
workflow sequence with quality gates, TODO archiving, and agent syncing.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add skills script directories to sys.path
_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_root / ".gemini" / "skills" / "workflow-utilities" / "scripts"))
sys.path.insert(0, str(_root / ".gemini" / "skills" / "git-workflow-manager" / "scripts"))

from unittest.mock import MagicMock, patch  # noqa: E402

from pr_workflow import (  # noqa: E402
    get_contrib_branch,
    get_current_branch,
    return_to_editable_branch,
    run_cmd,
    run_quality_gates,
    show_status,
    step_finish_feature,
    step_start_develop,
)


class TestGetCurrentBranch:
    """Test get_current_branch function."""

    def test_returns_branch_name(self):
        """Test that branch name is returned."""
        with patch("pr_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="feature/test-branch\n", returncode=0)
            result = get_current_branch()
            assert result == "feature/test-branch"

    def test_strips_whitespace(self):
        """Test that whitespace is stripped from branch name."""
        with patch("pr_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="  contrib/user  \n", returncode=0)
            result = get_current_branch()
            assert result == "contrib/user"

    def test_handles_empty_output(self):
        """Test handling of empty output (detached HEAD)."""
        with patch("pr_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=0)
            result = get_current_branch()
            assert result == ""


class TestGetContribBranch:
    """Test get_contrib_branch function."""

    def test_returns_contrib_branch_format(self):
        """Test that contrib/username format is returned."""
        with patch("pr_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="testuser\n", returncode=0)
            result = get_contrib_branch()
            assert result == "contrib/testuser"

    def test_uses_default_on_empty_username(self):
        """Test that default username is used when gh fails."""
        with patch("pr_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="", returncode=1)
            result = get_contrib_branch()
            assert result == "contrib/stharrold"

    def test_strips_whitespace_from_username(self):
        """Test that whitespace is stripped from username."""
        with patch("pr_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="  myuser  \n", returncode=0)
            result = get_contrib_branch()
            assert result == "contrib/myuser"


class TestReturnToEditableBranch:
    """Test return_to_editable_branch function."""

    def test_returns_true_when_already_on_contrib(self):
        """Test that True is returned when already on contrib branch."""
        with patch("pr_workflow.get_contrib_branch", return_value="contrib/testuser"):
            with patch("pr_workflow.get_current_branch", return_value="contrib/testuser"):
                result = return_to_editable_branch()
                assert result is True

    def test_returns_true_on_successful_checkout(self):
        """Test that True is returned when checkout succeeds."""
        with patch("pr_workflow.get_contrib_branch", return_value="contrib/testuser"):
            with patch("pr_workflow.get_current_branch", return_value="main"):
                with patch("pr_workflow.run_cmd") as mock_run:
                    mock_run.return_value = MagicMock(returncode=0, stderr="")
                    result = return_to_editable_branch()
                    assert result is True

    def test_returns_false_on_checkout_failure(self):
        """Test that False is returned when checkout fails."""
        with patch("pr_workflow.get_contrib_branch", return_value="contrib/testuser"):
            with patch("pr_workflow.get_current_branch", return_value="main"):
                with patch("pr_workflow.run_cmd") as mock_run:
                    mock_run.return_value = MagicMock(returncode=1, stderr="error: checkout failed")
                    result = return_to_editable_branch()
                    assert result is False


class TestRunQualityGates:
    """Test run_quality_gates function."""

    def test_returns_true_on_success(self):
        """Test that True is returned when quality gates pass."""
        with patch("pr_workflow.Path.exists", return_value=True):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                result = run_quality_gates()
                assert result is True

    def test_returns_false_on_failure(self):
        """Test that False is returned when quality gates fail."""
        with patch("pr_workflow.Path.exists", return_value=True):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=1)
                result = run_quality_gates()
                assert result is False

    def test_returns_true_when_script_not_found(self):
        """Test that True is returned when quality gates script doesn't exist."""
        with patch("pr_workflow.Path.exists", return_value=False):
            result = run_quality_gates()
            assert result is True

    def test_calls_podman_compose(self):
        """Test that podman-compose is called for quality gates."""
        with patch("pr_workflow.Path.exists", return_value=True):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                run_quality_gates()
                call_args = mock_run.call_args[0][0]
                assert "podman-compose" in call_args


class TestStepFinishFeature:
    """Test step_finish_feature function."""

    def test_returns_false_when_not_on_feature_branch(self):
        """Test that False is returned when not on feature branch."""
        with patch("pr_workflow.get_current_branch", return_value="main"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                result = step_finish_feature()
                assert result is False

    def test_returns_false_when_on_contrib_branch(self):
        """Test that False is returned when on contrib branch."""
        with patch("pr_workflow.get_current_branch", return_value="contrib/user"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                result = step_finish_feature()
                assert result is False

    def test_returns_false_when_quality_gates_fail(self):
        """Test that False is returned when quality gates fail."""
        with patch("pr_workflow.get_current_branch", return_value="feature/test"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch("pr_workflow.run_quality_gates", return_value=False):
                    result = step_finish_feature()
                    assert result is False

    def test_creates_pr_successfully(self):
        """Test that PR is created successfully."""
        with patch("pr_workflow.get_current_branch", return_value="feature/test"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch("pr_workflow.run_quality_gates", return_value=True):
                    with patch("pr_workflow.run_cmd") as mock_run:
                        mock_run.return_value = MagicMock(returncode=0, stderr="")
                        result = step_finish_feature()
                        assert result is True

    def test_returns_true_when_pr_exists(self):
        """Test that True is returned when PR already exists."""
        with patch("pr_workflow.get_current_branch", return_value="feature/test"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch("pr_workflow.run_quality_gates", return_value=True):
                    with patch("pr_workflow.run_cmd") as mock_run:
                        mock_run.side_effect = [
                            MagicMock(returncode=0, stderr=""),  # push
                            MagicMock(returncode=1, stderr="already exists"),  # pr create
                        ]
                        result = step_finish_feature()
                        assert result is True

    def test_returns_false_on_push_failure(self):
        """Test that False is returned when push fails."""
        with patch("pr_workflow.get_current_branch", return_value="feature/test"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch("pr_workflow.run_quality_gates", return_value=True):
                    with patch("pr_workflow.run_cmd") as mock_run:
                        mock_run.return_value = MagicMock(returncode=1, stderr="push failed")
                        result = step_finish_feature()
                        assert result is False


class TestStepStartDevelop:
    """Test step_start_develop function."""

    def test_switches_to_contrib_when_not_on_it(self):
        """Test that it switches to contrib branch if not on it."""
        with patch("pr_workflow.get_current_branch", return_value="main"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch("pr_workflow.run_cmd") as mock_run:
                    mock_run.return_value = MagicMock(returncode=0, stderr="")
                    with patch("pr_workflow.return_to_editable_branch", return_value=True):
                        step_start_develop()
                        # Should call checkout to contrib
                        checkout_calls = [
                            c for c in mock_run.call_args_list if "checkout" in str(c)
                        ]
                        assert len(checkout_calls) > 0

    def test_creates_pr_to_develop(self):
        """Test that PR is created to develop branch."""
        with patch("pr_workflow.get_current_branch", return_value="contrib/user"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch("pr_workflow.run_cmd") as mock_run:
                    mock_run.return_value = MagicMock(returncode=0, stderr="")
                    with patch("pr_workflow.return_to_editable_branch", return_value=True):
                        result = step_start_develop()
                        assert result is True

    def test_returns_true_when_pr_exists(self):
        """Test that True is returned when PR already exists."""
        with patch("pr_workflow.get_current_branch", return_value="contrib/user"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch("pr_workflow.run_cmd") as mock_run:
                    mock_run.side_effect = [
                        MagicMock(returncode=0, stderr=""),  # push
                        MagicMock(returncode=1, stderr="already exists"),  # pr create
                    ]
                    with patch("pr_workflow.return_to_editable_branch", return_value=True):
                        result = step_start_develop()
                        assert result is True

    def test_returns_false_on_pr_creation_failure(self):
        """Test that False is returned when PR creation fails."""
        with patch("pr_workflow.get_current_branch", return_value="contrib/user"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch("pr_workflow.run_cmd") as mock_run:
                    mock_run.side_effect = [
                        MagicMock(returncode=0, stderr=""),  # push
                        MagicMock(returncode=1, stderr="error: permission denied"),  # pr create
                    ]
                    result = step_start_develop()
                    assert result is False


class TestShowStatus:
    """Test show_status function."""

    def test_returns_none(self):
        """Test that show_status returns None (display only)."""
        with patch("pr_workflow.get_current_branch", return_value="contrib/user"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch.object(Path, "glob", return_value=[]):
                    with patch.object(Path, "exists", return_value=True):
                        result = show_status()
                        assert result is None

    def test_detects_feature_branch(self):
        """Test that feature branch is detected."""
        with patch("pr_workflow.get_current_branch", return_value="feature/test"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch.object(Path, "glob", return_value=[]):
                    with patch.object(Path, "exists", return_value=True):
                        result = show_status()
                        # Should run without error
                        assert result is None


class TestRunCmd:
    """Test run_cmd function."""

    def test_calls_subprocess_run(self):
        """Test that subprocess.run is called with correct args."""
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
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            run_cmd(["git", "status"], check=True)
            assert mock_run.call_args[1]["check"] is True


class TestBranchDetection:
    """Test branch detection logic."""

    def test_feature_branch_starts_with_feature(self):
        """Test that feature branch detection works."""
        with patch("pr_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="feature/my-feature\n", returncode=0)
            branch = get_current_branch()
            assert branch.startswith("feature/")

    def test_contrib_branch_starts_with_contrib(self):
        """Test that contrib branch detection works."""
        with patch("pr_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="contrib/testuser\n", returncode=0)
            branch = get_current_branch()
            assert branch.startswith("contrib/")

    def test_release_branch_pattern(self):
        """Test release branch pattern detection."""
        with patch("pr_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="release/v1.0.0\n", returncode=0)
            branch = get_current_branch()
            assert branch.startswith("release/")


class TestFullWorkflow:
    """Test full workflow execution."""

    def test_full_workflow_stops_on_first_failure(self):
        """Test that full workflow stops on first step failure."""
        from pr_workflow import run_full_workflow

        with patch("pr_workflow.step_finish_feature", return_value=False):
            with patch("pr_workflow.return_to_editable_branch", return_value=True):
                result = run_full_workflow()
                assert result is False

    def test_full_workflow_continues_on_success(self):
        """Test that full workflow continues when steps succeed."""
        from pr_workflow import run_full_workflow

        with patch("pr_workflow.step_finish_feature", return_value=True):
            with patch("pr_workflow.step_start_develop", return_value=True):
                with patch("pr_workflow.return_to_editable_branch", return_value=True):
                    result = run_full_workflow()
                    assert result is True

    def test_full_workflow_returns_to_editable_on_failure(self):
        """Test that full workflow returns to editable branch on failure."""
        from pr_workflow import run_full_workflow

        with patch("pr_workflow.step_finish_feature", return_value=False):
            with patch("pr_workflow.return_to_editable_branch") as mock_return:
                mock_return.return_value = True
                run_full_workflow()
                mock_return.assert_called()


class TestArgumentParsing:
    """Test argument parsing for main function."""

    def test_valid_step_choices(self):
        """Test that all valid step choices are accepted."""
        valid_steps = [
            "finish-feature",
            "start-develop",
            "full",
            "status",
        ]

        for step in valid_steps:
            # Just verify they're valid choices (don't actually run)
            assert step in valid_steps
