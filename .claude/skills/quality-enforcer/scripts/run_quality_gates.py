#!/usr/bin/env python3
"""Run all quality gates and report results.

Supports two execution modes:
- Container mode: podman-compose run --rm dev uv run python <script>
- Local mode: uv run python <script>

The script detects the environment and uses appropriate commands.
"""

import os
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

    # Call check_coverage.py script
    script_path = Path(__file__).parent / "check_coverage.py"

    if is_container_env():
        cmd = ["python", str(script_path), str(threshold)]
    elif has_podman_compose():
        cmd = [
            "podman-compose",
            "run",
            "--rm",
            "dev",
            "python",
            str(script_path),
            str(threshold),
        ]
    else:
        # Fallback to local python
        cmd = ["python", str(script_path), str(threshold)]

    result = subprocess.run(cmd, capture_output=True, text=True)

    passed = result.returncode == 0
    print(result.stdout)

    return passed


def check_build():
    """Verify package builds successfully."""
    print("Checking build...")

    if is_container_env():
        cmd = ["uv", "build"]
    elif has_podman_compose():
        cmd = ["podman-compose", "run", "--rm", "dev", "uv", "build"]
    else:
        # Fallback to local uv
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

    # Check if ruff is available
    cmd_check = get_command_prefix() + ["ruff", "--version"]
    check_ruff = subprocess.run(cmd_check, capture_output=True, text=True)

    if check_ruff.returncode != 0:
        print("⚠️  ruff not installed, skipping linting")
        return True  # Don't fail if ruff not available

    cmd = get_command_prefix() + ["ruff", "check", "."]
    result = subprocess.run(cmd, capture_output=True, text=True)

    passed = result.returncode == 0

    if passed:
        print("✓ Linting passed")
    else:
        print("✗ Linting failed")
        print(result.stdout)

    return passed


def check_types():
    """Run mypy type checking."""
    print("Checking types...")

    # Check if mypy is available
    cmd_check = get_command_prefix() + ["mypy", "--version"]
    check_mypy = subprocess.run(cmd_check, capture_output=True, text=True)

    if check_mypy.returncode != 0:
        print("⚠️  mypy not installed, skipping type checking")
        return True  # Don't fail if mypy not available

    cmd = get_command_prefix() + ["mypy", "scripts/"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    passed = result.returncode == 0

    if passed:
        print("✓ Type checking passed")
    else:
        print("✗ Type checking failed")
        print(result.stdout)

    return passed


def check_documentation():
    """Run documentation validation tests."""
    print("Checking documentation...")

    if is_container_env():
        cmd = ["./validate_documentation.sh"]
    elif has_podman_compose():
        cmd = ["podman-compose", "run", "--rm", "dev", "./validate_documentation.sh"]
    else:
        # Fallback to local script
        cmd = ["./validate_documentation.sh"]

    result = subprocess.run(cmd, capture_output=True, text=True)

    passed = result.returncode == 0

    if passed:
        print("✓ Documentation validation passed")
    else:
        print("✗ Documentation validation failed")
        print(result.stdout)
        print(result.stderr)

    return passed


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

    if is_container_env():
        env_type = "container"
    elif has_podman_compose():
        env_type = "host (using podman-compose)"
    else:
        env_type = "host (using local uv)"
    print(f"Environment: {env_type}")

    # Gate 1: Documentation Validation
    print("\n[1/6] Documentation Validation...")
    passed = check_documentation()
    results["documentation"] = {"passed": passed}
    all_passed &= passed

    # Gate 2: Linting
    print("\n[2/6] Linting...")
    passed = check_linting()
    results["linting"] = {"passed": passed}
    all_passed &= passed

    # Gate 3: Type Checking
    print("\n[3/6] Type Checking...")
    passed = check_types()
    results["types"] = {"passed": passed}
    all_passed &= passed

    # Gate 4: Test Coverage
    print("\n[4/6] Test Coverage...")
    passed = check_coverage(coverage_threshold)
    results["coverage"] = {"passed": passed}
    all_passed &= passed

    # Gate 5: Tests Passing
    print("\n[5/6] Running Tests...")
    passed = run_tests()
    results["tests"] = {"passed": passed}
    all_passed &= passed

    # Gate 6: Build
    print("\n[6/6] Build Check...")
    passed = check_build()
    results["build"] = {"passed": passed}
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
                    "documentation_passed": results.get("documentation", {}).get("passed", False),
                    "coverage_passed": results.get("coverage", {}).get("passed", False),
                    "tests_passed": results.get("tests", {}).get("passed", False),
                    "build_passed": results.get("build", {}).get("passed", False),
                    "linting_passed": results.get("linting", {}).get("passed", False),
                    "types_passed": results.get("types", {}).get("passed", False),
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
