# Implementation Plan: IT Analytics Turnover Sources

**Type:** feature
**Slug:** it-analytics-turnover-sources
**Date:** 2025-12-14
**GitHub Issue:** #275

## Overview

This is a **documentation update task** - no code changes required. Updates `paper.md` with new academic citations for IT/technical staff turnover rates in healthcare to support claims about non-clinical workforce turnover.

## Task Breakdown

### Phase 1: Source Verification (E-001)

#### Task doc_001: Verify Ang & Slaughter (2004) DOI

**Priority:** P0
**Files:** None (research task)

**Description:**
Verify DOI and key statistics for primary IT turnover source.

**Steps:**
1. Access ACM Digital Library for Ang & Slaughter (2004)
2. Confirm DOI: `10.1145/1017114.1017118`
3. Verify statistics: 2.9 years tenure, 15.54% annual turnover for healthcare IT
4. Document full citation with DOI

**Acceptance Criteria:**
- [ ] DOI resolves to correct paper
- [ ] Statistics confirmed against original source

**Dependencies:** None

---

#### Task doc_002: Verify Das et al. (2010) DOI

**Priority:** P0
**Files:** None (research task)

**Description:**
Verify DOI and key statistics for hospital IT tenure source.

**Steps:**
1. Access IEEE Xplore for Das et al. (2010)
2. Confirm DOI: `10.1109/TEM.2009.2034254`
3. Verify statistics: 4-6 years IT tenure in hospitals
4. Document full citation with DOI

**Acceptance Criteria:**
- [ ] DOI resolves to correct paper
- [ ] Statistics confirmed against original source

**Dependencies:** None

---

### Phase 2: Add References (E-002)

#### Task doc_003: Add [A11] Citation

**Priority:** P0
**Files:**
- `paper.md` (References section)

**Description:**
Add Ang & Slaughter (2004) citation to paper.md references.

**Citation Format:**
```
[A11] Ang, S., & Slaughter, S. (2004). Turnover of information technology professionals:
The effects of internal labor market strategies. ACM SIGMIS Database: The DATABASE
for Advances in Information Systems, 35(3), 11-27. https://doi.org/10.1145/1017114.1017118
```

**Acceptance Criteria:**
- [ ] Citation follows existing [A#] format
- [ ] DOI included and functional
- [ ] Placed after [A10] in References section

**Dependencies:** doc_001

---

#### Task doc_004: Add [A12] Citation

**Priority:** P0
**Files:**
- `paper.md` (References section)

**Description:**
Add Das et al. (2010) citation to paper.md references.

**Citation Format:**
```
[A12] Das, S., Yaylacicegi, U., & Menon, N.M. (2010). The effect of information
technology investments in healthcare: A longitudinal study of its lag, duration,
and economic value. IEEE Transactions on Engineering Management, 58(1), 124-140.
https://doi.org/10.1109/TEM.2009.2034254
```

**Acceptance Criteria:**
- [ ] Citation follows existing [A#] format
- [ ] DOI included and functional
- [ ] Placed after [A11] in References section

**Dependencies:** doc_002

---

### Phase 3: Update Paper Text (E-003)

#### Task doc_005: Update Abstract

**Priority:** P0
**Files:**
- `paper.md` (Line ~15)

**Description:**
Update Abstract to distinguish nursing vs IT turnover rates.

**Current:**
> Healthcare workforce turnover rates of 8-36% create institutional memory loss

**Revised:**
> Healthcare nursing turnover rates of 8-36% and IT staff turnover of ~15% create institutional memory loss

**Acceptance Criteria:**
- [ ] Clear distinction between nursing and IT turnover
- [ ] Statistics accurate

**Dependencies:** doc_003

---

#### Task doc_006: Update Executive Summary

**Priority:** P0
**Files:**
- `paper.md` (Line ~80)

**Description:**
Update Executive Summary with IT turnover citation.

**Current:**
> annual turnover rates of 8-36% [A1, A2] create institutional memory loss

**Revised:**
> nursing turnover rates of 8-36% [A1, A2] and IT staff turnover of 15.54% [A11] create institutional memory loss

**Acceptance Criteria:**
- [ ] [A11] citation added
- [ ] Clear role distinction

**Dependencies:** doc_003

---

#### Task doc_007: Update Introduction

**Priority:** P0
**Files:**
- `paper.md` (Line ~96)

**Description:**
Update Introduction paragraph with IT turnover data.

**Current:**
> Annual turnover of 15-36% for clinical and technical staff creates cascading knowledge loss

**Revised:**
> Annual nursing turnover of 8-36% [A1, A2] combines with IT staff turnover of 15.54% [A11] (the highest among IT sectors), creating cascading knowledge loss

**Acceptance Criteria:**
- [ ] Citations properly attributed to specific staff types
- [ ] IT sector comparison noted

**Dependencies:** doc_003

---

#### Task doc_008: Update Problem Statement

**Priority:** P0
**Files:**
- `paper.md` (Lines ~108-109)

**Description:**
Expand Problem Statement with IT turnover details.

**Current:**
> Healthcare workforce turnover rates of 15-36% annually [A1, A2] create devastating institutional memory loss.

**Revised:**
> Healthcare nursing turnover rates of 8-36% annually [A1, A2] create devastating institutional memory loss. IT staff at healthcare providers experience even higher turnover at 15.54% annually, with average tenure of only 2.9 years—the lowest among IT sectors studied [A11].

**Acceptance Criteria:**
- [ ] IT-specific data with citation
- [ ] Tenure statistic included

**Dependencies:** doc_003

---

#### Task doc_009: Add Literature Review Paragraph

**Priority:** P0
**Files:**
- `paper.md` (After Line ~195)

**Description:**
Add new paragraph on IT/technical staff turnover to Literature Review section.

**New Paragraph:**
> Technical and analytics staff face even more severe turnover challenges. Ang and Slaughter [A11] found that IT professionals at healthcare provider institutions—where IT serves as a support function rather than core business—have average tenure of just 2.9 years and annual turnover of 15.54%, the highest rate among all IT organization types studied. Das et al. [A12] documented hospital IT personnel tenure of 4-6 years, still considerably shorter than the 9.68-year average for IT managerial positions overall.

**Acceptance Criteria:**
- [ ] Both [A11] and [A12] cited
- [ ] Comparison to other IT sectors included
- [ ] Flows logically after nursing turnover discussion

**Dependencies:** doc_003, doc_004

---

### Phase 4: Validation (E-004)

#### Task doc_010: Run Reference Validation

**Priority:** P0
**Files:** None

**Description:**
Validate all references including new citations.

**Verification:**
```bash
python scripts/validate_references.py --all
```

**Acceptance Criteria:**
- [ ] All citations in References section
- [ ] No orphaned citations in paper text
- [ ] All DOIs valid

**Dependencies:** doc_003, doc_004, doc_005, doc_006, doc_007, doc_008, doc_009

---

#### Task doc_011: Run Documentation Validation

**Priority:** P0
**Files:** None

**Description:**
Run full documentation validation suite.

**Verification:**
```bash
./validate_documentation.sh
```

**Acceptance Criteria:**
- [ ] All 6 tests pass
- [ ] No validation errors

**Dependencies:** doc_010

---

#### Task doc_012: Run Quality Gates

**Priority:** P0
**Files:** None

**Description:**
Run complete quality gates before PR.

**Verification:**
```bash
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

**Acceptance Criteria:**
- [ ] All quality gates pass
- [ ] Ready for PR to develop

**Dependencies:** doc_011

---

## Task Dependencies Graph

```
doc_001 ─> doc_003 ─┬─> doc_005
                    ├─> doc_006
doc_002 ─> doc_004 ─┼─> doc_007  ─> doc_010 ─> doc_011 ─> doc_012
                    ├─> doc_008
                    └─> doc_009
```

## Critical Path

1. doc_001 (Verify Ang & Slaughter)
2. doc_003 (Add [A11])
3. doc_009 (Add Literature Review paragraph - depends on both citations)
4. doc_010 (Reference validation)
5. doc_011 (Documentation validation)
6. doc_012 (Quality gates)

## Parallel Work Opportunities

- doc_001 and doc_002 can be done in parallel
- doc_005, doc_006, doc_007, doc_008 can be done in parallel (after doc_003)

## Quality Checklist

Before considering this feature complete:

- [ ] All DOIs verified and functional
- [ ] All new citations follow existing format
- [ ] Clear distinction between nursing and IT turnover data throughout
- [ ] Reference validation passes
- [ ] Documentation validation passes (all 6 tests)
- [ ] Quality gates pass
- [ ] PR ready for review

## Notes

### Key Statistics to Use

| Source | Key Statistic | Context |
|--------|---------------|---------|
| [A11] Ang & Slaughter | 2.9 years, 15.54% turnover | Healthcare IT highest among sectors |
| [A12] Das et al. | 4-6 years tenure | Hospital IT personnel |

### Citation Format Reminders

- Academic: `[A#]` prefix (A11, A12, etc.)
- Industry: `[I#]` prefix
- All citations need DOI or authoritative URL
