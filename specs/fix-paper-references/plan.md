# Implementation Plan: Fix Paper References

**Type:** feature
**Slug:** fix-paper-references
**Date:** 2025-12-11
**GitHub Issue:** #261

## Overview

Fix paper.md references: remove unused references, fix broken URLs, verify claims against real academic literature, and replace any hallucinated references with verified peer-reviewed sources.

**Key tools:** `academic-review` CLI, `validate_references.py`, manual literature verification

## Task Breakdown

### Phase 1: Assessment

#### Task T001: Run reference validation baseline

**Priority:** High

**Files:**
- `paper.md`
- `scripts/validate_references.py`

**Description:**
Run the reference validation script to establish a baseline of issues to fix.

**Steps:**
1. Run `python scripts/validate_references.py --all`
2. Document the count of unused references
3. Document the count of broken URLs
4. Create a tracking list of all issues

**Acceptance Criteria:**
- [ ] Baseline report generated
- [ ] Issue counts documented (29 unused, 23 broken URLs per issue #261)

**Verification:**
```bash
python scripts/validate_references.py --all 2>&1 | tee validation_baseline.txt
```

**Dependencies:** None

---

#### Task T002: Extract and categorize claims from paper.md

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Extract all claims from paper.md that require citations, categorize them by the three pillars.

**Steps:**
1. Read paper.md and identify all factual claims
2. Categorize claims by pillar:
   - Pillar 1: Analytics maturity (HIMSS AMAM stages, healthcare analytics adoption)
   - Pillar 2: Workforce turnover (institutional knowledge loss, training costs)
   - Pillar 3: Technical barriers (NL2SQL challenges, schema complexity)
3. Note which claims have citations and which don't
4. Flag claims with potentially fabricated references

**Acceptance Criteria:**
- [ ] All claims extracted and categorized
- [ ] Claims mapped to three pillars
- [ ] Uncited claims identified

**Verification:**
Manual review - claims documented in a structured format

**Dependencies:** T001

---

### Phase 2: Literature Search

#### Task T003: Search academic databases for Pillar 1 (Analytics Maturity)

**Priority:** High

**Files:**
- Literature review artifacts (to be created)

**Description:**
Use academic-review CLI to search for papers supporting analytics maturity claims.

**Steps:**
1. Initialize a literature review: `uv run academic-review init pillar1-analytics`
2. Define search queries covering HIMSS AMAM, healthcare analytics adoption, BI maturity
3. Execute search: `uv run academic-review search pillar1-analytics`
4. Review results and assess relevance

**Acceptance Criteria:**
- [ ] Search queries executed across Crossref, PubMed, ArXiv
- [ ] Results deduplicated
- [ ] Relevant papers identified for analytics maturity claims

**Verification:**
```bash
uv run academic-review status pillar1-analytics
```

**Dependencies:** T002

---

#### Task T004: Search academic databases for Pillar 2 (Workforce Turnover)

**Priority:** High

**Files:**
- Literature review artifacts

**Description:**
Search for papers supporting workforce turnover and institutional knowledge claims.

**Steps:**
1. Initialize review: `uv run academic-review init pillar2-workforce`
2. Define search queries: healthcare turnover, nurse retention, institutional memory, training costs
3. Execute search and review results

**Acceptance Criteria:**
- [ ] Workforce-related papers found
- [ ] Turnover statistics verified against peer-reviewed sources

**Verification:**
```bash
uv run academic-review status pillar2-workforce
```

**Dependencies:** T002

---

#### Task T005: Search academic databases for Pillar 3 (Technical Barriers)

**Priority:** High

**Files:**
- Literature review artifacts

**Description:**
Search for papers on NL2SQL challenges, text-to-SQL benchmarks, healthcare data complexity.

**Steps:**
1. Initialize review: `uv run academic-review init pillar3-technical`
2. Define search queries: NL2SQL, text-to-SQL, Spider benchmark, healthcare schemas
3. Execute search and review results

**Acceptance Criteria:**
- [ ] NL2SQL benchmark papers found (Spider, BIRD, etc.)
- [ ] Healthcare-specific SQL challenges documented

**Verification:**
```bash
uv run academic-review status pillar3-technical
```

**Dependencies:** T002

---

### Phase 3: Verification and Replacement

#### Task T006: Verify existing references against claims

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Check each existing reference to verify it actually supports the claim it's cited for.

**Steps:**
1. For each citation in paper.md, verify the reference exists
2. Check if the reference content actually supports the claim
3. Flag references that don't support claims (potential hallucinations)
4. Flag references that are inaccessible (403/404 URLs)

**Acceptance Criteria:**
- [ ] Each reference verified against its claim
- [ ] Hallucinated references flagged
- [ ] Inaccessible references flagged

**Verification:**
Manual review - verification status documented per reference

**Dependencies:** T003, T004, T005

---

#### Task T007: Replace hallucinated/broken references

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Replace fabricated or broken references with verified peer-reviewed sources from the literature search.

**Steps:**
1. For each flagged reference, find a verified replacement from search results
2. Update paper.md with correct reference details (authors, title, journal, year, DOI)
3. Ensure replacement actually supports the claim
4. Update citation format to [A*] for academic, [I*] for industry

**Acceptance Criteria:**
- [ ] All hallucinated references replaced
- [ ] All broken URLs fixed or replaced with DOI alternatives
- [ ] Citation format consistent

**Verification:**
```bash
python scripts/validate_references.py --all
```

**Dependencies:** T006

---

#### Task T008: Remove unused references

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Remove references that are defined but never cited in the paper.

**Steps:**
1. Run validation to get list of unused references
2. Remove unused reference definitions from paper.md
3. Verify no orphaned citations remain

**Acceptance Criteria:**
- [ ] All unused references removed
- [ ] No orphaned citations
- [ ] Reference numbering consistent

**Verification:**
```bash
python scripts/validate_references.py --all
# Should report 0 unused references
```

**Dependencies:** T007

---

### Phase 4: Export and Validation

#### Task T009: Export literature review artifacts

**Priority:** Medium

**Files:**
- `docs/references.bib` (to be created)
- `docs/literature_synthesis.md` (to be created)

**Description:**
Export BibTeX and synthesis report documenting the reference verification methodology.

**Steps:**
1. Export BibTeX: `uv run academic-review export --format bibtex`
2. Generate synthesis report documenting methodology
3. Store artifacts in docs/ directory

**Acceptance Criteria:**
- [ ] BibTeX file generated with all verified references
- [ ] Synthesis report documents verification methodology

**Verification:**
```bash
ls docs/references.bib docs/literature_synthesis.md
```

**Dependencies:** T007, T008

---

#### Task T010: Final validation and quality gates

**Priority:** High

**Files:**
- `paper.md`
- All validation scripts

**Description:**
Run all validation checks to ensure paper.md passes quality gates.

**Steps:**
1. Run documentation validation: `./validate_documentation.sh`
2. Run reference validation: `python scripts/validate_references.py --all`
3. Run linting: `uv run ruff format . && uv run ruff check --fix .`
4. Run full quality gates: `python .claude/skills/quality-enforcer/scripts/run_quality_gates.py`

**Acceptance Criteria:**
- [ ] Documentation validation passes (6 tests)
- [ ] Reference validation passes with 0 critical issues
- [ ] All URLs accessible or have DOI alternatives
- [ ] No hallucinated references remain

**Verification:**
```bash
./validate_documentation.sh
python scripts/validate_references.py --all
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

**Dependencies:** T008, T009

---

## Task Summary

| Task | Description | Priority | Dependencies |
|------|-------------|----------|--------------|
| T001 | Run reference validation baseline | High | None |
| T002 | Extract and categorize claims | High | T001 |
| T003 | Search for Pillar 1 papers | High | T002 |
| T004 | Search for Pillar 2 papers | High | T002 |
| T005 | Search for Pillar 3 papers | High | T002 |
| T006 | Verify existing references | High | T003, T004, T005 |
| T007 | Replace hallucinated references | High | T006 |
| T008 | Remove unused references | High | T007 |
| T009 | Export literature artifacts | Medium | T007, T008 |
| T010 | Final validation | High | T008, T009 |

## Task Dependencies Graph

```
T001 ─> T002 ─┬─> T003 ─┐
              ├─> T004 ─┼─> T006 ─> T007 ─> T008 ─┬─> T009 ─> T010
              └─> T005 ─┘                         └─────────────┘
```

## Parallel Work Opportunities

- **[P] T003, T004, T005** can run in parallel (independent literature searches)
- T009 can start after T007 while T008 is in progress

## Quality Checklist

Before considering this feature complete:

- [ ] All 10 tasks marked as complete
- [ ] Reference validation passes with 0 unused references
- [ ] Reference validation passes with 0 broken URLs (or DOI alternatives)
- [ ] No hallucinated references remain
- [ ] Documentation validation passes (6 tests)
- [ ] BibTeX export generated
- [ ] Synthesis report documents methodology

## Risk Assessment

### High Risk Tasks

- **T006**: Verifying references requires manual review of actual paper content
  - Mitigation: Use DOIs to access papers, document verification methodology

- **T007**: Finding quality replacements for hallucinated references
  - Mitigation: Use multiple academic databases, prioritize peer-reviewed sources with DOIs

### Medium Risk Tasks

- **T003-T005**: Academic database rate limits may slow searches
  - Mitigation: Use NCBI_API_KEY for PubMed, stagger requests

## Notes

### Three-Pillar Framework

All claims must connect to one of:
1. **Analytics maturity** - HIMSS AMAM stages, healthcare analytics adoption rates
2. **Workforce turnover** - Impact on institutional knowledge, training costs
3. **Technical barriers** - NL2SQL challenges, schema complexity, ambiguity resolution

### Citation Format

- Academic sources: `[A1]`, `[A2]`, etc.
- Industry sources: `[I1]`, `[I2]`, etc.

### Resources

- `uv run academic-review --help` - Literature review CLI
- `python scripts/validate_references.py --help` - Reference validation
- `./validate_documentation.sh` - Documentation validation
