# Epics: Remove Lee 2022 Reference

**Date:** 2025-12-14
**Issue:** #285
**Author:** stharrold

## Epic Summary

| Epic ID | Name | Priority | Complexity | Estimate |
|---------|------|----------|------------|----------|
| E-001 | Update paper.md | High | Medium | 15 min |
| E-002 | Update metadata files | Medium | Low | 5 min |
| E-003 | Update documentation | Medium | Low | 5 min |
| E-004 | Regenerate outputs | Medium | Low | 5 min |
| E-005 | Validate and verify | High | Low | 5 min |

**Total Estimated Time:** 35 minutes

## Epic Definitions

### E-001: Update paper.md

**Priority:** High
**Complexity:** Medium (11 locations to update)

**Tasks:**
1. Rewrite line 232 to remove Lee et al. [A8] mention
2. Delete reference definition at line 756
3. Renumber [A9]-[A14] → [A8]-[A13] in References section
4. Update in-text citation at line 696 ([A11] → [A10])
5. Update in-text citations at line 610 ([A9], [A10] → [A8], [A9])
6. Update in-text citation at line 541 ([A10] → [A9])
7. Update in-text citation at line 539 ([A9] → [A8])
8. Update in-text citations at line 274 ([A12], [A13], [A14] → [A11], [A12], [A13])
9. Update in-text citation at line 272 ([A11] → [A10])
10. Update in-text citations at line 238 ([A9, A10] → [A8, A9])
11. Update in-text citations at line 226 ([A9, A10] → [A8, A9])
12. Update in-text citation at line 109 ([A11] → [A10])
13. Update in-text citation at line 96 ([A11] → [A10])
14. Update in-text citation at line 80 ([A11] → [A10])

**Acceptance Criteria:**
- [ ] Line 232 reads naturally with only Wang et al. [A5]
- [ ] No [A8] reference definition exists
- [ ] References numbered [A1]-[A13] sequentially
- [ ] All in-text citations updated

### E-002: Update Metadata Files

**Priority:** Medium
**Complexity:** Low

**Tasks:**
1. Update CLAUDE.md line 28 - citation count to "24 (13 academic, 11 industry)"
2. Update CLAUDE.md line 33 - citation history to include Issue #285

**Acceptance Criteria:**
- [ ] CLAUDE.md reflects accurate post-removal count
- [ ] Citation history mentions this removal

### E-003: Update Documentation Files

**Priority:** Medium
**Complexity:** Low

**Tasks:**
1. Update docs/citation-audit-report.md - remove [A8] references
2. Update specs/fix-paper-references/reference_verification.md - remove [A8] section
3. Update specs/fix-paper-references/claims_analysis.md - update [A8] references

**Acceptance Criteria:**
- [ ] No documentation files reference removed [A8]
- [ ] All reference numbers updated to new scheme

### E-004: Regenerate Output Files

**Priority:** Medium
**Complexity:** Low

**Tasks:**
1. Run `./scripts/build_paper.sh --format all`

**Acceptance Criteria:**
- [ ] paper.pdf regenerated successfully
- [ ] paper.html regenerated successfully
- [ ] paper.docx regenerated successfully
- [ ] paper.tex regenerated successfully

### E-005: Validate and Verify

**Priority:** High
**Complexity:** Low

**Tasks:**
1. Run `./validate_documentation.sh`
2. Run `python scripts/validate_references.py --all`
3. Verify no orphaned citations
4. Verify no unused references
5. Verify sequential numbering

**Acceptance Criteria:**
- [ ] validate_documentation.sh exits with code 0
- [ ] validate_references.py --check-citations exits with code 0
- [ ] 0 orphaned citations
- [ ] 0 unused references
- [ ] [A1]-[A13], [I1]-[I11] sequential numbering

## Dependencies

```
E-001 → E-002 → E-003 → E-004 → E-005
   |__________________|
          |
    (can run in parallel after E-001)
```

E-001 must complete first, then E-002/E-003 can run in parallel, followed by E-004 and E-005.

## Critical Path

E-001 (paper.md) → E-005 (validation)

The critical path is updating paper.md and validating the result. Metadata and documentation updates are secondary.
