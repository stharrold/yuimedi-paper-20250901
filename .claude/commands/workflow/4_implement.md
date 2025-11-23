---
description: "workflow/3_tasks → workflow/4_implement → workflow/5_integrate | Execute tasks automatically"
order: 4
prev: /3_tasks
next: /5_integrate
---

# /4_implement - Step 4 of 7

**Workflow**: `/1_specify` → `/2_plan` → `/3_tasks` → `/4_implement` → `/5_integrate` → `/6_release` → `/7_backmerge`

**Purpose**: Execute tasks from tasks.md automatically with progress tracking.

**Prerequisites**: `tasks.md` must exist (created by `/3_tasks`)

**Outputs**: Implemented feature, completed tasks, quality gates passed

**Next**: Run `/5_integrate` to create PRs and integrate feature

---

Execute tasks from tasks.md automatically. User can stop/rewind via Claude Code controls at any time.

## Execution Flow

1. Run `.specify/scripts/bash/check-task-prerequisites.sh --json` from repo root and parse FEATURE_DIR.
2. Load and parse `FEATURE_DIR/tasks.md`:
   - Extract all tasks (T001, T002, etc.)
   - Identify task dependencies from the Dependencies section
   - Identify [P] marked tasks that can run in parallel
3. Initialize TodoWrite with all tasks from tasks.md
4. Execute tasks in dependency order:
   - **Phase 3.1 Setup**: Create directories, initialize project
   - **Phase 3.2 Tests**: Write failing tests first (TDD)
   - **Phase 3.3 Core**: Implement models, services, commands
   - **Phase 3.4 Integration**: Connect components, add middleware
   - **Phase 3.5 Polish**: Unit tests, docs, cleanup
5. For each task:
   - Mark task as `in_progress` in TodoWrite
   - Execute the task instructions
   - Mark task as `completed` when done
   - If task fails, keep as `in_progress` and report error
6. Run [P] marked tasks in parallel using Task tool when dependencies allow
7. After all tasks complete, run quality gates:
   ```bash
   podman-compose run --rm dev python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
   ```
8. Report completion and readiness for `/5_integrate`

## Task Parsing Rules

- Tasks are numbered: `T001`, `T002`, etc.
- `[P]` suffix means task can run in parallel with other [P] tasks
- Tasks without [P] must run sequentially
- Dependencies are listed in the Dependencies section
- Each task has a description and file path

## Error Handling

- If a task fails, stop and report the error
- User can fix the issue and resume
- Use TodoWrite to track which tasks are complete
- Never skip a task unless explicitly told to

## Quality Gates (must pass before /5_integrate)

1. Test coverage ≥80%
2. All tests passing
3. Build successful
4. Linting clean
5. TODO*.md YAML frontmatter valid
6. AI config sync

## Example

```
Loading tasks.md...
Found 12 tasks: T001-T012

[T001] Creating workflow directory... ✓
[T002-T006] Creating command files (parallel)... ✓
[T007] Updating CLAUDE.md... ✓
[T008-T011] Removing old files (parallel)... ✓
[T012] Running verification... ✓

Running quality gates...
All gates passed ✓

Ready for /5_integrate
```
