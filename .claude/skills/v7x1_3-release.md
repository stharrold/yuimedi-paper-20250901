---
name: v7x1_3-release
description: Release to production (Step 3 of 4)
---

# /v7x1_3-release - Step 3 of 4

**v7x1 Workflow**: `/v7x1_1-worktree` → Implementation → `/v7x1_2-integrate` → `/v7x1_3-release` → `/v7x1_4-backmerge`

**Task**: Create release from develop, PR to main, tag release.

**Input**: Version (optional - auto-calculates if empty)

## Step 1: Create Release Branch

```bash
uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py create-release
```

Or with explicit version:
```bash
uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py create-release --version v1.2.0
```

## Step 2: Create PR to Main

```bash
uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py pr-main
```

**MANUAL GATE**: User merges PR in GitHub UI.

## Step 3: Tag Release (After Merge)

```bash
uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py tag-release
```

## Step 4: Report Completion

```
✓ Release {version} complete

- Release branch: release/{version}
- PR to main: merged
- Tag: {version} created on main

Next: /v7x1_4-backmerge to sync back to develop
```

## Alternative: Full Workflow

Run all steps automatically (still requires manual PR merges):

```bash
uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py full
```

## Reference

Full documentation: `.claude/skills/v7x1-workflow.md`
