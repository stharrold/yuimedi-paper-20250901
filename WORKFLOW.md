# Workflow Guide - YuiQuery Healthcare Analytics Research

**Version:** 5.3.0
**Date:** 2025-11-25
**Architecture:** Skill-based progressive disclosure with BMAD + SpecKit + Claude Code + PR Feedback Work-Items

## Overview

This repository uses a modular skill-based git workflow for documentation and research development. The workflow combines:
- **Git-flow + GitHub-flow hybrid** with worktrees for isolation
- **BMAD planning** (requirements + architecture) in main repo
- **SpecKit specifications** (spec + plan) in feature worktrees
- **8 specialized skills** loaded progressively per workflow phase
- **Quality gates** enforced before integration (≥80% coverage, all tests passing)

## Prerequisites

Required tools:
- **VCS CLI** - GitHub (`gh`) OR Azure DevOps (`az`) for PR operations
- **uv** - Python package manager
- **git** - Version control with worktree support
- **Python 3.11+** - Language runtime
- **podman** (optional) - Container operations

Verify prerequisites:
```bash
# VCS Provider (one of):
gh auth status          # GitHub: Must be authenticated
# OR
az account show         # Azure DevOps: Must be logged in
az extension add --name azure-devops  # Required for Azure DevOps

uv --version            # Must be installed
python3 --version       # Must be 3.11+
podman --version        # Optional
```

**VCS auto-detection:** The workflow detects your VCS provider from git remote URL.
For explicit config, create `.vcs_config.yaml` (see CLAUDE.md for format).

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
│       ├── worktree_context.py
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

**backmerge_workflow.py** follows PR workflow:
- **Purpose:** Back-merge release branches to develop (Step 7)
- **Process:** Creates PR directly from release branch to develop
- **Location:** `.claude/skills/git-workflow-manager/scripts/backmerge_workflow.py`
- **No direct commits:** Script creates PR only (merge happens in GitHub/Azure DevOps UI)
- **Note:** `backmerge_release.py` has been archived (redundant with backmerge_workflow.py)

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

The workflow consists of 7 phases. Detailed documentation for each phase is in `docs/reference/`:

| Phase | Name | Document | Description |
|-------|------|----------|-------------|
| 0 | Initial Setup | [workflow-planning.md](docs/reference/workflow-planning.md) | Prerequisites, skill setup, contrib branch |
| 1 | Planning (BMAD) | [workflow-planning.md](docs/reference/workflow-planning.md) | Requirements, architecture, epics |
| 2 | Feature Development | [workflow-planning.md](docs/reference/workflow-planning.md) | Worktree creation, SpecKit specs |
| 3 | Quality Assurance | [workflow-planning.md](docs/reference/workflow-planning.md) | Testing, coverage gates |
| 4 | Integration & PR | [workflow-integration.md](docs/reference/workflow-integration.md) | Semantic versioning, PR workflow |
| 5 | Release | [workflow-integration.md](docs/reference/workflow-integration.md) | Release branches, tagging |
| 6 | Hotfix | [workflow-hotfix.md](docs/reference/workflow-hotfix.md) | Production fixes |

**Operations & Maintenance:** [workflow-operations.md](docs/reference/workflow-operations.md)
- Context management, file deprecation, troubleshooting

### Quick Start

```bash
# Phase 0: Setup (one-time)
# For GitHub:
gh auth status && git checkout -b contrib/$(gh api user --jq '.login')
# For Azure DevOps:
az account show && git checkout -b contrib/$(az devops user show --user me --query user.emailAddress -o tsv | cut -d@ -f1)

# Phase 1: Planning (replace <username> with your VCS username)
python .claude/skills/bmad-planner/scripts/create_planning.py my-feature <username>

# Phase 2: Development
python .claude/skills/git-workflow-manager/scripts/create_worktree.py feature my-feature contrib/<username>

# Phase 3: Quality
podman-compose run --rm dev python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# Phase 4-5: Integration & Release
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/pr_workflow.py full
```

### Slash Commands

Use these slash commands for guided workflow execution:

| Command | Phase | Purpose |
|---------|-------|---------|
| `/workflow/all` | All | Orchestrate full workflow with auto-detection |
| `/1_specify` | 1 | Create feature branch and specification |
| `/2_plan` | 2 | Generate design artifacts |
| `/3_tasks` | 3 | Generate ordered task list |
| `/4_implement` | 4 | Execute tasks automatically |
| `/5_integrate` | 5 | Create PRs (feature→contrib→develop) |
| `/6_release` | 6 | Create release (develop→main) |
| `/7_backmerge` | 7 | Sync release to develop and contrib |

## Related Documentation

- **[CLAUDE.md](CLAUDE.md)** - Main AI context file
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

### Detailed Phase Documentation

- **[Planning Phases (0-3)](docs/reference/workflow-planning.md)** - Setup, BMAD, development, QA
- **[Integration Phases (4-5)](docs/reference/workflow-integration.md)** - PR workflow, releases
- **[Hotfix Phase (6)](docs/reference/workflow-hotfix.md)** - Production fixes
- **[Operations](docs/reference/workflow-operations.md)** - Context, maintenance, troubleshooting
