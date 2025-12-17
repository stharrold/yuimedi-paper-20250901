# Requirements: Paper-1 Revisions

## Overview

Transform the Three-Pillar Analytical Framework paper (Paper 1) from a solution-advocacy piece into a pure analytical framework contribution, addressing all 17 GitHub issues labeled `paper-1`.

## Problem Statement

The current paper.md contains:
1. Solution advocacy sections (Sections 5-6) that belong in Paper 2
2. Speculative market claims without evidence
3. Promotional language ("strategic imperative", "call to action")
4. Outdated statistics requiring qualification
5. Insufficient methodology documentation
6. Missing framework development rationale

## Related GitHub Issues

| Priority | Issue | Title |
|----------|-------|-------|
| P0 | #319 | Remove Section 5 (Proposed Solution) |
| P0 | #317 | Remove Section 6 (Evaluation) |
| P0 | #315 | Revise Section 4.7: remove speculative market claims |
| P0 | #312 | Add search strategy table |
| P0 | #311 | Add simplified literature flow diagram |
| P0 | #310 | Qualify [A10] turnover data with caveat |
| P0 | #324 | Revise COI statement |
| P1 | #321 | Add Framework Development and Validation section |
| P1 | #320 | Revise conclusion: focus on framework contribution |
| P1 | #318 | Remove promotional language |
| P1 | #316 | Add research caveat to Section 4.7 |
| P1 | #313 | Document single-coder limitation |
| P2 | #322 | Map framework to existing models (HIMSS AMAM, DIKW) |
| P2 | #314 | Consider OSF post-hoc registration |
| Doc | #323 | Solicit expert review (2-3 colleagues) |
| Doc | #270 | Submit Paper 1 preprint to arXiv |
| Doc | #271 | Archive Paper 1 on Zenodo |

## Functional Requirements

### FR-1: Content Removal
- Remove Section 5 (Proposed Solution) entirely
- Remove Section 6 (Evaluation) entirely
- Preserve removed content for Paper 2

### FR-2: Section 4.7 Revision
- Remove speculative market claims about vendor incentives
- Keep Watson Health [I9] and Haven [I10] as observed events only
- Add research caveat about causal mechanisms

### FR-3: Methodology Enhancement
- Add search strategy table with databases, terms, date ranges
- Create simplified literature selection flow diagram
- Document single-coder limitation
- Qualify [A10] turnover statistics with caveat language

### FR-4: Framework Documentation
- Add "Framework Development and Validation" section
- Map framework to HIMSS AMAM and DIKW hierarchy
- Revise conclusion to focus on framework contribution

### FR-5: Language Cleanup
- Remove all "strategic imperative" phrases (3 occurrences)
- Remove promotional/advocacy language throughout
- Revise COI statement for accuracy

### FR-6: Submission Preparation
- Prepare expert review checklist
- Prepare OSF post-hoc registration materials
- Prepare arXiv submission checklist
- Prepare Zenodo archive checklist

## Non-Functional Requirements

### NFR-1: Academic Rigor
- Maintain objective, scholarly tone throughout
- All claims must be evidence-based or qualified as speculation
- Proper acknowledgment of limitations

### NFR-2: Consistency
- Section numbering must be updated after removals
- Cross-references must be verified
- Citation format maintained ([A#], [I#])

### NFR-3: Validation
- All changes must pass `./validate_documentation.sh`
- Reference validation must pass
- PDF/HTML/DOCX generation must succeed

## Acceptance Criteria

- [ ] Paper contains no product recommendations or vendor mentions
- [ ] All statistics qualified appropriately
- [ ] Methodology section includes search strategy table and literature flow diagram
- [ ] Framework development process documented
- [ ] Three-pillar framework clearly articulated as novel contribution
- [ ] Limitations section addresses single-author bias
- [ ] Section 4.7 contains no speculative causal claims
- [ ] COI statement accurate
- [ ] No promotional language remains
- [ ] Conclusion emphasizes analytical framework value
- [ ] Submission materials prepared for arXiv, Zenodo, OSF, expert review
- [ ] All 17 GitHub issues closeable with commit references
