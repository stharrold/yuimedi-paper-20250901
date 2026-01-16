---
type: gemini-context
directory: .gemini/skills/workflow-utilities
purpose: Workflow Utilities provides **shared utilities** for all workflow skills. It includes file deprecation, directory structure creation, GEMINI.md hierarchy management, VCS abstraction (GitHub/Azure DevOps), documentation maintenance tools, and version validation. All other skills depend on workflow-utilities for consistent file operations.
parent: ../GEMINI.md
sibling_readme: README.md
children:
  - ARCHIVED/GEMINI.md
  - scripts/GEMINI.md
related_skills:
  - workflow-orchestrator
  - git-workflow-manager
  - initialize-repository
  - agentdb-state-manager
---

# Gemini Code Context: workflow-utilities

## Purpose

Workflow Utilities provides **shared utilities** for all workflow skills. It includes file deprecation, directory structure creation, GEMINI.md hierarchy management, VCS abstraction (GitHub/Azure DevOps), documentation maintenance tools, and version validation. All other skills depend on workflow-utilities for consistent file operations.

> **Note**: As of v7x1.0, workflow state tracking has migrated from TODO_*.md files to AgentDB (DuckDB). See `agentdb-state-manager` for the new system. The TODO-related scripts (todo_updater.py, workflow_registrar.py, workflow_archiver.py, sync_manifest.py) have been moved to ARCHIVED/.

## Directory Structure

```
.gemini/skills/workflow-utilities/
├── scripts/                        # Active utilities
│   ├── archive_manager.py          # List and extract archives
│   ├── check_ascii_only.py         # ASCII-only enforcement (Issue #121)
│   ├── container_utils.py          # Container detection utilities
│   ├── create_skill.py             # Create new skills
│   ├── deprecate_files.py          # Archive deprecated files
│   ├── directory_structure.py      # Create standard directory structure
│   ├── generate_gemini_md.py       # Generate missing GEMINI.md files
│   ├── safe_output.py              # ASCII-safe output formatting
│   ├── sync_skill_docs.py          # Documentation sync
│   ├── update_gemini_md_refs.py    # Update GEMINI.md children refs
│   ├── update_gemini_references.py # Update GEMINI.md references
│   ├── validate_versions.py        # Validate version consistency
│   ├── verify_workflow_context.py  # Workflow context validation + pending worktree detection
│   ├── workflow_progress.py        # Workflow progress tracking
│   ├── worktree_context.py         # Worktree state isolation
│   ├── vcs/                        # VCS abstraction layer
│   │   ├── provider.py             # VCS provider detection
│   │   ├── github_adapter.py       # GitHub CLI adapter
│   │   ├── azure_adapter.py        # Azure DevOps adapter
│   │   └── ...
│   └── __init__.py
├── SKILL.md                        # Complete skill documentation
├── GEMINI.md                       # This file
├── README.md                       # Human-readable overview
├── CHANGELOG.md                    # Version history
└── ARCHIVED/                       # Deprecated scripts
    ├── todo_updater.py             # [DEPRECATED] TODO file updates
    ├── workflow_registrar.py       # [DEPRECATED] TODO.md registration
    ├── workflow_archiver.py        # [DEPRECATED] TODO.md archiving
    ├── sync_manifest.py            # [DEPRECATED] TODO.md sync
    ├── GEMINI.md
    └── README.md
```

## Key Scripts

### deprecate_files.py

**Purpose:** Archive deprecated files with timestamp into ARCHIVED/ directory (never delete files directly)

**When to use:** When replacing old implementations, removing obsolete files, or deprecating unused code

**Invocation:**
```bash
python .gemini/skills/workflow-utilities/scripts/deprecate_files.py \
  <description> <file1> [file2 ...]
```

**Example:**
```bash
# Deprecate old authentication implementation
python .gemini/skills/workflow-utilities/scripts/deprecate_files.py \
  old-auth-flow \
  src/old_auth.py \
  tests/test_old_auth.py
```

**What it does:**
1. Validates all files to deprecate exist
2. Creates zip archive: `ARCHIVED/<timestamp>_<description>.zip`
3. Moves original files to archive
4. Removes original files from filesystem

**Key features:**
- Preserves file history (no deletion)
- Timestamped archives for traceability
- Validates all files before archiving
- Atomic operation (all or nothing)

---

### directory_structure.py

**Purpose:** Create standard directory structure with required files (GEMINI.md, README.md, ARCHIVED/)

**When to use:** When creating new directories (planning/, specs/, etc.) to ensure compliance with directory standards

**Invocation:**
```bash
python .gemini/skills/workflow-utilities/scripts/directory_structure.py \
  <directory>
```

**Example:**
```bash
# Create planning directory with standard structure
python .gemini/skills/workflow-utilities/scripts/directory_structure.py \
  planning/auth-system
```

**What it does:**
1. Creates directory if it doesn't exist
2. Creates `GEMINI.md` with template
3. Creates `README.md` with template
4. Creates `ARCHIVED/` subdirectory
5. Creates `ARCHIVED/GEMINI.md` and `ARCHIVED/README.md`

**Key features:**
- Enforces directory standards consistently
- Idempotent (safe to run multiple times)
- Template-based file creation
- Nested ARCHIVED/ structure

---

### archive_manager.py

**Purpose:** List, extract, and create archived files in ARCHIVED/ directory

**When to use:** When creating archives, inspecting archived files, recovering deprecated files, or auditing archives

**Invocation:**
```bash
# List archives in ARCHIVED/
python .gemini/skills/workflow-utilities/scripts/archive_manager.py list [directory]

# Extract archive to output directory
python .gemini/skills/workflow-utilities/scripts/archive_manager.py \
  extract <archive> [output_dir]

# Create archive from files (keeps originals)
python .gemini/skills/workflow-utilities/scripts/archive_manager.py \
  create [options] <description> <file1> [file2 ...]
```

**Create options:**
- `--delete` - Delete originals after archiving (same as deprecate_files.py)
- `--preserve-paths` - Preserve directory structure in archive
- `--output-dir DIR` - Output directory (default: ARCHIVED)

**Examples:**
```bash
# List all archives
python .gemini/skills/workflow-utilities/scripts/archive_manager.py list

# List archives in specific directory
python .gemini/skills/workflow-utilities/scripts/archive_manager.py list planning/auth-system

# Extract archive
python .gemini/skills/workflow-utilities/scripts/archive_manager.py \
  extract ARCHIVED/20251103T143000Z_old-auth-flow.zip \
  restored/

# Create archive (keep originals)
python .gemini/skills/workflow-utilities/scripts/archive_manager.py \
  create backup-before-refactor src/auth.py tests/test_auth.py

# Create archive and delete originals (same as deprecate)
python .gemini/skills/workflow-utilities/scripts/archive_manager.py \
  create --delete old-auth-flow src/old_auth.py

# Preserve directory paths in archive
python .gemini/skills/workflow-utilities/scripts/archive_manager.py \
  create --preserve-paths full-backup src/a/file.py src/b/file.py
```

**What it does:**
1. **List mode:** Scans ARCHIVED/ for .zip files, prints archive names and contents
2. **Extract mode:** Extracts archive to output directory (default: `restored/`)
3. **Create mode:** Creates timestamped archive, optionally deletes originals

**Key features:**
- Uses absolute paths (dynamically resolved from git root)
- Validates archive exists before extraction
- Lists archive contents before extraction
- Preserves directory structure on extraction
- Safe extraction (validates zip integrity)
- Shared `create_archive()` function used by deprecate_files.py

---

### validate_versions.py

**Purpose:** Validate version consistency across SKILL.md and WORKFLOW.md files

**When to use:** Before committing skill changes, before releases, when updating documentation

**Invocation:**
```bash
# Validate all versions
python .gemini/skills/workflow-utilities/scripts/validate_versions.py

# Show detailed version information
python .gemini/skills/workflow-utilities/scripts/validate_versions.py --verbose

# Attempt auto-fix (use with caution)
python .gemini/skills/workflow-utilities/scripts/validate_versions.py --fix
```

**What it does:**
1. Validates all SKILL.md files have valid semantic version in YAML frontmatter
2. Validates WORKFLOW.md has valid version
3. Checks WORKFLOW.md phase descriptions reference correct skill versions
4. Reports inconsistencies

**Key features:**
- Semantic versioning validation (`MAJOR.MINOR.PATCH`)
- Cross-file consistency checks
- Verbose mode for detailed reporting
- Exit code indicates success (0) or failure (1)

---

### verify_workflow_context.py

**Purpose:** Validate workflow context (main repo vs worktree, correct branch) before running slash commands. For steps 5-7, also detects pending worktrees with unmerged commits.

**When to use:** Automatically called by slash commands to ensure correct context

**Invocation:**
```bash
# Step shortcuts (recommended)
python .gemini/skills/workflow-utilities/scripts/verify_workflow_context.py --step 5

# Explicit flags
python .gemini/skills/workflow-utilities/scripts/verify_workflow_context.py \
  --require-main-repo --require-branch contrib/
```

**What it does:**
1. Validates location (main repo vs worktree)
2. Validates branch prefix (contrib/, feature/, release/)
3. For steps 5-7: Detects pending worktrees with unmerged commits
4. Prints non-blocking warnings about pending worktrees

**Step requirements:**
| Step | Location | Branch |
|------|----------|--------|
| 1 | Main repo | `contrib/*` |
| 2-4 | Worktree | `feature/*` |
| 5-6 | Main repo | `contrib/*` |
| 7 | Main repo | `contrib/*` |

**Key features:**
- Non-blocking pending worktree warnings (exit code 0 if context valid)
- Parses `git worktree list --porcelain` for accurate detection
- Counts commits ahead using `git rev-list --count`
- Reads `.gemini-state/workflow.json` for workflow step info

---

### create_skill.py

**Purpose:** Create new workflow skill with official Gemini Code documentation validation

**When to use:** When adding new skills to workflow system (rare - only 9 skills exist)

**Invocation:**
```bash
python .gemini/skills/workflow-utilities/scripts/create_skill.py <skill-name>
```

**Example:**
```bash
# Create new skill
python .gemini/skills/workflow-utilities/scripts/create_skill.py my-new-skill
```

**What it does:**
1. Asks configuration questions (purpose, phase, integration)
2. Fetches official Gemini Code skill documentation
3. Compares local workflow patterns with official patterns
4. Alerts user if discrepancies exist (with citations)
5. Generates all required files (SKILL.md, GEMINI.md, README.md, CHANGELOG.md)
6. Creates scripts/ directory with __init__.py
7. Creates ARCHIVED/ with documentation
8. Commits changes to current branch

**Key features:**
- Official docs integration (fetches from docs.gemini.com)
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
python .gemini/skills/workflow-utilities/scripts/sync_skill_docs.py \
  <skill-name> <new-version>
```

**Example:**
```bash
# Sync documentation after updating bmad-planner
python .gemini/skills/workflow-utilities/scripts/sync_skill_docs.py \
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

## Usage by Gemini Code

### File Deprecation

**Context:** User wants to replace old implementation with new one

**User says:**
- "Replace old auth with new implementation"
- "Deprecate old files"
- "Remove old code"

**Gemini Code should:**
```python
import subprocess

# Deprecate old files (NEVER delete directly)
result = subprocess.run([
    'python',
    '.gemini/skills/workflow-utilities/scripts/deprecate_files.py',
    'old-auth-flow',
    'src/old_auth.py',
    'tests/test_old_auth.py'
], check=True)

print("✓ Old files archived to ARCHIVED/<timestamp>_old-auth-flow.zip")
```

---

### Creating Standard Directories

**Context:** User wants to create new planning or specs directory

**User says:**
- "Create planning directory"
- "Set up specs folder"
- "Make new directory for X"

**Gemini Code should:**
```python
import subprocess

# Create directory with standard structure
result = subprocess.run([
    'python',
    '.gemini/skills/workflow-utilities/scripts/directory_structure.py',
    'planning/auth-system'
], check=True)

# Now directory has: GEMINI.md, README.md, ARCHIVED/
```

---

### Documentation Maintenance

**Context:** User updated a skill, need to sync documentation

**User says:**
- "Updated bmad-planner to v7x1.0"
- "Sync documentation"
- "Validate versions"

**Gemini Code should:**
```python
import subprocess

# Validate version consistency
result = subprocess.run([
    'python',
    '.gemini/skills/workflow-utilities/scripts/validate_versions.py',
    '--verbose'
], check=False)

if result.returncode != 0:
    print("✗ Version inconsistencies found")
    # Show errors and prompt user

# Sync skill documentation
subprocess.run([
    'python',
    '.gemini/skills/workflow-utilities/scripts/sync_skill_docs.py',
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

**Gemini Code should:**
```python
from pathlib import Path
import sys

# Add vcs module to path
vcs_path = Path('.gemini/skills/workflow-utilities/scripts')
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

**git-workflow-manager:**
- Uses VCS abstraction layer for PR creation
- Uses worktree_context.py for worktree state isolation

**workflow-orchestrator:**
- Uses validate_versions.py to ensure consistency
- Uses workflow_progress.py for phase tracking

**initialize-repository:**
- Uses directory_structure.py to create skill directories
- Uses create_skill.py patterns for new repository setup

**agentdb-state-manager:**
- Workflow state tracking (replaces TODO_*.md workflow)
- See `agentdb-state-manager` for current state tracking system

**Legacy Skills (Archived):**
- **bmad-planner**: Replaced by autonomous planning
- **speckit-author**: Replaced by autonomous implementation
- **quality-enforcer**: Replaced by Gemini Code Review

---

## Directory Standards

All directories created by workflow-utilities follow the standard structure:

```
directory/
├── GEMINI.md      # Context for Gemini Code
├── README.md      # Human-readable documentation
└── ARCHIVED/      # Deprecated files (except if directory IS archived)
    ├── GEMINI.md
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

**GEMINI.md hierarchy:**
- ❌ Don't manually create GEMINI.md files
- ✅ Use generate_gemini_md.py to create missing files
- ✅ Use update_gemini_md_refs.py to update children references

**Workflow state tracking:**
- ❌ Don't use TODO_*.md files (deprecated)
- ✅ Use AgentDB via `agentdb-state-manager` scripts

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

**GEMINI.md hierarchy:** Every directory has GEMINI.md with parent/child refs
- **Rationale:** AI navigation, context inheritance, documentation consistency

**VCS abstraction:** Unified interface for GitHub/Azure DevOps
- **Rationale:** Portability, maintainability, future-proof

**Semantic versioning:** `MAJOR.MINOR.PATCH`
- **Rationale:** Industry standard, clear upgrade paths

---







## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
- **[../GEMINI.md](../GEMINI.md)** - Parent directory: skills

**Child Directories:**
- **[ARCHIVED/GEMINI.md](ARCHIVED/GEMINI.md)** - Archived
- **[scripts/GEMINI.md](scripts/GEMINI.md)** - Scripts

## Related Skills

- **workflow-orchestrator** - Uses workflow utilities for phase tracking
- **git-workflow-manager** - Uses VCS abstraction, worktree_context.py
- **initialize-repository** - Uses directory_structure.py, create_skill.py
- **agentdb-state-manager** - Workflow state tracking (replaces TODO_*.md)
