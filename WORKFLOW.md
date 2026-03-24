# Workflow Guide - v7x1 (Implementation)

**Version:** 7.0.0
**Date:** 2026-01-01
**Architecture:** 4-phase workflow using Claude Code

## Overview

This repository uses a streamlined 4-phase workflow for Python development:
- **Git-flow hybrid** with worktrees for isolation
- **Claude Code** for planning, architecture, and implementation
- **No separate manual quality gates** (Claude Code Review automated via GitHub Actions)

## Prerequisites

Required tools:
- **VCS CLI** - GitHub (`gh`) for PR operations
- **uv** - Python package manager
- **git** - Version control with worktree support
- **Python 3.11+** - Language runtime
- **Claude Code** - AI development assistant

Verify prerequisites:
```bash
# GitHub CLI:
gh auth status          # Must be authenticated

uv --version            # Must be installed
python3 --version       # Must be 3.11+
```

## Phase 0: Bootstrapping a New Repository

This repository provides a meta-skill to bootstrap other projects with this workflow system.

### From This Repository
```bash
python .claude/skills/initialize-repository/scripts/initialize_repository.py . /path/to/new-repo
```

### From a Cloned Release
If you have cloned `stharrold-templates` into a subdirectory (e.g., `.tmp/`):
```bash
python .tmp/stharrold-templates/.claude/skills/initialize-repository/scripts/apply_workflow.py .tmp/stharrold-templates .
```

## v7x1 Workflow

```
/workflow:v7x1_1-worktree "feature description"
    | creates worktree, user implements feature in worktree
    v
/workflow:v7x1_2-integrate "feature/YYYYMMDDTHHMMSSZ_slug"
    | PR feature->contrib->develop
    v
/workflow:v7x1_3-release
    | create release, PR to main, tag
    v
/workflow:v7x1_4-backmerge
    | PR release->develop, rebase contrib, manual cleanup
```

### Step 1: Create Worktree (`/workflow:v7x1_1-worktree`)

Creates isolated git worktree for feature development.

```bash
/workflow:v7x1_1-worktree "add user authentication"
```

**Output:**
- Branch: `feature/{timestamp}_{slug}`
- Worktree: `../{project}_feature_{timestamp}_{slug}/`

**Next steps displayed:** Navigate to worktree and implement the feature.

### Step 2: Feature Implementation

Run in the feature worktree (not main repo) using Claude Code:

```bash
cd <worktree-path>
# Then just chat with Claude Code:
"Implement user authentication with JWT tokens"
```

**Claude Code handles:**
- Understanding the codebase
- Planning the implementation
- Writing code and tests
- Refinement

No separate planning documents needed.

### Step 3: Integrate (`/workflow:v7x1_2-integrate`)

From main repo, after implementation is complete:

```bash
/workflow:v7x1_2-integrate "feature/20251229T120000Z_add-user-auth"
```

**Two modes:**
- **Full mode** (with branch arg): PR feature->contrib, manual worktree cleanup, manual branch cleanup, PR contrib->develop
- **Contrib-only mode** (no arg): PR contrib->develop only

**Manual gates:** PRs require approval in GitHub UI.

### Step 4: Release (`/workflow:v7x1_3-release`)

Creates release from develop:

```bash
/workflow:v7x1_3-release           # Auto-calculate version
/workflow:v7x1_3-release v1.2.0    # Explicit version
```

**Creates:**
- Branch: `release/{version}` from develop
- PR to main (requires approval)
- Tag on main after merge

### Step 5: Backmerge (`/workflow:v7x1_4-backmerge`)

Syncs release changes back:

```bash
/workflow:v7x1_4-backmerge
```

**Actions:**
- PR release->develop (requires approval)
- Rebases contrib on develop
- Instructs manual deletion of release branch

## Branch Structure

```
main                           <- Production (tagged vX.Y.Z)
  ^
release/vX.Y.Z                <- Release candidate (ephemeral)
  ^
develop                        <- Integration branch
  ^
contrib/<gh-user>             <- Personal contribution (contrib/stharrold)
  ^
feature/<timestamp>_<slug>    <- Isolated feature (worktree)
```

### Branch Protection

**Protected branches (PR-only):**
- `main` - Production
- `develop` - Integration

**Editable branches:**
- `contrib/*` - Personal contribution
- `feature/*` - Feature development

**Ephemeral branches:**
- `release/*` - Created in `/workflow:v7x1_3-release`, manually deleted after `/workflow:v7x1_4-backmerge`

## Key Differences from v1-v7

| Aspect | v1-v7 | v7x1 |
|--------|-------|-----|
| Planning | BMAD documents + SpecKit specs | Built-in Claude Code tools |
| Quality gates | 5 separate gates | Claude Code Review |
| Steps | 7 phases | 4 steps |
| Artifacts | requirements.md, architecture.md, spec.md, plan.md | None (Claude Code handles internally) |

## Skills System

| Skill | Purpose |
|-------|---------|
| workflow-orchestrator | Main coordinator, templates |
| git-workflow-manager | Worktrees, PRs, semantic versioning |
| tech-stack-adapter | Python/uv detection |
| workflow-utilities | Archive, directory structure |
| agentdb-state-manager | Workflow state tracking |
| initialize-repository | Bootstrap new repos |

**Archived skills** (see `ARCHIVED/`):
- bmad-planner
- speckit-author
- quality-enforcer

## Related Documentation

- **[CLAUDE.md](CLAUDE.md)** - Main AI context file
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
