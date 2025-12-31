---
description: "(start) → workflow/1_specify → workflow/2_plan | Create feature spec"
order: 1
next: /2_plan
---

# /1_specify - Step 1 of 7

**Workflow**: `/1_specify` → `/2_plan` → `/3_tasks` → `/4_implement` → `/5_integrate` → `/6_release` → `/7_backmerge`

**Purpose**: Create feature planning documents and worktree from natural language description.

**Prerequisites**: None (this is the starting point)

**Outputs**: `planning/{slug}/`, worktree at `../{project}_feature_{slug}/`, AgentDB state record

---

Given the feature description provided as an argument, do this:

## Step 0: Verify Context (REQUIRED - STOP if fails)

**Run this first. If it fails, STOP and tell the user to fix the context.**

```bash
python .claude/skills/workflow-utilities/scripts/verify_workflow_context.py --step 1
```

Expected: Main repo, `contrib/*` branch

---

## Step 1: Extract Feature Slug

Parse the feature description to create a kebab-case slug (e.g., "add user authentication" → "user-authentication").

## Step 2: Create GitHub Issue (Optional)

Ask the user if they want to create a GitHub Issue:
```bash
gh issue create --title "Feature: {description}" --label "feature"
```

Note the issue number for later use.

## Step 3: Create Planning Documents

Run the BMAD planner to create planning documents:
```bash
podman-compose run --rm dev python .claude/skills/bmad-planner/scripts/create_planning.py \
  --slug {slug} \
  --issue {issue-number}
```

This creates `planning/{slug}/` with:
- `requirements.md` - Functional requirements and user stories
- `architecture.md` - Technical architecture
- `epics.md` - Epic breakdown

## Step 4: Create Feature Worktree

Create an isolated worktree for development (no TODO file):
```bash
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature {slug} contrib/stharrold \
  --no-todo
```

This creates:
- Branch: `feature/{timestamp}_{slug}`
- Worktree: `../{project}_feature_{timestamp}_{slug}/`
- State directory: `.claude-state/` in worktree

## Step 5: Record State in AgentDB

Record the workflow transition:
```bash
podman-compose run --rm dev python .claude/skills/agentdb-state-manager/scripts/record_sync.py \
  --sync-type workflow_transition \
  --pattern phase_1_specify \
  --source "planning/{slug}" \
  --target "worktree"
```

## Step 6: Report Completion

Report to the user:
- Planning documents created at `planning/{slug}/`
- Worktree created at `../{project}_feature_{slug}/`
- Branch name: `feature/{timestamp}_{slug}`
- GitHub Issue: #{issue-number} (if created)
- Next step: `cd` to worktree and run `/2_plan`

**Important**: Prompt the user to change directory to the worktree before continuing.
