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
  - `TODO_FOR_AI.json` - Structured task tracking (synced with GitHub Issues)
  - `TODO_FOR_HUMAN.md` - Human-readable task list
  - `DECISION_LOG.json` - Project decision history
  - `project-management/` - Detailed PM artifacts (budget, risks, roles, quality gates)
  - `project-management.md` - Executive summary and strategic overview

- **Code & Automation**:
  - `scripts/` - GitHub sync automation (Python, uses stdlib only)
  - `tools/validation/` - Documentation quality validation scripts (bash)
  - `tools/workflow-utilities/` - Archive management and version checking

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

## Development Notes

**Key Architectural Decision**: This is primarily a documentation repository. Python automation scripts (`scripts/`, `tools/`) use **only Python standard library** - no external dependencies. Development tools (Ruff, MyPy) are optional and managed via UV.

When working with this repository, focus on:
- Maintaining academic citation formatting (`[A#]` for academic, `[I#]` for industry sources)
- Preserving document structure and organization
- Running validation scripts before commits
- Using UV for all Python script execution: `uv run python script.py`

## Project Patterns Discovered

### File Naming Conventions
- **Research Documents**: Use descriptive names with `.md` extension (`paper.md`, not `whitepaper.md`)
- **Timestamp Format**: Historical research files used `YYYYMMDDTHHMMSSZ_` prefix (now consolidated)
- **Project Management**: Descriptive uppercase names (`TODO_FOR_AI.json`, `DECISION_LOG.json`)

### Document Organization Patterns
- **Academic Structure**: Follow standard academic paper format (abstract, introduction, literature review, methods, results, discussion, conclusion)
- **Citation Format**: Use `[A#]` for academic sources, `[I#]` for industry sources throughout text
- **Evidence Integration**: Combine peer-reviewed research with real-world case studies for comprehensive validation
- **Appendices**: Include domain-specific glossaries and practical examples

### Directory README Pattern
**Every major directory contains a README.md** explaining its purpose and contents:
- `src/README.md` - Development environment, algorithms overview, healthcare adaptations
- `docs/README.md` - Paper management, submission targets, version control
- `compliance/README.md` - IRB status, HIPAA compliance, regulatory requirements
- `config/README.md` - Database configuration, security requirements, data sources
- `archive/README.md` - Retention policy, file recovery, historical tracking
- `project-management/README.md` - PM methodology, artifact relationships
- `tools/validation/README.md` - Validation test descriptions and usage
- `docs/references/README.md` - Citation management and reference tracking

This pattern ensures every directory is self-documenting and navigable.

### Content Development Approach
- **Systematic Methodology**: Use systematic literature review approach with PRISMA guidelines
- **Evidence Synthesis**: Integrate multiple source types (academic journals, industry reports, case studies)
- **Quantitative Validation**: Include specific metrics and statistical significance (83% reduction, p<0.001)
- **Healthcare Context**: Always frame findings within healthcare-specific challenges and terminology

## Common Issues & Solutions

### Citation Management Challenges
**Issue**: Managing 111+ sources across academic and industry categories
**Root Cause**: Large evidence base with mixed source types and formats
**Solution**: 
- Separate academic `[A#]` and industry `[I#]` citation systems
- Maintain consistent formatting within each category
- Use structured bibliography with DOI links where available

### Document Coherence During Merge
**Issue**: Maintaining narrative flow when consolidating separate research documents
**Root Cause**: Different writing styles and focus areas in original documents
**Solution**:
- Create overarching framework (three-pillar challenge model)
- Use transitional sections to connect different evidence domains
- Maintain consistent terminology throughout merged document

### Academic vs. Industry Evidence Balance
**Issue**: Balancing peer-reviewed research with real-world implementation evidence
**Root Cause**: Academic sources provide rigor, industry sources provide practical validation
**Solution**:
- Use academic sources for theoretical foundation and methodology
- Use industry sources for case studies and ROI validation
- Clearly distinguish between empirical research findings and practitioner reports

## Project-Specific Requirements

### Healthcare Domain Knowledge
- **Medical Terminology**: Must accurately use ICD-10, CPT, SNOMED, RxNorm vocabularies
- **Healthcare IT Standards**: Reference HIMSS AMAM, HL7, FHIR standards appropriately
- **Clinical Workflows**: Understand and accurately represent clinical decision-making processes
- **Regulatory Context**: Account for HIPAA, data governance, and healthcare compliance requirements

### Academic Quality Standards
- **Systematic Review Methodology**: Follow established guidelines for literature reviews
- **Statistical Reporting**: Include confidence intervals, p-values, and effect sizes where appropriate
- **Evidence Hierarchy**: Prioritize randomized controlled trials and systematic reviews
- **Conflict of Interest**: Clearly identify any potential conflicts with YuiQuery platform

### Technical Accuracy Requirements
- **NL2SQL Technology**: Accurately represent current state of natural language to SQL generation
- **Healthcare Analytics Maturity**: Correctly describe HIMSS AMAM stages and organizational capabilities
- **Implementation Complexity**: Realistically portray challenges and timelines for conversational AI adoption
- **ROI Calculations**: Ensure financial projections are based on documented case studies

### Business Logic Constraints
- **Three-Pillar Framework**: All arguments must connect to core challenges (maturity, turnover, technical barriers)
- **Evidence-Based Claims**: Every recommendation must be supported by cited research
- **Healthcare Focus**: Maintain focus on healthcare-specific applications rather than general AI
- **Practical Implementation**: Balance theoretical research with actionable recommendations

## API Contracts & Data Formats

### Document Generation (Pandoc)
```bash
# Basic PDF generation
pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.pdf

# Professional academic formatting
pandoc paper.md -o output.pdf \
  --template=eisvogel \
  --pdf-engine=xelatex \
  --listings \
  --toc \
  --number-sections
```

### Citation Reference Format
- **Academic Sources**: `[A1]`, `[A2]`, etc. in text, with full citations in References > Academic Sources
- **Industry Sources**: `[I1]`, `[I2]`, etc. in text, with full citations in References > Industry Sources
- **Internal References**: Section numbers and page references for cross-document navigation

### Project Management Data Structures
- **TODO_FOR_AI.json**: Structured task tracking with priority, effort estimates, and technical context
- **DECISION_LOG.json**: Decision history with rationale, alternatives, tradeoffs, and reversibility
- **GitHub Issues Integration**: Bidirectional sync between local TODO files and GitHub Issues
- **Version Control**: Use semantic versioning for major document releases (v1.0, v1.1, etc.)

## Development Environment Patterns

### UV Environment Management (Required)
- **Python Version Control**: Use UV to ensure Python 3.9+ compatibility across team members
- **Dependency Isolation**: Zero runtime dependencies, optional dev dependencies for code quality
- **Automatic Virtual Environments**: UV creates and manages .venv automatically
- **Development Tools**: Ruff (formatting + linting), MyPy (type checking), Pre-commit hooks
- **Command Pattern**: Always use `uv run python <script>` instead of bare `python3`

**Key UV Commands:**
```bash
uv sync                          # Install/sync all dependencies
uv run python script.py          # Run script in UV environment
uv run ruff format .             # Format code (Black-compatible)
uv run ruff check .              # Lint code (replaces flake8 + isort)
uv run ruff check --fix .        # Auto-fix linting issues
uv run mypy scripts/             # Type checking
uv add --dev <package>           # Add dev dependency
```

### GitHub Integration Workflow
- **Bidirectional Sync**: `./scripts/sync_todos.sh` creates GitHub Issues from TODO tasks and syncs back
- **Metadata-Driven Issues**: GitHub Issues include structured metadata comments for priority and status
- **Automatic Backup**: System creates timestamped backups before any sync operations
- **Error Recovery**: Automatic restoration of backups if sync operations fail

**Sync Architecture** (`scripts/sync_github_todos.py`):
```python
# YuiQueryGitHubSync class - Pure Python stdlib implementation
# Sync Flow (5 phases):
#   Phase 0: Backup existing TODO files to .todo_backups/
#   Phase 1: fetch_github_issues() → Fetch all issues via gh CLI
#   Phase 2: sync_to_github() → Create missing GitHub Issues from TODO tasks
#   Phase 3: sync_from_github() → GitHub Issues → TODO_FOR_AI.json
#   Phase 4: generate_human_readable() → TODO_FOR_AI.json → TODO_FOR_HUMAN.md
#   Phase 5: Validate consistency between GitHub and local files

# Critical Implementation Detail:
# - Uses issue['state'].upper() for case-insensitive comparison
# - GitHub returns 'CLOSED', not 'closed' (previously caused sync bugs)
# - Line 97: if issue['state'].upper() == 'CLOSED': metadata['status'] = 'done'
```

## Advanced Issues & Solutions Discovered

### Python Version Compatibility Challenges
**Issue**: Python 3.6 compatibility error with `subprocess.run(text=True)` parameter
**Root Cause**: User environment had anaconda Python 3.6, but scripts required Python 3.7+ features
**Solution**:
- Implemented UV environment with Python 3.9+ requirement in pyproject.toml
- Updated scripts to use UV environment automatically
- Added environment validation to sync scripts
- Documented UV setup process in all guides

**Prevention**: Always specify minimum Python version in pyproject.toml (currently 3.9+)

### Python Tooling Migration
**Issue**: Black + Flake8 provided separate formatting and linting with slower performance
**Root Cause**: Multiple tools doing similar work, legacy Python tooling choices
**Solution**:
- Migrated to Ruff for both formatting and linting (10-100x faster)
- Configured Ruff with Black-compatible formatting rules
- Enabled comprehensive linting rules (pycodestyle, pyflakes, isort, naming, etc.)
- Maintained line-length = 100 for consistency

**Prevention**: Use modern, unified tooling (Ruff) from the start

### Empty Repository Sync Failures
**Issue**: Sync script treated empty GitHub Issues repository as failure condition
**Root Cause**: Original script design assumed existing GitHub Issues as source of truth
**Solution**:
- Modified `fetch_github_issues()` to distinguish between errors (None) and empty lists ([])
- Updated `sync_from_github()` to handle empty issues as valid state
- Implemented `sync_to_github()` to create GitHub Issues from existing TODO tasks
- Added bidirectional workflow: TODO → GitHub → TODO sync

**Prevention**: Design sync systems to handle empty initial states gracefully

### GitHub Repository Label Dependencies
**Issue**: GitHub Issue creation failed when trying to add non-existent labels
**Root Cause**: Scripts attempted to add 'research' and 'documentation' labels that didn't exist in repository
**Solution**:
- Removed automatic label assignment from GitHub Issue creation
- Made labels optional in issue creation workflow
- Documented label creation as optional setup step
- Focused on core functionality (title, body, metadata) for reliable operation

**Prevention**: Always make external dependencies (labels, assignees) optional in automated workflows

### GitHub Issue State Case Sensitivity Bug
**Issue**: Sync script wasn't marking closed GitHub Issues as "done" status in TODO files
**Root Cause**: Code used `issue['state'] == 'closed'` but GitHub API returns `'CLOSED'` (uppercase)
**Solution**:
- Updated line 97 in sync_github_todos.py to use case-insensitive comparison
- Changed to: `if issue['state'].upper() == 'CLOSED': metadata['status'] = 'done'`
- Re-ran sync to correctly mark 86 closed issues as done (previously showed as todo)

**Prevention**: Always use case-insensitive comparison for external API data

## Updated Project-Specific Requirements

### Development Environment Requirements
- **UV Package Manager**: Required for Python environment management (replaces pip/venv/pyenv)
  - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Manages Python versions automatically
  - Creates .venv on first `uv sync`
- **Python 3.9+**: Minimum version per pyproject.toml (UV handles installation if needed)
- **GitHub CLI (gh)**: Required for automated issue creation and bidirectional sync
  - Install: `brew install gh` (macOS) or see https://cli.github.com/
  - Must be authenticated: `gh auth login`
- **Git Repository**: Must be connected to GitHub remote for sync functionality
- **Pandoc** (optional): For PDF/HTML generation from paper.md

**First-Time Setup:**
```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone <repo-url>
cd yuimedi-paper-20250901

# Setup environment (creates .venv automatically)
uv sync

# Verify installation
uv run python --version
./validate_documentation.sh
```

### Academic Research Workflow Requirements
- **Systematic Methodology**: All research claims must be supported by systematic literature review evidence
- **Empirical Validation**: Include quantitative results from peer-reviewed studies and case studies
- **Healthcare Context**: Frame all technical solutions within healthcare-specific challenges and constraints
- **Publication Readiness**: Maintain academic paper structure suitable for peer review and journal submission

### Bidirectional Sync System Requirements
- **Metadata Preservation**: GitHub Issues must include priority, status, and dependency metadata in comments
- **Backup Strategy**: Always create timestamped backups before sync operations
- **Error Resilience**: Handle empty repositories, missing labels, and authentication failures gracefully
- **Validation Consistency**: Verify bidirectional sync maintains data integrity across GitHub and local files

## Common Development Tasks

### Documentation Validation
```bash
# Run all 5 validation tests (orchestrator)
./validate_documentation.sh        # Symlink to tools/validation/validate_documentation.sh

# Individual tests (now in tools/validation/)
tools/validation/test_file_size.sh                # Check 30KB limit on modular docs
tools/validation/test_cross_references.sh         # Validate internal markdown links
tools/validation/test_content_duplication.sh      # Detect duplicate sections
tools/validation/test_command_syntax.sh           # Validate bash code blocks
tools/validation/test_yaml_structure.sh           # Check JSON structure

# Note: Root-level symlink maintained for backward compatibility
# Actual scripts located in tools/validation/ directory
```

### GitHub Issue Sync
```bash
# Full bidirectional sync (recommended)
./scripts/sync_todos.sh

# Direct Python execution
uv run python scripts/sync_github_todos.py

# Verify results
gh issue list
cat TODO_FOR_HUMAN.md
```

### Code Quality Checks
```bash
# Format Python code
uv run ruff format scripts/ tools/

# Lint and auto-fix
uv run ruff check --fix scripts/ tools/

# Type checking
uv run mypy scripts/ tools/
```

### Workflow Utilities
```bash
# Archive old files
uv run python tools/workflow-utilities/archive_manager.py list
uv run python tools/workflow-utilities/archive_manager.py create <file>

# Validate directory structure (requires CLAUDE.md, README.md, ARCHIVED/)
uv run python tools/workflow-utilities/directory_structure.py <dir>

# Check version consistency across files
uv run python tools/workflow-utilities/validate_versions.py
```

### Document Generation (Pandoc)
```bash
# Basic PDF
pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.pdf

# Professional PDF (requires Eisvogel template)
pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.pdf \
  --template=eisvogel \
  --pdf-engine=xelatex \
  --listings \
  --toc \
  --number-sections

# HTML for web
pandoc paper.md -o output.html --standalone --toc --self-contained
```

## Workflow Skills and Automation

### Available Skills (9 Total)

This repository includes a comprehensive workflow automation system adapted from german-workflow v1.15.1. Skills provide specialized capabilities for project management, git operations, and quality assurance.

**Core Workflow Skills:**
- **workflow-orchestrator** - Main coordinator for multi-phase workflows
- **git-workflow-manager** - Git operations (worktree, branches, commits, PRs, semantic versioning)
- **workflow-utilities** - Shared utilities (archive management, directory structure, version validation)
- **initialize-repository** - Repository initialization and setup

**Planning and Specification Skills:**
- **bmad-planner** - BMAD planning framework (requirements, architecture, epics)
- **speckit-author** - SpecKit specifications (spec and plan generation)

**Quality and Technical Skills:**
- **quality-enforcer** - Quality gates (test coverage, linting, validation)
- **tech-stack-adapter** - Technology stack detection (Python/uv/Podman)
- **agentdb-state-manager** - DuckDB state management and synchronization

**Usage:** Skills are invoked by name when needed. Claude Code will load relevant skills based on context and task requirements.

### Available Commands (3 Slash Commands)

Progressive disclosure workflow commands for complex tasks:

- **/plan** - Execute implementation planning workflow
  - Loads plan template
  - Generates design artifacts
  - Creates tasks from implementation plan

- **/specify** - Create or update feature specifications
  - Generates feature specification from natural language
  - Uses spec template structure
  - Prepares for implementation phase

- **/tasks** - Generate dependency-ordered task lists
  - Analyzes design documents
  - Creates actionable tasks
  - Identifies parallel vs sequential work

**Usage:** Type `/plan`, `/specify`, or `/tasks` in the conversation to invoke these workflows.

### Workflow Application to This Repository

While this is a documentation-focused repository, the workflow system provides valuable capabilities:

**Git Workflow Management:**
- Daily rebase of contrib branch onto main
- Semantic versioning for documentation releases
- PR creation and management for major changes
- Release tagging for published versions

**Quality Enforcement:**
- Documentation validation (already using `./validate_documentation.sh`)
- Python code quality (Ruff, MyPy for automation scripts)
- Test coverage for workflow utilities

**Project Organization:**
- Archive management for deprecated documentation
- Directory structure validation
- Version consistency checking

**Planning Integration:**
- BMAD planning for major documentation updates
- SpecKit for new feature documentation
- Task generation for complex research integration

**When to Use:**
- **Git operations:** Use git-workflow-manager for complex branch operations
- **Documentation releases:** Use semantic versioning and release workflow
- **Large updates:** Use BMAD planning before major paper revisions
- **Validation:** Quality-enforcer already integrated with validation scripts

**When NOT to Use:**
- Simple documentation edits (use direct editing)
- Minor citation updates (no workflow overhead needed)
- Day-to-day paper writing (workflows are for releases/major changes)

## Enhanced API Contracts & Data Formats

### GitHub Issue Metadata Format
GitHub Issues must include structured metadata in HTML comments:
```markdown
<!-- priority: P0|P1|P2|P3 -->
<!-- status: todo|in_progress|blocked|done -->
<!-- depends-on: #123, #456 -->

Issue description content here...
```

### UV Environment Commands
```bash
# Environment setup
uv venv                      # Create virtual environment
uv pip install -e ".[dev]"  # Install project with dev dependencies
source .venv/bin/activate    # Activate environment

# Development workflow
uv pip install <package>     # Add new dependency
uv pip freeze > requirements.txt  # Export for reference
uv pip install -r requirements.txt  # Install from requirements
```

### Bidirectional Sync Workflow
```bash
# Complete sync workflow
./scripts/sync_todos.sh      # Run full bidirectional sync
                             # Phase 0: Backup existing TODO files
                             # Phase 1: Fetch GitHub Issues → TODO_FOR_AI.json
                             # Phase 2: Create missing GitHub Issues from TODO tasks
                             # Phase 3: Generate TODO_FOR_HUMAN.md
                             # Phase 4: Validate consistency

# Manual sync components
uv run python scripts/sync_github_todos.py  # Run sync directly (requires UV)
gh issue list --limit 100                    # Verify GitHub Issues exist
cat TODO_FOR_HUMAN.md                        # Review human-readable summary

# Sync uses YuiQueryGitHubSync class (scripts/sync_github_todos.py:19)
# Metadata format in GitHub Issues:
# <!-- priority: P0|P1|P2|P3 -->
# <!-- status: todo|in_progress|blocked|done -->
# <!-- research_type: literature_review|citation_management|technical_analysis -->
```

### Document Generation Workflow
```bash
# Basic PDF generation
pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.pdf

# Professional academic PDF (requires Eisvogel template)
pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.pdf \
  --template=eisvogel \
  --pdf-engine=xelatex \
  --listings \
  --toc \
  --number-sections

# HTML for web sharing
pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.html \
  --standalone \
  --toc \
  --self-contained
```