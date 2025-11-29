# Architecture: Repository Organization Cleanup

**Issue:** #243
**Author:** stharrold
**Created:** 2025-11-29

## Current State

### Root Directory Structure (24 files)
```
.
├── AGENTS.md                    # Mirror of CLAUDE.md
├── CHANGELOG.md                 # Version history
├── CLAUDE.md                    # AI assistant instructions
├── DECISION_LOG.json            # Decision history
├── Dockerfile                   # Container definition
├── LICENSE                      # MIT license
├── README.md                    # Project overview
├── TODO.md                      # Points to GitHub Issues
├── TODO_FOR_AI.json             # DEPRECATED (127KB)
├── TODO_FOR_HUMAN.md            # DEPRECATED (17KB)
├── paper.md                     # Primary research document
├── podman-compose.yaml          # Container orchestration
├── pyproject.toml               # Python project config
├── uv.lock                      # Dependency lock
├── validate_documentation.sh    # Validation orchestrator
└── ... (other essential files)
```

### .agents/ Structure (PROBLEMATIC)
```
.agents/
├── agentdb-state-manager/       # Flat mirror (correct)
├── bmad-planner/                # Flat mirror (correct)
├── commands/                    # Commands mirror
├── git-workflow-manager/        # Flat mirror (correct)
├── initialize-repository/       # Flat mirror (correct)
├── quality-enforcer/            # Flat mirror (correct)
├── skills/                      # DUPLICATE - should not exist
│   ├── agentdb-state-manager/
│   ├── bmad-planner/
│   └── ... (all skills duplicated)
├── speckit-author/              # Flat mirror (correct)
├── tech-stack-adapter/          # Flat mirror (correct)
├── workflow-orchestrator/       # Flat mirror (correct)
└── workflow-utilities/          # Flat mirror (correct)
```

## Target State

### Root Directory (Reduced)
```
.
├── AGENTS.md                    # Keep - cross-tool compatibility
├── CHANGELOG.md                 # Keep - version history
├── CLAUDE.md                    # Keep - AI instructions
├── DECISION_LOG.json            # Keep - decision history
├── Dockerfile                   # Keep - container
├── LICENSE                      # Keep - license
├── README.md                    # Keep - project overview
├── TODO.md                      # Keep - points to issues
├── paper.md                     # Keep - primary document
├── podman-compose.yaml          # Keep - orchestration
├── pyproject.toml               # Keep - project config
├── uv.lock                      # Keep - lock file
└── validate_documentation.sh    # Keep - validation
```

Files removed:
- `TODO_FOR_AI.json` - archived
- `TODO_FOR_HUMAN.md` - archived

### .agents/ Structure (Fixed)
```
.agents/
├── agentdb-state-manager/       # Flat mirror
├── bmad-planner/                # Flat mirror
├── commands/                    # Commands mirror
├── git-workflow-manager/        # Flat mirror
├── initialize-repository/       # Flat mirror
├── quality-enforcer/            # Flat mirror
├── speckit-author/              # Flat mirror
├── tech-stack-adapter/          # Flat mirror
├── workflow-orchestrator/       # Flat mirror
└── workflow-utilities/          # Flat mirror
```

Removed:
- `.agents/skills/` directory (duplicate)

## Technical Design

### Component 1: File Removal

Simple `git rm` operations:
```bash
git rm TODO_FOR_AI.json
git rm TODO_FOR_HUMAN.md
```

### Component 2: .agents/ Cleanup

Remove nested duplicate:
```bash
rm -rf .agents/skills/
```

### Component 3: Sync Script Update

Update CLAUDE.md sync command to prevent re-creation:
```bash
# Current (creates flat mirror)
rsync -av --delete --exclude=".DS_Store" --exclude="__pycache__" .claude/skills/ .agents/

# Already correct - no change needed
```

Verify pre-commit hook doesn't recreate:
- Check `.claude/skills/workflow-utilities/scripts/sync_ai_config.py`
- Ensure it syncs to `.agents/skill-name/` not `.agents/skills/skill-name/`

## Integration Points

1. **Pre-commit hooks** - Must not recreate `.agents/skills/`
2. **CLAUDE.md documentation** - Sync commands must remain accurate
3. **Validation scripts** - Must continue to pass
4. **Git history** - Clean removal without breaking history

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Accidental data loss | Files already archived in ARCHIVED/TODO/ |
| Breaking sync | Review sync_ai_config.py before changes |
| Pre-commit failure | Test pre-commit run --all-files after changes |
