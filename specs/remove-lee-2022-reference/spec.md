# Specification: Remove Lee 2022 Reference

**Type:** feature
**Slug:** remove-lee-2022-reference
**Date:** 2025-12-14
**Author:** stharrold
**Issue:** #285

## Overview

Remove incorrect reference [A8] (Lee 2022 - "Medical entity recognition and SQL query generation using semantic parsing for electronic health records") from paper.md and renumber all subsequent academic references to maintain sequential numbering. This is a documentation-only change to maintain academic integrity.

## Implementation Context

**GitHub Issue:** #285

**BMAD Planning:** See `planning/remove-lee-2022-reference/` for complete requirements and architecture.

**Implementation Preferences:**

- **Task Granularity:** Small tasks (1-2 hours each)
- **Follow Epic Order:** True
- **Execution Order:** Bottom-to-top within each file to avoid line number shift issues

## Requirements Summary

### Functional Requirements

| ID | Description | Priority |
|----|-------------|----------|
| FR-001 | Remove [A8] citation from line 232 in paper.md | High |
| FR-002 | Delete [A8] reference definition from line 756 | High |
| FR-003 | Renumber [A9]-[A14] → [A8]-[A13] | High |
| FR-004 | Update CLAUDE.md citation count to "24 (13 academic, 11 industry)" | Medium |
| FR-005 | Update documentation files referencing [A8] | Medium |
| FR-006 | Regenerate PDF, HTML, DOCX, TEX output files | Medium |
| FR-007 | Pass all validation tests | High |

## Reference Renumbering Map

| Before | After | Reference |
|--------|-------|-----------|
| [A1] | [A1] | Wu et al. (2024) |
| [A2] | [A2] | Ren et al. (2024) |
| [A3] | [A3] | Lee, G. et al. (2023) |
| [A4] | [A4] | Navarro et al. (2023) |
| [A5] | [A5] | Wang et al. (2020) |
| [A6] | [A6] | Ziletti & D'Ambrosi (2024) |
| [A7] | [A7] | Kamble et al. (2019) |
| [A8] | **REMOVED** | Lee et al. (2022) |
| [A9] | [A8] | MedAgentBench (2024) |
| [A10] | [A9] | Chen et al. (2024) |
| [A11] | [A10] | Ang & Slaughter (2004) |
| [A12] | [A11] | Ledikwe et al. (2013) |
| [A13] | [A12] | Mantas et al. (2010) |
| [A14] | [A13] | Musa et al. (2023) |

## In-Text Citation Updates

| Line | Current | New |
|------|---------|-----|
| 80 | [A11] | [A10] |
| 96 | [A11] | [A10] |
| 109 | [A11] | [A10] |
| 226 | [A9, A10] | [A8, A9] |
| 232 | [A5] and [A8] | [A5] only |
| 238 | [A9, A10] | [A8, A9] |
| 272 | [A11] | [A10] |
| 274 | [A12], [A13], [A14] | [A11], [A12], [A13] |
| 539 | [A9] | [A8] |
| 541 | [A10] | [A9] |
| 610 | [A9], [A10] | [A8], [A9] |
| 696 | [A11] | [A10] |

## Files to Modify

### Primary File

**File:** `paper.md`

**Changes:**
1. Line 232: Rewrite sentence to remove "and Lee et al. [A8]"
2. Line 756: Delete [A8] reference definition
3. Lines 758-768: Renumber reference definitions
4. Various lines: Update in-text citations per table above

### Metadata File

**File:** `CLAUDE.md`

**Changes:**
- Line 28: Update count to "24 verified citations (13 academic, 11 industry)"
- Line 33: Update citation history

### Documentation Files

| File | Changes |
|------|---------|
| `docs/citation-audit-report.md` | Remove [A8] from citation lists |
| `specs/fix-paper-references/reference_verification.md` | Remove [A8] section |
| `specs/fix-paper-references/claims_analysis.md` | Update [A8] references |

### Generated Output Files

| File | Action |
|------|--------|
| `paper.pdf` | Regenerate via `./scripts/build_paper.sh` |
| `paper.html` | Regenerate |
| `paper.docx` | Regenerate |
| `paper.tex` | Regenerate |

## Validation Strategy

### Pre-Implementation

```bash
# Verify current state
./validate_documentation.sh
python scripts/validate_references.py --all
```

### Post-Implementation

```bash
# Verify changes
./validate_documentation.sh                    # Must pass all 7 tests
python scripts/validate_references.py --all   # Regenerates validation_report.md
python scripts/validate_references.py --check-citations  # No orphaned citations
```

## Constraints

- Must perform edits from bottom-to-top to avoid line number shift issues
- Python stdlib only for scripts (no external packages)
- All remaining citations must be DOI-verified

## Success Criteria

- [ ] Reference [A8] completely removed from paper
- [ ] All subsequent academic references renumbered sequentially [A1]-[A13]
- [ ] All in-text citations updated correctly
- [ ] CLAUDE.md reflects accurate post-removal count (24 citations)
- [ ] All validation tests pass (7/7)
- [ ] Output files (PDF, HTML, DOCX, TEX) regenerated successfully
