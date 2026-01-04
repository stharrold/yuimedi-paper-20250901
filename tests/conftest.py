# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Pytest configuration and shared fixtures."""

import os
import sys
from pathlib import Path

import pytest

# Add skills script directories to sys.path for test collection
_repo_root = Path(__file__).parent.parent
_skills_paths = [
    _repo_root / ".gemini" / "skills" / "workflow-utilities" / "scripts",
    _repo_root / ".gemini" / "skills" / "git-workflow-manager" / "scripts",
]
for _p in _skills_paths:
    if _p.exists() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


@pytest.fixture
def repo_root() -> Path:
    """Return the repository root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def skills_dir(repo_root: Path) -> Path:
    """Return the .gemini/skills directory."""
    return repo_root / ".gemini" / "skills"


@pytest.fixture
def test_data_dir() -> Path:
    """Return the test data directory."""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture(autouse=True)
def change_to_repo_root(repo_root: Path) -> None:
    """Change to repository root for all tests."""
    original_dir = os.getcwd()
    os.chdir(repo_root)
    yield
    os.chdir(original_dir)
