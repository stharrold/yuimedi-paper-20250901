#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Check that Python files have SPDX license headers.

This script validates that all Python files in the repository contain
proper SPDX license headers for Apache 2.0 compliance.

Usage:
    python check_spdx_headers.py [--fix]
"""

from __future__ import annotations

import sys
from pathlib import Path

# Directories to exclude from SPDX checking
EXCLUDE_DIRS = {
    ".venv",
    ".git",
    ".tmp",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "ARCHIVED",
    ".agents",  # Read-only mirror synced from .claude/skills/
}

# Required SPDX header lines
SPDX_COPYRIGHT = "# SPDX-FileCopyrightText: 2025 stharrold"
SPDX_LICENSE = "# SPDX-License-Identifier: Apache-2.0"


def should_check_file(path: Path) -> bool:
    """Determine if a file should be checked for SPDX headers."""
    # Skip excluded directories
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return False

    # Only check Python files
    if path.suffix != ".py":
        return False

    # All Python files require SPDX headers, including __init__.py
    return True


def has_spdx_header(path: Path) -> bool:
    """Check if a file has proper SPDX headers."""
    try:
        content = path.read_text()
    except (OSError, UnicodeDecodeError):
        return True  # Skip files we can't read

    lines = content.split("\n")

    # Look for SPDX headers in first 10 lines (allowing for shebang, encoding, etc.)
    header_lines = "\n".join(lines[:10])

    has_copyright = SPDX_COPYRIGHT in header_lines or "SPDX-FileCopyrightText:" in header_lines
    has_license = SPDX_LICENSE in header_lines or "SPDX-License-Identifier:" in header_lines

    return has_copyright and has_license


def main() -> int:
    """Check all Python files for SPDX headers."""
    root = Path.cwd()
    missing_headers: list[Path] = []

    for py_file in root.rglob("*.py"):
        if should_check_file(py_file):
            if not has_spdx_header(py_file):
                missing_headers.append(py_file)

    if missing_headers:
        print("ERROR: The following Python files are missing SPDX license headers:")
        for path in sorted(missing_headers):
            print(f"  - {path.relative_to(root)}")
        print()
        print("Required headers:")
        print(f"  {SPDX_COPYRIGHT}")
        print(f"  {SPDX_LICENSE}")
        print()
        print("Add these lines after the shebang (if present) but before any docstrings.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
