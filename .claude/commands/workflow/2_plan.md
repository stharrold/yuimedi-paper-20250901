---
description: "workflow/1_specify → workflow/2_plan → workflow/3_tasks | Generate design artifacts"
order: 2
prev: /1_specify
next: /3_tasks
---

# /2_plan - Step 2 of 7

**Workflow**: `/1_specify` → `/2_plan` → `/3_tasks` → `/4_implement` → `/5_integrate` → `/6_release` → `/7_backmerge`

**Purpose**: Generate specifications (spec.md, plan.md) from planning documents.

**Prerequisites**:
- Must be in feature worktree (created by `/1_specify`)
- `../planning/{slug}/` must exist with BMAD documents

**Outputs**: `specs/{slug}/spec.md`, `specs/{slug}/plan.md`, AgentDB state record

---

Given the feature context, do this:

## Step 0: Verify Context (REQUIRED - STOP if fails)

**Run this first. If it fails, STOP and tell the user to fix the context.**

```bash
python .claude/skills/workflow-utilities/scripts/verify_workflow_context.py --step 2
```

Expected: Worktree directory, `feature/*` branch

---

## Step 1: Detect Feature Slug

Extract the slug from the current branch name:
```bash
git branch --show-current
```
Branch format: `feature/{timestamp}_{slug}` → extract `{slug}`

## Step 2: Verify Planning Documents

Check that BMAD planning documents exist in the **main repo**:
```bash
ls ../planning/{slug}/requirements.md ../planning/{slug}/architecture.md ../planning/{slug}/epics.md 2>/dev/null
```

If missing, STOP and prompt user to run `/1_specify` first.

## Step 3: Create Specifications

Run the SpecKit author to create specifications:
```bash
podman-compose run --rm dev python .claude/skills/speckit-author/scripts/create_specifications.py \
  feature {slug} stharrold \
  --issue {issue-number}
```

This creates `specs/{slug}/` with:
- `spec.md` - Technical specification
- `plan.md` - Implementation plan with tasks
- `CLAUDE.md` - AI context
- `README.md` - Overview

## Step 4: Record State in AgentDB

Record the workflow transition:
```bash
podman-compose run --rm dev python .claude/skills/agentdb-state-manager/scripts/record_sync.py \
  --sync-type workflow_transition \
  --pattern phase_2_plan \
  --source "../planning/{slug}" \
  --target "specs/{slug}"
```

## Step 5: Report Completion

Report to the user:
- Specifications created at `specs/{slug}/`
- Planning documents referenced from `../planning/{slug}/`
- Next step: Run `/3_tasks` to validate task list

**Important**: Verify `specs/{slug}/plan.md` has a valid task breakdown before proceeding.
