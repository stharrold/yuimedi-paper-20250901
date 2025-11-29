# Requirements: Repository Organization Cleanup

**Issue:** #243
**Author:** stharrold
**Created:** 2025-11-29

## Problem Statement

Repository audit identified several organizational issues requiring cleanup:

1. **Triple skills duplication** - `.agents/` contains both flat skills AND nested `.agents/skills/`
2. **Deprecated files at root** - `TODO_FOR_AI.json` and `TODO_FOR_HUMAN.md` still exist despite migration to GitHub Issues
3. **Root directory clutter** - 24 files at root level

## Requirements

### REQ-001: Remove Deprecated Root Files
**Priority:** P0

Remove deprecated TODO files from root that have already been archived:
- `TODO_FOR_AI.json` (127KB) - archived in `ARCHIVED/TODO/`
- `TODO_FOR_HUMAN.md` (17KB) - archived in `ARCHIVED/TODO/`

**Acceptance Criteria:**
- Files removed from root directory
- Files remain available in `ARCHIVED/TODO/`
- No references to deprecated files in active documentation

### REQ-002: Fix .agents/ Structure
**Priority:** P0

Fix the duplicate structure in `.agents/`:
- Remove nested `.agents/skills/` directory (duplication)
- Keep only flat mirror structure: `.agents/skill-name/`
- Update sync scripts to prevent re-creation of nested structure

**Acceptance Criteria:**
- `.agents/skills/` directory removed
- `.agents/` contains only top-level skill directories
- Sync commands updated in CLAUDE.md
- Pre-commit hooks updated if needed

### REQ-003: Root Directory Organization
**Priority:** P1

Evaluate and reduce root-level file clutter:
- Current: 24 files at root level
- Target: Essential files only

**Acceptance Criteria:**
- Root file count reduced
- Supporting docs moved to appropriate subdirectories (if applicable)
- All existing functionality preserved

## Constraints

- Documentation validation must still pass (`./validate_documentation.sh`)
- Pre-commit hooks must continue to work
- AI config sync (CLAUDE.md → AGENTS.md) must remain functional
- No changes to primary research document (`paper.md`)

## Success Criteria

- [ ] Deprecated TODO files removed from root
- [ ] `.agents/` contains only flat skill mirrors (no nested skills/)
- [ ] Root file count reduced
- [ ] Documentation validation passes
- [ ] Pre-commit hooks work correctly
