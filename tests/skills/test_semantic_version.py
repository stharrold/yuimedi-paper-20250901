"""Tests for semantic version calculation.

Tests the semantic_version.py module which calculates the next version
based on code changes.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add skills path to import the module
sys.path.insert(
    0,
    str(
        Path(__file__).parent.parent.parent
        / ".claude"
        / "skills"
        / "git-workflow-manager"
        / "scripts"
    ),
)

from semantic_version import (
    analyze_changes,
    bump_version,
    calculate_semantic_version,
    get_changed_files,
)


class TestBumpVersion:
    """Test bump_version function."""

    def test_major_bump(self):
        """Test major version bump."""
        assert bump_version("v1.2.3", "major") == "v2.0.0"

    def test_minor_bump(self):
        """Test minor version bump."""
        assert bump_version("v1.2.3", "minor") == "v1.3.0"

    def test_patch_bump(self):
        """Test patch version bump."""
        assert bump_version("v1.2.3", "patch") == "v1.2.4"

    def test_handles_version_without_v_prefix(self):
        """Test handling of version without v prefix."""
        assert bump_version("1.2.3", "minor") == "v1.3.0"

    def test_invalid_version_defaults_to_v1_0_0(self):
        """Test that invalid version defaults to v1.0.0."""
        assert bump_version("invalid", "minor") == "v1.0.0"

    def test_major_resets_minor_and_patch(self):
        """Test that major bump resets minor and patch to 0."""
        result = bump_version("v1.5.7", "major")
        assert result == "v2.0.0"

    def test_minor_resets_patch(self):
        """Test that minor bump resets patch to 0."""
        result = bump_version("v1.5.7", "minor")
        assert result == "v1.6.0"

    def test_patch_only_increments_patch(self):
        """Test that patch bump only increments patch."""
        result = bump_version("v1.5.7", "patch")
        assert result == "v1.5.8"

    def test_handles_zero_version(self):
        """Test handling of 0.x.x versions."""
        assert bump_version("v0.1.0", "patch") == "v0.1.1"
        assert bump_version("v0.1.0", "minor") == "v0.2.0"
        assert bump_version("v0.1.0", "major") == "v1.0.0"

    def test_handles_large_versions(self):
        """Test handling of large version numbers."""
        assert bump_version("v99.99.99", "patch") == "v99.99.100"
        assert bump_version("v99.99.99", "minor") == "v99.100.0"
        assert bump_version("v99.99.99", "major") == "v100.0.0"


class TestAnalyzeChanges:
    """Test analyze_changes function."""

    def test_api_changes_return_major(self):
        """Test that API changes return major bump."""
        with patch.object(Path, "exists", return_value=True):
            result = analyze_changes(["src/api/routes.py"])
            assert result == "major"

    def test_new_src_files_return_minor(self):
        """Test that new source files return minor bump."""
        with patch.object(Path, "exists", return_value=True):
            result = analyze_changes(["src/new_module.py"])
            assert result == "minor"

    def test_test_changes_return_patch(self):
        """Test that test changes return patch bump."""
        result = analyze_changes(["tests/test_something.py"])
        assert result == "patch"

    def test_docs_changes_return_patch(self):
        """Test that documentation changes return patch bump."""
        result = analyze_changes(["docs/guide.md"])
        assert result == "patch"

    def test_config_changes_return_patch(self):
        """Test that configuration changes return patch bump."""
        result = analyze_changes(["pyproject.toml"])
        assert result == "patch"

    def test_requirements_changes_return_patch(self):
        """Test that requirements changes return patch bump."""
        result = analyze_changes(["requirements.txt"])
        assert result == "patch"

    def test_uv_lock_changes_return_patch(self):
        """Test that uv.lock changes return patch bump."""
        result = analyze_changes(["uv.lock"])
        assert result == "patch"

    def test_multiple_changes_prioritize_breaking(self):
        """Test that multiple changes prioritize breaking (major)."""
        with patch.object(Path, "exists", return_value=True):
            result = analyze_changes(
                [
                    "tests/test_something.py",  # patch
                    "src/new_module.py",  # minor
                    "src/api/routes.py",  # major
                ]
            )
            assert result == "major"

    def test_multiple_changes_prioritize_feature(self):
        """Test that multiple changes prioritize feature (minor) over fix."""
        with patch.object(Path, "exists", return_value=True):
            result = analyze_changes(
                [
                    "tests/test_something.py",  # patch
                    "src/new_module.py",  # minor
                    "docs/readme.md",  # patch
                ]
            )
            assert result == "minor"

    def test_empty_changes_return_patch(self):
        """Test that empty changes default to patch."""
        result = analyze_changes([])
        assert result == "patch"

    def test_unknown_files_return_patch(self):
        """Test that unknown files default to patch."""
        result = analyze_changes(["random_file.xyz"])
        assert result == "patch"

    def test_resources_changes_return_patch(self):
        """Test that resources changes return patch bump."""
        result = analyze_changes(["resources/data.json"])
        assert result == "patch"


class TestGetChangedFiles:
    """Test get_changed_files function."""

    def test_returns_list_of_files(self):
        """Test that changed files are returned as a list."""
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "file1.py\nfile2.py\nfile3.py\n"
            result = get_changed_files("develop")
            assert result == ["file1.py", "file2.py", "file3.py"]

    def test_handles_empty_output(self):
        """Test handling of no changed files."""
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = ""
            result = get_changed_files("develop")
            assert result == []

    def test_handles_single_file(self):
        """Test handling of single changed file."""
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "file1.py\n"
            result = get_changed_files("develop")
            assert result == ["file1.py"]

    def test_filters_empty_lines(self):
        """Test that empty lines are filtered out."""
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "file1.py\n\nfile2.py\n\n"
            result = get_changed_files("develop")
            assert result == ["file1.py", "file2.py"]

    def test_returns_empty_on_error(self):
        """Test that empty list is returned on git error."""
        with patch("subprocess.check_output") as mock_output:
            mock_output.side_effect = subprocess.CalledProcessError(1, "git")
            result = get_changed_files("develop")
            assert result == []

    def test_uses_three_dot_diff(self):
        """Test that three-dot diff is used for comparison."""
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = ""
            get_changed_files("develop")
            call_args = mock_output.call_args[0][0]
            assert "develop...HEAD" in call_args


class TestCalculateSemanticVersion:
    """Test calculate_semantic_version function."""

    def test_returns_current_version_if_no_changes(self):
        """Test that current version is returned if no changes."""
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = ""
            result = calculate_semantic_version("develop", "v1.2.3")
            assert result == "v1.2.3"

    def test_calculates_minor_for_feature_changes(self):
        """Test minor bump for feature changes."""
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "src/new_feature.py\n"
            with patch.object(Path, "exists", return_value=True):
                result = calculate_semantic_version("develop", "v1.2.3")
                assert result == "v1.3.0"

    def test_calculates_patch_for_test_changes(self):
        """Test patch bump for test changes."""
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "tests/test_something.py\n"
            result = calculate_semantic_version("develop", "v1.2.3")
            assert result == "v1.2.4"

    def test_calculates_major_for_api_changes(self):
        """Test major bump for API changes."""
        with patch("subprocess.check_output") as mock_output:
            mock_output.return_value = "src/api/routes.py\n"
            with patch.object(Path, "exists", return_value=True):
                result = calculate_semantic_version("develop", "v1.2.3")
                assert result == "v2.0.0"


class TestVersionFormatHandling:
    """Test handling of various version formats."""

    @pytest.mark.parametrize(
        ("input_version", "expected_major"),
        [
            ("v1.0.0", "v2.0.0"),
            ("1.0.0", "v2.0.0"),
            ("v0.0.1", "v1.0.0"),
            ("v10.20.30", "v11.0.0"),
        ],
    )
    def test_various_input_formats(self, input_version: str, expected_major: str):
        """Test that various input formats produce correct output."""
        result = bump_version(input_version, "major")
        assert result == expected_major

    def test_output_always_has_v_prefix(self):
        """Test that output always has v prefix."""
        result = bump_version("1.0.0", "patch")
        assert result.startswith("v")

    @pytest.mark.parametrize(
        "invalid_version",
        [
            "v1",
            "v1.0",
            "1.0",
            "abc",
            "v1.a.0",
            "",
            "vvv1.0.0",
        ],
    )
    def test_invalid_formats_default_to_v1_0_0(self, invalid_version: str):
        """Test that invalid formats default to v1.0.0."""
        result = bump_version(invalid_version, "minor")
        assert result == "v1.0.0"
