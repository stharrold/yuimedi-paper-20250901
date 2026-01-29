---
name: v7x1_4-backmerge
description: Sync release to develop and contrib (Step 4 of 4)
---

# /v7x1_4-backmerge - Step 4 of 4

**v7x1 Workflow**: `/v7x1_1-worktree` → Implementation → `/v7x1_2-integrate` → `/v7x1_3-release` → `/v7x1_4-backmerge`

**Task**: Merge release back to develop, rebase contrib, cleanup release branch.

## Step 1: PR release → develop

```bash
uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py pr-develop
```

**MANUAL GATE**: User merges PR in GitHub UI.

## Step 2: Rebase Contrib (After Merge)

```bash
uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py rebase-contrib
```

## Step 3: Cleanup Release Branch

```bash
uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py cleanup-release
```

Then execute the manual commands it outputs:
```bash
git branch -d release/vX.Y.Z
git push origin --delete release/vX.Y.Z
```

## Step 4: Report Completion

```
✓ Backmerge complete

- Release merged to develop
- Contrib rebased on develop
- Release branch cleaned up

Workflow complete! Ready for next feature.
Next: /v7x1_1-worktree "next feature"
```

## Alternative: Full Workflow

Run all steps automatically (still requires manual PR merge):

```bash
uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py full
```

## Reference

Full documentation: `.claude/skills/v7x1-workflow.md`
