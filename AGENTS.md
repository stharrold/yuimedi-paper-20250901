# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

**Templates and utilities for MCP (Model Context Protocol) server configuration:**
- Multi-platform MCP manager (`mcp_manager.py`) for Claude Code CLI, VS Code, and Claude Desktop
- Modular documentation guides (≤30KB per file for AI context optimization)
- Workflow automation tools (git helpers, archive management, semantic versioning)
- **Containerized development** - Podman + uv + Python 3.11 for consistent dev/CI environments

**Key Principle**: All development uses `podman-compose run --rm dev <command>`. One way to run everything.

## Essential Commands

```bash
# Build container (once)
podman-compose build

# Run any command
podman-compose run --rm dev <command>

# Common operations
podman-compose run --rm dev pytest                    # Run tests
podman-compose run --rm dev pytest -v -k test_name    # Single test
podman-compose run --rm dev ruff check .              # Lint
podman-compose run --rm dev ruff check --fix .        # Auto-fix
podman-compose run --rm dev python mcp_manager.py --status
```

## Quality Gates (6 gates, all must pass before PR)

```bash
podman-compose run --rm dev python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

| Gate | Description |
|------|-------------|
| 1. Coverage | ≥80% test coverage |
| 2. Tests | All pytest tests pass |
| 3. Build | `uv build` succeeds |
| 4. Linting | `ruff check .` clean |
| 5. TODO Frontmatter | All TODO*.md have valid YAML frontmatter |
| 6. AI Config Sync | CLAUDE.md → AGENTS.md synced |

## PR Workflow (Enforced Sequence)

```bash
# Step 1: PR feature → contrib (runs quality gates)
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/pr_workflow.py finish-feature

# Step 2: Archive TODO after PR merge
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/pr_workflow.py archive-todo

# Step 3: Sync CLAUDE.md → AGENTS.md
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/pr_workflow.py sync-agents

# Step 4: PR contrib → develop
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/pr_workflow.py start-develop

# Or run all steps
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/pr_workflow.py full
```

## TODO*.md YAML Frontmatter (Required)

All TODO files must start with:
```yaml
---
status: in_progress|completed|blocked
feature: feature-name
branch: feature/timestamp_slug
---
```

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/plan` | Execute implementation planning workflow |
| `/specify` | Create/update feature specification |
| `/tasks` | Generate tasks.md from design artifacts |
| `/workflow` | Execute PR workflow steps |

## Core Architecture

### MCP Manager (`mcp_manager.py`)

**Platform Detection**: Auto-detects claude-code → vscode → claude-desktop

**Key Functions**:
- `MCPConfig(platform, config_path)` - Platform-specific handler
- `select_target_platform()` - Returns first available platform
- `deduplicate_servers()` - Preserves DISABLED_ prefixed versions

**Schema Differences**:
- Claude Code & Desktop: `"mcpServers": {}`
- VS Code: `"servers": {}`

### Branch Structure

```
main (production) ← develop (integration) ← contrib/stharrold (active) ← feature/*
```

**PR Flow**: feature → contrib → develop → main

**Branch Editability:**
| Branch | Editable | Direct Commits |
|--------|----------|----------------|
| `feature/*` | Yes | Yes |
| `contrib/*` | Yes | Yes |
| `develop` | No | PRs only |
| `main` | No | PRs only |
| `release/*` | Ephemeral | Deleted after merge |

### Skills System (9 skills in `.claude/skills/`)

| Skill | Purpose |
|-------|---------|
| workflow-orchestrator | Main coordinator, templates |
| git-workflow-manager | Worktrees, PRs, semantic versioning |
| quality-enforcer | Quality gates (6 gates) |
| bmad-planner | Requirements + architecture |
| speckit-author | Specifications |
| tech-stack-adapter | Python/uv/Podman detection |
| workflow-utilities | Archive, directory structure |
| agentdb-state-manager | DuckDB state sync |
| initialize-repository | Bootstrap new repos |

### Document Lifecycle

```
00_draft-initial/ → 10_draft-merged/ → ARCHIVED/
(research)         (production)       (compressed)
```

### AI Config Sync

CLAUDE.md automatically syncs to:
- `AGENTS.md` (cross-tool)
- `.github/copilot-instructions.md` (GitHub Copilot)
- `.agents/` (mirrored skills)

## Git Workflow Commands

```bash
# Create feature worktree
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/create_worktree.py feature my-feature contrib/stharrold

# Semantic version calculation
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/semantic_version.py develop v5.0.0

# Archive management
podman-compose run --rm dev python tools/workflow-utilities/archive_manager.py list
```

## MCP Configuration Paths

| Platform | macOS | Windows | Linux |
|----------|-------|---------|-------|
| Claude Code | `~/.claude.json` | `~/.claude.json` | `~/.claude.json` |
| VS Code | `~/Library/.../mcp.json` | `~/AppData/.../mcp.json` | `~/.config/.../mcp.json` |
| Claude Desktop | `~/Library/.../config.json` | `~/AppData/.../config.json` | `~/.config/.../config.json` |

## Prerequisites

```bash
podman --version          # 4.0+
podman-compose --version
git --version
gh --version              # GitHub CLI
```

## Critical Guidelines

- **One way to run**: Always use `podman-compose run --rm dev <command>`
- **End on editable branch**: All workflows must end on `contrib/*` (never `develop` or `main`)
- **ALWAYS prefer editing existing files** over creating new ones
- **NEVER proactively create documentation files** unless explicitly requested
- **Follow PR workflow sequence**: finish-feature → archive-todo → sync-agents → start-develop
- **TODO files require YAML frontmatter**: status, feature, branch fields
- **Quality gates must pass** before creating any PR

## Common Issues

| Issue | Solution |
|-------|----------|
| Container not building | `podman info` to verify Podman running |
| Import errors | Use `podman-compose run --rm dev python` |
| Platform not found | `mcp_manager.py --status` to check |
| Worktree conflicts | `git worktree remove` + `git worktree prune` |
| Ended on wrong branch | `git checkout contrib/stharrold` |

## Reference Documentation

- `WORKFLOW.md` - Complete 6-phase workflow guide (v5.3.0)
- `ARCHITECTURE.md` - System architecture analysis
- `CHANGELOG.md` - Version history
- `docs/reference/` - Workflow reference docs
