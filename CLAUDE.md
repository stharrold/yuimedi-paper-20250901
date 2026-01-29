# CLAUDE.md

## Project Overview

Documentation-focused academic research repository. Primary deliverable: `paper.md` — a Theoretical Framework / Viewpoint paper targeting JMIR Medical Informatics.

**Topic:** "Mitigating Institutional Amnesia" in healthcare analytics via Human-in-the-Loop Semantic Governance (HiL-SG).

**Three-paper series:** Paper 1 (framework, nearly complete) → Paper 2 (empirical validation, Synthea/GCP) → Paper 3 (FHIR/OMOP interoperability). GitHub issues tagged `paper-1`, `paper-2`, `paper-3`.

## Essential Commands

**Always use `uv run` to execute Python** — never bare `python` or `python3`. This ensures the correct venv and dependencies.

```bash
# Build paper (all formats)
./scripts/build_paper.sh --format all

# Quality checks (run before commits)
uv run ruff format . && uv run ruff check --fix .
uv run mypy scripts/ lit_review/
uv run pytest
uv run python scripts/validate_references.py --all
uv run python scripts/validate_jmir_compliance.py

# GitHub CLI with secrets (injects GH_TOKEN from OS keyring)
uv run scripts/secrets_run.py gh issue list --label "P0"
uv run scripts/secrets_run.py gh issue create --title "..."
```

## Branch Strategy

`main` ← `release/*` ← `develop` ← `contrib/stharrold` ← `feature/*`
- Direct commits allowed on `feature/*` and `contrib/*`
- `develop` and `main` require PRs

## Commit Convention

Conventional commits: `fix(paper):`, `feat(ci):`, `docs:`, `build:`
Include `Closes #<issue>` to auto-close GitHub issues.

## Writing Rules

- **No em-dashes (—)**. Use commas, colons, semicolons, or parentheses instead.
- Citations use pandoc-citeproc: `[@key]`, multiple: `[@wu2024; @himss2024]`
- BibTeX in `references.bib`, styled with `citation-style-ama.csl` (AMA 11th ed)
- Framework is **descriptive** (reveals interconnections), not **prescriptive** (recommends solutions)
- Conversational AI is a "Governance Forcing Function," not the standalone solution

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
- **Do not set `GITHUB_TOKEN` or `GH_TOKEN` globally in shell profiles** — use `secrets_run.py` instead
- `secrets.toml` uses `GH_TOKEN` (not `GITHUB_TOKEN`) — this is what `gh` CLI checks first
- After regenerating a GitHub fine-grained PAT, verify write access: `uv run scripts/secrets_run.py gh api --method PATCH repos/OWNER/REPO/issues/1 -f state=open`

## Architecture

- **Scripts (`scripts/`):** Python stdlib only, except `secrets_*.py` which use PEP 723 inline deps (`keyring`, `tomlkit`) auto-installed by `uv run`
- **Literature review (`lit_review/`):** Clean Architecture with external deps (pydantic, httpx, click, scikit-learn)
- **Figures:** Mermaid `.mmd` sources → PNG via container + Puppeteer
- **Container:** `Containerfile` with Python 3.12, Pandoc 3.2, TeXLive, Node.js

## Key Files

| File | Purpose |
|------|---------|
| `paper.md` | Main paper source (Markdown + pandoc-citeproc citations) |
| `references.bib` | BibTeX bibliography |
| `metadata.yaml` | Pandoc metadata for PDF generation |
| `GEMINI.md` | Comprehensive AI context guide (detailed reference) |
| `scripts/build_paper.sh` | Paper build pipeline |
| `scripts/validate_references.py` | Citation URL validation |
| `scripts/validate_jmir_compliance.py` | Journal compliance checks |
| `secrets.toml` | Secret names declaration (no values; committed to git) |
| `scripts/secrets_setup.py` | Interactive keyring setup for secrets |
| `scripts/secrets_run.py` | Injects secrets from keyring before running commands |
