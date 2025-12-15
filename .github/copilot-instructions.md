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

**Primary deliverable:** `paper.md` - Academic research paper with 41 verified citations (30 academic, 11 industry) addressing:
1. Low healthcare analytics maturity
2. Healthcare workforce turnover and institutional memory loss
3. Technical barriers in natural language to SQL generation

**Citation verification:** All citations verified via DOI or authoritative sources. See `specs/fix-paper-references/reference_verification.md` for methodology.

**Paper classification:** Narrative review with original analytical framework (NOT a systematic review with meta-analysis). This affects publication options - see `docs/journal-submission-guide.md`.

## Essential Commands

```bash
# Setup (choose one)
uv sync                                    # Local
podman-compose build                       # Container (recommended)

# Quality checks (run before commits)
./validate_documentation.sh                # Documentation validation (7 tests)
python scripts/validate_references.py --all  # Reference validation + URL checks
uv run ruff format . && uv run ruff check --fix .  # Format + lint
uv run mypy scripts/ lit_review/           # Type checking

# Full quality gates (before PRs)
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# Literature review workflow
uv run academic-review --help              # CLI for systematic reviews
uv run academic-review init <review-id>    # Initialize new review
uv run academic-review search <review-id>  # Execute search stage
uv run academic-review status <review-id>  # Check review status

# Testing
uv run pytest                              # Run all tests
uv run pytest tests/lit_review/ -v         # Literature review tests only
uv run pytest tests/skills/ -v             # Workflow skills tests (289 tests)
uv run pytest --cov=lit_review             # With coverage
uv run pytest -k "test_paper" -v           # Run single test by name
uv run pytest -m "not integration"         # Skip integration tests (default in CI)

# Skills coverage (targeted modules)
uv run pytest tests/skills/ \
  --cov=.claude/skills/git-workflow-manager/scripts \
  --cov=.claude/skills/quality-enforcer/scripts \
  --cov=.claude/skills/workflow-utilities/scripts/vcs \
  --cov-report=term

# Task management
gh issue list --label "P0"                 # Critical tasks
gh issue view <number>                     # Task details

# PDF generation
./scripts/build_paper.sh                   # Generate PDF (local)
./scripts/build_paper.sh --format html     # Generate HTML
./scripts/build_paper.sh --format all      # Generate PDF, HTML, DOCX
podman-compose run --rm dev ./scripts/build_paper.sh  # Generate in container
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
- Dependencies: pydantic, httpx, click, scikit-learn, biopython, jinja2 (see pyproject.toml)
- All dependencies managed via `uv sync`

**Clean Architecture Layers:**
1. **Domain (innermost):** Paper, Review, DOI entities; no external dependencies
2. **Application:** SearchPapers, AnalyzeThemes, GenerateSynthesis use cases; port interfaces
3. **Infrastructure:** Crossref, PubMed, ArXiv, SemanticScholar adapters; ClaudeAnalyzer; JSONRepository
4. **Interfaces (outermost):** CLI commands using Click framework

**Key Features:**
- Multi-database search with parallel execution (ThreadPoolExecutor)
- TF-IDF + hierarchical clustering for theme analysis (<30s for 500 papers)
- Multiple export formats: BibTeX, DOCX, LaTeX, HTML, JSON, Markdown, CSV
- Optional AI-powered synthesis with fallback to keyword-based approach

### Validation System
`./validate_documentation.sh` runs 7 tests: file size (30KB limit), cross-references, duplication, command syntax, YAML structure, reference validation (citations in paper.md), and LaTeX-in-URL validation.

### AI Config Sync
Pre-commit hooks sync `.claude/` → `.agents/` and `CLAUDE.md` → `AGENTS.md` for cross-tool compatibility.

### Workflow Skills
9 skills in `.claude/skills/` for major releases and complex git operations. **Don't use for daily edits.**

### CI/CD

**Container-based testing:** GitHub Actions runs all tests inside Docker containers built from `Containerfile` to ensure environment parity with local Podman development.

```bash
# Local container development
podman-compose build                    # Build container
podman-compose run --rm dev uv run pytest  # Run tests in container
podman-compose run --rm dev uv run python <script>  # Run any script
```

**Container architecture:**
- Python 3.12 + uv with `--all-extras` (includes duckdb for AgentDB)
- GitHub CLI (`gh`) for workflow automation (PR creation, issue management)
- PDF generation: pandoc + texlive-xetex + Eisvogel template
- Named volume `venv_cache` isolates container `.venv` from host (avoids macOS/Linux binary mismatch)
- Always use `uv run` prefix in container for proper venv activation

**Why containers?** Eliminates "works locally, fails in CI" issues by using identical environment (Python 3.12, uv, dependencies) in both contexts.

**Auto-build paper artifacts:** When `paper.md`, `metadata.yaml`, or `figures/**` changes are pushed to `main`, `develop`, or `contrib/*` branches, GitHub Actions automatically rebuilds all paper formats (PDF, HTML, DOCX, TEX) and commits them back with `[skip ci]` to prevent loops.

### Environment Variables
- `LIT_REVIEW_DATA_DIR` - Data storage location (default: `~/.lit_review`)
- `ANTHROPIC_API_KEY` - Claude API key for AI features (optional)
- `NCBI_EMAIL` - Email for PubMed API (required by NCBI policy)
- `NCBI_API_KEY` - NCBI API key for PubMed (optional, enables 10 req/sec vs 3 req/sec)

## Key Patterns

### Citations
- Academic: `[A1]`, `[A2]`, etc.
- Industry: `[I1]`, `[I2]`, etc.

### File Naming
- Historical files: `YYYYMMDDTHHMMSSZ_` prefix
- Project management: UPPERCASE (`DECISION_LOG.json`)

### Generated Files Strategy
**Committed to git (intentional):**
- `paper.pdf`, `paper.html`, `paper.docx`, `paper.tex` - Release artifacts for journal submission
- Versioned for reproducibility and release tagging

**Excluded via .gitignore:**
- `docs/references/*.pdf` - Downloaded reference PDFs (copyright, size)
- `.claude-state/*.duckdb` - Local database files

### Archiving
Every directory uses local `ARCHIVED/` subdirectory for deprecated files.

### Three-Pillar Framework
All research connects to: (1) analytics maturity, (2) workforce turnover, (3) technical barriers.

**Planning documents:** `planning/<feature-slug>/` in repository (committed to version control)

## Healthcare Domain Context

**Required knowledge:** ICD-10, CPT, SNOMED, RxNorm vocabularies; HIMSS AMAM stages; HL7/FHIR standards; HIPAA compliance.

**Academic standards:** PRISMA guidelines for systematic reviews (not applicable to this narrative review - see `docs/prisma-assessment.md`); statistical reporting with p-values/CIs; evidence hierarchy prioritizing RCTs.

## Publication Strategy

**Target journal:** npj Digital Medicine (Nature Portfolio) - IF 15.1, 7-day first decision
- Journal policies: `npj_digital-medicine_about*.md`
- Submission guide: `docs/journal-submission-guide.md`

**Preprint strategy:**
- arXiv (primary): cs.CL, cross-list cs.DB, cs.HC, cs.CY
- medRxiv: NOT eligible (narrative reviews excluded)
