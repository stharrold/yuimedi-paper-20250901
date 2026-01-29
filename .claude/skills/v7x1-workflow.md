---
name: v7x1-workflow
description: |
  Git workflow assistant for the v7x1 4-phase model (worktree, integrate, release, backmerge).

  Use when: User asks about workflow phases, "what's next?", or needs git workflow commands.
  Triggers: workflow, worktree, integrate, release, backmerge, PR, what's next
---

# v7x1 Workflow Skill

Wraps existing Python scripts in `.claude/skills/git-workflow-manager/scripts/` with context-aware suggestions.

## Context Detection

Run these commands to determine current phase:

```bash
git branch --show-current    # Current branch
git worktree list            # Active worktrees
git describe --tags --abbrev=0 origin/main 2>/dev/null  # Latest release
```

**Branch patterns indicate phase:**
| Branch | Suggested Phase |
|--------|-----------------|
| `feature/*` | Phase 2 (Integrate) |
| `contrib/*` | Phase 1 (new feature) or Phase 2 (PR to develop) |
| `release/*` | Phase 3 (tag) or Phase 4 (backmerge) |
| `develop` | Phase 3 (Release) |

**Placeholders:** `<gh-user>` = your GitHub username, `<slug>` = kebab-case feature name

## Phase 1: Create Worktree

**When:** Starting a new feature from contrib branch.

```bash
uv run python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature <slug> contrib/<gh-user>
```

**Example:**
```bash
uv run python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature add-user-auth contrib/stharrold
```

**Output:** Creates worktree at `../{repo}_feature_{timestamp}_{slug}/` with branch `feature/{timestamp}_{slug}`

**Next:** Navigate to worktree, implement feature.

## Phase 2: Integrate

**When:** Feature complete, ready to merge.

**Full mode** (from feature branch):
```bash
# Push feature and create PR to contrib
git push -u origin <feature-branch>
uv run scripts/secrets_run.py gh pr create --base contrib/stharrold --head <feature-branch> --fill

# [MANUAL] Merge PR in GitHub UI

# After merge, get cleanup instructions
uv run python .claude/skills/git-workflow-manager/scripts/cleanup_feature.py <slug>
# Then execute the manual commands it outputs:
#   git worktree remove <path>
#   git branch -d <branch>
#   git push origin --delete <branch>

# Create PR contrib -> develop
uv run scripts/secrets_run.py gh pr create --base develop --head contrib/stharrold --fill

# [MANUAL] Merge PR in GitHub UI
```

**Contrib-only mode** (no feature branch):
```bash
uv run scripts/secrets_run.py gh pr create --base develop --head contrib/stharrold --fill
# [MANUAL] Merge PR in GitHub UI
```

## Phase 3: Release

**When:** Develop ready for production.

```bash
# Full workflow (auto-calculates version)
uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py full

# Or with explicit version
uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py full --version v1.46.0
```

**Step-by-step:**
```bash
uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py create-release
uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py pr-main
# [MANUAL] Merge PR in GitHub UI
uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py tag-release
```

**Status:** `uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py status`

## Phase 4: Backmerge

**When:** Release tagged, sync back to develop.

```bash
# Full workflow
uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py full
```

**Step-by-step:**
```bash
uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py pr-develop
# [MANUAL] Merge PR in GitHub UI
uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py rebase-contrib
uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py cleanup-release
# Script outputs manual commands - execute them:
#   git branch -d release/vX.Y.Z
#   git push origin --delete release/vX.Y.Z
```

**Status:** `uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py status`

## Quick Reference

```
contrib/* (start)
    |
    v
Phase 1: create_worktree.py feature <slug> contrib/stharrold
    |
    v
feature/* (implement)
    |
    v
Phase 2: gh pr create (feature->contrib, then contrib->develop)
    |
    v
develop (features integrated)
    |
    v
Phase 3: release_workflow.py full
    |
    v
main (tagged vX.Y.Z)
    |
    v
Phase 4: backmerge_workflow.py full
    |
    v
contrib/* (synced, ready for next feature)
```

## Manual Gates

All PRs require manual approval in GitHub UI:
- Feature -> contrib
- Contrib -> develop
- Release -> main
- Release -> develop (backmerge)

## Detailed Documentation

For complete script arguments, error handling, and examples:
- `.claude/skills/git-workflow-manager/SKILL.md`
