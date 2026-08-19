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

**Three-paper series:** Paper 1 (Viewpoint, **ACCEPTED** at i-JMR 2026-07-13; copyediting completed 2026-08-10; publication as Interact J Med Res 2026;15:e96541, doi 10.2196/96541, HELD at final stage until the in-house visual abstract is ready, agreed 2026-08-11; the 21.Aug.2026 proof date is superseded) → Paper 2 (empirical validation, Synthea/GCP) → Paper 3 (FHIR/OMOP interoperability). GitHub issues tagged `paper-1`, `paper-2`, `paper-3`.

**Paper 1 history:** Originally submitted as Original Paper (~12,730 words), rejected for length. Archived at `ARCHIVED/20260115_JMIR-Submission/paper.md`. Rewritten as Viewpoint. Desk-rejected at JMIR Medical Informatics (Decision E2, 2026-04-17), transferred to i-JMR 2026-04-22, major revision (Decision D, 2026-06-05; response at `docs/20260607_i-jmr-r1-response-to-reviewers.md`), minor revision (Decision B, 2026-07-07; response at `docs/20260710_i-jmr-r2-response-to-reviewers.md`), R2 submitted 2026-07-11, **accepted 2026-07-13 (Decision A)**. Editor Matthew Balcarras; peer reviewers Moez Hamedani and Xiaoni Zhang (neither was among the 5 nominated on the original submission form, which was desk-rejected before review). Epics #529/#551 closed; released as v4.0.0. GH#506 is retired/superseded by the i-JMR transfer.

**Post-acceptance state:** the published article is the source of truth, not `paper.md`. i-JMR house style differs from this repo: numerals ("3 pillars", "6-step") and lowercase coined terms ("triple threat", "validated query triple"). The one-pass style sync of `paper.md` was completed 2026-08-19 against the `modified5` proof, the version approved for publication (commit e0f920a). This was done ahead of the original trigger (the article going live) because the proof text is final and the hold is on the visual abstract and scheduling only, not on further manuscript changes. If a later proof round changes any wording, re-diff `paper.md` against it before the next release.

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
- **The whitespace hooks edit `.diff` files.** Trailing whitespace is semantically significant in a diff (context lines can legitimately end in spaces). After any commit whose hooks touched a `.diff`, re-verify with `git apply --check --reverse <file>` before re-committing.
- **Pre-commit `ruff` creates `.ruff_cache/` inside `ARCHIVED/<package>/`** because the archived `pyproject.toml` reads as a project root, the same trap as the `.venv` one. It is gitignored so it never enters the commit, but it DOES pollute a filesystem-generated `MANIFEST.sha256`. Regenerate the manifest after the hooks run, then `--amend`.
- **The `.venv` trap:** any `uv run` invocation with cwd inside `ARCHIVED/<package>/` creates a `.venv` there too, for the same reason. Clean it with `rm -rf ARCHIVED/<package>/.venv`, never a bare `rm -rf .venv` after `cd`-ing back out; the bare form can delete the repo ROOT's own venv if the cwd didn't fully return, breaking pre-commit/ruff/mypy with cryptic errors until `uv sync` rebuilds it.

## Writing Rules

- **No em-dashes (—) in any file** (paper, scripts, docs). Use commas, colons, semicolons, or parentheses instead. Python strings use ASCII hyphens.
- **No bold for emphasis** in paper.md or appendices. JMIR requires italics only (`*text*` not `**text**`). Bold is stripped on acceptance.
- **Corporate authors in `references.bib`** need double braces (`author = {{HIMSS Analytics}}`) to prevent CSL name inversion (e.g., "Analytics H."). Use `and` not `&` inside the protected block.
- **BibTeX author fields must use `Family, Given and Family, Given` separators.** Comma/`&`/`et al` blobs parse as single names and render mangled in the reference list ("Latrella &B M."). Name particles need braces: `{{de Holan}, Pablo Martin}` renders "de Holan PM" (unbraced, the CSL demotes to "Holan PM de"). Use `and others` for et-al.
- **`references.bib` is hand-maintained** (the converter workflow is retired). AMA CSL renders `doi:` for DOI-bearing entries, so `url` field edits don't change their rendered reference; URLs still matter for no-DOI entries and `validate_references.py`. `scripts/url_allowlist.json` (bib-key -> URL) suppresses known publisher bot-wall 403s; keep its URLs synced when bib URLs change, and prune keys removed from the bib.
- **`audit_references.py` cannot verify no-DOI entries.** It cross-matches titles via Crossref, which requires a DOI; 25 of 84 entries have none, so their titles were never checked against anything while `validate_references.py` passed them (the URL resolves, the title is wrong). A 2026-08-10 sweep of all 24 no-DOI entries with URLs found **5 defective** (`himss2024news`, `moore2018`, `anthropic2025`, `bravorocca2023`, `nsi2025`). Sweep method: fetch each URL with a browser User-Agent, take the HTML `<title>`/`og:title` or page 1 of the PDF, diff against the stored title. Use one temp file per URL (a shared path races across threads). Bot-walled publishers (HIMSS, ScienceDirect) must be checked against the local copies in `../library/docs/`.
- **Unversioned source URLs rot by overwrite.** `nsi2025` cites an annual report at a URL NSI replaces each year; it now serves the 2026 edition. Check `note` fields for edition caveats before trusting a year.
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
- **`secrets_run.py` prints `[INFO]`/`[OK]`/`[WARN]` banner lines to stdout**, so `gh ... --json ... | python3 -c "json.load(...)"` fails with "Extra data". Use `gh --jq` and grep the formatted line out of the banner noise instead of parsing the whole stream.
- **Do not put `<(...)` process substitution inside a shell function** in this environment; it silently yields no matches, so a verification helper reports every check as failing. Pre-write the data to a file and grep that.

## Video Analysis

- AJE video byte has no subtitle track; captions are burned into frames
- Extract frames: `ffmpeg -i video.mp4 -vf "fps=0.5" -q:v 2 output/frame_%04d.jpg`
- Read frames with Claude's multimodal capability to reconstruct narration transcript

## Terminology

- **HITL-KG**: Human-in-the-Loop Knowledge Governance (was HiL-SG). Industry-standard HITL acronym + established "knowledge governance" field (Foss 2007).
- **Three-Pillar Assessment Rubric**: Replaced Analytics Resilience Index (ARI). 9 indicators across 3 pillars with Low/Medium/High anchors.
- **Validated Query Triple**: NL Intent + Executable SQL + Rationale Metadata. Keep "triple" (not "tuple").
- **AMAM**: expand as "**Analytics Maturity Assessment Model**". HIMSS renamed the model at its 2024-10-02 relaunch (HIMSS24 APAC); "Adoption Model for Analytics Maturity" is the legacy name, surviving only on himssanalytics.org. This supersedes the R1-era decision in commit `64ca59f`, which chose the legacy expansion. Cited source titles keep their published wording either way.
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
- **Multimedia appendix uploads must be named `<ms#>-Multimedia-Appendix-N.docx`** (e.g. `96541-Multimedia-Appendix-1.docx`). The system requires this, so the repo's build output name (`multimedia_appendix_N.docx`) has to be renamed on the way out.
- **The appendices JMIR holds are the last files you uploaded, not the copyedited ones.** They are separate uploads that in-system copyedits never touch, so a copyeditor's bibliography or terminology corrections reach the manuscript and silently leave the appendices stale. At the 2026-08-13 proof round this left appendix 2 contradicting the article on 2 references, plus 2 author lists that JMIR's own typesetting had mangled ("Shahbaz G M.", "Ziletti &D A."), and appendix 1 quoting a section title that no longer existed. Re-review and re-supply the appendices at EVERY proof round.
- **`author:` and `date:` are duplicated across `metadata.yaml` and `paper.md`'s own YAML header**, and `header-right:` is a third hardcoded copy of the date. `metadata.yaml` feeds the appendix builds; `paper.md`'s header feeds `paper.docx`. Changing one splits them silently. After any such edit, grep for the OLD value rather than confirming the new one, or the second copy survives undetected.
- Pandoc renders `title`/`author`/`date` into the DOCX **body**, but a DOCX to `plain` conversion lifts them into metadata and drops them from the text. Any appendix or manuscript check done via `pandoc -t plain` is blind to the byline and date; read `word/document.xml` instead.
- i-JMR resubmission form structure: section A = clean manuscript (no tracked changes), B = editor notification (paste the plain-text point-by-point response), D = title + Unstructured abstract (plain text, the easy-to-miss field) + keywords, section 1 = figures, section 2 = ALL multimedia appendices, section 3 = additional material (tracked-changes docx + response PDF + TOC/feature image + License/Permission proof). No cover-letter slot on the revision form.
- **The submission package dir (`ARCHIVED/<date>_IJMR-Submission/`) is the submission source of truth**; repo-root artifacts are CI builds. Conventions: every section-3 upload gets a `_metadata.txt` companion (generation provenance + Description field text in long/short variants); the response PDF is a CLEAN copy (internal "NOTE FOR SUBMISSION"/"DO NOT SEND" blocks stripped, `====` ASCII dividers converted to headings; the .md keeps them for the plain-text section-B paste); dated plaintext files for every form field (`_title-`, `_abstract-`, `_keywords-plaintext.txt`, keywords semicolon-separated); archive the submitted system file (`96541-NNNNNNN-1-ED.docx`), form PDF, and confirmation email after submission.
- Point-by-point response letters: verify every quoted caption/count against the built manuscript before submitting (letters go stale as edits continue; understated audit counts read as undisclosed changes against the tracked-changes diff).

### Copyediting stage (post-acceptance)

- Copyediting happens **in JMIR's Kriyadocs web system** (Chrome only, submitting author only), NOT by uploading a DOCX to a form. Address every query in-system, add queries for anything the system can't do, then Approve and Submit, which closes author access until final proofs. Turnaround: 2-3 business days.
- The copyedited proof PDF arrives as an email attachment (`96541.pdf`); the reply-with-edits is `96541_modified.pdf`. Archive both.
- The proof's end matter carries the **planned publication date** and the assigned DOI. It is a pre-populated field, not a commitment.
- Review the modified proof by text-diffing it against the original: `pdftotext -layout` both, flatten with `tr -s ' \n' ' '`, then grep short needles. Two-column layout interleaves columns, so long contiguous phrases produce false negatives; verify a failed match by eye before reporting it.
- **Checking reference-list integrity (all `[N]` citations present, in numeric order) needs plain `pdftotext`, NOT `-layout`.** `-layout` interleaves the two-column reference list and breaks the line-start regex for reference numbers, producing dozens of false "cited but not listed" gaps. Use `-layout` for phrase diffing (above); use the no-flag reading-order extraction for citation-count and citation-order checks.
- **Confirming figures are untouched across proof rounds:** `pdfimages -png <proof>.pdf out-prefix` then `shasum -a256` each PNG. Only render to PNG (`pdftoppm -png -r 150`) and inspect visually when a hash differs; rasterized figure label text never shows up in a text diff.
- Expect "not previously stated" queries on terms that live only in the title/abstract/figures. Compression from the 12,730-word Original Paper to the ~4,500-word Viewpoint cut introducing passages while leaving downstream references intact (hit twice: "three-pillar structure", "AI query generation").
- The copyeditor may silently correct your bibliography. Diff their reference list against `references.bib` and back-port their fixes.

### Production stage: who owns what

- **Laura McReynolds** (laura.mcreynolds@jmir.org, Production Editor, cc production@jmir.org) owns the publication date, the ToC image, and the purchased promotion products. Thread runs to the **yuimedi** address. She is the escalation point for anything cross-team.
- **Natalia March** (natalia.march@jmir.org, Author Experience Manager) owns the in-house visual abstract. Thread runs to the **gmail** address, so the two are separate threads and neither sees the other by default.
- Purchased promotion products on ms#96541: **Sponsored Tweet Campaign** and **Lifelong Author Ad** (banner points to https://us.yuimedi.com/).
- Visual abstract service: **3 weeks from receipt of the completed questionnaire**, **ONE** author review round, extensive later changes may incur charges. If the article is production-ready first it publishes with a JMIR-selected standard ToC image and the graphic is swapped in later.
- The **sponsored tweet is the timing exposure, not the ToC image.** A ToC image swaps after publication for free; a sponsored tweet is a one-shot spend that would carry the placeholder. Raise timing with Laura, not Natalia.
- **The visual abstract cannot be expedited** (outsourced vendor, contractual minimum turnaround), but **the paper CAN be held at the final production stage** until it is ready. That hold was Laura's own recommendation and was accepted 2026-08-11: publish with the visual abstract in place and send the sponsored tweet alongside it. The proof's publication date is an estimate and is editable in the end matter.
- **Publishing first is the irreversible branch.** If the article goes live with a standard ToC image, a *default, non-promoted* tweet may fire automatically at publication carrying that placeholder, which no later swap undoes; Laura flagged this as unconfirmed and was checking with marketing. Holding avoids it entirely and keeps the launch under her direct control. Swapping the ToC later updates the HTML article and JMIR listing pages; the PDF never carries the ToC image at all, so the PDF is not a consideration.
- The hold as agreed has **no outside date**. If the vendor slips well past the ~3-week estimate (questionnaire submitted 2026-08-06, so a draft near 27.Aug.2026 plus one review round and a revision pass), propose a bound rather than letting it run open-ended. Mid-September still falls in volume 15 (2026), so the citation is unaffected either way.
- The AJE-commissioned graphic **cannot be the ToC image** (JMIR policy) and was declined as a Multimedia Appendix on 2026-08-10: it carries the pre-copyediting title, never names HITL-KG, and would reintroduce superseded terminology. Rights were never the obstacle (AJE's ToS makes no copyright claim over Manuscript Services; copyright is Harrold / Yuimedi).

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
- **Figures:** Mermaid `.mmd` sources → PNG via container + Puppeteer. `figures/puppeteer-config.json` hardcodes `/usr/bin/chromium` and works only in the container; on macOS mermaid-cli fails with "Could not find Chrome". Pass a host config instead: `npx --yes @mermaid-js/mermaid-cli@latest -p <cfg> -i figures/X.mmd -o figures/X.mmd.png`, where `<cfg>` sets `executablePath` to `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. Regenerate the 1200px upload copy afterward (`cp X.mmd.png X.figure.png && sips --resampleHeight 1200 X.figure.png`) and check for style drift by comparing dimensions and viewing both renders.
- **Figure label text is rasterized into the PNG**, so copyeditor requests on figure wording require editing the `.mmd` and re-rendering; a manuscript rebuild alone changes nothing. The `figures/*.caption.txt` files are upload-form metadata (not build inputs) and go stale silently when node labels change.
- **Container:** `Containerfile` with Python 3.11, pinned Pandoc 3.8.2.1, TeXLive, Node.js
- **Multi-stage Python containers:** builder `WORKDIR` must equal runtime `WORKDIR` (console-script shebangs are absolute paths baked at venv-creation time). Use `uv sync --no-editable` after copying sources so entry points survive `COPY --from=builder`. Multi-stage structure pattern lives in `Containerfile.lit_review`; `uv` installation pattern (via `COPY --from=ghcr.io/astral-sh/uv:...`) lives in the main `Containerfile`. Both `Containerfile` and `Containerfile.lit_review` install uv via `COPY --from=ghcr.io/astral-sh/uv:0.5.5`.
- **Anthropic SDK**: `response.content[0]` is a union type; filter with `[b for b in response.content if hasattr(b, "text")]` before accessing `.text` (mypy `union-attr`)

## Release Train (learned running v5.0.0)

- **Version comes from the tag convention, not from tooling.** MAJOR marks a manuscript lifecycle milestone: v2.0.0 submission, v3.0.0 R1, v4.0.0 R2, v5.0.0 accepted+copyedited. `.claude/skills/git-workflow-manager/scripts/semantic_version.py` only classifies `src/**.py` as a feature and `tests/`/`docs/`/`resources/`/`pyproject.toml` as a patch, so this repo's content (`paper.md`, `references.bib`, `figures/`, `ARCHIVED/`) matches **nothing** and it always defaults to PATCH. It returned 4.0.1 for a 103-file release. Record the override reasoning in the release PR.
- **The CI gate cannot be satisfied on `contrib/stharrold`.** Every push triggers Paper Artifacts Generation, which pushes a `[skip ci]` commit that becomes the PR head with zero check-runs, so `gh pr checks` returns exit 1 and "no checks reported". The PDF rebuild is nondeterministic (differs by ~5 bytes), so it commits every time and the loop never converges. Verify the **source** commit's checks instead, then confirm the artifacts by content: grep `paper.docx` for the expected changes and hash `word/media/*` against `figures/*.mmd.png`. On `release/*` branches the gate behaves normally.
- Release order that worked: PR contrib->develop (wait for the artifact `[skip ci]` commit first) -> confirm version -> `release/vN.N.N` from develop -> bump `pyproject.toml` + `uv lock` + `CITATION.cff` (version AND `date-released`) + `.zenodo.json` -> PR to main -> merge -> annotated tag on the merge commit -> `gh release create` -> verify Zenodo -> backmerge main->develop -> fast-forward contrib.
- `Build and Push Container` **fails on every release** at the SBOM-attach step (`Resource not accessible by integration`); the workflow has no `permissions:` block. Non-required, so it does not block merges. Tracked in #565; the `[skip ci]` head-commit problem is #566.

## Zenodo Integration

- Repo has an active release webhook (hook id `591675875`) to `zenodo.org/api/hooks/receivers/github/events/`.
- Webhook fires on GitHub **Release publish**, not tag push. `release_workflow.py tag-release` only creates the tag; run `gh release create vX.Y.Z` afterward (with the concept DOI leading the notes) to actually trigger Zenodo archival.
- Webhook `202 Accepted` is only queue ack; actual archival is async and can fail silently. Verify a new version actually appears on the [Zenodo record page](https://doi.org/10.5281/zenodo.18264359) after each release, or via API: `curl -s "https://zenodo.org/api/records?q=conceptdoi:%2210.5281/zenodo.18264359%22&sort=mostrecent&size=1"` (check `metadata.version`).
- **`metadata.version` is the tag verbatim, i.e. `v5.0.0` with the `v`.** A poll comparing against `5.0.0` never matches and runs to its iteration limit, which looks identical to a failed archival. Compare against the tag string, and make any wait-loop emit on failure as well as success.
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
| `ARCHIVED/20260810_IJMR-Copyediting/` | Copyediting round of record: both proofs, correspondence, reply, full build snapshot (inputs + tooling + artifacts + vendored Eisvogel template), `BUILD-PROVENANCE.md`, `MANIFEST.sha256`, source diff |
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

## i-JMR house style (learned at the 96541 proof rounds)

- **Numerals never open a sentence or a title.** House style converts small numbers to numerals ("3 pillars", "6-step", "2 critical weaknesses") EXCEPT sentence-initially. A caption is a sentence, so "Three-pillar assessment rubric indicators" is correct while "The 6-step validated query cycle and its mapping to the 3 pillars" is also correct. Check position before calling a spelled-out number an inconsistency.
- **Section cross-references take the form `the <Section Title>` with the title verbatim.** When the section title itself begins with "The", this produces "the The Evidence Base: 3 Pillars section". That doubling is REQUIRED, not a typo. The control case is "in the Theoretical Grounding: Socialization Failure section", same rule, no doubling only because that title does not start with "The".
- Both of the above are constructions that read as errors in isolation but are mandated by a rule operating one level up. Verify the rule before raising either.
