# Requirements: Remove Lee 2022 Reference

**Date:** 2025-12-14
**Issue:** #285
**Author:** stharrold

## Business Context

### Problem Statement

GitHub Issue #285 identifies that reference [A8] (Lee 2022 - "Medical entity recognition and SQL query generation using semantic parsing for electronic health records") is an incorrect reference that needs to be removed from the paper to maintain academic integrity.

### Primary Users

- Researchers reviewing the paper
- Journal reviewers evaluating citation accuracy
- Readers following reference links

### Success Criteria

- Reference [A8] completely removed from paper
- All subsequent academic references renumbered sequentially
- All validation tests pass
- Documentation updated to reflect correct citation count

## Functional Requirements

### FR-001: Remove In-Text Citation
- **Priority:** High
- **Description:** Remove the [A8] citation from line 232 of paper.md, rewriting the sentence to flow naturally with only Wang et al. [A5].
- **Acceptance Criteria:**
  - Sentence reads naturally without mentioning Lee et al.
  - Wang et al. [A5] remains as the sole citation

### FR-002: Delete Reference Definition
- **Priority:** High
- **Description:** Delete the [A8] reference definition from line 756 of paper.md.
- **Acceptance Criteria:**
  - Reference entry completely removed
  - No orphaned reference marker

### FR-003: Renumber Academic References
- **Priority:** High
- **Description:** Renumber academic references [A9] through [A14] to [A8] through [A13].
- **Acceptance Criteria:**
  - Sequential numbering [A1]-[A13] with no gaps
  - Both reference definitions and in-text citations updated

### FR-004: Update Citation Count
- **Priority:** Medium
- **Description:** Update CLAUDE.md citation count from "22 (11 academic, 11 industry)" to "24 (13 academic, 11 industry)".
- **Acceptance Criteria:**
  - CLAUDE.md reflects accurate post-removal count
  - Citation history updated

### FR-005: Update Documentation Files
- **Priority:** Medium
- **Description:** Update all documentation files referencing [A8].
- **Acceptance Criteria:**
  - docs/citation-audit-report.md updated
  - specs/fix-paper-references/reference_verification.md updated
  - specs/fix-paper-references/claims_analysis.md updated

### FR-006: Regenerate Output Files
- **Priority:** Medium
- **Description:** Regenerate PDF, HTML, DOCX, and TEX output files.
- **Acceptance Criteria:**
  - All output files reflect updated references
  - No rendering errors

### FR-007: Pass Validation
- **Priority:** High
- **Description:** Ensure all validation tests pass after changes.
- **Acceptance Criteria:**
  - `./validate_documentation.sh` exits with code 0
  - `python scripts/validate_references.py --check-citations` exits with code 0

## Non-Functional Requirements

### Performance
- Standard validation runtime (< 30 seconds)

### Security
- No security implications (documentation-only changes)

### Scalability
- Not applicable

## Constraints

- Must perform edits from bottom-to-top to avoid line number shift issues
- Python stdlib only for scripts (no external packages)
- All remaining citations must be DOI-verified

## Assumptions

- Current paper.md has 25 total references (14 academic + 11 industry)
- After removal: 24 total references (13 academic + 11 industry)
