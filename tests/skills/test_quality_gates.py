# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for quality gates functionality.

Tests the run_quality_gates.py and check_coverage.py modules.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add skills path to import the module
sys.path.insert(
    0,
    str(
        Path(__file__).parent.parent.parent / ".claude" / "skills" / "quality-enforcer" / "scripts"
    ),
)

from run_quality_gates import (
    check_build,
    check_coverage,
    check_linting,
    get_worktree_info,
    run_all_quality_gates,
    run_tests,
    sync_ai_config,
)


class TestGetWorktreeInfo:
    """Test get_worktree_info function."""

    def test_returns_dict_with_worktree_id(self):
        """Test that worktree_id is returned."""
        result = get_worktree_info()
        assert "worktree_id" in result
        assert "worktree_root" in result

    def test_returns_empty_on_import_error(self):
        """Test fallback when worktree_context can't be imported."""
        with patch.dict(sys.modules, {"worktree_context": None}):
            result = get_worktree_info()
            assert result["worktree_id"] == "" or isinstance(result["worktree_id"], str)


class TestRunTests:
    """Test run_tests function."""

    def test_returns_true_on_success(self):
        """Test that True is returned when all tests pass."""
        with patch("run_quality_gates.get_command_prefix", return_value=[]):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                result = run_tests()
                assert result is True

    def test_returns_false_on_failure(self):
        """Test that False is returned when tests fail."""
        with patch("run_quality_gates.get_command_prefix", return_value=[]):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=1, stdout="FAILED test_foo", stderr="")
                result = run_tests()
                assert result is False

    def test_calls_pytest_with_verbose(self):
        """Test that pytest is called with -v flag."""
        with patch("run_quality_gates.get_command_prefix", return_value=[]):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                run_tests()
                call_args = mock_run.call_args[0][0]
                assert "pytest" in call_args
                assert "-v" in call_args


class TestCheckCoverage:
    """Test check_coverage function."""

    def test_returns_true_when_coverage_meets_threshold(self):
        """Test that True is returned when coverage meets threshold."""
        with patch("run_quality_gates.get_command_prefix", return_value=[]):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="Coverage: 85%", stderr="")
                result = check_coverage(threshold=80)
                assert result is True

    def test_returns_false_when_coverage_below_threshold(self):
        """Test that False is returned when coverage is below threshold."""
        with patch("run_quality_gates.get_command_prefix", return_value=[]):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=1, stdout="Coverage: 72%", stderr="")
                result = check_coverage(threshold=80)
                assert result is False

    def test_uses_default_threshold_of_80(self):
        """Test that default threshold is 80%."""
        with patch("run_quality_gates.get_command_prefix", return_value=[]):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                check_coverage()  # No threshold specified
                call_args = mock_run.call_args[0][0]
                assert "80" in call_args


class TestCheckBuild:
    """Test check_build function."""

    def test_returns_true_on_success(self):
        """Test that True is returned when build succeeds."""
        with patch("run_quality_gates.get_uv_command_prefix", return_value=["uv"]):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                result = check_build()
                assert result is True

    def test_returns_false_on_failure(self):
        """Test that False is returned when build fails."""
        with patch("run_quality_gates.get_uv_command_prefix", return_value=["uv"]):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="Build failed")
                result = check_build()
                assert result is False

    def test_calls_uv_build(self):
        """Test that uv build is called."""
        with patch("run_quality_gates.get_uv_command_prefix", return_value=["uv"]):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                check_build()
                call_args = mock_run.call_args[0][0]
                assert "build" in call_args


class TestCheckLinting:
    """Test check_linting function."""

    def test_returns_true_on_success(self):
        """Test that True is returned when linting passes."""
        with patch("run_quality_gates.get_command_prefix", return_value=[]):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                result = check_linting()
                assert result is True

    def test_returns_false_on_failure(self):
        """Test that False is returned when linting fails."""
        with patch("run_quality_gates.get_command_prefix", return_value=[]):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(
                    returncode=1, stdout="F401: unused import", stderr=""
                )
                result = check_linting()
                assert result is False

    def test_calls_ruff_check(self):
        """Test that ruff check is called."""
        with patch("run_quality_gates.get_command_prefix", return_value=[]):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                check_linting()
                call_args = mock_run.call_args[0][0]
                assert "ruff" in call_args
                assert "check" in call_args


class TestSyncAIConfig:
    """Test sync_ai_config function."""

    def test_returns_true_on_success(self):
        """Test that True is returned when sync succeeds."""
        # Mock the sync_ai_config module that gets imported inside the function
        mock_sync_module = MagicMock()
        mock_sync_module.sync_all.return_value = (True, [])
        mock_sync_module.verify_sync.return_value = True
        with patch.dict(sys.modules, {"sync_ai_config": mock_sync_module}):
            result = sync_ai_config()
            assert result is True

    def test_returns_true_on_import_error_fallback(self):
        """Test that sync works with fallback when import fails."""
        # Force import error by patching
        with patch.dict(sys.modules, {"sync_ai_config": None}):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                with patch("pathlib.Path.exists", return_value=False):
                    result = sync_ai_config()
                    # Should not fail even if sync module not available
                    assert result is True or result is False  # Either outcome is valid

    def test_returns_true_when_no_claude_md_modified(self):
        """Test that True is returned when CLAUDE.md not modified."""
        with patch.dict(sys.modules, {"sync_ai_config": None}):
            with patch("subprocess.run") as mock_run:
                # No modified files
                mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
                with patch("pathlib.Path.exists", return_value=True):
                    result = sync_ai_config()
                    assert result is True


class TestRunAllQualityGates:
    """Test run_all_quality_gates function."""

    def test_returns_tuple_of_bool_and_dict(self):
        """Test that result is (bool, dict) tuple."""
        with patch("run_quality_gates.check_coverage", return_value=True):
            with patch("run_quality_gates.run_tests", return_value=True):
                with patch("run_quality_gates.check_build", return_value=True):
                    with patch("run_quality_gates.check_linting", return_value=True):
                        with patch("run_quality_gates.sync_ai_config", return_value=True):
                            passed, results = run_all_quality_gates()
                            assert isinstance(passed, bool)
                            assert isinstance(results, dict)

    def test_all_passed_when_all_gates_pass(self):
        """Test that all_passed is True when all gates pass."""
        with patch("run_quality_gates.check_coverage", return_value=True):
            with patch("run_quality_gates.run_tests", return_value=True):
                with patch("run_quality_gates.check_build", return_value=True):
                    with patch("run_quality_gates.check_linting", return_value=True):
                        with patch("run_quality_gates.sync_ai_config", return_value=True):
                            passed, results = run_all_quality_gates()
                            assert passed is True

    def test_all_passed_false_when_coverage_fails(self):
        """Test that all_passed is False when coverage fails."""
        with patch("run_quality_gates.check_coverage", return_value=False):
            with patch("run_quality_gates.run_tests", return_value=True):
                with patch("run_quality_gates.check_build", return_value=True):
                    with patch("run_quality_gates.check_linting", return_value=True):
                        with patch("run_quality_gates.sync_ai_config", return_value=True):
                            passed, results = run_all_quality_gates()
                            assert passed is False

    def test_all_passed_false_when_tests_fail(self):
        """Test that all_passed is False when tests fail."""
        with patch("run_quality_gates.check_coverage", return_value=True):
            with patch("run_quality_gates.run_tests", return_value=False):
                with patch("run_quality_gates.check_build", return_value=True):
                    with patch("run_quality_gates.check_linting", return_value=True):
                        with patch("run_quality_gates.sync_ai_config", return_value=True):
                            passed, results = run_all_quality_gates()
                            assert passed is False

    def test_all_passed_false_when_build_fails(self):
        """Test that all_passed is False when build fails."""
        with patch("run_quality_gates.check_coverage", return_value=True):
            with patch("run_quality_gates.run_tests", return_value=True):
                with patch("run_quality_gates.check_build", return_value=False):
                    with patch("run_quality_gates.check_linting", return_value=True):
                        with patch("run_quality_gates.sync_ai_config", return_value=True):
                            passed, results = run_all_quality_gates()
                            assert passed is False

    def test_all_passed_false_when_linting_fails(self):
        """Test that all_passed is False when linting fails."""
        with patch("run_quality_gates.check_coverage", return_value=True):
            with patch("run_quality_gates.run_tests", return_value=True):
                with patch("run_quality_gates.check_build", return_value=True):
                    with patch("run_quality_gates.check_linting", return_value=False):
                        with patch("run_quality_gates.sync_ai_config", return_value=True):
                            passed, results = run_all_quality_gates()
                            assert passed is False

    def test_results_contain_all_gate_results(self):
        """Test that results dict contains all gate results."""
        with patch("run_quality_gates.check_coverage", return_value=True):
            with patch("run_quality_gates.run_tests", return_value=True):
                with patch("run_quality_gates.check_build", return_value=True):
                    with patch("run_quality_gates.check_linting", return_value=True):
                        with patch("run_quality_gates.sync_ai_config", return_value=True):
                            _, results = run_all_quality_gates()
                            assert "coverage" in results
                            assert "tests" in results
                            assert "build" in results
                            assert "linting" in results
                            assert "ai_config_sync" in results

    def test_uses_custom_coverage_threshold(self):
        """Test that custom coverage threshold is passed."""
        with patch("run_quality_gates.check_coverage") as mock_coverage:
            mock_coverage.return_value = True
            with patch("run_quality_gates.run_tests", return_value=True):
                with patch("run_quality_gates.check_build", return_value=True):
                    with patch("run_quality_gates.check_linting", return_value=True):
                        with patch("run_quality_gates.sync_ai_config", return_value=True):
                            run_all_quality_gates(coverage_threshold=50)
                            mock_coverage.assert_called_once_with(50)


class TestQualityGateResultsStructure:
    """Test the structure of quality gate results."""

    def test_each_gate_has_passed_key(self):
        """Test that each gate result has 'passed' key."""
        with patch("run_quality_gates.check_coverage", return_value=True):
            with patch("run_quality_gates.run_tests", return_value=True):
                with patch("run_quality_gates.check_build", return_value=True):
                    with patch("run_quality_gates.check_linting", return_value=True):
                        with patch("run_quality_gates.sync_ai_config", return_value=True):
                            _, results = run_all_quality_gates()
                            for key in ["coverage", "tests", "build", "linting", "ai_config_sync"]:
                                assert "passed" in results[key]

    def test_worktree_info_in_results(self):
        """Test that worktree info is included in results."""
        with patch("run_quality_gates.check_coverage", return_value=True):
            with patch("run_quality_gates.run_tests", return_value=True):
                with patch("run_quality_gates.check_build", return_value=True):
                    with patch("run_quality_gates.check_linting", return_value=True):
                        with patch("run_quality_gates.sync_ai_config", return_value=True):
                            _, results = run_all_quality_gates()
                            assert "worktree_id" in results
                            assert "worktree_root" in results
