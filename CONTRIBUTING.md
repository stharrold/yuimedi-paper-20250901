# Contributing to stharrold-templates

Thank you for considering contributing to this project! This document provides guidelines for contributing to the MCP configuration templates and workflow automation tools.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [MCP Server Contributions](#mcp-server-contributions)
- [Documentation Requirements](#documentation-requirements)
- [Pull Request Process](#pull-request-process)
- [Quality Standards](#quality-standards)

## Code of Conduct

This project follows a professional and respectful code of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Prioritize technical accuracy and truthfulness
- Welcome contributions from all skill levels

## Getting Started

### Prerequisites

Ensure you have the required tools installed:

```bash
# Required
podman --version          # Container runtime (Podman 4.0+)
podman-compose --version  # Container orchestration
git --version             # Version control

# VCS Provider CLI (one of):
gh --version              # GitHub CLI (for GitHub repos)
# OR
az --version              # Azure CLI (for Azure DevOps repos)
az extension add --name azure-devops  # Required extension for Azure DevOps
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

3. **Test MCP manager:**
   ```bash
   podman-compose run --rm dev python mcp_manager.py --status
   ```

4. **Run validation scripts:**
   ```bash
   podman-compose run --rm dev ./validate_documentation.sh
   ```

## Development Workflow

This repository uses a contrib branch workflow for personal contributions:

### Branch Structure

```
main (production)
  ↑
develop (integration)
  ↑
contrib/stharrold (active development)
  ↑
feature/* (individual features via worktrees)
```

### Creating a Feature Branch

```bash
# Option 1: Using workflow tool (recommended)
podman-compose run --rm dev python .gemini/skills/git-workflow-manager/scripts/create_worktree.py feature my-feature contrib/stharrold

# Option 2: Manual worktree creation
git worktree add ../stharrold-templates.worktrees/my-feature -b feat/my-feature
```

### Daily Maintenance

```bash
# Rebase contrib branch onto develop
git checkout contrib/stharrold
git fetch origin
git rebase origin/develop
git push origin contrib/stharrold --force-with-lease
```

### Pull Request Flow

1. **Feature → contrib/stharrold**: After feature implementation
2. **contrib/stharrold → develop**: When ready for integration
3. **develop → main**: For production releases

## MCP Server Contributions

### Adding New MCP Server Templates

When adding templates for new MCP servers:

1. **Document in docs/guides/**
   - Create guide following modular GEMINI.md pattern
   - Keep file size ≤30KB for AI context optimization
   - Include server configuration, credentials, platform compatibility

2. **Test on all platforms:**
   - Gemini Code CLI (`~/.gemini.json`)
   - VS Code MCP Extension (platform-specific paths)
   - Gemini Desktop (platform-specific paths)

3. **Update mcp_manager.py if needed:**
   - Add platform detection logic
   - Handle new credential types
   - Test deduplication logic

### MCP Configuration Standards

**JSON Structure:**
```json
{
  "mcpServers": {  // or "servers" for VS Code
    "server-name": {
      "command": "command",
      "args": ["arg1", "arg2"],
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

**Credential Management:**
- Use keychain/credential manager (not plaintext)
- Document required environment variables
- Test with `mcp_manager.py --check-credentials`

## Documentation Requirements

### Modular GEMINI.md Pattern

All directories must have:

1. **GEMINI.md** - AI context and navigation
   - YAML frontmatter with type, parent, children
   - Cross-references to related concepts
   - Command examples and workflows

2. **README.md** - Human-readable documentation
   - YAML frontmatter with directory metadata
   - Detailed explanations and tutorials
   - Usage examples

3. **ARCHIVED/** - Deprecated files subdirectory

### File Size Constraints

- All files in `docs/guides/` must be ≤30KB
- Use modular structure with cross-references
- ARCHIVED/ uses compressed date-based archives (YYYYMMDD.tar.gz)
  - Archives are located in the `ARCHIVED/` directory at the repository root
  - To extract an archive: `tar -xzf ARCHIVED/YYYYMMDD.tar.gz` (Unix-like systems)

### Validation

Before committing documentation changes:

```bash
./validate_documentation.sh  # Runs all 5 validation tests:
# - test_file_size.sh (30KB limit)
# - test_cross_references.sh (internal links)
# - test_content_duplication.sh (detect duplicates)
# - test_command_syntax.sh (validate bash commands)
# - test_yaml_structure.sh (check frontmatter)
```

## Pull Request Process

### 1. Create Pull Request

```bash
# Push feature branch
git push origin feat/my-feature

# Create PR to contrib/stharrold
gh pr create \
  --title "feat: descriptive title" \
  --body "Detailed description" \
  --base contrib/stharrold
```

### 2. PR Requirements

- [ ] All validation scripts pass
- [ ] MCP manager functional (if Python changes)
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] Dependencies added to pyproject.toml if needed

### 3. Commit Message Format

```
<type>(<scope>): <subject>

<body>

Closes #issue-number

🤖 Generated with [Gemini Code](https://gemini.com/gemini-code)

Co-Authored-By: Gemini <noreply@anthropic.com>
```

**Types:** feat, fix, docs, style, refactor, test, chore

### 4. Review Process

- Self-merge enabled for personal contrib branches
- Request review for significant changes
- Address feedback before merge

### 5. After Merge

```bash
# Cleanup worktree and branches
git worktree remove ../stharrold-templates.worktrees/my-feature
git branch -D feat/my-feature
git push origin --delete feat/my-feature
```

## Quality Standards

### Python Code Standards

**Core Principles:**
- **Containerized**: Use podman-compose for all development
- **Cross-platform**: Works on macOS, Linux, Windows
- **One way to run**: Always use `podman-compose run --rm dev <command>`
- **Error handling**: Comprehensive try/except with clear messages

**Quality Tools:**
```bash
# Linting with ruff
podman-compose run --rm dev ruff check .
podman-compose run --rm dev ruff check --fix .

# Testing with pytest
podman-compose run --rm dev pytest
podman-compose run --rm dev pytest --cov=. --cov-report=term
```

### Documentation Standards

**GEMINI.md Files:**
- Purpose-focused (what this directory contains)
- Command-focused (quick reference)
- Navigation-focused (where to go next)
- Context-optimized (≤30KB)

**README.md Files:**
- Explanation-focused (why and how)
- Tutorial-focused (step-by-step guides)
- Reference-focused (complete documentation)
- Human-optimized (no size limit)

### Testing Standards

**Manual Testing:**
```bash
# MCP manager functionality
podman-compose run --rm dev python mcp_manager.py --status
podman-compose run --rm dev pytest test_mcp_deduplication.py

# Documentation validation
podman-compose run --rm dev ./validate_documentation.sh

# Workflow tools
podman-compose run --rm dev python .gemini/skills/workflow-utilities/scripts/archive_manager.py list
podman-compose run --rm dev python .gemini/skills/git-workflow-manager/scripts/semantic_version.py develop v5.0.0
```

**Automated Testing (CI/CD):**
- GitHub Actions runs on push/PR (same podman-compose setup)
- Azure Pipelines available (same podman-compose setup)
- Must pass before merge

## Workflow Tools Integration

This repository includes workflow automation tools in `.gemini/skills/`:

### Using Workflow Tools

```bash
# Archive management
podman-compose run --rm dev python .gemini/skills/workflow-utilities/scripts/archive_manager.py list

# Directory structure validation
podman-compose run --rm dev python .gemini/skills/workflow-utilities/scripts/directory_structure.py docs/guides/

# Version consistency checking
podman-compose run --rm dev python .gemini/skills/workflow-utilities/scripts/validate_versions.py

# Semantic versioning
podman-compose run --rm dev python .gemini/skills/git-workflow-manager/scripts/semantic_version.py develop v5.0.0

# Worktree creation
podman-compose run --rm dev python .gemini/skills/git-workflow-manager/scripts/create_worktree.py feature my-feature contrib/stharrold
```

### NOT Included from German Workflow

The following are intentionally NOT integrated:
- BMAD planner (Python project focus)
- SpecKit author (Python project focus)
- Quality enforcer with pytest (overkill for documentation)
- AgentDB state manager (external dependency)
- Full 6-phase workflow orchestrator (not applicable)

See `docs/reference/german-workflow-v5.3.0.md` for complete workflow documentation.

## AI Configuration Guidelines

### Where to Make Changes

| To change... | Edit this | NOT this |
|--------------|-----------|----------|
| Skills | `.gemini/skills/` | `.agents/` |
| Commands | `.gemini/commands/` | N/A |
| Root instructions | `GEMINI.md` | `AGENTS.md` |

### Why?

- `.gemini/` is the **PRIMARY** source
- `.agents/` is automatically synced (read-only mirror)
- `AGENTS.md` is automatically generated from `GEMINI.md`

Changes to `.agents/` or `AGENTS.md` will be overwritten on next sync.

### Sync Mechanism

The sync happens:
1. **Pre-commit hook** - `sync-ai-config` runs automatically
2. **Manual** - `uv run python .gemini/skills/workflow-utilities/scripts/sync_ai_config.py sync`
3. **PR workflow** - `pr_workflow.py sync-agents` during integration

## Questions or Issues?

- Open an issue on GitHub
- Check GEMINI.md for detailed guidance
- Review existing PRs for examples

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
