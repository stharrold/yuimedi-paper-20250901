---
type: claude-context
directory: .
purpose: Root project context for yuimedi-paper-20250901 academic research repository.
parent: null
sibling_readme: README.md
children:
  - .claude/CLAUDE.md
  - .github/CLAUDE.md
  - ARCHIVED/CLAUDE.md
  - compliance/CLAUDE.md
  - config/CLAUDE.md
  - docs/CLAUDE.md
  - figures/CLAUDE.md
  - lit_review/CLAUDE.md
  - project-management/CLAUDE.md
  - scripts/CLAUDE.md
  - src/CLAUDE.md
  - tests/CLAUDE.md
  - tools/CLAUDE.md
---

# CLAUDE.md

## Project Overview

Documentation-focused academic research repository. Primary deliverable: `paper.md`, a Theoretical Framework / Viewpoint paper targeting JMIR Medical Informatics.

**Topic:** "Mitigating Institutional Amnesia" in healthcare analytics via Human-in-the-Loop Semantic Governance (HiL-SG).

**Three-paper series:** Paper 1 (Viewpoint, resubmitting to JMIR ms#91493) → Paper 2 (empirical validation, Synthea/GCP) → Paper 3 (FHIR/OMOP interoperability). GitHub issues tagged `paper-1`, `paper-2`, `paper-3`.

**Paper 1 history:** Originally submitted as Original Paper (~12,730 words), rejected for length. Archived at `ARCHIVED/20260115_JMIR-Submission/paper.md`. Rewritten as Viewpoint (~3,600 body words). See GH#506.

## Essential Commands

**Always use `uv run` to execute Python** (never bare `python` or `python3`). This ensures the correct venv and dependencies.

```bash
# Build paper (all formats)
./scripts/build_paper.sh --format all

# CLI tools (not in project deps)
uv tool install yt-dlp                  # YouTube metadata/download

# Quality checks (run before commits)
uv run ruff format . && uv run ruff check --fix .
uv run mypy scripts/ lit_review/
uv run pytest
uv run python scripts/validate_references.py --all
uv run python scripts/validate_jmir_compliance.py --article-type viewpoint

# Word count (body only, excludes frontmatter + back matter)
# Note: validator strips markdown artifacts; raw wc -w gives ~10% higher count
cat paper.md | sed '1,/^---$/d' | sed '/^# Acknowledgments/,$d' | wc -w

# Build artifacts: rebuild after any paper.md edit, then commit.
# Pre-commit hooks fix trailing whitespace in generated HTML files,
# so build artifact commits require two stages: first attempt triggers
# hook fixes, then re-stage and commit.

# GitHub CLI with secrets (injects GH_TOKEN from OS keyring)
# IMPORTANT: Always use secrets_run.py for gh CLI. Bare `gh` lacks token permissions.
uv run scripts/secrets_run.py gh issue list --label "P0"
uv run scripts/secrets_run.py gh issue create --title "..."

# PR inline review comments (not visible via `gh pr view --comments`):
uv run scripts/secrets_run.py gh api repos/OWNER/REPO/pulls/PULL_NUMBER/comments

# Container testing (catches issues local pytest misses)
podman machine start                    # Start podman VM (macOS)
podman build -t yuimedi-paper -f Containerfile .
podman run --rm --security-opt label=disable -v "$(pwd)":/app yuimedi-paper uv run pytest -m "not integration and not benchmark"
# WARNING: bind mount overwrites .venv with Linux binaries; run `uv sync` after
```

## Branch Strategy

`main` ← `release/*` ← `develop` ← `contrib/stharrold` ← `feature/*`
- Direct commits allowed on `feature/*` and `contrib/*`
- `develop` and `main` require PRs

## Commit Convention

Conventional commits: `fix(paper):`, `feat(ci):`, `docs:`, `build:`
Include `Closes #<issue>` to auto-close GitHub issues.

## Writing Rules

- **No em-dashes (—) in any file** (paper, scripts, docs). Use commas, colons, semicolons, or parentheses instead. Python strings use ASCII hyphens.
- Citations use pandoc-citeproc: `[@key]`, multiple: `[@wu2024; @himss2024]`
- BibTeX in `references.bib`, styled with `citation-style-ama.csl` (AMA 11th ed)
- Framework is **descriptive** (reveals interconnections), not **prescriptive** (recommends solutions)
- Conversational AI is a "Governance Forcing Function," not the standalone solution
- **JMIR Viewpoint format:** No "Methods" or "Results" H1 headers; unstructured abstract (≤450 words); body ≤5,000 words. See `standards/jmir_submission_article-types.md` lines 60-73.

## Visual & Video Abstracts (AJE / Springer Nature Author Services)

- **Visual abstract** (graphical abstract): Ticket #1144316, V2 delivered, revision requested 2026-03-23
- **Video byte** (60-90s video): Ticket #1144097, approved and published 2026-02-25
- YouTube: `q4sE4O9F9pU` (AJE Video Bytes channel), Vimeo: `1161046047` (Password: AJE_Healthcare)
- Contact: support@as.springernature.com (Bhavik, Darshan J)
- Framework is **descriptive** (reveals interconnections), not **prescriptive** (recommends solutions) -- enforce this in all communications

## Secrets Management

Cross-platform secret injection via OS keyring (macOS Keychain, Windows Credential Locker, Linux SecretService). Chosen over `direnv` because `direnv` lacks native Windows/PowerShell support.

```bash
# First-time setup (interactive, stores in OS keyring)
uv run scripts/secrets_setup.py

# Verify secrets are configured
uv run scripts/secrets_setup.py --check

# Run any command with secrets injected
uv run scripts/secrets_run.py gh issue create --title "..."
uv run scripts/secrets_run.py uv run pytest
```

- `secrets.toml` declares secret **names** only (committed to git, no values)
- `scripts/secrets_setup.py` stores values in OS keyring interactively
- `scripts/secrets_run.py` injects keyring values into env vars before running a command
- Precedence: env var > keyring (local) | env var only (CI/container)
- **Do not set `GITHUB_TOKEN` or `GH_TOKEN` globally in shell profiles**; use `secrets_run.py` instead
- `secrets.toml` uses `GH_TOKEN` (not `GITHUB_TOKEN`); this is what `gh` CLI checks first
- After regenerating a GitHub fine-grained PAT, verify write access: `uv run scripts/secrets_run.py gh api --method PATCH repos/OWNER/REPO/issues/1 -f state=open`
- PEP 723 inline scripts (`secrets_run.py`, `secrets_setup.py`) use `importlib.util` for sibling imports because `from scripts.X` fails when run via `uv run scripts/X.py`

## Video Analysis

- AJE video byte has no subtitle track; captions are burned into frames
- Extract frames: `ffmpeg -i video.mp4 -vf "fps=0.5" -q:v 2 output/frame_%04d.jpg`
- Read frames with Claude's multimodal capability to reconstruct narration transcript

## stharrold-templates Bundles

Applied bundles: `git`, `secrets`, `ci` (from `.tmp/stharrold-templates/`).
- Apply: `uv run python .tmp/stharrold-templates/scripts/apply_bundle.py .tmp/stharrold-templates . --bundle git --bundle secrets --bundle ci`
- Dry run first: append `--dry-run`
- After applying: check for residual Gemini naming (`grep -ri gemini .claude/skills/`), fix `Containerfile` COPY lines (needs `LICENSE README.md` before `uv sync`), and delete stale test files for removed modules
- Template-owned files will be overwritten on next apply; repo-specific fixes should be upstreamed to `stharrold-templates`

## Architecture

- **Scripts (`scripts/`):** Python stdlib only, except `secrets_*.py` which use PEP 723 inline deps (`keyring`, `tomlkit`) auto-installed by `uv run`
- **Upstream for `secrets_*.py`:** `../library/scripts/` (sync changes from there)
- **Literature review (`lit_review/`):** Clean Architecture with external deps (pydantic, httpx, click, scikit-learn)
- **Figures:** Mermaid `.mmd` sources → PNG via container + Puppeteer
- **Container:** `Containerfile` with Python 3.12, Pandoc 3.2, TeXLive, Node.js
- **Anthropic SDK**: `response.content[0]` is a union type; filter with `[b for b in response.content if hasattr(b, "text")]` before accessing `.text` (mypy `union-attr`)

## Key Files

| File | Purpose |
|------|---------|
| `paper.md` | Main paper source (Markdown + pandoc-citeproc citations) |
| `references.bib` | BibTeX bibliography |
| `metadata.yaml` | Pandoc metadata for PDF generation |
| `CLAUDE.md` | Comprehensive AI context guide (this file) |
| `scripts/build_paper.sh` | Paper build pipeline |
| `scripts/validate_references.py` | Citation URL validation |
| `scripts/validate_jmir_compliance.py` | Journal compliance checks |
| `secrets.toml` | Secret names declaration (no values; committed to git) |
| `scripts/secrets_setup.py` | Interactive keyring setup for secrets |
| `scripts/secrets_run.py` | Injects secrets from keyring before running commands |
| `cover-letter.md` | Resubmission cover letter for JMIR ms#91493 |
| `abstract-visual-video/` | AJE/Springer Nature deliverables: visual abstract, video byte, email correspondence, critical assessments |
| `docs/plans/` | Implementation plans (created per task) |
| `ARCHIVED/20260115_JMIR-Submission/` | Original rejected submission (~12,730 words) |
| `tests/test_validate_jmir_compliance.py` | Tests for JMIR validator (58 tests, covers Viewpoint + Original) |
| `../library/` | Sibling repo: semantic search engine for academic papers (DuckDB, 23+ ingested papers) |
| `../yuimedi/` | Sibling repo: parent Yuimedi project (lead-gen, meeting notes in `20251212_Meeting_Paper-Conference-Review/`) |
