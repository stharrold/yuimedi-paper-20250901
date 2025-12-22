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

**Primary deliverable:** `paper.md` - Academic research paper with 92 verified citations (81 academic [A1-A81], 11 industry [I1-I11]) addressing:
1. Low healthcare analytics maturity
2. Healthcare workforce turnover and institutional memory loss
3. Technical barriers in natural language to SQL generation

**Citation verification:** All citations verified via DOI or authoritative sources. See `specs/fix-paper-references/reference_verification.md` for methodology.

**Paper classification:** Narrative review with original three-pillar analytical framework (NOT a systematic review with meta-analysis). This affects publication options - see `docs/journal-submission-guide.md`.

**Quality assessment:** Grey literature sources assessed using AACODS checklist (Tyndall, 2010). See `ppr_review/20251215_AACODS-Grey-Literature.md` for assessment table.

**Paper 1 structure (npj-aligned):** Introduction → Methodology → Framework Development → Literature Review → Discussion → Conclusion. Executive Summary removed (redundant with YAML abstract); Sections 5-6 (Proposed Solution, Evaluation) previously removed to transform paper from solution-advocacy to pure analytical framework.

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

# Testing (758 tests total: 415 lit_review + 316 skills + 27 other)
uv run pytest                              # Run all tests
uv run pytest tests/lit_review/ -v         # Literature review tests (415 tests)
uv run pytest tests/skills/ -v             # Workflow skills tests (316 tests)
uv run pytest --cov=lit_review             # With coverage
uv run pytest -k "test_paper" -v           # Run single test by name
uv run pytest -m "not integration"         # Skip integration tests (pre-push default)

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

## Commit Convention

Use conventional commits format:
- `fix(paper):` - Reference or content fixes
- `feat(ci):` - New CI/CD features
- `docs(CLAUDE.md):` - Documentation updates
- `build:` - Build/artifact changes

Include `Closes #<issue>` in commit body to auto-close GitHub issues.

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

### Pre-commit Hooks
Hooks run automatically on every commit:
- Trim trailing whitespace, fix end of files
- Validate YAML/JSON structure
- Check for large files, merge conflicts, private keys
- Run ruff format/lint on Python files
- Sync AI configs: `.claude/` → `.agents/`, `CLAUDE.md` → `AGENTS.md`

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

### Writing Style
- **NEVER use em-dashes (—)**. Replace with:
  - Commas for parenthetical insertions: "34% [A10], the highest rate, creates..."
  - Colons for definitions: "barrier: the gap between..."
  - Semicolons for related clauses: "descriptive; it provides..."
  - Parentheses for asides: "(backed by Amazon)"
- **Excluded from this rule:** `standards/` directory (external journal content)

### Citations
- Academic: `[A1]`, `[A2]`, etc. (81 sources)
- Industry: `[I1]`, `[I2]`, etc. (11 sources)
- Key dated citation: [A10] (2004 turnover data) - always qualify with temporal context

### File Naming
- Historical files: `YYYYMMDDTHHMMSSZ_` prefix (ISO 8601 UTC)
- Project management: UPPERCASE names
- Deprecated files: Move to local `ARCHIVED/` subdirectory

### Generated Files Strategy
**Committed to git (intentional):**
- `paper.pdf`, `paper.html`, `paper.docx`, `paper.tex` - Release artifacts for journal submission
- `figures/*` - All figure assets (source `.mmd`/`.dot`, generated `.jpg`/`.png`/`.svg`/`.pdf`)
- Versioned for reproducibility and release tagging

**Figure generation:** Generate from Mermaid or DOT source:
```bash
# Mermaid (.mmd) → PNG (in container for consistent fonts)
podman-compose run --rm dev npx --yes @mermaid-js/mermaid-cli@latest \
  -i figures/<name>.mmd -o figures/<name>.mmd.png -p /app/puppeteer-config.json

# Mermaid (.mmd) → SVG
podman-compose run --rm dev npx --yes @mermaid-js/mermaid-cli@latest \
  -i figures/<name>.mmd -o figures/<name>.mmd.svg -p /app/puppeteer-config.json

# DOT (.dot) → SVG/PNG (requires graphviz)
podman-compose run --rm dev dot -Tsvg figures/<name>.mmd.dot -o figures/<name>.mmd.dot.svg
podman-compose run --rm dev dot -Tpng figures/<name>.mmd.dot -o figures/<name>.mmd.dot.png
```

**Figure naming convention:** Suffix chain documents derivation:
- `<name>.mmd` - Mermaid source
- `<name>.mmd.png` - PNG derived from .mmd
- `<name>.mmd.dot` - DOT format (alternate)
- `<name>.mmd.dot.svg` - SVG derived from .dot

**Excluded via .gitignore:**
- `docs/references/*.pdf` - Downloaded reference PDFs (copyright, size)
- `.claude-state/*.duckdb` - Local database files

### Archiving
Every directory uses local `ARCHIVED/` subdirectory for deprecated files.

### Three-Pillar Framework
All research connects to: (1) analytics maturity, (2) workforce turnover, (3) technical barriers. The framework reveals how these challenges interconnect and compound each other: low maturity accelerates turnover, turnover degrades maturity, and technical barriers prevent recovery from either.

**Framework documentation:** See `paper.md` "Framework Development and Validation" section for development process, theoretical grounding (Table 3: HIMSS AMAM/DIKW alignment), and validation approach.

**Assessment rubric:** Table 4 in paper.md provides a 10-indicator rubric with Lower/Moderate/Higher Risk thresholds for organizational self-assessment. Each indicator is evidence-anchored to citations.

**Planning documents:** `planning/<feature-slug>/` in repository (committed to version control)

**Submission materials:** `ppr_review/` contains expert-review-checklist.md, osf-registration-draft.md, arxiv-submission-checklist.md, zenodo-submission-checklist.md

## Healthcare Domain Context

**Required knowledge:** ICD-10, CPT, SNOMED, RxNorm vocabularies; HIMSS maturity models; HL7/FHIR standards; HIPAA compliance.

**HIMSS maturity models (important distinction):**
- **EMRAM** (Electronic Medical Record Adoption Model): EHR adoption stages 0-7. Extensive outcome literature exists.
- **AMAM** (Analytics Maturity Assessment Model): Analytics capability stages. Released October 2024; no peer-reviewed outcome studies yet.
- Most literature uses EMRAM. When searching for AMAM evidence, note that AMAM-specific studies are a confirmed gap.

**Academic standards:** PRISMA guidelines for systematic reviews (not applicable to this narrative review - see `docs/prisma-assessment.md`); statistical reporting with p-values/CIs; evidence hierarchy prioritizing RCTs.

## Publication Strategy

**Three-paper series** targeting JMIR Medical Informatics:

| Paper | Focus | Due Date |
|-------|-------|----------|
| 1 | Three-Pillar Analytical Framework | Dec 31, 2025 |
| 2 | Reference Implementation (GCP/Synthea) | Jan 31, 2026 |
| 3 | FHIR/OMOP Schema Mapping | Mar 15, 2026 |

**Why JMIR (not npj Digital Medicine):** Open-source GCP/Synthea approach eliminates commercial COI concerns.

**Key documents:**
- Revision strategy: `ppr_review/20251215_Revision-Strategy-Milestones.md`
- Budget breakdown: `project-management.md` (Publication & Distribution Costs section)
- Status updates: `status-updates.md` (reverse-chronological log)
- Research questions: `docs/references/Research_Questions.md` (linked to GitHub issues via `research` label)
- Submission guide: `docs/journal-submission-guide.md`

**Research question tracking:** All literature review questions are tracked in `docs/references/Research_Questions.md`:
- **Answered Questions tables:** Question, Scope, Issue, Research File, Merged (citation numbers added to paper.md, e.g., `[A31]-[A34]`)
- **Unanswered Questions tables:** Question, Scope, Issue, Status, Notes
- **Status values:** Answered, Partial, Unanswered, → Gap (searched but not found)
- **Merged column:** Shows citation numbers (e.g., `[A66]`, `[A31]-[A34]`) when findings incorporated into paper.md; `-` means not yet merged
- Use `gh issue list --label "research"` to see all research-related issues
- Use `/scholar:research-question` skill for Google Scholar Labs searches

**Preprint strategy:**
- arXiv (primary): cs.CL, cross-list cs.DB, cs.HC, cs.CY
- medRxiv: NOT eligible (narrative reviews excluded)

## Licensing

**Dual-licensed repository:**
- **Code** (Python, scripts, tools): Apache 2.0
- **Paper** (paper.md, docs/): CC BY 4.0

All Python source files include SPDX headers:
```python
# SPDX-FileCopyrightText: 2025 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
```
