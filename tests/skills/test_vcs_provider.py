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
from unittest.mock import patch

# Add skills script directories to sys.path
_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_root / ".claude" / "skills" / "workflow-utilities" / "scripts"))
sys.path.insert(0, str(_root / ".claude" / "skills" / "git-workflow-manager" / "scripts"))

import pytest  # noqa: E402
from vcs.provider import (  # noqa: E402
    VCSProvider,
    detect_provider,
)


class TestVCSProviderEnum:
    """Test VCSProvider enumeration."""

    def test_github_value(self):
        """Test GitHub enum value."""
        assert VCSProvider.GITHUB.value == "github"

    def test_azure_devops_value(self):
        """Test Azure DevOps enum value."""
        assert VCSProvider.AZURE_DEVOPS.value == "azure_devops"


class TestDetectProviderGitHub:
    """Test detect_provider for GitHub URLs."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://github.com/user/repo.git",
            "https://github.com/user/repo",
            "git@github.com:user/repo.git",
        ],
    )
    def test_detect_github_urls(self, url: str):
        """Test detection of various GitHub URL formats."""
        import vcs.provider as mod

        mod._cached_provider = None  # Reset cache
        with patch("subprocess.check_output", return_value=url):
            result = detect_provider()
            assert result == VCSProvider.GITHUB
        mod._cached_provider = None  # Clean up


class TestDetectProviderAzure:
    """Test detect_provider for Azure DevOps URLs."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://dev.azure.com/org/project/_git/repo",
            "https://org.visualstudio.com/project/_git/repo",
        ],
    )
    def test_detect_azure_urls(self, url: str):
        """Test detection of various Azure DevOps URL formats."""
        import vcs.provider as mod

        mod._cached_provider = None
        with patch("subprocess.check_output", return_value=url):
            result = detect_provider()
            assert result == VCSProvider.AZURE_DEVOPS
        mod._cached_provider = None


class TestDetectProviderErrors:
    """Test error handling in provider detection."""

    def test_unknown_provider_raises_error(self):
        """Test that unknown providers raise RuntimeError."""
        import vcs.provider as mod

        mod._cached_provider = None
        with patch("subprocess.check_output", return_value="https://gitlab.com/user/repo.git"):
            with pytest.raises(RuntimeError, match="Unrecognised VCS provider"):
                detect_provider()
        mod._cached_provider = None

    def test_no_remote_raises_error(self):
        """Test handling when no remote is configured."""
        import vcs.provider as mod

        mod._cached_provider = None
        with patch(
            "subprocess.check_output",
            side_effect=subprocess.CalledProcessError(1, "git", stderr=""),
        ):
            with pytest.raises(RuntimeError, match="Failed to read"):
                detect_provider()
        mod._cached_provider = None

    def test_git_not_found_raises_error(self):
        """Test handling when git is not installed."""
        import vcs.provider as mod

        mod._cached_provider = None
        with patch("subprocess.check_output", side_effect=FileNotFoundError("git not found")):
            with pytest.raises(RuntimeError, match="git.*CLI not found"):
                detect_provider()
        mod._cached_provider = None

    def test_timeout_raises_error(self):
        """Test handling when git command times out."""
        import vcs.provider as mod

        mod._cached_provider = None
        with patch("subprocess.check_output", side_effect=subprocess.TimeoutExpired("git", 5)):
            with pytest.raises(RuntimeError, match="Timeout"):
                detect_provider()
        mod._cached_provider = None


class TestDetectProviderCaching:
    """Test that detect_provider caches results."""

    def test_uses_cached_provider(self):
        """Test that cached provider is returned without subprocess call."""
        import vcs.provider as mod

        mod._cached_provider = VCSProvider.GITHUB
        with patch("subprocess.check_output") as mock_check:
            result = detect_provider()
            assert result == VCSProvider.GITHUB
            mock_check.assert_not_called()
        mod._cached_provider = None
