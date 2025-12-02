---
description: "workflow/3_tasks → workflow/4_implement → workflow/5_integrate | Execute tasks automatically"
order: 4
prev: /3_tasks
next: /5_integrate
---

# /4_implement - Step 4 of 7

**Workflow**: `/1_specify` → `/2_plan` → `/3_tasks` → `/4_implement` → `/5_integrate` → `/6_release` → `/7_backmerge`

**Purpose**: Execute tasks from plan.md/tasks.md automatically with progress tracking.

**Prerequisites**:
- Must be in feature worktree
- Tasks validated (from `/3_tasks`)

**Outputs**: Implemented feature, quality gates passed, AgentDB state record

**Next**: Run `/5_integrate` to create PRs and integrate feature

---

Execute tasks automatically. User can stop/rewind via Claude Code controls at any time.

## Step 0: Verify Context (REQUIRED - STOP if fails)

**Run this first. If it fails, STOP and tell the user to fix the context.**

```bash
python .claude/skills/workflow-utilities/scripts/verify_workflow_context.py --step 4
```

Expected: Worktree directory, `feature/*` branch

---

## Step 1: Verify Task Artifacts

Extract slug from branch (`feature/{timestamp}_{slug}`) and verify task artifacts exist:
```bash
ls specs/{slug}/plan.md specs/{slug}/tasks.md 2>/dev/null
```

If artifacts missing, STOP and prompt user to run `/2_plan` and `/3_tasks` first.

## Step 2: Load Tasks

Load tasks from `specs/{slug}/plan.md` or `specs/{slug}/tasks.md`:
- Extract all tasks (T001, T002, etc.)
- Identify task dependencies
- Identify [P] marked tasks that can run in parallel

## Step 3: Initialize Progress Tracking

Initialize TodoWrite with all tasks from the plan.

## Step 4: Execute Tasks

Execute tasks in dependency order:
1. For each task:
   - Mark task as `in_progress` in TodoWrite
   - Execute the task instructions
   - Mark task as `completed` when done
   - If task fails, keep as `in_progress` and report error
2. Run [P] marked tasks in parallel using Task tool when dependencies allow

## Step 5: Run Quality Gates

After all tasks complete, run quality gates:
```bash
podman-compose run --rm dev python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

Quality gates must pass (5/5):
1. Test coverage ≥80%
2. All tests passing
3. Build successful
4. Linting clean
5. AI config sync

## Step 6: Calculate Semantic Version

Calculate the next version based on changes:
```bash
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  develop v{current-version}
```

## Step 7: Record State in AgentDB

Record the workflow transition:
```bash
podman-compose run --rm dev python .claude/skills/agentdb-state-manager/scripts/record_sync.py \
  --sync-type quality_gate \
  --pattern phase_4_implement
```

## Step 8: Report Completion

Report to the user:
- All tasks completed
- Quality gates passed (5/5)
- Semantic version calculated
- Next step: Run `/5_integrate` to create PRs

## Error Handling

- If a task fails, stop and report the error
- User can fix the issue and resume
- Use TodoWrite to track which tasks are complete
- Never skip a task unless explicitly told to

## Step 9: Commit and Push All Changes

**After all tasks complete and quality gates pass, finalize the work:**

1. Stage all changes:
   ```bash
   git add .
   ```

2. Commit with implementation summary:
   ```bash
   git commit -m "feat({slug}): implement feature per plan.md

   Implemented tasks from specs/{slug}/plan.md.
   Quality gates passed (5/5).

   Refs: #{issue-number}"
   ```

3. Push to remote:
   ```bash
   git push
   ```

## Step 10: Next Steps (User Action Required)

**IMPORTANT: You must switch to the main repository before running `/5_integrate`.**

The `/5_integrate` step must run from the **main repository** on the `contrib/*` branch, NOT from this worktree.

**Instructions:**

1. Return to the main repository:
   ```bash
   cd /path/to/main/repo
   ```
   (The main repo path is the parent directory name without the `_feature_*` suffix)

2. Ensure you're on the contrib branch:
   ```bash
   git checkout contrib/stharrold
   ```

3. Then run the next step:
   ```
   /5_integrate
   ```

**Why?** Step 5 creates PRs and cleans up the worktree, which must be done from outside the worktree itself.
