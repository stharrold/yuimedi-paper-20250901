# Architecture: Remove Lee 2022 Reference

**Date:** 2025-12-14
**Issue:** #285
**Author:** stharrold

## Overview

This is a documentation-only change requiring careful coordination across multiple files. The primary change is removing reference [A8] and renumbering all subsequent academic references. No code changes are required.

## Components Affected

### 1. paper.md (Primary)

**Location:** `/Users/stharrold/Documents/GitHub/yuimedi-paper-20250901/paper.md`

**Changes:**

| Location | Change Type | Details |
|----------|------------|---------|
| Line 232 | Rewrite | Remove "and Lee et al. [A8]" from sentence |
| Line 756 | Delete | Remove [A8] reference definition |
| Lines 758-768 | Renumber | [A9]→[A8], [A10]→[A9], etc. |
| Lines 80, 96, 109, 226, 238, 272, 274, 539, 541, 610, 696 | Update | Update in-text citations |

### 2. CLAUDE.md

**Location:** `/Users/stharrold/Documents/GitHub/yuimedi-paper-20250901/CLAUDE.md`

**Changes:**
- Line 28: Update citation count to "24 verified citations (13 academic, 11 industry)"
- Line 33: Update citation history text

### 3. Documentation Files

| File | Changes |
|------|---------|
| `docs/citation-audit-report.md` | Remove [A8] from citation lists |
| `docs/validation_report.md` | Regenerate via script |
| `specs/fix-paper-references/reference_verification.md` | Remove [A8] section |
| `specs/fix-paper-references/claims_analysis.md` | Update [A8] references |

### 4. Generated Output Files

| File | Action |
|------|--------|
| `paper.pdf` | Regenerate |
| `paper.html` | Regenerate |
| `paper.docx` | Regenerate |
| `paper.tex` | Regenerate |

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
| 238 | [A9, A10] | [A8, A9] |
| 272 | [A11] | [A10] |
| 274 | [A12], [A13], [A14] | [A11], [A12], [A13] |
| 539 | [A9] | [A8] |
| 541 | [A10] | [A9] |
| 610 | [A9], [A10] | [A8], [A9] |
| 696 | [A11] | [A10] |

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

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Line number shifts during edits | Perform edits from bottom-to-top within each file |
| Missing citation updates | Use grep to find all occurrences before and after |
| Validation failures | Run validation after each major step |

## Execution Order

1. Edit paper.md (bottom-to-top):
   - Delete reference at line 756
   - Renumber references in References section
   - Update in-text citations (highest line numbers first)
   - Rewrite line 232
2. Update CLAUDE.md
3. Update documentation files
4. Regenerate output files
5. Run validation
