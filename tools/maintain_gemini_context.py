#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
import os
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
    for item in dir_path.iterdir():
        if item.is_dir() and item.name not in IGNORE_DIRS:
            child_gemini = item / "GEMINI.md"
            if child_gemini.exists():
                children.append(f"{item.name}/GEMINI.md")

    children.sort()

    # Read existing content
    content = gemini_path.read_text()

    # Parse frontmatter
    if content.startswith("---\n"):
        parts = content.split("---\\n", 2)
        if len(parts) >= 3:
            frontmatter_raw = parts[1]
            body = parts[2]

            try:
                data = yaml.safe_load(frontmatter_raw)

                # Update children
                data["children"] = children

                # Update parent if not root
                if dir_path != ROOT_DIR:
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
                print(f"Error parsing {gemini_path}: {e}")


def main():
    for dir_path, dirs, files in os.walk(ROOT_DIR):
        # Filter ignore dirs
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        update_gemini_md(Path(dir_path))


if __name__ == "__main__":
    main()
