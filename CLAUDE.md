# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research project focused on natural language to SQL in healthcare, specifically a whitepaper demonstrating the YuiQuery system. The repository contains academic documentation and research materials rather than executable code.

## Repository Structure

- **Primary Research Document**:
  - `paper.md` - Comprehensive academic research paper on YuiQuery healthcare analytics (merged from multiple sources)
  - Contains: literature review, empirical validation, case studies, 111 academic and industry citations

- **Project Management Documents**:
  - `README.md` - Project overview and repository guide  
  - `CLAUDE.md` - AI assistant instructions and project context
  - `TODO_FOR_AI.json` - Structured task tracking for AI assistants
  - `TODO_FOR_HUMAN.md` - Human-readable task list and quality assurance checklist
  - `DECISION_LOG.json` - Project decision history and rationale documentation

- **Supporting Materials**: 
  - `images/` - Visual documentation and diagrams related to YuiQuery features
  - `scripts/` - Utilities and data processing scripts
  - `LICENSE` - MIT License

## Project Context

This repository documents research on YuiQuery, a conversational AI platform for healthcare analytics that addresses three key challenges:
1. Low healthcare analytics maturity 
2. Healthcare workforce turnover and institutional memory loss
3. Technical barriers in natural language to SQL generation

The literature review synthesizes findings from systematic reviews, peer-reviewed journals, and industry sources to provide evidence for implementing conversational AI platforms in healthcare settings.

## Development Notes

This is a documentation-only repository without traditional software development workflows. There are no:
- Build systems or package managers
- Test frameworks
- Linting or type checking tools
- Source code directories

When working with this repository, focus on:
- Maintaining academic citation formatting
- Preserving document structure and organization
- Ensuring consistency in research documentation standards

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
- **Python Version Control**: Use UV to ensure Python 3.8+ compatibility across team members
- **Dependency Isolation**: Zero runtime dependencies, optional dev dependencies for code quality
- **Automatic Virtual Environments**: UV creates and manages .venv automatically
- **Development Tools**: Black, Flake8, MyPy, Pre-commit hooks for code quality
- **Command Pattern**: Always use `uv run python <script>` instead of bare `python3`

**Key UV Commands:**
```bash
uv sync                          # Install/sync all dependencies
uv run python script.py          # Run script in UV environment
uv run black .                   # Format code
uv run mypy scripts/             # Type checking
uv add --dev <package>           # Add dev dependency
```

### GitHub Integration Workflow
- **Bidirectional Sync**: `./scripts/sync_todos.sh` creates GitHub Issues from TODO tasks and syncs back
- **Metadata-Driven Issues**: GitHub Issues include structured metadata comments for priority and status
- **Automatic Backup**: System creates timestamped backups before any sync operations
- **Error Recovery**: Automatic restoration of backups if sync operations fail

## Advanced Issues & Solutions Discovered

### Python Version Compatibility Challenges
**Issue**: Python 3.6 compatibility error with `subprocess.run(text=True)` parameter
**Root Cause**: User environment had anaconda Python 3.6, but scripts required Python 3.7+ features
**Solution**: 
- Implemented UV environment with Python 3.8+ requirement in pyproject.toml
- Updated scripts to use UV environment automatically
- Added environment validation to sync scripts
- Documented UV setup process in all guides

**Prevention**: Always specify minimum Python version requirements in pyproject.toml

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

## Updated Project-Specific Requirements

### Development Environment Requirements
- **UV Package Manager**: Required for Python environment management (replaces pip/venv/pyenv)
  - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Manages Python versions automatically
  - Creates .venv on first `uv sync`
- **Python 3.8+**: Minimum version (UV handles installation if needed)
- **GitHub CLI**: Required for automated issue creation and bidirectional sync
- **Git Repository**: Must be connected to GitHub remote for sync functionality

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
                             # Phase 0: Load existing TODO_FOR_AI.json
                             # Phase 1: Create GitHub Issues from TODO tasks
                             # Phase 2: Sync GitHub Issues → TODO files
                             # Phase 3: Validate consistency

# Manual sync components
python scripts/sync_github_todos.py  # Run sync directly
gh issue list                        # Verify GitHub Issues exist
cat TODO_FOR_HUMAN.md               # Review human-readable summary
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