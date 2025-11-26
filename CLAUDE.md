---
type: claude-context
directory: .
purpose: Research paper on YuiQuery healthcare analytics - documentation-only repository
parent: null
sibling_readme: README.md
children:
  - .claude/CLAUDE.md
  - docs/CLAUDE.md
  - scripts/CLAUDE.md
  - tools/CLAUDE.md
related_skills:
  - workflow-orchestrator
  - quality-enforcer
  - git-workflow-manager
---

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research project focused on natural language to SQL in healthcare, specifically a whitepaper demonstrating the YuiQuery system. The repository contains academic documentation and research materials rather than executable code.

**Critical Context:** This is a documentation-only repository (no source code to compile/run). All "development" is documentation writing, validation, and workflow automation.

## Repository Structure

- **Primary Research Document**:
  - `paper.md` - Comprehensive academic research paper on YuiQuery healthcare analytics
  - Contains: literature review, empirical validation, case studies, 111 academic and industry citations

- **Project Management**:
  - `README.md` - Project overview and quick start guide
  - `CLAUDE.md` - AI assistant instructions (this file)
  - `TODO.md` - Task management documentation (points to GitHub Issues)
  - `DECISION_LOG.json` - Project decision history
  - `project-management/` - Detailed PM artifacts (budget, risks, roles, quality gates)
  - `ARCHIVED/TODO/` - Historical TODO files (deprecated, now using GitHub Issues)

- **Code & Automation**:
  - `scripts/` - GitHub sync automation (Python, uses stdlib only)
  - `tools/validation/` - Documentation quality validation scripts (bash)
  - `tools/workflow-utilities/` - Archive management and version checking
  - `.claude/skills/` - Workflow automation skills (9 skills, v5.15.0)
  - `.agents/` - Mirror of .claude/skills/ for cross-tool compatibility
  - `.claude/commands/workflow/` - Workflow slash commands (8 phase-based commands)

- **Research Supporting Materials**:
  - `src/` - Algorithms, analysis code, and schema mapping
  - `docs/` - Paper versions, figures, and reference materials
  - `images/` - YuiQuery feature diagrams and screenshots
  - `compliance/` - IRB determinations and HIPAA documentation
  - `config/` - Database and query configuration
  - `archive/` - Historical files and backups

## Project Context

This repository documents research on YuiQuery, a conversational AI platform for healthcare analytics that addresses three key challenges:
1. Low healthcare analytics maturity
2. Healthcare workforce turnover and institutional memory loss
3. Technical barriers in natural language to SQL generation

The literature review synthesizes findings from systematic reviews, peer-reviewed journals, and industry sources to provide evidence for implementing conversational AI platforms in healthcare settings.

## Zero Runtime Dependencies Architecture

**Design Principle:** Automation scripts (`scripts/`, `tools/`) use **Python stdlib only**. Workflow skills (`.claude/skills/`) may require optional dependencies.

**Core Scripts (Zero Dependencies):**
- `scripts/sync_github_todos.py` - GitHub Issues sync
- `tools/validation/*` - Documentation validation tests

**Workflow Skills (Optional Dependencies):**
- `.claude/skills/agentdb-state-manager/` - Requires `duckdb>=1.4.0`
- Install: `uv sync --extra workflow`

**When adding new automation scripts:** Use only Python stdlib (`sys, os, subprocess, json, pathlib`). NO external packages.

## Branch Strategy

### Branch Structure

```
main (production) ← release/* ← develop (integration) ← contrib/stharrold (active) ← feature/*
```

**PR Flow**: `feature → contrib → develop → release/* → main`

**Branch Editability:**
| Branch | Editable | Direct Commits |
|--------|----------|----------------|
| `feature/*` | Yes | Yes |
| `contrib/*` | Yes | Yes |
| `develop` | No | PRs only |
| `release/*` | Ephemeral | Created from develop, deleted after merge |
| `main` | No | PRs only |

**Workflow:**
- Daily work: `contrib/stharrold` (or `feature/*` branches)
- Integration: PR `contrib/stharrold` → `develop`
- Releases: Create `release/vX.Y.Z` from `develop`, PR to `main`, tag after merge
- Backmerge: After release, PR `release/*` → `develop`, then delete release branch
- Use git-workflow-manager for complex operations

## Containerized Development (Recommended)

**Key Principle**: All development uses `podman-compose run --rm dev <command>`. One way to run everything.

### Setup
```bash
# Build container (once)
podman-compose build

# Verify setup
podman-compose run --rm dev uv --version
podman-compose run --rm dev ./validate_documentation.sh
```

### Code Quality
```bash
podman-compose run --rm dev uv run ruff format .      # Format Python
podman-compose run --rm dev uv run ruff check --fix . # Lint and auto-fix
podman-compose run --rm dev uv run mypy scripts/      # Type checking
```

### Quality Gates (6 gates, all must pass before PR)
```bash
podman-compose run --rm dev python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

| Gate | Description |
|------|-------------|
| 1. Documentation | All validation tests pass |
| 2. Linting | `ruff check .` clean |
| 3. Types | `mypy scripts/` passes |
| 4. Coverage | ≥80% test coverage (if tests exist) |
| 5. Tests | All pytest tests pass (if tests exist) |
| 6. Build | `uv build` succeeds |

**Note:** This is a documentation-only repository. Gates 4-5 (coverage/tests) pass automatically when no test directory exists. The quality-enforcer script auto-detects if podman-compose is unavailable and falls back to local `uv run` commands.

## Local Development (Alternative)

If you prefer running without containers:

### Setup
```bash
uv sync                              # Install dev dependencies
./validate_documentation.sh          # Verify documentation quality
```

### Code Quality
```bash
uv run ruff format .                 # Format Python (Black-compatible)
uv run ruff check --fix .            # Lint and auto-fix
uv run mypy scripts/                 # Type checking
```

### Task Management (GitHub Issues)
```bash
gh issue list                        # View all open issues
gh issue list --label "P0"          # Critical priority tasks
gh issue list --label "P1"          # High priority tasks
gh issue view <number>               # View specific issue details
gh issue comment <number> --body "Update..."  # Add progress update
gh issue close <number> --comment "Done"      # Close completed task
```

### Validation Tests
```bash
tools/validation/test_file_size.sh              # Check 30KB limit
tools/validation/test_cross_references.sh       # Validate markdown links
tools/validation/test_content_duplication.sh    # Detect duplicates
tools/validation/test_command_syntax.sh         # Validate bash blocks
tools/validation/test_yaml_structure.sh         # Check JSON structure
./validate_documentation.sh                     # Run all 5 tests
```

### Document Generation
```bash
# Basic PDF
pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.pdf

# Professional PDF (requires Eisvogel template)
pandoc paper.md -o output.pdf --template=eisvogel --pdf-engine=xelatex --listings --toc --number-sections

# HTML for web
pandoc paper.md -o output.html --standalone --toc --self-contained
```

## Key Architectural Systems

### Task Management with GitHub Issues

**Current System (as of 2025-11-21):** GitHub Issues are the single source of truth for all tasks.

**Task Workflow:**
1. **Find tasks:** `gh issue list --state open`
2. **View details:** `gh issue view <number>`
3. **Work on task:** Follow instructions in issue body (includes Claude Code context)
4. **Update progress:** `gh issue comment <number> --body "Progress: ..."`
5. **Complete task:** `gh issue close <number> --comment "Completed: <summary>"`

**Priority Labels:**
- `P0` - Critical (immediate attention)
- `P1` - High (next sprint)
- `P2` - Medium (backlog)

**Task Context:**
Each GitHub Issue includes comprehensive context for Claude Code:
- Full task description
- Repository patterns and validation requirements
- Expected deliverables
- Development workflow instructions

**Historical Note:** Previously used `TODO_FOR_AI.json` (deprecated 2025-11-21, archived in `ARCHIVED/TODO/`).

### Documentation Validation Architecture

**Orchestrator:** `./validate_documentation.sh` (symlink to `tools/validation/validate_documentation.sh`)

**5 Validation Tests:**
1. **test_file_size.sh** - Enforces 30KB limit on modular docs (AI context optimization)
2. **test_cross_references.sh** - Validates internal markdown links
3. **test_content_duplication.sh** - Detects duplicate sections
4. **test_command_syntax.sh** - Validates bash code blocks
5. **test_yaml_structure.sh** - Checks JSON/YAML structure

**Run before all commits affecting documentation.**

### Workflow Skills System (v5.15.0)

**9 Skills Available in `.claude/skills/`:**

**Core:** workflow-orchestrator, git-workflow-manager, workflow-utilities, initialize-repository
**Planning:** bmad-planner (requirements/architecture/epics), speckit-author (specifications)
**Quality:** quality-enforcer (gates), tech-stack-adapter (stack detection), agentdb-state-manager (state sync)

**Workflow Commands** (`.claude/commands/workflow/`):
- `/workflow/all` - Complete workflow orchestration (auto-detect state, continue)
- `/workflow/1_specify` - Feature specification creation
- `/workflow/2_plan` - Implementation planning
- `/workflow/3_tasks` - Task breakdown generation
- `/workflow/4_implement` - Implementation guidance
- `/workflow/5_integrate` - Integration and PR creation
- `/workflow/6_release` - Release branch workflow
- `/workflow/7_backmerge` - Back-merge after release

**When to Use:**
- Major releases and complex git operations
- Semantic versioning for documentation releases
- Structured planning for major paper revisions
- Quality gates integration

**When NOT to Use:**
- Daily paper edits, minor citation updates, routine documentation

See individual `SKILL.md` files in `.claude/skills/` for detailed usage.

## Project Patterns

### File Naming Conventions
- **Research Documents**: Descriptive names with `.md` extension (`paper.md`)
- **Timestamp Format**: `YYYYMMDDTHHMMSSZ_` prefix for historical files
- **Project Management**: Uppercase names (`TODO_FOR_AI.json`, `DECISION_LOG.json`)

### Document Organization
- **Academic Structure**: Standard format (abstract, intro, lit review, methods, results, discussion, conclusion)
- **Citation Format**: `[A#]` for academic, `[I#]` for industry sources
- **Evidence Integration**: Combine peer-reviewed research with real-world case studies
- **Directory README Pattern**: Every major directory has README.md explaining contents

### Content Development
- **Systematic Methodology**: PRISMA guidelines for literature reviews
- **Evidence Synthesis**: Multiple source types (journals, industry reports, case studies)
- **Quantitative Validation**: Specific metrics with statistical significance (83% reduction, p<0.001)
- **Healthcare Context**: Frame findings within healthcare-specific challenges

## Common Issues & Solutions

### Citation Management
**Issue**: Managing 111+ sources across academic and industry categories
**Solution**:
- Separate `[A#]` and `[I#]` citation systems
- Structured bibliography with DOI links

### Document Coherence
**Issue**: Maintaining narrative flow when merging documents
**Solution**:
- Use three-pillar framework (maturity, turnover, technical barriers)
- Transitional sections connecting evidence domains
- Consistent terminology throughout

### Task Management
**Current Approach:** Direct GitHub Issues management via `gh` CLI
**Reference:** See `TODO.md` for historical migration details

## Project Requirements

### Healthcare Domain Knowledge
- **Medical Terminology**: ICD-10, CPT, SNOMED, RxNorm vocabularies
- **Healthcare IT Standards**: HIMSS AMAM, HL7, FHIR
- **Clinical Workflows**: Clinical decision-making processes
- **Regulatory Context**: HIPAA, data governance, compliance

### Academic Quality Standards
- **Systematic Review**: Follow established guidelines
- **Statistical Reporting**: Include confidence intervals, p-values, effect sizes
- **Evidence Hierarchy**: Prioritize RCTs and systematic reviews
- **Conflict of Interest**: Clearly identify potential conflicts

### Technical Accuracy
- **NL2SQL Technology**: Current state of natural language to SQL
- **Healthcare Analytics Maturity**: HIMSS AMAM stages correctly
- **Implementation Complexity**: Realistic challenges and timelines
- **ROI Calculations**: Based on documented case studies

### Business Logic Constraints
- **Three-Pillar Framework**: Connect to core challenges (maturity, turnover, barriers)
- **Evidence-Based Claims**: Support with cited research
- **Healthcare Focus**: Maintain healthcare-specific focus
- **Practical Implementation**: Balance theory with actionable recommendations

## Development Environment Setup

### Prerequisites
- **UV Package Manager**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Python 3.11+**: Minimum version (UV handles installation)
- **GitHub CLI**: `brew install gh` + `gh auth login`
- **Podman** (optional): `brew install podman && podman machine init && podman machine start`
- **Pandoc** (optional): For PDF/HTML generation

### First-Time Setup (Container - Recommended)
```bash
# Clone repository
git clone <repo-url>
cd yuimedi-paper-20250901

# Build container (once)
podman-compose build

# Verify setup
podman-compose run --rm dev uv --version
podman-compose run --rm dev ./validate_documentation.sh

# Run any command
podman-compose run --rm dev <command>
```

### First-Time Setup (Local - Alternative)
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone <repo-url>
cd yuimedi-paper-20250901
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Verify
uv run python --version
./validate_documentation.sh
```

### Pre-commit Hooks

Pre-commit hooks run automatically on `git commit`:
- **trailing-whitespace, end-of-file-fixer** - Basic formatting
- **ruff** - Python linting and formatting
- **sync-ai-config** - Syncs CLAUDE.md → AGENTS.md, .agents/
- **claude-md-frontmatter** - Validates YAML frontmatter in CLAUDE.md files
- **skill-structure** - Validates .claude/skills/ directory structure

Run manually: `uv run pre-commit run --all-files`

### Container Command Patterns
```bash
# All development through container
podman-compose run --rm dev uv run pytest              # Run tests
podman-compose run --rm dev uv run ruff format .       # Format code
podman-compose run --rm dev uv run ruff check --fix .  # Lint
podman-compose run --rm dev uv run mypy scripts/       # Type check
podman-compose run --rm dev ./validate_documentation.sh # Doc validation

# Interactive shell
podman-compose run --rm dev bash
```

### UV Environment Management (Local)
```bash
uv sync                          # Install/sync dependencies
uv run python script.py          # Run script in UV environment
uv run ruff format .             # Format code
uv run ruff check --fix .        # Lint and auto-fix
uv run mypy scripts/             # Type checking
uv add --dev <package>           # Add dev dependency
```

**Command Pattern:** Use `podman-compose run --rm dev <command>` (container) or `uv run <command>` (local)

## Advanced Issues Discovered

### Python Version Compatibility
**Issue**: Python 3.6 compatibility errors
**Solution**: Implemented UV environment with Python 3.9+ requirement
**Prevention**: Always specify minimum Python version in pyproject.toml

### Python Tooling Migration
**Issue**: Black + Flake8 slower performance
**Solution**: Migrated to Ruff (10-100x faster, Black-compatible)
**Prevention**: Use modern, unified tooling from the start

### TODO Management Migration (2025-11-21)
**Issue**: Duplicate tasks in TODO_FOR_AI.json
**Solution**: Migrated to GitHub Issues as single source of truth
**Reference**: See `TODO.md` for migration details

## Citation Reference Format

- **Academic Sources**: `[A1]`, `[A2]`, etc. → References > Academic Sources
- **Industry Sources**: `[I1]`, `[I2]`, etc. → References > Industry Sources
- **Internal References**: Section numbers for cross-document navigation

## Data Structures

- **GitHub Issues**: Primary task tracking with priority labels (P0/P1/P2)
- **DECISION_LOG.json**: Decision history with rationale, alternatives, tradeoffs
- **ARCHIVED/TODO/**: Historical TODO files (deprecated 2025-11-21)
- **Version Control**: Semantic versioning (v1.0 through v1.6.0+)

## AI Config Sync

The repository maintains parallel AI configuration directories:
- `CLAUDE.md` → `AGENTS.md` (for cross-tool compatibility)
- `.claude/skills/` → `.agents/` (mirror of workflow skills)
- `.claude/commands/` → `.agents/commands/` (mirror of slash commands)

**Sync after changes:**
```bash
rsync -av --delete --exclude=".DS_Store" --exclude="__pycache__" .claude/skills/ .agents/
rsync -av --delete --exclude=".DS_Store" --exclude="__pycache__" .claude/commands/ .agents/commands/
cp CLAUDE.md AGENTS.md
```
