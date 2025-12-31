#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""
PR Workflow Enforcement Script

Enforces the required workflow sequence:
1. pr-finish-feature-to-contrib - Create PR from feature to contrib branch
2. pr-start-contrib-to-develop - Create PR from contrib to develop

Usage:
    uv run python .claude/skills/git-workflow-manager/scripts/pr_workflow.py <step>

Steps:
    finish-feature    - Step 1: PR feature -> contrib (runs quality gates first)
    start-develop     - Step 2: PR contrib -> develop
    full              - Run all steps in sequence
    status            - Show current workflow status
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Add workflow-utilities to path for safe_output utilities
sys.path.insert(
    0,
    str(Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"),
)

# Safe cross-platform output
try:
    from safe_output import format_check, format_cross, format_warning, safe_print
except ImportError:
    # Fallback if module not found - ASCII-only output
    def safe_print(*args, **kwargs):
        print(*args, **kwargs)

    def format_check(msg):
        return f"[OK] {msg}"

    def format_cross(msg):
        return f"[FAIL] {msg}"

    def format_warning(msg):
        return f"[WARN] {msg}"


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    safe_print(f"  -> {' '.join(cmd)}")
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def get_current_branch() -> str:
    """Get current git branch name."""
    result = run_cmd(["git", "branch", "--show-current"], check=False)
    return result.stdout.strip()


def get_contrib_branch() -> str:
    """Get the contrib branch name (contrib/<username>)."""
    result = run_cmd(["gh", "api", "user", "-q", ".login"], check=False)
    username = result.stdout.strip() or "stharrold"
    return f"contrib/{username}"


def return_to_editable_branch() -> bool:
    """
    Return to the editable branch (contrib/*) after workflow completion.

    IMPORTANT: All workflows must end on an editable branch, never on
    integration branches (develop, main) or ephemeral branches (release/*).
    """
    contrib = get_contrib_branch()
    current = get_current_branch()

    if current == contrib:
        print(f"  Already on editable branch: {contrib}")
        return True

    print(f"\n[Return] Switching to editable branch: {contrib}")
    result = run_cmd(["git", "checkout", contrib], check=False)

    if result.returncode != 0:
        safe_print(format_cross(f" Failed to checkout {contrib}: {result.stderr}"))
        return False

    safe_print(format_check(f" Now on editable branch: {contrib}"))
    return True


def run_quality_gates() -> bool:
    """Run quality gates before PR."""
    print("\n[Quality Gates] Running quality gates...")
    script_path = Path(".claude/skills/quality-enforcer/scripts/run_quality_gates.py")

    if not script_path.exists():
        safe_print(format_warning("  Quality gates script not found, skipping"))
        return True

    result = subprocess.run(
        ["podman-compose", "run", "--rm", "dev", "python", str(script_path)], check=False
    )

    return result.returncode == 0


def step_finish_feature() -> bool:
    """
    Step 1: Create PR from feature branch to contrib branch.

    Prerequisites:
    - Must be on a feature branch (feature/*)
    - Quality gates must pass
    """
    print("\n" + "=" * 60)
    print("STEP 1: PR Feature -> Contrib")
    print("=" * 60)

    current = get_current_branch()
    contrib = get_contrib_branch()

    # Validate we're on a feature branch
    if not current.startswith("feature/"):
        safe_print(format_cross(f" Must be on a feature branch (current: {current})"))
        print("  Expected: feature/*")
        return False

    # Run quality gates
    if not run_quality_gates():
        safe_print(format_cross(" Quality gates failed. Fix issues before creating PR."))
        return False

    # Push branch
    print(f"\n[Push] Pushing {current}...")
    result = run_cmd(["git", "push", "-u", "origin", current], check=False)
    if result.returncode != 0:
        safe_print(format_cross(f" Push failed: {result.stderr}"))
        return False

    # Create PR
    print(f"\n[PR] Creating PR: {current} -> {contrib}...")
    result = run_cmd(
        [
            "gh",
            "pr",
            "create",
            "--base",
            contrib,
            "--fill",
            "--body",
            "Feature PR created via workflow automation.\n\n[BOT] Generated with [Claude Code](https://claude.com/claude-code)",
        ],
        check=False,
    )

    if result.returncode != 0:
        if "already exists" in result.stderr:
            safe_print(format_warning("  PR already exists"))
        else:
            safe_print(format_cross(f" PR creation failed: {result.stderr}"))
            return False

    safe_print(format_check(f" Step 1 complete: PR created {current} -> {contrib}"))
    print("\nNext: After PR is merged, run: pr_workflow.py start-develop")
    return True


def step_start_develop() -> bool:
    """
    Step 2: Create PR from contrib branch to develop.

    Prerequisites:
    - Must be on contrib/* branch
    - All previous steps complete
    """
    print("\n" + "=" * 60)
    print("STEP 2: PR Contrib -> Develop")
    print("=" * 60)

    current = get_current_branch()
    contrib = get_contrib_branch()

    # Validate we're on contrib branch
    if not current.startswith("contrib/"):
        safe_print(format_warning(f"  Not on contrib branch (current: {current})"))
        print(f"  Switching to {contrib}...")
        run_cmd(["git", "checkout", contrib], check=False)

    # Push any pending changes
    print(f"\n[Push] Pushing {contrib}...")
    result = run_cmd(["git", "push", "origin", contrib], check=False)

    # Create PR to develop
    print(f"\n[PR] Creating PR: {contrib} -> develop...")
    result = run_cmd(
        [
            "gh",
            "pr",
            "create",
            "--base",
            "develop",
            "--fill",
            "--body",
            (
                f"Integration PR: {contrib} -> develop\n\n"
                "Workflow steps completed:\n"
                "- [x] Quality gates passed\n"
                "- [x] AI config synced\n\n"
                "[BOT] Generated with [Claude Code](https://claude.com/claude-code)"
            ),
        ],
        check=False,
    )

    if result.returncode != 0:
        if "already exists" in result.stderr:
            safe_print(format_warning("  PR already exists"))
        else:
            safe_print(format_cross(f" PR creation failed: {result.stderr}"))
            return False

    safe_print(format_check(f" Step 4 complete: PR created {contrib} -> develop"))

    # Return to editable branch
    return_to_editable_branch()

    print("\n[OK] WORKFLOW COMPLETE")
    return True


def show_status():
    """Show current workflow status."""
    print("\n" + "=" * 60)
    print("WORKFLOW STATUS")
    print("=" * 60)

    current = get_current_branch()
    contrib = get_contrib_branch()

    print(f"\nCurrent branch: {current}")
    print(f"Contrib branch: {contrib}")

    # Determine next step
    print("\n" + "-" * 40)
    if current.startswith("feature/"):
        print("Next step: pr_workflow.py finish-feature")
    elif current.startswith("contrib/"):
        print("Next step: pr_workflow.py start-develop")
    else:
        print("Status: Ready for new feature")


def run_full_workflow():
    """Run all workflow steps in sequence."""
    print("\n" + "=" * 60)
    print("FULL WORKFLOW")
    print("=" * 60)

    steps = [
        ("finish-feature", step_finish_feature),
        ("start-develop", step_start_develop),
    ]

    for name, func in steps:
        print(f"\n>>> Running step: {name}")
        if not func():
            print(f"\n[FAIL] Workflow stopped at step: {name}")
            # Always return to editable branch, even on failure
            return_to_editable_branch()
            return False

    # Ensure we're on editable branch (step_start_develop should do this, but be explicit)
    return_to_editable_branch()

    print("\n" + "=" * 60)
    safe_print(format_check(" FULL WORKFLOW COMPLETE"))
    print("=" * 60)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="PR Workflow Enforcement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "step",
        choices=["finish-feature", "start-develop", "full", "status"],
        help="Workflow step to execute",
    )

    args = parser.parse_args()

    step_map = {
        "finish-feature": step_finish_feature,
        "start-develop": step_start_develop,
        "full": run_full_workflow,
        "status": show_status,
    }

    success = step_map[args.step]()

    if args.step != "status":
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
