---
type: claude-context
directory: ARCHIVED/20260615_IJMR-Submission
purpose: Frozen snapshot of the i-JMR ms#96541 R1 (major revision) submission, 2026-06-15
parent: ../CLAUDE.md
sibling_readme: README.md
related_skills:
  - workflow-orchestrator
  - workflow-utilities
---

# Claude Code Context: 20260615_IJMR-Submission

## Purpose

Frozen snapshot of the Interactive Journal of Medical Research (i-JMR)
manuscript ms#96541 at the R1 major-revision stage (Decision D, returned
2026-06-05; revision due 2026-07-03). Captures the revised manuscript, all
build artifacts, the editor decision letter, and the point-by-point response
to reviewers, as submitted/prepared on 2026-06-15.

## Directory Structure

- Manuscript: `paper.md` (source) plus `paper.{pdf,docx,html,tex}` outputs
- i-JMR correspondence: `20260605_Editor-Decision-D_Major-Revisions.pdf`,
  `20260607_response-to-reviewers.md`, `cover-letter.{md,docx,pdf}`,
  `submission-checklist.md`
- Supporting: `metadata.yaml`, `references.bib` (89 entries),
  `citation-style-ama.csl` (customized for `[N]` bracket citations),
  `reference.docx`
- `figures/`: Figure 1 (architecture, with R1 step-8 feedback loop) and
  Figure 2 (knowledge-cycle), plus Mermaid render infrastructure
- `multimedia_appendix_1.*`: Validated Query Triple examples
- Build: `build_paper.sh`, `Containerfile`, `pyproject.toml`, `uv.lock`
- Project metadata: `CITATION.cff`, `.zenodo.json`, `LICENSE`, `NOTICE`

## Usage

This is an immutable archive. Do not edit files here; they record the R1
submission state. For ongoing work, edit the live files in the repository
root. See `README.md` for the full file inventory, R1 change summary, and
author submission steps.

## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
- **[../CLAUDE.md](../CLAUDE.md)** - Parent directory: ARCHIVED
- **[../20260329_JMIR-Submission/README.md](../20260329_JMIR-Submission/README.md)** - Prior submission (pre-transfer) snapshot

## Related Skills

- workflow-orchestrator
- workflow-utilities
