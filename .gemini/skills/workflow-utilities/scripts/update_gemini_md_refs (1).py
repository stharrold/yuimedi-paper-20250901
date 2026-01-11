#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Update existing GEMINI.md files to include new children references.

This script updates skill GEMINI.md files to include references to newly
created scripts/, templates/, and schemas/ GEMINI.md files.

Usage:
    python update_gemini_md_refs.py [--dry-run]

Created: 2025-11-23
"""

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.parent.parent


def update_skill_gemini_md(skill_path: Path, dry_run: bool = False) -> bool:
    """Update a skill's GEMINI.md to include new children."""
    gemini_md = skill_path / "GEMINI.md"

    if not gemini_md.exists():
        print(f"  SKIP: {skill_path.name} (no GEMINI.md)")
        return False

    content = gemini_md.read_text()

    # Find existing children in YAML frontmatter
    children_match = re.search(r"^children:\n((?:  - .+\n)*)", content, re.MULTILINE)

    if not children_match:
        print(f"  SKIP: {skill_path.name} (no children section)")
        return False

    existing_children = children_match.group(1)

    # Determine what new children should exist
    new_children = []
    for subdir in ("scripts", "templates", "schemas"):
        subdir_path = skill_path / subdir
        if subdir_path.exists() and (subdir_path / "GEMINI.md").exists():
            child_ref = f"{subdir}/GEMINI.md"
            if child_ref not in existing_children:
                new_children.append(child_ref)

    if not new_children:
        print(f"  OK: {skill_path.name} (no updates needed)")
        return False

    # Build new children section
    # Parse existing children
    existing_list = re.findall(r"  - (.+)", existing_children)

    # Add new children, maintaining order: ARCHIVED first, then scripts, templates, schemas
    all_children = existing_list.copy()
    for new_child in new_children:
        if new_child not in all_children:
            all_children.append(new_child)

    # Sort: ARCHIVED first, then alphabetically
    def sort_key(x):
        if "ARCHIVED" in x:
            return (0, x)
        return (1, x)

    all_children.sort(key=sort_key)

    new_children_section = "children:\n" + "".join(f"  - {c}\n" for c in all_children)

    # Replace in content
    new_content = re.sub(
        r"^children:\n((?:  - .+\n)*)", new_children_section, content, flags=re.MULTILINE
    )

    if dry_run:
        print(f"  UPDATE: {skill_path.name}")
        print(f"    Adding: {new_children}")
        return True

    gemini_md.write_text(new_content)
    print(f"  UPDATED: {skill_path.name}")
    print(f"    Added: {new_children}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Update GEMINI.md children references")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying")
    args = parser.parse_args()

    skills_dir = REPO_ROOT / ".gemini" / "skills"

    print(f"Updating skill GEMINI.md files in: {skills_dir}\n")

    updated = 0
    for skill in sorted(skills_dir.iterdir()):
        if skill.is_dir() and not skill.name.startswith("."):
            if update_skill_gemini_md(skill, dry_run=args.dry_run):
                updated += 1

    print(f"\n{'[DRY-RUN] ' if args.dry_run else ''}Updated {updated} GEMINI.md files")


if __name__ == "__main__":
    main()
