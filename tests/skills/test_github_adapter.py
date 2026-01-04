# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for GitHub VCS adapter.

Tests the github_adapter.py module which provides GitHub CLI operations.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add skills script directories to sys.path
_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_root / ".gemini" / "skills" / "workflow-utilities" / "scripts"))
sys.path.insert(0, str(_root / ".gemini" / "skills" / "git-workflow-manager" / "scripts"))

import pytest  # noqa: E402
from vcs.github_adapter import GITHUB_CLI, GitHubAdapter  # noqa: E402


class TestGitHubAdapterCheckAuthentication:
    """Test check_authentication method."""

    def test_returns_true_when_authenticated(self):
        """Test that True is returned when gh auth status succeeds."""
        adapter = GitHubAdapter()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = adapter.check_authentication()
            assert result is True
            mock_run.assert_called_once()
            # Verify correct command was called
            call_args = mock_run.call_args[0][0]
            assert GITHUB_CLI in call_args
            assert "auth" in call_args
            assert "status" in call_args

    def test_returns_false_when_not_authenticated(self):
        """Test that False is returned when gh auth status fails."""
        adapter = GitHubAdapter()
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "gh auth status")
            result = adapter.check_authentication()
            assert result is False

    def test_returns_false_when_gh_not_found(self):
        """Test that False is returned when gh CLI is not installed."""
        adapter = GitHubAdapter()
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("gh not found")
            result = adapter.check_authentication()
            assert result is False

    def test_returns_false_on_timeout(self):
        """Test that False is returned on timeout."""
        adapter = GitHubAdapter()
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("gh", 10)
            result = adapter.check_authentication()
            assert result is False


class TestGitHubAdapterGetCurrentUser:
    """Test get_current_user method."""

    def test_returns_username(self):
        """Test that username is returned on success."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "testuser\n"
            result = adapter.get_current_user()
            assert result == "testuser"

    def test_raises_on_gh_not_found(self):
        """Test that RuntimeError is raised when gh is not installed."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.side_effect = FileNotFoundError("gh not found")
            with pytest.raises(RuntimeError) as exc_info:
                adapter.get_current_user()
            assert "CLI not found" in str(exc_info.value)

    def test_raises_on_auth_failure(self):
        """Test that RuntimeError is raised on auth failure."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            error = subprocess.CalledProcessError(1, "gh")
            error.stderr = "not authenticated"
            mock_output.side_effect = error
            with pytest.raises(RuntimeError) as exc_info:
                adapter.get_current_user()
            assert "Failed to get GitHub username" in str(exc_info.value)

    def test_raises_on_timeout(self):
        """Test that RuntimeError is raised on timeout."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.side_effect = subprocess.TimeoutExpired("gh", 10)
            with pytest.raises(RuntimeError) as exc_info:
                adapter.get_current_user()
            assert "Timeout" in str(exc_info.value)


class TestGitHubAdapterCreatePullRequest:
    """Test create_pull_request method."""

    def test_creates_pr_successfully(self):
        """Test that PR URL is returned on success."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "https://github.com/user/repo/pull/123\n"
            result = adapter.create_pull_request(
                source_branch="feature/test",
                target_branch="main",
                title="Test PR",
                body="Test body",
            )
            assert result == "https://github.com/user/repo/pull/123"

    def test_calls_gh_with_correct_args(self):
        """Test that gh pr create is called with correct arguments."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "https://github.com/user/repo/pull/123\n"
            adapter.create_pull_request(
                source_branch="feature/test",
                target_branch="main",
                title="Test PR",
                body="Test body",
            )
            call_args = mock_output.call_args[0][0]
            assert GITHUB_CLI in call_args
            assert "pr" in call_args
            assert "create" in call_args
            assert "--base" in call_args
            assert "main" in call_args
            assert "--head" in call_args
            assert "feature/test" in call_args
            assert "--title" in call_args
            assert "Test PR" in call_args
            assert "--body" in call_args
            assert "Test body" in call_args

    def test_raises_on_gh_not_found(self):
        """Test that RuntimeError is raised when gh is not installed."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.side_effect = FileNotFoundError("gh not found")
            with pytest.raises(RuntimeError) as exc_info:
                adapter.create_pull_request(
                    source_branch="feature/test",
                    target_branch="main",
                    title="Test PR",
                    body="Test body",
                )
            assert "CLI not found" in str(exc_info.value)

    def test_raises_on_pr_creation_failure(self):
        """Test that RuntimeError is raised when PR creation fails."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            error = subprocess.CalledProcessError(1, "gh")
            error.stderr = "pull request already exists"
            mock_output.side_effect = error
            with pytest.raises(RuntimeError) as exc_info:
                adapter.create_pull_request(
                    source_branch="feature/test",
                    target_branch="main",
                    title="Test PR",
                    body="Test body",
                )
            assert "Failed to create" in str(exc_info.value)

    def test_raises_on_timeout(self):
        """Test that RuntimeError is raised on timeout."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.side_effect = subprocess.TimeoutExpired("gh", 30)
            with pytest.raises(RuntimeError) as exc_info:
                adapter.create_pull_request(
                    source_branch="feature/test",
                    target_branch="main",
                    title="Test PR",
                    body="Test body",
                )
            assert "Timeout" in str(exc_info.value)


class TestGitHubAdapterGetPRStatus:
    """Test get_pr_status method."""

    def test_returns_status_dict(self):
        """Test that status dictionary is returned on success."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = json.dumps(
                {
                    "state": "OPEN",
                    "mergeable": "MERGEABLE",
                    "reviewDecision": "APPROVED",
                }
            )
            result = adapter.get_pr_status(123)
            assert result["state"] == "open"
            assert result["mergeable"] is True
            assert result["approved"] is True
            assert result["reviews_required"] == 0

    def test_handles_not_approved(self):
        """Test handling of non-approved PRs."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = json.dumps(
                {
                    "state": "OPEN",
                    "mergeable": "MERGEABLE",
                    "reviewDecision": "CHANGES_REQUESTED",
                }
            )
            result = adapter.get_pr_status(123)
            assert result["approved"] is False
            assert result["reviews_required"] == 1

    def test_handles_not_mergeable(self):
        """Test handling of non-mergeable PRs."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = json.dumps(
                {
                    "state": "OPEN",
                    "mergeable": "CONFLICTING",
                    "reviewDecision": None,
                }
            )
            result = adapter.get_pr_status(123)
            assert result["mergeable"] is False

    def test_raises_on_invalid_json(self):
        """Test that RuntimeError is raised on invalid JSON."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "not valid json"
            with pytest.raises(RuntimeError) as exc_info:
                adapter.get_pr_status(123)
            assert "Failed to parse" in str(exc_info.value)

    def test_raises_on_gh_not_found(self):
        """Test that RuntimeError is raised when gh is not installed."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.side_effect = FileNotFoundError("gh not found")
            with pytest.raises(RuntimeError) as exc_info:
                adapter.get_pr_status(123)
            assert "CLI not found" in str(exc_info.value)


class TestGitHubAdapterFetchPRComments:
    """Test fetch_pr_comments method."""

    def test_returns_comments_list(self):
        """Test that comments list is returned on success."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = json.dumps(
                {
                    "reviews": [
                        {
                            "author": {"login": "reviewer1"},
                            "body": "Looks good!",
                            "submittedAt": "2025-01-01T12:00:00Z",
                        }
                    ],
                    "comments": [
                        {
                            "author": {"login": "commenter1"},
                            "body": "Question about this",
                            "createdAt": "2025-01-01T13:00:00Z",
                        }
                    ],
                }
            )
            result = adapter.fetch_pr_comments(123)
            assert len(result) == 2
            assert result[0]["author"] == "reviewer1"
            assert result[0]["body"] == "Looks good!"
            assert result[1]["author"] == "commenter1"

    def test_handles_empty_reviews(self):
        """Test handling of PRs with no reviews."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = json.dumps({"reviews": [], "comments": []})
            result = adapter.fetch_pr_comments(123)
            assert result == []

    def test_handles_missing_author(self):
        """Test handling of comments with missing author (Ghost)."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = json.dumps(
                {
                    "reviews": [],
                    "comments": [
                        {
                            "author": None,
                            "body": "Comment from deleted user",
                            "createdAt": "2025-01-01T12:00:00Z",
                        }
                    ],
                }
            )
            result = adapter.fetch_pr_comments(123)
            assert result[0]["author"] == "Ghost"

    def test_raises_on_invalid_json(self):
        """Test that RuntimeError is raised on invalid JSON."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "not valid json"
            with pytest.raises(RuntimeError) as exc_info:
                adapter.fetch_pr_comments(123)
            assert "Failed to parse" in str(exc_info.value)


class TestGitHubAdapterUpdatePR:
    """Test update_pr method."""

    def test_updates_title(self):
        """Test updating PR title."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = ""
            adapter.update_pr(123, title="New Title")
            call_args = mock_output.call_args[0][0]
            assert "--title" in call_args
            assert "New Title" in call_args

    def test_updates_body(self):
        """Test updating PR body."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = ""
            adapter.update_pr(123, body="New body content")
            call_args = mock_output.call_args[0][0]
            assert "--body" in call_args
            assert "New body content" in call_args

    def test_updates_both_title_and_body(self):
        """Test updating both title and body."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = ""
            adapter.update_pr(123, title="New Title", body="New body")
            call_args = mock_output.call_args[0][0]
            assert "--title" in call_args
            assert "--body" in call_args

    def test_no_op_when_nothing_to_update(self):
        """Test that nothing happens when no updates provided."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            adapter.update_pr(123)  # No title or body
            mock_output.assert_not_called()

    def test_raises_on_update_failure(self):
        """Test that RuntimeError is raised on update failure."""
        adapter = GitHubAdapter()
        with patch("subprocess.check_output") as mock_output:
            error = subprocess.CalledProcessError(1, "gh")
            error.stderr = "permission denied"
            mock_output.side_effect = error
            with pytest.raises(RuntimeError) as exc_info:
                adapter.update_pr(123, title="New Title")
            assert "Failed to update" in str(exc_info.value)


class TestGitHubAdapterGetProviderName:
    """Test get_provider_name method."""

    def test_returns_github(self):
        """Test that 'GitHub' is returned."""
        adapter = GitHubAdapter()
        assert adapter.get_provider_name() == "GitHub"
