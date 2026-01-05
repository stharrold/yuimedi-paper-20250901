#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Create feature/release/hotfix worktree for isolated development.

Constants:
- TIMESTAMP_FORMAT: YYYYMMDDTHHMMSSZ (compact ISO8601)
  Rationale: Compact format that remains intact when branch names are parsed
  by underscores and hyphens. No colons/hyphens avoid shell escaping issues.

Note: TODO file generation is removed. Use GitHub Issues for task tracking.
"""

import argparse
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

# Add workflow-utilities to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"))
from worktree_context import compute_worktree_id

# Constants with documented rationale
TIMESTAMP_FORMAT = "%Y%m%dT%H%M%SZ"  # Compact ISO8601 for filename/branch safety
VALID_WORKFLOW_TYPES = ["feature", "release", "hotfix"]  # Supported workflow types


def setup_agentdb_symlink(worktree_path: Path, main_repo_path: Path) -> bool:
    """Create link from worktree's agentdb.duckdb to main repo's database.

    Uses symlinks on Unix/macOS. On Windows, attempts symlink first (requires
    Developer Mode or admin), then falls back to hard link (works on same volume).

    This enables all worktrees to share a unified AgentDB, allowing cross-session
    visibility of workflow state.

    Args:
        worktree_path: Path to the newly created worktree
        main_repo_path: Path to the main repository (source of AgentDB)

    Returns:
        True if link created successfully, False otherwise
    """
    worktree_state_dir = worktree_path / ".gemini-state"
    main_state_dir = main_repo_path / ".gemini-state"
    main_db_path = main_state_dir / "agentdb.duckdb"
    worktree_db_path = worktree_state_dir / "agentdb.duckdb"

    try:
        # Ensure main repo state directory exists
        main_state_dir.mkdir(parents=True, exist_ok=True)

        # Initialize main repo database if it doesn't exist
        if not main_db_path.exists():
            # Touch the file so link target exists
            main_db_path.touch()

        # Skip if link already exists (idempotent)
        if worktree_db_path.exists() or worktree_db_path.is_symlink():
            return True

        # Try symlink first (works on all platforms if permissions allow)
        try:
            relative_target = os.path.relpath(main_db_path, worktree_state_dir)
            worktree_db_path.symlink_to(relative_target)
            return True
        except (OSError, PermissionError) as symlink_error:
            # On Windows, symlink may fail without Developer Mode or admin
            if sys.platform == "win32":
                # Fall back to hard link (works on same volume without special perms)
                try:
                    os.link(main_db_path, worktree_db_path)
                    print(
                        "[INFO]  Using hard link for AgentDB (symlink requires Developer Mode)",
                        file=sys.stderr,
                    )
                    return True
                except OSError as hardlink_error:
                    # Hard link also failed (likely cross-volume)
                    print(
                        f"[WARN]  Could not create AgentDB link: symlink failed ({symlink_error}), hard link failed ({hardlink_error})",
                        file=sys.stderr,
                    )
                    return False
            else:
                # On Unix, symlink should work - if it fails, report and return False
                print(f"[WARN]  Could not create AgentDB symlink: {symlink_error}", file=sys.stderr)
                return False

    except (OSError, PermissionError) as e:
        print(f"[WARN]  Could not create AgentDB link: {e}", file=sys.stderr)
        return False


def create_worktree(workflow_type, slug, base_branch):
    """
    Create a worktree for feature/release/hotfix development.

    Args:
        workflow_type: 'feature' | 'release' | 'hotfix'
        slug: Short descriptive name (e.g., 'json-validator')
        base_branch: Branch to create from (e.g., 'contrib/username')

    Returns:
        dict with worktree_path, branch_name, state_dir

    Raises:
        ValueError: If inputs are invalid
        subprocess.CalledProcessError: If git/gh commands fail
        FileNotFoundError: If required tools are missing
    """
    # Input validation
    if workflow_type not in VALID_WORKFLOW_TYPES:
        raise ValueError(
            f"Invalid workflow_type '{workflow_type}'. Must be one of: {', '.join(VALID_WORKFLOW_TYPES)}"
        )

    if not slug or not slug.replace("-", "").replace("_", "").isalnum():
        raise ValueError(
            f"Invalid slug '{slug}'. Must contain only letters, numbers, hyphens, and underscores."
        )

    # Use timezone-aware datetime (datetime.utcnow() is deprecated in Python 3.12+)
    timestamp = datetime.now(UTC).strftime(TIMESTAMP_FORMAT)
    branch_name = f"{workflow_type}/{timestamp}_{slug}"

    # Get repository root
    try:
        repo_root = Path(
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"], text=True, stderr=subprocess.PIPE
            ).strip()
        )
    except subprocess.CalledProcessError as e:
        print("ERROR: Not in a git repository", file=sys.stderr)
        print(f"Git error: {e.stderr.strip()}", file=sys.stderr)
        raise

    # Verify base branch exists
    try:
        subprocess.run(
            ["git", "rev-parse", "--verify", base_branch],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        print(f"ERROR: Base branch '{base_branch}' does not exist", file=sys.stderr)
        print("Available branches:", file=sys.stderr)
        subprocess.run(["git", "branch", "-a"], stderr=subprocess.DEVNULL)
        raise

    worktree_path = repo_root.parent / f"{repo_root.name}_{workflow_type}_{timestamp}_{slug}"

    # Check if worktree path already exists
    if worktree_path.exists():
        raise FileExistsError(
            f"Worktree path already exists: {worktree_path}\nRemove it first with: git worktree remove {worktree_path}"
        )

    # Create worktree
    try:
        subprocess.run(
            ["git", "worktree", "add", str(worktree_path), "-b", branch_name, base_branch],
            check=True,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print("ERROR: Failed to create worktree", file=sys.stderr)
        print(
            f"Command: git worktree add {worktree_path} -b {branch_name} {base_branch}",
            file=sys.stderr,
        )
        print(f"Git error: {e.stderr.strip()}", file=sys.stderr)
        raise

    # Initialize .gemini-state/ directory in new worktree
    state_dir = worktree_path / ".gemini-state"
    try:
        state_dir.mkdir(exist_ok=True)
        # Create .gitignore in state dir
        (state_dir / ".gitignore").write_text("# Ignore all files in state directory\n*\n")
        # Create .worktree-id with hash of worktree path (using shared implementation)
        worktree_id = compute_worktree_id(worktree_path)
        (state_dir / ".worktree-id").write_text(worktree_id)
        print(f"[OK] State directory: {state_dir}")

        # Create symlink for shared AgentDB (repo_root is main repo)
        if setup_agentdb_symlink(worktree_path, repo_root):
            print(f"[OK] AgentDB symlink: {state_dir / 'agentdb.duckdb'} -> main repo")
        else:
            print("[INFO]  AgentDB: isolated (symlink creation failed)")
    except (OSError, PermissionError) as e:
        print(f"[WARN]  Could not create state directory: {e}", file=sys.stderr)

    print(f"[OK] Worktree created: {worktree_path}")
    print(f"[OK] Branch: {branch_name}")

    return {
        "worktree_path": str(worktree_path),
        "branch_name": branch_name,
        "state_dir": str(state_dir) if state_dir.exists() else None,
    }


def main():
    """Main entry point with argparse."""
    parser = argparse.ArgumentParser(
        description="Create feature/release/hotfix worktree",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create feature worktree
  python create_worktree.py feature my-feature contrib/stharrold

  # Create release worktree
  python create_worktree.py release v1.6.0 develop
""",
    )

    parser.add_argument("workflow_type", choices=VALID_WORKFLOW_TYPES, help="Workflow type")
    parser.add_argument("slug", help="Short descriptive name (e.g., my-feature, v1.6.0)")
    parser.add_argument(
        "base_branch", help="Branch to create from (e.g., contrib/username, develop)"
    )

    args = parser.parse_args()

    try:
        result = create_worktree(args.workflow_type, args.slug, args.base_branch)

        import json

        print(json.dumps(result))
    except (ValueError, FileExistsError) as e:
        print(f"\n{e}", file=sys.stderr)
        sys.exit(1)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Error already printed in function
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
