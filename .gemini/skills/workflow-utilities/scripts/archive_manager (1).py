#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Manage archived files: list, extract, create, verify, archive workflows."""

import os
import shutil
import subprocess
import sys
import zipfile
from datetime import UTC, datetime
from pathlib import Path

from safe_output import format_warning


def get_repo_root() -> Path:
    """Get the repository root directory as an absolute path."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip()).resolve()
    except subprocess.CalledProcessError:
        # Fallback to current directory if not in git repo
        return Path.cwd().resolve()


def ensure_archived_directory(archived_dir: Path) -> Path:
    """Create ARCHIVED/ directory with GEMINI.md and README.md if missing.

    Args:
        archived_dir: Path to archived directory (absolute)

    Returns:
        Path to archived directory
    """
    archived_dir.mkdir(parents=True, exist_ok=True)

    # Create GEMINI.md if missing
    archived_gemini = archived_dir / "GEMINI.md"
    if not archived_gemini.exists():
        archived_gemini.write_text(
            """# Gemini Code Context: Archived Content

## Purpose

Archive of deprecated files.

## Contents

Zip files containing deprecated code and resources.

## Restoration

Use archive_manager.py to list and extract archived files.
"""
        )

    # Create README.md if missing
    archived_readme = archived_dir / "README.md"
    if not archived_readme.exists():
        archived_readme.write_text(
            """# Archived Files

This directory contains archived (deprecated) files that are no longer in active use.

Files are stored in timestamped zip archives for potential recovery.
"""
        )

    return archived_dir


def create_archive(
    description: str,
    files: list[str],
    archived_dir: str | Path = "ARCHIVED",
    preserve_paths: bool = False,
    delete_originals: bool = False,
    ensure_archived_structure: bool = True,
    timestamp: str | None = None,
) -> tuple[str, list[tuple[str, str]]]:
    """Create a timestamped archive of files.

    Args:
        description: Short description for archive name (e.g., 'old-auth-flow')
        files: List of file paths to archive
        archived_dir: Output directory for archive (default: ARCHIVED)
        preserve_paths: If True, preserve directory structure in archive
        delete_originals: If True, delete source files after archiving
        ensure_archived_structure: If True, create GEMINI.md and README.md
        timestamp: Optional timestamp (default: current UTC time)

    Returns:
        Tuple of (path to created archive, list of (file_path, error) for failed files)

    Raises:
        ValueError: If no valid files were archived
    """
    # Get repo root for absolute path resolution
    repo_root = get_repo_root()

    # Resolve archived_dir to absolute path
    if isinstance(archived_dir, str):
        archived_path = repo_root / archived_dir
    else:
        archived_path = archived_dir if archived_dir.is_absolute() else repo_root / archived_dir
    archived_path = archived_path.resolve()

    # Ensure archived directory exists with standard files
    if ensure_archived_structure:
        ensure_archived_directory(archived_path)
    else:
        archived_path.mkdir(parents=True, exist_ok=True)

    # Generate timestamp if not provided
    if timestamp is None:
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

    # Create zip archive
    zip_name = f"{timestamp}_{description}.zip"
    zip_path = archived_path / zip_name

    archived_count = 0
    failed_files: list[tuple[str, str]] = []

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            # Resolve to absolute path
            file_path = Path(file)
            if not file_path.is_absolute():
                file_path = repo_root / file_path
            file_path = file_path.resolve()

            if file_path.exists():
                # Determine archive name
                if preserve_paths:
                    try:
                        archive_name = str(file_path.relative_to(repo_root))
                    except ValueError:
                        archive_name = file_path.name
                else:
                    archive_name = file_path.name

                try:
                    if file_path.is_dir():
                        for root, _, files_in_dir in os.walk(file_path):
                            for f in files_in_dir:
                                full_path = Path(root) / f
                                if preserve_paths:
                                    try:
                                        arcname = str(full_path.relative_to(repo_root))
                                    except ValueError:
                                        arcname = str(full_path.relative_to(file_path.parent))
                                else:
                                    arcname = str(full_path.relative_to(file_path.parent))
                                zipf.write(full_path, arcname)
                        print(f"  Archived directory: {file_path}")
                        archived_count += 1
                    else:
                        zipf.write(file_path, archive_name)
                        print(f"  Archived: {file_path}")
                        archived_count += 1
                except (PermissionError, OSError) as e:
                    error_msg = str(e)
                    failed_files.append((str(file_path), error_msg))
                    print(
                        f"  {format_warning(f'Could not archive {file_path}: {e}')}",
                        file=sys.stderr,
                    )
                    continue

                if delete_originals:
                    if file_path.is_dir():
                        shutil.rmtree(file_path)
                    else:
                        file_path.unlink()
                    print(f"  Deleted: {file_path}")
            else:
                error_msg = "File not found"
                failed_files.append((str(file_path), error_msg))
                print(f"  {format_warning(f'{file_path} not found')}", file=sys.stderr)

    if archived_count == 0:
        # Remove empty archive
        zip_path.unlink()
        raise ValueError("No valid files were archived")

    # Report summary including any failures
    if failed_files:
        print(f"[WARN] {len(failed_files)} file(s) failed to archive:")
        for path, error in failed_files:
            print(f"  - {path}: {error}")
    print(f"[OK] Created archive: {zip_path} ({archived_count} file(s))")
    return str(zip_path), failed_files


def list_archives(archived_dir: str = "ARCHIVED") -> list[Path]:
    """List all archives with timestamps."""
    repo_root = get_repo_root()

    # Resolve to absolute path
    archived_path = Path(archived_dir)
    if not archived_path.is_absolute():
        archived_path = repo_root / archived_path
    archived_path = archived_path.resolve()

    if not archived_path.exists():
        print(f"No {archived_dir} directory found")
        return []

    archives = sorted(archived_path.glob("*.zip"))

    if not archives:
        print(f"No archives found in {archived_dir}/")
        return []

    print(f"Archives in {archived_dir}/:")
    print("-" * 60)

    for archive in archives:
        # Parse timestamp from filename: YYYYMMDDTHHMMSSZ_description.zip
        name = archive.stem
        parts = name.split("_", 1)

        if len(parts) == 2:
            timestamp_str, description = parts
            try:
                # Parse timestamp
                timestamp = datetime.strptime(timestamp_str, "%Y%m%dT%H%M%SZ")
                print(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {description}")
                print(f"  File: {archive.name}")

                # List contents
                with zipfile.ZipFile(archive, "r") as zipf:
                    files = zipf.namelist()
                    print(f"  Contains: {', '.join(files)}")

            except ValueError:
                print(f"  {archive.name} (invalid timestamp format)")
        else:
            print(f"  {archive.name}")

        print()

    return archives


def extract_archive(archive_path, output_dir="."):
    """Extract archive to specified directory."""
    repo_root = get_repo_root()

    # Resolve archive path
    archive = Path(archive_path)
    if not archive.is_absolute():
        archive = repo_root / archive
    archive = archive.resolve()

    if not archive.exists():
        print(f"Error: Archive not found: {archive_path}", file=sys.stderr)
        sys.exit(1)

    # Resolve output path
    output = Path(output_dir)
    if not output.is_absolute():
        output = repo_root / output
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    print(f"Extracting {archive.name} to {output}/")

    with zipfile.ZipFile(archive, "r") as zipf:
        zipf.extractall(output)
        print("[OK] Extracted files:")
        for name in zipf.namelist():
            print(f"  - {name}")

    print("\n[OK] Extraction complete")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: archive_manager.py <command> [args]")
        print()
        print("Commands:")
        print(
            "  list [directory]                    - List archives in directory (default: ARCHIVED)"
        )
        print("  extract <archive> [output]          - Extract archive to output directory")
        print("  create [options] <desc> <files...>  - Create archive from files")
        print()
        print("Create options:")
        print("  --delete          Delete originals after archiving")
        print("  --preserve-paths  Preserve directory structure in archive")
        print("  --output-dir DIR  Output directory (default: ARCHIVED)")
        print()
        print("Examples:")
        print("  archive_manager.py list")
        print("  archive_manager.py list ARCHIVED")
        print("  archive_manager.py extract ARCHIVED/20251022T143022Z_old-impl.zip restored/")
        print("  archive_manager.py create old-impl src/old.py tests/test_old.py")
        print("  archive_manager.py create --delete deprecated src/legacy.py")
        print("  archive_manager.py create --preserve-paths backup src/a/f.py src/b/f.py")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        archived_dir = sys.argv[2] if len(sys.argv) > 2 else "ARCHIVED"
        list_archives(archived_dir)

    elif command == "extract":
        if len(sys.argv) < 3:
            print("Usage: archive_manager.py extract <archive_path> [output_dir]")
            sys.exit(1)

        archive_path = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "."
        extract_archive(archive_path, output_dir)

    elif command == "create":
        # Parse options
        delete_originals = False
        preserve_paths = False
        output_dir = "ARCHIVED"

        args = sys.argv[2:]
        remaining_args = []

        i = 0
        while i < len(args):
            if args[i] == "--delete":
                delete_originals = True
            elif args[i] == "--preserve-paths":
                preserve_paths = True
            elif args[i] == "--output-dir":
                i += 1
                if i < len(args):
                    output_dir = args[i]
                else:
                    print("Error: --output-dir requires a directory argument", file=sys.stderr)
                    sys.exit(1)
            else:
                remaining_args.append(args[i])
            i += 1

        if len(remaining_args) < 2:
            print("Usage: archive_manager.py create [options] <description> <file1> [file2 ...]")
            print("Options: --delete, --preserve-paths, --output-dir DIR")
            sys.exit(1)

        description = remaining_args[0]
        files = remaining_args[1:]

        try:
            archive_path, failed_files = create_archive(
                description=description,
                files=files,
                archived_dir=output_dir,
                preserve_paths=preserve_paths,
                delete_originals=delete_originals,
            )
            # Exit with code 2 if there were partial failures
            if failed_files:
                sys.exit(2)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        print("Use 'list', 'extract', or 'create'")
        sys.exit(1)
