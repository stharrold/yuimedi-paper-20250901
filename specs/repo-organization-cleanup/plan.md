# Implementation Plan: Repo Organization Cleanup

**Type:** feature
**Slug:** repo-organization-cleanup
**Issue:** #243
**Date:** 2025-11-29

## Task Breakdown

### Phase 1: Preparation

#### Task impl_001: Verify archived files exist

**Priority:** High

**Files:**
- `ARCHIVED/TODO/TODO_FOR_AI.json`
- `ARCHIVED/TODO/TODO_FOR_HUMAN.md`

**Description:**
Confirm that deprecated TODO files have been properly archived before removal from root.

**Steps:**
1. Check `ARCHIVED/TODO/` directory exists
2. Verify `TODO_FOR_AI.json` is present in archive
3. Verify `TODO_FOR_HUMAN.md` is present in archive

**Acceptance Criteria:**
- [ ] ARCHIVED/TODO/ directory exists
- [ ] TODO_FOR_AI.json archived
- [ ] TODO_FOR_HUMAN.md archived

**Verification:**
```bash
ls -la ARCHIVED/TODO/
```

**Dependencies:**
- None

---

### Phase 2: File Removal

#### Task impl_002: Remove deprecated root files

**Priority:** High

**Files:**
- `TODO_FOR_AI.json` (remove)
- `TODO_FOR_HUMAN.md` (remove)

**Description:**
Remove deprecated TODO files from root directory. These have already been migrated to GitHub Issues and archived in ARCHIVED/TODO/.

**Steps:**
1. git rm TODO_FOR_AI.json
2. git rm TODO_FOR_HUMAN.md
3. Verify files removed from root

**Acceptance Criteria:**
- [ ] TODO_FOR_AI.json removed from root
- [ ] TODO_FOR_HUMAN.md removed from root
- [ ] git status shows expected changes

**Verification:**
```bash
git status
ls TODO_FOR_AI.json TODO_FOR_HUMAN.md 2>/dev/null && echo "FAILED" || echo "OK - files removed"
```

**Dependencies:**
- impl_001

---

### Phase 3: .agents/ Cleanup

#### Task impl_003: Audit .agents/ structure

**Priority:** High

**Files:**
- `.agents/`

**Description:**
Examine current .agents/ directory structure to identify duplicate nested structure.

**Steps:**
1. List all directories in .agents/
2. Check for .agents/skills/ duplicate directory
3. Document current structure

**Acceptance Criteria:**
- [ ] Current structure documented
- [ ] Duplicate .agents/skills/ identified (if exists)

**Verification:**
```bash
find .agents/ -type d -maxdepth 2
ls -la .agents/skills/ 2>/dev/null && echo "DUPLICATE EXISTS" || echo "NO DUPLICATE"
```

**Dependencies:**
- None (can run in parallel with Phase 2)

---

#### Task impl_004: Remove duplicate .agents/skills/

**Priority:** High

**Files:**
- `.agents/skills/` (remove if exists)

**Description:**
Remove the nested duplicate .agents/skills/ directory if it exists. The correct structure should have skills directly under .agents/ (e.g., .agents/workflow-orchestrator/).

**Steps:**
1. Check if .agents/skills/ exists
2. If exists, remove rm -rf .agents/skills/
3. Verify only flat structure remains

**Acceptance Criteria:**
- [ ] .agents/skills/ directory removed (if existed)
- [ ] .agents/ contains only flat skill mirrors

**Verification:**
```bash
ls -la .agents/
# Should show: agentdb-state-manager/, bmad-planner/, commands/, etc. (no skills/)
```

**Dependencies:**
- impl_003

---

### Phase 4: Sync Script Verification

#### Task impl_005: Review sync_ai_config.py

**Priority:** Medium

**Files:**
- `.claude/skills/workflow-utilities/scripts/sync_ai_config.py`

**Description:**
Review the AI config sync script to ensure it creates the correct flat structure and won't recreate the nested .agents/skills/ directory.

**Steps:**
1. Read sync_ai_config.py
2. Verify rsync command targets flat structure
3. Update if necessary

**Acceptance Criteria:**
- [ ] Script reviewed
- [ ] Sync creates flat .agents/skill-name/ structure
- [ ] No risk of recreating .agents/skills/

**Verification:**
```bash
grep -A 5 "rsync" .claude/skills/workflow-utilities/scripts/sync_ai_config.py
```

**Dependencies:**
- impl_004

---

#### Task impl_006: Update CLAUDE.md if needed

**Priority:** Medium

**Files:**
- `CLAUDE.md`

**Description:**
Verify CLAUDE.md sync commands are correct and update any references to deprecated files.

**Steps:**
1. Check AI Config Sync section
2. Verify rsync commands are correct
3. Remove any references to TODO_FOR_AI.json or TODO_FOR_HUMAN.md

**Acceptance Criteria:**
- [ ] Sync commands verified correct
- [ ] No references to deprecated files

**Verification:**
```bash
grep -n "TODO_FOR_AI\|TODO_FOR_HUMAN" CLAUDE.md && echo "NEEDS UPDATE" || echo "OK"
```

**Dependencies:**
- impl_002

---

### Phase 5: Validation

#### Task test_001: Run documentation validation

**Priority:** High

**Files:**
- `validate_documentation.sh`

**Description:**
Run all documentation validation tests to ensure changes haven't broken anything.

**Steps:**
1. Run ./validate_documentation.sh
2. Fix any failures

**Acceptance Criteria:**
- [ ] All 5 validation tests pass

**Verification:**
```bash
./validate_documentation.sh
```

**Dependencies:**
- impl_002, impl_004, impl_006

---

#### Task test_002: Run pre-commit hooks

**Priority:** High

**Description:**
Run pre-commit hooks to ensure all formatting and sync checks pass.

**Steps:**
1. Run uv run pre-commit run --all-files
2. Fix any failures

**Acceptance Criteria:**
- [ ] All pre-commit hooks pass

**Verification:**
```bash
uv run pre-commit run --all-files
```

**Dependencies:**
- test_001

---

## Task Summary

| Task ID | Description | Priority | Dependencies |
|---------|-------------|----------|--------------|
| impl_001 | Verify archived files exist | High | None |
| impl_002 | Remove deprecated root files | High | impl_001 |
| impl_003 | Audit .agents/ structure | High | None |
| impl_004 | Remove duplicate .agents/skills/ | High | impl_003 |
| impl_005 | Review sync_ai_config.py | Medium | impl_004 |
| impl_006 | Update CLAUDE.md if needed | Medium | impl_002 |
| test_001 | Run documentation validation | High | impl_002, impl_004, impl_006 |
| test_002 | Run pre-commit hooks | High | test_001 |

## Task Dependencies Graph

```
impl_001 ─> impl_002 ─────────────────────┐
                                          │
impl_003 ─> impl_004 ─> impl_005          ├─> test_001 ─> test_002
                                          │
                    ─> impl_006 ──────────┘
```

## Parallel Work Opportunities

- impl_001/impl_002 can run in parallel with impl_003/impl_004
- impl_005 and impl_006 can run in parallel after their dependencies

## Quality Checklist

Before considering this feature complete:

- [ ] All tasks marked as complete
- [ ] Documentation validation passes
- [ ] Pre-commit hooks pass
- [ ] Root file count reduced (TODO files removed)
- [ ] .agents/ has correct flat structure
- [ ] No references to deprecated files in documentation
