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

**Three-paper series:** Paper 1 (Viewpoint, ms#96541 at i-JMR; transferred from JMIR Medical Informatics after Decision E2 desk-reject 2026-04-17; major revision Decision D 2026-06-05, R1 resubmitted 2026-06-15; minor revision Decision B 2026-07-07, R2 submitted 2026-07-11, awaiting decision; epics #529/#551 closed; released as v4.0.0) → Paper 2 (empirical validation, Synthea/GCP) → Paper 3 (FHIR/OMOP interoperability). GitHub issues tagged `paper-1`, `paper-2`, `paper-3`.

**Paper 1 history:** Originally submitted as Original Paper (~12,730 words), rejected for length. Archived at `ARCHIVED/20260115_JMIR-Submission/paper.md`. Rewritten as Viewpoint (~4,470 body words). Desk-rejected at JMIR Medical Informatics (Decision E2), transferred to i-JMR, major revision (Decision D, 2026-06-05; R1 response at `docs/20260607_i-jmr-r1-response-to-reviewers.md`), then minor revision (Decision B, 2026-07-07; R2 response at `docs/20260710_i-jmr-r2-response-to-reviewers.md`); R2 submitted 2026-07-11, awaiting decision. GH#506 (resubmit to JMIR Medical Informatics) is retired/superseded by the i-JMR transfer.

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
uv run python scripts/audit_references.py --skip-landing  # DOI/metadata audit; run after any references.bib edit

# Word count: the compliance validator reports BOTH counts; the JMIR-Method
# count is the authoritative one (title + abstract + keywords + body incl.
# tables and figure captions + end matter + abbreviations; excludes only
# references, author metadata, figure content, appendices; limit 5,000).
# The editor counts the whole DOCX in Word, which tracks the JMIR-method
# count once references are subtracted. Do NOT use a body-only count to
# judge compliance. See: standards/jmir_submission_word-count-elements.md

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
- Avoid `git add -A <dir>` when the dir holds untracked large files (e.g. the 51MB video byte in `abstract-visual-video/`): it stages them, trips the >10MB pre-commit hook, and silently aborts the commit (the push then reports "Everything up-to-date" with HEAD unchanged). Stage specific files instead.
- ANY commit whose hooks modify files (trailing whitespace in generated HTML) silently aborts the same way ("[INFO] Restored changes from .../pre-commit/patch..."). Recovery: `git add -u && git commit` with the same message; always verify HEAD moved with `git log --oneline -1`.
- New Python files under `scripts/` need SPDX headers after the shebang (`# SPDX-FileCopyrightText: 2025 stharrold` + `# SPDX-License-Identifier: Apache-2.0`) or the spdx-headers hook rejects the commit.

## Writing Rules

- **No em-dashes (—) in any file** (paper, scripts, docs). Use commas, colons, semicolons, or parentheses instead. Python strings use ASCII hyphens.
- **No bold for emphasis** in paper.md or appendices. JMIR requires italics only (`*text*` not `**text**`). Bold is stripped on acceptance.
- **Corporate authors in `references.bib`** need double braces (`author = {{HIMSS Analytics}}`) to prevent CSL name inversion (e.g., "Analytics H."). Use `and` not `&` inside the protected block.
- **BibTeX author fields must use `Family, Given and Family, Given` separators.** Comma/`&`/`et al` blobs parse as single names and render mangled in the reference list ("Latrella &B M."). Name particles need braces: `{{de Holan}, Pablo Martin}` renders "de Holan PM" (unbraced, the CSL demotes to "Holan PM de"). Use `and others` for et-al.
- **`references.bib` is hand-maintained** (the converter workflow is retired). AMA CSL renders `doi:` for DOI-bearing entries, so `url` field edits don't change their rendered reference; URLs still matter for no-DOI entries and `validate_references.py`. `scripts/url_allowlist.json` (bib-key -> URL) suppresses known publisher bot-wall 403s; keep its URLs synced when bib URLs change, and prune keys removed from the bib.
- **Bibliography audit evidence** lives in gitignored `bibliography-audit/` (files 0-7 per citation; `audit_references.py` regenerates 0-5 idempotently and never touches the hand-written 6 = author-verified metadata and 7 = full-text verification records). `VERIFICATION-LOG.md` there documents the layout. Full texts for grep-verification: `../library/docs/<paper-dir>/page_NNN.md` chunks.
- **Figure max dimension:** 1200px for JMIR upload. Resize preserving aspect ratio: macOS `sips --resampleHeight 1200 <file>`, cross-platform (ImageMagick) `mogrify -resize x1200 <file>`. Upload copies are `figures/*.figure.png`; build sources (`*.mmd.png`) stay full-size.
- **Figure/table caption numbering:** pandoc's DOCX writer emits captions with NO "Figure N"/"Table N" prefix (only LaTeX auto-numbers), so the reviewed DOCX shows bare caption text. Captions carry literal "Figure 1." / "Table 1." prefixes in paper.md, with `\usepackage[labelformat=empty]{caption}` in `metadata.yaml` header-includes suppressing LaTeX's auto-label (else the PDF shows "Figure 1: Figure 1."). JMIR figure style = short numbered caption + separate footnote paragraph below the image.
- **DOCX table borders come from `reference.docx`'s `Table` style** (pandoc emits no inline borders). The style now defines full gridlines; edit it by unzipping `reference.docx`, patching `word/styles.xml`, re-zipping. Keywords render only in DOCX document properties (docProps/core.xml), never in the body.
- **Pandoc image sizing in paper.md:** specify only ONE of `{width=X%}` or `{height=Yin}`. Pandoc *always* injects a page-fit secondary dimension (`height=\textheight` or `width=\linewidth`), but whether `keepaspectratio` is auto-injected depends on the pandoc version: recent local pandoc emits it, but the CI container's pandoc does not, so without the `\setkeys{Gin}{keepaspectratio}` `header-includes` entry in `metadata.yaml`, CI-built figures get stretched to exactly the specified width-by-height box. Size square figures by width, portrait figures by height (a modest width on a tall figure blows past page bottom).
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

## Submission Tooling

- PDF redaction for the public repo: rasterize first (`pdftoppm -png -r 150`) then paint an opaque box with Pillow (`uv run --with pillow`). A black box drawn over a PDF text layer leaves the underlying text extractable.
- Tracked-changes (redline) manuscript: `npx --yes pandiff old.docx paper.docx -o out.docx` produces native Word tracked changes (`w:ins`/`w:del`). Set the author with `sed -i '' 's/w:author="unknown"/w:author="Samuel T Harrold"/g' word/document.xml` then re-zip. pandiff can't embed images mid-diff, so figures render as their captions; upload figure files separately.
- i-JMR resubmission form structure: section A = clean manuscript (no tracked changes), B = editor notification (paste the plain-text point-by-point response), D = title + Unstructured abstract (plain text, the easy-to-miss field) + keywords, section 1 = figures, section 2 = ALL multimedia appendices, section 3 = additional material (tracked-changes docx + response PDF + TOC/feature image + License/Permission proof). No cover-letter slot on the revision form.
- **The submission package dir (`ARCHIVED/<date>_IJMR-Submission/`) is the submission source of truth**; repo-root artifacts are CI builds. Conventions: every section-3 upload gets a `_metadata.txt` companion (generation provenance + Description field text in long/short variants); the response PDF is a CLEAN copy (internal "NOTE FOR SUBMISSION"/"DO NOT SEND" blocks stripped, `====` ASCII dividers converted to headings; the .md keeps them for the plain-text section-B paste); dated plaintext files for every form field (`_title-`, `_abstract-`, `_keywords-plaintext.txt`, keywords semicolon-separated); archive the submitted system file (`96541-NNNNNNN-1-ED.docx`), form PDF, and confirmation email after submission.
- Point-by-point response letters: verify every quoted caption/count against the built manuscript before submitting (letters go stale as edits continue; understated audit counts read as undisclosed changes against the tracked-changes diff).

## CI Notes

- `validate_documentation.sh` uses `uv` -> `python3` fallback (CI lacks `uv`)
- Every push to contrib triggers Paper Artifacts Generation, which auto-commits `[skip ci]` artifacts; the NEXT push then rejects as non-fast-forward. Recipe: `git pull --rebase origin contrib/stharrold`; conflicts land on artifact binaries (paper.docx/pdf); resolve with `git checkout --theirs -- <file>` (during rebase, "theirs" = your replayed commit, i.e. keep your build), `git add`, `git rebase --continue`, push. Do NOT force-push.
- **CI pandoc is pinned to 3.8.2.1** (official release .deb in the `Containerfile`) to match local builds. Debian's apt pandoc (2.x) previously caused CI/local divergence: non-AMA author rendering in reference lists ("Michal S. Gal" instead of "Gal MS") and different `\includegraphics` attributes. The pdf-generation workflow now includes an AMA-rendering regression check on the built paper.docx. Still spot-check CI-committed artifacts after a `[skip ci]` regeneration; keep the pinned version in sync with the local pandoc used for submission builds.
- Paper Artifacts Generation requires pandoc + texlive in Containerfile
- Don't pipe remote install scripts in Containerfiles. For `uv`, use `COPY --from=ghcr.io/astral-sh/uv:<version> /uv /uvx /usr/local/bin/` (astral.sh install endpoint has returned 502s that hard-fail builds).
- Build PDF engine: `build_paper.sh` falls back to `tectonic` (xelatex not on direct shell PATH). Standalone pandoc PDF builds (cover letter, response-to-reviewers) need `--pdf-engine=tectonic`.
- Pandoc CLI flags override in-document metadata: `--toc` / `--number-sections` in `build_paper.sh` win over `toc:` / `number-sections:` in `metadata.yaml`. To drop a TOC from the submission, remove the `--toc`/`--toc-depth` flags from all four pandoc calls, not just edit metadata (local and CI pandoc resolve the conflict differently).
- `metadata.yaml` `header-right` is a hardcoded literal (e.g. `"June 2026"`), NOT derived from `date:`. Update it by hand when the submission month changes.

## Architecture

- **Scripts (`scripts/`):** Python stdlib only, except `secrets_*.py` which use PEP 723 inline deps (`keyring`, `tomlkit`) auto-installed by `uv run`
- **Upstream for `secrets_*.py`:** `../library/scripts/` (sync changes from there)
- **Literature review (`lit_review/`):** Clean Architecture with external deps (pydantic, httpx, click, scikit-learn)
- **Figures:** Mermaid `.mmd` sources → PNG via container + Puppeteer
- **Container:** `Containerfile` with Python 3.11, pinned Pandoc 3.8.2.1, TeXLive, Node.js
- **Multi-stage Python containers:** builder `WORKDIR` must equal runtime `WORKDIR` (console-script shebangs are absolute paths baked at venv-creation time). Use `uv sync --no-editable` after copying sources so entry points survive `COPY --from=builder`. Multi-stage structure pattern lives in `Containerfile.lit_review`; `uv` installation pattern (via `COPY --from=ghcr.io/astral-sh/uv:...`) lives in the main `Containerfile`. Both `Containerfile` and `Containerfile.lit_review` install uv via `COPY --from=ghcr.io/astral-sh/uv:0.5.5`.
- **Anthropic SDK**: `response.content[0]` is a union type; filter with `[b for b in response.content if hasattr(b, "text")]` before accessing `.text` (mypy `union-attr`)

## Zenodo Integration

- Repo has an active release webhook (hook id `591675875`) to `zenodo.org/api/hooks/receivers/github/events/`.
- Webhook fires on GitHub **Release publish**, not tag push. `release_workflow.py tag-release` only creates the tag; run `gh release create vX.Y.Z` afterward (with the concept DOI leading the notes) to actually trigger Zenodo archival.
- Webhook `202 Accepted` is only queue ack; actual archival is async and can fail silently. Verify a new version actually appears on the [Zenodo record page](https://doi.org/10.5281/zenodo.18264359) after each release, or via API: `curl -s "https://zenodo.org/api/records?q=conceptdoi:%2210.5281/zenodo.18264359%22&sort=mostrecent&size=1"` (check `metadata.version`).
- Release train (v4.0.0 pattern): PR contrib->develop (wait for the artifact run's `[skip ci]` auto-commit to land on the branch first), release/vX.Y.Z from origin/develop, bump `pyproject.toml` + `CITATION.cff` (version AND `date-released`) + `.zenodo.json` notes, PR->main, tag, `gh release create` (concept DOI first in notes + "Cite this release" block), verify Zenodo, backmerge PR main->develop, re-sync contrib.
- Diagnose failures at https://zenodo.org/account/settings/github/ (shows last-build status per repo).
- Redeliver a failed webhook: `gh api --method POST repos/{owner}/{repo}/hooks/591675875/deliveries/<id>/attempts` (gh CLI resolves `{owner}/{repo}` from the current git remote).

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
| `scripts/audit_references.py` | Per-citation DOI/metadata audit (evidence -> `bibliography-audit/`, gitignored) |
| `scripts/url_allowlist.json` | Bib-key -> URL allowlist for publisher bot-wall 403s |
| `ARCHIVED/20260712_IJMR-Submission/` | R2 submission package of record (submitted system file + form + confirmation email) |
| `scripts/validate_jmir_compliance.py` | Journal compliance checks |
| `secrets.toml` | Secret names declaration (no values; committed to git) |
| `scripts/secrets_setup.py` | Interactive keyring setup for secrets |
| `scripts/secrets_run.py` | Injects secrets from keyring before running commands |
| `cover-letter.md` | R2 resubmission cover letter (i-JMR ms#96541, Decision B) |
| `abstract-visual-video/` | AJE/Springer Nature deliverables: visual abstract, video byte, email correspondence, critical assessments |
| `docs/plans/` | Implementation plans (created per task) |
| `submission-checklist.md` | i-JMR R2 submission checklist (Viewpoint, ms#96541) |
| `project-status.md` | Lightweight project status for all 3 papers |
| `reference.docx` | Custom Word template (Times New Roman 12pt, double-spaced, black headings) |
| `ARCHIVED/20260329_JMIR-Submission/` | Complete submission archive (37 files); rejection email and transfer request email draft also here |
| `ARCHIVED/20260115_JMIR-Submission/` | Original rejected submission (~12,730 words) |
| `tests/test_validate_jmir_compliance.py` | Tests for JMIR validator (58 tests, covers Viewpoint + Original) |
| `../library/` | Sibling repo: semantic search engine for academic papers (DuckDB, 23+ ingested papers) |
| `../yuimedi/` | Sibling repo: parent Yuimedi project (lead-gen, meeting notes in `20251212_Meeting_Paper-Conference-Review/`) |
