#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Deprecate files by archiving them with timestamp.

This is a thin wrapper around archive_manager.create_archive() that:
1. Extracts timestamp from TODO file (legacy behavior)
2. Calls create_archive() with delete_originals=True

For new code, prefer using archive_manager.py directly:
    archive_manager.py create --delete <description> <files...>
"""

import sys
from datetime import UTC, datetime
from pathlib import Path

# Import shared function from archive_manager
try:
    from archive_manager import create_archive
except ImportError:
    # Handle case when run directly from scripts directory
    import subprocess

    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    repo_root = Path(result.stdout.strip())
    sys.path.insert(0, str(repo_root / ".claude" / "skills" / "workflow-utilities" / "scripts"))
    from archive_manager import create_archive


def deprecate_files(todo_file, description, *files):
    """
    Archive deprecated files with timestamp.

    Args:
        todo_file: Path to TODO file (for timestamp extraction)
        description: Short description (e.g., 'old-auth-flow')
        *files: File paths to deprecate

    Returns:
        Tuple of (archive_path, failed_files) where failed_files is a list of
        (file_path, error_message) tuples for files that could not be archived.

    Creates:
        ARCHIVED/YYYYMMDDTHHMMSSZ_<description>.zip
    """
    # Extract timestamp from TODO file name (legacy behavior)
    todo_path = Path(todo_file).resolve()
    todo_name = todo_path.stem  # TODO_feature_20251022T143022Z_slug
    parts = todo_name.split("_")
    timestamp = parts[2] if len(parts) > 2 else datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

    # Use shared create_archive function with delete_originals=True
    return create_archive(
        description=description,
        files=list(files),
        archived_dir="ARCHIVED",
        preserve_paths=False,
        delete_originals=True,
        ensure_archived_structure=True,
        timestamp=timestamp,
    )


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: deprecate_files.py <todo_file> <description> <file1> [file2 ...]")
        print("Example: deprecate_files.py TODO_feature_xxx.md old-impl src/old.py")
        print()
        print("For new code, prefer using archive_manager.py directly:")
        print("  archive_manager.py create --delete <description> <files...>")
        sys.exit(1)

    archive_path, failed_files = deprecate_files(sys.argv[1], sys.argv[2], *sys.argv[3:])
    # Exit with code 2 if there were partial failures
    if failed_files:
        sys.exit(2)
