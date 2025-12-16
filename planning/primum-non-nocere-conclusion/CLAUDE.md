---
type: claude-context
directory: planning/primum-non-nocere-conclusion
purpose: Planning documents for integrating primum non nocere framework into paper conclusion
parent: ../CLAUDE.md
sibling_readme: README.md
---

# Claude Code Context: primum-non-nocere-conclusion

## Purpose

Planning documents for GitHub Issue #293: Integrate the healthcare mantra "First, do no harm" (*primum non nocere*) into the paper's conclusion to address the tension between technology adoption benefits and rejection-first governance approaches.

## Key Files

- `requirements.md` - Problem statement, rhetorical framework, acceptance criteria
- `architecture.md` - Detailed structural changes to paper.md conclusion
- `epics.md` - Task breakdown for implementation

## Quick Reference

### Core Concept

Transform "First, do no harm" from one-directional caution to **bidirectional harm assessment**:
1. Traditional: Risk of harm from premature adoption
2. Expanded: Risk of harm from **inaction** (memory loss, analytics gaps)

### Paper.md Lines to Update

| Section | Lines | Change Type |
|---------|-------|-------------|
| Conclusion opening | 704-706 | Replace (remove advocacy) |
| NEW: Dual Dimensions of Harm | After 706 | Insert (~200 words) |
| Summary of Contributions #3 | 714-716 | Edit (remove "strategic imperative") |
| Strategic Implications | 730-734 | Replace → "Implications for Assessment" |
| Call to Action | 735-740 | Replace → "Future Directions" + "Closing" |

### Key Revision Strategy Alignment

From `ppr_review/20251215_Revision-Strategy-Milestones.md`:
- Remove solution advocacy
- Remove promotional language ("strategic imperative", "call to action")
- Focus on three-pillar framework as decision-support tool

### Validation Commands

```bash
./validate_documentation.sh
python scripts/validate_references.py --all
./scripts/build_paper.sh --format all
```

## Related

- **GitHub Issue:** #293
- **Revision Strategy:** `ppr_review/20251215_Revision-Strategy-Milestones.md`
- **Journal Guide:** `docs/journal-submission-guide.md`
- **Parent:** [planning CLAUDE.md](../CLAUDE.md)
