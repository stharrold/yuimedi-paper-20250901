---
description: "workflow/6_release → workflow/7_backmerge → (end) | Sync release to develop and contrib"
order: 7
prev: /6_release
---

# /7_backmerge - Step 7 of 7

**Workflow**: `/1_specify` → `/2_plan` → `/3_tasks` → `/4_implement` → `/5_integrate` → `/6_release` → `/7_backmerge`

**Purpose**: Sync release changes back to development branches (PR release to develop, rebase contrib on develop).

**Prerequisites**: Release PR merged to main (from `/6_release`), release branch still exists

**Outputs**: PR release to develop merged, contrib rebased on develop, release branch deleted

**Next**: Workflow complete. Return to `/1_specify` for next feature.

---

# Backmerge Workflow Command

Sync release changes back to development branches.

## Workflow Steps (in order)

1. **pr-develop** - Create PR from release branch to develop
2. **(Manual)** - Merge the PR in GitHub UI after approval
3. **rebase-contrib** - Rebase contrib branch on updated develop
4. **cleanup-release** - Delete release branch

## Two-Phase Sync Strategy

### Phase 1: PR release → develop (Merge)
- Preserves release history via merge commit
- Requires review for release changes (version bumps, hotfixes)
- Handles potential conflicts with develop

### Phase 2: Rebase contrib on develop
- Keeps contrib branch linear and clean
- Avoids merge commits in personal branch
- Uses `--force-with-lease` for safe push

## Usage

Run workflow step:
```bash
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py <step>
```

## Available Steps

- `pr-develop` - Create PR from release to develop
- **(Manual step)** - Merge the PR in GitHub UI after approval
- `rebase-contrib` - Rebase contrib/* on develop
- `cleanup-release` - Delete release branch locally and remotely
- `full` - Run all steps in sequence
- `status` - Show current backmerge status

## Example Session

```bash
# 1. Create PR from release to develop
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py pr-develop

# 2. After PR approved and merged
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py rebase-contrib

# 3. Cleanup release branch
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py cleanup-release
```

## Conflict Resolution

If rebase conflicts occur:
1. Script pauses with conflict message
2. Resolve conflicts manually
3. Run `git rebase --continue`
4. Script resumes with cleanup

## Notes

- Always ends on editable branch (`contrib/*`)
- Release branch is deleted after backmerge
- All branches synced and ready for next feature cycle
