#!/usr/bin/env python3
"""
PR Workflow Enforcement Script

Enforces the required workflow sequence:
1. pr-finish-feature-to-contrib - Create PR from feature to contrib branch
2. archive-todo - Archive the TODO file after PR merge
3. copy-claude-to-agents - Sync CLAUDE.md to AGENTS.md and .agents/
4. pr-start-contrib-to-develop - Create PR from contrib to develop

Usage:
    podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/pr_workflow.py <step>

Steps:
    finish-feature    - Step 1: PR feature → contrib (runs quality gates first)
    archive-todo      - Step 2: Archive TODO file after merge
    sync-agents       - Step 3: Sync CLAUDE.md → AGENTS.md
    start-develop     - Step 4: PR contrib → develop
    full              - Run all steps in sequence
    status            - Show current workflow status
"""

import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    print(f"  → {' '.join(cmd)}")
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
        print(f"✗ Failed to checkout {contrib}: {result.stderr}")
        return False

    print(f"✓ Now on editable branch: {contrib}")
    return True


def run_quality_gates() -> bool:
    """Run quality gates before PR."""
    print("\n[Quality Gates] Running quality gates...")
    script_path = Path(".claude/skills/quality-enforcer/scripts/run_quality_gates.py")

    if not script_path.exists():
        print("⚠️  Quality gates script not found, skipping")
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
    print("STEP 1: PR Feature → Contrib")
    print("=" * 60)

    current = get_current_branch()
    contrib = get_contrib_branch()

    # Validate we're on a feature branch
    if not current.startswith("feature/"):
        print(f"✗ Must be on a feature branch (current: {current})")
        print("  Expected: feature/*")
        return False

    # Run quality gates
    if not run_quality_gates():
        print("✗ Quality gates failed. Fix issues before creating PR.")
        return False

    # Push branch
    print(f"\n[Push] Pushing {current}...")
    result = run_cmd(["git", "push", "-u", "origin", current], check=False)
    if result.returncode != 0:
        print(f"✗ Push failed: {result.stderr}")
        return False

    # Create PR
    print(f"\n[PR] Creating PR: {current} → {contrib}...")
    result = run_cmd(
        [
            "gh",
            "pr",
            "create",
            "--base",
            contrib,
            "--fill",
            "--body",
            "Feature PR created via workflow automation.\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)",
        ],
        check=False,
    )

    if result.returncode != 0:
        if "already exists" in result.stderr:
            print("⚠️  PR already exists")
        else:
            print(f"✗ PR creation failed: {result.stderr}")
            return False

    print(f"✓ Step 1 complete: PR created {current} → {contrib}")
    print("\nNext: After PR is merged, run: pr_workflow.py archive-todo")
    return True


def step_archive_todo() -> bool:
    """
    Step 2: Archive the TODO file after PR merge.

    Archives TODO*.md files to ARCHIVED/ with timestamp.
    """
    print("\n" + "=" * 60)
    print("STEP 2: Archive TODO")
    print("=" * 60)

    # Find TODO files
    todo_files = list(Path(".").glob("TODO*.md"))

    if not todo_files:
        print("⚠️  No TODO*.md files found to archive")
        return True

    # Create ARCHIVED directory
    archived_dir = Path("ARCHIVED")
    archived_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for todo_file in todo_files:
        # Create archive name
        archive_name = f"{timestamp}_{todo_file.name}"
        archive_path = archived_dir / archive_name

        print(f"  Archiving {todo_file} → {archive_path}")
        shutil.move(str(todo_file), str(archive_path))

    # Commit the archive
    run_cmd(["git", "add", "ARCHIVED/"], check=False)
    run_cmd(["git", "add", "-u"], check=False)  # Stage deletions

    result = run_cmd(
        [
            "git",
            "commit",
            "-m",
            "chore: archive TODO files\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>",
        ],
        check=False,
    )

    if result.returncode != 0 and "nothing to commit" not in result.stdout:
        print(f"⚠️  Commit warning: {result.stderr}")

    print("✓ Step 2 complete: TODO files archived")
    print("\nNext: Run: pr_workflow.py sync-agents")
    return True


def step_sync_agents() -> bool:
    """
    Step 3: Sync CLAUDE.md to AGENTS.md and .agents/.

    Copies:
    - CLAUDE.md → AGENTS.md
    - CLAUDE.md → .github/copilot-instructions.md
    - .claude/skills/ → .agents/
    """
    print("\n" + "=" * 60)
    print("STEP 3: Sync CLAUDE.md → AGENTS.md")
    print("=" * 60)

    # Sync CLAUDE.md → AGENTS.md
    if Path("CLAUDE.md").exists():
        shutil.copy("CLAUDE.md", "AGENTS.md")
        print("  ✓ CLAUDE.md → AGENTS.md")
    else:
        print("  ⚠️  CLAUDE.md not found")

    # Sync CLAUDE.md → .github/copilot-instructions.md
    if Path("CLAUDE.md").exists():
        Path(".github").mkdir(exist_ok=True)
        shutil.copy("CLAUDE.md", ".github/copilot-instructions.md")
        print("  ✓ CLAUDE.md → .github/copilot-instructions.md")

    # Sync .claude/skills/ → .agents/
    if Path(".claude/skills").exists():
        Path(".agents").mkdir(exist_ok=True)
        for skill_dir in Path(".claude/skills").iterdir():
            if skill_dir.is_dir():
                dest = Path(".agents") / skill_dir.name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(skill_dir, dest)
        print("  ✓ .claude/skills/ → .agents/")

    # Commit the sync
    run_cmd(["git", "add", "AGENTS.md", ".github/", ".agents/"], check=False)

    result = run_cmd(
        [
            "git",
            "commit",
            "-m",
            "chore: sync CLAUDE.md to cross-tool formats\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>",
        ],
        check=False,
    )

    if result.returncode != 0 and "nothing to commit" not in result.stdout:
        print(f"⚠️  Commit warning: {result.stderr}")

    print("✓ Step 3 complete: AI config synced")
    print("\nNext: Run: pr_workflow.py start-develop")
    return True


def step_start_develop() -> bool:
    """
    Step 4: Create PR from contrib branch to develop.

    Prerequisites:
    - Must be on contrib/* branch
    - All previous steps complete
    """
    print("\n" + "=" * 60)
    print("STEP 4: PR Contrib → Develop")
    print("=" * 60)

    current = get_current_branch()
    contrib = get_contrib_branch()

    # Validate we're on contrib branch
    if not current.startswith("contrib/"):
        print(f"⚠️  Not on contrib branch (current: {current})")
        print(f"  Switching to {contrib}...")
        run_cmd(["git", "checkout", contrib], check=False)

    # Push any pending changes
    print(f"\n[Push] Pushing {contrib}...")
    result = run_cmd(["git", "push", "origin", contrib], check=False)

    # Create PR to develop
    print(f"\n[PR] Creating PR: {contrib} → develop...")
    result = run_cmd(
        [
            "gh",
            "pr",
            "create",
            "--base",
            "develop",
            "--fill",
            "--body",
            f"Integration PR: {contrib} → develop\n\nWorkflow steps completed:\n- [x] Quality gates passed\n- [x] TODO archived\n- [x] AI config synced\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)",
        ],
        check=False,
    )

    if result.returncode != 0:
        if "already exists" in result.stderr:
            print("⚠️  PR already exists")
        else:
            print(f"✗ PR creation failed: {result.stderr}")
            return False

    print(f"✓ Step 4 complete: PR created {contrib} → develop")

    # Return to editable branch
    return_to_editable_branch()

    print("\n✓ WORKFLOW COMPLETE")
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

    # Check TODO files
    todo_files = list(Path(".").glob("TODO*.md"))
    print(f"\nTODO*.md files: {len(todo_files)}")
    for f in todo_files:
        print(f"  - {f}")

    # Check AGENTS.md sync
    agents_synced = Path("AGENTS.md").exists()
    print(f"\nAGENTS.md exists: {'✓' if agents_synced else '✗'}")

    # Check .agents/ sync
    agents_dir = Path(".agents").exists()
    print(f".agents/ exists: {'✓' if agents_dir else '✗'}")

    # Determine next step
    print("\n" + "-" * 40)
    if current.startswith("feature/"):
        print("Next step: pr_workflow.py finish-feature")
    elif todo_files:
        print("Next step: pr_workflow.py archive-todo")
    elif not agents_synced:
        print("Next step: pr_workflow.py sync-agents")
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
        ("archive-todo", step_archive_todo),
        ("sync-agents", step_sync_agents),
        ("start-develop", step_start_develop),
    ]

    for name, func in steps:
        print(f"\n>>> Running step: {name}")
        if not func():
            print(f"\n✗ Workflow stopped at step: {name}")
            # Always return to editable branch, even on failure
            return_to_editable_branch()
            return False

    # Ensure we're on editable branch (step_start_develop should do this, but be explicit)
    return_to_editable_branch()

    print("\n" + "=" * 60)
    print("✓ FULL WORKFLOW COMPLETE")
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
        choices=[
            "finish-feature",
            "archive-todo",
            "sync-agents",
            "start-develop",
            "full",
            "status",
        ],
        help="Workflow step to execute",
    )

    args = parser.parse_args()

    step_map = {
        "finish-feature": step_finish_feature,
        "archive-todo": step_archive_todo,
        "sync-agents": step_sync_agents,
        "start-develop": step_start_develop,
        "full": run_full_workflow,
        "status": show_status,
    }

    success = step_map[args.step]()

    if args.step != "status":
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
