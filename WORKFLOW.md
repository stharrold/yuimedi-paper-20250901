# Workflow Guide - Standard Language Learning Repository

**Version:** 5.3.0
**Date:** 2025-11-08
**Architecture:** Skill-based progressive disclosure with BMAD + SpecKit + Claude Code + PR Feedback Work-Items

## Overview

This repository uses a modular skill-based git workflow for Python feature development. The workflow combines:
- **Git-flow + GitHub-flow hybrid** with worktrees for isolation
- **BMAD planning** (requirements + architecture) in main repo
- **SpecKit specifications** (spec + plan) in feature worktrees
- **8 specialized skills** loaded progressively per workflow phase
- **Quality gates** enforced before integration (≥80% coverage, all tests passing)

## Prerequisites

Required tools:
- **gh CLI** - GitHub API access (for username extraction)
- **uv** - Python package manager
- **git** - Version control with worktree support
- **Python 3.11+** - Language runtime
- **podman** (optional) - Container operations

Verify prerequisites:
```bash
gh auth status          # Must be authenticated
uv --version            # Must be installed
python3 --version       # Must be 3.11+
podman --version        # Optional
```

## Architecture

### Skill Structure

```
.claude/skills/
├── workflow-orchestrator/    # Main coordinator (~300 lines)
│   └── templates/
│       ├── TODO_template.md
│       ├── WORKFLOW.md.template
│       └── CLAUDE.md.template
├── tech-stack-adapter/        # Detects Python/uv/Podman (~200 lines)
│   └── scripts/detect_stack.py
├── git-workflow-manager/      # Git operations (~500 lines)
│   └── scripts/
│       ├── create_worktree.py
│       ├── daily_rebase.py
│       └── semantic_version.py
├── bmad-planner/              # Requirements + architecture (~400 lines)
│   └── templates/
│       ├── requirements.md.template
│       └── architecture.md.template
├── speckit-author/            # Specs in worktrees (~400 lines)
│   └── templates/
│       ├── spec.md.template
│       └── plan.md.template
├── quality-enforcer/          # Tests, coverage, versioning (~300 lines)
│   └── scripts/
│       ├── check_coverage.py
│       └── run_quality_gates.py
├── workflow-utilities/        # Shared utilities (~200 lines)
│   └── scripts/
│       ├── deprecate_files.py
│       ├── archive_manager.py
│       ├── todo_updater.py
│       └── directory_structure.py
└── initialize-repository/     # Bootstrap new repos (Phase 0 meta-skill) (~1000 lines)
    └── scripts/
        └── initialize_repository.py
```

**Token Efficiency:**
- Initial load: orchestrator only (~300 tokens)
- Per phase: orchestrator + 1-2 skills (~600-900 tokens)
- Previous monolith: 2,718 tokens all at once

### Branch Structure

```
main                           ← Production (tagged vX.Y.Z)
  ↑
release/vX.Y.Z                ← Release candidate
  ↑
develop                        ← Integration branch
  ↑
contrib/<gh-user>             ← Personal contribution (contrib/stharrold)
  ↑
feature/<timestamp>_<slug>    ← Isolated feature (worktree)
hotfix/vX.Y.Z-hotfix.N        ← Production hotfix (worktree)
```

### Branch Protection Policy

**CRITICAL:** The `main` and `develop` branches are **protected and permanent**.

#### Protected Branch Rules

**Never delete protected branches:**
- `main` - Production branch (tagged releases)
- `develop` - Integration branch (merged features)

**Never commit directly to protected branches:**
- All changes to `main` and `develop` must go through pull requests
- Direct commits violate the review and quality gate process
- Worktrees isolate feature work, preventing accidental commits

**Only merge via pull requests:**
- Feature → contrib (PR reviewed, merged in GitHub UI)
- Contrib → develop (PR reviewed, merged in GitHub UI)
- Release → main (PR reviewed, merged in GitHub UI)
- Hotfix → main (PR reviewed, merged in GitHub UI)

#### No Exceptions - All Merges via PR

**ALL merges** to `main` and `develop` go through pull requests. There are no exceptions.

**backmerge_release.py** follows PR workflow (as of v1.8.0):
- **Purpose:** Back-merge release branches to develop (Phase 5.5)
- **Process:** Rebases release branch onto develop, then creates PR
- **Why rebase first:**
  - Clean, linear git history (no merge commits)
  - PR is up-to-date with target branch (no "branch out-of-date" warnings)
  - Easier code review (only shows actual changes from release)
  - Follows git best practices
- **Location:** `.claude/skills/git-workflow-manager/scripts/backmerge_release.py`
- **No direct commits:** Script creates PR only (merge happens in GitHub/Azure DevOps UI)

#### Technical Enforcement (Recommended)

**GitHub branch protection settings:**
1. Navigate to: Repository Settings → Branches → Branch protection rules
2. Add rule for `main`:
   - ✅ Require pull request before merging
   - ✅ Require status checks to pass (if CI/CD configured)
   - ✅ Require conversation resolution before merging
   - ✅ Do not allow bypassing the above settings
3. Add rule for `develop`:
   - ✅ Require pull request before merging
   - ✅ Require status checks to pass (if CI/CD configured)

See `.github/BRANCH_PROTECTION.md` for detailed setup instructions.

**Pre-push hook (optional safety net):**
```bash
# Install pre-push hook to prevent accidental pushes
cp .git-hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

The hook prevents direct pushes to `main` or `develop` with a helpful error message.

#### What Happens If You Violate Protection?

**If you accidentally commit to main/develop:**

1. **Don't panic** - The commit is local only until pushed
2. **Undo the commit:**
   ```bash
   git reset --soft HEAD~1    # Undo commit, keep changes staged
   ```
3. **Switch to correct branch:**
   ```bash
   git checkout contrib/<gh-user>   # Or appropriate feature branch
   git commit -m "Your message"     # Commit on correct branch
   ```

**If you accidentally pushed to main/develop:**

1. **Don't force push** - This rewrites history
2. **Revert the commit:**
   ```bash
   git revert <commit-sha>    # Creates new commit undoing changes
   git push origin main       # Push revert commit
   ```
3. **Ask for help** if unsure - Better safe than sorry

**If you accidentally deleted a protected branch:**

1. **Recreate from remote:**
   ```bash
   git fetch origin
   git checkout -b main origin/main       # Recreate main
   # or
   git checkout -b develop origin/develop # Recreate develop
   ```
2. **Verify integrity:**
   ```bash
   git log --oneline -10     # Check recent commits
   git status                 # Verify clean state
   ```

### File Locations

**Main Repository:**
```
main-repo/
├── TODO.md                    ← Master workflow manifest (YAML frontmatter)
├── TODO_feature_*.md          ← Individual workflow trackers
├── TODO_release_*.md          ← Release workflow trackers
├── TODO_hotfix_*.md           ← Hotfix workflow trackers
├── requirements.md            ← BMAD: Requirements (Phase 1)
├── architecture.md            ← BMAD: Architecture (Phase 1)
├── WORKFLOW.md                ← This file
├── CLAUDE.md                  ← Claude Code interaction guide
├── README.md                  ← Project documentation
├── .claude/skills/            ← 8 skill modules (including Phase 0 meta-skill)
├── src/                       ← Source code
├── tests/                     ← Test suite
└── ARCHIVED/                  ← Deprecated files and completed workflows
```

**Feature Worktree:**
```
worktree-directory/
├── spec.md                    ← SpecKit: Detailed specification
├── plan.md                    ← SpecKit: Implementation task breakdown
├── src/                       ← Code (same as main repo)
├── tests/                     ← Tests (same as main repo)
└── .git                       ← Worktree git metadata (linked to main)
```

**Critical:** TODO_*.md files live in **main repo**, not in worktrees. Worktrees reference them via `../TODO_*.md`.

## Directory Standards

**Every directory in this project must follow these standards:**

1. **Contains CLAUDE.md with YAML frontmatter**
   - Context-specific guidance for Claude Code when working in this directory
   - YAML frontmatter with metadata and cross-references
   - References to sibling README.md, parent CLAUDE.md, and all children CLAUDE.md

2. **Contains README.md with YAML frontmatter**
   - Human-readable documentation for developers
   - YAML frontmatter with metadata and cross-references
   - References to sibling CLAUDE.md, parent README.md, and all children README.md

3. **Contains ARCHIVED/ subdirectory** (except ARCHIVED directories themselves)
   - For storing deprecated items from that directory
   - ARCHIVED/ also has its own CLAUDE.md and README.md with YAML frontmatter

**YAML Frontmatter Structure:**

**CLAUDE.md frontmatter:**
```yaml
---
type: claude-context
directory: specs/user-auth
purpose: Context-specific guidance for user-auth
parent: ../CLAUDE.md
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
  - feature-subdir/CLAUDE.md
related_skills:
  - workflow-orchestrator
  - workflow-utilities
---
```

**README.md frontmatter:**
```yaml
---
type: directory-documentation
directory: specs/user-auth
title: User Auth
sibling_claude: CLAUDE.md
parent: ../README.md
children:
  - ARCHIVED/README.md
  - feature-subdir/README.md
---
```

**Example directory structure:**
```
specs/feature-auth/
├── CLAUDE.md           ← YAML frontmatter + context guidance
├── README.md           ← YAML frontmatter + documentation
├── ARCHIVED/
│   ├── CLAUDE.md       ← YAML frontmatter + archived context
│   ├── README.md       ← YAML frontmatter + archived docs
│   └── 20251018T120000Z_old-oauth-flow.zip  ← Deprecated files
├── spec.md
└── plan.md
```

**Creating compliant directories:**

Use the workflow-utilities helper script to ensure directories meet standards:

```bash
python .claude/skills/workflow-utilities/scripts/directory_structure.py \
  <directory-path>
```

**Example:**
```bash
python .claude/skills/workflow-utilities/scripts/directory_structure.py \
  specs/user-auth
```

This automatically creates:
- The target directory
- CLAUDE.md with YAML frontmatter, purpose, and cross-references
- README.md with YAML frontmatter and documentation
- ARCHIVED/ subdirectory with its own CLAUDE.md and README.md

**Migrating existing directories:**

To add YAML frontmatter to existing CLAUDE.md and README.md files:

```bash
# Preview changes
python .claude/skills/workflow-utilities/scripts/migrate_directory_frontmatter.py --dry-run

# Apply migration
python .claude/skills/workflow-utilities/scripts/migrate_directory_frontmatter.py
```

## Workflow Phases

### Phase 0: Initial Setup

**Location:** Main repository
**Branch:** `main` or create `contrib/<gh-user>`
**Skills:** tech-stack-adapter, git-workflow-manager, workflow-utilities

**Steps:**

1. **Verify prerequisites:**
   ```bash
   # Check authentication
   gh auth status

   # Extract GitHub username
   GH_USER=$(gh api user --jq '.login')
   echo "GitHub User: $GH_USER"
   ```

2. **Create skill directory structure** (if not exists):
   ```bash
   # Directory structure is already in .claude/skills/
   ls -la .claude/skills/
   ```

3. **Create TODO.md manifest** (if not exists):
   ```bash
   python .claude/skills/workflow-utilities/scripts/todo_updater.py .
   ```

4. **Initialize contrib branch** (if not exists):
   ```bash
   GH_USER=$(gh api user --jq '.login')
   git checkout -b "contrib/$GH_USER"
   git push -u origin "contrib/$GH_USER"
   ```

**User prompt:** "Initialize workflow for this project" or "next step?"

**Output:**
- ✓ Skills verified
- ✓ TODO.md created with YAML frontmatter
- ✓ contrib/<gh-user> branch initialized

---

### Phase 0: Repository Initialization (Optional)

**Location:** External (source repository → target repository)
**Branch:** N/A (creates new repository)
**Skills:** initialize-repository (meta-skill)

**Purpose:** Bootstrap a new repository with the complete workflow system from an existing source repository.

**When to use:**
- Starting a new project that needs the workflow system
- Migrating existing project to workflow system
- Creating template repository with workflow standards

**Note:** This is a **one-time setup phase**, not part of the normal Phases 1-6 workflow cycle.

**Command:**
```bash
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  <source-repo> <target-repo>
```

**Example:**
```bash
# From current repository
python .claude/skills/initialize-repository/scripts/initialize_repository.py \
  . ../my-new-project
```

**Interactive Session Flow:**

**Phase 1: Configuration Selection (9 questions)**
```
What is the primary purpose of this repository?
  1) Web application
  2) CLI tool
  3) Library/package
  4) Data analysis
  5) Machine learning
  6) Other
> [User selects]

Brief description of the repository (one line):
> [User provides]

GitHub username [auto-detected from gh CLI]
> [User confirms or updates]

Python version (3.11 / 3.12 / 3.13) [default: 3.11]
> [User selects]

Copy workflow system? (required, always yes)
Copy domain-specific content (src/, resources/)? (yes/no)
Copy sample tests (tests/)? (yes/no)
Copy container configs? (yes/no)
```

**Phase 2: Git Setup (4-5 questions)**
```
Initialize git repository? (yes/no)
If yes: Create branch structure (main, develop, contrib)? (yes/no)
If yes: Set up remote? (yes/no)
If yes: Remote URL?
If yes and remote: Push to remote? (yes/no)
```

**What gets copied:**

**Always:**
- All 8 skills (.claude/skills/)
- Documentation (WORKFLOW.md, CONTRIBUTING.md, UPDATE_CHECKLIST.md)
- Quality configs (pyproject.toml, .gitignore)
- Directory structure (ARCHIVED/, planning/, specs/)

**Generated/adapted:**
- README.md (customized for new repo)
- CLAUDE.md (customized for new repo)
- CHANGELOG.md (initial v0.1.0)
- TODO.md (master workflow manifest)

**Optionally (based on Q&A):**
- Domain content (src/, resources/)
- Tests (tests/)
- Container configs (Containerfile, podman-compose.yml)

**Output:**
- ✓ New repository created with complete workflow system
- ✓ Documentation adapted for new context
- ✓ Git initialized with 3-branch structure (optional)
- ✓ Remote configured (optional)
- ✓ Ready to start Phase 1 (BMAD planning)

**Token Efficiency:**
- Manual setup: ~3,500 tokens
- Callable tool: ~150 tokens
- **Savings: ~3,350 tokens (96% reduction)**

**Next step after initialization:**
```bash
cd /path/to/new-repo
uv sync
python .claude/skills/bmad-planner/scripts/create_planning.py first-feature <gh-user>
```

---

### Phase 1: Planning (BMAD)

**Location:** Main repository
**Branch:** `contrib/<gh-user>`
**Skills:** bmad-planner (callable tool), workflow-utilities

**Interactive Planning Tool:**

BMAD is now an **interactive callable Python script** that uses a three-persona approach to gather requirements and design architecture.

**Command:**
```bash
python .claude/skills/bmad-planner/scripts/create_planning.py \
  <slug> <gh-user>
```

**Example:**
```bash
python .claude/skills/bmad-planner/scripts/create_planning.py \
  my-feature stharrold
```

**Interactive Session Flow:**

The script conducts three-persona Q&A automatically:

#### Persona 1: 🧠 BMAD Analyst (Requirements)

Script acts as business analyst to create requirements.md:

**Interactive Q&A (5-10 questions):**
```
🧠 BMAD Analyst Persona - Requirements Gathering

What problem does this feature solve?
> [User answers]

Who are the primary users of this feature?
> [User answers]

How will we measure success?
> [User answers]

Functional requirements (FR-001, FR-002, ...):
> [User provides requirements with acceptance criteria]

Performance, security, scalability requirements?
> [User answers]
```

**Generates:** `planning/<feature>/requirements.md` (using comprehensive template)
- Business context, problem statement, success criteria
- Functional requirements (FR-001, FR-002...) with acceptance criteria
- Non-functional requirements (performance, security, scalability)
- User stories with scenarios
- Risks and mitigation

#### Persona 2: 🏗️ BMAD Architect (Architecture)

Script acts as technical architect to create architecture.md:

**Interactive Q&A (5-8 questions):**
```
🏗️ BMAD Architect Persona - Technical Architecture Design

Based on the requirements, I'll design the technical architecture.

Technology Stack:

Web framework (if applicable)?
  1) FastAPI
  2) Flask
  3) Django
  4) None
> [User selects]

Database?
  1) SQLite (dev)
  2) PostgreSQL
  3) MySQL
  4) None
> [User selects]

Container strategy, testing framework, etc.
> [User answers remaining questions]
```

**Generates:** `planning/<feature>/architecture.md` (using comprehensive template)
- System overview, component diagrams
- Technology stack with justifications
- Data models, API endpoints
- Container architecture (Containerfile, podman-compose.yml)
- Security, error handling, testing strategy
- Deployment and observability

#### Persona 3: 📋 BMAD PM (Epic Breakdown)

Script acts as project manager to create epics.md:

**Automatic Analysis (no Q&A):**
```
📋 BMAD PM Persona - Epic Breakdown

Analyzing requirements and architecture to create epic breakdown...

✓ Identified 3 epics:
  - E-001: Data Layer Foundation (Priority: P0, Medium complexity)
  - E-002: Core Business Logic (Priority: P0, High complexity)
  - E-003: Testing & Quality Assurance (Priority: P1, Medium complexity)
```

**Generates:** `planning/<feature>/epics.md` (epic breakdown)
- Epic 1, Epic 2, Epic 3... with scope and complexity
- Dependencies between epics
- Implementation priority order
- Timeline estimates

#### Automatic Commit

Script automatically commits planning documents:

```bash
git add planning/<feature>/
git commit -m "docs(planning): add BMAD planning for <feature>

BMAD planning session completed via interactive tool:
- requirements.md: Business requirements and user stories (🧠 Analyst)
- architecture.md: Technical design and technology stack (🏗️ Architect)
- epics.md: Epic breakdown and priorities (📋 PM)

Generated by: .claude/skills/bmad-planner/scripts/create_planning.py

Refs: planning/<feature>/README.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
"
git push origin contrib/<gh-user>
```

**User prompt:** "next step?" (from contrib branch)

**Workflow Orchestrator Call:**
```python
# In workflow orchestrator - Phase 1.1
if current_phase == 1 and current_step == '1.1':
    import subprocess

    result = subprocess.run([
        'python',
        '.claude/skills/bmad-planner/scripts/create_planning.py',
        slug,       # my-feature
        gh_user,    # stharrold
    ], check=True)

    print(f"✓ BMAD planning created in planning/{slug}/")
    print("  Next: Create feature worktree (Phase 2)")
```

**Output:**
- ✓ planning/<feature>/requirements.md created (🧠 Analyst)
- ✓ planning/<feature>/architecture.md created (🏗️ Architect)
- ✓ planning/<feature>/epics.md created (📋 PM)
- ✓ planning/<feature>/CLAUDE.md, README.md, ARCHIVED/ created
- ✓ Committed to contrib/<gh-user>
- ✓ **Token savings: ~2,300 tokens vs manual approach**

**Next:** Create feature worktree (Phase 2 will use these planning docs as context)

**Reference:** [bmad-planner skill](/.claude/skills/bmad-planner/SKILL.md)

---

### Phase 2: Feature Development

**Location:** Feature worktree
**Branch:** `feature/<timestamp>_<slug>`
**Skills:** git-workflow-manager, speckit-author, quality-enforcer, workflow-utilities

#### Step 2.1: Create Feature Worktree

**Command:**
```bash
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature <slug> contrib/<gh-user>
```

**Example:**
```bash
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature certificate-a1 contrib/stharrold
```

**Output:**
```
✓ Worktree created: /Users/user/Documents/GitHub/standard_feature_certificate-a1
✓ Branch: feature/20251023T104248Z_certificate-a1
✓ TODO file: TODO_feature_20251023T104248Z_certificate-a1.md
```

**Side effects:**
- Creates worktree directory: `<repo>_feature_<slug>/`
- Creates branch: `feature/<timestamp>_<slug>`
- Creates TODO_*.md in **main repo** (not worktree)
- Updates TODO.md manifest with new workflow reference
- Runs `uv sync` in worktree

**User prompt:** "next step?" (after planning)

#### Step 2.2: Switch to Worktree

```bash
cd /Users/user/Documents/GitHub/standard_feature_certificate-a1
```

#### Step 2.3: Create SpecKit Specifications

**Files created in worktree:**
- `spec.md` - Detailed specification (API contracts, data models, behaviors)
- `plan.md` - Implementation task breakdown (impl_001, impl_002, test_001, etc.)

**BMAD Context Integration:**

If planning documents exist in `../planning/<feature>/`:
```
I found BMAD planning documents from Phase 1.

Using as context:
- requirements.md: 15 functional requirements, 5 user stories
- architecture.md: Python/FastAPI stack, PostgreSQL database
- epics.md: 3 epics (data layer, API, tests)

Generating SpecKit specifications that align with BMAD planning...
```

If no planning documents:
```
No BMAD planning found. Creating specifications from scratch.

What is the main purpose of this feature?
```

**SpecKit uses planning context to generate:**
- spec.md sections align with requirements.md functional requirements
- plan.md tasks organized by epics.md epic breakdown
- Technology choices match architecture.md stack

**User prompt:** "next step?" (from worktree)

**Output:**
- ✓ spec.md created (~400-600 lines, informed by BMAD if available)
- ✓ plan.md created (~300-400 lines, organized by epics if available)
- ✓ Committed and pushed to feature branch

#### Step 2.4: Implementation Tasks

**Process:**
1. Parse `plan.md` for next pending task
2. Implement code following spec.md
3. Write tests (target ≥80% coverage)
4. **Check for deprecated files** - If implementation replaces existing files, use [file deprecation](#file-deprecation) process
5. Commit with semantic message
6. Update TODO_*.md task status
7. Repeat for all tasks

**User prompt:** "next step?" (iteratively)

**Commit format:**
```
<type>(<scope>): <subject>

<body>

Implements: impl_003
Spec: spec.md
Tests: tests/test_validator.py
Coverage: 85%

Refs: TODO_feature_20251023T104248Z_certificate-a1.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### Phase 3: Quality Assurance

**Location:** Feature worktree
**Branch:** `feature/<timestamp>_<slug>`
**Skills:** quality-enforcer, workflow-utilities

**Quality Gates (all must pass):**

1. **Test Coverage ≥ 80%:**
   ```bash
   uv run pytest --cov=src --cov-report=term --cov-fail-under=80
   ```

2. **All Tests Passing:**
   ```bash
   uv run pytest
   ```

3. **Linting Clean:**
   ```bash
   uv run ruff check src/ tests/
   ```

4. **Type Checking Clean:**
   ```bash
   uv run mypy src/
   ```

5. **Build Successful:**
   ```bash
   uv build
   ```

6. **Container Healthy** (if applicable):
   ```bash
   podman build -t standard:test .
   podman run --rm standard:test pytest
   ```

**User prompt:** "next step?" (after all implementation)

**Command:**
```bash
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

**Output:**
```
Running Quality Gates...

COVERAGE: ✓ 87% (≥80% required)
TESTS: ✓ 45/45 passing
LINTING: ✓ 0 issues
TYPES: ✓ 0 errors
BUILD: ✓ Success

✓ ALL GATES PASSED

Next: Semantic version calculation
```

---

### Phase 4: Integration & Pull Request

**Location:** Feature worktree → Main repository
**Skills:** git-workflow-manager, workflow-utilities

#### Step 4.1: Calculate Semantic Version

**Command:**
```bash
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v1.0.0
```

**Version bump logic:**
- **MAJOR (v2.0.0):** Breaking changes (API changes, removed features)
- **MINOR (v1.1.0):** New features (new files, new functions, new endpoints)
- **PATCH (v1.0.1):** Bug fixes, refactoring, docs, tests

**Output:**
```
Base version: v1.0.0
Changes detected:
  - New files: src/vocabulary/a1.py
  - New functions: 3

Recommended version: v1.1.0 (MINOR)
```

#### Step 4.1.5: Sync AI Assistant Configuration

**Purpose:** Ensure CLAUDE.md changes are synced to cross-tool compatible formats before creating PR

**When to run:** After quality gates pass, before creating pull request

**Manual sync (Windows/all platforms):**
```bash
# Sync CLAUDE.md to cross-tool formats
cp CLAUDE.md AGENTS.md
mkdir -p .github && cp CLAUDE.md .github/copilot-instructions.md
mkdir -p .agents && cp -r .claude/* .agents/

# Verify sync
ls -la AGENTS.md .github/copilot-instructions.md .agents/
```

**PowerShell alternative:**
```powershell
# Sync CLAUDE.md to cross-tool formats
cp CLAUDE.md AGENTS.md
mkdir -Force .github; cp CLAUDE.md .github/copilot-instructions.md
mkdir -Force .agents; cp -Recurse .claude/* .agents/
```

**Automatic sync (Linux/macOS with jq + rsync installed):**
```bash
# The PostToolUse hook runs automatically when CLAUDE.md is edited
# If hook didn't run, manually execute:
./.claude/hooks/sync-agents.sh
```

**What gets synced:**
- `CLAUDE.md` → `AGENTS.md` (industry standard instruction file)
- `CLAUDE.md` → `.github/copilot-instructions.md` (GitHub Copilot)
- `.claude/` → `.agents/` (tool-agnostic configuration directory)

**Why this matters:**
- Ensures GitHub Copilot users see updated instructions
- Enables Cursor, Aider, and other tools to use same configuration
- Maintains cross-tool compatibility for team members

**Skip if:** You haven't modified CLAUDE.md or .claude/ configuration in this feature

#### Step 4.2: Create Pull Request (feature → contrib)

**Command:**
```bash
gh pr create \
  --base "contrib/stharrold" \
  --head "feature/20251023T104248Z_certificate-a1" \
  --title "feat(vocab): add A1 certificate vocabulary" \
  --body "$(cat <<'EOF'
## Summary
- Implements A1 level Standard vocabulary module
- 150+ words with gender, plural, and examples
- Full test coverage (87%)

## Changes
- New module: src/vocabulary/a1.py
- Tests: tests/test_a1_vocabulary.py
- Spec: spec.md in worktree

## Quality Gates
- Coverage: 87% (✓ ≥80%)
- Tests: 45/45 passing (✓)
- Linting: Clean (✓)
- Types: Clean (✓)
- Build: Success (✓)

## Semantic Version
Recommended: v1.1.0 (MINOR - new feature)

## References
- TODO: TODO_feature_20251023T104248Z_certificate-a1.md
- Spec: See worktree spec.md
- Plan: See worktree plan.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Output:**
```
✓ Pull request created: https://github.com/user/standard/pull/42
```

#### Step 4.3: Reviewers Add Comments

**Action:** Reviewers add comments and conversations in GitHub/Azure DevOps web portal

**What happens:**
- Reviewers add inline comments on specific files/lines
- Reviewers create conversation threads
- Some conversations require substantive changes (new features, refactoring)
- Some conversations are simple fixes (typos, formatting)

#### Step 4.4: Handle PR Feedback via Work-Items (Optional)

**When to use:**
- PR has unresolved conversations requiring substantive changes
- Changes are too large to fix on same feature branch
- Want to approve PR while tracking feedback separately

**Decision tree:**
```
PR reviewed with comments
├─ Simple fixes (typos, formatting, minor adjustments)
│  └─ Fix directly on feature branch, push update, skip to Step 4.5
└─ Substantive changes (new features, refactoring, architecture changes)
   └─ Generate work-items, continue below
```

**Command:**
```bash
python .claude/skills/git-workflow-manager/scripts/generate_work_items_from_pr.py 42
```

**Output:**
```
ℹ Analyzing PR #42 for unresolved conversations...
✓ Found 3 unresolved conversations
✓ Created work-item: pr-42-issue-1 (https://github.com/user/standard/issues/123)
  Title: "PR #42 feedback: Add error handling for missing vocabulary files"
  Labels: pr-feedback, pr-42
✓ Created work-item: pr-42-issue-2 (https://github.com/user/standard/issues/124)
  Title: "PR #42 feedback: Refactor gender validation to use enum"
  Labels: pr-feedback, pr-42
✓ Created work-item: pr-42-issue-3 (https://github.com/user/standard/issues/125)
  Title: "PR #42 feedback: Add examples to vocabulary word model"
  Labels: pr-feedback, pr-42

ℹ Work-items created. For each work-item:
  1. Create feature worktree: create_worktree.py feature pr-42-issue-1 contrib/stharrold
  2. Implement fix (SpecKit optional for simple fixes)
  3. Run quality gates
  4. Create PR: feature/YYYYMMDDTHHMMSSZ_pr-42-issue-1 → contrib/stharrold
  5. Merge in web portal
  6. Repeat for remaining work-items
```

**What it does:**
- Detects VCS provider (GitHub or Azure DevOps)
- Fetches unresolved PR conversations:
  - GitHub: `reviewThreads.isResolved == false`
  - Azure DevOps: `threads.status == active|pending`
- Creates work-items (GitHub issues or Azure DevOps tasks)
- Work-item slug pattern: `pr-{pr_number}-issue-{sequence}`
- Preserves conversation context (file, line, author, timestamps)

**Benefits:**
- Enables PR approval without blocking on follow-up work
- Creates traceable lineage: PR → work-items → feature branches → new PRs
- Compatible with all issue trackers (GitHub, Azure DevOps, others)
- Each work-item follows standard Phase 2-4 workflow

**For each work-item, repeat workflow:**
1. Create feature worktree: `create_worktree.py feature pr-42-issue-1 contrib/stharrold`
2. Implement fix (SpecKit optional for simple fixes)
3. Run quality gates (Phase 3)
4. Create PR: `feature/YYYYMMDDTHHMMSSZ_pr-42-issue-1 → contrib/stharrold`
5. Merge in web portal
6. Repeat until all work-items resolved

#### Step 4.5: User Approves and Merges PR

**Action:** User approves and merges PR in GitHub/Azure DevOps web portal

**Note:** Conversations may remain unresolved if work-items were generated (Step 4.4). This is expected - work-items track the follow-up work.

#### Step 4.6: Atomic Cleanup (Archive TODO + Delete Worktree + Delete Branches)

**⚠️ IMPORTANT:** Use the atomic cleanup script to ensure proper ordering. This script prevents orphaned TODO files by enforcing: Archive TODO → Delete worktree → Delete branches.

**Return to main repo:**
```bash
cd /Users/user/Documents/GitHub/standard
```

**Atomic cleanup (recommended):**
```bash
python .claude/skills/git-workflow-manager/scripts/cleanup_feature.py \
  certificate-a1 \
  --summary "Implemented A1 Standard certificate guide with complete exam structure" \
  --version "1.3.0"
```

**Output:**
```
🚀 Cleaning up feature: certificate-a1
======================================================================
✓ Found TODO: TODO_feature_20251023T104248Z_certificate-a1.md
✓ Found worktree: /Users/user/Documents/GitHub/standard_feature_certificate-a1
✓ Found branch: feature/20251023T104248Z_certificate-a1

======================================================================
Starting atomic cleanup operations...
======================================================================

📦 Archiving TODO: TODO_feature_20251023T104248Z_certificate-a1.md
✓ TODO archived to ARCHIVED/TODO_feature_20251023T104248Z_certificate-a1.md

🗑️  Removing worktree: /Users/user/Documents/GitHub/standard_feature_certificate-a1
✓ Worktree removed: /Users/user/Documents/GitHub/standard_feature_certificate-a1

🗑️  Deleting local branch: feature/20251023T104248Z_certificate-a1
✓ Local branch deleted: feature/20251023T104248Z_certificate-a1

🗑️  Deleting remote branch: origin/feature/20251023T104248Z_certificate-a1
✓ Remote branch deleted: origin/feature/20251023T104248Z_certificate-a1

======================================================================
✅ Feature cleanup complete: certificate-a1
======================================================================
```

**Why atomic cleanup?**
- **Prevents orphaned TODO files**: Cannot delete worktree without archiving TODO first
- **Single command**: One command instead of remembering 4 separate commands
- **Atomic operation**: Either everything succeeds or nothing changes (safe to retry)
- **Clear ordering**: Archives TODO → Deletes worktree → Deletes branches (guaranteed)
- **Error handling**: If TODO archive fails, worktree/branches NOT deleted (safe state)

**Manual cleanup (not recommended):**

If you need manual control, use these commands IN THIS ORDER:

1. Archive TODO (MUST be first):
```bash
python .claude/skills/workflow-utilities/scripts/workflow_archiver.py \
  TODO_feature_20251023T104248Z_certificate-a1.md \
  --summary "..." \
  --version "1.3.0"
```

2. Delete worktree (only after archive succeeds):
```bash
git worktree remove ../standard_feature_certificate-a1
```

3. Delete branches (only after worktree deletion):
```bash
git branch -D feature/20251023T104248Z_certificate-a1
git push origin --delete feature/20251023T104248Z_certificate-a1
```

**⚠️ WARNING:** Manual cleanup is error-prone. If you delete the worktree before archiving the TODO, you'll have an orphaned TODO file in the main repo. Use the atomic cleanup script to avoid this.

#### Step 4.7: Rebase contrib onto develop

**Command:**
```bash
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  contrib/stharrold
```

**Steps:**
1. Checkout contrib branch
2. Fetch origin
3. Rebase onto origin/develop
4. Force push with lease

#### Step 4.8: Create Pull Request (contrib → develop)

**Command:**
```bash
gh pr create \
  --base "develop" \
  --head "contrib/stharrold" \
  --title "feat(vocab): A1 certificate vocabulary module" \
  --body "Completed feature: A1 vocabulary with full test coverage"
```

**User merges in GitHub UI (develop branch)**

---

### Phase 5: Release Workflow

**Location:** Main repository
**Branch Flow:** `develop` → `release/vX.Y.Z` → `main` (with tag) → back to `develop`
**Skills:** git-workflow-manager, quality-enforcer, workflow-utilities

#### Overview

The release workflow creates a production release from the develop branch, tags it on main, and back-merges to develop. This follows git-flow release branch pattern.

#### Step 5.1: Create Release Branch

**Prerequisites:**
- All features merged to develop
- Quality gates passing on develop
- Version number determined

**Command:**
```bash
python .claude/skills/git-workflow-manager/scripts/create_release.py \
  v1.1.0 develop
```

**Steps:**
1. Verify develop branch is clean and up-to-date
2. Calculate/confirm semantic version from develop
3. Create `release/v1.1.0` branch from develop
4. Create release TODO file
5. Update version files (if applicable)

**Output:**
```
✓ Created release branch: release/v1.1.0
✓ Base: develop (commit abc123)
✓ TODO file: TODO_release_20251023T143000Z_v1-1-0.md
✓ Ready for final QA and documentation updates
```

#### Step 5.2: Release Quality Assurance

**In release branch:**

1. **Final quality gates:**
   ```bash
   python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
   ```

2. **Update release documentation:**
   - Update CHANGELOG.md
   - Update version in pyproject.toml (if not already done)
   - Update README.md if needed
   - Final review of documentation

3. **Commit release prep:**
   ```bash
   git add .
   git commit -m "chore(release): prepare v1.1.0 release

   - Update CHANGELOG.md with v1.1.0 changes
   - Update version in pyproject.toml
   - Final documentation review

   Refs: TODO_release_20251023T143000Z_v1-1-0.md
   "
   git push origin release/v1.1.0
   ```

#### Step 5.3: Create Pull Request (release → main)

**Command:**
```bash
gh pr create \
  --base "main" \
  --head "release/v1.1.0" \
  --title "release: v1.1.0" \
  --body "$(cat <<'EOF'
## Release v1.1.0

### Summary
Production release with new features and improvements from develop branch.

### Changes Since v1.0.0
- Feature: A1 certificate vocabulary module
- Feature: A2 certificate vocabulary module
- Enhancement: Improved vocabulary search
- Fix: Grammar validation edge cases

### Quality Gates
- Coverage: 87% (✓ ≥80%)
- Tests: 156/156 passing (✓)
- Linting: Clean (✓)
- Types: Clean (✓)
- Build: Success (✓)

### Merge Instructions
1. Review changes
2. Merge to main
3. Tag will be created automatically (v1.1.0)
4. Release notes will be generated
5. Back-merge to develop will follow

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Output:**
```
✓ Pull request created: https://github.com/user/standard/pull/45
```

#### Step 5.4: User Merges Release to Main

**Action:** User reviews and merges PR in GitHub UI (main branch)

**Result:** Release code now on main branch

#### Step 5.5: Tag Release

**Command:**
```bash
python .claude/skills/git-workflow-manager/scripts/tag_release.py \
  v1.1.0 main
```

**Steps:**
1. Checkout main branch
2. Pull latest (includes merge commit)
3. Create annotated tag v1.1.0
4. Push tag to origin
5. Trigger GitHub release creation (if configured)

**Output:**
```
✓ Checked out main branch
✓ Pulled latest changes (commit def456)
✓ Created annotated tag: v1.1.0
   Message: "Release v1.1.0: Production release with vocabulary modules"
✓ Pushed tag to origin
✓ View release: https://github.com/user/standard/releases/tag/v1.1.0
```

#### Step 5.6: Back-merge Release to Develop

**Purpose:** Merge any release-specific changes back to develop through PR

**Command:**
```bash
python .claude/skills/git-workflow-manager/scripts/backmerge_release.py \
  v1.1.0 develop
```

**Important:** This script ALWAYS creates a PR (never pushes directly to develop), ensuring proper review workflow and branch protection compliance.

**Steps:**
1. Checkout develop branch
2. Pull latest from origin
3. Attempt merge locally to check for conflicts
4. Abort local merge (will merge via PR)
5. Create PR: release/v1.1.0 → develop

**Output (no conflicts):**
```
✓ No merge conflicts detected
✓ Created PR: https://github.com/user/standard/pull/46
  Title: "chore(release): back-merge v1.1.0 to develop"

📋 Next steps:
  1. Review PR in GitHub/Azure DevOps portal
  2. Approve through portal
  3. Merge through portal
  4. Run cleanup: python .claude/skills/git-workflow-manager/scripts/cleanup_release.py v1.1.0
```

**Output (with conflicts):**
```
⚠️  Merge conflicts detected in 2 file(s)
✓ Created PR: https://github.com/user/standard/pull/46
  Title: "chore(release): back-merge v1.1.0 to develop"

Conflicting files:
  - pyproject.toml
  - uv.lock

📋 Next steps:
  1. Review PR in GitHub/Azure DevOps portal
  2. Resolve conflicts (see PR description for commands)
  3. Approve and merge through portal
  4. Run cleanup: python .claude/skills/git-workflow-manager/scripts/cleanup_release.py v1.1.0
```

**User Action Required:**
1. **Review PR in GitHub/Azure DevOps UI**
2. **Approve** (required by branch protection)
3. **Merge** through portal merge button
4. **Continue to Step 5.7** after merge completes

#### Step 5.7: Cleanup Release Branch

**After back-merge is complete:**

**Command:**
```bash
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py \
  v1.1.0
```

**Steps:**
1. Verify tag v1.1.0 exists
2. Verify back-merge to develop is complete
3. Delete local release/v1.1.0 branch
4. Delete remote release/v1.1.0 branch
5. Archive release TODO file

**Output:**
```
✓ Verified tag v1.1.0 exists
✓ Verified back-merge to develop complete
✓ Deleted local branch: release/v1.1.0
✓ Deleted remote branch: origin/release/v1.1.0
✓ Archived: TODO_release_20251023T143000Z_v1-1-0.md
✓ Release workflow complete for v1.1.0
```

#### Step 5.8: Update Contrib Branch

**After release is complete, rebase contrib:**

**Command:**
```bash
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  contrib/stharrold
```

This ensures contrib branch is up-to-date with latest develop (which now includes the release back-merge).

---

### Phase 6: Hotfix Workflow (Production Fixes)

**Location:** Hotfix worktree
**Branch Flow:** `main` → `hotfix/vX.Y.Z-hotfix.N` → `main` (with tag) → back to `develop`
**Skills:** git-workflow-manager, speckit-author (optional), quality-enforcer, workflow-utilities

#### Overview

The hotfix workflow creates urgent fixes for production issues. Hotfixes branch from `main`, are fixed in isolation, and merge back to both `main` and `develop`.

**When to use hotfixes:**
- Critical production bugs
- Security vulnerabilities
- Data corruption issues
- Performance emergencies

**Key difference from features:**
- Branch from `main` (not contrib)
- Merge directly to `main` (not via contrib/develop)
- Back-merge to `develop` to keep it in sync
- SpecKit is **optional** (use for complex fixes only)

#### Step 6.1: Create Hotfix Worktree

**Prerequisites:**
- Production issue identified
- Issue severity warrants hotfix (not regular feature fix)
- Version number determined (vX.Y.Z-hotfix.N)

**Command:**
```bash
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  hotfix v1.3.0-hotfix.1 main
```

**Example:**
```bash
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  hotfix critical-auth-bypass main
```

**Output:**
```
✓ Worktree created: /Users/user/Documents/GitHub/standard_hotfix_critical-auth-bypass
✓ Branch: hotfix/20251024T093000Z_critical-auth-bypass
✓ TODO file: TODO_hotfix_20251024T093000Z_critical-auth-bypass.md
```

**Side effects:**
- Creates hotfix worktree directory
- Branches from `main` (not contrib)
- Creates TODO_hotfix_*.md in main repo
- Updates TODO.md manifest

#### Step 6.2: Switch to Hotfix Worktree

```bash
cd /Users/user/Documents/GitHub/standard_hotfix_critical-auth-bypass
```

#### Step 6.3: Create SpecKit Specifications (Optional)

**When to use SpecKit for hotfixes:**

✓ **Use SpecKit if:**
- Complex fix requiring multiple files
- Fix benefits from planning/task breakdown
- Need to document approach for team review
- Fix involves architectural changes

✗ **Skip SpecKit if:**
- Simple one-line fix
- Obvious solution (typo, config error)
- Time-critical emergency (fix immediately)
- Fix already well-understood

**Command (if using SpecKit):**
```bash
python .claude/skills/speckit-author/scripts/create_specifications.py \
  hotfix critical-auth-bypass stharrold \
  --todo-file ../TODO_hotfix_20251024T093000Z_critical-auth-bypass.md
```

**Interactive session:**
```
======================================================================
SpecKit Interactive Specification Tool
======================================================================

⚠ No BMAD planning found for 'critical-auth-bypass'
I'll gather requirements through comprehensive Q&A.

What is the main purpose of this hotfix?
> Fix authentication bypass vulnerability in OAuth flow

Who are the primary users affected?
> All users with OAuth authentication

How will success be measured?
> Vulnerability patched, no auth bypass possible, all tests passing

[... continues with tech stack and testing questions ...]
```

**Output:**
- specs/critical-auth-bypass/spec.md (detailed fix approach)
- specs/critical-auth-bypass/plan.md (task breakdown)
- TODO_hotfix_*.md updated with tasks

**Note:** Most hotfixes skip SpecKit and proceed directly to implementation.

#### Step 6.4: Implement Fix

**Process:**
1. Identify root cause
2. Implement minimal fix (avoid scope creep)
3. Add/update tests to prevent regression
4. Document fix in commit message

**Best practices:**
- **Keep it minimal** - Fix only the immediate issue
- **Add regression tests** - Prevent issue from recurring
- **Document thoroughly** - Explain what broke and how fixed
- **Avoid refactoring** - Save non-critical improvements for features

**Commit format:**
```
fix(hotfix): <brief description of fix>

<detailed explanation of issue and fix>

Root cause: <what caused the bug>
Fix: <what was changed>
Impact: <who is affected>
Regression test: <test file added/updated>

Refs: TODO_hotfix_20251024T093000Z_critical-auth-bypass.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

#### Step 6.5: Quality Assurance

**Run all quality gates:**
```bash
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

**Quality gates (all must pass):**
1. **Test Coverage ≥ 80%**
   ```bash
   uv run pytest --cov=src --cov-report=term --cov-fail-under=80
   ```

2. **All Tests Passing** (including new regression tests)
   ```bash
   uv run pytest
   ```

3. **Linting Clean**
   ```bash
   uv run ruff check src/ tests/
   ```

4. **Type Checking Clean**
   ```bash
   uv run mypy src/
   ```

5. **Build Successful**
   ```bash
   uv build
   ```

**Output:**
```
Running Quality Gates...

COVERAGE: ✓ 82% (≥80% required)
TESTS: ✓ 47/47 passing (includes new regression test)
LINTING: ✓ 0 issues
TYPES: ✓ 0 errors
BUILD: ✓ Success

✓ ALL GATES PASSED

Next: Calculate hotfix version
```

#### Step 6.6: Calculate Hotfix Version

**Command:**
```bash
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  main v1.3.0
```

**Version format:** `vX.Y.Z-hotfix.N`
- Use current main version as base
- Increment hotfix number (N)
- Example: v1.3.0 → v1.3.0-hotfix.1

**Output:**
```
Base version: v1.3.0 (from main)
Hotfix number: 1

Recommended version: v1.3.0-hotfix.1 (HOTFIX)
```

#### Step 6.7: Create Pull Request (hotfix → main)

**Command:**
```bash
gh pr create \
  --base "main" \
  --head "hotfix/20251024T093000Z_critical-auth-bypass" \
  --title "hotfix(auth): fix critical authentication bypass vulnerability" \
  --body "$(cat <<'EOF'
## Hotfix: Critical Authentication Bypass

### Summary
- Fixes critical vulnerability in OAuth authentication flow
- Vulnerability allowed bypassing authentication via token manipulation
- Impact: All users with OAuth authentication

### Root Cause
Token validation was not checking signature properly, allowing
forged tokens to pass authentication.

### Fix
- Added proper JWT signature verification
- Enhanced token validation with expiry checks
- Added rate limiting to token endpoint

### Testing
- New regression test: tests/test_auth_bypass.py
- All existing tests passing
- Manual security testing completed

### Quality Gates
- Coverage: 82% (✓ ≥80%)
- Tests: 47/47 passing (✓ includes regression test)
- Linting: Clean (✓)
- Types: Clean (✓)
- Build: Success (✓)

### Hotfix Version
Recommended: v1.3.0-hotfix.1

### Security Advisory
This hotfix addresses CVE-XXXX-XXXXX (if applicable)

### Merge Instructions
1. Review security fix
2. Verify regression test coverage
3. Merge to main
4. Tag as v1.3.0-hotfix.1
5. Back-merge to develop

## References
- TODO: TODO_hotfix_20251024T093000Z_critical-auth-bypass.md
- Spec: specs/critical-auth-bypass/spec.md (if applicable)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Output:**
```
✓ Pull request created: https://github.com/user/standard/pull/48
```

#### Step 6.8: User Merges Hotfix to Main

**Action:** User reviews and merges PR in GitHub UI (main branch)

**Result:** Hotfix code now on main branch

#### Step 6.9: Tag Hotfix Release

**Command:**
```bash
python .claude/skills/git-workflow-manager/scripts/tag_release.py \
  v1.3.0-hotfix.1 main
```

**Steps:**
1. Checkout main branch
2. Pull latest (includes hotfix merge commit)
3. Create annotated tag v1.3.0-hotfix.1
4. Push tag to origin
5. Trigger GitHub release creation

**Output:**
```
✓ Checked out main branch
✓ Pulled latest changes (includes hotfix commit def789)
✓ Created annotated tag: v1.3.0-hotfix.1
   Message: "Hotfix v1.3.0-hotfix.1: Fix critical auth bypass vulnerability"
✓ Pushed tag to origin
✓ View release: https://github.com/user/standard/releases/tag/v1.3.0-hotfix.1
```

#### Step 6.10: Back-merge Hotfix to Develop

**Purpose:** Keep develop branch in sync with production hotfix

**Command:**
```bash
python .claude/skills/git-workflow-manager/scripts/backmerge_release.py \
  v1.3.0-hotfix.1 develop
```

**Steps:**
1. Checkout develop branch
2. Pull latest from origin
3. Merge hotfix/vX.Y.Z-hotfix.N into develop
4. Resolve conflicts (if any)
5. Push to origin

**Output (no conflicts):**
```
✓ Checked out develop
✓ Pulled latest changes
✓ Merged hotfix/20251024T093000Z_critical-auth-bypass into develop
✓ Pushed to origin/develop
✓ Back-merge complete
```

**Output (with conflicts):**
```
⚠ Merge conflicts detected
✓ Created PR: https://github.com/user/standard/pull/49
  Title: "chore(hotfix): back-merge v1.3.0-hotfix.1 to develop"

Please resolve conflicts in GitHub UI and merge.
```

#### Step 6.11: Cleanup Hotfix Worktree

**Return to main repo:**
```bash
cd /Users/user/Documents/GitHub/standard
```

**Delete hotfix worktree:**
```bash
git worktree remove ../standard_hotfix_critical-auth-bypass
git branch -D hotfix/20251024T093000Z_critical-auth-bypass
```

**Archive TODO file:**
```bash
python .claude/skills/workflow-utilities/scripts/archive_manager.py \
  archive TODO_hotfix_20251024T093000Z_critical-auth-bypass.md
```

**Output:**
```
✓ Removed worktree: ../standard_hotfix_critical-auth-bypass
✓ Deleted branch: hotfix/20251024T093000Z_critical-auth-bypass
✓ Archived TODO_hotfix_20251024T093000Z_critical-auth-bypass.md
✓ Updated TODO.md manifest
```

#### Step 6.12: Update Contrib Branch

**Rebase contrib to include hotfix:**
```bash
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  contrib/stharrold
```

This ensures contrib branch is up-to-date with hotfix (via develop back-merge).

---

## Hotfix vs Feature Comparison

| Aspect | Feature Workflow | Hotfix Workflow |
|--------|-----------------|-----------------|
| **Branches from** | contrib/<user> | main |
| **Merges to** | contrib → develop | main (then back to develop) |
| **SpecKit** | Standard (Phase 2.3) | Optional (use for complex fixes) |
| **BMAD Planning** | Recommended (Phase 1) | Not applicable |
| **Scope** | New functionality | Minimal fix only |
| **Quality gates** | Required (≥80% coverage) | Required (≥80% coverage) |
| **Versioning** | MAJOR/MINOR/PATCH | vX.Y.Z-hotfix.N |
| **Timeline** | Days to weeks | Hours to days (urgent) |
| **Worktree** | Yes (isolation) | Yes (isolation) |

---

## Production Safety & Rollback

### Overview

Production deployments should always use **tagged releases** (e.g., `v1.5.1`), never branch heads. Tags provide immutable snapshots that enable instant rollback without code changes.

### Deployment Best Practices

**✓ DO:**
- Deploy from tags: `git checkout v1.5.1`
- Test releases thoroughly before tagging on main
- Keep multiple recent tags available for rollback
- Monitor production after deployment
- Have rollback procedure documented and rehearsed

**✗ DON'T:**
- Deploy from `main` branch head (moving target)
- Deploy from feature/hotfix branches directly
- Delete tags after deployment (keep for rollback)
- Skip quality gates before releasing

### Emergency Rollback Procedures

#### Scenario 1: Production Broken After Release

**Symptoms:**
- v1.5.1 deployed to production
- Critical issue discovered (crashes, data loss, security vulnerability)
- Need immediate rollback

**Solution: Deploy Previous Tag (Fastest - 2 minutes)**

```bash
# 1. Checkout last known good tag
git checkout v1.5.0

# 2. Deploy this tag to production
# (deployment mechanism varies: docker, kubernetes, etc.)

# Result: Production now running v1.5.0
# - No code changes needed
# - Instant rollback
# - v1.5.1 remains tagged on main (untouched)
```

**Timeline:**
- 0:00 - Issue detected in production (v1.5.1)
- 0:02 - Checkout v1.5.0 tag
- 0:05 - Deploy v1.5.0 to production
- 0:10 - Verify production stable on v1.5.0
- **Total: ~10 minutes to restore service**

---

#### Scenario 2: Need to Remove Bad Release from Main

**Symptoms:**
- v1.5.1 deployed and rolled back to v1.5.0
- v1.5.1 merge commit still on main branch
- Need to remove bad code from main branch

**Solution: Revert Merge Commit**

```bash
# 1. Find the merge commit that introduced v1.5.1
git log --oneline main | head -10
# Example output:
#   abc123f Merge pull request #42 from user/release/v1.5.1
#   def456g docs(release): update CHANGELOG.md for v1.5.1
#   ...

# 2. Revert the merge commit

# ⚠️ WARNING: Before proceeding, review the current state of main!
# If main has moved forward significantly since the problematic release,
# ensure you are reverting the correct commit and not affecting newer changes.
# Use the following to inspect recent history:
git log --oneline main | head -20
# Confirm the merge commit hash and its position in history.

git checkout main
git pull origin main
git revert abc123f -m 1

# Explanation:
# -m 1 = keep parent 1 (main branch history)
# This creates a NEW commit that undoes the merge

# 3. Push revert commit
git push origin main

# 4. Tag the revert as new patch version
git tag -a v1.5.2 -m "Revert broken v1.5.1 release"
git push origin v1.5.2

# 5. Deploy v1.5.2 to production
git checkout v1.5.2
# Deploy...

# Result:
# - main branch now has revert commit
# - v1.5.2 tag points to reverted state
# - v1.5.1 tag still exists (for reference)
# - Production running v1.5.2 (functionally = v1.5.0)
```

**Timeline:**
- Already rolled back to v1.5.0 (production stable)
- Create revert commit: ~10 minutes
- Tag and deploy v1.5.2: ~10 minutes
- **Total: ~20 minutes (non-urgent, production already stable)**

---

#### Scenario 3: Hotfix Taking Too Long

**Symptoms:**
- Production broken, rolled back to v1.5.0
- Working on hotfix in worktree (v1.5.0-hotfix.1)
- Hotfix more complex than expected (hours, not minutes)
- Production still running v1.5.0 (stable but missing features from v1.5.1)

**Solution: Keep Production on v1.5.0, Finish Hotfix Properly**

```bash
# Production remains on v1.5.0 (stable)
# Continue hotfix work:

# 1. In hotfix worktree
cd ../standard_hotfix_issue-name

# 2. Complete the fix
# - Add tests
# - Run quality gates
# - Ensure ≥80% coverage

# 3. Create PR: hotfix → main
gh pr create --base main --title "hotfix(issue): description"

# 4. After merge, tag hotfix
git checkout main
git pull origin main
git tag -a v1.5.0-hotfix.1 -m "Hotfix: description"
git push origin v1.5.0-hotfix.1

# 5. Deploy hotfix
git checkout v1.5.0-hotfix.1
# Deploy...

# 6. Back-merge to develop
python .claude/skills/git-workflow-manager/scripts/backmerge_release.py \
  v1.5.0-hotfix.1 develop

# Result:
# - Production moved from v1.5.0 → v1.5.0-hotfix.1
# - Hotfix tested and properly merged
# - develop updated with fix
```

**Key principle:** Don't rush hotfixes. Production is stable on v1.5.0. Take time to do hotfix correctly.

---

### Why Tag-Based Deployment?

**Problem with branch-based deployment:**
```bash
# Deploy from main branch (BAD)
git checkout main
git pull origin main    # Gets latest commits
# Deploy...

# Issue: "latest" changes constantly
# - Can't reproduce exact deployment
# - Can't rollback without code changes
# - Unclear what version is running
```

**Solution with tag-based deployment:**
```bash
# Deploy from tag (GOOD)
git checkout v1.5.1    # Exact snapshot
# Deploy...

# Benefits:
# - v1.5.1 never changes (immutable)
# - Can reproduce deployment anytime
# - Rollback = checkout v1.5.0
# - Clear version in production
```

---

### Main Branch Protection

**How main stays safe during hotfix work:**

1. **Hotfix work isolated in worktree**
   ```bash
   # Main repo
   /Users/user/Documents/GitHub/standard (main branch untouched)

   # Hotfix worktree
   /Users/user/Documents/GitHub/standard_hotfix_issue (isolated work)
   ```

2. **Main only updated via merged PRs**
   - No direct commits to main
   - All changes reviewed
   - Quality gates enforced

3. **Tagged releases are immutable**
   - v1.5.0 tag never changes
   - Can always rollback to v1.5.0
   - Even if main branch has bad commits

---

### Rollback Decision Tree

```
Production broken after v1.5.1 deployment?
│
├─ YES → Checkout v1.5.0 and deploy (instant rollback)
│        │
│        ├─ Production now stable?
│        │  │
│        │  ├─ YES → Decide next action:
│        │  │        ├─ Remove v1.5.1 from main? → Revert merge commit, tag v1.5.2
│        │  │        ├─ Fix issue? → Create hotfix (v1.5.0-hotfix.1 or v1.5.1-hotfix.1)
│        │  │        └─ Wait for next release? → Keep v1.5.0, work on v1.6.0
│        │  │
│        │  └─ NO → Escalate (v1.5.0 also broken, checkout v1.4.0)
│        │
│        └─ Hotfix taking too long?
│           └─ Keep v1.5.0 in production (stable), complete hotfix properly
│
└─ NO → Continue with normal operations
```

---

### Summary

**Production Safety:**
- ✓ Deploy from tags (v1.5.1), never branches
- ✓ Keep multiple tags for instant rollback
- ✓ Hotfix work isolated (main untouched)
- ✓ Quality gates before tagging
- ✓ Can always rollback without code changes

**Emergency Rollback:**
- **Fastest:** `git checkout v1.5.0` → deploy (2 minutes)
- **Clean main:** Revert merge commit → tag v1.5.2 (20 minutes)
- **Proper fix:** Create hotfix from last good tag (hours)

**Key Principle:** Production stability > speed. Rollback first, fix properly second.

---

## TODO.md Manifest System

### Structure (v5.2.0)

**File:** `TODO.md` (root of main repository)

**Format:**
```markdown
---
manifest_version: 5.2.0
last_updated: 2025-10-23T14:30:22Z
repository: standard
active_workflows:
  count: 2
  updated: 2025-10-23T14:30:22Z
archived_workflows:
  count: 45
  last_archived: 2025-10-22T09:15:00Z
---

# Workflow Manifest

## Active Workflows

### TODO_feature_20251023T104248Z_certificate-a1.md
Implements A1 level Standard vocabulary with grammatical gender and plural forms.

### TODO_feature_20251023T104355Z_certificate-a2.md
Extends A1 vocabulary with A2 level words and advanced grammar patterns.

## Recently Archived Workflows (Last 10)

### ARCHIVED_TODO_feature_20251022T103000Z_initial-foundation.md
Created foundational Standard vocabulary library structure and CI/CD pipeline.

[... 9 more archived workflows ...]

## Workflow Commands

- **Create feature**: `next step?` (from contrib branch)
- **Continue workflow**: `next step?` (from any context)
- **Check quality gates**: Tests, coverage, linting, type checking
- **Create PR**: Automatic after all gates pass
- **View status**: Check current phase in active TODO_*.md files

## Archive Management

Workflows are archived when:
- Feature/hotfix PR merged to contrib branch
- Release PR merged to develop branch
- Contributor manually archives with `archive workflow` command

Archive process:
1. Move TODO_*.md → ARCHIVED_TODO_*.md
2. Update timestamp in filename
3. Create zip of all related files (spec.md, plan.md, logs)
4. Update TODO.md manifest references
5. Commit archive changes to main repo
```

### Update Manifest

**Command:**
```bash
python .claude/skills/workflow-utilities/scripts/todo_updater.py .
```

**Auto-updates when:**
- New worktree created
- Workflow archived
- Manual invocation

---

## Individual TODO_*.md Structure

**File:** `TODO_feature_<timestamp>_<slug>.md` (main repository)

**Format:**
```markdown
---
type: workflow-manifest
workflow_type: feature
slug: certificate-a1
timestamp: 20251023T104248Z
github_user: stharrold

workflow_progress:
  phase: 2
  current_step: "2.4"
  last_task: impl_003

quality_gates:
  test_coverage: 87
  tests_passing: true
  build_passing: true
  linting_clean: true
  types_clean: true
  semantic_version: "1.1.0"

metadata:
  worktree_path: /Users/stharrold/Documents/GitHub/standard_feature_certificate-a1
  branch_name: feature/20251023T104248Z_certificate-a1
  created: 2025-10-23T10:42:48Z
  last_updated: 2025-10-23T14:30:22Z

tasks:
  implementation:
    - id: impl_001
      description: "Create A1 vocabulary data structure"
      status: complete
      completed_at: "2025-10-23T11:00:00Z"
    - id: impl_002
      description: "Add grammatical gender metadata"
      status: complete
      completed_at: "2025-10-23T12:00:00Z"
    - id: impl_003
      description: "Implement vocabulary lookup functions"
      status: in_progress
      started_at: "2025-10-23T13:00:00Z"
  testing:
    - id: test_001
      description: "Unit tests for vocabulary module"
      status: pending
---

# TODO: Certificate A1 Vocabulary

Implements A1 level Standard vocabulary with grammatical gender and plural forms.

## Active Tasks

### impl_003: Vocabulary Lookup Functions
**Status:** in_progress
**Files:** src/vocabulary/a1.py
**Dependencies:** impl_001, impl_002

[... rest of TODO body ...]
```

---

## Common Commands Reference

### Project Setup
```bash
# Authenticate with GitHub
gh auth login

# Install dependencies
uv sync

# Detect technology stack
python .claude/skills/tech-stack-adapter/scripts/detect_stack.py
```

### Workflow Management
```bash
# Update TODO.md manifest
python .claude/skills/workflow-utilities/scripts/todo_updater.py .

# Create feature worktree
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature <slug> contrib/<gh-user>

# Daily rebase contrib branch
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  contrib/<gh-user>

# Run quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# Calculate semantic version
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v1.0.0

# Archive workflow (Phase 4.4)
python .claude/skills/workflow-utilities/scripts/workflow_archiver.py \
  TODO_feature_*.md --summary "What was completed" --version "X.Y.Z"

# Create directory with standards (CLAUDE.md, README.md, ARCHIVED/)
python .claude/skills/workflow-utilities/scripts/directory_structure.py \
  create <directory-path> "<purpose-description>"

# Deprecate files (archive with timestamp)
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  <todo-file> "<description>" <file1> <file2> ...
```

### Testing & Quality
```bash
# Run tests with coverage
uv run pytest --cov=src --cov-report=term --cov-fail-under=80

# Run tests only
uv run pytest

# Lint code
uv run ruff check src/ tests/

# Format code
uv run ruff format src/

# Type check
uv run mypy src/

# Build package
uv build
```

### Container Operations
```bash
# Build container
podman build -t standard:latest .

# Run tests in container
podman run --rm standard:latest pytest

# Run with compose
podman-compose up -d
podman-compose logs
podman-compose down
```

### Git Operations
```bash
# List worktrees
git worktree list

# Remove worktree
git worktree remove <path>

# Delete branch
git branch -D <branch-name>

# Create PR (feature → contrib)
gh pr create --base "contrib/<gh-user>" --head "<feature-branch>"

# Create PR (contrib → develop)
gh pr create --base "develop" --head "contrib/<gh-user>"
```

---

## Context Management

### Critical Token Threshold: 100K Tokens

**Effective context:** ~136K tokens (200K total - 64K system overhead)

**At 100K tokens used (~73% of effective capacity):**

Claude will **automatically**:
1. Save all task state to TODO_*.md (update YAML frontmatter)
2. Document current context in TODO body:
   - Current phase and step
   - Completed tasks
   - In-progress tasks
   - Next pending tasks
   - Any blockers or notes
3. Commit TODO_*.md updates

Then **you must**:
1. Run `/init` to update CLAUDE.md memory files with current state
2. Run `/compact` to compress memory and reduce token usage
3. Continue working - context is preserved in TODO_*.md

**Monitor context usage:**
```bash
/context
```

Token usage is shown in system warnings after each tool use:
```
Token usage: 100543/200000; 99457 remaining
```

**When you see usage approaching 100K:**
- Claude will proactively save state to TODO_*.md
- Wait for "✓ State saved to TODO file" confirmation
- Run /init (updates memory files) and /compact (compresses memory)
- Continue working with reduced token usage

**Best practices:**
- Check /context after each major phase (every 10-15K tokens)
- Archive completed workflows to reduce TODO.md size
- Use progressive skill loading (only load needed skills per phase)
- Expect 1-2 context resets per complex feature workflow

### State Preservation in TODO_*.md

When context reset is triggered, the following is saved to YAML frontmatter:

```yaml
workflow_progress:
  phase: 2                    # Current workflow phase (0-5)
  current_step: "2.4"        # Specific step within phase
  last_task: "impl_003"      # Last completed/active task ID
  last_update: "2025-10-23T15:30:00Z"
  status: "implementation"   # Current status

context_checkpoints:
  - timestamp: "2025-10-23T15:30:00Z"
    token_usage: 100234
    phase: 2
    step: "2.4"
    last_task: "impl_003"
    notes: "Completed script implementation, starting tests"
```

Plus task-level status updates for all tasks (pending → in_progress → completed)

---

## File Deprecation

When implementation replaces or removes existing files, use proper deprecation to maintain traceability.

### Deprecation Process

**When to deprecate files:**
- Replacing old implementation with new approach
- Removing obsolete features
- Consolidating multiple files into one
- Refactoring changes file structure

**Naming format:** `YYYYMMDDTHHMMSSZ_<description>.zip`
- **YYYYMMDDTHHMMSSZ:** Timestamp from the TODO file that deprecated the files
- **description:** Brief hyphen-separated description (e.g., "old-auth-flow", "legacy-api-v1")

### Using the Deprecation Script

**Command:**
```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  <todo-file> "<description>" <file1> <file2> ...
```

**Example:**
```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO_feature_20251023T104248Z_auth-refactor.md \
  "old-oauth-implementation" \
  src/auth/old_oauth.py \
  src/auth/legacy_tokens.py \
  tests/test_old_auth.py
```

**What happens:**
1. Extracts timestamp from TODO filename: `20251023T104248Z`
2. Creates archive: `ARCHIVED/20251023T104248Z_old-oauth-implementation.zip`
3. Adds files to zip archive
4. Removes original files from repository
5. Updates TODO file with deprecation entry
6. Commits changes

### Deprecation Examples

**Example 1: Replace authentication system**
```bash
# Deprecate old OAuth implementation
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO_feature_20251023T140000Z_auth-v2.md \
  "oauth-v1-system" \
  src/auth/oauth_v1.py \
  src/auth/token_manager_v1.py \
  tests/test_oauth_v1.py
```

Result: `ARCHIVED/20251023T140000Z_oauth-v1-system.zip`

**Example 2: Consolidate vocabulary modules**
```bash
# Deprecate separate A1/A2 files (now combined)
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO_feature_20251024T090000Z_vocab-consolidation.md \
  "separate-level-modules" \
  src/vocabulary/a1_nouns.py \
  src/vocabulary/a1_verbs.py \
  src/vocabulary/a2_nouns.py \
  src/vocabulary/a2_verbs.py
```

Result: `ARCHIVED/20251024T090000Z_separate-level-modules.zip`

**Example 3: Remove unused components**
```bash
# Deprecate experimental features that didn't work out
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO_feature_20251025T110000Z_cleanup.md \
  "experimental-quiz-engine" \
  src/quiz/experimental_engine.py \
  src/quiz/adaptive_algorithm.py \
  tests/test_experimental_quiz.py \
  docs/quiz_algorithm.md
```

Result: `ARCHIVED/20251025T110000Z_experimental-quiz-engine.zip`

### Locating Deprecated Files

**List all archived files by date:**
```bash
ls -lt ARCHIVED/*.zip
```

**Search for specific deprecation:**
```bash
ls ARCHIVED/*oauth*.zip
ls ARCHIVED/*20251023*.zip
```

**View archive contents without extracting:**
```bash
unzip -l ARCHIVED/20251023T140000Z_oauth-v1-system.zip
```

**Extract archived files for review:**
```bash
# Extract to temporary directory
mkdir -p /tmp/review
unzip ARCHIVED/20251023T140000Z_oauth-v1-system.zip -d /tmp/review

# Review files
ls -la /tmp/review

# Clean up when done
rm -rf /tmp/review
```

### Archive Retention

**Policy:**
- Archives stored indefinitely in ARCHIVED/ directory
- Tracked in git history
- Listed in TODO.md manifest (last 10)
- Review quarterly for cleanup (remove after 1 year if not needed)

**Finding related TODO:**
Each archive timestamp matches a TODO file:
```bash
# Archive: ARCHIVED/20251023T140000Z_oauth-v1-system.zip
# TODO: TODO_feature_20251023T140000Z_*.md

# Find corresponding TODO
ls TODO_feature_20251023T140000Z_*.md
# or if archived:
ls ARCHIVED_TODO_feature_20251023T140000Z_*.md
```

---

## Documentation Update Process

When modifying skill implementations (scripts, templates, Q&A flow), **all related documentation must be updated** to prevent documentation drift.

### Quick Reference

**Full update checklist:**
```bash
cat .claude/skills/UPDATE_CHECKLIST.md
```

**Validate versions:**
```bash
python .claude/skills/workflow-utilities/scripts/validate_versions.py --verbose
```

**Semi-automated sync:**
```bash
python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py \
  <skill-name> <new-version>
```

### Update Process (12 Steps)

When updating a skill (e.g., bmad-planner, speckit-author):

#### Step 1: Determine Version Bump

Use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR (X.0.0):** Breaking changes, removed features
- **MINOR (x.Y.0):** New features (backward compatible)
- **PATCH (x.y.Z):** Bug fixes, documentation improvements

#### Step 2-12: Follow UPDATE_CHECKLIST.md

The complete 12-step checklist ensures all files are updated:

```
.claude/skills/<skill-name>/SKILL.md       ← Version, commands, integration
.claude/skills/<skill-name>/CLAUDE.md      ← Usage examples
.claude/skills/<skill-name>/CHANGELOG.md   ← Version history
WORKFLOW.md                                 ← Phase sections, commands
CLAUDE.md                                   ← Command reference
[Integration files]                         ← Other skills affected
```

### Validation Tools

**Automatic validation:**
```bash
python .claude/skills/workflow-utilities/scripts/validate_versions.py
```

Validates:
- ✓ All SKILL.md files have valid semantic versions
- ✓ WORKFLOW.md has valid version
- ✓ TODO.md manifest version is valid
- ✓ Version references are consistent

**View current versions:**
```bash
python .claude/skills/workflow-utilities/scripts/validate_versions.py --verbose
```

Output:
```
Skill Versions:
  bmad-planner              v5.1.0
  speckit-author            v5.0.0
  workflow-orchestrator     v5.0.0
  git-workflow-manager      v5.0.0
  quality-enforcer          v5.0.0
  tech-stack-adapter        v5.0.0
  workflow-utilities        v5.0.0
```

### Semi-Automated Sync Tool

**Update skill documentation in one command:**

```bash
python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py \
  bmad-planner 5.2.0
```

**What it does:**
1. Updates version in SKILL.md frontmatter
2. Prompts for CHANGELOG entry
3. Updates CHANGELOG.md
4. Identifies affected WORKFLOW.md sections
5. Creates git commit with proper format

**Options:**
```bash
--archive     # Archive previous SKILL.md version
--dry-run     # Preview changes without making them
--auto-commit # Skip commit confirmation
```

**Example:**
```bash
# Dry run to preview changes
python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py \
  bmad-planner 5.2.0 --dry-run

# Update with archive
python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py \
  bmad-planner 5.2.0 --archive
```

### Common Mistakes to Avoid

❌ **Updating script without updating SKILL.md version**
- All script changes require version bump

❌ **Inconsistent command examples**
- Commands must match exactly in SKILL.md, CLAUDE.md, WORKFLOW.md

❌ **Forgetting to update WORKFLOW.md**
- Phase sections must reflect current skill behavior

❌ **Not updating token efficiency metrics**
- If script changes affect token usage, update all files

❌ **Missing CHANGELOG entry**
- Every version bump requires a CHANGELOG entry

### Example: Updating bmad-planner

**Change made:** Added database migration Q&A

**Version bump:** 5.0.0 → 5.1.0 (MINOR - new feature)

**Files updated:**
1. `.claude/skills/bmad-planner/SKILL.md` (version, Q&A flow)
2. `.claude/skills/bmad-planner/CLAUDE.md` (examples)
3. `.claude/skills/bmad-planner/CHANGELOG.md` (new entry)
4. `WORKFLOW.md` (Phase 1 interactive session)
5. `CLAUDE.md` (Phase 1 description)
6. `.claude/skills/speckit-author/SKILL.md` (integration note)

**Commit message:**
```
feat(bmad): add database migration strategy Q&A

Updated bmad-planner from v5.0.0 to v5.1.0:
- Added interactive Q&A for database migration strategy

Updated documentation:
- SKILL.md, CLAUDE.md, WORKFLOW.md, CHANGELOG.md

Refs: .claude/skills/bmad-planner/CHANGELOG.md
```

### Related Documentation

- **[UPDATE_CHECKLIST.md](.claude/skills/UPDATE_CHECKLIST.md)** - Complete 12-step checklist
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributor guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Repository changelog
- **[CLAUDE.md](CLAUDE.md)** - Quick command reference

---

## Troubleshooting

### Worktree Creation Failed
```bash
# Check for stale worktrees
git worktree list
git worktree prune

# Verify branch doesn't exist
git branch -a | grep <branch-name>
```

### Quality Gates Failing
```bash
# Check coverage
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html

# Check linting
uv run ruff check src/ tests/ --fix

# Check types
uv run mypy src/ --show-error-codes
```

### TODO.md Out of Sync
```bash
# Rebuild manifest
python .claude/skills/workflow-utilities/scripts/todo_updater.py .

# Verify
cat TODO.md
```

### Merge Conflicts
```bash
# In worktree
git fetch origin
git rebase origin/contrib/<gh-user>
# Resolve conflicts
git add .
git rebase --continue
```

---

## Success Metrics

Track these metrics to validate workflow effectiveness:

- **Token usage per phase:** Target <1,000 tokens (orchestrator + 1-2 skills)
- **Context resets:** Target <3 per feature
- **Quality gate pass rate:** Target 100% on first run
- **PR cycle time:** Track for optimization
- **Test coverage:** Maintain ≥80%
- **Manifest accuracy:** TODO.md reflects actual state (100%)

---

## Key Design Principles

1. **Progressive disclosure:** Load only relevant skills per phase
2. **Independence:** Skills don't cross-reference, orchestrator coordinates
3. **Token efficiency:** YAML metadata compact, load SKILL.md only when needed
4. **Context awareness:** Detect repo vs worktree, load appropriately
5. **User confirmation:** Always wait for "Y" before executing
6. **Quality enforcement:** Gates must pass before PR
7. **Python ecosystem:** uv, pytest-cov, Podman, FastAPI
8. **Semantic versioning:** Automatic calculation
9. **Archive management:** Proper deprecation with timestamps

---

## Related Documentation

- **[CLAUDE.md](CLAUDE.md)** - Claude Code interaction guide and quick command reference
- **[README.md](README.md)** - Project overview and getting started

### Skill Documentation

Referenced throughout this workflow:
- **Phase 0 (Initialization):** [initialize-repository](/.claude/skills/initialize-repository/SKILL.md) (meta-skill for bootstrapping new repos)
- **Phase 0 (Setup):** [tech-stack-adapter](/.claude/skills/tech-stack-adapter/SKILL.md), [git-workflow-manager](/.claude/skills/git-workflow-manager/SKILL.md), [workflow-utilities](/.claude/skills/workflow-utilities/SKILL.md)
- **Phase 1:** [bmad-planner](/.claude/skills/bmad-planner/SKILL.md), [workflow-utilities](/.claude/skills/workflow-utilities/SKILL.md)
- **Phase 2:** [git-workflow-manager](/.claude/skills/git-workflow-manager/SKILL.md), [speckit-author](/.claude/skills/speckit-author/SKILL.md), [quality-enforcer](/.claude/skills/quality-enforcer/SKILL.md), [workflow-utilities](/.claude/skills/workflow-utilities/SKILL.md)
- **Phase 3:** [quality-enforcer](/.claude/skills/quality-enforcer/SKILL.md), [workflow-utilities](/.claude/skills/workflow-utilities/SKILL.md)
- **Phase 4:** [git-workflow-manager](/.claude/skills/git-workflow-manager/SKILL.md), [workflow-utilities](/.claude/skills/workflow-utilities/SKILL.md)
- **Phase 5:** [git-workflow-manager](/.claude/skills/git-workflow-manager/SKILL.md), [quality-enforcer](/.claude/skills/quality-enforcer/SKILL.md), [workflow-utilities](/.claude/skills/workflow-utilities/SKILL.md)
- **Phase 6:** [git-workflow-manager](/.claude/skills/git-workflow-manager/SKILL.md), [speckit-author](/.claude/skills/speckit-author/SKILL.md) (optional), [quality-enforcer](/.claude/skills/quality-enforcer/SKILL.md), [workflow-utilities](/.claude/skills/workflow-utilities/SKILL.md)
- **Always available:** [workflow-orchestrator](/.claude/skills/workflow-orchestrator/SKILL.md)

---

**For more details on specific skills, see `.claude/skills/<skill-name>/SKILL.md`**
