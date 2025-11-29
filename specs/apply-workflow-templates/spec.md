# Specification: Apply Workflow Templates

**Type:** feature
**Slug:** apply-workflow-templates
**Date:** 2025-11-28
**Author:** stharrold
**GitHub Issue:** #239

## Overview

This feature syncs updated workflow skills and commands from the stharrold-templates repository to this repository. The templates contain over 60 updated Python scripts with improvements to AgentDB state management, git workflow operations, quality enforcement gates, VCS abstraction, and workflow context verification.

## Requirements Reference

See: `planning/apply-workflow-templates/requirements.md` in main repository

### Success Criteria

1. All 9 skills updated from template source
2. All 2 workflow commands updated
3. Pre-commit hooks pass
4. Quality gates pass (6 gates)
5. Documentation validation passes

## Detailed Specification

### Component 1: Skills Directory Sync

**Source:** `.tmp/stharrold-templates/.claude/skills/`
**Target:** `.claude/skills/`

**Skills to Update (9 total):**
1. agentdb-state-manager - Workflow state tracking with DuckDB
2. bmad-planner - Requirements and architecture planning
3. git-workflow-manager - Git operations, worktrees, PRs
4. initialize-repository - Repository bootstrapping
5. quality-enforcer - Quality gates (6 gates)
6. speckit-author - Specification authoring
7. tech-stack-adapter - Stack detection
8. workflow-orchestrator - Main coordinator
9. workflow-utilities - Shared utilities

**Implementation:**
```bash
rsync -av --delete \
  --exclude=".DS_Store" \
  --exclude="__pycache__" \
  --exclude="*.pyc" \
  .tmp/stharrold-templates/.claude/skills/ .claude/skills/
```

### Component 2: Commands Directory Sync

**Source:** `.tmp/stharrold-templates/.claude/commands/`
**Target:** `.claude/commands/`

**Implementation:**
```bash
rsync -av --delete \
  --exclude=".DS_Store" \
  .tmp/stharrold-templates/.claude/commands/ .claude/commands/
```

### Component 3: .agents Directory Sync

**Source:** `.tmp/stharrold-templates/.agents/`
**Target:** `.agents/`

**Purpose:** Mirror of .claude/skills/ for cross-tool compatibility

**Implementation:**
```bash
rsync -av --delete \
  --exclude=".DS_Store" \
  --exclude="__pycache__" \
  .tmp/stharrold-templates/.agents/ .agents/
```

## Files to Exclude from Sync

### Repository-Specific Files (DO NOT SYNC)
- `CLAUDE.md` (root) - Repository-specific instructions
- `AGENTS.md` (root) - Auto-generated from CLAUDE.md
- `pyproject.toml` - Repository-specific dependencies
- `README.md` (root) - Repository-specific documentation
- `WORKFLOW.md` - Repository-specific workflow docs
- `CONTRIBUTING.md` - Repository-specific guidelines

### Template-Only Files (DO NOT SYNC)
- `.tmp/stharrold-templates/specs/` - Template specs
- `.tmp/stharrold-templates/tests/` - Template tests
- `.tmp/stharrold-templates/planning/` - Template planning
- `.tmp/stharrold-templates/docs/` - Template docs

## Quality Gates

- [ ] Pre-commit hooks pass
- [ ] Documentation validation passes (`./validate_documentation.sh`)
- [ ] Linting clean (`uv run ruff check .`)
- [ ] Type checking clean (`uv run mypy scripts/`)
- [ ] Build succeeds (`uv build`)

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Breaking existing scripts | Create backup before sync |
| Overwriting repo-specific config | Exclude specific files from rsync |
| Quality gate failures | Run validation after sync |
| Import errors | Test scripts after sync |

## Dependencies

- rsync (system utility)
- Python 3.11+
- uv package manager
- GitHub CLI (gh)

## References

- Source templates: `.tmp/stharrold-templates/`
- Planning documents: `planning/apply-workflow-templates/`
