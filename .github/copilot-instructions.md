---
type: gemini-context
directory: .
purpose: Research paper on YuiQuery healthcare analytics - documentation-only repository
parent: null
sibling_readme: README.md
children:
  - .gemini/GEMINI.md
  - docs/GEMINI.md
  - tests/GEMINI.md
---

# GEMINI.md

This file provides guidance to Gemini Code (gemini.ai/code) when working with code in this repository.

## Project Overview

**Documentation-only repository** for a research paper on YuiQuery, a conversational AI platform for healthcare analytics. No source code to compile/run - all "development" is documentation writing, validation, and workflow automation.

**Primary deliverable:** `paper.md` - Academic research paper with 41 verified citations (30 academic, 11 industry) addressing:
1. Low healthcare analytics maturity
2. Healthcare workforce turnover and institutional memory loss
3. Technical barriers in natural language to SQL generation

**Citation verification:** All citations verified via DOI or authoritative sources. See `specs/fix-paper-references/reference_verification.md` for methodology.

**Paper classification:** Narrative review with original three-pillar analytical framework (NOT a systematic review with meta-analysis). This affects publication options - see `docs/journal-submission-guide.md`.

**Quality assessment:** Grey literature sources assessed using AACODS checklist (Tyndall, 2010). See `ppr_review/20251215_AACODS-Grey-Literature.md` for assessment table.

**Paper 1 structure (post-revision):** Executive Summary → Introduction → Methodology → Framework Development → Literature Review → Discussion → Conclusion. Sections 5-6 (Proposed Solution, Evaluation) were intentionally removed to transform paper from solution-advocacy to pure analytical framework.

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

## Pre-commit Hooks

```bash
# Install hooks (one-time)
uv run pre-commit install

# Run manually on all files
uv run pre-commit run --all-files
```

Hooks run automatically on commit:
- trailing whitespace, YAML/JSON validation
- ruff linting/formatting (v0.14.8)
- GEMINI.md frontmatter check
- skill structure validation
- **SPDX license headers** - Validates Apache 2.0 headers on all Python files

## Test Organization

```
tests/
├── unit/           # Single component tests
├── contract/       # Interface compliance tests
├── integration/    # End-to-end scenarios
└── skills/         # Skill-specific tests (git-workflow-manager, workflow-utilities)
```

Run specific test categories:
```bash
uv run pytest tests/skills/ -v          # Skill tests only
uv run pytest tests/contract/ -v        # Contract tests only
uv run pytest -m "not integration and not benchmark"  # Exclude slow tests (default in quality gates)
```

## v6 Workflow (feature-dev)

Streamlined 4-phase workflow using Gemini's feature-dev plugin:

```
/worktree "feature description"
    | creates worktree, user runs /feature-dev in worktree
    v
/integrate "feature/YYYYMMDDTHHMMSSZ_slug"
    | PR feature->contrib->develop
    v
/release
    | create release, PR to main, tag
    v
/backmerge
    | PR release->develop, rebase contrib, cleanup
```

| Step | Command | Purpose |
|------|---------|---------|
| 1 | `/worktree "desc"` | Create worktree, prompt for /feature-dev |
| 2 | `/integrate ["branch"]` | PR feature->contrib->develop |
| 3 | `/release` | Create release (develop->release->main) |
| 4 | `/backmerge` | Sync release (PR to develop, rebase contrib) |

**Key differences from old v1-v7 workflow:**
- No BMAD planning or SpecKit specifications (feature-dev handles planning)
- No quality gates (feature-dev's code review phase ensures quality)
- Simplified 4-step flow instead of 7 steps

## Core Architecture

### Branch Structure

```
main (production) ← develop (integration) ← contrib/stharrold (active) ← feature/*
```

**PR Flow**: feature → contrib → develop → main

**Branch Editability:**
| Branch | Editable | Direct Commits |
|--------|----------|----------------|
| `feature/*` | Yes | Yes |
| `contrib/*` | Yes | Yes |
| `develop` | No | PRs only |
| `main` | No | PRs only |
| `release/*` | Ephemeral | `/release` creates, `/backmerge` deletes |

### Skills System (6 skills in `.gemini/skills/`)

| Skill | Purpose |
|-------|---------|
| workflow-orchestrator | Main coordinator, templates |
| git-workflow-manager | Worktrees, PRs, semantic versioning |
| tech-stack-adapter | Python/uv/Podman detection |
| workflow-utilities | Archive, directory structure |
| agentdb-state-manager | Workflow state tracking (AgentDB) |
| initialize-repository | Bootstrap new repos |

**Archived skills** (see `ARCHIVED/`):
- bmad-planner - Replaced by feature-dev plugin
- speckit-author - Replaced by feature-dev plugin
- quality-enforcer - Replaced by feature-dev code review

### Document Lifecycle

```
docs/research/ → docs/guides/ → docs/archived/
(research)       (production)   (compressed)
```

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
3. **Infrastructure:** Crossref, PubMed, ArXiv, SemanticScholar adapters; GeminiAnalyzer; JSONRepository
4. **Interfaces (outermost):** CLI commands using Click framework

**Key Features:**
- Multi-database search with parallel execution (ThreadPoolExecutor)
- TF-IDF + hierarchical clustering for theme analysis (<30s for 500 papers)
- Multiple export formats: BibTeX, DOCX, LaTeX, HTML, JSON, Markdown, CSV
- Optional AI-powered synthesis with fallback to keyword-based approach

### Validation System
`./validate_documentation.sh` runs 7 tests: file size (30KB limit), cross-references, duplication, command syntax, YAML structure, reference validation (citations in paper.md), and LaTeX-in-URL validation.

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

### Citations
- Academic: `[A1]`, `[A2]`, etc. (30 sources)
- Industry: `[I1]`, `[I2]`, etc. (11 sources)
- Key dated citation: [A10] (2004 turnover data) - always qualify with temporal context

### File Naming
- Historical files: `YYYYMMDDTHHMMSSZ_` prefix (ISO 8601 UTC)
- Project management: UPPERCASE names (`DECISION_LOG.json`, `TODO.md`)
- Deprecated files: Move to local `ARCHIVED/` subdirectory

### Generated Files Strategy
**Committed to git (intentional):**
- `paper.pdf`, `paper.html`, `paper.docx`, `paper.tex` - Release artifacts for journal submission
- `figures/*` - All figure assets (source `.mmd`/`.dot`, generated `.jpg`/`.png`/`.svg`/`.pdf`)
- Versioned for reproducibility and release tagging

**Figure generation:** Generate from Mermaid or DOT source:
```bash
# Mermaid (.mmd) → PNG/JPG
npx --yes @mermaid-js/mermaid-cli@latest -i figures/<name>.mmd -o figures/<name>.png
# macOS (optional JPG conversion):
sips -s format jpeg figures/<name>.png --out figures/<name>.jpg

# DOT (.dot) → SVG/PNG (requires graphviz)
podman-compose run --rm dev dot -Tsvg figures/<name>.dot -o figures/<name>.dot.svg
podman-compose run --rm dev dot -Tpng figures/<name>.dot -o figures/<name>.dot.png
```

**Excluded via .gitignore:**
- `docs/references/*.pdf` - Downloaded reference PDFs (copyright, size)
- `.gemini-state/*.duckdb` - Local database files

### Archiving
Every directory uses local `ARCHIVED/` subdirectory for deprecated files.

### Three-Pillar Framework
All research connects to: (1) analytics maturity, (2) workforce turnover, (3) technical barriers. The framework reveals how these challenges interconnect and compound each other: low maturity accelerates turnover, turnover degrades maturity, and technical barriers prevent recovery from either.

**Framework documentation:** See `paper.md` "Framework Development and Validation" section for development process, theoretical grounding (Table 3: HIMSS AMAM/DIKW alignment), and validation approach.

**Assessment rubric:** Table 4 in paper.md provides a 10-indicator rubric with Lower/Moderate/Higher Risk thresholds for organizational self-assessment. Each indicator is evidence-anchored to citations.

**Planning documents:** `planning/<feature-slug>/` in repository (committed to version control)

**Submission materials:** `ppr_review/` contains expert-review-checklist.md, osf-registration-draft.md, arxiv-submission-checklist.md, zenodo-submission-checklist.md

## Healthcare Domain Context

**Required knowledge:** ICD-10, CPT, SNOMED, RxNorm vocabularies; HIMSS AMAM stages; HL7/FHIR standards; HIPAA compliance.

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

**Research question tracking:** All literature review questions are tracked in `docs/references/Research_Questions.md` with scope (Paper1/Paper2/Paper3), linked GitHub issues, and status (Answered/Unanswered/Gap). Use `gh issue list --label "research"` to see all research-related issues. Use `/scholar:research-question` skill for Google Scholar Labs searches.

**Preprint strategy:**
- arXiv (primary): cs.CL, cross-list cs.DB, cs.HC, cs.CY
- medRxiv: NOT eligible (narrative reviews excluded)

## Licensing

**Dual-licensed repository:**
- **Code** (Python, scripts, tools): Apache 2.0
- **Paper** (paper.md, docs/): CC BY 4.0

All Python source files include SPDX headers:
```python
# SPDX-FileCopyrightText: 2025 Yuimedi Corp.
# SPDX-License-Identifier: Apache-2.0
```

## Git Workflow Commands

```bash
# Create feature worktree
uv run python .gemini/skills/git-workflow-manager/scripts/create_worktree.py \
  feature my-feature contrib/stharrold

# Semantic version calculation
uv run python .gemini/skills/git-workflow-manager/scripts/semantic_version.py develop v7x1.0

# Archive management
uv run python .gemini/skills/workflow-utilities/scripts/archive_manager.py list

# Release workflow (develop → release → main)
uv run python .gemini/skills/git-workflow-manager/scripts/release_workflow.py <step>
# Steps: create-release, run-gates, pr-main, tag-release, full, status

# Backmerge workflow (release → develop, rebase contrib)
# Pattern: release/vX.Y.Z ──PR──> develop (direct, no intermediate branch)
# Requires: release/* branch must exist when starting step 7
uv run python .gemini/skills/git-workflow-manager/scripts/backmerge_workflow.py <step>
# Steps: pr-develop, rebase-contrib, cleanup-release, full, status

# CRITICAL: Backmerge direction
# CORRECT: release/vX.Y.Z -> develop (direct PR from release branch)
# WRONG:   main -> develop (NEVER merge main to develop!)

# Cleanup feature worktree and branches
uv run python .gemini/skills/git-workflow-manager/scripts/cleanup_feature.py my-feature
```

## Workflow State Tracking (AgentDB)

Workflow state is tracked in AgentDB (DuckDB) instead of TODO*.md files:

```bash
# Query current workflow phase
uv run python .gemini/skills/agentdb-state-manager/scripts/query_workflow_state.py

# Record workflow transition (called by slash commands)
uv run python .gemini/skills/agentdb-state-manager/scripts/record_sync.py \
  --sync-type workflow_transition \
  --pattern v6_1_worktree \
  --source "contrib/stharrold" \
  --target "feature/YYYYMMDDTHHMMSSZ_slug"
```

## Prerequisites

```bash
podman --version          # 4.0+
podman-compose --version
git --version
python3 --version         # 3.11+ (container uses 3.11)

# VCS Provider CLI (one of):
gh --version              # GitHub CLI (for GitHub repos)
# OR
az --version              # Azure CLI (for Azure DevOps repos)
az extension add --name azure-devops  # Required extension
```

## Cross-Platform Compatibility

- Pre-commit hooks use `language: python` (no shebang scripts) - works on Git Bash for Windows
- All scripts invoked via `uv run python <script>` - no shell script dependencies
- ASCII-only characters in Python files ensures terminal compatibility across platforms

## VCS Provider Configuration

The workflow **auto-detects** GitHub or Azure DevOps from your git remote URL:
- `github.com` → GitHub adapter (uses `gh` CLI)
- `dev.azure.com`, `*.visualstudio.com` → Azure DevOps adapter (uses `az` CLI)

For explicit configuration (or when auto-detection fails), create `.vcs_config.yaml`:

```yaml
# GitHub (usually auto-detected)
vcs_provider: github

# OR Azure DevOps
vcs_provider: azure_devops
azure_devops:
  organization: "https://dev.azure.com/myorg"
  project: "MyProject"
  repository: "MyRepo"  # Optional, defaults to project name
```

**VCS abstraction layer:** `.gemini/skills/workflow-utilities/scripts/vcs/`
- `provider.py` - Auto-detection from git remote
- `github_adapter.py` - GitHub CLI operations
- `azure_adapter.py` - Azure DevOps CLI operations
- `config.py` - Configuration file loader

## Critical Guidelines

- **One way to run**: Workflow commands use `uv run <command>` directly
- **End on editable branch**: All workflows must end on `contrib/*` (never `develop` or `main`)
- **ALWAYS prefer editing existing files** over creating new ones
- **NEVER proactively create documentation files** unless explicitly requested
- **Follow v6 workflow sequence**: `/worktree` -> `feature-dev` -> `/integrate` -> `/release` -> `/backmerge`
- **SPDX headers required**: All Python files must have Apache 2.0 license headers
- **ASCII-only**: Use only ASCII characters in Python files (Issue #121)
- **Absolute paths**: Use dynamically populated absolute paths in scripts (Issue #122)
- **Use GitHub Issues**: Task tracking uses GitHub Issues/Azure DevOps work items (not TODO*.md files)

## ASCII-Only Characters (Issue #121)

All Python files must use only ASCII characters (0x00-0x7F). No Unicode symbols.

**Why**: Ensures compatibility across all platforms, terminals, and encoding configurations.

**Encoding**: Files are UTF-8 encoded (UTF-8 is ASCII-compatible for ASCII characters).

**Common replacements** (use `safe_output.py` functions):

| Unicode | ASCII | Function |
|---------|-------|----------|
| `[checkmark]` | `[OK]` | `format_check()` |
| `[cross]` | `[FAIL]` | `format_cross()` |
| `[warning]` | `[WARN]` | `format_warning()` |
| `[arrow]` | `->` | `format_arrow()` |

**Validation**: `uv run python .gemini/skills/workflow-utilities/scripts/check_ascii_only.py`

**Pre-commit**: Enforced automatically via `ascii-only` hook.

## Absolute Paths (Issue #122)

Scripts must use dynamically populated absolute paths, not relative paths.

**Why**: Relative paths break when scripts are called from different working directories.

**Pattern**:
```python
import subprocess
from pathlib import Path

def get_repo_root() -> Path:
    """Get the repository root directory as an absolute path."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    )
    return Path(result.stdout.strip()).resolve()

# Use absolute paths
repo_root = get_repo_root()
archived_dir = repo_root / "ARCHIVED"
file_path = (repo_root / relative_path).resolve()
```

**Key rules**:
- Always resolve paths with `.resolve()` for absolute canonical form
- Derive paths from `git rev-parse --show-toplevel` for repo-relative paths
- Convert relative input paths to absolute before processing
- Store relative paths in archives for portability (use `relative_to(repo_root)`)

## SPDX License Headers

All Python files require SPDX headers for Apache 2.0 compliance:

```python
#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
```

**Validation**: `uv run python .gemini/skills/workflow-utilities/scripts/check_spdx_headers.py`

## Worktree State Isolation

Multiple Gemini Code instances can work on different features concurrently using git worktrees. Each worktree has isolated state in `.gemini-state/`:

```
repo/                         # Main repository
├── .gemini/skills/          # Shared (read-only)
├── .gemini-state/           # Per-worktree state
│   ├── agentdb.duckdb       # Isolated database
│   ├── workflow.json        # Workflow progress
│   └── .worktree-id         # Stable identifier
└── ...

repo_feature_abc/            # Feature worktree
├── .gemini-state/           # Separate state
│   └── ...                  # Independent from main
└── ...
```

**Key utilities**:
- `from worktree_context import get_state_dir` - Get worktree-specific state directory
- `from worktree_context import get_worktree_id` - Get stable worktree identifier
- State automatically isolated when using worktrees

## Common Issues

| Issue | Solution |
|-------|----------|
| Container not building | `podman info` to verify Podman running (CI/CD only) |
| pytest not found | Use `uv run pytest` |
| Import errors | Use `uv run python` |
| Worktree conflicts | `git worktree remove` + `git worktree prune` |
| Ended on wrong branch | `git checkout contrib/stharrold` |
| Orphaned state dirs | Run `cleanup_orphaned_state()` from worktree_context |
| Branch divergence | See [Preventing Branch Divergence](#preventing-branch-divergence) section |
| DuckDB not found | Run `uv sync` to install duckdb Python package (CLI not required) |

## Quick Debugging

```bash
# Where am I in the workflow?
uv run python .gemini/skills/agentdb-state-manager/scripts/query_workflow_state.py

# Am I in the right context for this step?
uv run python .gemini/skills/workflow-utilities/scripts/verify_workflow_context.py --step <N>

# What branches exist?
git branch -a | grep -E "(feature|release|contrib)"

# What worktrees exist?
git worktree list

# What's the current branch?
git branch --show-current

# Is this a worktree or main repo?
git rev-parse --git-dir  # .git = main repo, .git/worktrees/* = worktree
```

## Preventing Branch Divergence

**Problem**: When multiple sessions run `rebase-contrib` or `daily_rebase.py`, local and remote branches can diverge with same content but different SHAs.

**Root cause**: Rebasing creates new commit SHAs. If session A rebases and pushes while session B has old history, session B's subsequent rebase creates parallel history.

**Built-in safeguards** (v5.16.0+):
- `backmerge_workflow.py` and `daily_rebase.py` now check for divergence before rebasing
- If divergence detected, scripts halt with resolution options
- If remote is ahead, scripts auto-pull before rebasing

**Manual detection**:
```bash
# Check for divergence
git fetch origin
git rev-list --left-right --count contrib/stharrold...origin/contrib/stharrold
# Output: "X Y" where X=local-only commits, Y=remote-only commits
# If both > 0: DIVERGED
```

**Resolution options**:
```bash
# Option 1: Accept remote (recommended if remote has newer work)
git reset --hard origin/contrib/stharrold

# Option 2: Force push local (if local has work you want to keep)
git push --force-with-lease origin contrib/stharrold

# Option 3: Merge (creates merge commit, less clean history)
git pull --no-rebase
```

**Best practices**:
1. Always push after running backmerge or daily rebase
2. Pull before starting new work in a session
3. Avoid running backmerge from multiple machines simultaneously
4. Use single source of truth for rebase operations

## Branch Cleanup

```bash
# List stale feature branches (numbered prefixes from old specs)
git branch --list '[0-9][0-9][0-9]-*'

# Delete merged local branches
git branch -d <branch-name>

# Delete remote tracking branches
git push origin --delete <branch-name>

# Prune stale remote-tracking references
git fetch --prune
```

## Apply This Workflow to Another Repository (Phase 0)

This repository can bootstrap new projects with the full workflow system:

```bash
# From any location with stharrold-templates available:
python stharrold-templates/.gemini/skills/initialize-repository/scripts/initialize_repository.py \
  stharrold-templates /path/to/target-repo
```

**Interactive 4-phase Q&A:**
1. **Configuration** - Project name, description, VCS provider (GitHub/Azure DevOps)
2. **Component selection** - Which skills to include
3. **File generation** - Creates pyproject.toml, README.md, GEMINI.md, etc.
4. **Git initialization** - Sets up main/develop/contrib branch structure

**Requirements for target repo:**
- Python 3.11+ with `uv`
- `pytest` for testing
- `ruff` + `mypy` for linting
- Podman for containerization
- GitHub (`gh`) OR Azure DevOps (`az`) CLI

**See:** `.gemini/skills/initialize-repository/GEMINI.md` for full documentation.

## Reference Documentation

- `WORKFLOW.md` - Workflow overview (14KB) with phase index
- `docs/reference/workflow-*.md` - Phase-specific workflow docs (≤20KB each)
- `ARCHITECTURE.md` - System architecture analysis
- `CHANGELOG.md` - Version history
- `ARCHIVED/` - Archived specs, planning docs, and deprecated skills (zipped)

## GEMINI.md Hierarchy

Every directory has a GEMINI.md with YAML frontmatter for AI navigation:
- `parent` - Link to parent directory's GEMINI.md
- `children` - Links to child directories' GEMINI.md files
- `sibling_readme` - Link to same-level README.md

```bash
# Generate missing GEMINI.md files
uv run python .gemini/skills/workflow-utilities/scripts/generate_gemini_md.py

# Update children references in existing GEMINI.md files
uv run python .gemini/skills/workflow-utilities/scripts/update_gemini_md_refs.py
```
