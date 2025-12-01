# Requirements: Apply Workflow Templates

**Feature Slug:** apply-workflow-templates
**GitHub Issue:** #248
**Created:** 2025-11-28
**Author:** stharrold

## Problem Statement

The workflow skills in this repository (`.claude/skills/`) are outdated compared to the source templates in `.tmp/stharrold-templates/`. Over 60 Python scripts have been updated with improvements to:
- AgentDB state management
- Git workflow operations (worktrees, PRs, releases)
- Quality enforcement gates
- VCS abstraction layer
- Workflow context verification

## Success Criteria

1. All 9 skills updated from template source
2. All 2 workflow commands updated
3. Pre-commit hooks pass
4. Quality gates pass (6 gates)
5. Documentation validation passes

## Functional Requirements

### FR-001: Sync Skill Scripts
**Priority:** High
**Description:** Copy updated Python scripts from `.tmp/stharrold-templates/.claude/skills/` to `.claude/skills/`

### FR-002: Sync Workflow Commands
**Priority:** High
**Description:** Copy updated workflow commands from `.tmp/stharrold-templates/.claude/commands/workflow/` to `.claude/commands/workflow/`

### FR-003: Sync .agents Directory
**Priority:** Medium
**Description:** Mirror updated skills to `.agents/` directory for cross-tool compatibility

### FR-004: Validate Quality Gates
**Priority:** High
**Description:** Run all 6 quality gates to ensure updates don't break existing functionality

### FR-005: Run Documentation Validation
**Priority:** Medium
**Description:** Run `./validate_documentation.sh` to ensure documentation standards

## Non-Functional Requirements

### NFR-001: No Breaking Changes
**Description:** Updates must not break existing workflows or scripts

### NFR-002: Preserve Repository-Specific Configuration
**Description:** Do not overwrite repository-specific files (CLAUDE.md at root, pyproject.toml)

## Out of Scope

- Root-level CLAUDE.md (repository-specific)
- Repository-specific configuration files
- Test files in `.tmp/stharrold-templates/tests/`
- Spec files in `.tmp/stharrold-templates/specs/`
