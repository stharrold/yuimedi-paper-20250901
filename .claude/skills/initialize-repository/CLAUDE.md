---
type: claude-context
directory: .claude/skills/initialize-repository
purpose: Initialize-repository is a **meta-skill (Phase 0)** that bootstraps new repositories with the complete workflow system. It provides an interactive callable tool for replicating skills, documentation, and standards from a source repository to a new target repository. Unlike other skills that operate within a repository, this meta-skill operates across repositories (source → target) and is used once per new project.
parent: ../CLAUDE.md
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
  - scripts/CLAUDE.md
related_skills:
  - workflow-orchestrator - Main coordinator for workflow phases
  - tech-stack-adapter - Detects Python/uv project configuration
  - git-workflow-manager - Git operations, worktrees, semantic versioning
  - workflow-utilities - Shared utilities for all skills
  - agentdb-state-manager - Persistent state tracking (optional)
  - initialize-repository - This meta-skill (for future replication)
---

# Claude Code Context: initialize-repository

## Purpose

Initialize-repository is a **meta-skill (Phase 0)** that bootstraps new repositories with the complete workflow system. It provides an interactive callable tool for replicating skills, documentation, and standards from a source repository to a new target repository. Unlike other skills that operate within a repository, this meta-skill operates across repositories (source → target) and is used once per new project.

## Directory Structure

```
.claude/skills/initialize-repository/
├── scripts/
│   ├── initialize_repository.py  # Bootstrap NEW repos (interactive Q&A)
│   ├── apply_workflow.py         # Apply workflow to EXISTING repos (clone-and-apply)
│   └── __init__.py              # Package initialization
├── SKILL.md                      # Complete skill documentation
├── CLAUDE.md                     # This file
├── README.md                     # Human-readable overview
├── CHANGELOG.md                  # Version history
└── ARCHIVED/                     # Deprecated files
    ├── CLAUDE.md
    └── README.md
```

## Key Scripts

### initialize_repository.py (Bootstrap NEW repos)

**Purpose:** Interactive tool to bootstrap new repositories with complete workflow system (9 skills, documentation, standards)

**When to use:** Phase 0 (before any other workflow phases) - run once per new repository

**Location requirement:** Can be run from anywhere, requires paths to source and target repositories

**Invocation:**
```bash
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  <source-repo> <target-repo>
```

**Examples:**
```bash
# From current repository to new sibling repository
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  . ../my-new-project

# From absolute paths
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  /Users/stharrold/Documents/GitHub/german \
  /Users/stharrold/Documents/GitHub/my-cli-tool

# From relative paths
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  ~/Code/german ~/Code/fastapi-backend
```

**What it does:**

1. **Validation (Pre-flight checks):**
   - Validates source repository exists and has workflow system (≥3/9 skills)
   - Validates target repository path is valid
   - Validates required tools installed (`git`, VCS CLI if remote setup)
   - Checks source has .claude/skills/ directory
   - Counts skills in source (requires at least 3 of 9)

2. **Phase 1: Configuration Selection (Interactive Q&A - 9 questions):**
   - Q1: Repository purpose (Web app / CLI tool / Library / Data / ML / Other)
   - Q2: Brief description (one line summary)
   - Q3: GitHub username (auto-detected from `gh whoami`)
   - Q4: Python version (3.11 / 3.12 / 3.13)
   - Q5: Copy workflow system? (required, always yes)
   - Q6: Copy domain-specific content (src/, resources/)? (yes/no)
   - Q7: Copy sample tests (tests/)? (yes/no)
   - Q8: Copy container configs (Containerfile, podman-compose.yml)? (yes/no)
   - Q9: Copy CI/CD pipelines (.github/workflows/tests.yml, azure-pipelines.yml)? (yes/no)

3. **Phase 2: Git Setup (Interactive Q&A - 4-5 questions):**
   - Q10: Initialize git repository? (yes/no)
   - Q11: If yes: Create branch structure (main, develop, contrib)? (yes/no)
   - Q12: If yes: Set up remote repository? (yes/no)
   - Q13: If yes: Remote URL (e.g., https://github.com/user/repo.git)
   - Q14: If yes and remote: Push to remote? (yes/no)

4. **Phase 3: File Operations (Automatic - no user input):**

   **Always copied verbatim:**
   - `.claude/skills/workflow-orchestrator/` (main coordinator)
   - `.claude/skills/tech-stack-adapter/` (project detection)
   - `.claude/skills/git-workflow-manager/` (git automation)
   - `.claude/skills/bmad-planner/` (planning Q&A)
   - `.claude/skills/speckit-author/` (specification generation)
   - `.claude/skills/quality-enforcer/` (quality gates)
   - `.claude/skills/workflow-utilities/` (shared utilities)
   - `.claude/skills/initialize-repository/` (this meta-skill)
   - `WORKFLOW.md` (complete 6-phase workflow guide)
   - `CONTRIBUTING.md` (contributor guidelines)
   - `.claude/skills/UPDATE_CHECKLIST.md` (skill update checklist)
   - `.gitignore` (git exclusions)

   **Optionally copied verbatim:**
   - `.claude/skills/agentdb-state-manager/` (if user selected yes)
   - `src/` directory (if copy_domain = yes)
   - `resources/` directory (if copy_domain = yes)
   - `tests/` directory (if copy_tests = yes)
   - `Containerfile` (if copy_containers = yes)
   - `podman-compose.yml` (if copy_containers = yes)
   - `.github/workflows/tests.yml` (if copy_cicd = yes)
   - `azure-pipelines.yml` (if copy_cicd = yes)

   **Generated/adapted for new repo:**
   - `README.md` - Uses repo name, purpose, description from Q&A
   - `CLAUDE.md` - Uses repo purpose, inserts workflow section from source
   - `pyproject.toml` - Uses repo name, description, Python version from Q&A
   - `CHANGELOG.md` - Creates initial [0.1.0] entry with current date
   - `TODO.md` - Creates master workflow manifest with current timestamp

   **Created from scratch:**
   - `ARCHIVED/` directory with CLAUDE.md and README.md
   - `planning/` directory with CLAUDE.md, README.md, ARCHIVED/
   - `specs/` directory with CLAUDE.md, README.md, ARCHIVED/

5. **Phase 4: Git Initialization (Conditional - only if init_git = yes):**
   - Initialize git repository (`git init`)
   - Stage all files (`git add .`)
   - Create initial commit on main:
     ```
     chore: initialize repository with workflow system v7x1

     Bootstrapped from <source-repo> using initialize-repository meta-skill.

     Includes:
     - Complete workflow system (9 skills)
     - WORKFLOW.md, CONTRIBUTING.md documentation
     - Standard directory structure (ARCHIVED/, planning/, specs/)
     - Quality configurations (.gitignore, pyproject.toml)

     🤖 Generated with Claude Code
     Co-Authored-By: Claude Code <noreply@anthropic.com>
     ```
   - If create_branches = yes:
     - Create develop branch from main
     - Create contrib/<gh-user> branch from develop
     - Checkout main
   - If remote_url provided:
     - Add remote origin
     - If push_to_remote = yes:
       - Push main, develop, contrib branches to origin

6. **Validation (Post-creation checks):**
   - Validates target repository structure
   - Checks all required directories exist
   - Validates git repository (if initialized)
   - Validates branches (if created)
   - Counts skills in target (should equal skills in source)

7. **Report and Next Steps:**
   - Prints summary of what was created
   - Lists directories, files, branches created
   - Provides next step commands:
     ```bash
     cd /path/to/target-repo
     uv sync
     python .claude/skills/bmad-planner/scripts/create_planning.py <feature> <gh-user>
     ```

**Key features:**
- Copies all 9 skills (including this meta-skill for future replication)
- Adapts README.md, CLAUDE.md, pyproject.toml for new repo context
- Copies WORKFLOW.md, CONTRIBUTING.md verbatim (workflow is tech-agnostic)
- Creates compliant directory structure (ARCHIVED/, planning/, specs/)
- Optional git initialization with 3-branch structure (main, develop, contrib)
- Optional remote setup and push
- Validates result and provides actionable next steps
- **Color-coded output** for clarity (blue headers, green success, yellow warnings, red errors)
- **Error handling** with helpful messages and cleanup on failure

**Exit codes:**
- 0: Success - repository initialized
- 1: Validation error (invalid paths, missing skills, etc.)
- 2: Git error (initialization failed, remote unreachable, etc.)
- 3: File operation error (copy failed, permission denied, etc.)

---

### apply_workflow.py (Apply to EXISTING repos)

**Purpose:** Apply workflow system from a cloned template repository to an existing repository. Designed for the "clone and apply" use case.

**When to use:** When you have an existing repository and want to add the workflow system by cloning stharrold-templates locally.

**Invocation:**
```bash
cd my-repo
mkdir -p .tmp
git clone https://github.com/stharrold/stharrold-templates.git .tmp/stharrold-templates

python .tmp/stharrold-templates/.claude/skills/initialize-repository/scripts/apply_workflow.py \
  .tmp/stharrold-templates .

# Or with --force to overwrite without prompting:
python .tmp/stharrold-templates/.claude/skills/initialize-repository/scripts/apply_workflow.py \
  .tmp/stharrold-templates . --force
```

**What it does:**

1. Validates source has `.claude/skills/` and `.claude/commands/`
2. Validates target is a git repository
3. Prompts before overwriting existing `.claude/` (unless `--force`)
4. Copies `.claude/skills/` (all skills)
5. Copies `.claude/commands/` (v7x1 workflow commands)
6. Copies `WORKFLOW.md`, `CONTRIBUTING.md`
7. Merges `pyproject.toml` (adds dev dependencies, preserves existing)
8. Merges `.gitignore` (appends workflow patterns, deduplicates)

**Key differences from initialize_repository.py:**

| Aspect | initialize_repository.py | apply_workflow.py |
|--------|--------------------------|-------------------|
| Target | New (empty) repos | Existing repos |
| Q&A | Interactive (13+ questions) | Minimal (just confirm) |
| Config files | Generates new | Merges with existing |
| Git setup | Creates branches | Preserves existing |
| .tmp cleanup | N/A | Keeps clone |

**Flags:**

| Flag | Behavior |
|------|----------|
| (none) | Prompts if `.claude/` exists |
| `--force` | Deletes existing `.claude/` entirely, copies fresh |

**Exit codes:**
- 0: Success
- 1: Source validation failed
- 2: Target validation failed
- 3: User cancelled

---

## Usage by Claude Code

### When to Call This Meta-Skill

**Context:** User wants to start a new repository with the workflow system

**User says:**
- "Initialize a new repository"
- "Bootstrap workflow system"
- "Replicate workflow to new repo"
- "Start new project with this workflow"
- "Create new repo from this template"

**Claude Code should:**

1. **Recognize Phase 0 context:**
   ```python
   # This is NOT part of normal workflow (Phases 1-6)
   # This is Phase 0 - bootstrapping a NEW repository
   ```

2. **Call the script (don't reproduce functionality):**
   ```python
   import subprocess

   # Let the callable tool handle all logic
   result = subprocess.run([
       'python',
       '.claude/skills/initialize-repository/scripts/initialize_repository.py',
       '.',  # source repo (current directory)
       '../my-new-project'  # target repo
   ], check=False)

   if result.returncode == 0:
       print("✓ Repository initialized successfully")
       print("Next steps:")
       print("  1. cd ../my-new-project")
       print("  2. uv sync")
       print("  3. Start Phase 1 (BMAD planning)")
   else:
       print("✗ Initialization failed - check error messages above")
   ```

3. **Script handles everything:**
   - All Q&A with user
   - File copying and adaptation
   - Git initialization
   - Validation
   - Error handling with cleanup

4. **After script completes:**
   - User navigates to new repository
   - User starts Phase 1 (BMAD planning)
   - This meta-skill is not used again in new repository

---

### When to Call apply_workflow.py

**Context:** User has an existing repository and wants to apply the workflow system from a cloned template

**User says:**
- "Apply the workflow in .tmp/stharrold-templates to this repo"
- "Apply the workflow in X to Y"
- "Copy the workflow from the cloned templates"
- "Install the v7x1 workflow commands"

**Claude Code should:**

1. **Recognize apply-to-existing context:**
   ```python
   # User has cloned stharrold-templates to .tmp/
   # User wants to apply workflow to EXISTING repo
   ```

2. **Call the script:**
   ```bash
   python .tmp/stharrold-templates/.claude/skills/initialize-repository/scripts/apply_workflow.py \
     .tmp/stharrold-templates .
   ```

3. **Or with --force (if user says "overwrite" or "replace"):**
   ```bash
   python .tmp/stharrold-templates/.claude/skills/initialize-repository/scripts/apply_workflow.py \
     .tmp/stharrold-templates . --force
   ```

4. **After script completes:**
   - Review changes: `git status`
   - Install dependencies: `uv sync`
   - Start using v7x1 workflow: `/workflow:v7x1_1-worktree "feature"`
   - Optional cleanup: `rm -rf .tmp/`

---

### Token Efficiency

**Before callable tool (Manual approach):**
```
Claude Code reads WORKFLOW.md                     ~500 tokens
Claude Code reads CLAUDE.md                       ~300 tokens
Claude Code reads all skill SKILL.md files      ~1,200 tokens
Claude Code manually copies files                 ~800 tokens
Claude Code manually adapts documentation         ~400 tokens
Claude Code manually creates git structure        ~300 tokens
                                           ___________
Total:                                     ~3,500 tokens
```

**After callable tool:**
```
Claude Code invokes script                        ~150 tokens
Script handles all logic                        0 tokens (no Claude Code context)
                                           ___________
Total:                                       ~150 tokens
```

**Savings: ~3,350 tokens (96% reduction)**

**Time savings:** ~30-60 minutes of manual work

---

### Safety for Existing Repositories

**⚠️ WARNING:** This script is designed for **new, empty repositories**. Applying it to an existing repository with content will:

1. **Overwrite these files:**
   - README.md
   - CLAUDE.md
   - pyproject.toml
   - .gitignore
   - CHANGELOG.md
   - TODO.md

2. **Add these directories:**
   - .claude/skills/ (9 skills)
   - ARCHIVED/
   - planning/
   - specs/

3. **NOT touch:**
   - src/ (unless copy_domain = yes, then merges)
   - tests/ (unless copy_tests = yes, then merges)
   - Existing git history

**Recommended approach for existing repositories:**

**Option 1: Test-copy approach (SAFEST)**
```bash
# 1. Copy existing repo to test location
cp -r ~/Code/my-existing-repo ~/Code/my-existing-repo-test

# 2. Run initialization on test copy
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  ~/Code/german ~/Code/my-existing-repo-test

# 3. Review changes in test copy
cd ~/Code/my-existing-repo-test
git status
git diff

# 4. If satisfied, apply manually to original
# (cherry-pick specific files/directories)
```

**Option 2: Backup-first approach**
```bash
# 1. Create complete backup
cp -r ~/Code/my-existing-repo ~/Code/my-existing-repo-backup-$(date +%Y%m%d)

# 2. Commit current state
cd ~/Code/my-existing-repo
git add .
git commit -m "chore: backup before workflow initialization"

# 3. Run initialization (overwrites files)
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  ~/Code/german ~/Code/my-existing-repo

# 4. Review changes, revert if needed
git diff HEAD~1
git reset --hard HEAD~1  # if you want to revert
```

**Option 3: Manual selective copy (MOST CONTROL)**
```bash
# Copy only .claude/skills/ directory
cp -r ~/Code/german/.claude ~/Code/my-existing-repo/

# Copy WORKFLOW.md, CONTRIBUTING.md
cp ~/Code/german/WORKFLOW.md ~/Code/my-existing-repo/
cp ~/Code/german/CONTRIBUTING.md ~/Code/my-existing-repo/

# Manually integrate pyproject.toml, README.md, CLAUDE.md
# (don't overwrite - merge manually)
```

---

## Integration with Other Skills

**This meta-skill does NOT integrate with other skills during execution.**

**Relationship to workflow:**

```
Phase 0: Initialize Repository (this meta-skill)
  │
  ├─> Creates environment containing:
  │   ├─ 9 skills (.claude/skills/*)
  │   ├─ Complete documentation (WORKFLOW.md, CONTRIBUTING.md)
  │   ├─ Quality configurations (pyproject.toml, .gitignore)
  │   └─ Directory structure (ARCHIVED/, planning/, specs/)
  │
  ↓
Phase 1-6: Normal workflow (bmad, speckit, quality, git, etc.)
  └─> Skills operate within the repository created by Phase 0
```

**After initialization:**
- New repository has all skills installed
- User starts with Phase 1 (BMAD planning) or Phase 2 (SpecKit)
- This meta-skill is not used again in that repository
- If user wants to replicate to another new repo, they call this meta-skill again

**Key distinction:**
- **Other skills** operate **within** a repository (modify code, create docs, run tests)
- **This meta-skill** operates **across** repositories (source → target replication)
- **Other skills** are coordinated by workflow-orchestrator
- **This meta-skill** is standalone (no orchestrator involvement)
- **Other skills** are called repeatedly throughout development
- **This meta-skill** is called once per new repository

---

## Components Copied

### Always Copied (Required)

**6 workflow skills:**
1. workflow-orchestrator - Main coordinator for workflow phases
2. tech-stack-adapter - Detects Python/uv project configuration
3. git-workflow-manager - Git operations, worktrees, semantic versioning
4. workflow-utilities - Shared utilities for all skills
5. agentdb-state-manager - Persistent state tracking (optional)
6. initialize-repository - This meta-skill (for future replication)

**Documentation:**
- WORKFLOW.md (copied verbatim) - Complete 6-phase workflow guide
- CONTRIBUTING.md (copied verbatim) - Contributor guidelines
- .claude/skills/UPDATE_CHECKLIST.md (copied verbatim) - Skill update checklist

**Generated files (adapted for new repo):**
- README.md - Uses repo name, purpose, description from Q&A
- CLAUDE.md - Uses repo purpose, inserts workflow section
- pyproject.toml - Generated with new repo name, Python version, dependencies
- CHANGELOG.md - Generated with initial [0.1.0] entry
- TODO.md - Generated master workflow manifest

**Configuration:**
- .gitignore (copied verbatim) - Git exclusions

**Directory structure:**
- ARCHIVED/ - With CLAUDE.md, README.md
- planning/ - With CLAUDE.md, README.md, ARCHIVED/
- specs/ - With CLAUDE.md, README.md, ARCHIVED/

### Optionally Copied

**Domain content** (if user selects copy_domain = yes):
- src/ directory - Source code
- resources/ directory - Data files, templates, etc.

**Tests** (if user selects copy_tests = yes):
- tests/ directory - Test files

**Containers** (if user selects copy_containers = yes):
- Containerfile - Container image definition
- podman-compose.yml - Multi-container orchestration

**Advanced skill** (if user selects copy_agentdb = yes):
- .claude/skills/agentdb-state-manager/ - DuckDB state tracking

---

## Adaptation Logic

**Philosophy:** Copy workflow verbatim (tech-agnostic), adapt only repository-specific files

### Files Copied Verbatim (No Changes)

```python
COPY_VERBATIM = [
    '.claude/skills/*',           # All 9 skills
    'WORKFLOW.md',                # Complete workflow guide
    'CONTRIBUTING.md',            # Contributor guidelines
    '.claude/skills/UPDATE_CHECKLIST.md',  # Skill update checklist
    '.gitignore',                 # Git exclusions
]
```

**Rationale:** Workflow system is technology-agnostic and standardized. No customization needed.

### Files Generated/Adapted

**README.md template:**
```markdown
# {repo_name}

{description}

## Purpose

{purpose_description}

## Technology Stack

- Language: Python {python_version}
- Package Manager: uv
- Git Workflow: Git-flow + GitHub-flow hybrid with worktrees
- Workflow System: Skill-based architecture (9 specialized skills)

[... rest of template from source README.md ...]
```

**CLAUDE.md template:**
```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

{purpose_description}

{description}

## Workflow v7x1 Architecture

This repository uses a **skill-based workflow system** located in `.claude/skills/`.

[... complete workflow section copied from source CLAUDE.md ...]
```

**pyproject.toml template:**
```toml
[project]
name = "{repo_name}"
version = "0.1.0"
description = "{description}"
requires-python = ">={python_version}"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=8.4.2",
    "pytest-cov>=7.0.0",
    "ruff>=0.14.1",
    "mypy>=1.18.2",
]
```

**CHANGELOG.md template:**
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - {current_date}

### Added
- Initial repository structure
- Complete workflow system (9 skills)
- WORKFLOW.md, CONTRIBUTING.md documentation
- Quality configurations
```

**TODO.md template:**
```yaml
---
type: workflow-master-manifest
version: 5.2.0
last_update: "{current_timestamp}"

workflows:
  active: []
  archived: []

context_stats:
  total_workflows_completed: 0
  current_token_usage: 0
  last_checkpoint: "{current_timestamp}"
  recent_improvements: "Repository initialized with workflow system v7x1"
---

# Master TODO Manifest

No active workflows. Use Phase 1 (BMAD planning) to start your first feature.
```

---

## Interactive Q&A Summary

**Total questions: 13-14 (depending on git setup choices)**

### Phase 1: Configuration (9 questions)

1. **Repository purpose** (enum: Web app, CLI tool, Library, Data, ML, Other)
2. **Brief description** (string: one line summary)
3. **GitHub username** (string: auto-detected from `gh whoami`)
4. **Python version** (enum: 3.11, 3.12, 3.13)
5. **Copy workflow system?** (boolean: required, always yes)
6. **Copy domain content?** (boolean: src/, resources/)
7. **Copy sample tests?** (boolean: tests/)
8. **Copy container configs?** (boolean: Containerfile, podman-compose.yml)
9. **Copy CI/CD pipelines?** (boolean: .github/workflows/tests.yml, azure-pipelines.yml)

### Phase 2: Git Setup (4-5 questions)

10. **Initialize git repository?** (boolean)
11. **If yes: Create branch structure?** (boolean: main, develop, contrib)
12. **If yes: Set up remote?** (boolean)
13. **If yes: Remote URL** (string: e.g., https://github.com/user/repo.git)
14. **If yes and remote: Push to remote?** (boolean)

---

## Output Structure

After successful initialization, target repository has:

```
target-repo/
├── .claude/
│   └── skills/                  # 9 skills copied
│       ├── workflow-orchestrator/
│       ├── tech-stack-adapter/
│       ├── git-workflow-manager/
│       ├── bmad-planner/
│       ├── speckit-author/
│       ├── quality-enforcer/
│       ├── workflow-utilities/
│       ├── agentdb-state-manager/  # (optional)
│       ├── initialize-repository/  # (this meta-skill)
│       └── UPDATE_CHECKLIST.md
├── ARCHIVED/                    # With CLAUDE.md, README.md
├── planning/                    # With CLAUDE.md, README.md, ARCHIVED/
├── specs/                       # With CLAUDE.md, README.md, ARCHIVED/
├── README.md                    # Generated for new repo
├── CLAUDE.md                    # Generated for new repo
├── WORKFLOW.md                  # Copied verbatim
├── CONTRIBUTING.md              # Copied verbatim
├── CHANGELOG.md                 # Generated with v0.1.0
├── TODO.md                      # Generated master manifest
├── pyproject.toml               # Generated with new repo details
└── .gitignore                   # Copied verbatim

Optionally (based on user choices):
├── src/                         # If copy_domain = yes
├── resources/                   # If copy_domain = yes
├── tests/                       # If copy_tests = yes
├── Containerfile                # If copy_containers = yes
├── podman-compose.yml           # If copy_containers = yes
├── .github/workflows/tests.yml  # If copy_cicd = yes
└── azure-pipelines.yml          # If copy_cicd = yes

Git structure (if init_git = yes):
├── .git/                        # Git repository
└── Branches:
    ├── main                     # Initial commit
    ├── develop                  # From main (if create_branches = yes)
    └── contrib/<gh-user>        # From develop (if create_branches = yes)

Remote (if remote_url provided):
    origin → <remote_url>        # Pushed (if push_to_remote = yes)
```

---

## Workflow Integration

**NOT part of Phase 1-6 workflow.** This is Phase 0 (bootstrapping).

**Lifecycle:**

```
┌──────────────────────────────────────────────────┐
│ Phase 0: Initialize Repository (One-time setup)  │
│                                                  │
│ User has Repository A with workflow system      │
│ User wants Repository B with same workflow      │
│                                                  │
│ Action: Run initialize_repository.py            │
│         Source: Repository A                     │
│         Target: Repository B                     │
│                                                  │
│ Result: Repository B has workflow system        │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│ Phase 1-6: Normal Workflow (Ongoing development) │
│                                                  │
│ User works in Repository B:                     │
│   Phase 1: BMAD planning                        │
│   Phase 2: SpecKit + Implementation             │
│   Phase 3: Quality gates                        │
│   Phase 4: Integration + PRs                    │
│   Phase 5: Release                              │
│   Phase 6: Hotfix (as needed)                   │
│                                                  │
│ This meta-skill is NOT used again               │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│ Future: Replicate to Repository C (Optional)     │
│                                                  │
│ User wants Repository C with same workflow      │
│                                                  │
│ Action: Run initialize_repository.py again      │
│         Source: Repository B (or A)             │
│         Target: Repository C                     │
│                                                  │
│ Result: Repository C has workflow system        │
└──────────────────────────────────────────────────┘
```

---

## Example Usage

### Complete Interactive Session

```bash
# User has 'german' repository with workflow system
# User wants 'fastapi-backend' repository with same workflow

$ python .claude/skills/initialize-repository/scripts/initialize_repository.py \
    ~/Code/german ~/Code/fastapi-backend

=== Repository Initialization ===

Source repository: /Users/stharrold/Code/german
Target repository: /Users/stharrold/Code/fastapi-backend

✓ Source repository validated (9 skills found)
✓ Target path is valid

=== Phase 1: Configuration Selection ===

What is the primary purpose of this repository?
  1) Web application
  2) CLI tool
  3) Library/package
  4) Data analysis
  5) Machine learning
  6) Other
> 1

Brief description of the repository (one line):
> FastAPI backend service for web application

GitHub username (detected: stharrold):
> stharrold

Python version:
  1) 3.11
  2) 3.12
  3) 3.13
> 2

Copy workflow system? (required)
> yes

Copy domain-specific content (src/, resources/)?
> no

Copy sample tests (tests/)?
> yes

Copy container configs (Containerfile, podman-compose.yml)?
> yes

Copy CI/CD pipelines (.github/workflows/tests.yml, azure-pipelines.yml)?
> yes

=== Phase 2: Git Setup ===

Initialize git repository?
> yes

Create branch structure (main, develop, contrib)?
> yes

Set up remote repository?
> yes

Remote URL (e.g., https://github.com/user/repo.git):
> https://github.com/stharrold/fastapi-backend.git

Push to remote?
> yes

=== Phase 3: File Operations ===

✓ Created target directory
✓ Copied 8 workflow skills
✓ Copied documentation (WORKFLOW.md, CONTRIBUTING.md)
✓ Generated README.md
✓ Generated CLAUDE.md
✓ Generated pyproject.toml
✓ Generated CHANGELOG.md (v0.1.0)
✓ Generated TODO.md manifest
✓ Copied .gitignore
✓ Copied tests/ directory
✓ Copied Containerfile
✓ Copied podman-compose.yml
✓ Created directory structure (ARCHIVED/, planning/, specs/)

=== Phase 4: Git Initialization ===

✓ Initialized git repository
✓ Created initial commit on main
✓ Created develop branch
✓ Created contrib/stharrold branch
✓ Set up remote origin
✓ Pushed main branch to remote
✓ Pushed develop branch to remote
✓ Pushed contrib/stharrold branch to remote

=== Validation ===

✓ Target repository structure validated
✓ All required directories exist
✓ Git repository initialized
✓ Branches created (main, develop, contrib/stharrold)
✓ Remote configured (origin)

=== Summary ===

Repository initialized successfully!

Created:
  - 8 workflow skills (.claude/skills/)
  - Documentation (WORKFLOW.md, CONTRIBUTING.md, README.md, CLAUDE.md)
  - Configuration (pyproject.toml, .gitignore, CHANGELOG.md, TODO.md)
  - Directory structure (ARCHIVED/, planning/, specs/)
  - Test directory (tests/)
  - Container configs (Containerfile, podman-compose.yml)
  - CI/CD pipelines (GitHub Actions + Azure Pipelines)
  - Git repository with 3 branches
  - Remote origin configured and pushed

Next steps:
  1. cd ~/Code/fastapi-backend
  2. uv sync
  3. uv run pytest
  4. Start Phase 1: python .claude/skills/bmad-planner/scripts/create_planning.py <feature> stharrold

Repository: ~/Code/fastapi-backend
Remote: https://github.com/stharrold/fastapi-backend.git
```

---

## Best Practices

### When Calling This Meta-Skill

**✅ Do:**
1. Ensure source repository has complete workflow system (≥3/9 skills)
2. Validate `gh` CLI is authenticated before running (if using GitHub)
3. Decide what to copy:
   - **Workflow-only** recommended for clean start (no domain content)
   - **Include tests** if source has good test patterns
   - **Include containers** if deploying with containers
4. Have remote repository URL ready if setting up remote
5. After initialization, review and customize:
   - README.md (add project-specific details)
   - CLAUDE.md (add domain-specific guidance)
   - pyproject.toml (add project dependencies)

**❌ Don't:**
1. Use on repository with existing workflow system (update manually instead)
2. Use on repository with extensive custom content (risk of overwrites)
3. Skip validation messages (may indicate missing requirements)
4. Push to remote without reviewing generated files first
5. Forget to run `uv sync` after initialization

### For Existing Repositories

**If repository already has content:**

**Option 1: Test-copy approach (SAFEST)**
```bash
# Create test copy, run initialization, review changes
cp -r ~/Code/my-repo ~/Code/my-repo-test
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  ~/Code/german ~/Code/my-repo-test
# Review: cd ~/Code/my-repo-test && git status
# If good: manually copy specific files to original
```

**Option 2: Backup-first approach**
```bash
# Backup, commit current state, run initialization, review
cp -r ~/Code/my-repo ~/Code/my-repo-backup-$(date +%Y%m%d)
cd ~/Code/my-repo && git add . && git commit -m "backup"
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  ~/Code/german ~/Code/my-repo
# Review: git diff HEAD~1
# Revert if needed: git reset --hard HEAD~1
```

**Option 3: Manual selective copy (MOST CONTROL)**
```bash
# Copy only specific components
cp -r ~/Code/german/.claude ~/Code/my-repo/
cp ~/Code/german/WORKFLOW.md ~/Code/my-repo/
# Merge pyproject.toml, README.md manually (don't overwrite)
```

---

## Constants and Rationale

**SKILL_NAMES:** List of 9 workflow skills
```python
SKILL_NAMES = [
    'workflow-orchestrator',
    'tech-stack-adapter',
    'git-workflow-manager',
    'workflow-utilities',
    'agentdb-state-manager',
    'initialize-repository',
]
```
- **Rationale:** Define complete workflow system. All skills are copied to maintain full functionality.

**REQUIRED_TOOLS:** ['git']
- **Rationale:** Minimum tools required. VCS CLI (gh/az) detected automatically if remote setup requested.

**TIMESTAMP_FORMAT:** '%Y%m%dT%H%M%SZ'
- **Rationale:** Compact ISO8601 format, consistent with worktree/TODO file naming throughout workflow.

**COPY_VERBATIM:** ['.claude/skills/', 'WORKFLOW.md', 'CONTRIBUTING.md', '.gitignore']
- **Rationale:** Workflow system is tech-agnostic and standardized. No customization needed.

**ADAPT_FILES:** ['README.md', 'CLAUDE.md', 'pyproject.toml', 'CHANGELOG.md', 'TODO.md']
- **Rationale:** Repository-specific files must be customized with new repo details from Q&A.

---

## Error Handling

**Common errors and solutions:**

**Error: "Source repository does not have workflow system"**
```
✗ Error: Source repository does not have workflow system
  Expected: ≥3/9 skills in .claude/skills/
  Found: 0 skills

  Fix: Use a repository that has the workflow system installed
```

**Error: "Target repository already exists"**
```
✗ Error: Target directory already exists: /path/to/target

  Options:
  1. Remove target: rm -rf /path/to/target
  2. Choose different target: /path/to/target-v2
  3. Use test-copy approach (see Best Practices)
```

**Error: "git not installed"**
```
✗ Error: Required tool not installed: git

  Install: brew install git (macOS) or apt install git (Linux)
```

**Error: "gh CLI not authenticated"**
```
✗ Error: GitHub CLI not authenticated
  Cannot detect GitHub username

  Fix: gh auth login
```

**Error: "Remote repository unreachable"**
```
✗ Error: Failed to push to remote
  fatal: unable to access 'https://github.com/user/repo.git/': Could not resolve host

  Fixes:
  1. Check remote URL is correct
  2. Check network connectivity
  3. Check repository exists on GitHub
  4. Check gh auth status
```

**Error: "Permission denied during file copy"**
```
✗ Error: Permission denied: /path/to/target/file

  Fix: Check directory permissions and ownership
```

---

## Token Savings

**Detailed breakdown:**

**Manual approach (before callable tool):**
| Step | Tokens | Description |
|------|--------|-------------|
| Read WORKFLOW.md | 500 | Understanding workflow phases |
| Read CLAUDE.md | 300 | Understanding repository context |
| Read all SKILL.md files | 1,200 | Understanding 9 skills |
| Manually copy files | 800 | Copy commands, validation |
| Manually adapt docs | 400 | Customize README, CLAUDE.md, pyproject.toml |
| Manually create git structure | 300 | Initialize, create branches, remote |
| **Total** | **3,500** | **Full manual setup** |

**Callable tool approach:**
| Step | Tokens | Description |
|------|--------|-------------|
| Invoke script | 150 | Single subprocess call |
| Script execution | 0 | No Claude Code context needed |
| **Total** | **150** | **Automated setup** |

**Savings: 3,350 tokens (96% reduction)**

**Time savings:**
- Manual: 30-60 minutes
- Automated: 2-5 minutes (mostly Q&A time)
- **Savings: 25-55 minutes per repository**

---















## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
- **[../CLAUDE.md](../CLAUDE.md)** - Parent directory: skills

**Child Directories:**
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived
- **[scripts/CLAUDE.md](scripts/CLAUDE.md)** - Scripts

## Related Skills

**Does NOT integrate with other skills during execution** - this is a meta-skill that creates the environment for other skills.

**After initialization, the target repository has all 9 skills ready to use:**
- workflow-orchestrator - Main coordinator for workflow phases
- tech-stack-adapter - Detects Python/uv project configuration
- git-workflow-manager - Git operations, worktrees, semantic versioning
- bmad-planner - Creates BMAD planning documents (Phase 1)
- speckit-author - Creates detailed specifications (Phase 2)
- quality-enforcer - Enforces quality gates (Phase 3)
- workflow-utilities - Shared utilities for all skills
- agentdb-state-manager - Persistent state tracking (optional)
- initialize-repository - This meta-skill (for future replication)
