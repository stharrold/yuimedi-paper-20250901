#!/usr/bin/env python3
"""Run all quality gates and report results."""

import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run all tests and verify they pass."""
    print("Running tests...")
    result = subprocess.run(
        ['uv', 'run', 'pytest', '-v'],
        capture_output=True,
        text=True
    )

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
    script_path = Path(__file__).parent / 'check_coverage.py'
    result = subprocess.run(
        ['python', str(script_path), str(threshold)],
        capture_output=True,
        text=True
    )

    passed = result.returncode == 0
    print(result.stdout)

    return passed

def check_build():
    """Verify package builds successfully."""
    print("Checking build...")
    result = subprocess.run(
        ['uv', 'build'],
        capture_output=True,
        text=True
    )

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
    check_ruff = subprocess.run(
        ['uv', 'run', 'ruff', '--version'],
        capture_output=True,
        text=True
    )

    if check_ruff.returncode != 0:
        print("⚠️  ruff not installed, skipping linting")
        return True  # Don't fail if ruff not available

    result = subprocess.run(
        ['uv', 'run', 'ruff', 'check', 'src/', 'tests/'],
        capture_output=True,
        text=True
    )

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
    check_mypy = subprocess.run(
        ['uv', 'run', 'mypy', '--version'],
        capture_output=True,
        text=True
    )

    if check_mypy.returncode != 0:
        print("⚠️  mypy not installed, skipping type checking")
        return True  # Don't fail if mypy not available

    result = subprocess.run(
        ['uv', 'run', 'mypy', 'src/'],
        capture_output=True,
        text=True
    )

    passed = result.returncode == 0

    if passed:
        print("✓ Type checking passed")
    else:
        print("✗ Type checking failed")
        print(result.stdout)

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

    # Gate 1: Test Coverage
    print("\n[1/5] Test Coverage...")
    passed = check_coverage(coverage_threshold)
    results['coverage'] = {'passed': passed}
    all_passed &= passed

    # Gate 2: Tests Passing
    print("\n[2/5] Running Tests...")
    passed = run_tests()
    results['tests'] = {'passed': passed}
    all_passed &= passed

    # Gate 3: Build
    print("\n[3/5] Build Check...")
    passed = check_build()
    results['build'] = {'passed': passed}
    all_passed &= passed

    # Gate 4: Linting
    print("\n[4/5] Linting...")
    passed = check_linting()
    results['linting'] = {'passed': passed}
    all_passed &= passed

    # Gate 5: Type Checking
    print("\n[5/5] Type Checking...")
    passed = check_types()
    results['types'] = {'passed': passed}
    all_passed &= passed

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for gate, result in results.items():
        status = "✓ PASS" if result['passed'] else "✗ FAIL"
        print(f"{gate.upper()}: {status}")

    print("\n" + ("✓ ALL GATES PASSED" if all_passed else "✗ SOME GATES FAILED"))

    # Trigger sync engine (Phase 3 integration)
    try:
        import asyncio
        integration_path = Path(__file__).parent.parent.parent / "agentdb-state-manager" / "scripts"
        if str(integration_path) not in sys.path:
            sys.path.insert(0, str(integration_path))
        from worktree_agent_integration import trigger_sync_completion

        asyncio.run(trigger_sync_completion(
            agent_id="assess",
            action="test_complete",
            state_snapshot={
                "all_passed": all_passed,
                "coverage_passed": results.get('coverage', {}).get('passed', False),
                "tests_passed": results.get('tests', {}).get('passed', False),
                "build_passed": results.get('build', {}).get('passed', False),
                "linting_passed": results.get('linting', {}).get('passed', False),
                "types_passed": results.get('types', {}).get('passed', False)
            },
            context={}
        ))
    except Exception:
        # Graceful degradation: don't fail if sync unavailable
        pass

    return all_passed, results

if __name__ == '__main__':
    passed, _ = run_all_quality_gates()
    sys.exit(0 if passed else 1)
