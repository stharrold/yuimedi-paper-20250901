#!/usr/bin/env python3
"""
Backmerge Workflow Script

Syncs release changes back to development branches.

Usage:
    podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py <step>

Steps:
    pr-develop      - Create PR from release to develop
    rebase-contrib  - Rebase contrib branch on develop
    cleanup-release - Delete release branch
    full            - Run all steps in sequence
    status          - Show current backmerge status
"""

import argparse
import os
import subprocess
import sys
from typing import Optional


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result.

    If check=False and the command fails, stderr is logged for debugging.
    """
    print(f"  → {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, check=check)
    # Log stderr on failure when not raising exception (PR #226 review feedback)
    if not check and result.returncode != 0 and result.stderr:
        print(f"    [debug] stderr: {result.stderr.strip()}")
    return result


def get_current_branch() -> str:
    """Get current git branch name."""
    result = run_cmd(["git", "branch", "--show-current"], check=False)
    return result.stdout.strip()


def get_contrib_branch() -> str:
    """Get the contrib branch name (contrib/<username>).

    Tries multiple sources for username (PR #226 review feedback):
    1. GitHub CLI (gh api user)
    2. Environment variable GITHUB_USERNAME
    3. Git config user.name
    4. Raises error if none available
    """
    # Try GitHub CLI first
    result = run_cmd(["gh", "api", "user", "-q", ".login"], check=False)
    username = result.stdout.strip()

    # Fallback to environment variable
    if not username:
        username = os.environ.get("GITHUB_USERNAME", "")

    # Fallback to git config
    if not username:
        result = run_cmd(["git", "config", "user.name"], check=False)
        username = result.stdout.strip()

    # Error if no username found
    if not username:
        print("✗ Could not determine GitHub username.")
        print("  Fix: Run 'gh auth login' or set GITHUB_USERNAME env var")
        sys.exit(1)

    return f"contrib/{username}"


def return_to_editable_branch() -> bool:
    """Return to the editable branch (contrib/*) after workflow completion."""
    contrib = get_contrib_branch()
    current = get_current_branch()

    if current == contrib:
        print(f"  Already on editable branch: {contrib}")
        return True

    print(f"\n[Return] Switching to editable branch: {contrib}")
    result = run_cmd(["git", "checkout", contrib], check=False)

    if result.returncode != 0:
        print(f"✗ Failed to checkout {contrib}: {result.stderr}")
        return False

    print(f"✓ Now on editable branch: {contrib}")
    return True


def find_release_branch() -> Optional[str]:
    """Find the most recent release branch."""
    result = run_cmd(["git", "branch", "-r", "--list", "origin/release/*"], check=False)
    branches = result.stdout.strip().split("\n")
    if branches and branches[0]:
        # Return the most recent (last) release branch
        return branches[-1].strip().replace("origin/", "")
    return None


def step_pr_develop(version: Optional[str] = None) -> bool:
    """Create PR from release to develop."""
    print("\n" + "=" * 60)
    print("STEP 1: PR Release → Develop")
    print("=" * 60)

    # Find release branch
    release_branch = None
    if version:
        release_branch = f"release/{version}"
    else:
        release_branch = find_release_branch()

    if not release_branch:
        print("✗ No release branch found. Specify --version or create release first.")
        return False

    print(f"  Using release branch: {release_branch}")

    # Fetch latest
    run_cmd(["git", "fetch", "origin"], check=False)

    # Create PR
    print(f"\n[PR] Creating PR: {release_branch} → develop...")
    result = run_cmd(
        [
            "gh",
            "pr",
            "create",
            "--base",
            "develop",
            "--head",
            release_branch,
            "--fill",
            "--title",
            f"Backmerge {release_branch} to develop",
            "--body",
            "Backmerge release changes to develop.\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)",
        ],
        check=False,
    )

    if result.returncode != 0:
        if "already exists" in result.stderr:
            print("⚠️  PR already exists")
        else:
            print(f"✗ PR creation failed: {result.stderr}")
            return False

    print(f"✓ Step 1 complete: PR created {release_branch} → develop")
    print("\nNext: Merge PR in GitHub, then run: backmerge_workflow.py rebase-contrib")
    return True


def step_rebase_contrib() -> bool:
    """Rebase contrib branch on develop."""
    print("\n" + "=" * 60)
    print("STEP 2: Rebase Contrib on Develop")
    print("=" * 60)

    contrib = get_contrib_branch()

    # Fetch latest
    print("\n[Fetch] Fetching latest...")
    run_cmd(["git", "fetch", "origin"], check=False)

    # Checkout contrib
    print(f"\n[Checkout] Switching to {contrib}...")
    result = run_cmd(["git", "checkout", contrib], check=False)
    if result.returncode != 0:
        print(f"✗ Failed to checkout {contrib}: {result.stderr}")
        return False

    # Check for uncommitted changes
    result = run_cmd(["git", "status", "--porcelain"], check=False)
    if result.stdout.strip():
        print("✗ Uncommitted changes detected. Commit or stash before rebase.")
        return False

    # Rebase on develop
    print(f"\n[Rebase] Rebasing {contrib} onto origin/develop...")
    result = run_cmd(["git", "rebase", "origin/develop"], check=False)

    if result.returncode != 0:
        print("⚠️  Rebase conflict detected!")
        print("  Resolve conflicts manually, then run:")
        print("    git rebase --continue")
        print("    git push --force-with-lease")
        return False

    # Force push with lease
    print(f"\n[Push] Force pushing {contrib}...")
    result = run_cmd(["git", "push", "--force-with-lease", "origin", contrib], check=False)

    if result.returncode != 0:
        print(f"✗ Push failed: {result.stderr}")
        return False

    print(f"✓ Step 2 complete: {contrib} rebased on develop")
    return True


def step_cleanup_release(version: Optional[str] = None) -> bool:
    """Delete release branch locally and remotely."""
    print("\n" + "=" * 60)
    print("STEP 3: Cleanup Release Branch")
    print("=" * 60)

    # Find release branch
    release_branch = None
    if version:
        release_branch = f"release/{version}"
    else:
        release_branch = find_release_branch()

    if not release_branch:
        print("⚠️  No release branch found to cleanup")
        return True

    print(f"  Cleaning up: {release_branch}")

    # Make sure we're not on the release branch
    current = get_current_branch()
    if current == release_branch:
        return_to_editable_branch()

    # Delete local branch
    print(f"\n[Delete] Deleting local {release_branch}...")
    run_cmd(["git", "branch", "-D", release_branch], check=False)

    # Delete remote branch
    print(f"\n[Delete] Deleting remote {release_branch}...")
    result = run_cmd(["git", "push", "origin", "--delete", release_branch], check=False)

    if result.returncode != 0:
        if "remote ref does not exist" in result.stderr:
            print("  Remote branch already deleted")
        else:
            print(f"⚠️  Remote delete warning: {result.stderr}")

    # Return to editable branch
    return_to_editable_branch()

    print(f"✓ Step 3 complete: {release_branch} cleaned up")
    return True


def show_status() -> bool:
    """Show current backmerge status."""
    print("\n" + "=" * 60)
    print("BACKMERGE STATUS")
    print("=" * 60)

    current = get_current_branch()
    contrib = get_contrib_branch()

    print(f"\nCurrent branch: {current}")
    print(f"Contrib branch: {contrib}")

    # Show release branches
    release_branch = find_release_branch()
    if release_branch:
        print(f"Release branch: {release_branch}")
    else:
        print("Release branch: None")

    # Check if contrib is behind develop
    run_cmd(["git", "fetch", "origin"], check=False)
    result = run_cmd(["git", "rev-list", "--count", f"{contrib}..origin/develop"], check=False)
    behind = result.stdout.strip()
    if behind and behind != "0":
        print(f"\n⚠️  {contrib} is {behind} commits behind develop")

    # Determine next step
    print("\n" + "-" * 40)
    if release_branch:
        print("Next step: backmerge_workflow.py pr-develop")
    elif behind and behind != "0":
        print("Next step: backmerge_workflow.py rebase-contrib")
    else:
        print("Status: All synced, ready for next feature")

    return True


def run_full_workflow(version: Optional[str] = None) -> bool:
    """Run all workflow steps in sequence."""
    print("\n" + "=" * 60)
    print("FULL BACKMERGE WORKFLOW")
    print("=" * 60)

    # Note: pr-develop requires manual PR merge, so we split the workflow
    print("\n⚠️  Full workflow requires manual PR merge between steps.")
    print("Running pr-develop first...")

    if not step_pr_develop(version):
        return_to_editable_branch()
        return False

    print("\n" + "-" * 40)
    print("MANUAL STEP: Merge the PR in GitHub")
    print("Then run: backmerge_workflow.py rebase-contrib")
    print("-" * 40)

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Backmerge Workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "step",
        choices=["pr-develop", "rebase-contrib", "cleanup-release", "full", "status"],
        help="Workflow step to execute",
    )
    parser.add_argument(
        "--version", help="Version for release (e.g., v1.6.0). Auto-detected if not provided."
    )

    args = parser.parse_args()

    step_map = {
        "pr-develop": lambda: step_pr_develop(args.version),
        "rebase-contrib": step_rebase_contrib,
        "cleanup-release": lambda: step_cleanup_release(args.version),
        "full": lambda: run_full_workflow(args.version),
        "status": show_status,
    }

    success = step_map[args.step]()

    if args.step != "status":
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
