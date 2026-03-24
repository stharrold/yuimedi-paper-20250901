---
description: Create worktree for autonomous implementation (Step 1 of 4)
argument-hint: "[feature description]"
---

# /workflow:v7x1_1-worktree - Step 1 of 4

**Context Check**: !`python3 .claude/skills/workflow-utilities/scripts/verify_workflow_context.py --step 1`

**Task**: Create a git worktree for: $ARGUMENTS

**v7x1 Workflow**: `/workflow:v7x1_1-worktree` → Implementation → `/workflow:v7x1_2-integrate` → `/workflow:v7x1_3-release` → `/workflow:v7x1_4-backmerge`

## Step 1: Extract Feature Slug
Parse "$ARGUMENTS" to create a kebab-case slug (lowercase, hyphens, limit 50 chars).

## Step 1.5: Detect Contrib Branch
Detect the contrib branch: first check if the current branch (`git branch --show-current`) matches `contrib/*` — if so, use it. Otherwise, run `git branch --list 'contrib/*' --sort=-committerdate` and use the first result (most recently updated). If no contrib branches exist, fail with instructions to create one.

## Step 2: Create Feature Worktree
Run: `uv run python .claude/skills/git-workflow-manager/scripts/create_worktree.py feature {slug} {contrib_branch}`

## Step 3: Record State in AgentDB
Run: `uv run python .claude/skills/agentdb-state-manager/scripts/record_sync.py --sync-type workflow_transition --pattern phase_v7x1_1_worktree --source "main_repo" --target "worktree"`

## Step 4: Display Next Steps
Show worktree path and instructions for running `built-in tools "$ARGUMENTS"` in the worktree.

## Error Recovery
- **Context check fails**: Ensure you are on `contrib/*` branch in the main repo (not a worktree). Run `git checkout contrib/<user>`.
- **Worktree already exists**: Run `git worktree list` to check. Remove with `git worktree remove <path>` then `git worktree prune`.
- **Branch already exists**: Delete with `git branch -d <branch>` (or `-D` to force).
- **AgentDB record fails**: Non-blocking. Worktree is still created. Re-run the record_sync command manually.
