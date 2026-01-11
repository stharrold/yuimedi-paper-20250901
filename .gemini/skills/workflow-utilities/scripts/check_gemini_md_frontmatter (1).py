#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Pre-commit hook: Check GEMINI.md files have YAML frontmatter."""

import sys
from pathlib import Path


def main() -> int:
    """Check all GEMINI.md files for YAML frontmatter."""
    errors = []
    for f in Path(".").rglob("GEMINI.md"):
        # Skip .agents/ (synced from .gemini/)
        if ".agents/" in str(f):
            continue
        content = f.read_text()
        # Root GEMINI.md and skill GEMINI.md should have frontmatter
        if not content.startswith("---"):
            errors.append(str(f))

    if errors:
        print("GEMINI.md files missing YAML frontmatter:")
        for e in errors:
            print(f"  - {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
