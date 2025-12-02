---
type: claude-context
directory: .
purpose: Research paper on YuiQuery healthcare analytics - documentation-only repository
parent: null
sibling_readme: README.md
children:
  - .claude/CLAUDE.md
  - docs/CLAUDE.md
  - scripts/CLAUDE.md
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
uv sync                                    # Local
podman-compose build                       # Container (recommended)

# Quality checks (run before commits)
./validate_documentation.sh                # Documentation validation (6 tests)
python scripts/validate_references.py --all  # Reference validation + URL checks
uv run ruff format . && uv run ruff check --fix .  # Format + lint
uv run mypy scripts/                       # Type checking

# Full quality gates (before PRs)
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# Task management
gh issue list --label "P0"                 # Critical tasks
gh issue view <number>                     # Task details
```

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

### Zero Runtime Dependencies
Scripts in `scripts/` and `tools/` use **Python stdlib only**. No external packages.
```python
# Allowed: sys, os, subprocess, json, pathlib, datetime, re, typing
# NOT allowed: requests, click, etc.
```

### Validation System
`./validate_documentation.sh` runs 6 tests: file size (30KB limit), cross-references, duplication, command syntax, YAML structure, and reference validation (citations in paper.md).

### AI Config Sync
Pre-commit hooks sync `.claude/` → `.agents/` and `CLAUDE.md` → `AGENTS.md` for cross-tool compatibility.

### Workflow Skills
9 skills in `.claude/skills/` for major releases and complex git operations. **Don't use for daily edits.**

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

## Healthcare Domain Context

**Required knowledge:** ICD-10, CPT, SNOMED, RxNorm vocabularies; HIMSS AMAM stages; HL7/FHIR standards; HIPAA compliance.

**Academic standards:** PRISMA guidelines for systematic reviews; statistical reporting with p-values/CIs; evidence hierarchy prioritizing RCTs.
