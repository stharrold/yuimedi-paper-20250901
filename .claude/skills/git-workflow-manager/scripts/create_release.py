#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Create release branch from base branch.

This script implements Step 5.1 of Phase 5 (Release Workflow) as documented
in WORKFLOW.md. It creates a release branch following git-flow conventions
and validates the version.

Note: TODO file generation is deprecated. Use GitHub Issues for task tracking.

Usage:
    python create_release.py <version> <base_branch> [--yes]

Example:
    python create_release.py v1.1.0 develop
    python create_release.py v1.1.0 develop --yes  # Skip confirmation prompts

Requirements:
    - Clean working directory (no uncommitted changes)
    - Base branch must exist
    - Version must follow semantic versioning (vX.Y.Z)
    - Version tag must not already exist
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Constants with documented rationale
RELEASE_BRANCH_PREFIX = "release/"
# Rationale: git-flow release branch naming convention for clarity and tooling compatibility

VERSION_PATTERN = r"^v\d+\.\d+\.\d+$"
# Rationale: Enforce semantic versioning (vMAJOR.MINOR.PATCH) for consistency


def validate_version_format(version):
    """
    Validate version follows semantic versioning pattern.

    Args:
        version: Version string to validate (e.g., 'v1.1.0')

    Raises:
        ValueError: If version doesn't match vX.Y.Z pattern
    """
    if not re.match(VERSION_PATTERN, version):
        raise ValueError(
            f"Invalid version format '{version}'. Must match pattern vX.Y.Z (e.g., v1.1.0, v2.0.0)"
        )


def check_working_directory_clean():
    """
    Verify working directory has no uncommitted changes.

    Raises:
        RuntimeError: If working directory has uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
        )

        if result.stdout.strip():
            raise RuntimeError(
                "Working directory has uncommitted changes. Please commit or stash changes before creating release branch."
            )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to check git status: {e.stderr.strip()}") from e


def verify_branch_exists(branch_name):
    """
    Verify that a git branch exists.

    Args:
        branch_name: Name of branch to verify

    Raises:
        ValueError: If branch doesn't exist
    """
    try:
        subprocess.run(
            ["git", "rev-parse", "--verify", branch_name], capture_output=True, check=True
        )
    except subprocess.CalledProcessError:
        raise ValueError(
            f"Base branch '{branch_name}' does not exist. Use 'git branch -a' to list available branches."
        )


def verify_tag_not_exists(version):
    """
    Verify that a version tag doesn't already exist.

    Args:
        version: Version tag to check (e.g., 'v1.1.0')

    Raises:
        ValueError: If tag already exists
    """
    try:
        result = subprocess.run(
            ["git", "tag", "-l", version], capture_output=True, text=True, check=True
        )

        if result.stdout.strip():
            raise ValueError(
                f"Tag '{version}' already exists. Use 'git tag -l' to list existing tags."
            )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to check git tags: {e.stderr.strip()}") from e


def get_semantic_version_recommendation(base_branch):
    """
    Get recommended version from semantic_version.py.

    Args:
        base_branch: Branch to analyze for changes

    Returns:
        Recommended version string (e.g., 'v1.1.0'), or None if script unavailable
    """
    script_path = Path(__file__).parent / "semantic_version.py"

    if not script_path.exists():
        print(f"Warning: semantic_version.py not found at {script_path}", file=sys.stderr)
        return None

    try:
        # Get latest tag to determine current version
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True, check=False
        )

        current_version = result.stdout.strip() if result.returncode == 0 else "v1.0.0"

        # Call semantic_version.py to get recommendation
        result = subprocess.run(
            ["python3", str(script_path), base_branch, current_version],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        print(
            f"Warning: Failed to get semantic version recommendation: {e.stderr.strip()}",
            file=sys.stderr,
        )
        return None


def confirm_version_mismatch(provided_version, recommended_version, auto_confirm=False):
    """
    Prompt user to confirm if provided version differs from recommendation.

    Args:
        provided_version: Version provided by user
        recommended_version: Version recommended by semantic_version.py
        auto_confirm: If True, skip confirmation prompt (for --yes flag)

    Returns:
        True if user confirms or auto_confirm is True, False otherwise
    """
    if provided_version == recommended_version:
        return True

    if auto_confirm:
        print(
            f"[WARN]  Version mismatch: provided {provided_version}, recommended {recommended_version}",
            file=sys.stderr,
        )
        print(f"Continuing with {provided_version} (--yes flag enabled)", file=sys.stderr)
        return True

    print("\n[WARN]  Version Mismatch Warning", file=sys.stderr)
    print(f"Provided version:    {provided_version}", file=sys.stderr)
    print(f"Recommended version: {recommended_version}", file=sys.stderr)
    print(
        f"\nSemantic versioning suggests {recommended_version} based on changes.", file=sys.stderr
    )
    print(f"Do you want to continue with {provided_version}? (Y/n): ", end="", file=sys.stderr)

    response = input().strip().lower()
    return response in ["y", "yes", ""]


def create_release_branch(version, base_branch):
    """
    Create release branch from base branch.

    Args:
        version: Release version (e.g., 'v1.1.0')
        base_branch: Branch to create release from (e.g., 'develop')

    Returns:
        Tuple of (branch_name, base_commit_sha)

    Raises:
        RuntimeError: If branch creation fails
    """
    branch_name = f"{RELEASE_BRANCH_PREFIX}{version}"

    try:
        # Get base commit SHA for reporting
        result = subprocess.run(
            ["git", "rev-parse", "--short", base_branch], capture_output=True, text=True, check=True
        )
        base_commit = result.stdout.strip()

        # Create branch
        subprocess.run(
            ["git", "checkout", "-b", branch_name, base_branch], capture_output=True, check=True
        )

        # Push to origin
        subprocess.run(
            ["git", "push", "-u", "origin", branch_name], capture_output=True, check=True
        )

        return branch_name, base_commit

    except subprocess.CalledProcessError as e:
        # Cleanup on failure
        print("ERROR: Failed to create release branch", file=sys.stderr)
        print("Cleaning up...", file=sys.stderr)

        # Try to delete local branch if it was created
        subprocess.run(["git", "branch", "-D", branch_name], capture_output=True, check=False)

        # Try to return to base branch
        subprocess.run(["git", "checkout", base_branch], capture_output=True, check=False)

        raise RuntimeError(
            f"Failed to create release branch: {e.stderr.decode() if e.stderr else 'Unknown error'}"
        ) from e


def main():
    """Main entry point for create_release.py script."""
    parser = argparse.ArgumentParser(
        description="Create release branch from base branch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s v1.1.0 develop
  %(prog)s v1.1.0 develop --yes

For more information, see WORKFLOW.md Phase 5 (Release Workflow).
        """,
    )
    parser.add_argument("version", help="Release version (e.g., v1.1.0)")
    parser.add_argument("base_branch", help="Base branch to create release from (e.g., develop)")
    parser.add_argument(
        "--yes", "-y", action="store_true", help="Skip confirmation prompts (non-interactive mode)"
    )

    args = parser.parse_args()
    version = args.version
    base_branch = args.base_branch
    auto_confirm = args.yes

    try:
        # Step 1: Input Validation
        print("Validating inputs...", file=sys.stderr)
        validate_version_format(version)
        verify_branch_exists(base_branch)
        check_working_directory_clean()
        verify_tag_not_exists(version)

        # Step 2: Version Verification
        print("Checking semantic version recommendation...", file=sys.stderr)
        recommended_version = get_semantic_version_recommendation(base_branch)

        if recommended_version and recommended_version != version:
            if not confirm_version_mismatch(version, recommended_version, auto_confirm):
                print("Release creation cancelled by user.", file=sys.stderr)
                sys.exit(1)

        # Step 3: Create Release Branch
        print("Creating release branch...", file=sys.stderr)
        branch_name, base_commit = create_release_branch(version, base_branch)

        # Success output
        print(f"\n[OK] Created release branch: {branch_name}")
        print(f"[OK] Base: {base_branch} (commit {base_commit})")
        print("[OK] Ready for final QA and documentation updates")
        print("\nNext steps:")
        print(
            "  1. Run quality gates: uv run python .claude/skills/quality-enforcer/scripts/run_quality_gates.py"
        )
        print("  2. Update documentation and version in pyproject.toml")
        print(f"  3. Create PR to main: gh pr create --base main --title 'Release {version}'")

    except (ValueError, RuntimeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nRelease creation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
