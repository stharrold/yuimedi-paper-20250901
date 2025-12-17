# Epics: Paper-1 Revisions

## Epic 1: Critical Content Removal (P0)

**Goal:** Remove solution-advocacy content to establish paper as pure analytical framework

### Tasks

| ID | Task | Issue | Est. Lines |
|----|------|-------|------------|
| 1.1 | Remove Section 5 (Proposed Solution) | #319 | -140 |
| 1.2 | Remove Section 6 (Evaluation) | #317 | -70 |
| 1.3 | Update section numbering and cross-references | - | ~20 edits |

**Dependencies:** None (do first)
**Validation:** No Section 5/6 headers remain; section numbers correct

---

## Epic 2: Section 4.7 Revisions (P0/P1)

**Goal:** Remove speculative market claims, add research caveats

### Tasks

| ID | Task | Issue | Est. Lines |
|----|------|-------|------------|
| 2.1 | Remove "structural disincentives" language | #315 | -10 |
| 2.2 | Reframe Watson Health/Haven as observed patterns | #315 | ~5 edits |
| 2.3 | Add research caveat paragraph | #316 | +4 |

**Dependencies:** After Epic 1 (line numbers change)
**Validation:** No speculative causal claims; caveat present

---

## Epic 3: Statistics & Methodology (P0/P1)

**Goal:** Strengthen methodology documentation and qualify statistics

### Tasks

| ID | Task | Issue | Est. Lines |
|----|------|-------|------------|
| 3.1 | Qualify [A10] turnover statistics (5 locations) | #310 | ~10 edits |
| 3.2 | Add search strategy table to Methodology | #312 | +10 |
| 3.3 | Create literature-flow.mmd diagram | #311 | +30 (new file) |
| 3.4 | Generate literature-flow.jpg | #311 | (build step) |
| 3.5 | Add figure reference in Methodology | #311 | +3 |
| 3.6 | Document single-coder limitation | #313 | +5 |
| 3.7 | Add [A10] limitation to limitations section | #310 | +4 |

**Dependencies:** After Epic 1
**Validation:** Table present; figure renders; limitations documented

---

## Epic 4: Framework Enhancement (P1/P2)

**Goal:** Add framework development rationale and theoretical grounding

### Tasks

| ID | Task | Issue | Est. Lines |
|----|------|-------|------------|
| 4.1 | Create "Framework Development and Validation" section | #321 | +25 |
| 4.2 | Add HIMSS AMAM / DIKW mapping table | #322 | +15 |
| 4.3 | Revise conclusion for framework focus | #320 | ~20 edits |
| 4.4 | Remove solution advocacy from conclusion | #320 | -10 |

**Dependencies:** After Epic 3 (section structure stabilized)
**Validation:** New section present; conclusion focuses on framework

---

## Epic 5: Language & Tone (P1)

**Goal:** Remove promotional language and update COI statement

### Tasks

| ID | Task | Issue | Est. Lines |
|----|------|-------|------------|
| 5.1 | Remove "strategic imperative" (3 occurrences) | #318 | 3 edits |
| 5.2 | Replace "urgent need" with "identified gap" | #318 | ~3 edits |
| 5.3 | Replace "devastating" with "significant" | #318 | ~2 edits |
| 5.4 | Remove competitive language | #318 | ~3 edits |
| 5.5 | Revise COI statement | #324 | ~5 edits |

**Dependencies:** After Epic 4 (conclusion revised)
**Validation:** Grep for prohibited phrases returns empty

---

## Epic 6: Submission Preparation (Doc)

**Goal:** Create materials for external submission workflows

### Tasks

| ID | Task | Issue | Est. Lines |
|----|------|-------|------------|
| 6.1 | Create expert-review-checklist.md | #323 | +50 (new file) |
| 6.2 | Create osf-registration-draft.md | #314 | +60 (new file) |
| 6.3 | Create arxiv-submission-checklist.md | #270 | +80 (new file) |
| 6.4 | Create zenodo-submission-checklist.md | #271 | +60 (new file) |

**Dependencies:** After Epic 5 (paper finalized)
**Validation:** Files exist and contain required sections

---

## Execution Order

```
Epic 1 ──> Epic 2 ──> Epic 3 ──> Epic 4 ──> Epic 5 ──> Epic 6
(removal)  (4.7)     (method)   (framework) (language) (submit)
```

## Summary

| Epic | Issues Closed | Net Line Change |
|------|---------------|-----------------|
| 1 | #319, #317 | -210 |
| 2 | #315, #316 | -6 |
| 3 | #310, #312, #311, #313 | +52 |
| 4 | #321, #322, #320 | +30 |
| 5 | #318, #324 | ~0 |
| 6 | #323, #314, #270, #271 | +250 (new files) |
| **Total** | **17 issues** | **~+116 (paper.md: -134)** |
