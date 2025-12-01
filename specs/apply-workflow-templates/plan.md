# Implementation Plan: Apply Workflow Templates

**Type:** feature
**Slug:** apply-workflow-templates
**Date:** 2025-12-01
**GitHub Issue:** #248

## Overview

Sync workflow skills and commands from `.tmp/stharrold-templates/` to update the repository's workflow automation with the latest improvements to AgentDB, git workflows, quality gates, and VCS abstraction.

## Task Breakdown

### Epic 1: Backup Current Skills

#### Task T001: Create Backup Archive

**Priority:** High
**Estimate:** 5 min

**Description:**
Create a timestamped backup of current `.claude/skills/` before making changes.

**Steps:**
1. Verify ARCHIVED/ directory exists
2. Create zip archive with timestamp prefix
3. Verify backup integrity

**Commands:**
```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  pre-template-sync-backup \
  .claude/skills/
```

**Acceptance Criteria:**
- [ ] Backup zip exists in ARCHIVED/
- [ ] Backup contains all 9 skill directories

---

### Epic 2: Sync Skills Directory

#### Task T002: Sync Skills from Template

**Priority:** High
**Estimate:** 10 min
**Dependencies:** T001

**Description:**
Copy updated Python scripts from template to local skills directory.

**Steps:**
1. Verify template source exists at `.tmp/stharrold-templates/.claude/skills/`
2. Run rsync with proper exclusions
3. Verify all 9 skills synced

**Commands:**
```bash
rsync -av --delete \
  --exclude=".DS_Store" \
  --exclude="__pycache__" \
  --exclude="*.pyc" \
  .tmp/stharrold-templates/.claude/skills/ \
  .claude/skills/
```

**Acceptance Criteria:**
- [ ] All 9 skill directories updated
- [ ] No .DS_Store or __pycache__ copied
- [ ] File permissions preserved

**Skills to verify:**
1. agentdb-state-manager
2. bmad-planner
3. git-workflow-manager
4. initialize-repository
5. quality-enforcer
6. speckit-author
7. tech-stack-adapter
8. workflow-orchestrator
9. workflow-utilities

---

### Epic 3: Sync Commands Directory

#### Task T003: Sync Workflow Commands

**Priority:** High
**Estimate:** 5 min
**Dependencies:** T002

**Description:**
Copy updated workflow slash commands from template.

**Steps:**
1. Verify template commands exist
2. Run rsync for commands directory
3. Verify all 8 workflow commands present

**Commands:**
```bash
rsync -av --delete \
  --exclude=".DS_Store" \
  .tmp/stharrold-templates/.claude/commands/workflow/ \
  .claude/commands/workflow/
```

**Acceptance Criteria:**
- [ ] All workflow commands updated
- [ ] 1_specify.md through 7_backmerge.md present
- [ ] all.md present

---

### Epic 4: Sync .agents Directory

#### Task T004: Mirror to .agents Directory

**Priority:** Medium
**Estimate:** 5 min
**Dependencies:** T002, T003

**Description:**
Mirror updated skills and commands to .agents/ for cross-tool compatibility.

**Steps:**
1. Sync skills to .agents/
2. Sync commands to .agents/commands/
3. Verify mirror consistency

**Commands:**
```bash
rsync -av --delete \
  --exclude=".DS_Store" \
  --exclude="__pycache__" \
  .claude/skills/ .agents/

rsync -av --delete \
  --exclude=".DS_Store" \
  .claude/commands/ .agents/commands/
```

**Acceptance Criteria:**
- [ ] .agents/ mirrors .claude/skills/
- [ ] .agents/commands/ mirrors .claude/commands/

---

### Epic 5: Validate and Test

#### Task T005: Run Pre-commit Hooks

**Priority:** High
**Estimate:** 5 min
**Dependencies:** T004

**Description:**
Run pre-commit hooks to validate all changes.

**Commands:**
```bash
uv run pre-commit run --all-files
```

**Acceptance Criteria:**
- [ ] All hooks pass
- [ ] No formatting issues
- [ ] CLAUDE.md frontmatter valid

---

#### Task T006: Run Quality Gates

**Priority:** High
**Estimate:** 5 min
**Dependencies:** T005

**Description:**
Run all 6 quality gates to ensure updates don't break functionality.

**Commands:**
```bash
uv run python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

**Acceptance Criteria:**
- [ ] Gate 1: Documentation validation passes
- [ ] Gate 2: Linting passes (ruff check)
- [ ] Gate 3: Type checking passes (mypy)
- [ ] Gate 4: Coverage passes (or skipped if no tests)
- [ ] Gate 5: Tests pass (or skipped if no tests)
- [ ] Gate 6: Build succeeds

---

#### Task T007: Run Documentation Validation

**Priority:** Medium
**Estimate:** 5 min
**Dependencies:** T005

**Description:**
Run documentation validation scripts.

**Commands:**
```bash
./validate_documentation.sh
```

**Acceptance Criteria:**
- [ ] File size check passes
- [ ] Cross-references valid
- [ ] No content duplication
- [ ] Command syntax valid
- [ ] YAML structure valid

---

#### Task T008: Verify Python Imports

**Priority:** High
**Estimate:** 5 min
**Dependencies:** T006

**Description:**
Test that key Python scripts can be imported without errors.

**Commands:**
```bash
uv run python -c "import sys; sys.path.insert(0, '.claude/skills'); from workflow_utilities.scripts import deprecate_files; print('OK')"
uv run python -c "from pathlib import Path; exec(Path('.claude/skills/quality-enforcer/scripts/run_quality_gates.py').read_text()[:100]); print('OK')"
```

**Acceptance Criteria:**
- [ ] No import errors
- [ ] No syntax errors
- [ ] Scripts executable

---

## Task Summary

| Task | Description | Priority | Estimate | Dependencies |
|------|-------------|----------|----------|--------------|
| T001 | Create backup archive | High | 5 min | - |
| T002 | Sync skills from template | High | 10 min | T001 |
| T003 | Sync workflow commands | High | 5 min | T002 |
| T004 | Mirror to .agents directory | Medium | 5 min | T002, T003 |
| T005 | Run pre-commit hooks | High | 5 min | T004 |
| T006 | Run quality gates | High | 5 min | T005 |
| T007 | Run documentation validation | Medium | 5 min | T005 |
| T008 | Verify Python imports | High | 5 min | T006 |

**Total Estimated Time:** ~45 minutes

## Task Dependencies Graph

```
T001 (backup)
  │
  v
T002 (sync skills)
  │
  ├──> T003 (sync commands)
  │      │
  │      v
  └────> T004 (mirror .agents) <─┘
           │
           v
         T005 (pre-commit)
           │
           ├──> T006 (quality gates) ──> T008 (verify imports)
           │
           └──> T007 (doc validation)
```

## Parallel Opportunities

- T006 and T007 can run in parallel after T005
- None of the sync tasks can be parallelized (sequential dependency)

## Quality Checklist

Before considering this feature complete:

- [ ] All 8 tasks marked complete
- [ ] Backup exists in ARCHIVED/
- [ ] All 9 skills synced
- [ ] All 8 workflow commands synced
- [ ] .agents/ directory in sync
- [ ] Pre-commit hooks pass
- [ ] All 6 quality gates pass
- [ ] Documentation validation passes
- [ ] No Python import errors
