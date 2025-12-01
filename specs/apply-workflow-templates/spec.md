# Specification: Apply Workflow Templates

**Type:** feature
**Slug:** apply-workflow-templates
**Date:** 2025-12-01
**Author:** stharrold
**GitHub Issue:** #248

## Overview

Update the repository's workflow skills (`.claude/skills/`) and commands (`.claude/commands/workflow/`) from the source templates in `.tmp/stharrold-templates/`. This sync brings improvements to:

- AgentDB state management
- Git workflow operations (worktrees, PRs, releases)
- Quality enforcement gates
- VCS abstraction layer (GitHub/Azure DevOps)
- Workflow context verification

## Requirements Reference

See: `planning/apply-workflow-templates/requirements.md`

### Functional Requirements

| ID | Description | Priority |
|----|-------------|----------|
| FR-001 | Sync skill scripts from template | High |
| FR-002 | Sync workflow commands from template | High |
| FR-003 | Mirror to .agents/ directory | Medium |
| FR-004 | Validate with quality gates | High |
| FR-005 | Run documentation validation | Medium |

### Non-Functional Requirements

| ID | Description |
|----|-------------|
| NFR-001 | No breaking changes to existing workflows |
| NFR-002 | Preserve repository-specific configuration |

## Source and Target Mapping

### Skills Directory

**Source:** `.tmp/stharrold-templates/.claude/skills/`
**Target:** `.claude/skills/`

| Skill | Description |
|-------|-------------|
| agentdb-state-manager | DuckDB-based workflow state tracking |
| bmad-planner | BMAD planning document generation |
| git-workflow-manager | Git operations (worktrees, branches, PRs) |
| initialize-repository | New repository setup |
| quality-enforcer | Quality gate validation (6 gates) |
| speckit-author | Specification and plan generation |
| tech-stack-adapter | Technology stack detection |
| workflow-orchestrator | Workflow phase coordination |
| workflow-utilities | Shared utilities (deprecation, VCS, etc.) |

### Commands Directory

**Source:** `.tmp/stharrold-templates/.claude/commands/workflow/`
**Target:** `.claude/commands/workflow/`

| Command | Description |
|---------|-------------|
| 1_specify.md | Create feature specification |
| 2_plan.md | Generate implementation plan |
| 3_tasks.md | Validate task list |
| 4_implement.md | Execute implementation |
| 5_integrate.md | Create PR to contrib |
| 6_release.md | Release branch workflow |
| 7_backmerge.md | Backmerge after release |
| all.md | Full workflow orchestration |

### Mirror Directory

**Source:** `.claude/skills/`, `.claude/commands/`
**Target:** `.agents/`, `.agents/commands/`

Purpose: Cross-tool compatibility for non-Claude AI assistants.

## Sync Strategy

### rsync Command Pattern

```bash
rsync -av --delete \
  --exclude=".DS_Store" \
  --exclude="__pycache__" \
  --exclude="*.pyc" \
  <source>/ <target>/
```

### Exclusions

| Pattern | Reason |
|---------|--------|
| .DS_Store | macOS metadata |
| __pycache__ | Python bytecode cache |
| *.pyc | Compiled Python |

### Files NOT to Sync

| File | Reason |
|------|--------|
| Root CLAUDE.md | Repository-specific content |
| pyproject.toml | Repository-specific dependencies |
| .tmp/stharrold-templates/tests/ | Template tests, not needed |
| .tmp/stharrold-templates/specs/ | Template specs, not needed |

## Validation Strategy

### Pre-commit Hooks

```bash
uv run pre-commit run --all-files
```

Validates:
- Trailing whitespace
- End of file newlines
- Ruff formatting and linting
- CLAUDE.md YAML frontmatter
- Skill directory structure

### Quality Gates (6 gates)

```bash
uv run python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

| Gate | Description |
|------|-------------|
| 1 | Documentation validation |
| 2 | Linting (ruff check) |
| 3 | Type checking (mypy) |
| 4 | Coverage (≥80% or skip) |
| 5 | Tests (pass or skip) |
| 6 | Build (uv build) |

### Documentation Validation

```bash
./validate_documentation.sh
```

Runs 5 tests:
1. File size (30KB limit)
2. Cross-references
3. Content duplication
4. Command syntax
5. YAML structure

## Rollback Strategy

If sync causes issues:

1. Extract backup from `ARCHIVED/<timestamp>_pre-template-sync-backup.zip`
2. Restore `.claude/skills/` from backup
3. Re-sync `.agents/` from restored skills

## Dependencies

### Required

- `.tmp/stharrold-templates/` must exist with template files
- rsync available (standard on macOS/Linux)
- uv package manager installed

### Optional

- duckdb (for AgentDB state tracking)
- podman-compose (for container-based validation)

## Implementation Notes

### Order of Operations

1. **Backup first** - Always create backup before destructive sync
2. **Skills before commands** - Commands may reference skill scripts
3. **Mirror after both** - .agents/ should reflect final state
4. **Validate last** - Run all validation after sync complete

### Known Issues

- Container environment can't access git worktrees (use `uv run` instead)
- AgentDB requires `uv sync --extra workflow` for duckdb

### Success Indicators

- All 9 skill directories present and updated
- All 8 workflow commands present
- .agents/ mirrors .claude/ structure
- All pre-commit hooks pass
- All 6 quality gates pass
- Documentation validation passes
