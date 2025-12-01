---
description: "workflow/2_plan → workflow/3_tasks → workflow/4_implement | Generate task list"
order: 3
prev: /2_plan
next: /4_implement
---

# /3_tasks - Step 3 of 7

**Workflow**: `/1_specify` → `/2_plan` → `/3_tasks` → `/4_implement` → `/5_integrate` → `/6_release` → `/7_backmerge`

**Purpose**: Validate task list from plan.md and prepare for implementation.

**Prerequisites**:
- Must be in feature worktree
- `specs/{slug}/plan.md` must exist with ## Tasks section (created by `/2_plan`)

**Outputs**: Validated task list ready for execution, AgentDB state record

**Next**: Run `/4_implement` to execute tasks automatically

---

Given the feature context, do this:

## Step 0: Verify Context (REQUIRED - STOP if fails)

**Run this first. If it fails, STOP and tell the user to fix the context.**

```bash
python .claude/skills/workflow-utilities/scripts/verify_workflow_context.py --step 3
```

Expected: Worktree directory, `feature/*` branch

---

## Step 1: Detect Feature Slug and Locate Plan File

Extract slug from branch (`feature/{timestamp}_{slug}`) and find plan at `specs/{slug}/plan.md`.

If plan file missing, STOP and prompt user to run `/2_plan` first.

## Step 2: Validate Task Structure

Read `specs/{slug}/plan.md` and verify it contains:
- A `## Tasks` or `## Task Breakdown` section
- Numbered tasks (T001, T002, etc. or similar format)
- Clear task descriptions with file paths

If tasks are missing or incomplete:
- Check `specs/{slug}/tasks.md` as an alternative location
- If no tasks found, prompt user to complete the plan first

## Step 3: Parse and Display Tasks

Parse the tasks from plan.md and display:
- Total task count
- Task categories (setup, implementation, testing, documentation)
- Parallel execution opportunities (tasks marked [P])
- Dependencies between tasks

## Step 4: Record State in AgentDB

Record the workflow transition:
```bash
podman-compose run --rm dev python .claude/skills/agentdb-state-manager/scripts/record_sync.py \
  --sync-type workflow_transition \
  --pattern phase_3_tasks \
  --source "specs/{slug}/plan.md"
```

## Step 5: Report Readiness

Report to the user:
- Tasks validated and ready for execution
- Task summary (count, categories, parallel opportunities)
- Next step: Run `/4_implement` to execute tasks

**Important**: The task list must be complete and unambiguous before proceeding to implementation.
