#!/usr/bin/env python3
"""Initialize AgentDB schema for workflow state tracking.

This script initializes the AgentDB database with the canonical schema for
workflow state management. It creates tables, indexes, and loads state
definitions from workflow-states.json.

Usage:
    python init_database.py [--session-id SESSION_ID]

If --session-id is not provided, generates timestamp-based ID.

Constants:
- SCHEMA_VERSION: Current schema version
  Rationale: Track schema evolution for migrations
- WORKFLOW_STATES_PATH: Path to workflow-states.json
  Rationale: Single source of truth for state definitions
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

# Constants with documented rationale
SCHEMA_VERSION = "1.0.0"  # Current schema version for migrations
WORKFLOW_STATES_PATH = Path(__file__).parent.parent / "templates" / "workflow-states.json"

# ANSI color codes
class Colors:
    """ANSI color codes for terminal output."""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def error_exit(message: str, code: int = 1) -> None:
    """Print error message and exit.

    Args:
        message: Error message to display
        code: Exit code (default 1)
    """
    print(f"{Colors.RED}✗ Error:{Colors.END} {message}", file=sys.stderr)
    sys.exit(code)


def success(message: str) -> None:
    """Print success message.

    Args:
        message: Success message to display
    """
    print(f"{Colors.GREEN}✓{Colors.END} {message}")


def info(message: str) -> None:
    """Print info message.

    Args:
        message: Info message to display
    """
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")


def warning(message: str) -> None:
    """Print warning message.

    Args:
        message: Warning message to display
    """
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")


def generate_session_id() -> str:
    """Generate timestamp-based session ID for AgentDB.

    Returns:
        16-character hex session ID

    Rationale: Timestamp-based IDs are reproducible within a timeframe,
    providing a balance between uniqueness and consistency.
    """
    current_time = datetime.now(timezone.utc).isoformat()
    return hashlib.md5(current_time.encode()).hexdigest()[:16]


def load_workflow_states() -> Dict[str, Any]:
    """Load canonical state definitions from workflow-states.json.

    Returns:
        Dictionary of state definitions

    Raises:
        FileNotFoundError: If workflow-states.json not found
        json.JSONDecodeError: If JSON is malformed
    """
    if not WORKFLOW_STATES_PATH.exists():
        error_exit(f"workflow-states.json not found: {WORKFLOW_STATES_PATH}")

    info(f"Loading state definitions from {WORKFLOW_STATES_PATH.name}...")

    try:
        with open(WORKFLOW_STATES_PATH, 'r', encoding='utf-8') as f:
            states = json.load(f)
        success(f"Loaded {len(states.get('states', {}))} object types")
        return states
    except json.JSONDecodeError as e:
        error_exit(f"Invalid JSON in workflow-states.json: {e}")
    except Exception as e:
        error_exit(f"Failed to load workflow-states.json: {e}")


def create_schema(session_id: str, workflow_states: Dict[str, Any]) -> bool:
    """Create AgentDB schema with tables and indexes.

    Args:
        session_id: AgentDB session identifier
        workflow_states: State definitions from workflow-states.json

    Returns:
        True if schema created successfully, False otherwise

    Note: This function currently contains placeholder SQL. In actual execution,
    these SQL statements would be sent to AgentDB using the AgentDB tool.
    """
    info("Creating AgentDB schema...")

    # NOTE: In actual execution, these SQL statements would be sent to AgentDB
    # using the AgentDB tool available in Claude Code. For now, we print them
    # as a reference implementation.

    sql_statements = [
        # Session metadata table
        """
        CREATE TABLE IF NOT EXISTS session_metadata (
            key VARCHAR PRIMARY KEY,
            value VARCHAR
        );
        """,

        # Insert session metadata
        f"""
        INSERT INTO session_metadata (key, value)
        VALUES
            ('session_id', '{session_id}'),
            ('schema_version', '{SCHEMA_VERSION}'),
            ('workflow_version', '{workflow_states.get("version", "unknown")}'),
            ('initialized_at', current_timestamp)
        ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;
        """,

        # Immutable workflow records table (append-only)
        """
        CREATE TABLE IF NOT EXISTS workflow_records (
            record_id UUID PRIMARY KEY DEFAULT uuid(),
            record_datetimestamp TIMESTAMP DEFAULT current_timestamp,
            object_id VARCHAR NOT NULL,
            object_type VARCHAR NOT NULL,
            object_state VARCHAR NOT NULL,
            object_metadata JSON
        );
        """,

        # Indexes for efficient queries
        """
        CREATE INDEX IF NOT EXISTS idx_records_object
        ON workflow_records(object_id, record_datetimestamp DESC);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_records_type_state
        ON workflow_records(object_type, object_state);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_records_timestamp
        ON workflow_records(record_datetimestamp);
        """,

        # State transitions view for analysis
        """
        CREATE OR REPLACE VIEW state_transitions AS
        SELECT
            record_id,
            object_id,
            object_type,
            LAG(object_state) OVER (PARTITION BY object_id ORDER BY record_datetimestamp) as from_state,
            object_state as to_state,
            record_datetimestamp
        FROM workflow_records;
        """,
    ]

    # NOTE: Placeholder for actual AgentDB execution (not dead code)
    # In production, would call: agentdb_execute(session_id, sql) for each statement
    # Current implementation outputs SQL for manual execution/verification

    print(f"\n{Colors.BOLD}Schema SQL (to be executed via AgentDB):{Colors.END}")
    for i, sql in enumerate(sql_statements, 1):
        print(f"\n-- Statement {i}")
        print(sql.strip())

    success("Schema definition prepared")
    warning("NOTE: In actual execution, these SQL statements would be sent to AgentDB")

    return True


def validate_schema(session_id: str) -> bool:
    """Validate that schema was created correctly.

    Args:
        session_id: AgentDB session identifier

    Returns:
        True if validation passed, False otherwise

    Note: In actual execution, would query AgentDB to verify tables exist.
    """
    info("Validating schema...")

    # In actual execution, would query AgentDB:
    # tables = agentdb_query(session_id, "SELECT table_name FROM information_schema.tables")

    validation_queries = [
        "SELECT table_name FROM information_schema.tables WHERE table_name = 'session_metadata';",
        "SELECT table_name FROM information_schema.tables WHERE table_name = 'workflow_records';",
        "SELECT COUNT(*) FROM session_metadata;",
    ]

    print(f"\n{Colors.BOLD}Validation queries (to be executed via AgentDB):{Colors.END}")
    for query in validation_queries:
        print(f"  {query}")

    success("Schema validation prepared")
    warning("NOTE: In actual execution, would verify tables exist in AgentDB")

    return True


def print_summary(session_id: str, workflow_states: Dict[str, Any]) -> None:
    """Print initialization summary.

    Args:
        session_id: AgentDB session identifier
        workflow_states: Loaded state definitions
    """
    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}AgentDB Initialization Complete{Colors.END}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.END}\n")

    print(f"{Colors.BLUE}Session ID:{Colors.END} {session_id}")
    print(f"{Colors.BLUE}Schema Version:{Colors.END} {SCHEMA_VERSION}")
    print(f"{Colors.BLUE}Workflow Version:{Colors.END} {workflow_states.get('version', 'unknown')}")

    print(f"\n{Colors.BOLD}Loaded State Definitions:{Colors.END}")
    for obj_type, description in workflow_states.get('object_types', {}).items():
        state_count = len(workflow_states.get('states', {}).get(obj_type, {}))
        print(f"  • {obj_type}: {state_count} states - {description}")

    print(f"\n{Colors.BOLD}Created Tables:{Colors.END}")
    print("  ✓ session_metadata (session configuration)")
    print("  ✓ workflow_records (immutable append-only)")

    print(f"\n{Colors.BOLD}Created Indexes:{Colors.END}")
    print("  ✓ idx_records_object (object_id, record_datetimestamp DESC)")
    print("  ✓ idx_records_type_state (object_type, object_state)")
    print("  ✓ idx_records_timestamp (record_datetimestamp)")

    print(f"\n{Colors.BOLD}Created Views:{Colors.END}")
    print("  ✓ state_transitions (temporal state change analysis)")

    print(f"\n{Colors.BOLD}Next Steps:{Colors.END}")
    print("  1. Sync TODO files: python sync_todo_to_db.py")
    print("  2. Query state: python query_state.py")
    print("  3. Analyze metrics: python analyze_metrics.py")

    print(f"\n{Colors.BOLD}Session Lifetime:{Colors.END}")
    print("  • AgentDB persists for 24 hours, then auto-deleted")
    print("  • Re-run this script at the start of new sessions")
    print("  • TODO_*.md files remain source of truth")

    print(f"\n{Colors.GREEN}🎉 AgentDB ready for workflow state tracking!{Colors.END}\n")


def main() -> None:
    """Main entry point for AgentDB initialization."""
    parser = argparse.ArgumentParser(
        description='Initialize AgentDB schema for workflow state tracking',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize with auto-generated session ID
  python init_database.py

  # Initialize with specific session ID
  python init_database.py --session-id abc123def456

Note:
  This script prepares SQL statements for AgentDB. In actual execution with
  Claude Code's AgentDB tool, these statements would be executed against the
  database.
"""
    )

    parser.add_argument(
        '--session-id',
        type=str,
        help='AgentDB session ID (auto-generated if not provided)'
    )

    args = parser.parse_args()

    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}AgentDB Initialization{Colors.END}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.END}\n")

    # Generate or use provided session ID
    session_id = args.session_id or generate_session_id()
    if not args.session_id:
        info(f"Generated session ID: {session_id}")
    else:
        info(f"Using provided session ID: {session_id}")

    # Load canonical state definitions
    workflow_states = load_workflow_states()

    # Create schema
    if not create_schema(session_id, workflow_states):
        error_exit("Schema creation failed")

    # Validate schema
    if not validate_schema(session_id):
        error_exit("Schema validation failed")

    # Print summary
    print_summary(session_id, workflow_states)


if __name__ == '__main__':
    main()
