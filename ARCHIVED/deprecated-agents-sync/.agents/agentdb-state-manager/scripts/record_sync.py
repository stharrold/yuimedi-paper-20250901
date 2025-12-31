#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
"""Record workflow transitions in AgentDB.

This script records synchronization events in the AgentDB database for
workflow state tracking. Each slash command should call this after
completing its primary operations.

Usage:
    python record_sync.py --sync-type workflow_transition --pattern phase_1_specify
    python record_sync.py --sync-type workflow_transition --pattern phase_2_plan \
        --source "../planning/my-feature" --target "specs/my-feature"

Created: 2025-11-23
Feature: 008-workflow-skill-integration
"""

import argparse
import json
import subprocess
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

# Valid sync types (from agentdb_sync_schema.sql)
VALID_SYNC_TYPES = ["workflow_transition", "quality_gate", "file_update"]

# Valid workflow patterns
VALID_PATTERNS = [
    "phase_1_specify",
    "phase_2_plan",
    "phase_3_tasks",
    "phase_4_implement",
    "phase_5_integrate",
    "phase_6_release",
    "phase_7_backmerge",
    "quality_gate_passed",
    "quality_gate_failed",
]


def get_worktree_path() -> str | None:
    """Detect current worktree path if in a worktree.

    Returns:
        Worktree path or None if in main repo
    """
    try:
        # Get git toplevel
        toplevel = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True, stderr=subprocess.PIPE
        ).strip()

        # Get current directory
        cwd = str(Path.cwd())

        # If different, we're in a worktree
        if cwd != toplevel:
            return cwd
        return None
    except subprocess.CalledProcessError:
        return None


def get_database_path() -> Path:
    """Get path to shared AgentDB database in main repository.

    Always returns the main repository's AgentDB path, ensuring all
    worktrees share the same workflow state.

    Returns:
        Path to agentdb.duckdb in main repo's .claude-state/
    """
    # Try to use shared worktree_context module
    try:
        script_dir = Path(__file__).parent
        worktree_utils = script_dir.parent.parent / "workflow-utilities" / "scripts"
        sys.path.insert(0, str(worktree_utils))
        from worktree_context import get_shared_agentdb_path

        return get_shared_agentdb_path()
    except (ImportError, RuntimeError):
        pass

    # Fallback: use git worktree list to find main repo
    try:
        result = subprocess.check_output(
            ["git", "worktree", "list", "--porcelain"],
            text=True,
            stderr=subprocess.PIPE,
        )
        # First worktree line is the main repo
        for line in result.strip().split("\n"):
            if line.startswith("worktree "):
                main_repo = Path(line.split(" ", 1)[1])
                state_dir = main_repo / ".claude-state"
                state_dir.mkdir(parents=True, exist_ok=True)
                return state_dir / "agentdb.duckdb"
    except subprocess.CalledProcessError:
        # If git worktree inspection fails (e.g., not a git repository), fall back
        # to using the current directory's .claude-state/ as the AgentDB location.
        pass

    # Last resort fallback: current directory
    cwd = Path.cwd()
    state_dir = cwd / ".claude-state"
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir / "agentdb.duckdb"


def init_database_if_needed(db_path: Path) -> None:
    """Initialize AgentDB if it doesn't exist.

    Args:
        db_path: Path to database file
    """
    if db_path.exists():
        return

    # Find and run init script
    script_dir = Path(__file__).parent
    init_script = script_dir / "init_database.py"

    if init_script.exists():
        subprocess.run([sys.executable, str(init_script)], check=True, capture_output=True)


def record_sync(
    sync_type: str,
    pattern: str,
    source: str = "",
    target: str = "",
    worktree: str | None = None,
    metadata: dict | None = None,
) -> str:
    """Record a synchronization event in AgentDB.

    Args:
        sync_type: Type of sync (workflow_transition, quality_gate, file_update)
        pattern: Phase pattern (e.g., phase_1_specify)
        source: Source location
        target: Target location
        worktree: Worktree path (auto-detected if None)
        metadata: Additional JSON metadata

    Returns:
        sync_id of the created record

    Raises:
        ValueError: If sync_type or pattern is invalid
        RuntimeError: If database operation fails
    """
    # Validate inputs
    if sync_type not in VALID_SYNC_TYPES:
        raise ValueError(f"Invalid sync-type: {sync_type}. Must be one of: {VALID_SYNC_TYPES}")

    if pattern not in VALID_PATTERNS:
        # Allow custom patterns but warn
        print(f"Warning: Pattern '{pattern}' not in standard list", file=sys.stderr)

    # Generate sync_id
    sync_id = str(uuid.uuid4())

    # Auto-detect worktree if not provided
    if worktree is None:
        worktree = get_worktree_path()

    # Get database path
    db_path = get_database_path()

    # Initialize if needed
    init_database_if_needed(db_path)

    # Prepare timestamps
    now = datetime.now(UTC)
    timestamp = now.isoformat()

    # Prepare metadata JSON
    metadata_json = json.dumps(metadata) if metadata else "{}"

    # Build parameterized SQL to prevent SQL injection
    sql = """
    INSERT INTO agent_synchronizations (
        sync_id, agent_id, worktree_path, sync_type,
        source_location, target_location, pattern, status,
        created_at, completed_at, created_by, metadata
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    # Parameters tuple - use None for NULL values
    params = (
        sync_id,
        "claude-code",
        worktree,  # Will be NULL if None
        sync_type,
        source,
        target,
        pattern,
        "completed",
        timestamp,
        timestamp,
        "claude-code",
        metadata_json,
    )

    # Execute using DuckDB CLI or Python
    try:
        import duckdb

        conn = duckdb.connect(str(db_path))
        conn.execute(sql, params)
        conn.close()
    except ImportError:
        # Fallback to CLI if duckdb not available
        # Note: CLI fallback uses escaped values for safety
        escaped_sql = f"""
        INSERT INTO agent_synchronizations (
            sync_id, agent_id, worktree_path, sync_type,
            source_location, target_location, pattern, status,
            created_at, completed_at, created_by, metadata
        ) VALUES (
            '{sync_id}',
            'claude-code',
            {f"'{worktree}'" if worktree else "NULL"},
            '{sync_type}',
            '{source.replace("'", "''")}',
            '{target.replace("'", "''")}',
            '{pattern}',
            'completed',
            '{timestamp}',
            '{timestamp}',
            'claude-code',
            '{metadata_json.replace("'", "''")}'
        );
        """
        result = subprocess.run(
            ["duckdb", str(db_path), "-c", escaped_sql], capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Database error: {result.stderr}")

    return sync_id


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Record workflow transitions in AgentDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Record phase 1 completion
  python record_sync.py --sync-type workflow_transition --pattern phase_1_specify

  # Record with source/target
  python record_sync.py --sync-type workflow_transition --pattern phase_2_plan \\
    --source "../planning/my-feature" --target "specs/my-feature"

  # Record quality gate result
  python record_sync.py --sync-type quality_gate --pattern quality_gate_passed
""",
    )

    parser.add_argument(
        "--sync-type", required=True, choices=VALID_SYNC_TYPES, help="Type of synchronization"
    )
    parser.add_argument("--pattern", required=True, help="Phase pattern (e.g., phase_1_specify)")
    parser.add_argument("--source", default="", help="Source location")
    parser.add_argument("--target", default="", help="Target location")
    parser.add_argument(
        "--worktree", default=None, help="Worktree path (auto-detected if not provided)"
    )
    parser.add_argument("--metadata", default=None, help="Additional JSON metadata")

    args = parser.parse_args()

    # Parse metadata if provided
    metadata = None
    if args.metadata:
        try:
            metadata = json.loads(args.metadata)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in --metadata: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        sync_id = record_sync(
            sync_type=args.sync_type,
            pattern=args.pattern,
            source=args.source,
            target=args.target,
            worktree=args.worktree,
            metadata=metadata,
        )

        print(f"✓ Recorded sync: {sync_id}")
        print(f"  Type: {args.sync_type}")
        print(f"  Pattern: {args.pattern}")
        if args.source:
            print(f"  Source: {args.source}")
        if args.target:
            print(f"  Target: {args.target}")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
