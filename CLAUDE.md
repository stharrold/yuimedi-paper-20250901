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

**Topic:** "Mitigating Institutional Amnesia" in healthcare analytics via Human-in-the-Loop Knowledge Governance (HITL-KG).

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

# Word count (JMIR method: excludes metadata + references only)
# See: standards/jmir_submission_word-count-elements.md
cat paper.md | sed '1,/^---$/d' | sed '/^# References/,$d' | wc -w  # limit: 5,000

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
podman run --rm --security-opt label=disable -v "$(pwd)":/app -v yuimedi_venv_cache:/app/.venv -w /app yuimedi-paper uv run pytest -m "not integration and not benchmark"
# Named venv cache (`yuimedi_venv_cache`) avoids host/container binary conflicts and the need for manual `uv sync`
```

## Branch Strategy

`main` ← `release/*` ← `develop` ← `contrib/stharrold` ← `feature/*`
- Direct commits allowed on `feature/*` and `contrib/*`
- `develop` and `main` require PRs
- `/workflow:v7x1_3-release` cuts the release branch from `origin/develop`. Always run `/workflow:v7x1_2-integrate` first to move `contrib/*` commits into `develop`, otherwise the release will ship without them.

## Commit Convention

Conventional commits: `fix(paper):`, `feat(ci):`, `docs:`, `build:`
Include `Closes #<issue>` to auto-close GitHub issues.

## Writing Rules

- **No em-dashes (—) in any file** (paper, scripts, docs). Use commas, colons, semicolons, or parentheses instead. Python strings use ASCII hyphens.
- **No bold for emphasis** in paper.md or appendices. JMIR requires italics only (`*text*` not `**text**`). Bold is stripped on acceptance.
- **Corporate authors in `references.bib`** need double braces (`author = {{HIMSS Analytics}}`) to prevent CSL name inversion (e.g., "Analytics H."). Use `and` not `&` inside the protected block.
- **Figure max dimension:** 1200px for JMIR upload. Resize preserving aspect ratio: macOS `sips --resampleHeight 1200 <file>`, cross-platform (ImageMagick) `mogrify -resize x1200 <file>`.
- **Pandoc image sizing in paper.md:** specify only ONE of `{width=X%}` or `{height=Yin}`. LaTeX preserves aspect ratio by default when a single dimension is given; both together distorts unless `keepaspectratio` is set. Size square figures by width, portrait figures by height (a modest width on a tall figure blows past page bottom).
- **Figure float gotcha:** if a figure is slightly too large, the caption stays on-page with the figure but the figure's *introductory sentence* gets orphaned on a blank preceding page (LaTeX floats don't drag their intro text). After resizing, verify total page count; a nearly-blank page between figures means the next image needs a small reduction.
- **Always rebuild ALL artifacts** after editing paper.md: `./scripts/build_paper.sh --format all`. Reviewers check paper.tex/paper.docx for stale terminology.
- Citations use pandoc-citeproc: `[@key]`, multiple: `[@wu2024; @himss2024]`
- BibTeX in `references.bib`, styled with `citation-style-ama.csl` (AMA 11th ed)
- As a Viewpoint, the paper advances a **prescriptive** position grounded in descriptive evidence. The framework's *analysis* of why current approaches fail is descriptive; the *recommendations* (HITL-KG, Three-Pillar Assessment, governance tiers) are intentionally directive.
- Conversational AI is a "Governance Forcing Function," not the standalone solution
- **JMIR Viewpoint format:** No "Methods" or "Results" H1 headers; unstructured abstract (≤450 words); body ≤5,000 words. See `standards/jmir_submission_article-types.md` lines 60-73.

## Visual & Video Abstracts (AJE / Springer Nature Author Services)

- **Visual abstract** (graphical abstract): Ticket #1144316, V2 delivered, revision requested 2026-03-23
- **Visual abstract assessments:** Two-pass: (1) paper-consistency for author, (2) general-audience for vendor email. General audience assessment drives revision requests. Saved to `abstract-visual-video/YYYYMMDDTHHMMSSZ_visual-abstract_critical-assessment.md`
- **Pre-commit blocks files >10MB.** Video byte (51MB) cannot be committed to git.
- **Video byte** (60-90s video): Ticket #1144097, approved and published 2026-02-25
- YouTube: `q4sE4O9F9pU` (AJE Video Bytes channel), Vimeo: `1161046047` (Password: AJE_Healthcare)
- Contact: support@as.springernature.com (Bhavik, Darshan J)
- In external communications (visual abstract, video byte), emphasize the framework's **descriptive** analysis of interconnected challenges; the paper's prescriptive recommendations are for the academic audience

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

## Terminology

- **HITL-KG**: Human-in-the-Loop Knowledge Governance (was HiL-SG). Industry-standard HITL acronym + established "knowledge governance" field (Foss 2007).
- **Three-Pillar Assessment Rubric**: Replaced Analytics Resilience Index (ARI). 9 indicators across 3 pillars with Low/Medium/High anchors.
- **Validated Query Triple**: NL Intent + Executable SQL + Rationale Metadata. Keep "triple" (not "tuple").
- **Zenodo DOI**: 10.5281/zenodo.18264359 (concept DOI: resolves to latest version; always use this, never a version-specific DOI)

## stharrold-templates Bundles

Applied bundles: `git`, `secrets`, `ci` (from `.tmp/stharrold-templates/`).
- Apply: `uv run python .tmp/stharrold-templates/scripts/apply_bundle.py .tmp/stharrold-templates . --bundle git --bundle secrets --bundle ci`
- Dry run first: append `--dry-run`
- After applying: check for residual Gemini naming (`grep -ri gemini .claude/skills/`), fix `Containerfile` COPY lines (needs `LICENSE README.md` before `uv sync`), and delete stale test files for removed modules
- Template-owned files will be overwritten on next apply; repo-specific fixes should be upstreamed to `stharrold-templates`

## Research Workflow

- **Questions index:** `docs/research/Research-Questions.md` (35 answered, 13 unanswered)
- **Answer files:** `docs/research/answers/Research_<slug>.md` (63 files, each with full citations + URLs)
- **Every new paper claim must trace to a research answer file** with source URLs and citation metadata
- **Google Scholar Labs:** Use Playwright MCP (`authuser=1` for second account if daily limit hit); click "New session" between questions; each query evaluates ~60-200 results, surfaces ~10 papers
- **Scholar Labs workflow:** `docs/guides/scholar-labs-workflow.md`

## Paper Revision Process

1. Critical assessment of current PDF -> `ARCHIVED/` with timestamp
2. Recommendations doc -> `ARCHIVED/` (may have multiple versions, v2 supersedes v1)
3. Cross-reference with original rejected submission (`ARCHIVED/20260115_JMIR-Submission/`) for recoverable material
4. Identify research gaps -> search Google Scholar Labs -> save to `docs/research/answers/`
5. Update `docs/research/Research-Questions.md` with each answered question
6. Implementation plan with line-level edits, word budget, commit sequence -> `ARCHIVED/`
7. Execute in passes (language edits -> content additions -> supporting improvements -> figures)

## CI Notes

- `validate_documentation.sh` uses `uv` -> `python3` fallback (CI lacks `uv`)
- CI auto-commits (`[skip ci]`) can diverge from local; may need `--force-with-lease` on contrib branch
- Paper Artifacts Generation requires pandoc + texlive in Containerfile
- Don't pipe remote install scripts in Containerfiles. For `uv`, use `COPY --from=ghcr.io/astral-sh/uv:<version> /uv /uvx /usr/local/bin/` (astral.sh install endpoint has returned 502s that hard-fail builds).

## Architecture

- **Scripts (`scripts/`):** Python stdlib only, except `secrets_*.py` which use PEP 723 inline deps (`keyring`, `tomlkit`) auto-installed by `uv run`
- **Upstream for `secrets_*.py`:** `../library/scripts/` (sync changes from there)
- **Literature review (`lit_review/`):** Clean Architecture with external deps (pydantic, httpx, click, scikit-learn)
- **Figures:** Mermaid `.mmd` sources → PNG via container + Puppeteer
- **Container:** `Containerfile` with Python 3.12, Pandoc 3.2, TeXLive, Node.js
- **Multi-stage Python containers:** builder `WORKDIR` must equal runtime `WORKDIR` (console-script shebangs are absolute paths baked at venv-creation time). Use `uv sync --no-editable` after copying sources so entry points survive `COPY --from=builder`. Pattern lives in `Containerfile.lit_review`.
- **Anthropic SDK**: `response.content[0]` is a union type; filter with `[b for b in response.content if hasattr(b, "text")]` before accessing `.text` (mypy `union-attr`)

## Zenodo Integration

- Repo has an active release webhook (hook id `591675875`) to `zenodo.org/api/hooks/receivers/github/events/`.
- Webhook `202 Accepted` is only queue ack; actual archival is async and can fail silently. Verify a new version actually appears on the [Zenodo record page](https://doi.org/10.5281/zenodo.18264359) after each release.
- Diagnose failures at https://zenodo.org/account/settings/github/ (shows last-build status per repo).
- Redeliver a failed webhook: `gh api --method POST repos/stharrold/yuimedi-paper-20250901/hooks/591675875/deliveries/<id>/attempts`.

## Key Files

| File | Purpose |
|------|---------|
| `ARCHIVED/YYYYMMDDTHHMMSSZ_critical-assessment_*.md` | Critical assessments of paper drafts |
| `ARCHIVED/YYYYMMDDTHHMMSSZ_recommendations_*.md` | Revision recommendations (versioned) |
| `ARCHIVED/YYYYMMDDTHHMMSSZ_implementation-plan_*.md` | Line-level implementation plans for paper edits |
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
| `submission-checklist.md` | JMIR submission checklist (Viewpoint, ms#91493) |
| `project-status.md` | Lightweight project status for all 3 papers |
| `reference.docx` | Custom Word template (Times New Roman 12pt, double-spaced, black headings) |
| `ARCHIVED/20260329_JMIR-Submission/` | Complete submission archive (37 files) |
| `ARCHIVED/20260115_JMIR-Submission/` | Original rejected submission (~12,730 words) |
| `tests/test_validate_jmir_compliance.py` | Tests for JMIR validator (58 tests, covers Viewpoint + Original) |
| `../library/` | Sibling repo: semantic search engine for academic papers (DuckDB, 23+ ingested papers) |
| `../yuimedi/` | Sibling repo: parent Yuimedi project (lead-gen, meeting notes in `20251212_Meeting_Paper-Conference-Review/`) |
