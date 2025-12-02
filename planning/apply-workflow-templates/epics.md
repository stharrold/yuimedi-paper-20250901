# Epics: Apply Workflow Templates

**Feature Slug:** apply-workflow-templates
**GitHub Issue:** #248
**Created:** 2025-11-28

## Epic Overview

| Epic | Description | Priority |
|------|-------------|----------|
| E1 | Backup current skills | High |
| E2 | Sync skills directory | High |
| E3 | Sync commands directory | High |
| E4 | Sync .agents directory | Medium |
| E5 | Validate and test | High |

## E1: Backup Current Skills

**Priority:** High
**Estimate:** 5 min

### Tasks
1. Create ARCHIVED/ directory if not exists
2. Create timestamped zip backup of `.claude/skills/`
3. Verify backup integrity

### Acceptance Criteria
- [ ] Backup zip exists in ARCHIVED/
- [ ] Backup contains all skill directories

---

## E2: Sync Skills Directory

**Priority:** High
**Estimate:** 10 min

### Tasks
1. Run rsync from template skills to local skills
2. Exclude .DS_Store and __pycache__
3. Verify all 9 skills synced

### Acceptance Criteria
- [ ] All 9 skill directories updated
- [ ] No .DS_Store or __pycache__ copied
- [ ] File permissions preserved

---

## E3: Sync Commands Directory

**Priority:** High
**Estimate:** 5 min

### Tasks
1. Run rsync from template commands to local commands
2. Verify workflow commands updated

### Acceptance Criteria
- [ ] 2_plan.md updated
- [ ] 5_integrate.md updated
- [ ] All other commands intact

---

## E4: Sync .agents Directory

**Priority:** Medium
**Estimate:** 5 min

### Tasks
1. Run rsync from template .agents to local .agents
2. Verify mirror consistency

### Acceptance Criteria
- [ ] .agents/ mirrors .claude/skills/
- [ ] No Claude-specific files in .agents/

---

## E5: Validate and Test

**Priority:** High
**Estimate:** 15 min

### Tasks
1. Run pre-commit hooks
2. Run quality gates (6 gates)
3. Run documentation validation
4. Test key scripts (verify imports work)

### Acceptance Criteria
- [ ] Pre-commit hooks pass
- [ ] All 6 quality gates pass
- [ ] Documentation validation passes
- [ ] No import errors in Python scripts
