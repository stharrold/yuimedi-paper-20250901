---
title: "Claude Code Prompt: Second Batch of Consolidated GitHub Issues"
created: "2025-11-21T12:14:32Z"
target_issues: "193-202"
issue_count: 10
repository: "stharrold/yuimedi-paper-20250901"
branch: "contrib/stharrold"
priority_mix: "P0 (3), P2 (7)"
estimated_effort: "10-14 hours"
context_source: "CLAUDE.md, TODO.md, README.md, project-management/"
validation_required: true
dependencies: "Issue #193 has legacy dependency marker"
---

# Comprehensive Prompt for Claude Code: Second Batch GitHub Issues (#193-202)

**Target:** Complete 10 consolidated GitHub issues from the recent TODO migration
**Repository:** https://github.com/stharrold/yuimedi-paper-20250901
**Issue Tracker:** https://github.com/stharrold/yuimedi-paper-20250901/issues

## Context: What This Repository Is

You're working on a **healthcare research documentation repository** for YuiQuery, a conversational AI platform for healthcare analytics. This is **NOT a software application** - it's an academic research project documenting natural language to SQL in healthcare.

**Critical Understanding:**
- Primary deliverable: `paper.md` (comprehensive academic research paper with 111+ citations)
- "Development" = documentation writing, validation, and workflow automation
- All automation scripts use **Python stdlib only** (zero runtime dependencies)
- Current version: v1.3.0
- Active branch: `contrib/stharrold` (integration branch: `main`)

## Recent Project Evolution (Context for Your Work)

**November 21, 2025 - GitHub Issues Organization:**
- All 36 consolidated issues (#183-218) now have labels, milestones, and priority tracking
- Batch 1 (#183-192): May be in progress or completed
- Batch 2 (#193-202): **YOUR CURRENT FOCUS**
- Created comprehensive label system: P0-Critical, P1-High, P2-Medium, batch-X, has-dependencies
- Milestones: "v1.3.0 Issues - Batch 1" through "Batch 4"

**Repository State:**
- Branch: `contrib/stharrold` (check current status with `git status`)
- Recent major work: GitHub Issues migration, workflow system integration, v1.3.0 release
- Documentation repository with academic paper, project management artifacts, automation scripts

## Your Mission: Complete Issues #193-202

Work through these 10 issues systematically. Each issue includes comprehensive context in its body. Follow the workflow below for each issue.

### Issue Batch Overview

**Priority Distribution:**
- **P0 (Critical - 3 issues):** #193, #194, #195 - **RISK MANAGEMENT CLUSTER**
- **P2 (Medium - 7 issues):** #196-202

**Issue Titles:**
1. #193: Create Risk Scoring Matrix (P0, has-dependencies)
2. #194: Document Probability Calculations (P0)
3. #195: Document Risk Assessment Methodology (P0)
4. #196: Document YuiQuery Healthcare Data Integration Architecture with RAG and Schema Mapping References (P2)
5. #197: Generate final PDF/HTML versions of research paper (P2)
6. #198: Generate final PDF/HTML versions of research paper using pandoc (P2)
7. #199: Implement Query Classification and Data Catalog Generation Using Anthropic Classification Methodology (P2)
8. #200: Clean up orphaned code in validation script (P2)
9. #201: Merge YuiQuery AI Teammate Benchmarking Report into Main Paper (P2)
10. #202: Reference Issues in YuiQuery Research Paper - Validated Observations (P2)

### Recommended Order

**IMPORTANT:** This batch has a **risk management cluster** (3 P0 issues) that should be worked together.

**Phase 1 - Risk Management Cluster (P0 - CRITICAL):**
1. #195: Document Risk Assessment Methodology (foundation)
2. #194: Document Probability Calculations (builds on #195)
3. #193: Create Risk Scoring Matrix (depends on #194, #195)

**Phase 2 - Documentation & Quality (P2):**
4. #196: Document YuiQuery Healthcare Data Integration Architecture
5. #201: Merge AI Teammate Benchmarking Report
6. #202: Validate and fix reference issues in paper
7. #200: Clean up orphaned code

**Phase 3 - Publication & Implementation (P2):**
8. #197: Generate PDF/HTML versions (may be duplicate of #198)
9. #198: Generate PDF/HTML using pandoc (check if duplicate)
10. #199: Implement Query Classification and Data Catalog Generation

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

# Check batch 2 milestone
gh issue list --milestone "v1.3.0 Issues - Batch 2"
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
- Priority and dependency information

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

### Project Management Structure
- `project-management/` - Detailed PM artifacts
  - `risks/` - Risk register, scoring matrices, assessment methodology
  - `budget/` - Budget estimates and breakdowns
  - `roles/` - RACI matrices, role definitions
  - `quality/` - Quality gates and validation checklists
- `project-management.md` - Executive summary

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

## Healthcare & Academic Requirements

### Risk Management Standards (Critical for P0 Issues)
- **PMI PMBOK Guide:** Project Management Body of Knowledge - risk management framework
- **ISO 31000:2018:** Risk management - guidelines and principles
- **HIMSS Project Management Standards:** Healthcare IT-specific risk factors
- **Probability-Impact Matrix:** 5x5 matrix with numerical scoring (1-25 scale)
- **Statistical Validation:** Include confidence intervals, calculation methodology

### Healthcare Domain Context
**Medical Terminology:** ICD-10, CPT, SNOMED, RxNorm vocabularies
**Healthcare IT Standards:** HIMSS AMAM, HL7, FHIR
**Clinical Workflows:** Clinical decision-making processes
**Regulatory Context:** HIPAA, data governance, compliance

### Research Quality Standards
- Systematic review methodology (PRISMA guidelines)
- Statistical reporting (confidence intervals, p-values, effect sizes)
- Evidence hierarchy (prioritize RCTs and systematic reviews)
- Quantitative validation (specific metrics with statistical significance)

## Issue-Specific Guidance

### #193: Create Risk Scoring Matrix (P0, has-dependencies)
**CRITICAL:** This issue has a dependency marker `<!-- depends-on: risk-1 -->` which refers to an old task ID from before the GitHub migration. Check if this dependency is actually #194 or #195.

**Requirements:**
- Develop 5x5 probability-impact matrix
- Numerical scoring for all identified risks (1-25 scale)
- Map probability levels: Very Low (1), Low (2), Medium (3), High (4), Very High (5)
- Map impact levels: Negligible (1), Minor (2), Moderate (3), Major (4), Critical (5)
- Score = Probability × Impact
- Document in `project-management/risks/risk_scoring_matrix.md`
- Include scoring examples for healthcare IT projects
- Reference PMI PMBOK and ISO 31000 standards

**Validation:**
- All existing risks in risk register can be scored using this matrix
- Methodology is cited with authoritative sources
- Consistent with healthcare IT project risk frameworks

### #194: Document Probability Calculations (P0)
**Foundation for #193** - Complete this before the risk scoring matrix.

**Requirements:**
- Create comprehensive documentation for success probability calculation methodology
- Include verified references to:
  - PMI PMBOK Guide (project management framework)
  - ISO 31000:2018 (risk management standards)
  - HIMSS project management guidelines (healthcare IT specific)
- Document calculation formulas with statistical foundations
- Include confidence intervals and uncertainty quantification
- Provide worked examples for healthcare IT projects
- Document in `project-management/risks/probability_methodology.md`

**Key formulas to document:**
- Probability estimation: Historical data, expert judgment, Monte Carlo
- Confidence intervals: Statistical methods for uncertainty
- Risk scoring: Probability × Impact with justification

**Validation:**
- All citations are to authoritative sources (no blog posts)
- Methodology is reproducible and clearly documented
- Examples demonstrate healthcare relevance

### #195: Document Risk Assessment Methodology (P0)
**Foundation for entire risk management cluster** - Complete this FIRST.

**Requirements:**
- Create comprehensive risk assessment methodology documentation
- Cover complete risk management lifecycle:
  1. Risk identification (brainstorming, checklists, interviews)
  2. Risk analysis (qualitative and quantitative)
  3. Risk evaluation (probability-impact assessment)
  4. Risk treatment (avoid, mitigate, transfer, accept)
  5. Risk monitoring (ongoing tracking and review)
- Reference authoritative standards:
  - PMI PMBOK Guide (6th or 7th edition)
  - ISO 31000:2018
  - HIMSS healthcare IT project management
- Healthcare-specific considerations:
  - HIPAA compliance risks
  - Clinical workflow disruption
  - Data quality and interoperability
  - Regulatory approval delays
- Document in `project-management/risks/assessment_methodology.md`

**Validation:**
- Methodology aligns with PMI/ISO standards
- Healthcare-specific risks are thoroughly addressed
- Examples from healthcare IT implementations included

### #196: Document YuiQuery Healthcare Data Integration Architecture
**Complex documentation task** - Requires understanding of RAG and schema mapping.

**Requirements:**
- Document YuiQuery's data integration architecture
- Include Retrieval-Augmented Generation (RAG) approach
- Explain schema mapping methodology (ICD-10, CPT, SNOMED, RxNorm)
- Reference relevant sections of paper.md
- Create architectural diagrams (consider using Mermaid diagrams in markdown)
- Document in `docs/architecture/` or integrate into paper.md
- Cite academic sources on RAG and schema mapping

**Key topics:**
- How YuiQuery handles healthcare vocabulary mappings
- RAG implementation for context retrieval
- Schema harmonization across vocabularies
- Data quality and validation

### #197 & #198: Generate PDF/HTML Versions
**NOTE:** These may be duplicate issues - check both before starting.

**Requirements:**
- Generate professional PDF from paper.md using Pandoc
- Generate HTML version for web sharing
- Use Eisvogel template for PDF (if available)
- Ensure citations render correctly
- Validate that all images and diagrams are included
- Test with: `pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.pdf`

**Advanced PDF (if Eisvogel template available):**
```bash
pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.pdf \
  --template=eisvogel \
  --pdf-engine=xelatex \
  --listings \
  --toc \
  --number-sections
```

**HTML generation:**
```bash
pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.html \
  --standalone \
  --toc \
  --self-contained
```

**If these are duplicates:** Close one as duplicate, complete the other.

### #199: Implement Query Classification and Data Catalog Generation
**Implementation task** - Requires coding work.

**Requirements:**
- Implement query classification using Anthropic's classification methodology
- Generate data catalog for healthcare analytics queries
- Use Python stdlib only (no external dependencies)
- Create script in `scripts/` or `src/`
- Include comprehensive docstrings and type hints
- Add tests if applicable
- Document methodology in code comments

**Anthropic Classification Approach:**
- Few-shot prompting with healthcare query examples
- Classification categories: descriptive, diagnostic, predictive, prescriptive
- Catalog structure: query patterns, complexity levels, data requirements

**Validation:**
- Code passes `uv run ruff check`
- Type checking passes `uv run mypy`
- Functionality tested with example queries

### #200: Clean Up Orphaned Code
**Code quality issue** - Quick fix.

**Problem:** Line 56 in validation script is orphaned hardcoded check, line 57 correctly uses EXPECTED_REPO_NAME variable.

**Requirements:**
- Identify the specific validation script
- Remove line 56 (orphaned code)
- Verify line 57 is correct
- Test validation script after change
- Commit with clear explanation

**Validation:**
- Script still functions correctly
- No hardcoded values remain
- All tests pass

### #201: Merge AI Teammate Benchmarking Report
**Documentation integration task**

**Requirements:**
- Locate YuiQuery AI Teammate Benchmarking Report
- Review content for quality and relevance
- Integrate key findings into main paper.md
- Maintain academic citation format
- Ensure no duplication with existing content
- Preserve three-pillar framework structure

**Integration points:**
- Results section (empirical validation)
- Case studies (practical applications)
- Discussion (implications for healthcare)

**Validation:**
- No content duplication
- Citations properly formatted
- Paper structure maintained
- Academic tone preserved

### #202: Validate and Fix Reference Issues
**Quality assurance task**

**Requirements:**
- Review all references in paper.md
- Validate that all `[A#]` and `[I#]` citations exist in References section
- Check for broken or missing citations
- Verify URLs are accessible (for industry sources)
- Ensure DOI links work (for academic sources)
- Fix any inconsistencies in citation format
- Document observations and fixes

**Common issues to check:**
- Missing citations in References section
- Duplicate citation numbers
- Broken URLs or DOIs
- Inconsistent formatting

**Validation:**
- All citations resolve correctly
- No orphaned references
- No duplicate citations
- Consistent format throughout

## Dependency Notes

### Issue #193 Dependency
Issue #193 has a dependency marker `<!-- depends-on: risk-1 -->` which refers to an OLD task ID from before GitHub migration.

**Resolution approach:**
1. Check if "risk-1" was #194 or #195
2. Complete #194 and #195 BEFORE #193
3. Update #193 issue to clarify actual dependency
4. Remove old dependency marker, add GitHub issue reference if needed

**Work order for risk cluster:**
1. #195 (methodology - foundation)
2. #194 (probability calculations - builds on methodology)
3. #193 (scoring matrix - uses methodology and calculations)

## Common Pitfalls to Avoid

1. **Don't add external dependencies** - Scripts must use Python stdlib only
2. **Don't skip validation** - Always run `./validate_documentation.sh`
3. **Don't modify citation numbering** - Preserve existing `[A#]` and `[I#]` sequences
4. **Don't use bare `python3`** - Always use `uv run python script.py`
5. **Don't create new files unnecessarily** - Prefer editing existing files
6. **Don't skip commit messages** - Follow format with issue number
7. **Don't forget to close issues** - Use `gh issue close <number>`
8. **Don't work on #193 before #194 and #195** - Follow dependency order
9. **Don't duplicate #197 and #198** - Check if they're the same task

## Success Criteria

For each issue completed:
- ✅ All validation tests pass (`./validate_documentation.sh`)
- ✅ Code quality checks pass (if applicable)
- ✅ Academic citation format maintained
- ✅ Healthcare domain accuracy preserved
- ✅ Risk management standards followed (for P0 issues)
- ✅ Commit includes issue reference (`Resolves #<number>`)
- ✅ Issue updated with progress comment
- ✅ Issue closed with completion summary

## Helpful References

**In Repository:**
- `CLAUDE.md` - Complete project guide (read this first!)
- `TODO.md` - Task management documentation
- `README.md` - Project overview
- `project-management.md` - Executive summary
- `project-management/risks/` - Risk management artifacts (create for P0 issues)
- `.claude/skills/` - 9 workflow automation skills (if needed)

**External Standards:**
- PMI PMBOK Guide: https://www.pmi.org/pmbok-guide-standards
- ISO 31000:2018: https://www.iso.org/iso-31000-risk-management.html
- HIMSS: https://www.himss.org/resources/project-management

**Commands:**
- `gh issue list --milestone "v1.3.0 Issues - Batch 2"` - View batch issues
- `gh issue view <number>` - Read issue details
- `./validate_documentation.sh` - Run all tests
- `uv run ruff format .` - Format code
- `git status` - Check working tree

## Issue Tracking

As you complete issues, track your progress:

```bash
# View remaining issues in batch 2
gh issue list --milestone "v1.3.0 Issues - Batch 2" --state open

# Check your progress
gh issue list --milestone "v1.3.0 Issues - Batch 2" --state closed

# View by priority
gh issue list --label "P0-Critical" --milestone "v1.3.0 Issues - Batch 2"
gh issue list --label "P2-Medium" --milestone "v1.3.0 Issues - Batch 2"

# Check dependencies
gh issue view 193  # Should see dependency note in comments
```

## Final Notes

**This batch focuses on risk management:**
- 3 P0 issues form a coherent risk management cluster
- Complete in order: #195 → #194 → #193
- Follow PMI PMBOK and ISO 31000 standards
- Healthcare-specific risk factors are critical

**Documentation quality is paramount:**
- Academic citations must be authoritative
- Methodology must be reproducible
- Healthcare domain accuracy is non-negotiable

**Work systematically:**
- P0 risk cluster first (foundation for project)
- Documentation and quality tasks second
- Publication and implementation tasks last
- Validate before committing
- Update issues with progress
- Close when complete

**Branch strategy:**
- Work on: `contrib/stharrold`
- Integrate to: `main` (via PR when batch complete)
- Tag releases: Semantic versioning (v1.3.0 current)

**Potential duplicates:**
- Issues #197 and #198 may be duplicates (both about PDF/HTML generation)
- Check both, close one as duplicate if confirmed

**You've got this!** The risk management cluster (P0 issues) is the most critical work in this batch. Complete those first with rigorous methodology and authoritative citations, then tackle the remaining documentation and quality tasks.

---

**When you've completed all 10 issues (#193-202), create a summary:**

```bash
# Generate completion report
gh issue list --milestone "v1.3.0 Issues - Batch 2" --state closed \
  --json number,title,closedAt --jq '.[] | "✓ #\(.number): \(.title)"'

# Commit count for this batch
git log --oneline --grep="#193\|#194\|#195\|#196\|#197\|#198\|#199\|#200\|#201\|#202"

# Check if ready for PR to main
git log --oneline contrib/stharrold ^origin/contrib/stharrold
```

Good luck! Focus on the risk management foundation - it's critical for the project's credibility. 🎯
