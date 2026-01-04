#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
import os
import re
from pathlib import Path

import yaml

ROOT_DIR = Path(".")
IGNORE_DIRS = {
    ".git",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    ".gemini-state",
    ".claude-state",
}


def update_gemini_md(dir_path):
    gemini_path = dir_path / "GEMINI.md"
    if not gemini_path.exists():
        return

    # Find children
    children = []
    try:
        for item in dir_path.iterdir():
            if item.is_dir() and item.name not in IGNORE_DIRS:
                child_gemini = item / "GEMINI.md"
                if child_gemini.exists():
                    children.append(f"{item.name}/GEMINI.md")
    except PermissionError:
        return

    children.sort()

    # Read existing content
    content = gemini_path.read_text()

    # Parse frontmatter using regex to be robust against different newline styles
    # Match: start of file, ---, newline, content, newline, ---, newline or end
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)

    if match:
        frontmatter_raw = match.group(1)
        body = match.group(2)

        try:
            data = yaml.safe_load(frontmatter_raw)
            if data is None:
                data = {}

            # Update children
            data["children"] = children if children else []

            # Update parent if not root
            if dir_path.resolve() != ROOT_DIR.resolve():
                data["parent"] = "../GEMINI.md"
            else:
                data["parent"] = None

            # Reconstruct
            new_frontmatter = yaml.dump(data, sort_keys=False, default_flow_style=False).strip()
            new_content = f"---\n{new_frontmatter}\n---\n{body}"

            if new_content != content:
                gemini_path.write_text(new_content)
                print(f"Updated: {gemini_path}")
        except Exception as e:
            print(f"Error parsing/updating {gemini_path}: {e}")
    else:
        # If no frontmatter, create it?
        # For now, just warn or skip
        # print(f"Skipping {gemini_path}: No valid frontmatter found")
        pass


def main():
    for dir_path, dirs, files in os.walk(ROOT_DIR):
        # Filter ignore dirs
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        update_gemini_md(Path(dir_path))


if __name__ == "__main__":
    main()
