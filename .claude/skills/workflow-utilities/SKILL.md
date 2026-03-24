---
name: workflow-utilities
version: 5.2.0
description: |
  Shared utilities for file deprecation, directory structure creation,
  TODO file updates, workflow lifecycle management, archive management,
  and VCS abstraction (GitHub/Azure DevOps).
  Used by all other skills.

  Use when: Need shared utilities, deprecating files, updating TODO,
  registering/archiving workflows, managing TODO.md manifest, VCS operations,
  PR feedback handling

  Triggers: deprecate, archive, update TODO, create directory, register workflow,
  archive workflow, sync manifest, VCS operations, PR feedback
---

## Quick Reference

```bash
# Archive deprecated files
uv run python .claude/skills/workflow-utilities/scripts/deprecate_files.py <desc> <files...>

# List/extract archives
uv run python .claude/skills/workflow-utilities/scripts/archive_manager.py list
uv run python .claude/skills/workflow-utilities/scripts/archive_manager.py extract <archive>

# Validate versions
uv run python .claude/skills/workflow-utilities/scripts/validate_versions.py
```

# Workflow Utilities

## Purpose

Provides reusable Python utilities for common workflow tasks that are used
across multiple skills.

## Scripts

### deprecate_files.py

Archive deprecated files with timestamp into ARCHIVED/ directory.

```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  <todo_file> <description> <file1> [file2 ...]
```

**Arguments:**
- `todo_file`: Path to TODO file (for timestamp extraction)
- `description`: Short description (e.g., 'old-auth-flow')
- `files`: One or more file paths to deprecate

**Creates:**
- `ARCHIVED/YYYYMMDDTHHMMSSZ_<description>.zip`

### directory_structure.py

Create standard directory structure with required files.

```bash
python .claude/skills/workflow-utilities/scripts/directory_structure.py \
  <directory>
```

**Arguments:**
- `directory`: Path to directory to create/populate

**Creates:**
- `CLAUDE.md` - Context-specific guidance
- `README.md` - Human-readable documentation
- `ARCHIVED/` subdirectory (with its own CLAUDE.md and README.md)

### todo_updater.py

Update task status and workflow progress in TODO file.

```bash
python .claude/skills/workflow-utilities/scripts/todo_updater.py \
  <todo_file> <task_id> <status> [context_usage]
```

**Arguments:**
- `todo_file`: Path to TODO file
- `task_id`: Task ID (e.g., 'impl_003')
- `status`: New status ('pending' | 'complete' | 'blocked')
- `context_usage` (optional): Context usage percentage

**Updates:**
- Task status in YAML frontmatter
- `completed_at` timestamp
- `workflow_progress.last_task`
- `workflow_progress.last_update`

### archive_manager.py

List and extract archived files.

```bash
# List archives
python .claude/skills/workflow-utilities/scripts/archive_manager.py list [directory]

# Extract archive
python .claude/skills/workflow-utilities/scripts/archive_manager.py extract <archive> [output_dir]
```

### workflow_registrar.py

Register new workflow in TODO.md master manifest.

```bash
python .claude/skills/workflow-utilities/scripts/workflow_registrar.py \
  <todo_file> <workflow_type> <slug> [--title TITLE]
```

**Arguments:**
- `todo_file`: Path to TODO_*.md file
- `workflow_type`: Workflow type ('feature' | 'release' | 'hotfix')
- `slug`: Workflow slug
- `--title` (optional): Workflow title (auto-generated if not provided)

**Updates:**
- Adds workflow to `TODO.md workflows.active[]` array
- Updates `TODO.md last_update` timestamp

**When to use:**
- After creating BMAD planning (Phase 1)
- After creating feature worktree (Phase 2)
- Ensures TODO.md tracks all active workflows

### workflow_archiver.py

Archive completed workflow and update TODO.md manifest.

```bash
python .claude/skills/workflow-utilities/scripts/workflow_archiver.py \
  <todo_file> [--summary SUMMARY] [--version VERSION]
```

**Arguments:**
- `todo_file`: Path to TODO_*.md file to archive
- `--summary` (optional): Summary of what was completed
- `--version` (optional): Semantic version (e.g., '1.5.0')

**Actions:**
1. Moves TODO_*.md → ARCHIVED/TODO_*.md
2. Updates TODO.md: moves workflow from active[] to archived[] array
3. Updates TODO.md statistics (total_workflows_completed)
4. Extracts metadata from workflow file (version, summary)

**When to use:**
- Phase 4.3: After PR merged to contrib branch
- Before creating PR contrib → develop

### sync_manifest.py

Synchronize TODO.md manifest with filesystem state.

```bash
# Preview changes
python .claude/skills/workflow-utilities/scripts/sync_manifest.py --dry-run

# Sync TODO.md
python .claude/skills/workflow-utilities/scripts/sync_manifest.py
```

**Actions:**
1. Scans current directory for TODO_*.md files (active)
2. Scans ARCHIVED/ for TODO_*.md files (archived)
3. Rebuilds TODO.md workflows.active[] and workflows.archived[] arrays
4. Updates statistics

**When to use:**
- Recovery: TODO.md out of sync with filesystem
- Verification: Check TODO.md reflects actual files
- Migration: Rebuilding TODO.md from scratch

**Warning:** Replaces TODO.md arrays with filesystem state. Manual metadata edits may be lost.

### VCS Abstraction Layer (vcs/)

Wrapper functions for GitHub (`gh`) and Azure DevOps (`az`) CLI operations.

**Location:** `.claude/skills/workflow-utilities/scripts/vcs/`

**Key files:**
- `provider.py` - VCS provider enum + `detect_provider()` (auto-detects from git remote URL, cached)
- `operations.py` - Wrapper functions: `get_username`, `get_contrib_branch`, `create_pr`, `create_release`, `create_issue`, `query_pr_review_threads`, `check_auth`

**Usage:**
```python
from vcs import create_pr, get_contrib_branch, get_username

branch = get_contrib_branch()  # auto-detects provider
username = get_username()

# Create PR
pr_url = create_pr(
    base=branch,
    head="feature/20251103T143000Z_auth",
    title="feat: auth system (v1.6.0)",
    body="PR body content",
)
```

**Key features:**
- Auto-detects provider from `git remote.origin.url` (github.com / dev.azure.com)
- Errors surfaced as `RuntimeError(stderr)` — callers inspect string contents
- Module-level caching for provider detection
- PR creation, issue creation, release management, auth checking

## Usage Examples

### Deprecating Old Files

```python
import subprocess

# Deprecate old implementation files
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/deprecate_files.py',
    'TODO_feature_20251022T143022Z_json-validator.md',
    'old-validator',
    'src/old_validator.py',
    'tests/test_old_validator.py'
], check=True)
```

### Creating Standard Directories

```python
import subprocess

# Create planning directory with standard structure
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/directory_structure.py',
    'planning/json-validator'
], check=True)
```

### Updating TODO Tasks

```python
import subprocess

# Mark task as complete
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/todo_updater.py',
    'TODO_feature_20251022T143022Z_json-validator.md',
    'impl_003',
    'complete',
    '35'  # context usage percentage
], check=True)
```

### Managing Workflow Lifecycle

```python
import subprocess

# Register new workflow in TODO.md (Phase 1/2)
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/workflow_registrar.py',
    'TODO_feature_20251103T143000Z_auth.md',
    'feature',
    'auth',
    '--title', 'User Authentication System'
], check=True)

# Archive completed workflow (Phase 4.3)
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/workflow_archiver.py',
    'TODO_feature_20251103T143000Z_auth.md',
    '--summary', 'Implemented OAuth2 authentication with Google and GitHub',
    '--version', '1.5.0'
], check=True)

# Sync TODO.md with filesystem (recovery)
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/sync_manifest.py'
], check=True)
```

## Directory Standards

All directories created by these utilities follow the standard structure:

```
directory/
├── CLAUDE.md      # Context for Claude Code
├── README.md      # Human-readable documentation
└── ARCHIVED/      # Deprecated files (except if directory IS archived)
    ├── CLAUDE.md
    └── README.md
```

## Integration with Other Skills

All skills can use these helper functions:

```python
# Example from bmad-planner
from pathlib import Path
import subprocess

def create_planning_with_structure(feature_name):
    """Create planning directory with standard structure."""

    planning_dir = Path('planning') / feature_name

    # Create directory structure
    subprocess.run([
        'python',
        '.claude/skills/workflow-utilities/scripts/directory_structure.py',
        str(planning_dir)
    ], check=True)

    # Now create planning documents
    # ...
```

## Best Practices

- Always use these utilities for consistency
- Don't manually create directory structures
- Use deprecation for old files, not deletion
- Update TODO file after each meaningful step
- Check archives before deleting files permanently
