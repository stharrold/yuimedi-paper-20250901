# Implementation Plan: Remove Lee 2022 Reference

**Type:** feature
**Slug:** remove-lee-2022-reference
**Date:** 2025-12-14
**Issue:** #285

## Task Breakdown

### Epic E-001: Update paper.md (High Priority)

**Critical Path:** Yes
**Execution Order:** Bottom-to-top to avoid line number shifts

---

#### Task impl_001: Delete Reference Definition

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Delete the [A8] reference definition from line 756.

**Steps:**
1. Navigate to line 756 in paper.md
2. Delete the complete [A8] reference entry (Lee et al. 2022)

**Acceptance Criteria:**
- [ ] No [A8] reference definition exists in References section

**Verification:**
```bash
grep -n "\[A8\]" paper.md | head -5
```

**Dependencies:**
- None (start here, highest line number)

---

#### Task impl_002: Renumber Reference Definitions

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Renumber references [A9]-[A14] to [A8]-[A13] in the References section (lines 758-768).

**Steps:**
1. Change [A9] → [A8] (MedAgentBench)
2. Change [A10] → [A9] (Chen et al.)
3. Change [A11] → [A10] (Ang & Slaughter)
4. Change [A12] → [A11] (Ledikwe et al.)
5. Change [A13] → [A12] (Mantas et al.)
6. Change [A14] → [A13] (Musa et al.)

**Acceptance Criteria:**
- [ ] References numbered [A1]-[A13] sequentially
- [ ] No gaps in numbering
- [ ] Industry references [I1]-[I11] unchanged

**Verification:**
```bash
grep -E "^\[A[0-9]+\]" paper.md
```

**Dependencies:**
- impl_001 (delete [A8] first)

---

#### Task impl_003: Update In-Text Citation at Line 696

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Update in-text citation: [A11] → [A10]

**Steps:**
1. Find line 696
2. Replace [A11] with [A10]

**Acceptance Criteria:**
- [ ] Line 696 uses [A10] instead of [A11]

**Dependencies:**
- impl_002

---

#### Task impl_004: Update In-Text Citations at Line 610

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Update in-text citations: [A9], [A10] → [A8], [A9]

**Steps:**
1. Find line 610
2. Replace [A9] with [A8]
3. Replace [A10] with [A9]

**Acceptance Criteria:**
- [ ] Line 610 uses [A8] and [A9]

**Dependencies:**
- impl_003

---

#### Task impl_005: Update In-Text Citation at Line 541

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Update in-text citation: [A10] → [A9]

**Steps:**
1. Find line 541
2. Replace [A10] with [A9]

**Acceptance Criteria:**
- [ ] Line 541 uses [A9] instead of [A10]

**Dependencies:**
- impl_004

---

#### Task impl_006: Update In-Text Citation at Line 539

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Update in-text citation: [A9] → [A8]

**Steps:**
1. Find line 539
2. Replace [A9] with [A8]

**Acceptance Criteria:**
- [ ] Line 539 uses [A8] instead of [A9]

**Dependencies:**
- impl_005

---

#### Task impl_007: Update In-Text Citations at Line 274

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Update in-text citations: [A12], [A13], [A14] → [A11], [A12], [A13]

**Steps:**
1. Find line 274
2. Replace [A12] with [A11]
3. Replace [A13] with [A12]
4. Replace [A14] with [A13]

**Acceptance Criteria:**
- [ ] Line 274 uses [A11], [A12], [A13]

**Dependencies:**
- impl_006

---

#### Task impl_008: Update In-Text Citation at Line 272

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Update in-text citation: [A11] → [A10]

**Steps:**
1. Find line 272
2. Replace [A11] with [A10]

**Acceptance Criteria:**
- [ ] Line 272 uses [A10] instead of [A11]

**Dependencies:**
- impl_007

---

#### Task impl_009: Update In-Text Citations at Line 238

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Update in-text citations: [A9, A10] → [A8, A9]

**Steps:**
1. Find line 238
2. Replace [A9, A10] with [A8, A9]

**Acceptance Criteria:**
- [ ] Line 238 uses [A8, A9]

**Dependencies:**
- impl_008

---

#### Task impl_010: Rewrite Line 232 (Remove Lee et al. mention)

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Remove "and Lee et al. [A8]" from sentence, keeping Wang et al. [A5] as sole citation.

**Steps:**
1. Find line 232
2. Rewrite sentence to flow naturally with only Wang et al. [A5]
3. Ensure grammatical correctness

**Acceptance Criteria:**
- [ ] Line 232 reads naturally without Lee et al. mention
- [ ] Wang et al. [A5] remains as sole citation

**Dependencies:**
- impl_009

---

#### Task impl_011: Update In-Text Citations at Line 226

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Update in-text citations: [A9, A10] → [A8, A9]

**Steps:**
1. Find line 226
2. Replace [A9, A10] with [A8, A9]

**Acceptance Criteria:**
- [ ] Line 226 uses [A8, A9]

**Dependencies:**
- impl_010

---

#### Task impl_012: Update In-Text Citations at Lines 80, 96, 109

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Update in-text citations: [A11] → [A10] at lines 80, 96, 109

**Steps:**
1. Find line 109, replace [A11] with [A10]
2. Find line 96, replace [A11] with [A10]
3. Find line 80, replace [A11] with [A10]

**Acceptance Criteria:**
- [ ] Lines 80, 96, 109 all use [A10]

**Dependencies:**
- impl_011

---

### Epic E-002: Update Metadata Files (Medium Priority)

---

#### Task meta_001: Update CLAUDE.md Citation Count

**Priority:** Medium

**Files:**
- `CLAUDE.md`

**Description:**
Update citation count from "22 (11 academic, 11 industry)" to "24 (13 academic, 11 industry)" and update citation history.

**Steps:**
1. Update line 28 with new count
2. Update line 33 citation history to mention Issue #285

**Acceptance Criteria:**
- [ ] CLAUDE.md shows "24 verified citations (13 academic, 11 industry)"
- [ ] Citation history updated

**Dependencies:**
- Epic E-001 complete

---

### Epic E-003: Update Documentation Files (Medium Priority)

---

#### Task doc_001: Update Citation Audit Report

**Priority:** Medium

**Files:**
- `docs/citation-audit-report.md`

**Description:**
Remove [A8] references from citation lists and update reference numbers.

**Acceptance Criteria:**
- [ ] No [A8] references in citation-audit-report.md

**Dependencies:**
- Epic E-001 complete

---

#### Task doc_002: Update Reference Verification

**Priority:** Medium

**Files:**
- `specs/fix-paper-references/reference_verification.md`

**Description:**
Remove [A8] section and update reference numbers.

**Acceptance Criteria:**
- [ ] No [A8] section in reference_verification.md
- [ ] Reference numbers updated

**Dependencies:**
- doc_001

---

#### Task doc_003: Update Claims Analysis

**Priority:** Medium

**Files:**
- `specs/fix-paper-references/claims_analysis.md`

**Description:**
Update [A8] references to reflect removal.

**Acceptance Criteria:**
- [ ] claims_analysis.md updated

**Dependencies:**
- doc_002

---

### Epic E-004: Regenerate Output Files (Medium Priority)

---

#### Task output_001: Regenerate All Output Formats

**Priority:** Medium

**Files:**
- `paper.pdf`
- `paper.html`
- `paper.docx`
- `paper.tex`

**Description:**
Regenerate all output files using build script.

**Steps:**
1. Run `./scripts/build_paper.sh --format all`
2. Verify all files generated successfully

**Acceptance Criteria:**
- [ ] paper.pdf regenerated
- [ ] paper.html regenerated
- [ ] paper.docx regenerated
- [ ] paper.tex regenerated
- [ ] No rendering errors

**Verification:**
```bash
./scripts/build_paper.sh --format all
ls -la paper.pdf paper.html paper.docx paper.tex
```

**Dependencies:**
- Epic E-001, E-002, E-003 complete

---

### Epic E-005: Validate and Verify (High Priority)

---

#### Task validate_001: Run Documentation Validation

**Priority:** High

**Files:**
- (validation scripts)

**Description:**
Run full documentation validation suite.

**Steps:**
1. Run `./validate_documentation.sh`
2. Verify all 7 tests pass

**Acceptance Criteria:**
- [ ] validate_documentation.sh exits with code 0
- [ ] All 7 tests pass

**Verification:**
```bash
./validate_documentation.sh
```

**Dependencies:**
- Epic E-004 complete

---

#### Task validate_002: Run Reference Validation

**Priority:** High

**Files:**
- (validation scripts)

**Description:**
Run reference validation and check for orphaned citations.

**Steps:**
1. Run `python scripts/validate_references.py --all`
2. Run `python scripts/validate_references.py --check-citations`
3. Verify no orphaned citations or unused references

**Acceptance Criteria:**
- [ ] validate_references.py --all passes
- [ ] validate_references.py --check-citations passes
- [ ] 0 orphaned citations
- [ ] 0 unused references
- [ ] Sequential numbering [A1]-[A13], [I1]-[I11]

**Verification:**
```bash
python scripts/validate_references.py --all
python scripts/validate_references.py --check-citations
```

**Dependencies:**
- validate_001

---

## Task Dependencies Graph

```
impl_001 ─> impl_002 ─> impl_003 ─> ... ─> impl_012
                                              │
                                              v
                        ┌─────────────────────┼─────────────────────┐
                        │                     │                     │
                        v                     v                     v
                    meta_001              doc_001              doc_002
                        │                     │                     │
                        │                     v                     v
                        │                 doc_003               (merged)
                        │                     │
                        └─────────┬───────────┘
                                  │
                                  v
                            output_001
                                  │
                                  v
                           validate_001
                                  │
                                  v
                           validate_002
```

## Critical Path

1. impl_001 → impl_002 → ... → impl_012 (paper.md edits)
2. output_001 (regenerate outputs)
3. validate_001 → validate_002 (validation)

## Parallel Work Opportunities

After Epic E-001 (paper.md edits) completes:
- meta_001 (CLAUDE.md) can run in parallel with
- doc_001, doc_002, doc_003 (documentation updates)

## Quality Checklist

Before considering this feature complete:

- [ ] All tasks marked as complete
- [ ] Reference [A8] completely removed
- [ ] References numbered [A1]-[A13], [I1]-[I11] sequentially
- [ ] All in-text citations updated
- [ ] CLAUDE.md citation count accurate
- [ ] All documentation files updated
- [ ] Output files regenerated
- [ ] validate_documentation.sh passes (7/7 tests)
- [ ] validate_references.py --check-citations passes
- [ ] No orphaned citations
- [ ] No unused references

## Risk Assessment

### Low Risk
- This is a documentation-only change
- All edits are straightforward find/replace operations
- Validation scripts will catch any missed updates

### Mitigation
- Edit from bottom-to-top to avoid line number shifts
- Use grep to verify all occurrences before and after
- Run validation after each major step
