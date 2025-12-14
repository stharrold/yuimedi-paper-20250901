# Requirements: IT Analytics Turnover Sources

**Feature Slug:** it-analytics-turnover-sources
**GitHub Issue:** #275
**Created:** 2025-12-13
**Author:** stharrold

---

## Problem Statement

The paper claims turnover data for "clinical and technical staff" but only cites nurse-specific meta-analyses [A1, A2]. GitHub Issue #275 requests sources for non-clinical staff (specifically IT/analytics/technical roles) turnover in healthcare.

### Current State

- **[A1] Wu et al. (2024)**: Nurse turnover 18% pooled (11-26% CI)
- **[A2] Ren et al. (2024)**: Nurse turnover 8-36.6% range, 16% pooled
- **[I6] Oracle (2024)**: Cost data only (0.5-2.0x annual salary)

### Gap

Paper makes claims about "clinical and technical staff" but citations only support nursing staff turnover.

---

## User Research (Issue #275 Comment)

Key findings from user research:

1. **Technical IT Staff at Healthcare Providers: ~2.9 years tenure**
   - Annual turnover rate: 34% (calculated as 1/2.9 years; highest among IT sectors studied)
   - Source: Ang & Slaughter (2004)

2. **Hospital IT Personnel: 4-6 years average tenure**
   - Broader estimate includes medical and administrative IT staff
   - Source: Das et al. (2010)

3. **Comparison with Other IT Sectors**
   - IT managerial jobs overall: 9.68 years average tenure
   - Organizations with industrial ILM strategies: 14.1 years
   - Organizations with craft ILM strategies: 3.4 years

---

## Acceptance Criteria

- [ ] All claims about technical/IT staff have verifiable citations
- [ ] New citations verified via DOI or authoritative URL
- [ ] Consistent turnover range (8-36% for nursing, ~34% for IT) throughout paper
- [ ] Clear distinction between nursing data (peer-reviewed) and IT data
- [ ] Quality gates pass after changes

---

## References from User Research

| Citation | Source | Key Data | DOI/URL |
|----------|--------|----------|---------|
| **[A11]** | Ang & Slaughter (2004) | 2.9 years tenure, 34% turnover (1/2.9 years) for healthcare IT | ACM SIGMIS Database |
| **[A12]** | Das et al. (2010) | 4-6 years IT tenure in hospitals | IEEE Trans Eng Mgmt |
| **[A13]** | Rodriguez (2020) | Healthcare IT professional relationships | ProQuest |
| **[A14]** | Belcher (2023) | Voluntary attrition in healthcare tech | ProQuest |
