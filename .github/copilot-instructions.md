---
type: claude-context
directory: .
purpose: Research paper on YuiQuery healthcare analytics - documentation-only repository
parent: null
sibling_readme: README.md
children:
  - .claude/CLAUDE.md
  - docs/CLAUDE.md
  - lit_review/CLAUDE.md
  - scripts/CLAUDE.md
  - tests/CLAUDE.md
  - tools/CLAUDE.md
related_skills:
  - workflow-orchestrator
  - quality-enforcer
  - git-workflow-manager
---

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Documentation-only repository** for a research paper on YuiQuery, a conversational AI platform for healthcare analytics. No source code to compile/run - all "development" is documentation writing, validation, and workflow automation.

**Primary deliverable:** `paper.md` - Academic research paper with 111 citations addressing:
1. Low healthcare analytics maturity
2. Healthcare workforce turnover and institutional memory loss
3. Technical barriers in natural language to SQL generation

## Essential Commands

```bash
# Setup (choose one)
uv sync                                    # Local (with dev dependencies)
uv sync --extra ai --extra export         # With AI and export features
podman-compose build                       # Container (recommended)

# Quality checks (run before commits)
./validate_documentation.sh                # Documentation validation (6 tests)
python scripts/validate_references.py --all  # Reference validation + URL checks
uv run ruff format . && uv run ruff check --fix .  # Format + lint
uv run mypy scripts/ lit_review/           # Type checking

# Full quality gates (before PRs)
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# Literature review workflow (academic-review CLI)
uv run academic-review --help              # CLI for systematic reviews
uv run academic-review init "Title" -q "Research question" -i "Inclusion"  # Initialize
uv run academic-review search "Title" -d crossref -k "keywords"  # Search databases
uv run academic-review assess "Title" "10.1234/doi" --score 8 --include  # Assess paper
uv run academic-review analyze "Title"     # Run thematic analysis (TF-IDF + clustering)
uv run academic-review synthesize "Title" --output synthesis.md  # Generate narrative
uv run academic-review export "Title" -f bibtex -f html -o output/  # Export multiple formats
uv run academic-review status "Title"      # Check review status
uv run academic-review list                # List all reviews

# Testing
uv run pytest                              # Run all tests
uv run pytest tests/lit_review/ -v         # Literature review tests only
uv run pytest --cov=lit_review --cov-fail-under=80  # With coverage threshold
uv run pytest -m "not integration and not benchmark"  # Skip slow tests
uv run pytest tests/lit_review/domain/ -v  # Test specific layer

# Performance benchmarks
uv run pytest -m benchmark                 # Run performance tests only

# Task management
gh issue list --label "P0"                 # Critical tasks
gh issue view <number>                     # Task details
```

## Workflow System (for feature development)

7-step workflow for implementing new features:

```bash
# Step 1: Create feature specification and planning documents
/workflow:1_specify  # Creates planning/ documents and GitHub issue

# Step 2: Design implementation in isolated worktree
/workflow:2_plan     # Run from feature worktree after creation

# Step 3: Generate task breakdown
/workflow:3_tasks    # Creates detailed implementation tasks

# Step 4: Execute implementation
/workflow:4_implement  # Automated task execution with quality gates

# Step 5: Integrate to develop branch
/workflow:5_integrate  # Create and merge PR to develop

# Step 6: Release to production
/workflow:6_release    # Create release branch, tag, deploy

# Step 7: Backmerge and cleanup
/workflow:7_backmerge  # Sync changes back to develop and contrib
```

**Note:** Workflow skills (`.claude/skills/`) are for major releases and complex git operations, not daily editing tasks.

## Branch Strategy

```
main (production) ← release/* ← develop ← contrib/stharrold ← feature/*
```

| Branch | Direct Commits |
|--------|----------------|
| `feature/*`, `contrib/*` | Yes |
| `develop`, `main` | PRs only |
| `release/*` | Ephemeral (create from develop, delete after merge) |

## Architecture

### Dependency Strategy
**Scripts (`scripts/`, `tools/`):** Python stdlib only - no external packages.
```python
# Allowed: sys, os, subprocess, json, pathlib, datetime, re, typing
# NOT allowed: requests, click, etc.
```

**Literature Review Package (`lit_review/`):** External dependencies allowed.
- Clean Architecture (domain/application/infrastructure/interfaces layers)
- **Core dependencies:** pydantic, httpx, click, scikit-learn, biopython, jinja2
- **Optional extras:** `ai` (anthropic), `export` (python-docx, bibtexparser), `workflow` (duckdb)
- **Test coverage:** 88.20% overall (domain 98.52%, application 95.88%, infrastructure 83.96%, CLI 80.70%)
- All dependencies managed via `uv sync`

**Clean Architecture Layers:**
1. **Domain (innermost):** Paper, Review, DOI entities; no external dependencies
2. **Application:** SearchPapers, AnalyzeThemes, GenerateSynthesis use cases; port interfaces
3. **Infrastructure:** Crossref, PubMed, ArXiv, SemanticScholar adapters; ClaudeAnalyzer; JSONRepository
4. **Interfaces (outermost):** CLI commands using Click framework

**Key Features:**
- Multi-database search with parallel execution (ThreadPoolExecutor)
- TF-IDF + hierarchical clustering for theme analysis (<30s for 500 papers)
- Atomic writes with automatic backups (.backups/ keeps last 5)
- Multiple export formats: BibTeX, DOCX, LaTeX, HTML, JSON, Markdown, CSV
- Optional AI-powered synthesis with fallback to keyword-based approach

### Validation System
`./validate_documentation.sh` runs 6 tests: file size (30KB limit), cross-references, duplication, command syntax, YAML structure, and reference validation (citations in paper.md).

### AI Config Sync
Pre-commit hooks sync `.claude/` → `.agents/` and `CLAUDE.md` → `AGENTS.md` for cross-tool compatibility.

### Workflow Skills
9 skills in `.claude/skills/` for major releases and complex git operations. **Don't use for daily edits.**

### Environment Variables
- `LIT_REVIEW_DATA_DIR` - Data storage location (default: `~/.lit_review`)
- `ANTHROPIC_API_KEY` - Claude API key for AI features (optional)
- `PUBMED_EMAIL` - Email for PubMed API (optional, enables 10 req/sec vs 3 req/sec)
- `NCBI_API_KEY` - NCBI API key for PubMed (optional, further rate limit increase)

## Key Patterns

### Citations
- Academic: `[A1]`, `[A2]`, etc.
- Industry: `[I1]`, `[I2]`, etc.

### File Naming
- Historical files: `YYYYMMDDTHHMMSSZ_` prefix
- Project management: UPPERCASE (`DECISION_LOG.json`)

### Archiving
Every directory uses local `ARCHIVED/` subdirectory for deprecated files.

### Three-Pillar Framework
All research connects to: (1) analytics maturity, (2) workforce turnover, (3) technical barriers.

### Data Storage

**Literature reviews:** `~/.lit_review/` (configurable via `LIT_REVIEW_DATA_DIR` environment variable)
- Reviews stored as JSON files with atomic writes
- Automatic backups in `.backups/` (keeps last 5 versions)
- File locking for concurrent access
- Soft deletes move to `.deleted/` directory

**Planning documents:** `planning/<feature-slug>/` in repository (committed to version control)

## Healthcare Domain Context

**Required knowledge:** ICD-10, CPT, SNOMED, RxNorm vocabularies; HIMSS AMAM stages; HL7/FHIR standards; HIPAA compliance.

**Academic standards:** PRISMA guidelines for systematic reviews; statistical reporting with p-values/CIs; evidence hierarchy prioritizing RCTs.
