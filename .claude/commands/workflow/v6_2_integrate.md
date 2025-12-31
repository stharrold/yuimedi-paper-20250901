---
description: "Integrate feature to develop | v6 workflow step 2 of 4"
order: 2
prev: /workflow:v6_1_worktree
next: /workflow:v6_3_release
---

# /workflow:v6_2_integrate - Step 2 of 4

**v6 Workflow**: `/workflow:v6_1_worktree` -> [feature-dev] -> `/workflow:v6_2_integrate` -> `/workflow:v6_3_release` -> `/workflow:v6_4_backmerge`

**Purpose**: Create PRs from feature -> contrib -> develop.

**Prerequisites**: Main repo, `contrib/*` branch, feature implementation complete

**Outputs**: PRs created, worktree cleaned (if full mode)

---

## Usage

### Full Integration (with feature branch)
```
/workflow:v6_2_integrate "feature/YYYYMMDDTHHMMSSZ_slug"
```

### Contrib-Only Integration (no feature branch)
```
/workflow:v6_2_integrate
```

---

## Mode Detection

- **Full mode**: Branch argument provided (e.g., "feature/20251229T120000Z_auth")
  - Runs: feature -> contrib PR, worktree cleanup, contrib -> develop PR
- **Contrib-only mode**: No argument provided
  - Runs: contrib -> develop PR only

---

## Step 1: Create PR feature -> contrib [FULL MODE ONLY]

Skip this step in contrib-only mode.

Push the feature branch and create PR:

```bash
# Push feature branch
git push -u origin {feature_branch}

# Create PR
gh pr create \
  --base contrib/stharrold \
  --head {feature_branch} \
  --title "feat: {slug}" \
  --body "## Summary

Feature implementation from v6 workflow.

## Changes

[List key changes]

## Test Plan

- [ ] Feature works as expected
- [ ] No regressions introduced
"
```

**MANUAL GATE**: Wait for PR approval and merge in GitHub UI.

After merge, pull latest:
```bash
git checkout contrib/stharrold
git pull origin contrib/stharrold
```

---

## Step 2: Cleanup Feature Worktree [FULL MODE ONLY]

Skip this step in contrib-only mode.

Extract slug from branch name and cleanup:

```bash
uv run python .claude/skills/git-workflow-manager/scripts/cleanup_feature.py {slug}
```

This removes:
- Feature worktree directory
- Local feature branch
- Remote feature branch

---

## Step 3: Create PR contrib -> develop

Push contrib and create PR to develop:

```bash
# Push contrib
git push origin contrib/stharrold

# Create PR
gh pr create \
  --base develop \
  --head contrib/stharrold \
  --title "merge: contrib/stharrold to develop" \
  --body "## Summary

Integration of latest changes from contrib branch.

## Checklist

- [ ] All features tested
- [ ] No breaking changes
- [ ] Ready for integration
"
```

**MANUAL GATE**: Wait for PR approval and merge in GitHub UI.

---

## Step 4: Record State in AgentDB

```bash
uv run python .claude/skills/agentdb-state-manager/scripts/record_sync.py \
  --sync-type workflow_transition \
  --pattern phase_v6_2_integrate
```

---

## Step 5: Report Completion

Display to user:

```
[OK] Integration complete

{If full mode:}
- Feature PR merged to contrib
- Worktree cleaned up

- Contrib -> develop PR created
- Ready for release when develop has enough changes

Next: Run /workflow:v6_3_release when ready for production
```

---

## Notes

- No quality gates in v6 workflow - feature-dev handles quality
- PRs require manual approval in GitHub UI
- Always ends on contrib/* branch (editable)
