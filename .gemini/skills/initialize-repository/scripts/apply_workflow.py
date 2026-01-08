#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Apply workflow system from a cloned template repository to an existing repository.

This script is designed for the "clone and apply" use case:
1. User navigates to their existing repository
2. User clones stharrold-templates to .tmp/stharrold-templates
3. User tells Gemini Code to apply the workflow

Usage:
    python apply_workflow.py <source-repo> <target-repo> [--force]

Arguments:
    source-repo: Path to cloned stharrold-templates (e.g., .tmp/stharrold-templates)
    target-repo: Path to existing repository (e.g., . or /path/to/my-repo)
    --force: Overwrite .gemini/ directory without prompting

Example:
    cd my-repo
    mkdir -p .tmp
    git clone https://github.com/stharrold/stharrold-templates.git .tmp/stharrold-templates
    python .tmp/stharrold-templates/.gemini/skills/initialize-repository/scripts/apply_workflow.py \\
      .tmp/stharrold-templates .

What it does:
1. Validates source has .gemini/skills/ and .gemini/commands/
2. Validates target is a git repository
3. Prompts before overwriting existing .gemini/ (unless --force)
4. Copies .gemini/skills/ (all skills)
5. Copies .gemini/commands/ (v7x1 workflow commands)
6. Copies WORKFLOW.md, CONTRIBUTING.md
7. Merges pyproject.toml (adds dev dependencies, preserves existing)
8. Merges .gitignore (appends workflow patterns, deduplicates)
9. Prints summary with next steps

Exit codes:
    0: Success
    1: Source validation failed
    2: Target validation failed
    3: User cancelled (declined overwrite prompt)
"""

import argparse
import os
import shutil
import sys
import tempfile
import tomllib
from pathlib import Path

# Add workflow-utilities to path for safe_output
# Use resolve() to get canonical path and validate it's within expected structure
_script_dir = Path(__file__).resolve().parent
_skills_dir = _script_dir.parent.parent
_utils_path = (_skills_dir / "workflow-utilities" / "scripts").resolve()
# Validate path is within skills directory (prevents path traversal attacks)
if not str(_utils_path).startswith(str(_skills_dir.resolve())):
    raise RuntimeError("Invalid path: workflow-utilities not in expected location")
sys.path.insert(0, str(_utils_path))
from safe_output import (  # noqa: E402
    SYMBOLS,
    print_error,
    print_info,
    print_success,
    print_warning,
)

# Module-level constants to avoid duplication and make updates easier
# These are the minimum versions required for the workflow system
DEFAULT_DEV_DEPENDENCIES = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "pre-commit>=3.6.0",
]

# Minimum number of skills expected in a complete workflow system.
# The full system has 6+ skills (workflow-orchestrator, git-workflow-manager,
# tech-stack-adapter, workflow-utilities, agentdb-state-manager, initialize-repository).
# We require at least 3 to catch incomplete or corrupted installations.
MIN_EXPECTED_SKILLS = 3


def validate_source(source_path: Path) -> tuple[bool, str]:
    """Validate source repository has workflow system.

    Args:
        source_path: Path to source repository

    Returns:
        Tuple of (is_valid, message)
    """
    if not source_path.exists():
        return False, f"Source path does not exist: {source_path}"

    if not source_path.is_dir():
        return False, f"Source path is not a directory: {source_path}"

    skills_dir = source_path / ".gemini" / "skills"
    if not skills_dir.exists():
        return False, "Source missing .gemini/skills/ directory"

    commands_dir = source_path / ".gemini" / "commands"
    if not commands_dir.exists():
        return False, "Source missing .gemini/commands/ directory"

    # Count skills
    skills = [d.name for d in skills_dir.iterdir() if d.is_dir()]
    if len(skills) < MIN_EXPECTED_SKILLS:
        return (
            False,
            f"Source has incomplete workflow system ({len(skills)} skills, need {MIN_EXPECTED_SKILLS}+)",
        )

    return True, f"Source validated ({len(skills)} skills found)"


def validate_target(target_path: Path) -> tuple[bool, str]:
    """Validate target is a git repository.

    Args:
        target_path: Path to target repository

    Returns:
        Tuple of (is_valid, message)
    """
    if not target_path.exists():
        return False, f"Target path does not exist: {target_path}"

    if not target_path.is_dir():
        return False, f"Target path is not a directory: {target_path}"

    # Check if it's a git repository
    # Note: .git can be a directory (normal repo) or a file (worktree)
    git_path = target_path / ".git"
    if not git_path.exists():
        return False, "Target is not a git repository (no .git)"

    return True, "Target validated (git repository)"


def prompt_overwrite(target_path: Path) -> bool:
    """Prompt user before overwriting .gemini/ directory.

    Args:
        target_path: Path to target repository

    Returns:
        True if user confirms, False otherwise
    """
    gemini_dir = target_path / ".gemini"
    if not gemini_dir.exists():
        return True  # Nothing to overwrite

    print_warning("Target repository already has .gemini/ directory")
    print_warning("Existing .gemini/ will be replaced")

    response = input("\nProceed with workflow application? (y/N) ").strip().lower()
    return response in ["y", "yes"]


def copy_skills(source_path: Path, target_path: Path, force: bool) -> int:
    """Copy .gemini/skills/ directory using atomic replacement.

    Uses a two-phase approach for safety: copies to a temporary location first,
    then replaces the target only if the copy succeeds. This prevents data loss
    if the copy operation fails partway through.

    Args:
        source_path: Path to source repository
        target_path: Path to target repository
        force: If True, delete existing before copying

    Returns:
        Number of skills copied
    """
    print_info("Copying .gemini/skills/ directory...")

    source_skills = source_path / ".gemini" / "skills"
    target_skills = target_path / ".gemini" / "skills"
    target_skills.parent.mkdir(parents=True, exist_ok=True)

    if force and target_skills.exists():
        # Use atomic replacement with backup: copy to temp, rename old to backup,
        # rename temp to target, delete backup. This prevents race conditions.
        with tempfile.TemporaryDirectory(dir=target_skills.parent) as tmp_dir:
            tmp_skills = Path(tmp_dir) / "skills"
            backup_skills = target_skills.parent / f"skills.backup.{os.getpid()}"
            try:
                shutil.copytree(source_skills, tmp_skills)
                # Atomic rename: old -> backup
                target_skills.rename(backup_skills)
                try:
                    # Atomic rename: temp -> target
                    shutil.move(str(tmp_skills), str(target_skills))
                    # Success - remove backup
                    shutil.rmtree(backup_skills)
                except Exception:
                    # Restore from backup if move failed
                    backup_skills.rename(target_skills)
                    raise
            except PermissionError as e:
                raise PermissionError(f"Permission denied copying skills: {e}") from e
    else:
        # No existing directory or not force, just copy
        try:
            shutil.copytree(source_skills, target_skills, dirs_exist_ok=True)
        except PermissionError as e:
            raise PermissionError(f"Permission denied copying skills: {e}") from e

    # Count and report skills
    skills = [d.name for d in target_skills.iterdir() if d.is_dir()]
    for skill in sorted(skills):
        print_success(f"Copied skill: {skill}")

    print_success(f"Copied {len(skills)} skills")
    return len(skills)


def copy_commands(source_path: Path, target_path: Path, force: bool) -> int:
    """Copy .gemini/commands/ directory using atomic replacement.

    Uses a two-phase approach for safety: copies to a temporary location first,
    then replaces the target only if the copy succeeds. This prevents data loss
    if the copy operation fails partway through.

    Args:
        source_path: Path to source repository
        target_path: Path to target repository
        force: If True, delete existing before copying

    Returns:
        Number of commands copied
    """
    print_info("Copying .gemini/commands/ directory...")

    source_commands = source_path / ".gemini" / "commands"
    target_commands = target_path / ".gemini" / "commands"

    if not source_commands.exists():
        print_warning("Source has no .gemini/commands/ directory")
        return 0

    target_commands.parent.mkdir(parents=True, exist_ok=True)

    if force and target_commands.exists():
        # Use atomic replacement with backup: copy to temp, rename old to backup,
        # rename temp to target, delete backup. This prevents race conditions.
        with tempfile.TemporaryDirectory(dir=target_commands.parent) as tmp_dir:
            tmp_commands = Path(tmp_dir) / "commands"
            backup_commands = target_commands.parent / f"commands.backup.{os.getpid()}"
            try:
                shutil.copytree(source_commands, tmp_commands)
                # Atomic rename: old -> backup
                target_commands.rename(backup_commands)
                try:
                    # Atomic rename: temp -> target
                    shutil.move(str(tmp_commands), str(target_commands))
                    # Success - remove backup
                    shutil.rmtree(backup_commands)
                except Exception:
                    # Restore from backup if move failed
                    backup_commands.rename(target_commands)
                    raise
            except PermissionError as e:
                raise PermissionError(f"Permission denied copying commands: {e}") from e
    else:
        # No existing directory or not force, just copy
        try:
            shutil.copytree(source_commands, target_commands, dirs_exist_ok=True)
        except PermissionError as e:
            raise PermissionError(f"Permission denied copying commands: {e}") from e

    # Count command files (*.md in workflow/)
    workflow_dir = target_commands / "workflow"
    if not workflow_dir.exists():
        print_warning("Workflow directory not found after copying commands")
        return 0

    commands = list(workflow_dir.glob("v7x1_*.md"))
    if not commands:
        print_warning("No v7x1_* workflow commands found in commands/workflow/")
        return 0

    for cmd in sorted(commands):
        print_success(f"Copied command: {cmd.stem}")
    print_success(f"Copied {len(commands)} workflow commands")
    return len(commands)


def copy_documentation(source_path: Path, target_path: Path) -> list[str]:
    """Copy workflow documentation files.

    Args:
        source_path: Path to source repository
        target_path: Path to target repository

    Returns:
        List of copied file names
    """
    print_info("Copying workflow documentation...")

    docs = ["WORKFLOW.md", "CONTRIBUTING.md"]
    copied = []

    for doc in docs:
        source_file = source_path / doc
        if source_file.exists():
            target_file = target_path / doc
            shutil.copy2(source_file, target_file)
            print_success(f"Copied {doc}")
            copied.append(doc)

    return copied


def extract_dev_deps_from_toml(toml_data: dict) -> list[str]:
    """Extract dev dependencies from parsed TOML data.

    Checks multiple locations in order of preference:
    1. [dependency-groups].dev (PEP 735, uv)
    2. [tool.uv].dev-dependencies (older uv format)
    3. [project.optional-dependencies].dev (setuptools/pip)

    Args:
        toml_data: Parsed TOML dictionary

    Returns:
        List of dependency strings, or empty list if not found
    """
    # Check [dependency-groups].dev (PEP 735)
    if "dependency-groups" in toml_data:
        dev = toml_data["dependency-groups"].get("dev", [])
        if dev:
            return list(dev)

    # Check [tool.uv].dev-dependencies (older uv format)
    if "tool" in toml_data and "uv" in toml_data["tool"]:
        dev = toml_data["tool"]["uv"].get("dev-dependencies", [])
        if dev:
            return list(dev)

    # Check [project.optional-dependencies].dev (setuptools/pip)
    if "project" in toml_data:
        optional = toml_data["project"].get("optional-dependencies", {})
        dev = optional.get("dev", [])
        if dev:
            return list(dev)

    return []


def merge_pyproject_toml(source_path: Path, target_path: Path) -> bool:
    """Merge dev dependencies into target pyproject.toml.

    Uses tomllib to properly parse TOML and extract dev dependencies
    from multiple possible locations.

    Args:
        source_path: Path to source repository
        target_path: Path to target repository

    Returns:
        True if merged, False if skipped
    """
    print_info("Merging pyproject.toml...")

    source_file = source_path / "pyproject.toml"
    target_file = target_path / "pyproject.toml"

    if not source_file.exists():
        print_warning("Source has no pyproject.toml")
        return False

    # Parse source TOML properly using tomllib
    try:
        with source_file.open("rb") as f:
            source_data = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        print_warning(f"Source pyproject.toml is invalid: {e}")
        return False

    # Extract dev dependencies from source
    dev_deps = extract_dev_deps_from_toml(source_data)

    if not dev_deps:
        # Fallback: use module-level default dev deps
        dev_deps = DEFAULT_DEV_DEPENDENCIES.copy()

    # Format dev deps for TOML output
    formatted_deps = ",\n    ".join(f'"{dep}"' for dep in dev_deps)

    if not target_file.exists():
        # Create minimal pyproject.toml
        target_name = target_path.name
        content = f'''[project]
name = "{target_name}"
version = "0.1.0"
description = ""
requires-python = ">=3.11"
dependencies = []

[dependency-groups]
dev = [
    {formatted_deps},
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

[tool.ruff]
line-length = 170
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "B", "UP"]
'''
        target_file.write_text(content)
        print_success("Created pyproject.toml with dev dependencies")
        return True

    # Parse target TOML to check for existing dev section
    try:
        with target_file.open("rb") as f:
            target_data = tomllib.load(f)
    except tomllib.TOMLDecodeError:
        # If target is invalid, preserve it as-is and warn
        print_warning("Target pyproject.toml is invalid, preserving as-is")
        return True

    # Check if dev section already exists
    existing_deps = extract_dev_deps_from_toml(target_data)
    if existing_deps:
        print_success("pyproject.toml already has dev dependencies (preserved)")
        return True

    # Append dev section to target
    target_content = target_file.read_text()
    dev_section = f"""
[dependency-groups]
dev = [
    {formatted_deps},
]
"""
    new_content = target_content + dev_section
    target_file.write_text(new_content)

    # Validate the resulting TOML is syntactically valid
    try:
        with target_file.open("rb") as f:
            tomllib.load(f)
        print_success("Added dev dependencies to pyproject.toml")
    except tomllib.TOMLDecodeError as e:
        print_warning(f"pyproject.toml may have syntax issues after merge: {e}")
        print_warning("Please review the file manually")

    return True


def merge_gitignore(source_path: Path, target_path: Path) -> bool:
    """Append workflow patterns to .gitignore, deduplicate.

    Adds workflow-specific patterns (.gemini-state/, .tmp/, *.duckdb) to the
    target .gitignore file. Non-blank lines are deduplicated while preserving
    order. Consecutive blank lines are collapsed to a single blank line to
    maintain clean formatting.

    Args:
        source_path: Path to source repository
        target_path: Path to target repository

    Returns:
        True if merged, False if skipped
    """
    print_info("Merging .gitignore...")

    source_file = source_path / ".gitignore"
    target_file = target_path / ".gitignore"

    # Workflow-specific patterns to add
    workflow_patterns = [
        "",
        "# Workflow system",
        ".gemini-state/",
        ".tmp/",
        "*.duckdb",
        "*.duckdb.wal",
    ]

    if not target_file.exists():
        # Create .gitignore with workflow patterns
        if source_file.exists():
            shutil.copy2(source_file, target_file)
            print_success("Copied .gitignore from source")
        else:
            target_file.write_text("\n".join(workflow_patterns) + "\n")
            print_success("Created .gitignore with workflow patterns")
        return True

    # Read existing
    existing_lines = target_file.read_text().split("\n")

    # Add workflow patterns if not present
    added = []
    for pattern in workflow_patterns:
        if pattern and pattern not in existing_lines:
            existing_lines.append(pattern)
            if pattern and not pattern.startswith("#"):
                added.append(pattern)

    # Deduplicate non-blank lines while preserving order
    # Blank lines are preserved but consecutive blanks are collapsed to one
    seen = set()
    unique_lines = []
    prev_was_blank = False
    for line in existing_lines:
        is_blank = line == ""
        if is_blank:
            # Collapse consecutive blank lines to one
            if not prev_was_blank:
                unique_lines.append(line)
            prev_was_blank = True
        else:
            # Deduplicate non-blank lines
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
            prev_was_blank = False

    # Write back
    target_file.write_text("\n".join(unique_lines))

    if added:
        print_success(f"Added {len(added)} workflow patterns to .gitignore")
    else:
        print_success(".gitignore already has workflow patterns (preserved)")

    return True


def print_summary(
    target_path: Path,
    skills_count: int,
    commands_count: int,
    docs_copied: list[str],
) -> None:
    """Print summary of what was applied.

    Args:
        target_path: Path to target repository
        skills_count: Number of skills copied
        commands_count: Number of commands copied
        docs_copied: List of documentation files copied
    """
    print("\n" + "=" * 50)
    print_success("Workflow Application Complete")
    print("=" * 50 + "\n")

    print(f"Target: {target_path.resolve()}\n")

    ok = SYMBOLS["checkmark"]
    print("Applied:")
    print(f"  {ok} {skills_count} workflow skills (.gemini/skills/)")
    print(f"  {ok} {commands_count} workflow commands (.gemini/commands/)")
    for doc in docs_copied:
        print(f"  {ok} {doc}")
    print(f"  {ok} pyproject.toml (merged dev dependencies)")
    print(f"  {ok} .gitignore (merged workflow patterns)")

    print("\nNext Steps:")
    print("  1. Review changes: git status")
    print("  2. Install dependencies: uv sync")
    print("  3. Run tests: uv run pytest")
    print('  4. Start v7x1 workflow: /workflow:v7x1_1-worktree "feature description"')
    print("  5. Optional cleanup: rm -rf .tmp/")


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0=success, 1=source error, 2=target error, 3=cancelled)
    """
    parser = argparse.ArgumentParser(
        description="Apply workflow system from cloned template to existing repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  cd my-repo
  mkdir -p .tmp
  git clone https://github.com/stharrold/stharrold-templates.git .tmp/stharrold-templates
  python .tmp/stharrold-templates/.gemini/skills/initialize-repository/scripts/apply_workflow.py \\
    .tmp/stharrold-templates .
""",
    )

    parser.add_argument(
        "source_repo",
        type=Path,
        help="Path to cloned stharrold-templates",
    )
    parser.add_argument(
        "target_repo",
        type=Path,
        help="Path to existing repository",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite .gemini/ directory without prompting",
    )

    args = parser.parse_args()

    # Resolve paths
    source_path = args.source_repo.resolve()
    target_path = args.target_repo.resolve()

    print("\n" + "=" * 50)
    print("Apply Workflow System")
    print("=" * 50 + "\n")

    # Validate source
    print_info(f"Validating source: {source_path}")
    valid, message = validate_source(source_path)
    if not valid:
        print_error(message)
        return 1
    print_success(message)

    # Validate target
    print_info(f"Validating target: {target_path}")
    valid, message = validate_target(target_path)
    if not valid:
        print_error(message)
        return 2
    print_success(message)

    # Prompt for overwrite (unless --force)
    if not args.force:
        if not prompt_overwrite(target_path):
            print_warning("Cancelled by user")
            return 3

    print()  # Blank line before operations

    # Copy operations
    skills_count = copy_skills(source_path, target_path, args.force)
    commands_count = copy_commands(source_path, target_path, args.force)
    docs_copied = copy_documentation(source_path, target_path)

    # Merge operations (always merge, never overwrite)
    merge_pyproject_toml(source_path, target_path)
    merge_gitignore(source_path, target_path)

    # Summary
    print_summary(target_path, skills_count, commands_count, docs_copied)

    return 0


if __name__ == "__main__":
    sys.exit(main())
