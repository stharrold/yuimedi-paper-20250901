---
title: "Claude Code Prompt: Third Batch of Consolidated GitHub Issues"
created: "2025-11-23T17:18:40Z"
target_issues: "203-212"
issue_count: 10
repository: "stharrold/yuimedi-paper-20250901"
branch: "contrib/stharrold"
priority_mix: "P0 (1), P1 (2), P2 (7)"
estimated_effort: "8-12 hours"
context_source: "CLAUDE.md, TODO.md, README.md, project-management/"
validation_required: true
dependencies: "Issue #205 has legacy dependency marker"
previous_batches:
  - batch-1: "#183-192 (completed)"
  - batch-2: "#193-202 (completed)"
---

# Comprehensive Prompt for Claude Code: Third Batch GitHub Issues (#203-212)

**Target:** Complete 10 consolidated GitHub issues from batch-3
**Repository:** https://github.com/stharrold/yuimedi-paper-20250901
**Issue Tracker:** https://github.com/stharrold/yuimedi-paper-20250901/issues
**Current Version:** v1.5.0

## Context: What This Repository Is

You're working on a **healthcare research documentation repository** for YuiQuery, a conversational AI platform for healthcare analytics. This is **NOT a software application** - it's an academic research project documenting natural language to SQL in healthcare.

**Critical Understanding:**
- Primary deliverable: `paper.md` (comprehensive academic research paper with 111+ citations)
- "Development" = documentation writing, validation, and workflow automation
- All automation scripts use **Python stdlib only** (zero runtime dependencies)
- Current version: v1.5.0 (just released)
- Active branch: `contrib/stharrold` (integration branches: `develop` → `main`)

## Recent Project Evolution

**November 23, 2025 - Release v1.5.0:**
- Phase-based workflow commands (`/workflow/1_specify` → `/workflow/7_backmerge`)
- New orchestrator (`/workflow/all`) with auto-state detection
- PR review fixes for username handling and type annotations
- Full git-flow branch strategy: `main ← release/* ← develop ← contrib/stharrold ← feature/*`

**Repository State:**
- Branch: `contrib/stharrold` (clean, rebased on develop)
- Batch 1 (#183-192): Completed
- Batch 2 (#193-202): Completed
- Batch 3 (#203-212): **YOUR CURRENT FOCUS**
- Batch 4 (#213-218): Pending

## Your Mission: Complete Issues #203-212

Work through these 10 issues systematically. Each issue includes context in its body. Follow the workflow below for each issue.

### Issue Batch Overview

**Priority Distribution:**
- **P0 (Critical - 1 issue):** #212 - Update Publication Strategy with Portals
- **P1 (High - 2 issues):** #204, #205 - Infrastructure setup
- **P2 (Medium - 7 issues):** #203, #206-211 - Code quality and documentation fixes

**Issue Summary:**

| # | Title | Priority | Type |
|---|-------|----------|------|
| 203 | Review merged paper for citation consistency and academic formatting | P2 | Documentation |
| 204 | Setup Complete Directory Structure | P1 | Infrastructure |
| 205 | Setup Synthetic Data with Synthea | P1 | Data/Setup |
| 206 | Fix JSON shell variable expansion syntax | P2 | Code fix |
| 207 | Fix incorrect increase_factor calculation | P2 | Code fix |
| 208 | Document Synthea task status change | P2 | Documentation |
| 209 | Fix contradictory task count metadata | P2 | Data fix |
| 210 | Fix inconsistent task count metadata | P2 | Data fix |
| 211 | Fix duplicate if statements in validation | P2 | Code fix |
| 212 | Update Publication Strategy with Portals | P0 | Documentation |

### Recommended Work Order

**Phase 1 - Critical Documentation (P0):**
1. **#212**: Update Publication Strategy with Portals (P0 - do this first)

**Phase 2 - Infrastructure Setup (P1):**
2. **#204**: Setup Complete Directory Structure (foundation for other work)
3. **#205**: Setup Synthetic Data with Synthea (has dependency on directory structure)

**Phase 3 - Code Quality Fixes (P2):**
4. **#211**: Fix duplicate if statements in validation script
5. **#206**: Fix JSON shell variable expansion syntax
6. **#207**: Fix incorrect increase_factor calculation

**Phase 4 - Metadata & Documentation Cleanup (P2):**
7. **#209**: Fix contradictory task count metadata
8. **#210**: Fix inconsistent task count metadata
9. **#208**: Document Synthea task status change
10. **#203**: Review merged paper for citation consistency

## Essential Commands & Workflow

### Initial Setup
```bash
# Verify environment
cd /path/to/yuimedi-paper-20250901
git status                           # Should show contrib/stharrold
git pull origin contrib/stharrold    # Get latest changes
uv run python --version              # Should be 3.9+
./validate_documentation.sh          # Verify tests pass

# Authenticate GitHub CLI (if needed)
gh auth status
gh auth login                        # If not authenticated

# Check batch 3 issues
gh issue list --label "batch-3" --state open
```

### Working on Each Issue

**1. Read the Issue**
```bash
gh issue view <number>               # Read full context
```

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
git commit -m "$(cat <<'EOF'
type(scope): description

Resolves #<issue-number>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Commit Types:** feat, fix, docs, style, refactor, test, chore

**5. Update and Close the Issue**
```bash
gh issue comment <number> --body "$(cat <<'EOF'
✓ Completed

Changes made:
- <bullet list of changes>

Validation: All tests pass
Commit: <hash>
EOF
)"

gh issue close <number>
```

## Issue-Specific Guidance

### #212: Update Publication Strategy with Portals (P0 - CRITICAL)

**Priority:** P0-Critical - Complete this FIRST
**Type:** Documentation
**Original Task IDs:** gh-115, gh-128, gh-142

**Requirements:**
- Document validated submission portals for whitepapers
- Research and list appropriate venues for healthcare AI research publication
- Include portals for:
  - Academic journals (JAMIA, JMIR, BMC Medical Informatics)
  - Preprint servers (arXiv, medRxiv)
  - Industry publications (HIMSS, CHIME)
  - Conference proceedings (AMIA, HIMS)
- Document submission requirements for each portal
- Include deadlines, review processes, and open access options
- Create or update `docs/publication-strategy.md` or similar

**Deliverables:**
- Comprehensive publication portal documentation
- Submission timeline recommendations
- Budget considerations for publication fees

**Validation:**
- All listed portals are verified as accepting healthcare AI research
- URLs and submission links are current and working
- Document follows academic formatting standards

---

### #204: Setup Complete Directory Structure (P1)

**Priority:** P1-High
**Type:** Infrastructure/Setup
**Original Task IDs:** gh-119, gh-132, gh-146

**Requirements:**
- Create missing project directories for papers, source code, and data
- Follow the existing directory patterns in CLAUDE.md
- Standard directories to ensure exist:
  ```
  src/                    # Source code and algorithms
  docs/                   # Documentation and paper versions
  data/                   # Data files (gitignored for large files)
  config/                 # Configuration files
  tools/                  # Utility scripts
  scripts/                # Automation scripts
  project-management/     # PM artifacts
  compliance/             # IRB and HIPAA documentation
  images/                 # Figures and diagrams
  ```
- Each directory should have README.md explaining its purpose
- Use workflow-utilities pattern: `python .claude/skills/workflow-utilities/scripts/directory_structure.py <dir>`

**Validation:**
- All standard directories exist
- Each has appropriate README.md
- No breaking changes to existing structure

---

### #205: Setup Synthetic Data with Synthea (P1)

**Priority:** P1-High (has-dependencies)
**Type:** Data/Setup
**Original Task IDs:** gh-120, gh-133, gh-147
**Dependency:** `<!-- depends-on: impl-2 -->` (legacy - likely #204)

**Requirements:**
- Clone Synthea repository for synthetic patient generation
- Generate 100 synthetic patients as backup data source
- Document the setup process
- This is for **research backup data** - not production use

**Note:** Issue #208 mentions this task was marked 'not_needed' because data is available at `yuiquery.yuimedi.com/chats/v3/`.

**Decision needed:**
1. If synthetic data is still needed: Follow setup instructions
2. If not needed: Close issue with explanation referencing #208

**If proceeding with setup:**
```bash
# Clone Synthea (do NOT commit to this repo)
cd /tmp
git clone https://github.com/synthetichealth/synthea.git
cd synthea

# Generate patients (requires Java)
./run_synthea -p 100

# Document location and usage in docs/synthetic-data.md
```

**Validation:**
- Either: Synthea setup documented with generated data location
- Or: Issue closed with clear rationale

---

### #206: Fix JSON Shell Variable Expansion Syntax (P2)

**Priority:** P2-Medium
**Type:** Code fix
**Original Task ID:** gh-40

**Problem:**
JSON contains shell variable expansion syntax `${references.salary_data}` which will not work in JSON context.

**Requirements:**
- Find the JSON file containing `${references.salary_data}`
- Replace shell variable expansion with:
  - Literal URL, OR
  - Different templating approach (e.g., Python string formatting)
- Ensure JSON is valid after changes

**Search for the file:**
```bash
grep -r '\${references' . --include="*.json"
```

**Fix approach:**
Replace `${references.salary_data}` with the actual URL:
`https://www.glassdoor.com/Salaries/healthcare-data-analyst-salary-SRCH_KO0,23.htm`

**Validation:**
- JSON file is syntactically valid
- No shell variable expansion syntax remains
- `./validate_documentation.sh` passes

---

### #207: Fix Incorrect increase_factor Calculation (P2)

**Priority:** P2-Medium
**Type:** Code fix
**Original Task ID:** gh-41

**Problem:**
The `increase_factor` of 12.4 is mathematically incorrect:
- Calculation shown: $33,495 ÷ $2,700 = 12.4
- But: grand_total is $33,495, subtotal before contingency is $30,450
- The factor should be calculated against the appropriate base amount

**Requirements:**
- Find the file containing `increase_factor: 12.4`
- Verify the correct calculation:
  - If comparing to $2,700: $33,495 ÷ $2,700 = 12.41 (this seems like comparing to wrong base)
  - If comparing to original estimate: Calculate correctly
- Update to correct value (suggested: 11.28 per Copilot review)

**Search for the file:**
```bash
grep -r 'increase_factor' . --include="*.json" --include="*.yaml" --include="*.md"
```

**Validation:**
- Mathematical calculation is verifiable
- Document the calculation methodology
- Value is updated correctly

---

### #208: Document Synthea Task Status Change (P2)

**Priority:** P2-Medium
**Type:** Documentation
**Original Task ID:** gh-42

**Problem:**
The status change to 'not_needed' for the Synthea task should be documented with a reason comment explaining why this task is no longer required.

**Context:**
- The description mentions data is available at `yuiquery.yuimedi.com/chats/v3/`
- This relates to issue #205

**Requirements:**
- Find where Synthea task status was changed to 'not_needed'
- Add documentation explaining:
  - Why Synthea setup is no longer required
  - Where the alternative data source is located
  - Any implications for the research

**Note:** This may already be documented. Check TODO.md or archived files first.

**Validation:**
- Status change is clearly documented
- Alternative data source is referenced
- Related issue #205 has consistent information

---

### #209: Fix Contradictory Task Count Metadata (P2)

**Priority:** P2-Medium
**Type:** Data fix
**Original Task ID:** gh-43

**Problem:**
The status distribution shows 96 todo tasks, which contradicts the PR description claiming to reduce active issues to 20. This suggests the deduplication may not be fully reflected in the metadata counts.

**Requirements:**
- Find the metadata showing 96 todo tasks
- Verify the actual current task count
- Update metadata to reflect accurate counts after deduplication
- Cross-reference with GitHub Issues to verify:
  ```bash
  gh issue list --state open | wc -l
  gh issue list --state closed | wc -l
  ```

**Note:** This issue and #210 are related - may be addressing same underlying problem.

**Validation:**
- Metadata accurately reflects current task counts
- Numbers are consistent across all documentation

---

### #210: Fix Inconsistent Task Count Metadata (P2)

**Priority:** P2-Medium
**Type:** Data fix
**Original Task ID:** gh-44

**Problem:**
Task counts appear inconsistent with the PR's stated goal of reducing issues from 92 to 20. Metadata shows an increase rather than the expected decrease after deduplication.

**Requirements:**
- Similar to #209 - these may be duplicates
- Verify and fix task count metadata
- Ensure consistency between:
  - GitHub Issues (actual count)
  - TODO.md metadata
  - Any other task tracking files

**Decision:** If #209 and #210 are duplicates, close one as duplicate.

**Validation:**
- Task counts are accurate and consistent
- Documentation reflects actual GitHub Issues state

---

### #211: Fix Duplicate If Statements in Validation Script (P2)

**Priority:** P2-Medium
**Type:** Code fix
**Original Task ID:** gh-45

**Problem:**
Duplicate if statements checking different repository names. The second condition will never be reached because both conditions are checking the same variable in sequence without proper logic flow.

**Requirements:**
- Find the validation script with duplicate if statements
- Identify the logic error
- Fix the conditional flow (likely needs `elif` or different structure)

**Search for the issue:**
```bash
grep -r "EXPECTED_REPO_NAME\|repo.*name" scripts/ tools/ --include="*.py" --include="*.sh"
```

**Common patterns to fix:**
```python
# WRONG:
if repo_name == "repo1":
    do_something()
if repo_name == "repo2":  # This always executes after first if
    do_something_else()

# RIGHT:
if repo_name == "repo1":
    do_something()
elif repo_name == "repo2":
    do_something_else()
```

**Validation:**
- Logic flow is correct
- Both conditions can be reached when appropriate
- Script functions correctly
- All tests pass

---

### #203: Review Merged Paper for Citation Consistency (P2)

**Priority:** P2-Medium
**Type:** Documentation/QA
**Original Task IDs:** gh-2, gh-5

**Requirements:**
- Review `paper.md` for citation consistency
- Check academic formatting throughout
- Verify:
  - All `[A#]` citations have corresponding entries in References > Academic Sources
  - All `[I#]` citations have corresponding entries in References > Industry Sources
  - Citation numbers are sequential and not duplicated
  - Citation format is consistent
  - Academic tone is maintained throughout
  - Formatting follows target journal guidelines

**Checklist:**
- [ ] All academic citations (`[A1]` through `[A##]`) are valid
- [ ] All industry citations (`[I1]` through `[I##]`) are valid
- [ ] No orphaned citations (referenced but not in bibliography)
- [ ] No orphaned references (in bibliography but not cited)
- [ ] Consistent formatting (italics, DOIs, URLs)
- [ ] Author names properly formatted
- [ ] Publication dates included
- [ ] DOIs/URLs are working

**Validation:**
- Run cross-reference check:
  ```bash
  ./tools/validation/test_cross_references.sh
  ```
- Manual spot-check of 10-15 citations
- Document any issues found and fixed

## Common Pitfalls to Avoid

1. **Don't add external dependencies** - Scripts must use Python stdlib only
2. **Don't skip validation** - Always run `./validate_documentation.sh`
3. **Don't modify citation numbering carelessly** - Renumbering citations cascades throughout the paper
4. **Don't use bare `python3`** - Always use `uv run python script.py`
5. **Don't create unnecessary files** - Prefer editing existing files
6. **Don't forget to close issues** - Use `gh issue close <number>`
7. **Don't duplicate effort on #209 and #210** - Check if they're the same issue
8. **Don't setup Synthea if not needed** - Check #208 status first

## Dependency Notes

### Issue #205 Dependency
Issue #205 has dependency marker `<!-- depends-on: impl-2 -->` which refers to a legacy task ID.

**Resolution:**
1. The dependency is likely #204 (Setup Complete Directory Structure)
2. Complete #204 before #205
3. Check if #205 is even needed per #208 documentation

### Issues #209 and #210 Relationship
These appear to address the same underlying metadata inconsistency issue.

**Resolution:**
1. Review both issues
2. If they're duplicates, close one as duplicate of the other
3. Fix the metadata issue once

## Success Criteria

For each issue completed:
- [ ] All validation tests pass (`./validate_documentation.sh`)
- [ ] Code quality checks pass (if applicable)
- [ ] Academic citation format maintained
- [ ] Commit includes issue reference (`Resolves #<number>`)
- [ ] Issue updated with completion comment
- [ ] Issue closed

## Helpful References

**In Repository:**
- `CLAUDE.md` - Complete project guide
- `TODO.md` - Task management documentation
- `README.md` - Project overview
- `paper.md` - Main research paper
- `project-management/` - PM artifacts
- `.claude/skills/` - 9 workflow automation skills

**Commands Quick Reference:**
```bash
# View batch 3 issues
gh issue list --label "batch-3" --state open

# Read specific issue
gh issue view <number>

# Run validation
./validate_documentation.sh

# Format and lint
uv run ruff format . && uv run ruff check --fix .

# Search for patterns
grep -r "pattern" . --include="*.py" --include="*.json"

# Check git status
git status
git log --oneline -5
```

## Progress Tracking

As you complete issues, track progress:

```bash
# View remaining batch 3 issues
gh issue list --label "batch-3" --state open

# View completed batch 3 issues
gh issue list --label "batch-3" --state closed

# Count remaining
gh issue list --label "batch-3" --state open | wc -l
```

## Completion Summary

When all issues are complete:

```bash
# Generate completion report
gh issue list --label "batch-3" --state closed \
  --json number,title --jq '.[] | "✓ #\(.number): \(.title)"'

# Verify all batch 3 issues are closed
gh issue list --label "batch-3" --state open
# Should return empty

# Push changes
git push origin contrib/stharrold

# Consider creating PR to develop if significant changes
gh pr create --base develop --head contrib/stharrold \
  --title "Complete batch-3 issues (#203-212)" \
  --body "Resolves batch-3 consolidated issues..."
```

## Final Notes

**This batch is primarily code quality and documentation fixes:**
- 1 P0 issue (publication strategy) - complete first
- 2 P1 issues (infrastructure) - foundational work
- 7 P2 issues (fixes and cleanup) - quick wins

**Key themes:**
- Fix validation script logic errors
- Correct metadata inconsistencies
- Update publication documentation
- Clean up after TODO migration

**Work strategy:**
1. Start with P0 (#212) - critical documentation
2. Do P1 infrastructure (#204, #205) - enables other work
3. Quick code fixes (#211, #206, #207) - low-hanging fruit
4. Metadata cleanup (#209, #210, #208) - may have overlap
5. Paper review (#203) - comprehensive QA pass

**Estimated time:** 8-12 hours total

Good luck! This batch is more focused on cleanup and fixes than the previous risk management cluster. Most issues should be straightforward once you locate the relevant files.

---

**After completing all issues, the next batch is #213-218 (batch-4) which includes:**
- #213: Update Risk Register with Numerical Scores (P1-High)
- #214-218: Various P2 nitpick fixes

Consider starting batch-4 prompt creation after completing this batch.
