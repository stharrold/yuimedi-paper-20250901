---
type: claude-context
directory: figures
purpose: Figure assets for research paper - Mermaid/DOT sources and generated outputs
parent: ../CLAUDE.md
sibling_readme: null
children: null
---

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Directory Purpose

Figure assets for the research paper. Contains source files (Mermaid, DOT) and generated outputs (SVG, PNG, JPG).

## File Naming Convention

Hierarchical naming shows derivation relationships:

```
<name>.mmd                    ← Mermaid source (source of truth)
├── <name>.mmd.svg            ← derived from .mmd
├── <name>.mmd.png            ← derived from .mmd
└── <name>.mmd.dot            ← DOT source (alternate format)
    ├── <name>.mmd.dot.svg    ← derived from .dot
    └── <name>.mmd.dot.png    ← derived from .dot
```

The suffix chain documents what generates what.

## Generation Commands

```bash
# Mermaid → SVG/PNG
npx --yes @mermaid-js/mermaid-cli@latest -i figures/<name>.mmd -o figures/<name>.mmd.svg
npx --yes @mermaid-js/mermaid-cli@latest -i figures/<name>.mmd -o figures/<name>.mmd.png

# DOT → SVG/PNG (requires graphviz, use container)
podman-compose run --rm dev dot -Tsvg figures/<name>.dot -o figures/<name>.dot.svg
podman-compose run --rm dev dot -Tpng figures/<name>.dot -o figures/<name>.dot.png

# PNG → JPG (for paper inclusion)
# macOS:
sips -s format jpeg figures/<name>.png --out figures/<name>.jpg && rm figures/<name>.png
# Linux/Container:
convert figures/<name>.png figures/<name>.jpg && rm figures/<name>.png
```

## Current Figures

| Source | Description |
|--------|-------------|
| `architecture.mmd` | Healthcare analytics architecture diagram |
| `literature-flow.mmd` | PRISMA 2020 literature selection flow |

## Git Tracking

- **Tracked:** `.mmd`, `.dot`, `.jpg`, `.svg` (sources and final outputs)
- **Ignored:** `.png` intermediates (per root `.gitignore`)
