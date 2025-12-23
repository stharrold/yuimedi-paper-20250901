# Architecture: IT Analytics Turnover Sources

**Feature Slug:** it-analytics-turnover-sources
**GitHub Issue:** #275
**Created:** 2025-12-13
**Author:** stharrold

---

## Overview

This is a **documentation update task**, not a software development task. The "architecture" describes the approach for updating paper.md with new citations.

---

## Citation Strategy

### New Academic Sources (from issue #275 research)

| Citation | Full Reference | Key Data |
|----------|----------------|----------|
| **[A11]** | Ang, S., & Slaughter, S. (2004). Turnover of information technology professionals: The effects of internal labor market strategies. *ACM SIGMIS Database: The DATABASE for Advances in Information Systems*. | Healthcare IT: 2.9 years tenure, 34% annual turnover (1/2.9 years) |
| **[A12]** | Das, S., Yaylacicegi, U., & Menon, N.M. (2010). The effect of information technology investments in healthcare: A longitudinal study of its lag, duration, and economic value. *IEEE Transactions on Engineering Management*. | Hospital IT: 4-6 years tenure |
| **[A13]** | Rodriguez, R.M. (2020). A Study of Information Technology Professionals in Healthcare and Higher Education Perceived Quality of Relationship with Their Leaders and Its Effects. *ProQuest*. | Healthcare IT professional relationships |
| **[A14]** | Belcher, S.R. (2023). Addressing Voluntary Attrition Within Healthcare Technology Organizations. *ProQuest*. | Healthcare tech voluntary attrition |

---

## Paper.md Update Locations

### Update 1: Abstract (Line 15)

**Current:**
> Healthcare workforce turnover rates of 8-36% create institutional memory loss

**Revised:**
> Healthcare nursing turnover rates of 8-36% and IT staff turnover of ~34% create institutional memory loss

### Update 2: Executive Summary (Line 80)

**Current:**
> annual turnover rates of 8-36% [A1, A2] create institutional memory loss

**Revised:**
> nursing turnover rates of 8-36% [A1, A2] and IT staff turnover of 34% [A11] create institutional memory loss

### Update 3: Introduction (Line 96)

**Current:**
> Annual turnover of 15-36% for clinical and technical staff creates cascading knowledge loss

**Revised:**
> Annual nursing turnover of 8-36% [A1, A2] combines with IT staff turnover of 34% [A11] (the highest among IT sectors), creating cascading knowledge loss

### Update 4: Problem Statement (Lines 108-109)

**Current:**
> Healthcare workforce turnover rates of 15-36% annually [A1, A2] create devastating institutional memory loss.

**Revised:**
> Healthcare nursing turnover rates of 8-36% annually [A1, A2] create devastating institutional memory loss. IT staff at healthcare providers experience even higher turnover at 34% annually (calculated as 1/2.9 years), with average tenure of only 2.9 years, the lowest among IT sectors studied [A11].

### Update 5: Literature Review (Lines 191-195)

**Current section** focuses only on nurse turnover.

**Add new paragraph after line 195:**
> Technical and analytics staff face even more severe turnover challenges. Ang and Slaughter [A11] found that IT professionals at healthcare provider institutions (where IT serves as a support function rather than core business) have average tenure of just 2.9 years, implying annual turnover of 34% (1/2.9 years), the highest rate among all IT organization types studied. Das et al. [A12] documented hospital IT personnel tenure of 4-6 years, still considerably shorter than the 9.68-year average for IT managerial positions overall.

### Update 6: References Section (after [A10])

Add the four new citations in proper format.

---

## Validation Plan

```bash
# 1. Reference validation
python scripts/validate_references.py --all

# 2. Documentation validation
./validate_documentation.sh

# 3. Quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

---

## Files to Modify

| File | Lines | Changes |
|------|-------|---------|
| `paper.md` | 15 | Abstract - clarify nursing vs IT turnover |
| `paper.md` | 80 | Executive Summary - add [A11] citation |
| `paper.md` | 96 | Introduction - add [A11] citation |
| `paper.md` | 108-109 | Problem Statement - add IT turnover data |
| `paper.md` | 195+ | Literature Review - add new paragraph |
| `paper.md` | References | Add [A11], [A12], [A13], [A14] |
