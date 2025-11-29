# Implementation Plan: Apply Workflow Templates

**Type:** feature
**Slug:** apply-workflow-templates
**Date:** 2025-11-28
**GitHub Issue:** #239

## Task Breakdown

### Phase 1: Preparation

#### Task E1_001: Backup Current Skills

**Priority:** High

**Description:**
Create a timestamped backup of current skills directory before syncing.

**Steps:**
1. Create ARCHIVED/ directory if not exists
2. Create timestamped zip backup of `.claude/skills/`
3. Verify backup integrity

**Verification:**
```bash
ls -la ARCHIVED/*.zip
unzip -l ARCHIVED/*skills-backup.zip | head -20
```

**Acceptance Criteria:**
- [ ] Backup zip exists in ARCHIVED/
- [ ] Backup contains all skill directories

---

### Phase 2: Sync Operations

#### Task E2_001: Sync Skills Directory

**Priority:** High

**Description:**
Copy updated Python scripts from template skills to local skills.

**Steps:**
1. Run rsync from template skills to local skills
2. Exclude .DS_Store and __pycache__
3. Verify all 9 skills synced

**Verification:**
```bash
rsync -av --delete \
  --exclude=".DS_Store" \
  --exclude="__pycache__" \
  --exclude="*.pyc" \
  .tmp/stharrold-templates/.claude/skills/ .claude/skills/
ls -la .claude/skills/
```

**Acceptance Criteria:**
- [ ] All 9 skill directories updated
- [ ] No .DS_Store or __pycache__ copied
- [ ] File permissions preserved

**Dependencies:**
- E1_001 (backup must complete first)

---

#### Task E3_001: Sync Commands Directory

**Priority:** High

**Description:**
Copy updated workflow commands from template to local.

**Steps:**
1. Run rsync from template commands to local commands
2. Verify workflow commands updated

**Verification:**
```bash
rsync -av --delete \
  --exclude=".DS_Store" \
  .tmp/stharrold-templates/.claude/commands/ .claude/commands/
ls -la .claude/commands/workflow/
```

**Acceptance Criteria:**
- [ ] 2_plan.md updated
- [ ] 5_integrate.md updated
- [ ] All other commands intact

**Dependencies:**
- E1_001 (backup must complete first)

---

#### Task E4_001: Sync .agents Directory

**Priority:** Medium

**Description:**
Mirror updated skills to .agents/ directory for cross-tool compatibility.

**Steps:**
1. Run rsync from template .agents to local .agents
2. Verify mirror consistency

**Verification:**
```bash
rsync -av --delete \
  --exclude=".DS_Store" \
  --exclude="__pycache__" \
  .tmp/stharrold-templates/.agents/ .agents/
diff -rq .claude/skills/ .agents/ 2>/dev/null | grep -v "__pycache__" | head -10
```

**Acceptance Criteria:**
- [ ] .agents/ mirrors .claude/skills/
- [ ] No Claude-specific files in .agents/

**Dependencies:**
- E2_001 (skills sync must complete first)

---

### Phase 3: Validation

#### Task E5_001: Run Pre-commit Hooks

**Priority:** High

**Description:**
Run pre-commit hooks to ensure code quality.

**Steps:**
1. Run pre-commit hooks on all files
2. Fix any formatting issues
3. Re-run to verify clean

**Verification:**
```bash
uv run pre-commit run --all-files
```

**Acceptance Criteria:**
- [ ] All hooks pass
- [ ] No manual intervention required

**Dependencies:**
- E2_001, E3_001, E4_001 (all syncs complete)

---

#### Task E5_002: Run Quality Gates

**Priority:** High

**Description:**
Run all 6 quality gates to ensure updates don't break functionality.

**Steps:**
1. Run quality-enforcer script
2. Review any failures
3. Fix issues if needed

**Verification:**
```bash
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

**Acceptance Criteria:**
- [ ] Gate 1: Documentation validation passes
- [ ] Gate 2: Linting clean
- [ ] Gate 3: Type checking passes
- [ ] Gate 4: Coverage (auto-pass, no tests)
- [ ] Gate 5: Tests (auto-pass, no tests)
- [ ] Gate 6: Build succeeds

**Dependencies:**
- E5_001 (pre-commit hooks must pass first)

---

#### Task E5_003: Verify Python Imports

**Priority:** Medium

**Description:**
Test that key Python scripts can be imported without errors.

**Steps:**
1. Try importing key modules
2. Verify no missing dependencies
3. Fix any import errors

**Verification:**
```bash
python -c "import sys; sys.path.insert(0, '.claude/skills'); print('OK')"
python -c "from pathlib import Path; exec(Path('.claude/skills/workflow-utilities/scripts/validate_versions.py').read_text()[:100]); print('Syntax OK')"
```

**Acceptance Criteria:**
- [ ] No import errors
- [ ] No syntax errors
- [ ] All scripts executable

**Dependencies:**
- E2_001 (skills sync complete)

---

## Task Dependencies Graph

```
E1_001 (Backup) ─┐
                 ├─> E2_001 (Skills) ─┐
                 ├─> E3_001 (Commands) ├─> E5_001 (Pre-commit) ─> E5_002 (Quality Gates)
                 └─> E4_001 (.agents) ─┘                       └─> E5_003 (Imports)
```

## Critical Path

1. E1_001 - Backup current skills
2. E2_001 - Sync skills directory
3. E3_001 - Sync commands directory
4. E4_001 - Sync .agents directory
5. E5_001 - Run pre-commit hooks
6. E5_002 - Run quality gates

## Parallel Work Opportunities

- E2_001, E3_001 can be done after backup completes
- E4_001 can be done after E2_001
- E5_003 can be done in parallel with E5_002

## Quality Checklist

Before considering this feature complete:

- [ ] All tasks marked as complete
- [ ] Pre-commit hooks passing
- [ ] All 6 quality gates passing
- [ ] Documentation validation passing
- [ ] Linting clean
- [ ] Type checking clean
- [ ] No import errors
- [ ] Git commit created

## Notes

### Implementation Tips

- Always create backup before sync operations
- Use `--delete` flag with rsync to remove obsolete files
- Exclude build artifacts and caches from sync
- Verify quality gates after each major sync

### Common Pitfalls

- Forgetting to exclude repository-specific files
- Overwriting local CLAUDE.md with template version
- Missing __pycache__ in exclude patterns

### Resources

- Source templates: `.tmp/stharrold-templates/`
- Quality gates: `.claude/skills/quality-enforcer/`
- Validation scripts: `tools/validation/`
