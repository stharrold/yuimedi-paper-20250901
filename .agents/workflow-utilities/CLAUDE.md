---
type: claude-context
directory: .claude/skills/workflow-utilities
purpose: Workflow Utilities provides **shared utilities** for all workflow skills. It includes file deprecation, directory structure creation, TODO file updates, workflow lifecycle management (register/archive), VCS abstraction (GitHub/Azure DevOps), documentation maintenance tools, and version validation. All other skills depend on workflow-utilities for consistent file operations and workflow state management.
parent: null
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
related_skills:
  - **workflow-orchestrator** - Uses workflow utilities for TODO management
  - **bmad-planner** - Uses directory_structure.py, workflow_registrar.py
  - **speckit-author** - Uses directory_structure.py, todo_updater.py
  - **quality-enforcer** - Uses todo_updater.py for quality gates
  - **git-workflow-manager** - Uses VCS abstraction, workflow lifecycle tools
  - **initialize-repository** - Uses directory_structure.py, create_skill.py patterns
  - **agentdb-state-manager** - Reads TODO files updated by workflow-utilities
---

# Claude Code Context: workflow-utilities

## Purpose

Workflow Utilities provides **shared utilities** for all workflow skills. It includes file deprecation, directory structure creation, TODO file updates, workflow lifecycle management (register/archive), VCS abstraction (GitHub/Azure DevOps), documentation maintenance tools, and version validation. All other skills depend on workflow-utilities for consistent file operations and workflow state management.

## Directory Structure

```
.claude/skills/workflow-utilities/
├── scripts/                      # Shared utilities
│   ├── deprecate_files.py        # Archive deprecated files
│   ├── directory_structure.py    # Create standard directory structure
│   ├── todo_updater.py           # Update task status in TODO files
│   ├── archive_manager.py        # List and extract archives
│   ├── workflow_registrar.py     # Register workflow in TODO.md manifest
│   ├── workflow_archiver.py      # Archive completed workflow
│   ├── sync_manifest.py          # Sync TODO.md with filesystem
│   ├── validate_versions.py      # Validate version consistency
│   ├── create_skill.py           # Create new skills with official docs
│   ├── sync_skill_docs.py        # Semi-automated documentation sync
│   ├── update_claude_references.py # Update CLAUDE.md references
│   ├── vcs/                      # VCS abstraction layer
│   │   ├── provider.py           # VCS provider detection
│   │   ├── base_adapter.py       # Base adapter interface
│   │   ├── github_adapter.py     # GitHub CLI adapter
│   │   ├── azure_adapter.py      # Azure DevOps CLI adapter
│   │   ├── config.py             # VCS configuration
│   │   └── __init__.py           # Package initialization
│   └── __init__.py               # Package initialization
├── templates/                    # (none - no template files)
├── SKILL.md                      # Complete skill documentation
├── CLAUDE.md                     # This file
├── README.md                     # Human-readable overview
├── CHANGELOG.md                  # Version history
└── ARCHIVED/                     # Deprecated files
    ├── CLAUDE.md
    └── README.md
```

## Key Scripts

### deprecate_files.py

**Purpose:** Archive deprecated files with timestamp into ARCHIVED/ directory (never delete files directly)

**When to use:** When replacing old implementations, removing obsolete files, or deprecating unused code

**Invocation:**
```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  <todo_file> <description> <file1> [file2 ...]
```

**Example:**
```bash
# Deprecate old authentication implementation
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO_feature_20251103T143000Z_auth.md \
  old-auth-flow \
  src/old_auth.py \
  tests/test_old_auth.py
```

**What it does:**
1. Validates TODO file exists (for timestamp extraction)
2. Validates all files to deprecate exist
3. Creates zip archive: `ARCHIVED/<timestamp>_<description>.zip`
4. Moves original files to archive
5. Removes original files from filesystem

**Key features:**
- Preserves file history (no deletion)
- Timestamped archives for traceability
- Validates all files before archiving
- Atomic operation (all or nothing)

---

### directory_structure.py

**Purpose:** Create standard directory structure with required files (CLAUDE.md, README.md, ARCHIVED/)

**When to use:** When creating new directories (planning/, specs/, etc.) to ensure compliance with directory standards

**Invocation:**
```bash
python .claude/skills/workflow-utilities/scripts/directory_structure.py \
  <directory>
```

**Example:**
```bash
# Create planning directory with standard structure
python .claude/skills/workflow-utilities/scripts/directory_structure.py \
  planning/auth-system
```

**What it does:**
1. Creates directory if it doesn't exist
2. Creates `CLAUDE.md` with template
3. Creates `README.md` with template
4. Creates `ARCHIVED/` subdirectory
5. Creates `ARCHIVED/CLAUDE.md` and `ARCHIVED/README.md`

**Key features:**
- Enforces directory standards consistently
- Idempotent (safe to run multiple times)
- Template-based file creation
- Nested ARCHIVED/ structure

---

### todo_updater.py

**Purpose:** Update task status and workflow progress in TODO file YAML frontmatter

**When to use:** When marking tasks complete, updating workflow progress, or tracking context usage

**Invocation:**
```bash
python .claude/skills/workflow-utilities/scripts/todo_updater.py \
  <todo_file> <task_id> <status> [context_usage]
```

**Example:**
```bash
# Mark task impl_003 as complete with 35% context usage
python .claude/skills/workflow-utilities/scripts/todo_updater.py \
  TODO_feature_20251103T143000Z_auth.md \
  impl_003 \
  complete \
  35
```

**What it does:**
1. Reads TODO file and parses YAML frontmatter
2. Finds task by task_id in `tasks` section
3. Updates task status (`pending` | `complete` | `blocked`)
4. Updates `completed_at` timestamp (ISO8601 UTC)
5. Updates `workflow_progress.last_task` to current task_id
6. Updates `workflow_progress.last_update` timestamp
7. Optionally updates context usage
8. Writes updated YAML frontmatter back to file

**Key features:**
- Preserves YAML structure
- Validates task exists before updating
- Atomic file updates (write to temp, then move)
- ISO8601 UTC timestamps

---

### archive_manager.py

**Purpose:** List and extract archived files from ARCHIVED/ directory

**When to use:** When inspecting archived files, recovering deprecated files, or auditing archives

**Invocation:**
```bash
# List archives in ARCHIVED/
python .claude/skills/workflow-utilities/scripts/archive_manager.py list [directory]

# Extract archive to output directory
python .claude/skills/workflow-utilities/scripts/archive_manager.py \
  extract <archive> [output_dir]
```

**Examples:**
```bash
# List all archives
python .claude/skills/workflow-utilities/scripts/archive_manager.py list

# List archives in specific directory
python .claude/skills/workflow-utilities/scripts/archive_manager.py list planning/auth-system

# Extract archive
python .claude/skills/workflow-utilities/scripts/archive_manager.py \
  extract ARCHIVED/20251103T143000Z_old-auth-flow.zip \
  restored/
```

**What it does:**
1. **List mode:** Scans ARCHIVED/ for .zip files, prints archive names and contents
2. **Extract mode:** Extracts archive to output directory (default: `restored/`)

**Key features:**
- Validates archive exists
- Lists archive contents before extraction
- Preserves directory structure on extraction
- Safe extraction (validates zip integrity)

---

### workflow_registrar.py

**Purpose:** Register new workflow in TODO.md master manifest (adds to `workflows.active[]` array)

**When to use:** Phase 1 (after BMAD planning) or Phase 2 (after creating feature worktree)

**Invocation:**
```bash
python .claude/skills/workflow-utilities/scripts/workflow_registrar.py \
  <todo_file> <workflow_type> <slug> [--title TITLE]
```

**Example:**
```bash
# Register new feature workflow
python .claude/skills/workflow-utilities/scripts/workflow_registrar.py \
  TODO_feature_20251103T143000Z_auth.md \
  feature \
  auth-system \
  --title "User Authentication System"
```

**What it does:**
1. Validates TODO file exists
2. Parses filename: `TODO_<type>_<timestamp>_<slug>.md`
3. Reads TODO.md YAML frontmatter
4. Adds new entry to `workflows.active[]` array:
   ```yaml
   - slug: auth-system
     timestamp: 20251103T143000Z
     title: "User Authentication System"
     status: in_progress
     file: "TODO_feature_20251103T143000Z_auth.md"
   ```
5. Updates `TODO.md last_update` timestamp
6. Writes updated TODO.md

**Key features:**
- Validates workflow not already registered
- Auto-generates title if not provided
- Updates master manifest atomically
- Preserves TODO.md structure

---

### workflow_archiver.py

**Purpose:** Archive completed workflow and update TODO.md manifest (moves from `active[]` to `archived[]`)

**When to use:** Phase 4.4 (after PR merged to contrib branch, before creating PR to develop)

**Invocation:**
```bash
python .claude/skills/workflow-utilities/scripts/workflow_archiver.py \
  <todo_file> [--summary SUMMARY] [--version VERSION]
```

**Example:**
```bash
# Archive completed workflow
python .claude/skills/workflow-utilities/scripts/workflow_archiver.py \
  TODO_feature_20251103T143000Z_auth.md \
  --summary "Implemented OAuth2 authentication with Google and GitHub" \
  --version "1.6.0"
```

**What it does:**
1. Validates TODO file exists
2. Moves TODO file: `TODO_*.md` → `ARCHIVED/TODO_*.md`
3. Reads TODO.md YAML frontmatter
4. Finds workflow in `workflows.active[]` array
5. Removes from `active[]`, adds to `workflows.archived[]`:
   ```yaml
   - slug: auth-system
     timestamp: 20251103T143000Z
     title: "User Authentication System"
     status: completed
     completed_at: "2025-11-03T19:30:00Z"
     semantic_version: "1.6.0"
     file: "ARCHIVED/TODO_feature_20251103T143000Z_auth.md"
     summary: "Implemented OAuth2 authentication with Google and GitHub"
   ```
6. Updates `context_stats.total_workflows_completed`
7. Updates `TODO.md last_update` timestamp
8. Writes updated TODO.md

**Key features:**
- Atomic move and manifest update
- Extracts metadata from workflow file (version, summary)
- Updates statistics automatically
- Validates workflow exists before archiving

---

### sync_manifest.py

**Purpose:** Synchronize TODO.md manifest with filesystem state (recovery tool)

**When to use:** When TODO.md is out of sync with actual TODO_*.md files (recovery, verification, migration)

**Invocation:**
```bash
# Preview changes (dry run)
python .claude/skills/workflow-utilities/scripts/sync_manifest.py --dry-run

# Sync TODO.md with filesystem
python .claude/skills/workflow-utilities/scripts/sync_manifest.py
```

**What it does:**
1. Scans current directory for `TODO_*.md` files (active workflows)
2. Scans `ARCHIVED/` for `TODO_*.md` files (archived workflows)
3. Parses each TODO file to extract metadata (slug, timestamp, title, version)
4. Rebuilds `TODO.md workflows.active[]` array from active files
5. Rebuilds `TODO.md workflows.archived[]` array from archived files
6. Updates `context_stats.total_workflows_completed`
7. Updates `TODO.md last_update` timestamp
8. Writes updated TODO.md

**Key features:**
- Rebuilds manifest from source of truth (filesystem)
- Validates TODO file format before adding to manifest
- Shows diff before applying (dry-run mode)
- **Warning:** Replaces TODO.md arrays - manual metadata edits may be lost

---

### validate_versions.py

**Purpose:** Validate version consistency across SKILL.md, WORKFLOW.md, TODO.md files

**When to use:** Before committing skill changes, before releases, when updating documentation

**Invocation:**
```bash
# Validate all versions
python .claude/skills/workflow-utilities/scripts/validate_versions.py

# Show detailed version information
python .claude/skills/workflow-utilities/scripts/validate_versions.py --verbose

# Attempt auto-fix (use with caution)
python .claude/skills/workflow-utilities/scripts/validate_versions.py --fix
```

**What it does:**
1. Validates all SKILL.md files have valid semantic version in YAML frontmatter
2. Validates WORKFLOW.md has valid version
3. Validates TODO.md has valid version
4. Checks WORKFLOW.md phase descriptions reference correct skill versions
5. Reports inconsistencies

**Key features:**
- Semantic versioning validation (`MAJOR.MINOR.PATCH`)
- Cross-file consistency checks
- Verbose mode for detailed reporting
- Exit code indicates success (0) or failure (1)

---

### create_skill.py

**Purpose:** Create new workflow skill with official Claude Code documentation validation

**When to use:** When adding new skills to workflow system (rare - only 9 skills exist)

**Invocation:**
```bash
python .claude/skills/workflow-utilities/scripts/create_skill.py <skill-name>
```

**Example:**
```bash
# Create new skill
python .claude/skills/workflow-utilities/scripts/create_skill.py my-new-skill
```

**What it does:**
1. Asks configuration questions (purpose, phase, integration)
2. Fetches official Claude Code skill documentation
3. Compares local workflow patterns with official patterns
4. Alerts user if discrepancies exist (with citations)
5. Generates all required files (SKILL.md, CLAUDE.md, README.md, CHANGELOG.md)
6. Creates scripts/ directory with __init__.py
7. Creates ARCHIVED/ with documentation
8. Commits changes to current branch

**Key features:**
- Official docs integration (fetches from docs.claude.com)
- Pattern comparison (local vs official)
- Discrepancy alerts with citations
- Complete file generation
- Automated commit

---

### sync_skill_docs.py

**Purpose:** Semi-automated documentation sync tool for skill updates

**When to use:** After modifying a skill, to propagate changes across all related documentation

**Invocation:**
```bash
python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py \
  <skill-name> <new-version>
```

**Example:**
```bash
# Sync documentation after updating bmad-planner
python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py \
  bmad-planner 5.2.0
```

**What it does:**
1. Updates SKILL.md version in frontmatter
2. Identifies affected sections in WORKFLOW.md
3. Prompts for CHANGELOG entry
4. Creates git commit with proper format
5. Optionally archives previous version

**Key features:**
- Semi-automated (prompts for manual input)
- Updates multiple files consistently
- Enforces semantic versioning
- Proper commit message format

---

### VCS Abstraction Layer (vcs/)

**Purpose:** Provide unified interface for GitHub and Azure DevOps operations (PR creation, issue management)

**When to use:** When creating PRs, managing issues, or working with VCS providers

**Key files:**
- **provider.py** - Auto-detects VCS provider from git remote URL
- **base_adapter.py** - Defines base adapter interface
- **github_adapter.py** - GitHub CLI (gh) adapter
- **azure_adapter.py** - Azure DevOps CLI (az) adapter
- **config.py** - VCS configuration

**Example usage (from git-workflow-manager):**
```python
from .vcs.provider import detect_from_remote
from .vcs.github_adapter import GitHubAdapter
from .vcs.azure_adapter import AzureDevOpsAdapter

# Auto-detect provider
provider = detect_from_remote()

if provider == VCSProvider.GITHUB:
    adapter = GitHubAdapter()
elif provider == VCSProvider.AZURE_DEVOPS:
    adapter = AzureDevOpsAdapter()

# Create PR (unified interface)
pr_url = adapter.create_pr(
    title="feat: auth system (v1.6.0)",
    body="PR body content",
    source_branch="feature/20251103T143000Z_auth",
    target_branch="contrib/stharrold"
)
```

**Key features:**
- Auto-detection from git remote
- Unified interface (GitHub/Azure DevOps)
- CLI-based operations (gh/az)
- Error handling with helpful messages

---

## Usage by Claude Code

### File Deprecation

**Context:** User wants to replace old implementation with new one

**User says:**
- "Replace old auth with new implementation"
- "Deprecate old files"
- "Remove old code"

**Claude Code should:**
```python
import subprocess

# Deprecate old files (NEVER delete directly)
result = subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/deprecate_files.py',
    'TODO_feature_20251103T143000Z_auth.md',
    'old-auth-flow',
    'src/old_auth.py',
    'tests/test_old_auth.py'
], check=True)

print("✓ Old files archived to ARCHIVED/20251103T143000Z_old-auth-flow.zip")
```

---

### Creating Standard Directories

**Context:** User wants to create new planning or specs directory

**User says:**
- "Create planning directory"
- "Set up specs folder"
- "Make new directory for X"

**Claude Code should:**
```python
import subprocess

# Create directory with standard structure
result = subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/directory_structure.py',
    'planning/auth-system'
], check=True)

# Now directory has: CLAUDE.md, README.md, ARCHIVED/
```

---

### Workflow Lifecycle Management

**Phase 1/2: Register workflow in TODO.md**

**Context:** Just created TODO_feature_*.md file, need to track in master manifest

**Claude Code should:**
```python
import subprocess

# Register workflow in TODO.md
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/workflow_registrar.py',
    'TODO_feature_20251103T143000Z_auth.md',
    'feature',
    'auth-system',
    '--title', 'User Authentication System'
], check=True)

print("✓ Workflow registered in TODO.md (workflows.active[])")
```

**Phase 4.4: Archive completed workflow**

**Context:** PR merged, workflow complete, need to archive and update master manifest

**Claude Code should:**
```python
import subprocess

# Archive workflow
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/workflow_archiver.py',
    'TODO_feature_20251103T143000Z_auth.md',
    '--summary', 'Implemented OAuth2 authentication with Google and GitHub',
    '--version', '1.6.0'
], check=True)

print("✓ Workflow archived:")
print("  - Moved: TODO_*.md → ARCHIVED/TODO_*.md")
print("  - Updated: TODO.md (active[] → archived[])")
```

---

### Documentation Maintenance

**Context:** User updated a skill, need to sync documentation

**User says:**
- "Updated bmad-planner to v5.2.0"
- "Sync documentation"
- "Validate versions"

**Claude Code should:**
```python
import subprocess

# Validate version consistency
result = subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/validate_versions.py',
    '--verbose'
], check=False)

if result.returncode != 0:
    print("✗ Version inconsistencies found")
    # Show errors and prompt user

# Sync skill documentation
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/sync_skill_docs.py',
    'bmad-planner',
    '5.2.0'
], check=True)
```

---

### VCS Operations (PR Creation)

**Context:** User wants to create PR, need to detect VCS provider

**User says:**
- "Create PR"
- "Open pull request"

**Claude Code should:**
```python
from pathlib import Path
import sys

# Add vcs module to path
vcs_path = Path('.claude/skills/workflow-utilities/scripts')
sys.path.insert(0, str(vcs_path))

from vcs.provider import detect_from_remote, VCSProvider
from vcs.github_adapter import GitHubAdapter
from vcs.azure_adapter import AzureDevOpsAdapter

# Auto-detect provider
provider = detect_from_remote()

if provider == VCSProvider.GITHUB:
    adapter = GitHubAdapter()
    pr_url = adapter.create_pr(
        title="feat: auth system (v1.6.0)",
        body="PR body",
        source_branch="feature/20251103T143000Z_auth",
        target_branch="contrib/stharrold"
    )
elif provider == VCSProvider.AZURE_DEVOPS:
    adapter = AzureDevOpsAdapter()
    pr_url = adapter.create_pr(
        title="feat: auth system (v1.6.0)",
        body="PR body",
        source_branch="feature/20251103T143000Z_auth",
        target_branch="contrib/stharrold"
    )

print(f"✓ PR created: {pr_url}")
```

---

## Integration with Other Skills

**All skills depend on workflow-utilities:**

**bmad-planner:**
- Uses directory_structure.py to create planning/ directories
- Uses workflow_registrar.py to register planning in TODO.md
- May use deprecate_files.py to archive old planning

**speckit-author:**
- Uses directory_structure.py to create specs/ directories
- Uses todo_updater.py to update task status
- May use deprecate_files.py to archive old specs

**quality-enforcer:**
- Uses todo_updater.py to update quality_gates section in TODO frontmatter

**git-workflow-manager:**
- Uses VCS abstraction layer for PR creation
- Uses workflow_registrar.py and workflow_archiver.py for TODO.md lifecycle
- Uses todo_updater.py to track progress

**workflow-orchestrator:**
- Uses workflow_registrar.py and workflow_archiver.py for TODO.md management
- Uses todo_updater.py to track context usage
- Uses validate_versions.py to ensure consistency

**initialize-repository:**
- Uses directory_structure.py to create skill directories
- Uses create_skill.py patterns for new repository setup

**agentdb-state-manager:**
- Reads TODO files updated by todo_updater.py
- Uses workflow lifecycle (registrar/archiver) for state tracking

---

## Directory Standards

All directories created by workflow-utilities follow the standard structure:

```
directory/
├── CLAUDE.md      # Context for Claude Code
├── README.md      # Human-readable documentation
└── ARCHIVED/      # Deprecated files (except if directory IS archived)
    ├── CLAUDE.md
    └── README.md
```

**Enforced by:** directory_structure.py

---

## Best Practices

**File deprecation:**
- ❌ Never delete files directly
- ✅ Always use deprecate_files.py to archive

**Directory creation:**
- ❌ Don't manually create directories
- ✅ Use directory_structure.py for consistency

**TODO updates:**
- ❌ Don't manually edit TODO YAML frontmatter
- ✅ Use todo_updater.py for atomic updates

**Workflow lifecycle:**
- ❌ Don't manually update TODO.md manifest
- ✅ Use workflow_registrar.py and workflow_archiver.py

**Documentation maintenance:**
- ❌ Don't update versions without validation
- ✅ Use validate_versions.py before committing
- ✅ Use sync_skill_docs.py after skill changes

**VCS operations:**
- ❌ Don't hardcode GitHub-specific commands
- ✅ Use VCS abstraction layer for portability

---

## Constants and Rationale

**ARCHIVED/ directory:** All deprecated files go here
- **Rationale:** Preserve file history, enable recovery, audit trail

**Timestamp format:** `YYYYMMDDTHHMMSSZ` (compact ISO8601)
- **Rationale:** Sortable, parseable, no shell escaping issues

**TODO.md manifest structure:** YAML frontmatter with active[] and archived[] arrays
- **Rationale:** Single source of truth, machine-readable, git-tracked

**VCS abstraction:** Unified interface for GitHub/Azure DevOps
- **Rationale:** Portability, maintainability, future-proof

**Semantic versioning:** `MAJOR.MINOR.PATCH`
- **Rationale:** Industry standard, clear upgrade paths

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[UPDATE_CHECKLIST.md](../../UPDATE_CHECKLIST.md)** - Skill update checklist

**Child Directories:**
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived files

## Related Skills

- **workflow-orchestrator** - Uses workflow utilities for TODO management
- **bmad-planner** - Uses directory_structure.py, workflow_registrar.py
- **speckit-author** - Uses directory_structure.py, todo_updater.py
- **quality-enforcer** - Uses todo_updater.py for quality gates
- **git-workflow-manager** - Uses VCS abstraction, workflow lifecycle tools
- **initialize-repository** - Uses directory_structure.py, create_skill.py patterns
- **agentdb-state-manager** - Reads TODO files updated by workflow-utilities
