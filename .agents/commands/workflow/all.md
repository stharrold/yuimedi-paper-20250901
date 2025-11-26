---
description: "Orchestrate full workflow | Run steps 1-7 with manual gate pauses"
order: 0
---

# /workflow/all - Workflow Orchestrator

**Workflow**: `/1_specify` → `/2_plan` → `/3_tasks` → `/4_implement` → `/5_integrate` → `/6_release` → `/7_backmerge`

**Purpose**: Orchestrate the complete workflow, automatically detecting state and pausing at manual gates.

---

## Modes

| Mode | Syntax | Description |
|------|--------|-------------|
| Default | `/workflow/all` | Detect state, continue from current step |
| New | `/workflow/all new "description"` | Start fresh from step 1 |
| Release | `/workflow/all release` | Run steps 6-7 only |
| Continue | `/workflow/all continue` | Resume after manual gate |

---

## Execution Instructions

Given the arguments provided, execute the workflow orchestration:

### Step 1: Parse Mode from Arguments

Parse `$ARGUMENTS` to determine mode:
- If starts with `new `: Extract description (strip surrounding quotes from text after "new"), set MODE=new
- If equals `release`: Set MODE=release
- If equals `continue`: Set MODE=continue
- Otherwise: Set MODE=default (auto-detect)

### Step 2: Detect Current State

#### 2a. Query AgentDB for Workflow State

Run state query to get last known phase:
```bash
podman-compose run --rm dev python .claude/skills/agentdb-state-manager/scripts/query_workflow_state.py \
  --format json
```

Parse the result for:
- `phase`: Last completed phase number (0-7)
- `phase_name`: Human-readable phase name
- `next_command`: Suggested next slash command
- `pattern`: Last recorded sync pattern

#### 2b. Detect Branch Type

Run git detection:
```bash
git branch --show-current
```

Determine branch type:
- Pattern `^feature/` → BRANCH_TYPE=feature (in worktree)
- Pattern `^contrib/` → BRANCH_TYPE=contrib (main repo)
- Pattern `^develop$` → BRANCH_TYPE=develop
- Pattern `^release/` → BRANCH_TYPE=release
- Pattern `^main$` → BRANCH_TYPE=main

### Step 3: Check Artifact Existence

For feature branches, check which artifacts exist:
- `planning/{slug}/` exists → PLANNING_EXISTS=true
- `specs/{slug}/spec.md` exists → SPEC_EXISTS=true
- `specs/{slug}/plan.md` with tasks → TASKS_EXISTS=true

Report detected state:
```
Detected state:
  Branch: {branch} ({branch_type})
  AgentDB Phase: {phase} ({phase_name})
  Next Command: {next_command}
  Artifacts: {list of existing artifacts}
```

### Step 4: Execute Based on Mode

#### MODE=new
1. Validate: Description must not be empty
   - If empty: Report error "Usage: /workflow/all new \"feature description\""
2. Report: `[▶] Starting new feature workflow`
3. Invoke: `/workflow:1_specify {description}`
4. Invoke: `/workflow:2_plan`
5. Invoke: `/workflow:3_tasks`
6. Invoke: `/workflow:4_implement`
7. Invoke: `/workflow:5_integrate`
8. → PAUSE at manual gate (see Step 5)

#### MODE=release
1. Validate: Branch must be `contrib/*` or `develop`
   - If not: Report error "Release mode requires contrib/* or develop branch"
2. Report: `[▶] Starting release workflow`
3. Invoke: `/workflow:6_release`
4. → PAUSE at manual gate (see Step 5) - wait for release→main PR merge
   - Instruct user: "After release→main PR is merged, run `/workflow/all continue`"

*(User runs `/workflow/all continue` after merging release→main PR)*

5. Invoke: `/workflow:7_backmerge`
6. → PAUSE at manual gate (see Step 5) - wait for release→develop PR merge
   - Instruct user: "After release→develop PR is merged, run `/workflow/all continue`"
7. Report completion

#### MODE=continue
1. Check PR status: `gh pr list --state open --head {branch}`
2. If PRs still open:
   - Report: "Waiting for PR merges"
   - List open PRs with URLs
   - Remain paused
3. If PRs merged:
   - Use the state matrix from MODE=default (see below) to determine the next step based on branch type and artifact existence
   - Continue execution from the determined step

#### MODE=default (auto-detect)
1. Use AgentDB phase + branch type to determine starting step:

| AgentDB Phase | Branch Type | Start From |
|---------------|-------------|------------|
| 0 (not_started) | any | Step 1 (/1_specify) |
| 1 (specify) | feature | Step 2 (/2_plan) |
| 2 (plan) | feature | Step 3 (/3_tasks) |
| 3 (tasks) | feature | Step 4 (/4_implement) |
| 4 (implement) | feature | Step 5 (/5_integrate) |
| 5 (integrate) | contrib | Step 6 (/6_release) or suggest |
| 6 (release) | any | Step 7 (/7_backmerge) |
| 7 (backmerge) | contrib | Workflow complete |

Fallback to artifact detection if AgentDB is unavailable:

| Branch Type | Artifacts | Start From |
|-------------|-----------|------------|
| feature | no planning | Step 1 (/1_specify) |
| feature | planning only | Step 2 (/2_plan) |
| feature | specs exist | Step 3 (/3_tasks) |
| contrib | - | Step 6 (/6_release) |
| main | - | Suggest: `/workflow/all new "description"` |

2. Report: `Starting from: Step {N} (/{N}_command) [from AgentDB: phase {phase}]`
3. Execute steps in sequence until manual gate or completion

### Step 5: Manual Gate Handling

After `/5_integrate`, `/6_release`, or `/7_backmerge` (pr-develop step), pause and report:
```
⏸ PAUSED: Manual gate reached

PRs created (merge these in GitHub):
  • {PR URL 1}
  • {PR URL 2}

After merging, run:
  /workflow/all continue
```

### Step 6: Progress Output

Use these indicators throughout:
- `[▶] Step N: /N_command` - Starting step
- `[✓] Step N: Complete` - Step finished successfully
- `[✗] Step N: Failed` - Step failed (stop execution)
- `⏸ PAUSED` - At manual gate

### Step 7: Error Handling

On any step failure:
1. Stop execution immediately
2. Report:
```
[✗] Step {N} failed: /{N}_command

Error: {error message}

To retry: /workflow/all
(To skip a step, manually resolve the issue and re-run the command)
```

### Step 8: Completion

When all steps complete:
```
✓ Workflow complete!

Summary:
  • Feature: {feature-name}
  • Branch: {current-branch}
  • Steps completed: {list}

Next: Start new feature with /workflow/all new "description"
```

---

## Quick Reference

```bash
# Start new feature
/workflow/all new "implement user authentication"

# Continue after PR merge
/workflow/all continue

# Release to production
/workflow/all release

# Auto-detect and continue
/workflow/all
```
