# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Tests for check_spdx_headers.py script.

Tests cover:
- Files with/without SPDX headers
- Empty __init__.py handling
- Excluded directory logic
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


@pytest.fixture
def spdx_module(skills_dir: Path):
    """Import the check_spdx_headers module."""
    scripts_path = skills_dir / "workflow-utilities" / "scripts"
    sys.path.insert(0, str(scripts_path))
    try:
        import check_spdx_headers

        yield check_spdx_headers
    finally:
        sys.path.pop(0)
        if "check_spdx_headers" in sys.modules:
            del sys.modules["check_spdx_headers"]


class TestShouldCheckFile:
    """Tests for should_check_file function."""

    def test_python_file_should_be_checked(self, spdx_module, tmp_path: Path) -> None:
        """Regular Python files should be checked."""
        py_file = tmp_path / "script.py"
        py_file.write_text("# test")
        assert spdx_module.should_check_file(py_file) is True

    def test_init_file_should_be_checked(self, spdx_module, tmp_path: Path) -> None:
        """__init__.py files should be checked (not exempted)."""
        init_file = tmp_path / "__init__.py"
        init_file.write_text("")
        assert spdx_module.should_check_file(init_file) is True

    def test_non_python_file_should_not_be_checked(self, spdx_module, tmp_path: Path) -> None:
        """Non-Python files should not be checked."""
        md_file = tmp_path / "README.md"
        md_file.write_text("# README")
        assert spdx_module.should_check_file(md_file) is False

        json_file = tmp_path / "config.json"
        json_file.write_text("{}")
        assert spdx_module.should_check_file(json_file) is False

    @pytest.mark.parametrize(
        "excluded_dir",
        [
            ".venv",
            ".git",
            ".tmp",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            "node_modules",
            "ARCHIVED",
        ],
    )
    def test_excluded_directories_should_be_skipped(
        self, spdx_module, tmp_path: Path, excluded_dir: str
    ) -> None:
        """Files in excluded directories should not be checked."""
        excluded_path = tmp_path / excluded_dir / "script.py"
        excluded_path.parent.mkdir(parents=True, exist_ok=True)
        excluded_path.write_text("# test")
        assert spdx_module.should_check_file(excluded_path) is False

    def test_nested_excluded_directory_should_be_skipped(self, spdx_module, tmp_path: Path) -> None:
        """Files in nested excluded directories should not be checked."""
        nested_path = tmp_path / "src" / ".venv" / "lib" / "module.py"
        nested_path.parent.mkdir(parents=True, exist_ok=True)
        nested_path.write_text("# test")
        assert spdx_module.should_check_file(nested_path) is False


class TestHasSpdxHeader:
    """Tests for has_spdx_header function."""

    def test_file_with_both_headers(self, spdx_module, tmp_path: Path) -> None:
        """File with both SPDX headers should pass."""
        py_file = tmp_path / "script.py"
        py_file.write_text(
            "# SPDX-FileCopyrightText: 2025 Yuimedi Corp.\n"
            "# SPDX-License-Identifier: Apache-2.0\n"
            '"""Module docstring."""\n'
        )
        assert spdx_module.has_spdx_header(py_file) is True

    def test_file_with_shebang_and_headers(self, spdx_module, tmp_path: Path) -> None:
        """File with shebang before SPDX headers should pass."""
        py_file = tmp_path / "script.py"
        py_file.write_text(
            "#!/usr/bin/env python3\n"
            "# SPDX-FileCopyrightText: 2025 Yuimedi Corp.\n"
            "# SPDX-License-Identifier: Apache-2.0\n"
        )
        assert spdx_module.has_spdx_header(py_file) is True

    def test_file_missing_copyright(self, spdx_module, tmp_path: Path) -> None:
        """File missing SPDX copyright should fail."""
        py_file = tmp_path / "script.py"
        py_file.write_text("# SPDX-License-Identifier: Apache-2.0\n")
        assert spdx_module.has_spdx_header(py_file) is False

    def test_file_missing_license(self, spdx_module, tmp_path: Path) -> None:
        """File missing SPDX license should fail."""
        py_file = tmp_path / "script.py"
        py_file.write_text("# SPDX-FileCopyrightText: 2025 Yuimedi Corp.\n")
        assert spdx_module.has_spdx_header(py_file) is False

    def test_file_without_headers(self, spdx_module, tmp_path: Path) -> None:
        """File without any SPDX headers should fail."""
        py_file = tmp_path / "script.py"
        py_file.write_text('"""Module without SPDX headers."""\n\ndef main():\n    pass\n')
        assert spdx_module.has_spdx_header(py_file) is False

    def test_empty_file(self, spdx_module, tmp_path: Path) -> None:
        """Empty file should fail (no headers)."""
        py_file = tmp_path / "empty.py"
        py_file.write_text("")
        assert spdx_module.has_spdx_header(py_file) is False

    def test_headers_in_first_10_lines(self, spdx_module, tmp_path: Path) -> None:
        """Headers within first 10 lines should be detected."""
        py_file = tmp_path / "script.py"
        # Headers at lines 5 and 6 (still within first 10)
        content = (
            "# Comment 1\n"
            "# Comment 2\n"
            "# Comment 3\n"
            "# Comment 4\n"
            "# SPDX-FileCopyrightText: 2025 Yuimedi Corp.\n"
            "# SPDX-License-Identifier: Apache-2.0\n"
        )
        py_file.write_text(content)
        assert spdx_module.has_spdx_header(py_file) is True

    def test_generic_spdx_headers_accepted(self, spdx_module, tmp_path: Path) -> None:
        """Generic SPDX header format should be accepted."""
        py_file = tmp_path / "script.py"
        py_file.write_text(
            "# SPDX-FileCopyrightText: 2024 Other Corp.\n# SPDX-License-Identifier: MIT\n"
        )
        assert spdx_module.has_spdx_header(py_file) is True


class TestExcludeDirs:
    """Tests for EXCLUDE_DIRS constant."""

    def test_exclude_dirs_is_set(self, spdx_module) -> None:
        """EXCLUDE_DIRS should be a set."""
        assert isinstance(spdx_module.EXCLUDE_DIRS, set)

    def test_common_excluded_dirs_present(self, spdx_module) -> None:
        """Common excluded directories should be in EXCLUDE_DIRS."""
        expected = {".venv", ".git", "__pycache__", "ARCHIVED"}
        assert expected.issubset(spdx_module.EXCLUDE_DIRS)


class TestSpdxConstants:
    """Tests for SPDX constant values."""

    def test_spdx_copyright_constant(self, spdx_module) -> None:
        """SPDX_COPYRIGHT should have correct value."""
        assert "SPDX-FileCopyrightText:" in spdx_module.SPDX_COPYRIGHT
        assert "Yuimedi Corp." in spdx_module.SPDX_COPYRIGHT

    def test_spdx_license_constant(self, spdx_module) -> None:
        """SPDX_LICENSE should have correct value."""
        assert "SPDX-License-Identifier:" in spdx_module.SPDX_LICENSE
        assert "Apache-2.0" in spdx_module.SPDX_LICENSE


def test_check_spdx_headers_script_exists(skills_dir: Path) -> None:
    """Verify check_spdx_headers.py script exists."""
    script_path = skills_dir / "workflow-utilities" / "scripts" / "check_spdx_headers.py"
    assert script_path.exists(), f"Script not found at {script_path}"


def test_check_spdx_headers_is_importable(skills_dir: Path) -> None:
    """Verify check_spdx_headers.py has valid Python syntax."""
    script_path = skills_dir / "workflow-utilities" / "scripts" / "check_spdx_headers.py"
    content = script_path.read_text()
    compile(content, str(script_path), "exec")
