# Workflow Guide - v6 (feature-dev)

**Version:** 6.0.0
**Date:** 2025-12-29
**Architecture:** 4-phase workflow using Gemini's feature-dev plugin

## Overview

This repository uses a streamlined 4-phase workflow for Python feature development:
- **Git-flow hybrid** with worktrees for isolation
- **Gemini feature-dev plugin** for planning, architecture, and code review
- **No separate quality gates** (feature-dev handles code quality)

## Prerequisites

Required tools:
- **VCS CLI** - GitHub (`gh`) OR Azure DevOps (`az`) for PR operations
- **uv** - Python package manager
- **git** - Version control with worktree support
- **Python 3.11+** - Language runtime
- **Gemini Code** - With feature-dev plugin

Verify prerequisites:
```bash
# VCS Provider (one of):
gh auth status          # GitHub: Must be authenticated
# OR
az account show         # Azure DevOps: Must be logged in

uv --version            # Must be installed
python3 --version       # Must be 3.11+
```

## v6 Workflow

```
/workflow:v6_1_worktree "feature description"
    | creates worktree, user runs /feature-dev in worktree
    v
/workflow:v6_2_integrate "feature/YYYYMMDDTHHMMSSZ_slug"
    | PR feature->contrib->develop (no quality gates)
    v
/workflow:v6_3_release
    | create release, PR to main, tag
    v
/workflow:v6_4_backmerge
    | PR release->develop, rebase contrib, cleanup
```

### Step 1: Create Worktree (`/workflow:v6_1_worktree`)

Creates isolated git worktree for feature development.

```bash
/workflow:v6_1_worktree "add user authentication"
```

**Output:**
- Branch: `feature/{timestamp}_{slug}`
- Worktree: `../{project}_feature_{timestamp}_{slug}/`

**Next steps displayed:** Navigate to worktree and run `/feature-dev`.

### Step 2: Feature Development (`/feature-dev`)

Run in the feature worktree (not main repo):

```bash
cd <worktree-path>
/feature-dev "add user authentication"
```

**feature-dev handles:**
- Understanding the codebase
- Planning the implementation
- Writing code
- Code review and refinement

No separate planning documents needed.

### Step 3: Integrate (`/workflow:v6_2_integrate`)

From main repo, after feature-dev is complete:

```bash
/workflow:v6_2_integrate "feature/20251229T120000Z_add-user-auth"
```

**Two modes:**
- **Full mode** (with branch arg): PR feature->contrib, cleanup worktree, PR contrib->develop
- **Contrib-only mode** (no arg): PR contrib->develop only

**Manual gates:** PRs require approval in GitHub/Azure DevOps UI.

### Step 4: Release (`/workflow:v6_3_release`)

Creates release from develop:

```bash
/workflow:v6_3_release           # Auto-calculate version
/workflow:v6_3_release v1.2.0    # Explicit version
```

**Creates:**
- Branch: `release/{version}` from develop
- PR to main (requires approval)
- Tag on main after merge

### Step 5: Backmerge (`/workflow:v6_4_backmerge`)

Syncs release changes back:

```bash
/workflow:v6_4_backmerge
```

**Actions:**
- PR release->develop (requires approval)
- Rebases contrib on develop
- Deletes release branch

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
- `release/*` - Created in v6_3_release, deleted in v6_4_backmerge

## Key Differences from v1-v7

| Aspect | v1-v7 | v6 |
|--------|-------|-----|
| Planning | BMAD documents + SpecKit specs | feature-dev plugin |
| Quality gates | 5 separate gates | feature-dev code review |
| Steps | 7 phases | 4 phases |
| Artifacts | requirements.md, architecture.md, spec.md, plan.md | None (feature-dev handles) |

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

- **[GEMINI.md](GEMINI.md)** - Main AI context file
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
