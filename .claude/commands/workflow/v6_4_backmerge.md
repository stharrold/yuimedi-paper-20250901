---
description: "Sync release to develop and contrib | v6 workflow step 4 of 4"
order: 4
prev: /workflow:v6_3_release
---

# /workflow:v6_4_backmerge - Step 4 of 4

**v6 Workflow**: `/workflow:v6_1_worktree` -> [feature-dev] -> `/workflow:v6_2_integrate` -> `/workflow:v6_3_release` -> `/workflow:v6_4_backmerge`

**Purpose**: Sync release changes back to develop and rebase contrib.

**Prerequisites**: Main repo, `contrib/*` branch, release tagged on main

**Outputs**: Release merged to develop, contrib rebased, release branch deleted

---

## Usage

```
/workflow:v6_4_backmerge
```

---

## Step 1: Create PR release -> develop

```bash
uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py pr-develop
```

This creates PR from release branch to develop.

**MANUAL GATE**: Wait for PR approval and merge in GitHub UI.

---

## Step 2: Rebase Contrib on Develop

After PR is merged:

```bash
uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py rebase-contrib
```

This:
- Fetches latest develop
- Rebases contrib/stharrold onto develop
- Force pushes (with lease) to update remote

---

## Step 3: Cleanup Release Branch

```bash
uv run python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py cleanup-release
```

This:
- Deletes local release branch
- Deletes remote release branch

---

## Step 4: Record State in AgentDB

```bash
uv run python .claude/skills/agentdb-state-manager/scripts/record_sync.py \
  --sync-type workflow_transition \
  --pattern phase_v6_4_backmerge
```

---

## Step 5: Report Completion

Display to user:

```
[OK] Backmerge complete

- Release merged to develop
- Contrib rebased on develop
- Release branch cleaned up

Workflow complete! Ready for next feature.
Next: Run /workflow:v6_1_worktree "next feature" to start again
```

---

## Notes

- Always ends on contrib/* branch (editable)
- Contrib is rebased to stay current with develop
- Release branch is ephemeral (created in v6_3, deleted in v6_4)
