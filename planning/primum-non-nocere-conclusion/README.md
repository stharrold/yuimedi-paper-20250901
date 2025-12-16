# Primum Non Nocere Conclusion Framework

**GitHub Issue:** [#293](https://github.com/stharrold/yuimedi-paper-20250901/issues/293)
**Status:** Planning Complete
**Created:** 2025-12-15

## Summary

This planning directory contains the implementation plan for integrating the healthcare mantra "First, do no harm" (*primum non nocere*) into the paper's conclusion section.

## Problem

The paper's current conclusion advocates for technology adoption without engaging with healthcare's legitimate concerns about caution and governance. The "First, do no harm" principle provides a rhetorical framework to address this tension.

## Solution

Reframe *primum non nocere* bidirectionally:
- **Traditional**: Risk of harm from premature technology adoption
- **Expanded**: Risk of harm from inaction (institutional memory loss, analytics gaps)

Position the three-pillar framework as a decision-support tool for organizations to evaluate both dimensions of harm.

## Files

| File | Description |
|------|-------------|
| `requirements.md` | Problem statement, acceptance criteria, risk assessment |
| `architecture.md` | Detailed structural changes to paper.md |
| `epics.md` | Task breakdown with implementation order |
| `CLAUDE.md` | Claude Code context for this directory |

## Implementation Summary

### Changes to paper.md Conclusion (Lines 702-740)

1. **Replace opening paragraph**: Remove advocacy language
2. **Add new section**: "The Dual Dimensions of Harm" (~200 words)
3. **Edit contributions #3**: Remove "strategic imperative" language
4. **Replace "Strategic Implications"**: New "Implications for Organizational Assessment"
5. **Replace "Call to Action"**: New "Future Research Directions" + "Closing Reflection"

### Estimated Impact
- Word count: +275 words to conclusion
- Tone: Advocacy → Evidence-based decision framework
- Alignment: Full compliance with Paper 1 revision strategy

## Quick Start

```bash
# Review the plan
cat planning/primum-non-nocere-conclusion/requirements.md
cat planning/primum-non-nocere-conclusion/architecture.md
cat planning/primum-non-nocere-conclusion/epics.md

# After implementation, validate
./validate_documentation.sh
python scripts/validate_references.py --all
./scripts/build_paper.sh --format all
```

## Related Documents

- Revision Strategy: `ppr_review/20251215_Revision-Strategy-Milestones.md`
- Journal Guide: `docs/journal-submission-guide.md`
- Paper Source: `paper.md` (lines 702-740)
