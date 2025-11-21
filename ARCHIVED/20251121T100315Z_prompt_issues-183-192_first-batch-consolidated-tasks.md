---
title: "Claude Code Prompt: First Batch of Consolidated GitHub Issues"
created: "2025-11-21T10:03:15Z"
target_issues: "183-192"
issue_count: 10
repository: "stharrold/yuimedi-paper-20250901"
branch: "contrib/stharrold"
priority_mix: "P0 (3), P1 (4), P2 (3)"
estimated_effort: "8-12 hours"
context_source: "CLAUDE.md, TODO.md, README.md, pyproject.toml"
validation_required: true
---

# Comprehensive Prompt for Claude Code: First Batch GitHub Issues (#183-192)

**Target:** Complete 10 consolidated GitHub issues from the recent TODO migration
**Repository:** https://github.com/stharrold/yuimedi-paper-20250901
**Issue Tracker:** https://github.com/stharrold/yuimedi-paper-20250901/issues

## Context: What This Repository Is

You're working on a **healthcare research documentation repository** for YuiQuery, a conversational AI platform for healthcare analytics. This is **NOT a software application** - it's an academic research project documenting natural language to SQL in healthcare.

**Critical Understanding:**
- Primary deliverable: `paper.md` (comprehensive academic research paper with 111+ citations)
- "Development" = documentation writing, validation, and workflow automation
- All automation scripts use **Python stdlib only** (zero runtime dependencies)
- Current version: v1.2.0
- Active branch: `contrib/stharrold` (integration branch: `main`)

## Recent Project Evolution (Context for Your Work)

**November 21, 2025 - Major TODO Migration:**
- Migrated from local TODO files (TODO_FOR_AI.json) to GitHub Issues
- Consolidated 69 items → 36 unique issues (47.8% deduplication)
- Created issues #183-218 with comprehensive Claude Code context
- Deprecated bidirectional sync workflow
- GitHub Issues now single source of truth

**Repository State:**
- Branch: `contrib/stharrold` (clean, 3 commits ahead of origin)
- Recent commits:
  - abfeabd: Updated CLAUDE.md to reflect GitHub Issues migration
  - 285de29: Migrated TODO management to GitHub Issues
  - e6558aa: Streamlined CLAUDE.md for better AI context
  - f742c90: Integrated workflow automation system (9 skills)

## Your Mission: Complete Issues #183-192

Work through these 10 issues systematically. Each issue includes comprehensive context in its body. Follow the workflow below for each issue.

### Issue Batch Overview

**Priority Distribution:**
- **P0 (Critical - 3 issues):** #189, #193, #194, #195
- **P1 (High - 4 issues):** #185, #186, #187, #192
- **P2 (Medium - 3 issues):** #183, #184, #188

**Issue Titles:**
1. #183: Code Quality Review: GitHub Projects Integration
2. #184: Pull Request Review: GitHub Projects Integration
3. #185: Add Anthropic Teams Claude Code best practices to project planning docs
4. #186: Add Healthcare-Specific Risk Factors
5. #187: Cite Anthropic Code Modernization Playbook in paper.md
6. #188: Consider submission to healthcare informatics journals
7. #189: Create Backup Developer Documentation (P0 - CRITICAL, deadline Sept 6)
8. #190: Create GitHub Actions Workflow
9. #191: Create GitHub Milestones
10. #192: Create Methodology Validation Checklist

### Recommended Order

Work in priority order (P0 → P1 → P2):

**Phase 1 - Critical (P0):**
1. #189: Backup Developer Documentation (CRITICAL deadline)
2. (Note: #193-195 are outside this batch but are also P0)

**Phase 2 - High Priority (P1):**
3. #185: Anthropic Teams best practices
4. #187: Cite Code Modernization Playbook
5. #186: Healthcare-Specific Risk Factors
6. #192: Methodology Validation Checklist

**Phase 3 - Medium Priority (P2):**
7. #183: Code Quality Review
8. #184: Pull Request Review
9. #188: Journal submission consideration
10. #190: GitHub Actions Workflow
11. #191: GitHub Milestones

## Essential Commands & Workflow

### Initial Setup
```bash
# Verify environment
cd /path/to/yuimedi-paper-20250901
git status                           # Should show contrib/stharrold
uv run python --version              # Should be 3.9+
./validate_documentation.sh          # Verify tests pass

# Authenticate GitHub CLI (if needed)
gh auth status
gh auth login                        # If not authenticated
```

### Working on Each Issue

**1. Read the Issue**
```bash
gh issue view <number>               # Read full context
```

Each issue includes:
- Task description
- Context for Claude Code
- Expected deliverables
- Repository patterns
- Validation requirements

**2. Do the Work**
- Follow instructions in issue body
- Maintain academic citation format: `[A#]` for academic, `[I#]` for industry
- Preserve document structure
- Use UV for Python execution: `uv run python script.py`
- NO external dependencies in scripts (stdlib only)

**3. Validate Your Work**
```bash
./validate_documentation.sh          # Run all 5 validation tests
uv run ruff format .                 # Format Python
uv run ruff check --fix .            # Lint and auto-fix
uv run mypy scripts/                 # Type check (if scripts changed)
```

**4. Commit Your Changes**
```bash
git add <files>
git commit -m "type(scope): description

Resolves #<issue-number>

<details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Commit Types:** feat, fix, docs, style, refactor, test, chore

**5. Update the Issue**
```bash
gh issue comment <number> --body "✓ Completed

Changes made:
- <bullet list>

Validation: All tests pass
Commit: <hash>"

gh issue close <number> --comment "Completed successfully"
```

## Critical Repository Patterns

### Academic Citation Format
- **Academic sources:** `[A1]`, `[A2]`, etc. → References > Academic Sources
- **Industry sources:** `[I1]`, `[I2]`, etc. → References > Industry Sources
- Currently 111+ citations in paper.md
- Maintain consistent numbering

### Document Structure
- `paper.md` - Main research paper (comprehensive, 111+ citations)
- Academic format: abstract, intro, lit review, methods, results, discussion, conclusion
- Three-pillar framework: maturity, turnover, technical barriers
- Evidence-based: combine peer-reviewed research with real-world case studies

### File Naming
- Research docs: Descriptive names with `.md` extension
- Timestamps: `YYYYMMDDTHHMMSSZ_` prefix for historical files
- Project management: Uppercase names (`TODO.md`, `DECISION_LOG.json`)

### Directory README Pattern
Every major directory has README.md explaining contents:
- `src/README.md`, `docs/README.md`, `compliance/README.md`, etc.
- Ensures self-documenting structure

### Zero Runtime Dependencies
- All scripts (`scripts/`, `tools/`) use **Python stdlib only**
- Development tools (Ruff, MyPy) are optional via UV
- When adding scripts: Use `import sys, os, subprocess, json, pathlib` etc.
- NO external packages in automation code

## Validation Requirements

### Documentation Validation (5 Tests)
```bash
./validate_documentation.sh          # Orchestrator (runs all 5)

# Individual tests:
tools/validation/test_file_size.sh              # 30KB limit on modular docs
tools/validation/test_cross_references.sh       # Validate markdown links
tools/validation/test_content_duplication.sh    # Detect duplicates
tools/validation/test_command_syntax.sh         # Validate bash blocks
tools/validation/test_yaml_structure.sh         # Check JSON structure
```

**Run before ALL commits affecting documentation.**

### Code Quality (Python Scripts)
```bash
uv run ruff format .                 # Format (Black-compatible)
uv run ruff check --fix .            # Lint and auto-fix
uv run mypy scripts/                 # Type checking
```

## Healthcare Domain Requirements

When working on healthcare-related content:

**Medical Terminology:** ICD-10, CPT, SNOMED, RxNorm vocabularies
**Healthcare IT Standards:** HIMSS AMAM, HL7, FHIR
**Clinical Workflows:** Clinical decision-making processes
**Regulatory Context:** HIPAA, data governance, compliance

**Research Quality:**
- Systematic review methodology (PRISMA guidelines)
- Statistical reporting (confidence intervals, p-values, effect sizes)
- Evidence hierarchy (prioritize RCTs and systematic reviews)
- Quantitative validation (specific metrics with statistical significance)

## Issue-Specific Guidance

### #183-184: Code Quality & PR Reviews
- These are review tasks (not implementation)
- Read the issue body for specific code/PR to review
- Provide constructive feedback following project patterns
- Check for: stdlib-only, academic format, validation requirements

### #185: Anthropic Teams Best Practices
- Document URL provided in issue
- Integrate insights into project planning docs
- Focus on: codebase navigation, testing, debugging, prototyping, documentation
- Maintain academic tone

### #186: Healthcare-Specific Risk Factors
- Include HIMSS project management standards
- Reference healthcare IT project risks
- Update `project-management/risks/` directory
- Maintain consistent format with existing risk documentation

### #187: Cite Code Modernization Playbook
- Add citation to paper.md
- Strengthen discussion of technical barriers
- Healthcare/pharma legacy systems section most relevant
- Use citation format: `[I##]` for industry source

### #188: Journal Submission Consideration
- Research healthcare informatics journals
- Document submission targets in `docs/` or `project-management/`
- Include submission guidelines, timelines, requirements
- Reference TODO.md for context

### #189: Backup Developer Documentation (CRITICAL P0)
- Deadline: September 6 (URGENT if still pending)
- Create role requirements and RACI matrix
- Document in `project-management/roles/`
- Include budget reference ($15,000-20,000 range)
- Use Glassdoor salary data for validation

### #190: GitHub Actions Workflow
- Create `.github/workflows/` if not exists
- Setup automated project tracking
- Include: documentation validation, code quality checks
- Use existing validation scripts
- Ensure Python 3.9+ compatibility

### #191: GitHub Milestones
- Create milestones for project phases
- Reference `project-management.md` for timeline
- Include deadlines and deliverables
- Link to relevant issues

### #192: Methodology Validation Checklist
- Develop checklist to verify URLs, references, calculations
- Document in `project-management/` or `docs/`
- Include validation steps for academic citations
- Reference validation scripts

## Common Pitfalls to Avoid

1. **Don't add external dependencies** - Scripts must use Python stdlib only
2. **Don't skip validation** - Always run `./validate_documentation.sh`
3. **Don't modify citation numbering** - Preserve existing `[A#]` and `[I#]` sequences
4. **Don't use bare `python3`** - Always use `uv run python script.py`
5. **Don't create new files unnecessarily** - Prefer editing existing files
6. **Don't skip commit messages** - Follow format with issue number
7. **Don't forget to close issues** - Use `gh issue close <number>`

## Success Criteria

For each issue completed:
- ✅ All validation tests pass (`./validate_documentation.sh`)
- ✅ Code quality checks pass (if applicable)
- ✅ Academic citation format maintained
- ✅ Healthcare domain accuracy preserved
- ✅ Commit includes issue reference (`Resolves #<number>`)
- ✅ Issue updated with progress comment
- ✅ Issue closed with completion summary

## Helpful References

**In Repository:**
- `CLAUDE.md` - Complete project guide (read this first!)
- `TODO.md` - Task management documentation
- `README.md` - Project overview
- `project-management.md` - Executive summary
- `.claude/skills/` - 9 workflow automation skills (if needed for complex tasks)

**Commands:**
- `gh issue list` - View all open issues
- `gh issue view <number>` - Read issue details
- `./validate_documentation.sh` - Run all tests
- `uv run ruff format .` - Format code
- `git status` - Check working tree

## Issue Tracking

As you complete issues, track your progress:

```bash
# View remaining issues in batch
gh issue list --json number,title,state | jq '.[] | select(.number >= 183 and .number <= 192)'

# Check your progress
gh issue list --state closed --json number,closedAt | jq '.[] | select(.number >= 183 and .number <= 192)'
```

## Final Notes

**This is a documentation repository:**
- Focus on research quality and academic standards
- Maintain healthcare domain accuracy
- Preserve existing citation systems
- Follow systematic review methodology

**Work systematically:**
- One issue at a time
- Validate before committing
- Update issue with progress
- Close when complete

**Branch strategy:**
- Work on: `contrib/stharrold`
- Integrate to: `main` (via PR when batch complete)
- Tag releases: Semantic versioning (v1.0, v1.1, v1.2, etc.)

**You've got this!** Each issue includes comprehensive context in its body. Follow the workflow above, validate your work, and you'll complete this batch successfully.

---

**When you've completed all 10 issues (#183-192), create a summary:**

```bash
# Generate completion report
gh issue list --state closed --json number,title,closedAt \
  --jq '.[] | select(.number >= 183 and .number <= 192) | "✓ #\(.number): \(.title)"'

# Commit count for this batch
git log --oneline --grep="#183\|#184\|#185\|#186\|#187\|#188\|#189\|#190\|#191\|#192"

# Ready for next batch or PR to main
git log --oneline contrib/stharrold ^origin/contrib/stharrold
```

Good luck! 🚀
