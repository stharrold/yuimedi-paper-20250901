---
type: claude-context
directory: specs/interactive-paper-editor
purpose: Interactive paper editing session specification
parent: ../../CLAUDE.md
---

# CLAUDE.md - Interactive Paper Editor

## Context

This specification defines an interactive editing workflow for `paper.md`. Unlike typical features, this is a **documentation workflow** rather than code implementation.

## Quick Reference

```bash
# View paper sections
head -100 paper.md

# Run validation
./validate_documentation.sh

# Check references
python scripts/validate_references.py --all
```

## Key Files

- `spec.md` - Technical specification
- `plan.md` - Implementation plan with tasks
- `../../paper.md` - Primary document to edit
- `../../planning/interactive-paper-editor/` - BMAD planning documents

## Session Workflow

1. **Setup**: Load paper.md, check stats and git status
2. **Edit**: Navigate sections, apply changes, verify citations
3. **Validate**: Run full validation suite
4. **Commit**: Create descriptive commit message

## Citation Format

- Academic: `[A1]` through `[A30]`
- Industry: `[I1]` through `[I11]`

## Validation Gates

All must pass before commit:
- File size < 30KB
- Cross-references valid
- No duplicate content
- YAML structure valid
- Citation format correct
