#!/usr/bin/env python3
"""Run all quality gates and report results.

Supports multiple execution modes:
- Container mode: Inside container, uses 'uv run' directly
- Local mode with podman-compose: Uses 'podman-compose run --rm dev uv run'
- Local mode without podman-compose: Falls back to 'uv run' directly

The script auto-detects the environment and uses appropriate commands.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def is_container_env():
    """Check if running inside a container."""
    return os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv")


def has_podman_compose():
    """Check if podman-compose is available."""
    try:
        result = subprocess.run(
            ["podman-compose", "--version"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_command_prefix():
    """Get command prefix based on environment.

    Inside container: use 'uv run' directly
    Outside container with podman-compose: use 'podman-compose run --rm dev uv run'
    Outside container without podman-compose: use 'uv run' directly (fallback)
    """
    if is_container_env():
        return ["uv", "run"]
    elif has_podman_compose():
        return ["podman-compose", "run", "--rm", "dev", "uv", "run"]
    else:
        # Fallback to local uv run
        return ["uv", "run"]


def run_tests():
    """Run all tests and verify they pass."""
    print("Running tests...")
    cmd = get_command_prefix() + ["pytest", "-v"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    passed = result.returncode == 0

    if passed:
        print("✓ All tests passed")
    else:
        print("✗ Some tests failed")
        print(result.stdout)
        print(result.stderr)

    return passed


def check_coverage(threshold=80):
    """Check test coverage meets threshold."""
    print(f"Checking coverage (≥{threshold}%)...")

    # Call check_coverage.py script using repo-relative path for container compatibility
    script_path = ".claude/skills/quality-enforcer/scripts/check_coverage.py"
    prefix = get_command_prefix()
    # Replace 'uv run' with 'python' for script execution
    if prefix[-2:] == ["uv", "run"]:
        cmd = prefix[:-2] + ["python", script_path, str(threshold)]
    else:
        cmd = ["python", script_path, str(threshold)]
    result = subprocess.run(cmd, capture_output=True, text=True)

    passed = result.returncode == 0
    print(result.stdout)

    return passed


def check_build():
    """Verify package builds successfully."""
    print("Checking build...")
    prefix = get_command_prefix()
    # For build, we need 'uv build' not 'uv run build'
    if prefix[-2:] == ["uv", "run"]:
        cmd = prefix[:-1] + ["build"]  # uv build
    else:
        cmd = ["uv", "build"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    passed = result.returncode == 0

    if passed:
        print("✓ Build successful")
    else:
        print("✗ Build failed")
        print(result.stderr)

    return passed


def check_linting():
    """Run ruff linting."""
    print("Checking linting...")

    cmd = get_command_prefix() + ["ruff", "check", "."]
    result = subprocess.run(cmd, capture_output=True, text=True)

    passed = result.returncode == 0

    if passed:
        print("✓ Linting passed")
    else:
        print("✗ Linting failed")
        print(result.stdout)

    return passed


def check_todo_frontmatter():
    """Validate TODO*.md files have required YAML frontmatter."""
    print("Checking TODO*.md YAML frontmatter...")

    # Find all TODO*.md files
    todo_files = list(Path(".").glob("TODO*.md"))

    if not todo_files:
        print("⚠️  No TODO*.md files found, skipping")
        return True

    all_valid = True
    required_fields = ["status", "feature", "branch"]

    for todo_file in todo_files:
        try:
            content = todo_file.read_text(encoding="utf-8")

            # Check for YAML frontmatter
            if not content.startswith("---"):
                print(f"✗ {todo_file}: Missing YAML frontmatter (must start with ---)")
                all_valid = False
                continue

            # Find end of frontmatter
            end_idx = content.find("---", 3)
            if end_idx == -1:
                print(f"✗ {todo_file}: YAML frontmatter not closed (missing second ---)")
                all_valid = False
                continue

            frontmatter = content[3:end_idx]

            # Check required fields
            missing = []
            for field in required_fields:
                if f"{field}:" not in frontmatter:
                    missing.append(field)

            if missing:
                print(f"✗ {todo_file}: Missing required fields: {', '.join(missing)}")
                all_valid = False
            else:
                print(f"  ✓ {todo_file}: Valid frontmatter")

        except (OSError, UnicodeDecodeError) as e:
            print(f"✗ {todo_file}: Error reading file ({type(e).__name__}): {e}")
            all_valid = False

    if all_valid:
        print("✓ All TODO*.md files have valid YAML frontmatter")

    return all_valid


def sync_ai_config():
    """Sync CLAUDE.md to cross-tool formats if modified.

    NOTE (PR #226 review feedback): This function copies files but does NOT
    stage them for commit. This is intentional - sync_ai_config() is a pre-commit
    step that runs during quality gates. After running quality gates, you should:
    1. Review the synced files (git status)
    2. Stage them manually (git add AGENTS.md .agents/ .github/)
    3. Commit with your other changes

    This allows developers to review and approve synced changes before commit.
    """
    print("Checking AI assistant configuration...")

    # Check if CLAUDE.md or .claude/ was modified (uncommitted or staged changes)
    try:
        # Get list of uncommitted changes
        git_diff = subprocess.run(
            ["git", "diff", "--name-only"], capture_output=True, text=True, check=False
        )

        # Also check staged files
        git_diff_staged = subprocess.run(
            ["git", "diff", "--name-only", "--cached"], capture_output=True, text=True, check=False
        )

        modified_files = git_diff.stdout + git_diff_staged.stdout

        # Check if CLAUDE.md or .claude/ was modified
        needs_sync = "CLAUDE.md" in modified_files or ".claude/" in modified_files

        if not needs_sync:
            print("⚠️  CLAUDE.md not modified, skipping sync")
            return True

        print("📝 CLAUDE.md modified - syncing to cross-tool formats...")

        # Sync CLAUDE.md → AGENTS.md
        if Path("CLAUDE.md").exists():
            shutil.copy("CLAUDE.md", "AGENTS.md")
            print("  ✓ Synced CLAUDE.md → AGENTS.md")

        # Sync CLAUDE.md → .github/copilot-instructions.md
        if Path("CLAUDE.md").exists():
            Path(".github").mkdir(exist_ok=True)
            shutil.copy("CLAUDE.md", ".github/copilot-instructions.md")
            print("  ✓ Synced CLAUDE.md → .github/copilot-instructions.md")

        # Sync .claude/skills/ → .agents/
        if Path(".claude/skills").exists():
            Path(".agents").mkdir(exist_ok=True)
            # Copy skills to .agents
            for skill_dir in Path(".claude/skills").iterdir():
                if skill_dir.is_dir():
                    dest = Path(".agents") / skill_dir.name
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(skill_dir, dest)
            print("  ✓ Synced .claude/skills/ → .agents/")

        print("✓ AI assistant configuration synced")
        return True

    except Exception as e:
        print(f"⚠️  Sync failed (non-critical): {e}")
        return True  # Don't fail quality gates if sync fails


def run_all_quality_gates(coverage_threshold=80):
    """
    Run all quality gates and report results.

    Returns:
        (passed: bool, results: dict)
    """
    results = {}
    all_passed = True

    print("=" * 60)
    print("QUALITY GATES")
    print("=" * 60)

    # Gate 1: Test Coverage
    print("\n[1/6] Test Coverage...")
    passed = check_coverage(coverage_threshold)
    results["coverage"] = {"passed": passed}
    all_passed &= passed

    # Gate 2: Tests Passing
    print("\n[2/6] Running Tests...")
    passed = run_tests()
    results["tests"] = {"passed": passed}
    all_passed &= passed

    # Gate 3: Build
    print("\n[3/6] Build Check...")
    passed = check_build()
    results["build"] = {"passed": passed}
    all_passed &= passed

    # Gate 4: Linting
    print("\n[4/6] Linting...")
    passed = check_linting()
    results["linting"] = {"passed": passed}
    all_passed &= passed

    # Gate 5: TODO*.md YAML Frontmatter
    print("\n[5/6] TODO*.md Frontmatter...")
    passed = check_todo_frontmatter()
    results["todo_frontmatter"] = {"passed": passed}
    all_passed &= passed

    # Gate 6: AI Assistant Configuration Sync
    print("\n[6/6] AI Assistant Configuration...")
    passed = sync_ai_config()
    results["ai_config_sync"] = {"passed": passed}
    all_passed &= passed

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for gate, result in results.items():
        status = "✓ PASS" if result["passed"] else "✗ FAIL"
        print(f"{gate.upper()}: {status}")

    print("\n" + ("✓ ALL GATES PASSED" if all_passed else "✗ SOME GATES FAILED"))

    # Trigger sync engine (Phase 3 integration)
    try:
        import asyncio

        integration_path = Path(__file__).parent.parent.parent / "agentdb-state-manager" / "scripts"
        if str(integration_path) not in sys.path:
            sys.path.insert(0, str(integration_path))
        from worktree_agent_integration import trigger_sync_completion

        asyncio.run(
            trigger_sync_completion(
                agent_id="assess",
                action="test_complete",
                state_snapshot={
                    "all_passed": all_passed,
                    "coverage_passed": results.get("coverage", {}).get("passed", False),
                    "tests_passed": results.get("tests", {}).get("passed", False),
                    "build_passed": results.get("build", {}).get("passed", False),
                    "linting_passed": results.get("linting", {}).get("passed", False),
                    "todo_frontmatter_passed": results.get("todo_frontmatter", {}).get(
                        "passed", False
                    ),
                    "ai_config_sync_passed": results.get("ai_config_sync", {}).get("passed", False),
                },
                context={},
            )
        )
    except Exception:
        # Graceful degradation: don't fail if sync unavailable
        pass

    return all_passed, results


if __name__ == "__main__":
    passed, _ = run_all_quality_gates()
    sys.exit(0 if passed else 1)
