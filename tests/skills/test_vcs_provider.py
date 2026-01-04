# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for VCS provider detection.

Tests the provider.py module which detects VCS providers (GitHub, Azure DevOps)
from git remote URLs.
"""

from __future__ import annotations

import subprocess
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
        / "workflow-utilities"
        / "scripts"
    ),
)

from vcs.provider import (
    AZURE_DEVOPS_PATTERNS,
    GITHUB_PATTERNS,
    VCSProvider,
    detect_from_remote,
    detect_provider,
    extract_azure_repo_from_remote,
)


class TestVCSProviderEnum:
    """Test VCSProvider enumeration."""

    def test_github_value(self):
        """Test GitHub enum value."""
        assert VCSProvider.GITHUB.value == "github"

    def test_azure_devops_value(self):
        """Test Azure DevOps enum value."""
        assert VCSProvider.AZURE_DEVOPS.value == "azure_devops"


class TestGitHubURLDetection:
    """Test GitHub URL pattern detection."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://github.com/user/repo.git",
            "https://github.com/user/repo",
            "git@github.com:user/repo.git",
            "git@github.com:user/repo",
            "ssh://git@github.com/user/repo.git",
        ],
    )
    def test_detect_github_urls(self, url: str):
        """Test detection of various GitHub URL formats."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout=url + "\n",
                returncode=0,
            )
            result = detect_from_remote()
            assert result == VCSProvider.GITHUB

    def test_github_pattern_matches_expected(self):
        """Verify GitHub patterns match expected URLs."""
        import re

        test_urls = [
            "https://github.com/user/repo.git",
            "git@github.com:user/repo.git",
        ]
        for url in test_urls:
            matched = any(re.search(pattern, url) for pattern in GITHUB_PATTERNS)
            assert matched, f"Pattern should match: {url}"


class TestAzureDevOpsURLDetection:
    """Test Azure DevOps URL pattern detection."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://dev.azure.com/org/project/_git/repo",
            "https://dev.azure.com/org/project/_git/repo.git",
            "git@ssh.dev.azure.com:v3/org/project/repo",
            "https://org.visualstudio.com/project/_git/repo",
        ],
    )
    def test_detect_azure_urls(self, url: str):
        """Test detection of various Azure DevOps URL formats."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout=url + "\n",
                returncode=0,
            )
            result = detect_from_remote()
            assert result == VCSProvider.AZURE_DEVOPS

    def test_azure_pattern_matches_expected(self):
        """Verify Azure DevOps patterns match expected URLs."""
        import re

        test_urls = [
            "https://dev.azure.com/org/project/_git/repo",
            "git@ssh.dev.azure.com:v3/org/project/repo",
        ]
        for url in test_urls:
            matched = any(re.search(pattern, url) for pattern in AZURE_DEVOPS_PATTERNS)
            assert matched, f"Pattern should match: {url}"


class TestUnknownProvider:
    """Test handling of unknown/unsupported providers."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://gitlab.com/user/repo.git",
            "https://bitbucket.org/user/repo.git",
            "https://example.com/repo.git",
            "file:///path/to/repo",
        ],
    )
    def test_unknown_provider_returns_none(self, url: str):
        """Test that unknown providers return None."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout=url + "\n",
                returncode=0,
            )
            result = detect_from_remote()
            assert result is None


class TestErrorHandling:
    """Test error handling in provider detection."""

    def test_no_remote_returns_none(self):
        """Test handling when no remote is configured."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "git")
            result = detect_from_remote()
            assert result is None

    def test_git_not_found_returns_none(self):
        """Test handling when git is not installed."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("git not found")
            result = detect_from_remote()
            assert result is None

    def test_timeout_returns_none(self):
        """Test handling when git command times out."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("git", 5)
            result = detect_from_remote()
            assert result is None


class TestDetectProvider:
    """Test detect_provider function with fallback."""

    def test_returns_github_when_detected(self):
        """Test that GitHub is returned when detected."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="https://github.com/user/repo.git\n",
                returncode=0,
            )
            result = detect_provider()
            assert result == VCSProvider.GITHUB

    def test_returns_azure_when_detected(self):
        """Test that Azure DevOps is returned when detected."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="https://dev.azure.com/org/project/_git/repo\n",
                returncode=0,
            )
            result = detect_provider()
            assert result == VCSProvider.AZURE_DEVOPS

    def test_defaults_to_github_when_unknown(self):
        """Test that GitHub is returned as default for unknown providers."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="https://gitlab.com/user/repo.git\n",
                returncode=0,
            )
            result = detect_provider()
            assert result == VCSProvider.GITHUB

    def test_defaults_to_github_on_error(self):
        """Test that GitHub is returned as default on error."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "git")
            result = detect_provider()
            assert result == VCSProvider.GITHUB


class TestExtractAzureRepoFromRemote:
    """Test Azure DevOps repository name extraction."""

    @pytest.mark.parametrize(
        ("url", "expected_repo"),
        [
            ("https://dev.azure.com/org/project/_git/myrepo", "myrepo"),
            ("https://dev.azure.com/org/project/_git/myrepo.git", "myrepo"),
            ("git@ssh.dev.azure.com:v3/org/project/myrepo", "myrepo"),
            ("git@ssh.dev.azure.com:v3/org/project/myrepo.git", "myrepo"),
            ("https://org.visualstudio.com/project/_git/myrepo", "myrepo"),
        ],
    )
    def test_extract_repo_name(self, url: str, expected_repo: str):
        """Test extraction of repository name from Azure DevOps URLs."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout=url + "\n",
                returncode=0,
            )
            result = extract_azure_repo_from_remote()
            assert result == expected_repo

    def test_returns_none_for_non_azure_url(self):
        """Test that None is returned for non-Azure URLs."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="https://github.com/user/repo.git\n",
                returncode=0,
            )
            result = extract_azure_repo_from_remote()
            assert result is None

    def test_returns_none_on_error(self):
        """Test that None is returned on git error."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "git")
            result = extract_azure_repo_from_remote()
            assert result is None
