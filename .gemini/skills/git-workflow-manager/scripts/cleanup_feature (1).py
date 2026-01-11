#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Cleanup feature worktree and branches.

This script cleans up after a feature is merged: Delete worktree -> Delete branches.

Constants:
- WORKTREE_PREFIX: '../{project}_feature_' or '../feature_'
  Rationale: Feature worktrees created by create_worktree.py use this pattern

Usage:
    python cleanup_feature.py <slug>
    python cleanup_feature.py <slug> --project-name <project>

Created: 2025-11-18
"""

import argparse
import subprocess
import sys
from pathlib import Path


def find_worktree(slug: str, project_name: str = None) -> Path:
    """Find worktree directory matching slug pattern.

    Args:
        slug: Feature slug
        project_name: Optional project name (e.g., 'german'). If None, uses generic pattern.

    Returns:
        Path to worktree directory, or None if not found
    """
    # Get repository root
    repo_root = Path(
        subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True, stderr=subprocess.PIPE
        ).strip()
    )

    # Try both project-specific and generic patterns
    patterns = []
    if project_name:
        patterns.append(repo_root.parent / f"{project_name}_feature_{slug}")
    patterns.append(repo_root.parent / f"feature_{slug}")

    for worktree_path in patterns:
        if worktree_path.exists():
            return worktree_path

    return None


def find_branch(slug: str) -> str:
    """Find branch name matching slug pattern.

    Args:
        slug: Feature slug

    Returns:
        Branch name (e.g., 'feature/20251118T115035Z_issue-243-todo-status')

    Raises:
        ValueError: If branch not found or multiple branches match
    """
    # List all local branches matching pattern
    result = subprocess.run(
        ["git", "branch", "--list", f"feature/*_{slug}"], capture_output=True, text=True, check=True
    )

    branches = [b.strip().lstrip("* ") for b in result.stdout.strip().split("\n") if b.strip()]

    if not branches:
        raise ValueError(f"No branch found for slug '{slug}'\nExpected pattern: feature/*_{slug}")

    if len(branches) > 1:
        raise ValueError(
            f"Multiple branches found for slug '{slug}':\n"
            + "\n".join(f"  - {b}" for b in branches)
        )

    return branches[0]


def delete_worktree(worktree_path: Path):
    """Delete worktree directory.

    Args:
        worktree_path: Path to worktree

    Raises:
        subprocess.CalledProcessError: If git worktree remove fails
    """
    print(f"[DEL]  Removing worktree: {worktree_path}")
    subprocess.run(["git", "worktree", "remove", str(worktree_path)], check=True)
    print(f"[OK] Worktree removed: {worktree_path}")


def delete_branch(branch_name: str):
    """Delete local and remote branches.

    Args:
        branch_name: Branch name (e.g., 'feature/20251118T115035Z_slug')

    Raises:
        subprocess.CalledProcessError: If git branch deletion fails
    """
    # Delete local branch
    print(f"[DEL]  Deleting local branch: {branch_name}")
    subprocess.run(["git", "branch", "-D", branch_name], check=True)
    print(f"[OK] Local branch deleted: {branch_name}")

    # Delete remote branch (if exists)
    print(f"[DEL]  Deleting remote branch: origin/{branch_name}")
    result = subprocess.run(
        ["git", "push", "origin", "--delete", branch_name], capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"[OK] Remote branch deleted: origin/{branch_name}")
    else:
        # Remote branch might not exist - not an error
        print(f"[INFO]  Remote branch not found (may have been deleted): origin/{branch_name}")


def cleanup_feature(slug: str, project_name: str = None):
    """Cleanup feature: delete worktree and branches.

    Args:
        slug: Feature slug
        project_name: Optional project name for worktree pattern

    Raises:
        ValueError: If branch not found or multiple matches
        subprocess.CalledProcessError: If any git operation fails
    """
    print(f"\n[GO] Cleaning up feature: {slug}")
    print("=" * 70)

    # Step 1: Find worktree (optional - may not exist)
    worktree_path = find_worktree(slug, project_name)
    if worktree_path:
        print(f"[OK] Found worktree: {worktree_path}")
    else:
        print("[INFO]  No worktree found (may have been deleted or work done on contrib directly)")

    # Step 2: Find branch (fail if missing)
    try:
        branch_name = find_branch(slug)
        print(f"[OK] Found branch: {branch_name}")
    except ValueError as e:
        print(f"\n[FAIL] ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 70)
    print("Starting cleanup operations...")
    print("=" * 70 + "\n")

    # Step 3: Delete worktree (if exists)
    if worktree_path:
        try:
            delete_worktree(worktree_path)
        except subprocess.CalledProcessError as e:
            print("\n[FAIL] ERROR: Failed to delete worktree", file=sys.stderr)
            print(f"   Path: {worktree_path}", file=sys.stderr)
            print(f"   Command failed: {e.cmd}", file=sys.stderr)
            print("\n[WARN]  Worktree NOT deleted", file=sys.stderr)
            print("   You can manually delete: git worktree remove", file=sys.stderr)
            sys.exit(1)

    # Step 4: Delete branches (local + remote)
    try:
        delete_branch(branch_name)
    except subprocess.CalledProcessError as e:
        print("\n[FAIL] ERROR: Failed to delete branch", file=sys.stderr)
        print(f"   Branch: {branch_name}", file=sys.stderr)
        print(f"   Command failed: {e.cmd}", file=sys.stderr)
        print("\n[WARN]  Worktree deleted, but branch NOT deleted", file=sys.stderr)
        print("   You can manually delete: git branch -D", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 70)
    print(f"[OK] Feature cleanup complete: {slug}")
    print("=" * 70)
    print("\nCleaned up:")
    if worktree_path:
        print(f"  [OK] Worktree deleted: {worktree_path}")
    print(f"  [OK] Local branch deleted: {branch_name}")
    print(f"  [OK] Remote branch deleted: origin/{branch_name}")
    print()


def main():
    """Parse arguments and execute cleanup."""
    parser = argparse.ArgumentParser(
        description="Cleanup feature: delete worktree and branches",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Cleanup feature
  python cleanup_feature.py auth-system

  # Cleanup feature with project-specific worktree pattern
  python cleanup_feature.py auth-system --project-name german

Notes:
  - Slug must match the slug used in create_worktree.py
  - Worktree pattern: ../feature_{slug}/ or ../{project}_feature_{slug}/
  - Branch pattern: feature/*_{slug}
""",
    )

    parser.add_argument("slug", help="Feature slug (e.g., auth-system, issue-243)")
    parser.add_argument(
        "--project-name", default=None, help="Project name for worktree pattern (e.g., german)"
    )

    args = parser.parse_args()

    cleanup_feature(slug=args.slug, project_name=args.project_name)


if __name__ == "__main__":
    main()
