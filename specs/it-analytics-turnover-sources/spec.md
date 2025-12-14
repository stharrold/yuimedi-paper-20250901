# Specification: IT Analytics Turnover Sources

**Type:** feature
**Slug:** it-analytics-turnover-sources
**Date:** 2025-12-14
**Author:** stharrold
**GitHub Issue:** #275

## Overview

This feature addresses GitHub Issue #275: Find sources for non-clinical staff (IT/analytics/technical roles) turnover in healthcare. The paper currently cites turnover data for "clinical and technical staff" but only references nurse-specific meta-analyses [A1, A2]. This specification defines the documentation updates needed to properly cite IT-specific turnover research.

## Problem Statement

**Current State:**
- Paper claims turnover data for "clinical and technical staff"
- Only nursing-specific sources cited: [A1] Wu et al. (2024), [A2] Ren et al. (2024)
- No citations supporting IT/analytics/technical staff turnover claims

**Solution:**
- Add verified academic sources for IT staff turnover in healthcare
- Update paper text to clearly distinguish nursing vs IT turnover rates
- Maintain citation integrity with DOI-verified references

## Implementation Context

**BMAD Planning:** See `planning/it-analytics-turnover-sources/` for complete requirements and architecture.

**Implementation Type:** Documentation-only (no code changes)

**Key Constraints:**
- All citations must be DOI-verifiable or from authoritative sources
- Maintain existing citation format ([A#] for academic, [I#] for industry)
- Clear distinction between nursing data (peer-reviewed meta-analyses) and IT data

## New Citations to Add

### [A11] Ang & Slaughter (2004)

**Full Citation:**
> Ang, S., & Slaughter, S. (2004). Turnover of information technology professionals: The effects of internal labor market strategies. *ACM SIGMIS Database: The DATABASE for Advances in Information Systems*, 35(3), 11-27. https://doi.org/10.1145/1017114.1017118

**Key Statistics:**
- Healthcare IT professionals: **2.9 years average tenure**
- Annual turnover rate: **15.54%** (highest among IT organization types studied)
- Context: IT serves as support function rather than core business at healthcare providers

**Why This Source:**
- Peer-reviewed academic journal
- Directly addresses healthcare IT sector
- Provides comparison across IT organization types
- Explains why healthcare IT has highest turnover

---

### [A12] Das et al. (2010)

**Full Citation:**
> Das, S., Yaylacicegi, U., & Menon, N.M. (2010). The effect of information technology investments in healthcare: A longitudinal study of its lag, duration, and economic value. *IEEE Transactions on Engineering Management*, 58(1), 124-140. https://doi.org/10.1109/TEM.2009.2034254

**Key Statistics:**
- Hospital IT personnel: **4-6 years average tenure**
- Context: Longer tenure than Ang & Slaughter findings, includes administrative IT staff

**Why This Source:**
- Peer-reviewed IEEE journal
- Hospital-specific IT focus
- Complements [A11] with broader tenure range

---

## Paper.md Update Locations

### 1. Abstract (Line ~15)

**Current Text:**
> Healthcare workforce turnover rates of 8-36% create institutional memory loss

**Updated Text:**
> Healthcare nursing turnover rates of 8-36% and IT staff turnover of ~15% create institutional memory loss

**Rationale:** Distinguishes nursing-specific data from IT-specific data

---

### 2. Executive Summary (Line ~80)

**Current Text:**
> annual turnover rates of 8-36% [A1, A2] create institutional memory loss

**Updated Text:**
> nursing turnover rates of 8-36% [A1, A2] and IT staff turnover of 15.54% [A11] create institutional memory loss

**Rationale:** Adds IT citation while preserving nursing attribution

---

### 3. Introduction (Line ~96)

**Current Text:**
> Annual turnover of 15-36% for clinical and technical staff creates cascading knowledge loss

**Updated Text:**
> Annual nursing turnover of 8-36% [A1, A2] combines with IT staff turnover of 15.54% [A11] (the highest rate among all IT organization types studied), creating cascading knowledge loss

**Rationale:** Separates staff types with specific citations

---

### 4. Problem Statement (Lines ~108-109)

**Current Text:**
> Healthcare workforce turnover rates of 15-36% annually [A1, A2] create devastating institutional memory loss.

**Updated Text:**
> Healthcare nursing turnover rates of 8-36% annually [A1, A2] create devastating institutional memory loss. IT staff at healthcare providers experience even higher turnover at 15.54% annually, with average tenure of only 2.9 years—the lowest among IT organization types studied [A11].

**Rationale:** Adds IT-specific detail with comparison context

---

### 5. Literature Review (After Line ~195)

**New Paragraph:**
> Technical and analytics staff face even more severe turnover challenges. Ang and Slaughter [A11] found that IT professionals at healthcare provider institutions—where IT serves as a support function rather than core business—have average tenure of just 2.9 years and annual turnover of 15.54%, the highest rate among all IT organization types studied. This compares unfavorably to the 9.68-year average for IT managerial positions overall, highlighting the particular vulnerability of healthcare IT departments to knowledge loss.

**Note:** [A12] Das et al. (2010) was listed as a secondary source but deferred from this implementation. The [A11] citation provides sufficient evidence for the IT turnover claims.

**Rationale:** Provides dedicated section on IT turnover with full context

---

### 6. References Section

**Add after [A10]:**

```
[A11] Ang, S., & Slaughter, S. (2004). Turnover of information technology professionals: The effects of internal labor market strategies. ACM SIGMIS Database: The DATABASE for Advances in Information Systems, 35(3), 11-27. https://doi.org/10.1145/1017114.1017118
```

**Note:** [A12] Das et al. (2010) was documented in this spec as a secondary source but deferred from implementation. See Citation Priority section for rationale.

---

## Validation Requirements

### Reference Validation
```bash
python scripts/validate_references.py --all
```
- All citations must appear in References section
- No orphaned citations in paper text
- DOIs must resolve correctly

### Documentation Validation
```bash
./validate_documentation.sh
```
- All 6 tests must pass
- File size under 30KB limit
- No cross-reference errors

### Quality Gates
```bash
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```
- Full quality gate suite must pass before PR

---

## Quality Checklist

Before completing this feature:

- [x] DOI for [A11] verified at ACM Digital Library
- [x] Statistics (2.9 years, 15.54%) confirmed against source
- [x] All paper.md locations updated per specification
- [x] Reference validation passes
- [x] Documentation validation passes
- [x] Quality gates pass
- [x] PR ready for develop branch

**Note:** [A12] verification deferred - see Citation Priority section.

---

## Notes

### Citation Priority

**Primary (must add):**
- [A11] Ang & Slaughter (2004) - Core IT turnover statistics

**Secondary (add if space permits):**
- [A12] Das et al. (2010) - Hospital IT tenure data

**Optional (from Issue #275 research):**
- [A13] Rodriguez (2020) - Healthcare IT relationships (ProQuest)
- [A14] Belcher (2023) - Healthcare tech attrition (ProQuest)

Note: [A13] and [A14] are ProQuest dissertations. Include only if [A11] and [A12] prove insufficient for paper's needs.

### Turnover Rate Summary

| Staff Type | Turnover Rate | Tenure | Source |
|------------|---------------|--------|--------|
| Nursing (pooled) | 8-36% | - | [A1], [A2] |
| Healthcare IT | 15.54% | 2.9 years | [A11] |
| Hospital IT | - | 4-6 years | [A12] |
| IT overall | - | 9.68 years | [A11] (comparison) |

---

## References

- [planning/it-analytics-turnover-sources/requirements.md](../../planning/it-analytics-turnover-sources/requirements.md)
- [planning/it-analytics-turnover-sources/architecture.md](../../planning/it-analytics-turnover-sources/architecture.md)
- [planning/it-analytics-turnover-sources/epics.md](../../planning/it-analytics-turnover-sources/epics.md)
- GitHub Issue #275
