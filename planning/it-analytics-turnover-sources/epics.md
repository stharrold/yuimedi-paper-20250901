# Epics: IT Analytics Turnover Sources

**Feature Slug:** it-analytics-turnover-sources
**GitHub Issue:** #275
**Created:** 2025-12-13
**Author:** stharrold

---

## Epic Summary

| Epic | Description | Priority | Status |
|------|-------------|----------|--------|
| E-001 | Verify new source DOIs/URLs | P0 | Pending |
| E-002 | Add new references to paper.md | P0 | Pending |
| E-003 | Update turnover claims in paper text | P0 | Pending |
| E-004 | Run validation and quality gates | P0 | Pending |

---

## E-001: Verify New Source DOIs/URLs

**Priority:** P0
**Estimated Effort:** Small

### Tasks

- [ ] Verify Ang & Slaughter (2004) DOI at ACM Digital Library
- [ ] Verify Das et al. (2010) DOI at IEEE Xplore
- [ ] Verify Rodriguez (2020) at ProQuest
- [ ] Verify Belcher (2023) at ProQuest
- [ ] Confirm key statistics match source documents

### Acceptance Criteria

- All 4 new sources have verifiable DOIs or stable URLs
- Key statistics (2.9 years tenure → 34% annual turnover) confirmed via calculation methodology

---

## E-002: Add New References to paper.md

**Priority:** P0
**Estimated Effort:** Small

### Tasks

- [ ] Add [A11] Ang & Slaughter (2004) citation
- [ ] Add [A12] Das et al. (2010) citation
- [ ] Add [A13] Rodriguez (2020) citation (if used)
- [ ] Add [A14] Belcher (2023) citation (if used)

### Acceptance Criteria

- New references follow existing citation format
- Academic citations use [A#] format
- All references include DOI or URL

---

## E-003: Update Turnover Claims in Paper Text

**Priority:** P0
**Estimated Effort:** Medium

### Tasks

- [ ] Update Abstract (line 15)
- [ ] Update Executive Summary (line 80)
- [ ] Update Introduction (line 96)
- [ ] Update Problem Statement (lines 108-109)
- [ ] Add new paragraph in Literature Review (after line 195)

### Acceptance Criteria

- Clear distinction between nursing turnover (8-36%) and IT turnover (~34%)
- All IT turnover claims cite [A11] or other new sources
- No orphaned citations

---

## E-004: Run Validation and Quality Gates

**Priority:** P0
**Estimated Effort:** Small

### Tasks

- [ ] Run `python scripts/validate_references.py --all`
- [ ] Run `./validate_documentation.sh`
- [ ] Run quality gates
- [ ] Fix any validation errors

### Acceptance Criteria

- All validation passes
- No broken references
- No duplicate citations

---

## Dependencies

```
E-001 (Verify DOIs) → E-002 (Add References) → E-003 (Update Text) → E-004 (Validate)
```

All epics are sequential - each depends on the previous completing successfully.
