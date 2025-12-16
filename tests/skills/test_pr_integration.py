# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Integration tests for PR workflow.

Tests end-to-end PR workflow scenarios including feature-to-contrib,
archive-todo, sync-agents, and contrib-to-develop steps.

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
class TestPRWorkflowIntegration:
    """Integration tests for PR workflow."""

    def test_full_pr_workflow_success(self):
        """Test complete PR workflow from feature to develop."""
        from pr_workflow import run_full_workflow

        with patch("pr_workflow.step_finish_feature", return_value=True):
            with patch("pr_workflow.step_archive_todo", return_value=True):
                with patch("pr_workflow.step_sync_agents", return_value=True):
                    with patch("pr_workflow.step_start_develop", return_value=True):
                        with patch("pr_workflow.return_to_editable_branch", return_value=True):
                            result = run_full_workflow()
                            assert result is True

    def test_pr_workflow_stops_on_first_failure(self):
        """Test that PR workflow stops on first step failure."""
        from pr_workflow import run_full_workflow

        with patch("pr_workflow.step_finish_feature", return_value=False):
            with patch("pr_workflow.step_archive_todo") as mock_archive:
                with patch("pr_workflow.return_to_editable_branch", return_value=True):
                    result = run_full_workflow()
                    assert result is False
                    mock_archive.assert_not_called()

    def test_pr_workflow_returns_to_editable_on_failure(self):
        """Test that workflow returns to editable branch on failure."""
        from pr_workflow import run_full_workflow

        with patch("pr_workflow.step_finish_feature", return_value=False):
            with patch("pr_workflow.return_to_editable_branch") as mock_return:
                mock_return.return_value = True
                run_full_workflow()
                mock_return.assert_called()


@pytest.mark.integration
class TestFeatureToContribIntegration:
    """Integration tests for feature-to-contrib step."""

    def test_feature_to_contrib_with_quality_gates(self):
        """Test feature-to-contrib PR with quality gates."""
        from pr_workflow import step_finish_feature

        with patch("pr_workflow.get_current_branch", return_value="feature/test"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch("pr_workflow.run_quality_gates", return_value=True):
                    with patch("pr_workflow.run_cmd") as mock_run:
                        mock_run.return_value = MagicMock(returncode=0, stderr="")
                        result = step_finish_feature()
                        assert result is True

    def test_feature_to_contrib_quality_gates_failure(self):
        """Test that quality gate failure blocks PR creation."""
        from pr_workflow import step_finish_feature

        with patch("pr_workflow.get_current_branch", return_value="feature/test"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch("pr_workflow.run_quality_gates", return_value=False):
                    result = step_finish_feature()
                    assert result is False


@pytest.mark.integration
class TestArchiveTodoIntegration:
    """Integration tests for TODO archiving."""

    def test_archive_todo_creates_directory(self):
        """Test that ARCHIVED directory is created."""
        from pr_workflow import step_archive_todo

        with patch("pr_workflow.Path.glob", return_value=[]):
            with patch.object(Path, "glob", return_value=[]):
                result = step_archive_todo()
                assert result is True

    def test_archive_todo_with_existing_files(self, tmp_path):
        """Test archiving existing TODO files."""
        from pr_workflow import step_archive_todo

        # Create a mock TODO file
        todo_file = tmp_path / "TODO_test.md"
        todo_file.write_text("# Test TODO")

        with patch("pr_workflow.Path.glob", return_value=[todo_file]):
            with patch("pr_workflow.Path.mkdir"):
                with patch("pr_workflow.shutil.move"):
                    with patch("pr_workflow.run_cmd") as mock_run:
                        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                        result = step_archive_todo()
                        assert result is True


@pytest.mark.integration
class TestSyncAgentsIntegration:
    """Integration tests for agent config syncing."""

    def test_sync_agents_with_module(self):
        """Test sync with sync_ai_config module available."""
        from pr_workflow import step_sync_agents

        mock_sync_module = MagicMock()
        mock_sync_module.sync_all.return_value = (True, True)
        with patch.dict(sys.modules, {"sync_ai_config": mock_sync_module}):
            with patch("pr_workflow.run_cmd") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                result = step_sync_agents()
                assert result is True

    def test_sync_agents_fallback(self):
        """Test sync with fallback when module not available."""
        from pr_workflow import step_sync_agents

        with patch.dict(sys.modules, {"sync_ai_config": None}):
            with patch("pr_workflow.Path.exists", return_value=True):
                with patch("pr_workflow.shutil.copy"):
                    with patch("pr_workflow.Path.mkdir"):
                        with patch("pr_workflow.Path.iterdir", return_value=[]):
                            with patch("pr_workflow.run_cmd") as mock_run:
                                mock_run.return_value = MagicMock(
                                    returncode=0, stdout="", stderr=""
                                )
                                result = step_sync_agents()
                                assert result is True


@pytest.mark.integration
class TestContribToDevelopIntegration:
    """Integration tests for contrib-to-develop step."""

    def test_contrib_to_develop_pr(self):
        """Test contrib-to-develop PR creation."""
        from pr_workflow import step_start_develop

        with patch("pr_workflow.get_current_branch", return_value="contrib/user"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch("pr_workflow.run_cmd") as mock_run:
                    mock_run.return_value = MagicMock(returncode=0, stderr="")
                    with patch("pr_workflow.return_to_editable_branch", return_value=True):
                        result = step_start_develop()
                        assert result is True

    def test_contrib_to_develop_switches_branch(self):
        """Test that workflow switches to contrib branch if needed."""
        from pr_workflow import step_start_develop

        with patch("pr_workflow.get_current_branch", return_value="main"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch("pr_workflow.run_cmd") as mock_run:
                    mock_run.return_value = MagicMock(returncode=0, stderr="")
                    with patch("pr_workflow.return_to_editable_branch", return_value=True):
                        step_start_develop()
                        # Verify checkout was called
                        checkout_calls = [
                            c for c in mock_run.call_args_list if "checkout" in str(c)
                        ]
                        assert len(checkout_calls) > 0


@pytest.mark.integration
class TestPRStatusIntegration:
    """Integration tests for PR workflow status."""

    def test_status_on_feature_branch(self):
        """Test status when on feature branch."""
        from pr_workflow import show_status

        with patch("pr_workflow.get_current_branch", return_value="feature/test"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch.object(Path, "glob", return_value=[]):
                    with patch.object(Path, "exists", return_value=True):
                        # Should run without error
                        show_status()

    def test_status_on_contrib_branch(self):
        """Test status when on contrib branch."""
        from pr_workflow import show_status

        with patch("pr_workflow.get_current_branch", return_value="contrib/user"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch.object(Path, "glob", return_value=[]):
                    with patch.object(Path, "exists", return_value=True):
                        # Should run without error
                        show_status()

    def test_status_with_todo_files(self):
        """Test status when TODO files exist."""
        from pr_workflow import show_status

        mock_todo = MagicMock()
        mock_todo.__str__ = lambda x: "TODO_test.md"

        with patch("pr_workflow.get_current_branch", return_value="contrib/user"):
            with patch("pr_workflow.get_contrib_branch", return_value="contrib/user"):
                with patch.object(Path, "glob", return_value=[mock_todo]):
                    with patch.object(Path, "exists", return_value=True):
                        # Should run without error
                        show_status()


@pytest.mark.integration
class TestQualityGatesInPRWorkflow:
    """Integration tests for quality gates in PR workflow."""

    def test_quality_gates_pass(self):
        """Test quality gates passing in PR workflow."""
        from pr_workflow import run_quality_gates

        with patch("pr_workflow.Path.exists", return_value=True):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                result = run_quality_gates()
                assert result is True

    def test_quality_gates_fail(self):
        """Test quality gates failing in PR workflow."""
        from pr_workflow import run_quality_gates

        with patch("pr_workflow.Path.exists", return_value=True):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=1)
                result = run_quality_gates()
                assert result is False

    def test_quality_gates_script_missing(self):
        """Test behavior when quality gates script is missing."""
        from pr_workflow import run_quality_gates

        with patch("pr_workflow.Path.exists", return_value=False):
            result = run_quality_gates()
            assert result is True  # Should skip and return True


@pytest.mark.integration
class TestBranchValidation:
    """Integration tests for branch validation."""

    def test_feature_branch_validation(self):
        """Test feature branch name validation."""
        from pr_workflow import get_current_branch

        with patch("pr_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="feature/20231201_test\n", returncode=0)
            branch = get_current_branch()
            assert branch.startswith("feature/")

    def test_contrib_branch_validation(self):
        """Test contrib branch name validation."""
        from pr_workflow import get_contrib_branch

        with patch("pr_workflow.run_cmd") as mock_run:
            mock_run.return_value = MagicMock(stdout="testuser\n", returncode=0)
            branch = get_contrib_branch()
            assert branch == "contrib/testuser"
            assert branch.startswith("contrib/")
