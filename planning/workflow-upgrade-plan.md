# Workflow Upgrade Plan: Apply stharrold-templates v5.15.0 to yuimedi-paper-20250901

**Created:** 2025-11-25
**Status:** READY FOR APPROVAL

**Key Decisions Made:**
- Python: Upgrade to 3.11+
- Skills: Full overwrite from templates
- Tests: Add minimal structure
- Execution: All phases at once

## Executive Summary

This plan migrates the yuimedi-paper-20250901 repository from workflow v1.6.0 to the stharrold-templates v5.15.0 workflow system. The migration preserves the documentation-only nature of this repository while upgrading to newer, more feature-rich workflow automation.

## Current State Analysis

### yuimedi-paper-20250901 (Current)
- **Workflow version:** 1.6.0 (skills system)
- **Primary purpose:** Documentation-only research paper repository
- **Skills:** 9 skills (older versions)
- **Build system:** Hatchling
- **Python:** 3.9+ (minimum)
- **Dependencies:** Zero runtime dependencies for core scripts
- **Task management:** GitHub Issues
- **Validation:** 5 bash validation scripts
- **Quality gates:** 6 gates (documentation focus)

### stharrold-templates (Target)
- **Workflow version:** 5.15.0
- **Primary purpose:** MCP templates and Python development workflows
- **Skills:** 9 skills (updated versions with new features)
- **Build system:** Setuptools
- **Python:** 3.11+ (minimum)
- **Dependencies:** rich, click, httpx, duckdb (runtime)
- **Pre-commit:** Full AI config sync hooks
- **YAML frontmatter:** All CLAUDE.md files have frontmatter
- **VCS abstraction:** GitHub/Azure DevOps support
- **Tests:** Full pytest structure (unit/contract/integration/skills)

## Key Differences

| Aspect | Current Repo | Templates Repo | Migration Impact |
|--------|-------------|----------------|------------------|
| Python version | 3.9+ | 3.11+ | **Decision needed** |
| Build backend | hatchling | setuptools | Keep hatchling |
| Runtime deps | None | rich, click, httpx, duckdb | Keep zero-deps for core |
| Pre-commit hooks | None | Full suite with AI sync | Add |
| YAML frontmatter | No | Yes (all CLAUDE.md) | Add |
| Tests | None (doc-only) | Full pytest suite | Skip (doc-only) |
| VCS abstraction | GitHub only | GitHub + Azure DevOps | Adopt |
| Workflow commands | 8 commands (older) | 8 commands (newer) | Update |
| Skills scripts | Older versions | Newer with features | Update |

## Migration Strategy

### Approach: Selective Merge (Recommended)

**NOT** a full `initialize_repository.py` run (would overwrite customizations).

Instead: **Selective update** of specific components while preserving:
- Documentation-only focus
- Zero runtime dependencies for core scripts
- Existing CLAUDE.md customizations
- GitHub Issues task management
- Healthcare-specific context

## Implementation Phases

### Phase 1: Skills Update (High Priority)
**Estimated files:** ~50 files across 9 skills

1. **Backup current skills:**
   ```bash
   cp -r .claude/skills/ .claude/skills.backup-$(date +%Y%m%d)/
   ```

2. **Update skill scripts** (selective merge, not full overwrite):
   - `agentdb-state-manager/scripts/` - Add `query_workflow_state.py`, `record_sync.py`
   - `git-workflow-manager/scripts/` - Add `archive_spec.py`, `worktree_agent_integration.py`
   - `workflow-utilities/scripts/` - Add `sync_ai_config.py`, `check_claude_md_frontmatter.py`, `check_skill_structure.py`, `verify_workflow_context.py`
   - Update existing scripts with newer versions (diff and merge)

3. **Add CLAUDE.md to subdirectories:**
   - Each `scripts/`, `templates/`, `schemas/` directory needs CLAUDE.md
   - Follow templates repo pattern

### Phase 2: Pre-commit Hooks (High Priority)
**Files:** 1 new file, 3 new scripts

1. **Create `.pre-commit-config.yaml`:**
   ```yaml
   repos:
     - repo: https://github.com/pre-commit/pre-commit-hooks
       rev: v4.5.0
       hooks:
         - id: trailing-whitespace
         - id: end-of-file-fixer
         - id: check-yaml
         - id: check-json
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.1.6
       hooks:
         - id: ruff
         - id: ruff-format
     - repo: local
       hooks:
         - id: sync-ai-config
           name: Sync AI configuration
           entry: python .claude/skills/workflow-utilities/scripts/sync_ai_config.py sync
           language: python
           files: ^(CLAUDE\.md|\.claude/)
           pass_filenames: false
   ```

2. **Add sync scripts:**
   - `sync_ai_config.py` - Sync CLAUDE.md → AGENTS.md, .agents/
   - `check_claude_md_frontmatter.py` - Validate YAML frontmatter
   - `check_skill_structure.py` - Validate skill directory structure

### Phase 3: YAML Frontmatter (Medium Priority)
**Files:** ~15-20 CLAUDE.md files

1. **Add frontmatter to root CLAUDE.md:**
   ```yaml
   ---
   type: claude-context
   directory: .
   purpose: Research paper on YuiQuery healthcare analytics
   parent: null
   sibling_readme: README.md
   children:
     - .claude/CLAUDE.md
     - docs/CLAUDE.md
     - scripts/CLAUDE.md
   ---
   ```

2. **Add frontmatter to all existing CLAUDE.md files:**
   - Each skill's CLAUDE.md
   - docs/ directory
   - scripts/ directory
   - tools/ directory

### Phase 4: Workflow Commands Update (Medium Priority)
**Files:** 8 files in `.claude/commands/workflow/`

1. **Update each command file** with newer versions:
   - `1_specify.md` → More comprehensive specification flow
   - `2_plan.md` → Better speckit integration
   - `3_tasks.md` → Task validation
   - `4_implement.md` → Quality gates integration
   - `5_integrate.md` → Improved PR workflow
   - `6_release.md` → Release workflow updates
   - `7_backmerge.md` → Backmerge workflow updates
   - `all.md` → Full orchestration with state detection
   - Add `CLAUDE.md` to commands directory

### Phase 5: Documentation Updates (Medium Priority)
**Files:** 3-5 files

1. **Add/Update WORKFLOW.md:**
   - Version 5.3.0 structure
   - Phase documentation references
   - Directory standards section
   - Preserve documentation-only context

2. **Add ARCHITECTURE.md:**
   - Adapt from templates repo
   - Focus on documentation workflow
   - Remove Python-specific sections

3. **Update/Add CONTRIBUTING.md:**
   - Contribution guidelines
   - Quality standards
   - PR process

### Phase 6: pyproject.toml Updates (Low Priority)
**Files:** 1 file

1. **Keep hatchling build backend** (don't change to setuptools)

2. **Add pre-commit to dev dependencies:**
   ```toml
   [project.optional-dependencies]
   dev = [
       "ruff>=0.8.0",
       "mypy>=1.0.0",
       "pre-commit>=4.0.0",
   ]
   ```

3. **Upgrade to Python 3.11+** per decision (align with templates repo)

### Phase 7: Agent Sync Infrastructure (Low Priority)
**Files:** 2-3 files

1. **Update .agents/ sync pattern:**
   - Ensure rsync commands work correctly
   - Add CLAUDE.md to .agents/ mirror

2. **Add .github/copilot-instructions.md** sync (optional)

### Phase 8: Tests Infrastructure (Medium Priority)
**Files:** ~10 files

1. **Create tests/ directory structure:**
   ```
   tests/
   ├── __init__.py
   ├── conftest.py
   ├── CLAUDE.md
   ├── skills/
   │   ├── __init__.py
   │   ├── CLAUDE.md
   │   └── test_quality_enforcer.py
   └── unit/
       ├── __init__.py
       └── CLAUDE.md
   ```

2. **Add pytest configuration to pyproject.toml:**
   ```toml
   [tool.pytest.ini_options]
   testpaths = ["tests"]
   pythonpath = ["."]
   ```

3. **Add pytest to dev dependencies:**
   ```toml
   dev = [
       "pytest>=8.4.0",
       "pytest-cov>=7.0.0",
       ...
   ]
   ```

## Files to NOT Modify

These files should be preserved as-is:
- `paper.md` - Primary research document
- `README.md` - Project-specific overview
- `TODO.md` - Points to GitHub Issues
- `DECISION_LOG.json` - Project decisions
- `scripts/sync_github_todos.py` - Custom zero-deps script
- `tools/validation/*` - Custom validation scripts
- `validate_documentation.sh` - Custom orchestrator

## Decision Points (RESOLVED)

### 1. Python Version
**Decision:** **Upgrade to 3.11+** - Align with templates repo for consistency

### 2. Runtime Dependencies
**Decision:** Keep zero-deps for core scripts, but update workflow optional deps

### 3. Tests Infrastructure
**Decision:** **Add minimal structure** - tests/skills/ for future skill validation

### 4. Full vs Selective Update
**Decision:** **Full overwrite** - Replace skills entirely with template versions

### 5. Execution Priority
**Decision:** **All phases at once** - Execute all phases in recommended order

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing workflows | Medium | High | Full backup before migration |
| CLAUDE.md content loss | Low | High | Git history preserves content |
| Skill incompatibilities | Medium | Medium | Test each skill after update |
| Pre-commit breaks CI | Low | Medium | Test locally first |

## Rollback Strategy

1. **Git revert:** All changes in single feature branch
2. **Backup restore:** `.claude/skills.backup-*` preserved
3. **Incremental commits:** Each phase in separate commit

## Success Criteria

- [ ] All 9 skills updated to v5.x versions
- [ ] Pre-commit hooks installed and working
- [ ] YAML frontmatter on all CLAUDE.md files
- [ ] Workflow commands updated to v5.x
- [ ] WORKFLOW.md updated to v5.3.0 format
- [ ] `./validate_documentation.sh` still passes
- [ ] Quality gates still pass
- [ ] AI config sync working (CLAUDE.md → AGENTS.md)

## Estimated Effort

| Phase | Files | Complexity | Time Estimate |
|-------|-------|------------|---------------|
| 1. Skills Update | ~50 | High | 2-3 sessions |
| 2. Pre-commit Hooks | ~4 | Medium | 1 session |
| 3. YAML Frontmatter | ~20 | Low | 1 session |
| 4. Workflow Commands | ~9 | Medium | 1 session |
| 5. Documentation | ~5 | Medium | 1 session |
| 6. pyproject.toml | 1 | Low | 0.5 session |
| 7. Agent Sync | ~3 | Low | 0.5 session |
| 8. Tests Infrastructure | ~10 | Medium | 1 session |

**Total:** ~8-9 sessions

## Implementation Order

Recommended sequence (all at once per user decision):
1. **Phase 6: pyproject.toml** - Update Python version first
2. **Phase 2: Pre-commit hooks** - Foundation for other changes
3. **Phase 3: YAML frontmatter** - Required for skill validation
4. **Phase 1: Skills Update** - Full overwrite from templates
5. **Phase 4: Workflow Commands** - Update to newer versions
6. **Phase 8: Tests Infrastructure** - Add tests structure
7. **Phase 5: Documentation** - WORKFLOW.md, ARCHITECTURE.md
8. **Phase 7: Agent Sync** - Final sync and validation

## Next Steps

Upon approval:
1. Create feature branch: `feature/workflow-v5-upgrade`
2. Execute phases in recommended order
3. Test each phase before proceeding
4. Create PR to `contrib/stharrold` when complete
