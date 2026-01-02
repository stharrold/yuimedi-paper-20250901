---
type: claude-context
directory: docs
purpose: Documentation artifacts including guides, reports, research notes, and reference materials
parent: ../GEMINI.md
sibling_readme: README.md
---

# Gemini Context Context: docs

## Purpose

Documentation directory containing how-to guides, analysis reports, research notes, and reference materials.

## Structure

```
docs/
├── guides/           # How-to documentation
├── reports/          # Analysis and audit reports
├── research/         # Literature review findings (38 files)
└── references/       # Source PDFs (git-crypt encrypted)
```

## Contents

| Directory | Purpose | Contents |
|-----------|---------|----------|
| `guides/` | How-to documentation | Journal submission, PDF generation, lit_review setup |
| `reports/` | Analysis reports | Citation audit, PRISMA assessment, validation |
| `research/` | Research findings | 38 research question notes with citations |
| `references/` | Source PDFs | 23 reference PDFs (encrypted at rest) |

## Primary Paper Files (in root directory)

- `paper.md` - Source document
- `paper.pdf` - PDF output
- `paper.html` - HTML output
- `paper.docx` - Word output
- `paper.tex` - LaTeX output

## Related

- **Parent**: [Root GEMINI.md](../GEMINI.md)
- **Sibling**: [README.md](README.md)
