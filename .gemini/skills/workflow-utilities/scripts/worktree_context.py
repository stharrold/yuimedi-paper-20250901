#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Worktree-aware context detection and state management.

This module provides utilities for detecting whether code is running in a git
worktree vs the main repository, and managing per-worktree state directories.

All skills that need worktree-aware state should import from this module.

Usage:
    from worktree_context import get_worktree_context, get_state_dir, get_worktree_id

    # Get full context
    ctx = get_worktree_context()
    print(f"Running in: {ctx.worktree_root}")
    print(f"Is worktree: {ctx.is_worktree}")

    # Get state directory (creates if needed)
    state_dir = get_state_dir()
    db_path = state_dir / "agentdb.duckdb"

    # Get stable worktree ID
    worktree_id = get_worktree_id()
"""

from __future__ import annotations

import hashlib
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class WorktreeContext:
    """Context information about the current worktree/repository.

    Attributes:
        worktree_root: Absolute path to the worktree or repository root.
        git_common_dir: Path to the shared .git directory.
        is_worktree: True if running in a git worktree, False for main repo.
        worktree_id: Stable 12-character hex identifier for this worktree.
        branch_name: Current git branch name.
    """

    worktree_root: Path
    git_common_dir: Path
    is_worktree: bool
    worktree_id: str
    branch_name: str

    @property
    def state_dir(self) -> Path:
        """Get the path to the worktree-specific state directory."""
        return self.worktree_root / ".gemini-state"


def compute_worktree_id(path: Path) -> str:
    """Compute a stable worktree identifier for any path.

    Generates a 12-character hex string derived from the given path
    using SHA-256. This is the shared implementation used by both
    worktree detection and worktree creation.

    Args:
        path: The path to compute an ID for.

    Returns:
        12-character hex string.
    """
    return hashlib.sha256(str(path).encode()).hexdigest()[:12]


def get_worktree_context() -> WorktreeContext:
    """Detect the current worktree context.

    Detects whether code is running in a git worktree or the main repository,
    and returns context information including paths and identifiers.

    Returns:
        WorktreeContext with all detection results.

    Raises:
        RuntimeError: If not running in a git repository.
    """
    try:
        # Get worktree root (current working tree)
        worktree_root = Path(
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
        )

        # Get the common git directory (shared .git for worktrees)
        git_common_dir = Path(
            subprocess.check_output(
                ["git", "rev-parse", "--git-common-dir"],
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
        )

        # If git_common_dir is relative, make it absolute
        if not git_common_dir.is_absolute():
            git_common_dir = (worktree_root / git_common_dir).resolve()

        # Check if .git is a file (worktree) or directory (main repo)
        git_path = worktree_root / ".git"
        is_worktree = git_path.is_file()

        # Generate stable worktree ID from path hash
        worktree_id = compute_worktree_id(worktree_root)

        # Get current branch name
        try:
            branch_name = subprocess.check_output(
                ["git", "branch", "--show-current"],
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            # Handle detached HEAD
            if not branch_name:
                branch_name = subprocess.check_output(
                    ["git", "rev-parse", "--short", "HEAD"],
                    text=True,
                    stderr=subprocess.PIPE,
                ).strip()
        except subprocess.CalledProcessError:
            branch_name = "unknown"

        return WorktreeContext(
            worktree_root=worktree_root,
            git_common_dir=git_common_dir,
            is_worktree=is_worktree,
            worktree_id=worktree_id,
            branch_name=branch_name,
        )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Not in a git repository: {e.stderr if e.stderr else str(e)}") from e


def get_state_dir() -> Path:
    """Get the worktree-specific state directory, creating if needed.

    Creates the .gemini-state/ directory within the current worktree,
    along with standard files (.gitignore, .worktree-id).

    Returns:
        Path to the .gemini-state/ directory.

    Raises:
        RuntimeError: If not in a git repository.
        PermissionError: If cannot create the state directory.
    """
    ctx = get_worktree_context()
    state_dir = ctx.state_dir

    # Create directory if not exists
    state_dir.mkdir(exist_ok=True)

    # Create .gitignore if not exists
    gitignore_path = state_dir / ".gitignore"
    if not gitignore_path.exists():
        gitignore_path.write_text("# Ignore all files in state directory\n*\n")

    # Create or update .worktree-id (update if stale, e.g., container path changed)
    worktree_id_path = state_dir / ".worktree-id"
    current_id = ctx.worktree_id
    if not worktree_id_path.exists() or worktree_id_path.read_text().strip() != current_id:
        worktree_id_path.write_text(current_id)

    return state_dir


def get_worktree_id() -> str:
    """Get the stable worktree identifier.

    Returns a 12-character hex string that uniquely identifies this worktree.
    The ID is derived from the worktree root path using SHA-256.

    Returns:
        12-character hex string.

    Raises:
        RuntimeError: If not in a git repository.
    """
    ctx = get_worktree_context()
    return ctx.worktree_id


def get_agentdb_path() -> Path:
    """Get the path to the AgentDB database, resolving symlinks.

    Returns the resolved (actual) path to agentdb.duckdb, which ensures
    DuckDB locks the correct file even when accessed through a symlink.

    Returns:
        Resolved absolute path to agentdb.duckdb

    Raises:
        RuntimeError: If not in a git repository.

    Example:
        >>> # From worktree with symlinked AgentDB
        >>> db_path = get_agentdb_path()
        >>> print(db_path)
        /path/to/main-repo/.gemini-state/agentdb.duckdb
    """
    state_dir = get_state_dir()
    db_path = state_dir / "agentdb.duckdb"

    # Resolve symlink to get actual file path
    # This ensures DuckDB locks the correct file
    return db_path.resolve()


def get_main_repo_path() -> Path | None:
    """Get the main repository path when running from a worktree.

    For worktrees, git_common_dir points to the shared .git directory
    in the main repository. This function returns the parent of that
    directory (the main repo root).

    This is useful when a worktree needs to access files in the main repo
    that aren't included in the worktree itself (e.g., planning/ directory).

    Returns:
        Path to main repo root, or None if not in a worktree.

    Raises:
        RuntimeError: If not in a git repository.

    Example:
        >>> # From worktree at /path/to/repo_feature_my-feature
        >>> main_repo = get_main_repo_path()
        >>> print(main_repo)
        /path/to/repo
        >>> planning_dir = main_repo / "planning" / "my-feature"
    """
    ctx = get_worktree_context()

    if not ctx.is_worktree:
        return None

    # git_common_dir is the shared .git directory in the main repo
    # e.g., /path/to/main-repo/.git
    # Its parent is the main repo root
    return ctx.git_common_dir.parent


def cleanup_orphaned_state(repo_root: Path) -> list[Path]:
    """Find orphaned state directories from removed worktrees.

    Scans for .gemini-state/ directories that belong to worktrees
    that no longer exist. This function checks any directory in the
    parent folder that contains a .gemini-state/ subdirectory, regardless
    of naming convention.

    Args:
        repo_root: Main repository root path.

    Returns:
        List of orphaned state directory paths.
    """
    orphaned: list[Path] = []

    try:
        # Get list of active worktrees
        result = subprocess.check_output(
            ["git", "-C", str(repo_root), "worktree", "list", "--porcelain"],
            text=True,
            stderr=subprocess.PIPE,
        )

        # Parse active worktree paths
        active_worktree_paths: set[Path] = set()
        for line in result.strip().split("\n"):
            if line.startswith("worktree "):
                path = Path(line.split(" ", 1)[1])
                active_worktree_paths.add(path)

        # Check for state directories in parent directory of repo
        parent_dir = repo_root.parent

        # Look for any directories in the parent that contain a .gemini-state subdirectory
        # This handles worktrees created with any naming convention
        # Explicitly exclude repo_root to avoid marking main repo as orphaned
        for item in parent_dir.iterdir():
            if item.is_dir() and item != repo_root:
                state_dir = item / ".gemini-state"
                if state_dir.exists() and item not in active_worktree_paths:
                    orphaned.append(state_dir)

    except subprocess.CalledProcessError:
        # If git command fails, return empty list
        pass

    return orphaned


if __name__ == "__main__":
    # Quick test when run directly
    import sys

    try:
        ctx = get_worktree_context()
        print(f"Worktree root: {ctx.worktree_root}")
        print(f"Git common dir: {ctx.git_common_dir}")
        print(f"Is worktree: {ctx.is_worktree}")
        print(f"Worktree ID: {ctx.worktree_id}")
        print(f"Branch: {ctx.branch_name}")
        print(f"State dir: {ctx.state_dir}")

        state_dir = get_state_dir()
        print(f"\nState directory created/verified: {state_dir}")
        print(f"Contents: {list(state_dir.iterdir())}")

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
