# Architecture: Apply Workflow Templates

**Feature Slug:** apply-workflow-templates
**GitHub Issue:** #248
**Created:** 2025-11-28

## Overview

This feature syncs updated workflow skills and commands from the stharrold-templates repository to this repository. The architecture follows the existing skill-based structure.

## Source and Target Mapping

### Skills Directory

| Source | Target | Action |
|--------|--------|--------|
| `.tmp/stharrold-templates/.claude/skills/` | `.claude/skills/` | Sync |
| `.tmp/stharrold-templates/.agents/` | `.agents/` | Sync |

### Commands Directory

| Source | Target | Action |
|--------|--------|--------|
| `.tmp/stharrold-templates/.claude/commands/workflow/` | `.claude/commands/workflow/` | Sync |

## Skills to Update (9 total)

1. **agentdb-state-manager** - Workflow state tracking with DuckDB
2. **bmad-planner** - Requirements and architecture planning
3. **git-workflow-manager** - Git operations, worktrees, PRs
4. **initialize-repository** - Repository bootstrapping
5. **quality-enforcer** - Quality gates (6 gates)
6. **speckit-author** - Specification authoring
7. **tech-stack-adapter** - Stack detection
8. **workflow-orchestrator** - Main coordinator
9. **workflow-utilities** - Shared utilities

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
- `.tmp/stharrold-templates/docs/` - Template docs (except reference/)
- `.tmp/stharrold-templates/mcp_manager.py` - Template-specific

## Sync Strategy

### Step 1: Backup Current Skills
```bash
# Create timestamped backup
zip -r ARCHIVED/$(date +%Y%m%dT%H%M%SZ)_skills-backup.zip .claude/skills/
```

### Step 2: Sync Skills Directory
```bash
rsync -av --delete \
  --exclude=".DS_Store" \
  --exclude="__pycache__" \
  --exclude="*.pyc" \
  .tmp/stharrold-templates/.claude/skills/ .claude/skills/
```

### Step 3: Sync Commands Directory
```bash
rsync -av --delete \
  --exclude=".DS_Store" \
  .tmp/stharrold-templates/.claude/commands/ .claude/commands/
```

### Step 4: Sync .agents Directory
```bash
rsync -av --delete \
  --exclude=".DS_Store" \
  --exclude="__pycache__" \
  .tmp/stharrold-templates/.agents/ .agents/
```

### Step 5: Validate
```bash
# Run quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# Run documentation validation
./validate_documentation.sh
```

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
