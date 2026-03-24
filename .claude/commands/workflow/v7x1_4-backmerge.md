---
description: Sync release to develop and contrib (Step 4 of 4)
---

# /workflow:v7x1_4-backmerge - Step 4 of 4

**Context Check**: !`python3 .claude/skills/workflow-utilities/scripts/verify_workflow_context.py --step 7`

## Step 1: PR release -> develop
Run: `uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py pr-develop`

## Step 2: Manual Merge (release -> develop)
**Action**: Merge the PR manually through the GitHub web portal GUI.

## Step 3: Rebase Contrib (After Merge)
Run: `uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py rebase-contrib`

## Step 4: Cleanup
Run: `uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py cleanup-release`

## Step 5: Record State
Run: `uv run python .claude/skills/agentdb-state-manager/scripts/record_sync.py --sync-type workflow_transition --pattern phase_v7x1_4_backmerge`

## Error Recovery
- **Context check fails**: Ensure you are on `contrib/*` branch in the main repo.
- **No release branch found**: Backmerge requires an active `release/*` branch. Run `/workflow:v7x1_3-release` first.
- **Rebase conflicts**: Resolve manually with `git rebase --continue` or `git rebase --abort` to restart.
- **Branch divergence**: If contrib diverged from remote, run `git fetch origin && git reset --hard origin/{contrib_branch}`.
