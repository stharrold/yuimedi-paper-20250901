# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Pytest configuration and shared fixtures."""

import os
from pathlib import Path

import pytest


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
