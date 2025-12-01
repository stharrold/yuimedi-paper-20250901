#!/usr/bin/env python3
"""Create feature/release/hotfix worktree with optional TODO file.

Constants:
- TIMESTAMP_FORMAT: YYYYMMDDTHHMMSSZ (compact ISO8601)
  Rationale: Compact format that remains intact when branch names are parsed
  by underscores and hyphens. No colons/hyphens avoid shell escaping issues.

Note: The --no-todo flag (default) skips TODO file creation since TODO*.md
files are deprecated in favor of GitHub Issues and specs/*/tasks.md.
"""

import argparse
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

# Add workflow-utilities to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"))
from vcs import get_vcs_adapter
from worktree_context import compute_worktree_id

# Constants with documented rationale
TIMESTAMP_FORMAT = "%Y%m%dT%H%M%SZ"  # Compact ISO8601 for filename/branch safety
VALID_WORKFLOW_TYPES = ["feature", "release", "hotfix"]  # Supported workflow types


def setup_agentdb_symlink(worktree_path: Path, main_repo_path: Path) -> bool:
    """Create symlink from worktree's agentdb.duckdb to main repo's database.

    This enables all worktrees to share a unified AgentDB, allowing cross-session
    visibility of workflow state.

    Args:
        worktree_path: Path to the newly created worktree
        main_repo_path: Path to the main repository (source of AgentDB)

    Returns:
        True if symlink created successfully, False otherwise
    """
    worktree_state_dir = worktree_path / ".claude-state"
    main_state_dir = main_repo_path / ".claude-state"
    main_db_path = main_state_dir / "agentdb.duckdb"
    worktree_db_path = worktree_state_dir / "agentdb.duckdb"

    try:
        # Ensure main repo state directory exists
        main_state_dir.mkdir(parents=True, exist_ok=True)

        # Initialize main repo database if it doesn't exist
        if not main_db_path.exists():
            # Touch the file so symlink target exists
            main_db_path.touch()

        # Skip if symlink already exists (idempotent)
        if worktree_db_path.exists() or worktree_db_path.is_symlink():
            return True

        # Create relative symlink for portability
        # Calculate relative path from worktree_state_dir to main_db_path
        relative_target = os.path.relpath(main_db_path, worktree_state_dir)
        worktree_db_path.symlink_to(relative_target)

        return True

    except (OSError, PermissionError) as e:
        print(f"⚠️  Could not create AgentDB symlink: {e}", file=sys.stderr)
        return False


def verify_planning_committed(slug: str, repo_root: Path) -> None:
    """
    Verify planning documents are committed and pushed before worktree creation.

    This function ensures that BMAD planning documents exist and are properly
    committed/pushed before a feature worktree can be created. This prevents
    worktrees that don't contain the planning context.

    Args:
        slug: Feature slug (e.g., 'auth-system')
        repo_root: Path to repository root

    Raises:
        ValueError: If planning directory doesn't exist
        ValueError: If uncommitted changes detected in planning directory
        ValueError: If local branch is ahead of remote

    Note:
        Only called for feature worktrees, not release/hotfix.
    """
    planning_dir = repo_root / "planning" / slug

    # Check 1: Planning directory exists
    if not planning_dir.exists():
        raise ValueError(
            f"Planning directory not found: planning/{slug}/\n\n"
            f"Resolution: Run /1_specify to create planning documents first.\n\n"
            f"Expected files:\n"
            f"  - planning/{slug}/requirements.md\n"
            f"  - planning/{slug}/architecture.md\n"
            f"  - planning/{slug}/epics.md"
        )

    # Check 2: No uncommitted changes in planning directory
    result = subprocess.run(
        ["git", "status", "--porcelain", f"planning/{slug}/"],
        capture_output=True,
        text=True,
        cwd=repo_root,
    )
    if result.stdout.strip():
        raise ValueError(
            f"Uncommitted changes detected in planning/{slug}/\n\n"
            f"Changed files:\n{result.stdout}\n"
            f"Resolution: Commit and push planning documents first:\n"
            f"  git add planning/{slug}/\n"
            f"  git commit -m 'docs(planning): add planning for {slug}'\n"
            f"  git push"
        )

    # Check 3: Local branch is pushed to remote
    # First fetch to ensure we have latest remote state
    subprocess.run(
        ["git", "fetch", "origin"],
        capture_output=True,
        text=True,
        cwd=repo_root,
    )

    # Get current branch
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
        cwd=repo_root,
    )
    current_branch = result.stdout.strip()

    # Check if local is ahead of remote (only if remote branch exists)
    result = subprocess.run(
        ["git", "rev-list", "--count", f"origin/{current_branch}..HEAD"],
        capture_output=True,
        text=True,
        cwd=repo_root,
    )
    # Only check if remote branch exists (returncode 0)
    if result.returncode == 0:
        ahead_count = result.stdout.strip()
        if ahead_count and int(ahead_count) > 0:
            raise ValueError(
                f"Local branch is {ahead_count} commit(s) ahead of remote.\n\n"
                f"Resolution: Push your changes first:\n"
                f"  git push origin {current_branch}"
            )


def create_worktree(workflow_type, slug, base_branch, create_todo=False):
    """
    Create a worktree for feature/release/hotfix development.

    Args:
        workflow_type: 'feature' | 'release' | 'hotfix'
        slug: Short descriptive name (e.g., 'json-validator')
        base_branch: Branch to create from (e.g., 'contrib/username')
        create_todo: If True, create TODO file (default False, deprecated)

    Returns:
        dict with worktree_path, branch_name, todo_file (None if not created)

    Raises:
        ValueError: If inputs are invalid
        subprocess.CalledProcessError: If git/gh commands fail
        FileNotFoundError: If required tools are missing
    """
    # Input validation
    if workflow_type not in VALID_WORKFLOW_TYPES:
        raise ValueError(
            f"Invalid workflow_type '{workflow_type}'. "
            f"Must be one of: {', '.join(VALID_WORKFLOW_TYPES)}"
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

    # Verify planning documents are committed and pushed (feature worktrees only)
    if workflow_type == "feature":
        verify_planning_committed(slug, repo_root)

    worktree_path = repo_root.parent / f"{repo_root.name}_{workflow_type}_{timestamp}_{slug}"

    # Check if worktree path already exists
    if worktree_path.exists():
        raise FileExistsError(
            f"Worktree path already exists: {worktree_path}\n"
            f"Remove it first with: git worktree remove {worktree_path}"
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

    # TODO file creation (deprecated, only if explicitly requested)
    todo_filename = None
    if create_todo:
        # Get VCS username (GitHub/Azure DevOps)
        try:
            vcs = get_vcs_adapter()
            gh_user = vcs.get_current_user()
        except RuntimeError as e:
            print("ERROR: Failed to get VCS username", file=sys.stderr)
            print(f"Error: {e}", file=sys.stderr)
            raise

        todo_filename = f"TODO_{workflow_type}_{timestamp}_{slug}.md"
        todo_path = repo_root / todo_filename

        # Check if TODO file already exists
        if todo_path.exists():
            print(
                f"WARNING: TODO file already exists: {todo_filename}\n"
                f"This worktree may have been created before.",
                file=sys.stderr,
            )

        # Copy template and customize
        template_path = (
            repo_root
            / ".claude"
            / "skills"
            / "workflow-orchestrator"
            / "templates"
            / "TODO_template.md"
        )

        # Use timezone-aware datetime for creation timestamp
        created_timestamp = datetime.now(UTC).isoformat().replace("+00:00", "Z")

        try:
            if template_path.exists():
                try:
                    with open(template_path) as f:
                        content = f.read()
                except (OSError, PermissionError) as e:
                    print(f"ERROR: Cannot read template file: {template_path}", file=sys.stderr)
                    print(f"Error: {e}", file=sys.stderr)
                    raise

                # Replace placeholders
                content = content.replace("{{WORKFLOW_TYPE}}", workflow_type)
                content = content.replace("{{SLUG}}", slug)
                content = content.replace("{{TIMESTAMP}}", timestamp)
                content = content.replace("{{GH_USER}}", gh_user)
                content = content.replace("{{TITLE}}", slug.replace("-", " ").title())
                content = content.replace("{{DESCRIPTION}}", f"{workflow_type.title()} for {slug}")
                content = content.replace("{{CREATED}}", created_timestamp)

                try:
                    with open(todo_path, "w") as f:
                        f.write(content)
                except (OSError, PermissionError) as e:
                    print(f"ERROR: Cannot write TODO file: {todo_path}", file=sys.stderr)
                    print(f"Error: {e}", file=sys.stderr)
                    raise
            else:
                # Create minimal TODO if template doesn't exist
                print(
                    f"WARNING: Template not found at {template_path}, using minimal TODO",
                    file=sys.stderr,
                )
                try:
                    with open(todo_path, "w") as f:
                        f.write(
                            f"""---
type: workflow-manifest
workflow_type: {workflow_type}
slug: {slug}
timestamp: {timestamp}
github_user: {gh_user}
---

# TODO: {slug}

Workflow: {workflow_type}
Created: {created_timestamp}
"""
                        )
                except (OSError, PermissionError) as e:
                    print(f"ERROR: Cannot write TODO file: {todo_path}", file=sys.stderr)
                    print(f"Error: {e}", file=sys.stderr)
                    raise
        except Exception:
            # Cleanup worktree if TODO creation failed
            print("ERROR: TODO file creation failed, cleaning up worktree...", file=sys.stderr)
            try:
                subprocess.run(
                    ["git", "worktree", "remove", str(worktree_path)],
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
                subprocess.run(
                    ["git", "branch", "-D", branch_name], stderr=subprocess.DEVNULL, check=False
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Ignore errors during cleanup: worktree/branch may not exist or removal may fail,
                # but the original error is more important and will be re-raised.
                pass
            raise

    # Initialize .claude-state/ directory in new worktree
    state_dir = worktree_path / ".claude-state"
    try:
        state_dir.mkdir(exist_ok=True)
        # Create .gitignore in state dir
        (state_dir / ".gitignore").write_text("# Ignore all files in state directory\n*\n")
        # Create .worktree-id with hash of worktree path (using shared implementation)
        worktree_id = compute_worktree_id(worktree_path)
        (state_dir / ".worktree-id").write_text(worktree_id)
        print(f"✓ State directory: {state_dir}")

        # Create symlink for shared AgentDB (repo_root is main repo)
        if setup_agentdb_symlink(worktree_path, repo_root):
            print(f"✓ AgentDB symlink: {state_dir / 'agentdb.duckdb'} → main repo")
        else:
            print("ℹ️  AgentDB: isolated (symlink creation failed)")
    except (OSError, PermissionError) as e:
        print(f"⚠️  Could not create state directory: {e}", file=sys.stderr)

    print(f"✓ Worktree created: {worktree_path}")
    print(f"✓ Branch: {branch_name}")
    if todo_filename:
        print(f"✓ TODO file: {todo_filename}")
    else:
        print("ℹ️  TODO file: skipped (deprecated)")

    return {
        "worktree_path": str(worktree_path),
        "branch_name": branch_name,
        "todo_file": todo_filename,
        "state_dir": str(state_dir) if state_dir.exists() else None,
    }


def main():
    """Main entry point with argparse."""
    parser = argparse.ArgumentParser(
        description="Create feature/release/hotfix worktree",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create feature worktree (no TODO file by default)
  python create_worktree.py feature my-feature contrib/stharrold

  # Create feature worktree with TODO file (deprecated)
  python create_worktree.py feature my-feature contrib/stharrold --create-todo

  # Create release worktree
  python create_worktree.py release v1.6.0 develop
""",
    )

    parser.add_argument("workflow_type", choices=VALID_WORKFLOW_TYPES, help="Workflow type")
    parser.add_argument("slug", help="Short descriptive name (e.g., my-feature, v1.6.0)")
    parser.add_argument(
        "base_branch", help="Branch to create from (e.g., contrib/username, develop)"
    )
    parser.add_argument(
        "--create-todo",
        action="store_true",
        default=False,
        help="Create TODO file (deprecated, defaults to False)",
    )
    parser.add_argument(
        "--no-todo",
        action="store_true",
        default=True,
        help="Skip TODO file creation (default, for backward compatibility)",
    )

    args = parser.parse_args()

    # Determine if we should create TODO
    # --create-todo explicitly enables it, otherwise default is False
    create_todo = args.create_todo

    try:
        result = create_worktree(
            args.workflow_type, args.slug, args.base_branch, create_todo=create_todo
        )

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
