# Contributing to stharrold-templates

Thank you for considering contributing to this project! This document provides guidelines for contributing to the MCP configuration templates and workflow automation tools.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Documentation Requirements](#documentation-requirements)
- [Pull Request Process](#pull-request-process)
- [Quality Standards](#quality-standards)

## Code of Conduct

This project follows a professional and respectful code of conduct:

- Be respectful and inclusive.
- Focus on constructive feedback.
- Prioritize technical accuracy and truthfulness.
- Welcome contributions from all skill levels.

## Getting Started

### Prerequisites

Ensure you have the required tools installed:

```bash
# Required
podman --version          # Container runtime (Podman 4.0+)
podman-compose --version  # Container orchestration
git --version             # Version control
python3 --version         # Python 3.11+
uv --version              # Python package manager

# GitHub CLI (or az CLI for Azure DevOps repos):
gh --version              # GitHub CLI (for PR operations)
# az --version            # Azure DevOps CLI (alternative, if using Azure DevOps)
```

### Initial Setup

1. **Fork and clone the repository:**
   ```bash
   gh repo fork stharrold/stharrold-templates --clone
   cd stharrold-templates
   ```

2. **Build container:**
   ```bash
   podman-compose build
   ```

3. **Install local dependencies:**
   ```bash
   uv sync
   ```

## Development Workflow (v7x1)

This repository uses a streamlined **v7x1** workflow.

### Branch Structure

```
main (production)
  ↑
develop (integration)
  ↑
contrib/stharrold (your editable branch)
  ↑
feature/* (isolated worktrees)
```

### Workflow Steps

1. **Create Worktree**: `/workflow:v7x1_1-worktree "feature description"`
2. **Implement**: Perform implementation using Claude Code (in worktree).
3. **Integrate**: `/workflow:v7x1_2-integrate` (in main repo)
4. **Release**: `/workflow:v7x1_3-release`
5. **Backmerge**: `/workflow:v7x1_4-backmerge`

### Manual Maintenance

```bash
# Rebase contrib branch onto develop
uv run python .claude/skills/git-workflow-manager/scripts/daily_rebase.py contrib/stharrold
```

## Documentation Requirements

### Modular CLAUDE.md Pattern

All directories must have:

1. **CLAUDE.md** - AI context and navigation.
2. **README.md** - Human-readable documentation.
3. **ARCHIVED/** - Deprecated files subdirectory.

### File Size Constraints

- All files in `docs/guides/` must be ≤30KB.
- Use modular structure with cross-references.

## Pull Request Process

### 1. Create Pull Request

Use the `/workflow:v7x1_2-integrate` command to automate PR creation, or do it manually:

```bash
# Create PR to contrib/stharrold
gh pr create \
  --title "feat: descriptive title" \
  --body "Detailed description" \
  --base contrib/stharrold
```

### 2. PR Requirements

- [ ] All CI/CD tests pass.
- [ ] Claude Code Review completed.
- [ ] Documentation updated to reflect changes.
- [ ] Commit messages follow Conventional Commits.

### 3. Commit Message Format

```
<type>(<scope>): <subject>

<body>

🤖 Generated with [Claude Code](https://claude.ai/code)
```

**Types:** feat, fix, docs, style, refactor, test, chore.

## Quality Standards

### Python Code Standards

- **Containerized**: Use `podman-compose` for consistency.
- **One way to run**: Prefer `uv run <command>` or `podman-compose run --rm dev uv run <command>`.
- **SPDX Headers**: All Python files must have Apache 2.0 license headers.
- **ASCII-only**: Python files must use only ASCII characters.

### Workflow Tools

This repository includes 6 active workflow skills in `.claude/skills/`:
- `workflow-orchestrator`: Main coordinator.
- `git-workflow-manager`: Git automation.
- `tech-stack-adapter`: Stack detection.
- `workflow-utilities`: Shared utilities.
- `agentdb-state-manager`: State tracking.
- `initialize-repository`: Repository bootstrapping.

## AI Configuration Guidelines

| To change... | Edit this | NOT this |
|--------------|-----------|----------|
| Skills | `.claude/skills/` | `.agents/` |
| Commands | `.claude/commands.toml` | N/A |
| Root instructions | `CLAUDE.md` | `AGENTS.md` |

**Note**: `.agents/` and `AGENTS.md` are automatically synced from `.claude/` sources.

## Questions or Issues?

- Open an issue on GitHub.
- Check `CLAUDE.md` for detailed guidance.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
