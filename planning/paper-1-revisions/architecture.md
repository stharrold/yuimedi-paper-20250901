# Architecture: Paper-1 Revisions

## Overview

This feature involves editing documentation files (primarily `paper.md`) and creating new supporting materials. No code architecture changes are required.

## Files Modified

### Primary File
- **`paper.md`** - Major structural and content edits across all phases

### New Files Created

| File | Purpose |
|------|---------|
| `figures/literature-flow.mmd` | Mermaid source for literature selection diagram |
| `figures/literature-flow.jpg` | Generated JPG for paper inclusion |
| `ppr_review/expert-review-checklist.md` | Checklist for expert reviewers |
| `ppr_review/osf-registration-draft.md` | OSF post-hoc registration materials |
| `ppr_review/arxiv-submission-checklist.md` | arXiv submission preparation |
| `ppr_review/zenodo-submission-checklist.md` | Zenodo archive preparation |

## paper.md Structure Changes

### Before (Current)

```
1. Executive Summary
2. Introduction
3. Methodology
4. Literature Review (with Section 4.7: Why the Problem Persists)
5. Proposed Solution
6. Evaluation
7. Discussion
8. Conclusion
9. References
10. Appendices
```

### After (Target)

```
1. Executive Summary
2. Introduction
3. Methodology (enhanced with search table, flow diagram)
4. Framework Development and Validation (NEW)
5. Literature Review (Section 4.7 revised)
6. Discussion (reduced promotional content)
7. Conclusion (framework-focused)
8. References
9. Appendices
```

## Content Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        Phase 1: Removal                         │
│  ┌─────────────────┐     ┌─────────────────┐                   │
│  │   Section 5     │ --> │  Paper 2        │                   │
│  │ (Proposed Sol.) │     │  (preserved)    │                   │
│  └─────────────────┘     └─────────────────┘                   │
│  ┌─────────────────┐     ┌─────────────────┐                   │
│  │   Section 6     │ --> │  Paper 2        │                   │
│  │  (Evaluation)   │     │  (preserved)    │                   │
│  └─────────────────┘     └─────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────────┐
│                      Phase 2-5: Revision                        │
│  ┌─────────────────┐                                           │
│  │ Section 4.7     │ Remove speculation, add caveat            │
│  └─────────────────┘                                           │
│  ┌─────────────────┐                                           │
│  │ Methodology     │ + Search table, flow diagram, limitations │
│  └─────────────────┘                                           │
│  ┌─────────────────┐                                           │
│  │ Framework Dev   │ NEW: HIMSS AMAM/DIKW mapping             │
│  └─────────────────┘                                           │
│  ┌─────────────────┐                                           │
│  │ Conclusion      │ Framework-focused, no advocacy            │
│  └─────────────────┘                                           │
│  ┌─────────────────┐                                           │
│  │ Language        │ Remove "strategic imperative" x3          │
│  └─────────────────┘                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────────┐
│                   Phase 6: Submission Prep                      │
│  ppr_review/                                                    │
│  ├── expert-review-checklist.md                                │
│  ├── osf-registration-draft.md                                 │
│  ├── arxiv-submission-checklist.md                             │
│  └── zenodo-submission-checklist.md                            │
└─────────────────────────────────────────────────────────────────┘
```

## Dependencies

### Build Dependencies
- Mermaid CLI (`mmdc`) for figure generation
- Pandoc + XeLaTeX for PDF generation

### Validation Dependencies
- `./validate_documentation.sh` - 7 validation tests
- `python scripts/validate_references.py --all` - Reference validation
- `./scripts/build_paper.sh --format all` - Artifact generation

## Risk Considerations

### Content Preservation
Sections 5-6 will be removed but content is needed for Paper 2. Before deletion:
1. Content exists in git history
2. Revision strategy document references this split

### Reference Integrity
After section removal:
- Cross-references may break
- Section numbers will shift
- Validation script will catch issues

### Citation Consistency
The [A10] qualification will be applied at 5 locations - ensure consistent wording.
