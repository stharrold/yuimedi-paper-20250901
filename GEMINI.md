---
type: gemini-context
directory: .
purpose: Research paper on YuiQuery healthcare analytics - documentation-only repository
parent: null
sibling_readme: README.md
children:
- .benchmarks/GEMINI.md
- .gemini/GEMINI.md
- .github/GEMINI.md
- ARCHIVED/GEMINI.md
- compliance/GEMINI.md
- config/GEMINI.md
- docs/GEMINI.md
- figures/GEMINI.md
- images/GEMINI.md
- lit_review/GEMINI.md
- project-management/GEMINI.md
- scripts/GEMINI.md
- src/GEMINI.md
- standards/GEMINI.md
- submission/GEMINI.md
- tests/GEMINI.md
- tools/GEMINI.md
related_skills:
- workflow-orchestrator
- git-workflow-manager
- agentdb-state-manager
archived:
- "planning/ \u2192 ARCHIVED/20260101T171631Z_planning_*.zip"
- "specs/ \u2192 ARCHIVED/20260101T172405Z_specs_*.zip"
- "ppr_review/ \u2192 ARCHIVED/20260101T171859Z_ppr_review.zip"
---

# GEMINI.md

This file provides guidance to Gemini (Gemini) when working with code in this repository.

## Project Overview

**Documentation-only repository** for a research paper on YuiQuery, a conversational AI platform for healthcare analytics. No source code to compile/run - all "development" is documentation writing, validation, and workflow automation.

**Primary deliverable:** `paper.md` - Academic research paper with 108 verified citations (pandoc-citeproc format) addressing:
1. Low healthcare analytics maturity
2. Healthcare workforce turnover and institutional memory loss
3. Technical barriers in natural language to SQL generation

**Citation verification:** All citations verified via DOI or authoritative sources. Methodology archived in `ARCHIVED/20260101T171645Z_specs_fix-paper-references.zip`.

**Paper classification:** Narrative review with original three-pillar analytical framework (NOT a systematic review with meta-analysis). This affects publication options - see `docs/guides/journal-submission-guide.md`.

**Quality assessment:** Grey literature sources assessed using AACODS checklist (Tyndall, 2010). See `ARCHIVED/20260101T171859Z_ppr_review.zip` for assessment table.

**Paper 1 structure:** Introduction → Methodology → Framework Development → Literature Review → Discussion → Conclusion. Executive Summary removed (redundant with YAML abstract); Sections 5-6 (Proposed Solution, Evaluation) previously removed to transform paper from solution-advocacy to pure analytical framework.

**CRITICAL - Framework-first thesis:** The paper's primary contribution is the three-pillar analytical framework itself, NOT advocacy for conversational AI as a solution. When editing:
- Frame conversational AI and the validated query cycle as "illustrative applications" of the framework
- Avoid language like "compelling case for," "evidence-based solution," or "support the adoption of"
- Subsection headers should be framework-focused, not solution-focused
- The framework is descriptive (reveals interconnections) rather than prescriptive (recommends solutions)

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

# Literature review CLI (for systematic reviews, not used for this paper's narrative review)
uv run academic-review --help              # CLI for systematic reviews
uv run academic-review init <review-id>    # Initialize new review
uv run academic-review search <review-id>  # Execute search stage
uv run academic-review status <review-id>  # Check review status

# Testing
uv run pytest                              # Run all tests
uv run pytest tests/lit_review/ -v         # Literature review tests
uv run pytest tests/skills/ -v             # Workflow skills tests
uv run pytest --cov=lit_review             # With coverage
uv run pytest -k "test_paper" -v           # Run single test by name
uv run pytest -m "not integration"         # Skip integration tests (pre-push default)

# Skills coverage (targeted modules)
uv run pytest tests/skills/ \
  --cov=.gemini/skills/git-workflow-manager/scripts \
  --cov=.gemini/skills/workflow-utilities/scripts/vcs \
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

## Workflow System (v6)

Streamlined 4-phase workflow using Gemini's feature-dev plugin:

```bash
# Step 1: Create feature worktree
/workflow:v6_1_worktree "feature description"
# Creates branch: feature/{timestamp}_{slug}
# Creates worktree: ../{project}_feature_{timestamp}_{slug}/

# Step 2: Develop in worktree (run from worktree, not main repo)
cd <worktree-path>
/feature-dev:feature-dev "feature description"
# Handles: codebase understanding, planning, implementation, code review

# Step 3: Integrate to develop
/workflow:v6_2_integrate "feature/YYYYMMDDTHHMMSSZ_slug"
# PR feature->contrib, cleanup worktree, PR contrib->develop

# Step 4: Release to main
/workflow:v6_3_release           # Auto-calculate version
/workflow:v6_3_release v1.2.0    # Explicit version

# Step 5: Backmerge and cleanup
/workflow:v6_4_backmerge
# PR release->develop, rebase contrib, delete release branch
```

**Note:** Workflow skills are for major releases and complex git operations, not daily editing tasks. See `WORKFLOW.md` for details.

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
- `docs(GEMINI.md):` - Documentation updates
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

### Documentation Structure
```
docs/
├── guides/           # How-to documentation (journal submission, PDF generation, lit_review)
├── reports/          # Analysis reports (citation audit, PRISMA assessment, validation)
├── research/         # Literature review notes (38 Research_*.md files)
└── references/       # Source PDFs (git-crypt encrypted)
```

### Validation System
`./validate_documentation.sh` runs 7 tests: file size (30KB limit), cross-references, duplication, command syntax, YAML structure, reference validation (citations in paper.md), and LaTeX-in-URL validation.

### Pre-commit Hooks
Hooks run automatically on every commit:
- Trim trailing whitespace, fix end of files
- Validate YAML/JSON structure
- Check for large files, merge conflicts, private keys
- Run ruff format/lint on Python files

### Workflow Skills
6 skills in `.gemini/skills/` for major releases and complex git operations:
- `workflow-orchestrator` - Main coordinator
- `git-workflow-manager` - Worktrees, PRs, semantic versioning
- `tech-stack-adapter` - Python/uv detection
- `workflow-utilities` - Archive, directory structure
- `agentdb-state-manager` - Workflow state tracking (DuckDB)
- `initialize-repository` - Bootstrap new repos

**Archived skills** (replaced by feature-dev plugin): bmad-planner, speckit-author, quality-enforcer

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

### Citations (pandoc-citeproc)
Uses pandoc-citeproc for automatic bibliography generation:
- Citation format: `[@key]` (e.g., `[@wu2024]`, `[@himss2024]`)
- Multiple citations: `[@wu2024; @ren2024]`
- BibTeX file: `references.bib` (108 entries)
- CSL style: `citation-style-ama.csl` (AMA 11th edition for JMIR compliance)

**Key files:**
- `references.bib` - BibTeX bibliography
- `citation-style-ama.csl` - AMA citation style (JMIR requirement)
- `citation-style.csl` - Vancouver citation style (legacy, kept for reference)

**JMIR compliance validation:**
```bash
python scripts/validate_jmir_compliance.py      # Check abstract, sections, CSL
python scripts/extract_abbreviations.py         # Generate abbreviations list
```

**Citation key convention:** `{firstauthor}{year}{suffix}` (e.g., `wu2024`, `wu2024a`)

**BibTeX entry format:** Use consistent author formatting with "and" (not `\&`):
```bibtex
@article{wu2024,
  author = {Wu, F., Lao, Y., Feng, Y., and Li, L.},
  title = {{Title with double braces for case preservation}},
  year = {2024},
  journal = {Journal Name},
  volume = {11},
  pages = {e2097},
  doi = {10.1002/nop2.2097},
  url = {https://...},
  note = {Original citation: [A1]},
}
```

**Reference verification:** When adding/updating citations, verify DOI and URL against Google Scholar or publisher site. The `note` field tracks the original citation marker (A1-A81 academic, I1-I11 industry).

### File Naming
- Historical files: `YYYYMMDDTHHMMSSZ_` prefix (ISO 8601 UTC)
- Project management: UPPERCASE names
- Deprecated files: Move to local `ARCHIVED/` subdirectory

### Generated Files Strategy
**Committed to git (intentional):**
- `paper.pdf`, `paper.html`, `paper.docx`, `paper.tex` - Release artifacts for journal submission
- `references.bib` - BibTeX bibliography (108 entries)
- `citation-style-ama.csl` - AMA 11th edition (JMIR requirement, from Zotero CSL repository)
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
- `../library/docs/*.pdf` - Downloaded reference PDFs (copyright, size)
- `.gemini-state/*.duckdb` - Local database files

### Archiving
Every directory uses local `ARCHIVED/` subdirectory for deprecated files.

### Three-Pillar Framework
All research connects to: (1) analytics maturity, (2) workforce turnover, (3) technical barriers. The framework reveals how these challenges interconnect and compound each other: low maturity accelerates turnover, turnover degrades maturity, and technical barriers prevent recovery from either.

**Framework documentation:** See `paper.md` "Framework Development and Validation" section for development process, theoretical grounding (Table 3: HIMSS AMAM/DIKW alignment), and validation approach.

**Assessment rubric:** Table 4 in paper.md provides a 10-indicator rubric with Lower/Moderate/Higher Risk thresholds for organizational self-assessment. Each indicator is evidence-anchored to citations.

**Planning documents:** Historical planning archived in `ARCHIVED/20260101T171631Z_planning_*.zip`

**Submission materials:** Archived in `ARCHIVED/20260101T171859Z_ppr_review.zip` (expert-review-checklist.md, osf-registration-draft.md, arxiv-submission-checklist.md, zenodo-submission-checklist.md)

## Healthcare Domain Context

**Required knowledge:** ICD-10, CPT, SNOMED, RxNorm vocabularies; HIMSS maturity models; HL7/FHIR standards; HIPAA compliance.

**HIMSS maturity models (important distinction):**
- **EMRAM** (Electronic Medical Record Adoption Model): EHR adoption stages 0-7. Extensive outcome literature exists.
- **AMAM** (Analytics Maturity Assessment Model): Analytics capability stages. Released October 2024; no peer-reviewed outcome studies yet.
- Most literature uses EMRAM. When searching for AMAM evidence, note that AMAM-specific studies are a confirmed gap.

**Academic standards:** PRISMA guidelines for systematic reviews (not applicable to this narrative review - see `docs/reports/prisma-assessment.md`); statistical reporting with p-values/CIs; evidence hierarchy prioritizing RCTs.

## Publication Strategy

**Three-paper series** targeting JMIR Medical Informatics:

| Paper | Focus | Due Date |
|-------|-------|----------|
| 1 | Three-Pillar Analytical Framework | Dec 31, 2025 |
| 2 | Reference Implementation (GCP/Synthea) | Jan 31, 2026 |
| 3 | FHIR/OMOP Schema Mapping | Mar 15, 2026 |

**Why JMIR (not npj Digital Medicine):** Open-source GCP/Synthea approach eliminates commercial COI concerns.

**Key documents:**
- Revision strategy: Archived in `ARCHIVED/20260101T171859Z_ppr_review.zip`
- Budget breakdown: `project-management.md` (Publication & Distribution Costs section)
- Status updates: `status-updates.md` (reverse-chronological log)
- Research questions: `docs/research/Research_Questions.md` (linked to GitHub issues via `research` label)
- Submission guide: `docs/guides/journal-submission-guide.md`

**Research question tracking:** All literature review questions are tracked in `docs/research/Research_Questions.md`:
- **Answered Questions tables:** Question, Scope, Issue, Research File, Merged
- **Unanswered Questions tables:** Question, Scope, Issue, Status, Notes
- **Status values:** Answered, Partial, Unanswered, → Gap (searched but not found)
- **Merged column:** Shows citation range (e.g., `[@wu2024]-[@ren2024]`) when findings incorporated into paper.md; `-` means not yet merged
- Use `gh issue list --label "research"` to see all research-related issues
- **Scholar Labs Workflow:** See `docs/guides/scholar-labs-workflow.md` for the user-attended automation process.

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

## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory

**Child Directories:**
- **[ARCHIVED/GEMINI.md](ARCHIVED/GEMINI.md)** - Archived
- **[compliance/GEMINI.md](compliance/GEMINI.md)** - Compliance
- **[config/GEMINI.md](config/GEMINI.md)** - Config
- **[docs/GEMINI.md](docs/GEMINI.md)** - Docs
- **[figures/GEMINI.md](figures/GEMINI.md)** - Figures
- **[images/GEMINI.md](images/GEMINI.md)** - Images
- **[lit_review/GEMINI.md](lit_review/GEMINI.md)** - Lit Review
- **[project-management/GEMINI.md](project-management/GEMINI.md)** - Project Management
- **[scripts/GEMINI.md](scripts/GEMINI.md)** - Scripts
- **[src/GEMINI.md](src/GEMINI.md)** - Src
- **[standards/GEMINI.md](standards/GEMINI.md)** - Standards
- **[submission/GEMINI.md](submission/GEMINI.md)** - Submission
- **[tests/GEMINI.md](tests/GEMINI.md)** - Tests
- **[tools/GEMINI.md](tools/GEMINI.md)** - Tools
