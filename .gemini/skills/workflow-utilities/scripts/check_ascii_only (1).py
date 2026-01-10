#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Check that Python files contain only ASCII characters.

This script enforces ASCII-only content in Python files to ensure
compatibility across all platforms and terminals.

Issue: #121

Unicode normalization note:
    This script assumes files are UTF-8 encoded in NFC (Canonical Composition)
    form, which is Python's default. Characters like "e" can be represented as:
      - U+00E9 (precomposed, NFC) - single code point
      - U+0065 U+0301 (decomposed, NFD) - e + combining acute accent
    The script detects both forms as non-ASCII since both contain code points
    > 127. For consistent detection, ensure source files use NFC normalization.

Usage:
    python check_ascii_only.py [--fix] [paths...]

    --fix     Show suggested fixes for non-ASCII characters
    paths     Specific files/directories to check (default: current directory)

Exit codes:
    0 - All files are ASCII-only
    1 - Non-ASCII characters found
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ASCII replacements for common Unicode symbols
#
# Note on variant selectors (U+FE0F):
# Some Unicode symbols have two representations - base form and emoji form.
# The variant selector U+FE0F requests emoji presentation. For example:
#   - U+26A0 (warning sign) = base form
#   - U+26A0 U+FE0F (warning sign + VS16) = emoji presentation
# Both variants are mapped to the same ASCII replacement to handle either form.
# This applies to symbols like warning, info, trash can, etc.
ASCII_REPLACEMENTS = {
    # Checkmarks and status
    "\u2713": "[OK]",  # checkmark
    "\u2714": "[OK]",  # heavy checkmark
    "\u2717": "[FAIL]",  # ballot X
    "\u2718": "[FAIL]",  # heavy ballot X
    "\u26a0": "[WARN]",  # warning (base form)
    "\u26a0\ufe0f": "[WARN]",  # warning (with variant selector)
    "\u2139": "[INFO]",  # info (base form)
    "\u2139\ufe0f": "[INFO]",  # info (with variant selector)
    # Arrows
    "\u2192": "->",  # →
    "\u2190": "<-",  # ←
    "\u2191": "^",  # ↑
    "\u2193": "v",  # ↓
    "\u2283": "=>",  # ⊃
    "\u2205": "0",  # ∅
    "\u2298": "[-]",  # ⊘
    # Bullets
    "\u2022": "*",  # •
    "\u25cf": "*",  # ●
    "\u25cb": "o",  # ○
    # Box drawing
    "\u251c": "|--",  # ├
    "\u2514": "`--",  # └
    "\u2502": "|",  # │
    "\u2500": "-",  # ─
    # Emoji (common ones used in code)
    "\U0001f389": "[DONE]",  # 🎉
    "\U0001f4e6": "[PKG]",  # 📦
    "\U0001f5d1": "[DEL]",  # 🗑
    "\U0001f5d1\ufe0f": "[DEL]",  # 🗑️
    "\U0001f680": "[GO]",  # 🚀
    "\U0001f4cb": "[LIST]",  # 📋
    "\U0001f527": "[FIX]",  # 🔧
    "\U0001f50d": "[FIND]",  # 🔍
    "\U0001f6a8": "[ALERT]",  # 🚨
    "\U0001f916": "[BOT]",  # 🤖
    "\U0001f4cc": "[PIN]",  # 📌
    "\U0001f4c4": "[FILE]",  # 📄
    "\U0001f517": "[LINK]",  # 🔗
    "\U0001f528": "[BUILD]",  # 🔨
    "\u2705": "[OK]",  # ✅
    "\u274c": "[FAIL]",  # ❌
    "\u2049\ufe0f": "[!?]",  # ⁉️
    # Mathematical
    "\u2265": ">=",  # ≥
    "\u2264": "<=",  # ≤
}

# Directories to skip (these are not source code or are auto-generated)
SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    ".eggs",
    "*.egg-info",
    "dist",
    "build",
    ".agents",  # Auto-synced mirror of .gemini/skills/
    "ARCHIVED",  # Deprecated files, not actively maintained
}

# Files to skip (these intentionally contain Unicode for documentation/mapping)
SKIP_FILES = {
    "check_ascii_only.py",  # This script defines Unicode replacement mappings
}


def is_ascii(text: str) -> bool:
    """Check if text contains only ASCII characters."""
    try:
        text.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def find_non_ascii(text: str) -> list[tuple[int, int, str]]:
    """Find all non-ASCII characters in text.

    Returns:
        List of (line_number, column, character) tuples.
    """
    violations = []
    for line_num, line in enumerate(text.split("\n"), start=1):
        for col, char in enumerate(line, start=1):
            if ord(char) > 127:
                violations.append((line_num, col, char))
    return violations


def get_replacement(char: str) -> str | None:
    """Get ASCII replacement for a non-ASCII character."""
    return ASCII_REPLACEMENTS.get(char)


def check_file(file_path: Path, show_fix: bool = False) -> list[str]:
    """Check a single file for non-ASCII characters.

    Returns:
        List of error messages.
    """
    errors = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"{file_path}: Unable to decode as UTF-8")
        return errors
    except OSError as e:
        errors.append(f"{file_path}: Unable to read file: {e}")
        return errors

    if is_ascii(content):
        return []

    violations = find_non_ascii(content)

    for line_num, col, char in violations:
        char_repr = repr(char)
        replacement = get_replacement(char)

        msg = f"{file_path}:{line_num}:{col}: Non-ASCII character {char_repr} (U+{ord(char):04X})"
        if show_fix and replacement:
            msg += f" -> replace with: {replacement}"
        errors.append(msg)

    return errors


def should_skip(path: Path) -> bool:
    """Check if path should be skipped."""
    # Check if filename is in skip list
    if path.name in SKIP_FILES:
        return True
    # Check if any directory in path is in skip list
    for part in path.parts:
        if part in SKIP_DIRS:
            return True
        for pattern in SKIP_DIRS:
            if "*" in pattern and path.match(pattern):
                return True
    return False


def check_paths(paths: list[Path], show_fix: bool = False) -> int:
    """Check multiple paths for non-ASCII characters.

    Returns:
        Exit code (0 = success, 1 = violations found).
    """
    all_errors: list[str] = []

    for path in paths:
        if path.is_file():
            if path.suffix == ".py" and not should_skip(path):
                all_errors.extend(check_file(path, show_fix))
        elif path.is_dir():
            for py_file in path.rglob("*.py"):
                if not should_skip(py_file):
                    all_errors.extend(check_file(py_file, show_fix))

    if all_errors:
        print("Non-ASCII characters found in Python files:\n")
        for error in all_errors:
            print(f"  {error}")
        print(f"\nTotal: {len(all_errors)} non-ASCII character(s) found")
        print("\nFix: Replace Unicode symbols with ASCII equivalents.")
        print("     Use safe_output.py functions: format_check(), format_cross(), etc.")
        return 1

    print("[OK] All Python files contain only ASCII characters")
    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check Python files for non-ASCII characters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Check current directory
    python check_ascii_only.py

    # Check specific files
    python check_ascii_only.py file1.py file2.py

    # Show suggested fixes
    python check_ascii_only.py --fix .gemini/skills/
""",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Show suggested ASCII replacements for non-ASCII characters",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path(".")],
        help="Files or directories to check (default: current directory)",
    )

    args = parser.parse_args()
    return check_paths(args.paths, show_fix=args.fix)


if __name__ == "__main__":
    sys.exit(main())
