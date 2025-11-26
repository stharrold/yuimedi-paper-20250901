---
description: "workflow/6_release → workflow/7_backmerge → (end) | Sync release to develop and contrib"
order: 7
prev: /6_release
---

# /7_backmerge - Step 7 of 7

**Workflow**: `/1_specify` → `/2_plan` → `/3_tasks` → `/4_implement` → `/5_integrate` → `/6_release` → `/7_backmerge`

**Purpose**: Sync release changes back to development branches (PR release to develop, rebase contrib on develop).

**Prerequisites**: Release PR merged to main (from `/6_release`), tag created on main, release branch still exists

**Outputs**: PR release to develop merged, contrib rebased on develop, release branch cleaned up

**Next**: Workflow complete. Return to `/1_specify` for next feature.

---

## Step 0: Verify Context (REQUIRED - STOP if fails)

**Run this first. If it fails, STOP and tell the user to fix the context.**

```bash
python .claude/skills/workflow-utilities/scripts/verify_workflow_context.py --step 7
```

Expected: Main repo, `contrib/*` branch

---

# Backmerge Workflow Command

Sync release changes back to development branches.

## Release-to-Develop Pattern

The backmerge uses the **release branch directly** to PR to develop:

```
release/vX.Y.Z ──PR──> main ──(tag vX.Y.Z)
       │
       └──────────PR──> develop
                        │
                        └──> (delete release/* after merge)
```

**Important**: The release branch must still exist when running step 7.

## Workflow Steps (in order)

1. **pr-develop** - Create PR from release branch to develop
2. **(Manual)** - Merge the PR in GitHub UI after approval
3. **rebase-contrib** - Rebase contrib branch on updated develop
4. **cleanup-release** - Delete release branch

## Version Auto-Detection

If `--version` is not specified, the script automatically detects the version from the latest tag on main:
```bash
git describe --tags --abbrev=0 origin/main
```

## Usage

Run workflow step:
```bash
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py <step>
```

## Available Steps

- `pr-develop` - Create PR from release branch to develop
- **(Manual step)** - Merge the PR in GitHub UI after approval
- `rebase-contrib` - Rebase contrib/* on develop
- `cleanup-release` - Delete release branch
- `full` - Run all steps in sequence
- `status` - Show current backmerge status

## Example Session

```bash
# 1. Create PR from release branch to develop (version auto-detected)
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py pr-develop

# Or specify version explicitly
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py pr-develop --version v5.10.0

# 2. After PR approved and merged
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py rebase-contrib

# 3. Cleanup release branch
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py cleanup-release
```

## Key Features

### Requires Release Branch
- Release branch must exist when running step 7
- If release branch was deleted early, recreate from main:
  ```bash
  git checkout -b release/vX.Y.Z origin/main
  git push -u origin release/vX.Y.Z
  ```

### Idempotency
- Running `pr-develop` twice reports "already exists" for existing PRs
- Running `cleanup-release` ignores missing branches

### Safe Rebasing
- Uses `--force-with-lease` for safe force push
- Detects uncommitted changes before rebase
- Provides manual conflict resolution instructions

## Conflict Resolution

If rebase conflicts occur:
1. Script pauses with conflict message
2. Resolve conflicts manually
3. Run `git rebase --continue`
4. Run `git push --force-with-lease`

## Step 4: Record State in AgentDB

After cleanup, record the workflow transition:
```bash
podman-compose run --rm dev python .claude/skills/agentdb-state-manager/scripts/record_sync.py \
  --sync-type workflow_transition \
  --pattern phase_7_backmerge
```

## Notes

- Always ends on editable branch (`contrib/*`)
- Release branch is deleted after backmerge PR is merged
- All branches synced and ready for next feature cycle
- AgentDB records the backmerge completion for workflow tracking
- Workflow complete - return to `/1_specify` for next feature
