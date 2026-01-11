#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Verify workflow context - ensures commands run in correct location/branch.

This script validates that workflow commands are executed in the correct
context (main repo vs worktree, correct branch prefix).

For steps 5, 6, 7 (main repo steps), also detects pending worktrees with
unmerged commits and prints non-blocking warnings.

Usage:
    # Explicit flags
    python verify_workflow_context.py --require-main-repo --require-branch contrib/

    # Step shortcuts (recommended)
    python verify_workflow_context.py --step 1   # Main repo, contrib/*
    python verify_workflow_context.py --step 2   # Worktree, feature/*
    python verify_workflow_context.py --step 3   # Worktree, feature/*
    python verify_workflow_context.py --step 4   # Worktree, feature/*
    python verify_workflow_context.py --step 5   # Main repo, contrib/* + pending worktree check
    python verify_workflow_context.py --step 6   # Main repo, contrib/* + pending worktree check
    python verify_workflow_context.py --step 7   # Main repo, contrib/* + pending worktree check

Exit codes:
    0 - Context validation passed (pending worktree warnings are non-blocking)
    1 - Context validation failed
    2 - Pending worktrees detected in --strict mode (for CI enforcement)
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import TypedDict

# Safe cross-platform output
try:
    from .safe_output import format_check, format_cross, format_warning, safe_print
except ImportError:
    from safe_output import format_check, format_cross, format_warning, safe_print


class PendingWorktree(TypedDict):
    """Information about a pending worktree with unmerged commits."""

    worktree_path: str
    branch: str
    commits_ahead: int
    workflow_step: int | None
    prunable: bool
    error: str | None


# Step definitions: (require_worktree, require_main_repo, branch_prefix, step_name)
STEP_REQUIREMENTS = {
    1: (False, True, "contrib/", "/1_specify - Create feature spec"),
    2: (True, False, "feature/", "/2_plan - Generate specifications"),
    3: (True, False, "feature/", "/3_tasks - Validate task list"),
    4: (True, False, "feature/", "/4_implement - Execute tasks"),
    5: (False, True, "contrib/", "/5_integrate - Integrate feature"),
    6: (False, True, "contrib/", "/6_release - Create release"),
    7: (False, True, "contrib/", "/7_backmerge - Sync release"),
}


def run_command(cmd: list[str], cwd: Path | None = None) -> str | None:
    """Run command and return output or None on error."""
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None


def detect_pending_worktrees(repo_root: Path | None = None) -> list[PendingWorktree]:
    """Detect active worktrees with commits ahead of their base branch.

    Args:
        repo_root: Path to main repository root. If None, auto-detect.

    Returns:
        List of PendingWorktree dicts with worktree information.
    """
    if repo_root is None:
        root_str = run_command(["git", "rev-parse", "--show-toplevel"])
        if not root_str:
            return []
        repo_root = Path(root_str)

    # Get current branch of main repo (base for comparison)
    base_branch = run_command(["git", "branch", "--show-current"], cwd=repo_root)
    if not base_branch:
        return []

    # Parse git worktree list --porcelain
    result = run_command(["git", "worktree", "list", "--porcelain"], cwd=repo_root)
    if not result:
        return []

    pending: list[PendingWorktree] = []
    current_worktree: dict[str, str | bool] = {}

    for line in result.split("\n"):
        if line.startswith("worktree "):
            # Start of new worktree entry
            if current_worktree:
                # Process previous worktree
                wt = _process_worktree_entry(current_worktree, repo_root, base_branch)
                if wt:
                    pending.append(wt)
            current_worktree = {"path": line.split(" ", 1)[1]}
        elif line.startswith("branch refs/heads/"):
            current_worktree["branch"] = line.replace("branch refs/heads/", "")
        elif line == "prunable":
            current_worktree["prunable"] = True
        elif line == "bare":
            current_worktree["bare"] = True
        elif line == "detached":
            current_worktree["detached"] = True

    # Process last worktree entry
    if current_worktree:
        wt = _process_worktree_entry(current_worktree, repo_root, base_branch)
        if wt:
            pending.append(wt)

    return pending


def _process_worktree_entry(
    entry: dict[str, str | bool],
    repo_root: Path,
    base_branch: str,
) -> PendingWorktree | None:
    """Process a single worktree entry and check for pending commits.

    Args:
        entry: Parsed worktree entry with path, branch, etc.
        repo_root: Path to main repository root.
        base_branch: Base branch name for comparison.

    Returns:
        PendingWorktree dict if worktree has pending commits, None otherwise.
    """
    path = Path(str(entry.get("path", "")))
    branch = str(entry.get("branch", ""))
    prunable = bool(entry.get("prunable", False))

    # Skip main repo worktree
    if path.resolve() == repo_root.resolve():
        return None

    # Skip non-feature branches
    if not branch.startswith("feature/"):
        return None

    # Skip prunable worktrees (orphaned)
    if prunable:
        return PendingWorktree(
            worktree_path=str(path),
            branch=branch,
            commits_ahead=-1,
            workflow_step=None,
            prunable=True,
            error="Worktree is prunable (orphaned)",
        )

    # Count commits ahead of base branch
    commits_ahead = 0
    error = None
    try:
        count_result = subprocess.run(
            ["git", "rev-list", "--count", f"{base_branch}..{branch}"],
            check=True,
            capture_output=True,
            text=True,
            cwd=repo_root,
        )
        commits_ahead = int(count_result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError) as e:
        error = f"Could not count commits: {e}"
        commits_ahead = -1

    # Only return worktrees with commits ahead
    if commits_ahead <= 0 and not error:
        return None

    # Read workflow.json for step info
    workflow_step = None
    workflow_json = path / ".gemini-state" / "workflow.json"
    if workflow_json.exists():
        try:
            with open(workflow_json) as f:
                data = json.load(f)
                workflow_step = data.get("current_step")
        except (json.JSONDecodeError, OSError):
            # Ignore errors reading workflow.json - step info is optional metadata
            pass

    return PendingWorktree(
        worktree_path=str(path),
        branch=branch,
        commits_ahead=commits_ahead,
        workflow_step=workflow_step,
        prunable=prunable,
        error=error,
    )


def print_pending_worktree_warnings(pending: list[PendingWorktree]) -> None:
    """Print warnings about pending worktrees.

    Args:
        pending: List of PendingWorktree dicts to print warnings for.
    """
    safe_print("")
    safe_print("=" * 70)
    safe_print(format_warning("PENDING WORKTREES DETECTED"))
    safe_print("=" * 70)

    for wt in pending:
        safe_print("")
        safe_print(f"  Branch: {wt['branch']}")
        safe_print(f"  Path: {wt['worktree_path']}")

        if wt["commits_ahead"] >= 0:
            safe_print(f"  Commits ahead: {wt['commits_ahead']}")
        elif wt["error"]:
            safe_print(f"  Error: {wt['error']}")

        if wt["workflow_step"] is not None:
            step_name = STEP_REQUIREMENTS.get(
                wt["workflow_step"], (None, None, None, f"step {wt['workflow_step']}")
            )[3]
            safe_print(f"  Workflow step: {wt['workflow_step']} ({step_name})")

    safe_print("")
    safe_print("=" * 70)
    safe_print("These worktrees have unmerged commits.")
    safe_print("Consider running /5_integrate with the worktree path argument.")
    safe_print("=" * 70)


def get_repo_root() -> Path | None:
    """Get the git repository root."""
    result = run_command(["git", "rev-parse", "--show-toplevel"])
    return Path(result) if result else None


def get_current_branch() -> str | None:
    """Get current branch name."""
    return run_command(["git", "branch", "--show-current"])


def is_worktree() -> bool:
    """Check if current directory is a git worktree (not main repo)."""
    # Get the common git dir (shared across worktrees)
    git_common_dir = run_command(["git", "rev-parse", "--git-common-dir"])
    # Get the git dir for this worktree
    git_dir = run_command(["git", "rev-parse", "--git-dir"])

    if not git_common_dir or not git_dir:
        return False

    # In main repo: git_dir is ".git" and git_common_dir is ".git"
    # In worktree: git_dir is ".git" but git_common_dir points to main repo's .git
    # Normalize paths for comparison
    git_common_path = Path(git_common_dir).resolve()
    git_dir_path = Path(git_dir).resolve()

    # If they're different, we're in a worktree
    return git_common_path != git_dir_path


def validate_context(
    require_worktree: bool = False,
    require_main_repo: bool = False,
    branch_prefix: str | None = None,
    step: int | None = None,
) -> tuple[bool, str]:
    """Validate the current workflow context.

    Returns:
        (success, message) tuple
    """
    errors = []
    current_branch = get_current_branch()
    in_worktree = is_worktree()
    repo_root = get_repo_root()
    cwd = Path.cwd()

    # Build context info for messages
    context_info = f"Current: branch={current_branch}, "
    context_info += f"location={'worktree' if in_worktree else 'main repo'}"

    # Check worktree requirement
    if require_worktree and not in_worktree:
        errors.append(
            f"Must run from a WORKTREE directory, not main repo.\n"
            f"  Current directory: {cwd}\n"
            f"  Repository root: {repo_root}\n"
            f"  \n"
            f"  To switch to worktree, use:\n"
            f"    cd <worktree-directory>"
        )

    if require_main_repo and in_worktree:
        errors.append(
            f"Must run from MAIN REPO directory, not a worktree.\n"
            f"  Current directory: {cwd}\n"
            f"  Repository root: {repo_root}\n"
            f"  \n"
            f"  To switch to main repo, use:\n"
            f"    cd {repo_root}"
        )

    # Check branch prefix requirement
    if branch_prefix and current_branch:
        if not current_branch.startswith(branch_prefix):
            errors.append(
                f"Must be on a branch starting with '{branch_prefix}'.\n"
                f"  Current branch: {current_branch}\n"
                f"  \n"
                f"  To switch branches, use:\n"
                f"    git checkout <branch-name>"
            )
    elif branch_prefix and not current_branch:
        errors.append("Could not determine current branch (detached HEAD?)")

    if errors:
        error_msg = "\n\n".join(errors)
        return False, error_msg

    return True, context_info


def main():
    parser = argparse.ArgumentParser(
        description="Verify workflow context for slash commands",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Step shortcuts:
  --step 1   Main repo, contrib/*   (/1_specify)
  --step 2   Worktree, feature/*    (/2_plan)
  --step 3   Worktree, feature/*    (/3_tasks)
  --step 4   Worktree, feature/*    (/4_implement)
  --step 5   Main repo, contrib/*   (/5_integrate)
  --step 6   Main repo, contrib/*   (/6_release)
  --step 7   Main repo, release/*   (/7_backmerge)
""",
    )

    parser.add_argument(
        "--step",
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7],
        help="Workflow step number (uses predefined requirements)",
    )
    parser.add_argument(
        "--require-worktree",
        action="store_true",
        help="Require execution from a worktree directory",
    )
    parser.add_argument(
        "--require-main-repo",
        action="store_true",
        help="Require execution from main repo (not worktree)",
    )
    parser.add_argument(
        "--require-branch",
        type=str,
        metavar="PREFIX",
        help="Require branch name to start with PREFIX",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Only output on failure",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 2 if pending worktrees are detected (for CI enforcement)",
    )

    args = parser.parse_args()

    # Resolve step shortcut
    if args.step:
        require_worktree, require_main_repo, branch_prefix, step_name = STEP_REQUIREMENTS[args.step]
    else:
        require_worktree = args.require_worktree
        require_main_repo = args.require_main_repo
        branch_prefix = args.require_branch
        step_name = None

    # Validate conflicting options
    if require_worktree and require_main_repo:
        print("ERROR: Cannot require both worktree and main repo", file=sys.stderr)
        sys.exit(1)

    # Run validation
    success, message = validate_context(
        require_worktree=require_worktree,
        require_main_repo=require_main_repo,
        branch_prefix=branch_prefix,
        step=args.step,
    )

    if success:
        if not args.quiet:
            if step_name:
                safe_print(format_check(f"Context valid for {step_name}"))
            else:
                safe_print(format_check("Context valid"))
            safe_print(f"  {message}")

        # Detect pending worktrees for steps 5, 6, 7 (main repo steps)
        if args.step in (5, 6, 7):
            pending = detect_pending_worktrees()
            pending_with_commits = [w for w in pending if w["commits_ahead"] > 0]
            if pending_with_commits:
                print_pending_worktree_warnings(pending_with_commits)
                # In strict mode, exit with code 2 for CI enforcement
                if args.strict:
                    safe_print("")
                    safe_print(format_cross("STRICT MODE: Pending worktrees block release"))
                    safe_print("Use --no-strict or resolve pending worktrees before proceeding.")
                    sys.exit(2)

        sys.exit(0)
    else:
        safe_print("=" * 70)
        safe_print(format_cross("WORKFLOW CONTEXT VALIDATION FAILED"))
        safe_print("=" * 70)
        if step_name:
            safe_print(f"\nStep: {step_name}")
        safe_print(f"\n{message}")
        safe_print("\n" + "=" * 70)
        safe_print("STOP: Fix the context issue above before proceeding.")
        safe_print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
