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
  - `.claude/skills/` - Workflow automation skills (9 skills, standard-workflow v1.15.1)
  - `.claude/commands/` - Slash commands (/plan, /specify, /tasks)

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

**Design Principle:** All automation scripts (`scripts/`, `tools/`) use **Python stdlib only**.

**Rationale:**
- Ensures scripts run on any Python 3.9+ installation
- No dependency management for automation utilities
- Reduces maintenance burden and security surface

**Development Tools (Optional):**
- Ruff (formatting + linting) - via UV
- MyPy (type checking) - via UV
- Pandoc (document generation) - system install

**When adding new scripts:** Use `import sys, os, subprocess, json, pathlib` etc. NO external packages.

## Branch Strategy

**Active Branch:** `contrib/stharrold` (default for development)
**Integration Branch:** `main`
**Release Management:** Semantic versioning via git tags

**Workflow:**
- Daily work: `contrib/stharrold`
- Major releases: Create PR to `main`, tag after merge
- Use git-workflow-manager for complex operations

## Common Development Commands

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

**Historical Note:** Previously used `TODO_FOR_AI.json` with bidirectional sync (`scripts/sync_github_todos.py`). This workflow was deprecated on 2025-11-21 due to duplicate task entries (47.8% deduplication achieved). Old TODO files archived in `ARCHIVED/TODO/` for reference.

### Documentation Validation Architecture

**Orchestrator:** `./validate_documentation.sh` (symlink to `tools/validation/validate_documentation.sh`)

**5 Validation Tests:**
1. **test_file_size.sh** - Enforces 30KB limit on modular docs (AI context optimization)
2. **test_cross_references.sh** - Validates internal markdown links
3. **test_content_duplication.sh** - Detects duplicate sections
4. **test_command_syntax.sh** - Validates bash code blocks
5. **test_yaml_structure.sh** - Checks JSON/YAML structure

**Run before all commits affecting documentation.**

### Workflow Skills System (standard-workflow v1.15.1)

**9 Skills Available in `.claude/skills/`:**

**Core:** workflow-orchestrator, git-workflow-manager, workflow-utilities, initialize-repository
**Planning:** bmad-planner (requirements/architecture/epics), speckit-author (specifications)
**Quality:** quality-enforcer (gates), tech-stack-adapter (stack detection), agentdb-state-manager (state sync)

**3 Slash Commands:**
- `/plan` - Implementation planning workflow
- `/specify` - Feature specifications
- `/tasks` - Dependency-ordered task generation

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
**Current Approach:** Direct GitHub Issues management (no sync needed)
**Migration Note:** Previous bidirectional sync (TODO_FOR_AI.json ↔ GitHub Issues) deprecated 2025-11-21
**Reference:** See `TODO.md` for migration details and archived files

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
- **UV Package Manager** (required): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Python 3.9+**: Minimum version (UV handles installation)
- **GitHub CLI**: `brew install gh` + `gh auth login`
- **Pandoc** (optional): For PDF/HTML generation

### First-Time Setup
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone <repo-url>
cd yuimedi-paper-20250901
uv sync

# Verify
uv run python --version
./validate_documentation.sh
```

### UV Environment Management
```bash
uv sync                          # Install/sync dependencies
uv run python script.py          # Run script in UV environment
uv run ruff format .             # Format code
uv run ruff check --fix .        # Lint and auto-fix
uv run mypy scripts/             # Type checking
uv add --dev <package>           # Add dev dependency
```

**Command Pattern:** Always use `uv run python <script>` instead of bare `python3`

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
**Issue**: Duplicate tasks in TODO_FOR_AI.json (69 items, 33 duplicates)
**Solution**: Migrated to GitHub Issues as single source of truth (36 unique issues)
**Benefits**: 47.8% deduplication, better collaboration, comprehensive Claude Code context
**Reference**: See `TODO.md` and commit 285de29 for migration details

## Citation Reference Format

- **Academic Sources**: `[A1]`, `[A2]`, etc. → References > Academic Sources
- **Industry Sources**: `[I1]`, `[I2]`, etc. → References > Industry Sources
- **Internal References**: Section numbers for cross-document navigation

## Data Structures

- **GitHub Issues**: Primary task tracking (replaces TODO_FOR_AI.json as of 2025-11-21)
  - Priority labels: P0 (critical), P1 (high), P2 (medium)
  - Each issue includes comprehensive Claude Code context
  - View: `gh issue list` or https://github.com/stharrold/yuimedi-paper-20250901/issues
- **TODO.md**: Task management documentation (points to GitHub Issues, includes migration details)
- **DECISION_LOG.json**: Decision history with rationale, alternatives, tradeoffs
- **ARCHIVED/TODO/**: Historical TODO files (deprecated 2025-11-21)
  - `20251121T095620Z_TODO_FOR_AI.json` - 169 tasks (100 done, 69 migrated)
  - `20251121T095620Z_TODO_FOR_HUMAN.md` - Human-readable version
- **Version Control**: Semantic versioning for major releases (v1.0, v1.1, v1.2, etc.)
