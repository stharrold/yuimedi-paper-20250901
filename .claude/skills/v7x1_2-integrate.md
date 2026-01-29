---
name: v7x1_2-integrate
description: Integrate feature to develop (Step 2 of 4)
---

# /v7x1_2-integrate - Step 2 of 4

**v7x1 Workflow**: `/v7x1_1-worktree` → Implementation → `/v7x1_2-integrate` → `/v7x1_3-release` → `/v7x1_4-backmerge`

**Task**: Integrate feature branch to contrib, then contrib to develop.

**Input**: Feature branch name or worktree path (optional - if empty, runs contrib-only mode)

## Mode Detection

- **Full mode**: Branch argument provided (e.g., `feature/20260126T120000Z_auth`)
  - Runs: feature → contrib PR, worktree cleanup, contrib → develop PR
- **Contrib-only mode**: No argument
  - Runs: contrib → develop PR only

## Step 1: feature → contrib [FULL MODE ONLY]

```bash
git push -u origin {feature_branch}

uv run scripts/secrets_run.py gh pr create \
  --base contrib/stharrold \
  --head {feature_branch} \
  --title "feat: {slug}" \
  --fill
```

**MANUAL GATE**: User merges PR in GitHub UI.

After merge:
```bash
git checkout contrib/stharrold
git pull origin contrib/stharrold
```

## Step 2: Cleanup Feature [FULL MODE ONLY]

```bash
uv run python .gemini/skills/git-workflow-manager/scripts/cleanup_feature.py {slug}
```

Then execute the manual commands it outputs.

## Step 3: contrib → develop

```bash
git push origin contrib/stharrold

uv run scripts/secrets_run.py gh pr create \
  --base develop \
  --head contrib/stharrold \
  --title "merge: contrib/stharrold to develop" \
  --fill
```

**MANUAL GATE**: User merges PR in GitHub UI.

## Step 4: Report Completion

```
✓ Integration complete

- Feature merged to contrib (if full mode)
- Worktree cleaned (if full mode)
- Contrib → develop PR created

Next: /v7x1_3-release when ready for production
```

## Reference

Full documentation: `.claude/skills/v7x1-workflow.md`
