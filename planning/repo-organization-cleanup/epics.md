# Epics: Repository Organization Cleanup

**Issue:** #243
**Author:** stharrold
**Created:** 2025-11-29

## Epic 1: Remove Deprecated Files

**Priority:** P0
**Estimated Effort:** Small

### User Story
As a repository maintainer, I want deprecated TODO files removed from root so that the repository structure reflects the current task management approach (GitHub Issues).

### Tasks

1. **Verify archives exist**
   - Confirm `TODO_FOR_AI.json` is in `ARCHIVED/TODO/`
   - Confirm `TODO_FOR_HUMAN.md` is in `ARCHIVED/TODO/`

2. **Remove deprecated files**
   - `git rm TODO_FOR_AI.json`
   - `git rm TODO_FOR_HUMAN.md`

3. **Update documentation references**
   - Search for references to deprecated files
   - Update any stale references

### Acceptance Criteria
- [ ] Deprecated files removed from root
- [ ] Archives verified to exist
- [ ] No broken references in documentation

---

## Epic 2: Fix .agents/ Structure

**Priority:** P0
**Estimated Effort:** Small

### User Story
As a repository maintainer, I want the `.agents/` directory to contain only flat skill mirrors so that there is no triple duplication of skills.

### Tasks

1. **Audit current structure**
   - List contents of `.agents/`
   - Identify duplicate `.agents/skills/` directory

2. **Remove duplicate directory**
   - `rm -rf .agents/skills/`

3. **Verify sync script behavior**
   - Review `sync_ai_config.py` in workflow-utilities
   - Ensure sync creates flat structure only
   - Test pre-commit hook doesn't recreate nested structure

4. **Update documentation if needed**
   - Verify CLAUDE.md sync commands are correct
   - Update if any references to nested structure exist

### Acceptance Criteria
- [ ] `.agents/skills/` directory removed
- [ ] Sync script verified to create flat structure
- [ ] Pre-commit hooks tested
- [ ] Documentation accurate

---

## Epic 3: Validate Changes

**Priority:** P0
**Estimated Effort:** Small

### User Story
As a repository maintainer, I want all validation and quality gates to pass after cleanup so that repository integrity is maintained.

### Tasks

1. **Run documentation validation**
   - `./validate_documentation.sh`

2. **Run pre-commit hooks**
   - `uv run pre-commit run --all-files`

3. **Run quality gates**
   - `python .claude/skills/quality-enforcer/scripts/run_quality_gates.py`

4. **Verify git status**
   - Confirm expected files removed
   - Confirm no unintended changes

### Acceptance Criteria
- [ ] Documentation validation passes
- [ ] Pre-commit hooks pass
- [ ] Quality gates pass
- [ ] Git status shows expected changes only

---

## Summary

| Epic | Priority | Effort | Dependencies |
|------|----------|--------|--------------|
| 1. Remove Deprecated Files | P0 | Small | None |
| 2. Fix .agents/ Structure | P0 | Small | None |
| 3. Validate Changes | P0 | Small | Epics 1-2 |

**Total Epics:** 3
**Total Estimated Effort:** Small (single session)
