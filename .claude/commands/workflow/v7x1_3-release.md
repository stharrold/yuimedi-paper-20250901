---
description: Release to production (Step 3 of 4)
argument-hint: "[version]"
---

# /workflow:v7x1_3-release - Step 3 of 4

**Task**: Release version $ARGUMENTS (auto-calculate if empty)

**Context Check**: !`python3 .claude/skills/workflow-utilities/scripts/verify_workflow_context.py --step 6`

## Step 1: Create Release Branch
Run: `uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py create-release`

## Step 2: Create PR to Main
Run: `uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py pr-main`

## Step 3: Manual Merge (release -> main)
**Action**: Merge the PR manually through the GitHub web portal GUI.

## Step 4: Tag Release (After Merge)
Run: `uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py tag-release`

## Step 5: Record State
Run: `uv run python .claude/skills/agentdb-state-manager/scripts/record_sync.py --sync-type workflow_transition --pattern phase_v7x1_3_release`

## Error Recovery
- **Context check fails**: Ensure you are on `contrib/*` branch in the main repo. Run `git checkout contrib/<user>`.
- **Release branch exists**: A previous release may be in progress. Run `git branch -a | grep release` to check.
- **Version conflict**: Pass explicit version via $ARGUMENTS (e.g., `/workflow:v7x1_3-release v8.2.0`).
- **Tag already exists**: Delete with `git tag -d <tag> && git push origin --delete <tag>`, then re-run.
