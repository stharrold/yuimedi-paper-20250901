# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Pytest fixtures for workflow skills tests.

Provides reusable fixtures for:
- Subprocess mocking (git, gh, az CLI commands)
- Temporary git repositories
- File system operations
- DuckDB mocking
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture
def mock_subprocess_run() -> Generator[MagicMock, None, None]:
    """Mock subprocess.run for testing CLI commands.

    Usage:
        def test_something(mock_subprocess_run):
            mock_subprocess_run.return_value = MagicMock(
                stdout="output",
                stderr="",
                returncode=0
            )
            # ... test code that calls subprocess.run
            mock_subprocess_run.assert_called_once()
    """
    with patch("subprocess.run") as mock:
        # Default successful return
        mock.return_value = MagicMock(
            stdout="",
            stderr="",
            returncode=0,
        )
        yield mock


@pytest.fixture
def mock_subprocess_check_output() -> Generator[MagicMock, None, None]:
    """Mock subprocess.check_output for testing CLI commands.

    Usage:
        def test_something(mock_subprocess_check_output):
            mock_subprocess_check_output.return_value = "output"
            # ... test code that calls subprocess.check_output
    """
    with patch("subprocess.check_output") as mock:
        mock.return_value = ""
        yield mock


@pytest.fixture
def temp_git_repo(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary git repository for testing.

    Creates a git repo with:
    - Initial commit
    - origin remote pointing to a bare repo

    Usage:
        def test_git_operations(temp_git_repo):
            # temp_git_repo is a Path to the repo root
            os.chdir(temp_git_repo)
            # ... run git operations
    """
    # Save original directory
    original_dir = Path.cwd()

    # Create bare "remote" repository
    bare_repo = tmp_path / "origin.git"
    bare_repo.mkdir()
    subprocess.run(["git", "init", "--bare"], cwd=bare_repo, check=True, capture_output=True)

    # Create working repository
    work_repo = tmp_path / "repo"
    work_repo.mkdir()

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=work_repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=work_repo,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=work_repo,
        check=True,
        capture_output=True,
    )

    # Create initial commit
    readme = work_repo / "README.md"
    readme.write_text("# Test Repository\n")
    subprocess.run(["git", "add", "README.md"], cwd=work_repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=work_repo,
        check=True,
        capture_output=True,
    )

    # Add remote
    subprocess.run(
        ["git", "remote", "add", "origin", str(bare_repo)],
        cwd=work_repo,
        check=True,
        capture_output=True,
    )

    # Push to remote
    subprocess.run(
        ["git", "push", "-u", "origin", "main"],
        cwd=work_repo,
        check=True,
        capture_output=True,
    )

    yield work_repo

    # Restore original directory
    os.chdir(original_dir)


@pytest.fixture
def temp_git_repo_with_tags(temp_git_repo: Path) -> Path:
    """Create a temporary git repository with version tags.

    Adds tags: v1.0.0, v1.1.0, v1.2.0

    Usage:
        def test_version_calculation(temp_git_repo_with_tags):
            # Repository has version tags
            result = calculate_next_version(...)
    """
    # Create commits and tags
    for version in ["v1.0.0", "v1.1.0", "v1.2.0"]:
        # Create a file for the commit
        file_path = temp_git_repo / f"file_{version}.txt"
        file_path.write_text(f"Version {version}\n")
        subprocess.run(
            ["git", "add", str(file_path)],
            cwd=temp_git_repo,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", f"Release {version}"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "tag", "-a", version, "-m", f"Version {version}"],
            cwd=temp_git_repo,
            check=True,
            capture_output=True,
        )

    return temp_git_repo


@pytest.fixture
def mock_duckdb() -> Generator[MagicMock, None, None]:
    """Mock DuckDB connection for testing AgentDB operations.

    Usage:
        def test_agentdb(mock_duckdb):
            mock_duckdb.return_value.execute.return_value.fetchall.return_value = []
            # ... test code that uses DuckDB
    """
    with patch("duckdb.connect") as mock:
        mock_conn = MagicMock()
        mock.return_value = mock_conn
        yield mock_conn


@pytest.fixture
def mock_github_cli() -> Generator[MagicMock, None, None]:
    """Mock GitHub CLI (gh) commands.

    Pre-configured responses for common gh commands.

    Usage:
        def test_github_operations(mock_github_cli):
            mock_github_cli.side_effect = github_cli_responses
            # ... test code that uses gh CLI
    """

    def github_cli_handler(cmd, **kwargs):
        """Handle gh CLI commands with mock responses."""
        result = MagicMock()
        result.returncode = 0
        result.stderr = ""

        if "auth" in cmd and "status" in cmd:
            result.stdout = "Logged in to github.com as testuser"
        elif "pr" in cmd and "create" in cmd:
            result.stdout = "https://github.com/user/repo/pull/123"
        elif "pr" in cmd and "view" in cmd:
            result.stdout = '{"state": "OPEN", "mergeable": "MERGEABLE"}'
        elif "api" in cmd and "user" in cmd:
            result.stdout = "testuser"
        else:
            result.stdout = ""

        return result

    with patch("subprocess.run") as mock:
        mock.side_effect = github_cli_handler
        yield mock


@pytest.fixture
def mock_azure_cli() -> Generator[MagicMock, None, None]:
    """Mock Azure CLI (az) commands.

    Pre-configured responses for common az commands.

    Usage:
        def test_azure_operations(mock_azure_cli):
            # ... test code that uses az CLI
    """

    def azure_cli_handler(cmd, **kwargs):
        """Handle az CLI commands with mock responses."""
        result = MagicMock()
        result.returncode = 0
        result.stderr = ""

        if "repos" in cmd and "pr" in cmd and "create" in cmd:
            result.stdout = '{"pullRequestId": 456, "url": "https://dev.azure.com/org/project/_git/repo/pullrequest/456"}'
        elif "account" in cmd and "show" in cmd:
            result.stdout = '{"name": "Test Subscription"}'
        else:
            result.stdout = ""

        return result

    with patch("subprocess.run") as mock:
        mock.side_effect = azure_cli_handler
        yield mock


@pytest.fixture
def skills_path() -> Path:
    """Get the path to the skills directory.

    Returns the absolute path to .claude/skills/ for importing modules.
    """
    return Path(__file__).parent.parent.parent / ".gemini" / "skills"


@pytest.fixture
def add_skills_to_path(skills_path: Path) -> Generator[None, None, None]:
    """Add skills directory to Python path for imports.

    Usage:
        def test_import_skill(add_skills_to_path):
            from workflow_utilities.scripts.vcs.provider import detect_from_remote
    """
    import sys

    # Add skills path
    sys.path.insert(0, str(skills_path))

    yield

    # Remove from path
    sys.path.remove(str(skills_path))


@pytest.fixture
def mock_git_remote_github() -> Generator[MagicMock, None, None]:
    """Mock git remote to return GitHub URL.

    Usage:
        def test_github_detection(mock_git_remote_github):
            provider = detect_from_remote()
            assert provider == VCSProvider.GITHUB
    """
    with patch("subprocess.run") as mock:
        result = MagicMock()
        result.stdout = "https://github.com/user/repo.git\n"
        result.returncode = 0
        mock.return_value = result
        yield mock


@pytest.fixture
def mock_git_remote_azure() -> Generator[MagicMock, None, None]:
    """Mock git remote to return Azure DevOps URL.

    Usage:
        def test_azure_detection(mock_git_remote_azure):
            provider = detect_from_remote()
            assert provider == VCSProvider.AZURE_DEVOPS
    """
    with patch("subprocess.run") as mock:
        result = MagicMock()
        result.stdout = "https://dev.azure.com/org/project/_git/repo\n"
        result.returncode = 0
        mock.return_value = result
        yield mock
