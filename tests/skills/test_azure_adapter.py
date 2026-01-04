# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for Azure DevOps VCS adapter.

Tests the azure_adapter.py module which provides Azure DevOps CLI operations.
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
from vcs.azure_adapter import AZURE_CLI, AzureDevOpsAdapter  # noqa: E402


class TestAzureDevOpsAdapterInit:
    """Test AzureDevOpsAdapter initialization."""

    def test_init_with_all_params(self):
        """Test initialization with all parameters."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
            repository="myrepo",
        )
        assert adapter.organization == "https://dev.azure.com/myorg"
        assert adapter.project == "myproject"
        assert adapter.repository == "myrepo"

    def test_init_repository_defaults_to_project(self):
        """Test that repository defaults to project name."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        assert adapter.repository == "myproject"

    def test_init_repository_none_defaults_to_project(self):
        """Test that None repository defaults to project name."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
            repository=None,
        )
        assert adapter.repository == "myproject"

    def test_init_repository_empty_defaults_to_project(self):
        """Test that empty repository defaults to project name."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
            repository="",
        )
        assert adapter.repository == "myproject"

    def test_init_strips_whitespace(self):
        """Test that whitespace is stripped from parameters."""
        adapter = AzureDevOpsAdapter(
            organization="  https://dev.azure.com/myorg  ",
            project="  myproject  ",
            repository="  myrepo  ",
        )
        assert adapter.organization == "https://dev.azure.com/myorg"
        assert adapter.project == "myproject"
        assert adapter.repository == "myrepo"

    def test_init_raises_on_empty_organization(self):
        """Test that ValueError is raised for empty organization."""
        with pytest.raises(ValueError) as exc_info:
            AzureDevOpsAdapter(organization="", project="myproject")
        assert "organization is required" in str(exc_info.value)

    def test_init_raises_on_none_organization(self):
        """Test that ValueError is raised for None organization."""
        with pytest.raises(ValueError) as exc_info:
            AzureDevOpsAdapter(organization=None, project="myproject")
        assert "organization is required" in str(exc_info.value)

    def test_init_raises_on_empty_project(self):
        """Test that ValueError is raised for empty project."""
        with pytest.raises(ValueError) as exc_info:
            AzureDevOpsAdapter(organization="https://dev.azure.com/myorg", project="")
        assert "project is required" in str(exc_info.value)

    def test_init_raises_on_none_project(self):
        """Test that ValueError is raised for None project."""
        with pytest.raises(ValueError) as exc_info:
            AzureDevOpsAdapter(organization="https://dev.azure.com/myorg", project=None)
        assert "project is required" in str(exc_info.value)


class TestAzureDevOpsAdapterCheckAuthentication:
    """Test check_authentication method."""

    def test_returns_true_when_authenticated(self):
        """Test that True is returned when az account show succeeds."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = adapter.check_authentication()
            assert result is True
            # Verify correct command was called
            call_args = mock_run.call_args[0][0]
            assert AZURE_CLI in call_args
            assert "account" in call_args
            assert "show" in call_args

    def test_returns_false_when_not_authenticated(self):
        """Test that False is returned when az account show fails."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "az account show")
            result = adapter.check_authentication()
            assert result is False

    def test_returns_false_when_az_not_found(self):
        """Test that False is returned when az CLI is not installed."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("az not found")
            result = adapter.check_authentication()
            assert result is False

    def test_returns_false_on_timeout(self):
        """Test that False is returned on timeout."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("az", 10)
            result = adapter.check_authentication()
            assert result is False


class TestAzureDevOpsAdapterGetCurrentUser:
    """Test get_current_user method."""

    def test_returns_email(self):
        """Test that email is returned on success."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "user@example.com\n"
            result = adapter.get_current_user()
            assert result == "user@example.com"

    def test_raises_on_az_not_found(self):
        """Test that RuntimeError is raised when az is not installed."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.side_effect = FileNotFoundError("az not found")
            with pytest.raises(RuntimeError) as exc_info:
                adapter.get_current_user()
            assert "CLI not found" in str(exc_info.value)

    def test_raises_on_auth_failure(self):
        """Test that RuntimeError is raised on auth failure."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            error = subprocess.CalledProcessError(1, "az")
            error.stderr = "not logged in"
            mock_output.side_effect = error
            with pytest.raises(RuntimeError) as exc_info:
                adapter.get_current_user()
            assert "Failed to get Azure DevOps user" in str(exc_info.value)

    def test_raises_on_timeout(self):
        """Test that RuntimeError is raised on timeout."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.side_effect = subprocess.TimeoutExpired("az", 15)
            with pytest.raises(RuntimeError) as exc_info:
                adapter.get_current_user()
            assert "Timeout" in str(exc_info.value)


class TestAzureDevOpsAdapterCreatePullRequest:
    """Test create_pull_request method."""

    def test_creates_pr_successfully(self):
        """Test that PR URL is returned on success."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = (
                "https://dev.azure.com/myorg/myproject/_git/myproject/pullrequest/123\n"
            )
            result = adapter.create_pull_request(
                source_branch="feature/test",
                target_branch="main",
                title="Test PR",
                body="Test body",
            )
            assert "pullrequest/123" in result

    def test_calls_az_with_correct_args(self):
        """Test that az repos pr create is called with correct arguments."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = (
                "https://dev.azure.com/myorg/myproject/_git/myproject/pullrequest/123\n"
            )
            adapter.create_pull_request(
                source_branch="feature/test",
                target_branch="main",
                title="Test PR",
                body="Test body",
            )
            call_args = mock_output.call_args[0][0]
            assert AZURE_CLI in call_args
            assert "repos" in call_args
            assert "pr" in call_args
            assert "create" in call_args
            assert "--source-branch" in call_args
            assert "feature/test" in call_args
            assert "--target-branch" in call_args
            assert "main" in call_args
            assert "--title" in call_args
            assert "Test PR" in call_args
            assert "--description" in call_args
            assert "Test body" in call_args
            assert "--organization" in call_args
            assert "https://dev.azure.com/myorg" in call_args
            assert "--project" in call_args
            assert "myproject" in call_args

    def test_raises_on_az_not_found(self):
        """Test that RuntimeError is raised when az is not installed."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.side_effect = FileNotFoundError("az not found")
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
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            error = subprocess.CalledProcessError(1, "az")
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
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.side_effect = subprocess.TimeoutExpired("az", 30)
            with pytest.raises(RuntimeError) as exc_info:
                adapter.create_pull_request(
                    source_branch="feature/test",
                    target_branch="main",
                    title="Test PR",
                    body="Test body",
                )
            assert "Timeout" in str(exc_info.value)


class TestAzureDevOpsAdapterGetPRStatus:
    """Test get_pr_status method."""

    def test_returns_status_dict(self):
        """Test that status dictionary is returned on success."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = json.dumps(
                {
                    "status": "active",
                    "mergeStatus": "succeeded",
                    "reviewers": [{"vote": 10}],  # 10 = Approved
                }
            )
            result = adapter.get_pr_status(123)
            assert result["state"] == "active"
            assert result["mergeable"] is True
            assert result["approved"] is True
            assert result["reviews_required"] == 0

    def test_handles_not_approved(self):
        """Test handling of non-approved PRs."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = json.dumps(
                {
                    "status": "active",
                    "mergeStatus": "succeeded",
                    "reviewers": [{"vote": 0}],  # 0 = No vote
                }
            )
            result = adapter.get_pr_status(123)
            assert result["approved"] is False
            assert result["reviews_required"] == 1

    def test_handles_not_mergeable(self):
        """Test handling of non-mergeable PRs."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = json.dumps(
                {
                    "status": "active",
                    "mergeStatus": "conflicts",
                    "reviewers": [],
                }
            )
            result = adapter.get_pr_status(123)
            assert result["mergeable"] is False

    def test_raises_on_invalid_json(self):
        """Test that RuntimeError is raised on invalid JSON."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "not valid json"
            with pytest.raises(RuntimeError) as exc_info:
                adapter.get_pr_status(123)
            assert "Failed to parse" in str(exc_info.value)

    def test_raises_on_az_not_found(self):
        """Test that RuntimeError is raised when az is not installed."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.side_effect = FileNotFoundError("az not found")
            with pytest.raises(RuntimeError) as exc_info:
                adapter.get_pr_status(123)
            assert "CLI not found" in str(exc_info.value)


class TestAzureDevOpsAdapterFetchPRComments:
    """Test fetch_pr_comments method."""

    def test_returns_comments_list(self):
        """Test that comments list is returned on success."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = json.dumps(
                [
                    {
                        "comments": [
                            {
                                "author": {"displayName": "Reviewer 1"},
                                "content": "Looks good!",
                                "publishedDate": "2025-01-01T12:00:00Z",
                            }
                        ],
                        "threadContext": {
                            "filePath": "/src/main.py",
                            "rightFileStart": {"line": 42},
                        },
                    }
                ]
            )
            result = adapter.fetch_pr_comments(123)
            assert len(result) == 1
            assert result[0]["author"] == "Reviewer 1"
            assert result[0]["body"] == "Looks good!"
            assert result[0]["file"] == "/src/main.py"
            assert result[0]["line"] == 42

    def test_handles_empty_threads(self):
        """Test handling of PRs with no comment threads."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = json.dumps([])
            result = adapter.fetch_pr_comments(123)
            assert result == []

    def test_handles_missing_author(self):
        """Test handling of comments with missing author."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = json.dumps(
                [
                    {
                        "comments": [
                            {
                                "author": None,
                                "content": "Comment from deleted user",
                                "publishedDate": "2025-01-01T12:00:00Z",
                            }
                        ],
                        "threadContext": {},
                    }
                ]
            )
            result = adapter.fetch_pr_comments(123)
            assert result[0]["author"] == "Unknown"

    def test_raises_on_invalid_json(self):
        """Test that RuntimeError is raised on invalid JSON."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "not valid json"
            with pytest.raises(RuntimeError) as exc_info:
                adapter.fetch_pr_comments(123)
            assert "Failed to parse" in str(exc_info.value)


class TestAzureDevOpsAdapterUpdatePR:
    """Test update_pr method."""

    def test_updates_title(self):
        """Test updating PR title."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = ""
            adapter.update_pr(123, title="New Title")
            call_args = mock_output.call_args[0][0]
            assert "--title" in call_args
            assert "New Title" in call_args

    def test_updates_body(self):
        """Test updating PR body (description)."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = ""
            adapter.update_pr(123, body="New description")
            call_args = mock_output.call_args[0][0]
            assert "--description" in call_args
            assert "New description" in call_args

    def test_no_op_when_nothing_to_update(self):
        """Test that nothing happens when no updates provided."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            adapter.update_pr(123)  # No title or body
            mock_output.assert_not_called()

    def test_raises_on_update_failure(self):
        """Test that RuntimeError is raised on update failure."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        with patch("subprocess.check_output") as mock_output:
            error = subprocess.CalledProcessError(1, "az")
            error.stderr = "permission denied"
            mock_output.side_effect = error
            with pytest.raises(RuntimeError) as exc_info:
                adapter.update_pr(123, title="New Title")
            assert "Failed to update" in str(exc_info.value)


class TestAzureDevOpsAdapterGetProviderName:
    """Test get_provider_name method."""

    def test_returns_azure_devops(self):
        """Test that 'Azure DevOps' is returned."""
        adapter = AzureDevOpsAdapter(
            organization="https://dev.azure.com/myorg",
            project="myproject",
        )
        assert adapter.get_provider_name() == "Azure DevOps"
