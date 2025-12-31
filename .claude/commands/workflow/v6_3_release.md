---
description: "Release to production | v6 workflow step 3 of 4"
order: 3
prev: /workflow:v6_2_integrate
next: /workflow:v6_4_backmerge
---

# /workflow:v6_3_release - Step 3 of 4

**v6 Workflow**: `/workflow:v6_1_worktree` -> [feature-dev] -> `/workflow:v6_2_integrate` -> `/workflow:v6_3_release` -> `/workflow:v6_4_backmerge`

**Purpose**: Create release from develop, create PR to main, tag release.

**Prerequisites**: Main repo, `contrib/*` branch, changes integrated to develop

**Outputs**: Release branch, PR to main, version tag

---

## Usage

```
/workflow:v6_3_release
```

Optional: Specify version
```
/workflow:v6_3_release v1.2.0
```

---

## Step 1: Calculate Version

If version not provided, calculate next version:

```bash
# Get latest tag
git fetch --tags
latest_tag=$(git describe --tags --abbrev=0 origin/main 2>/dev/null || echo "v0.0.0")

# Bump minor version (default)
# v1.2.3 -> v1.3.0
```

---

## Step 2: Create Release Branch

```bash
uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py create-release
```

This creates:
- Branch: `release/{version}` from develop
- Pushes branch to origin

---

## Step 3: Create PR to Main

```bash
uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py pr-main
```

Creates PR from release branch to main.

**MANUAL GATE**: Wait for PR approval and merge in GitHub UI.

---

## Step 4: Tag Release

After PR is merged:

```bash
uv run python .claude/skills/git-workflow-manager/scripts/release_workflow.py tag-release
```

This:
- Creates annotated tag on main
- Pushes tag to origin

---

## Step 5: Record State in AgentDB

```bash
uv run python .claude/skills/agentdb-state-manager/scripts/record_sync.py \
  --sync-type workflow_transition \
  --pattern phase_v6_3_release
```

---

## Step 6: Report Completion

Display to user:

```
[OK] Release {version} complete

- Release branch: release/{version}
- PR to main: merged
- Tag: {version} created on main

Next: Run /workflow:v6_4_backmerge to sync release to develop
```

---

## Notes

- Release branch is temporary (deleted in v6_4_backmerge)
- Semantic versioning: vMAJOR.MINOR.PATCH
- Tag is created on main after PR merge
