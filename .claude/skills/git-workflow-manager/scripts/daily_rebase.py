#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Perform daily rebase workflow.

Constants:
- TARGET_BRANCH: 'origin/develop'
  Rationale: All contrib branches rebase onto develop for integration

The --force-with-lease flag is used instead of --force for safety:
it only force-pushes if the remote branch hasn't changed since last fetch,
preventing accidental overwrites of others' work.
"""

import subprocess
import sys

# Constants with documented rationale
TARGET_BRANCH = "origin/develop"  # Integration branch for all contributions


def daily_rebase(contrib_branch):
    """
    Rebase contrib branch onto develop.

    Steps:
    1. Verify branch exists and no uncommitted changes
    2. Checkout contrib branch
    3. Fetch origin
    4. Rebase onto origin/develop
    5. Force push with lease (safe force push)

    Args:
        contrib_branch: Name of contrib branch (e.g., 'contrib/username')

    Returns:
        bool: True if successful, False if failed

    Raises:
        ValueError: If inputs are invalid
    """
    # Input validation
    if not contrib_branch or not contrib_branch.startswith("contrib/"):
        raise ValueError(
            f"Invalid contrib branch '{contrib_branch}'. "
            f"Must start with 'contrib/' (e.g., 'contrib/username')"
        )

    print(f"Rebasing {contrib_branch} onto develop...", file=sys.stderr)

    # Check for uncommitted changes
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
        )
        if result.stdout.strip():
            print(
                "ERROR: You have uncommitted changes. Please commit or stash them first.",
                file=sys.stderr,
            )
            print("\nUncommitted changes:", file=sys.stderr)
            print(result.stdout, file=sys.stderr)
            return False
    except subprocess.CalledProcessError as e:
        print("ERROR: Failed to check git status", file=sys.stderr)
        print(f"Git error: {e.stderr}", file=sys.stderr)
        return False

    # Verify contrib branch exists
    try:
        subprocess.run(
            ["git", "rev-parse", "--verify", contrib_branch], capture_output=True, check=True
        )
    except subprocess.CalledProcessError:
        print(f"ERROR: Branch '{contrib_branch}' does not exist", file=sys.stderr)
        print("\nAvailable contrib branches:", file=sys.stderr)
        subprocess.run(["git", "branch", "--list", "contrib/*"], check=False)
        return False

    try:
        # Checkout contrib branch
        print(f"Checking out {contrib_branch}...", file=sys.stderr)
        subprocess.run(["git", "checkout", contrib_branch], check=True, capture_output=True)

        # Fetch latest from origin
        print("Fetching from origin...", file=sys.stderr)
        subprocess.run(["git", "fetch", "origin"], check=True, capture_output=True)

        # DIVERGENCE CHECK: Ensure local and remote are not diverged
        # This prevents creating parallel histories when multiple sessions run rebase
        print("Checking for divergence...", file=sys.stderr)
        div_result = subprocess.run(
            [
                "git",
                "rev-list",
                "--left-right",
                "--count",
                f"{contrib_branch}...origin/{contrib_branch}",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if div_result.returncode == 0:
            counts = div_result.stdout.strip().split()
            if len(counts) == 2:
                local_ahead, remote_ahead = int(counts[0]), int(counts[1])
                if local_ahead > 0 and remote_ahead > 0:
                    print(
                        f"✗ DIVERGENCE DETECTED: {contrib_branch} has diverged from origin",
                        file=sys.stderr,
                    )
                    print(f"  Local has {local_ahead} commits not on remote", file=sys.stderr)
                    print(f"  Remote has {remote_ahead} commits not on local", file=sys.stderr)
                    print("\n  To resolve, choose one of:", file=sys.stderr)
                    print(
                        f"    1. Accept remote: git reset --hard origin/{contrib_branch}",
                        file=sys.stderr,
                    )
                    print(
                        f"    2. Force push local: git push --force-with-lease origin {contrib_branch}",
                        file=sys.stderr,
                    )
                    print(
                        "    3. Merge: git pull --no-rebase (creates merge commit)", file=sys.stderr
                    )
                    return False
                elif remote_ahead > 0:
                    # Remote is ahead - pull before rebase to avoid divergence
                    print(
                        f"  Remote is {remote_ahead} commits ahead, pulling first...",
                        file=sys.stderr,
                    )
                    pull_result = subprocess.run(
                        ["git", "pull", "--rebase", "origin", contrib_branch],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    if pull_result.returncode != 0:
                        print(f"✗ Pull failed: {pull_result.stderr}", file=sys.stderr)
                        print("  Resolve manually, then retry.", file=sys.stderr)
                        return False
                    print("  ✓ Synced with remote", file=sys.stderr)

        # Rebase onto origin/develop
        print(f"Rebasing onto {TARGET_BRANCH}...", file=sys.stderr)
        result = subprocess.run(
            ["git", "rebase", TARGET_BRANCH], check=True, capture_output=True, text=True
        )

        # Force push with lease (safe force push - only pushes if remote hasn't changed)
        print("Pushing to origin...", file=sys.stderr)
        subprocess.run(
            ["git", "push", "origin", contrib_branch, "--force-with-lease"],
            check=True,
            capture_output=True,
        )

        print(f"✓ {contrib_branch} successfully rebased onto develop", file=sys.stderr)
        return True

    except subprocess.CalledProcessError as e:
        print("✗ Rebase failed", file=sys.stderr)
        if e.stderr:
            print(f"\nGit error: {e.stderr.strip()}", file=sys.stderr)

        print("\nTo resolve conflicts:", file=sys.stderr)
        print("  1. Fix conflicts in affected files", file=sys.stderr)
        print("  2. git add <resolved-files>", file=sys.stderr)
        print("  3. git rebase --continue", file=sys.stderr)
        print(f"  4. git push origin {contrib_branch} --force-with-lease", file=sys.stderr)
        print("\nOr to abort the rebase:", file=sys.stderr)
        print("  git rebase --abort", file=sys.stderr)
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: daily_rebase.py <contrib_branch>", file=sys.stderr)
        print("\nExample: daily_rebase.py contrib/johndoe", file=sys.stderr)
        print("\nThis rebases your contrib branch onto origin/develop.", file=sys.stderr)
        sys.exit(1)

    try:
        success = daily_rebase(sys.argv[1])
        sys.exit(0 if success else 1)
    except ValueError as e:
        print(f"\n{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        sys.exit(1)
