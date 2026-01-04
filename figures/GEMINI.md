---
type: gemini-context
directory: figures
purpose: Figure assets for research paper - Mermaid/DOT sources and generated outputs
parent: ../GEMINI.md
sibling_readme: null
children:
- ARCHIVED/GEMINI.md
---

# GEMINI.md

This file provides guidance to Gemini (Gemini) when working with code in this repository.

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

## Publication-Ready Outputs

For academic journal submission, optimized versions are generated from VS Code Mermaid Preview SVG exports:

| File | Size | Description |
|------|------|-------------|
| `literature-flow.mmd.vmp.svg` | ~518KB | Original VS Code Mermaid Preview export |
| `literature-flow.mmd.vmp.clean.svg` | ~42KB | Optimized: FA CSS removed, grayscale |
| `literature-flow.mmd.vmp.300dpi.png` | ~423KB | 300 DPI raster for standard print |
| `literature-flow.mmd.vmp.600dpi.png` | ~632KB | 600 DPI raster for high-quality print |
| `literature-flow.mmd.vmp.pdf` | ~79KB | Vector PDF for publication |

### Optimization Script

```bash
# Generate optimized SVG (grayscale, Font Awesome CSS removed)
python scripts/optimize_svg_for_publication.py figures/literature-flow.mmd.vmp.svg figures/literature-flow.mmd.vmp.clean.svg

# Generate high-resolution PNG (requires sharp-cli)
npx --yes sharp-cli -i figures/literature-flow.mmd.vmp.clean.svg --density 300 -o figures/literature-flow.mmd.vmp.300dpi.png
npx --yes sharp-cli -i figures/literature-flow.mmd.vmp.clean.svg --density 600 -o figures/literature-flow.mmd.vmp.600dpi.png

# Generate vector PDF (requires librsvg2-bin in container)
podman-compose run --rm dev bash -c "apt-get install -y -qq librsvg2-bin && rsvg-convert -f pdf -o figures/literature-flow.mmd.vmp.pdf figures/literature-flow.mmd.vmp.clean.svg"
```

## Git Tracking

- **Tracked:** `.mmd`, `.dot`, `.png`, `.jpg`, `.svg`, `.pdf` (sources and outputs)

## Related Documentation

- **[../GEMINI.md](../GEMINI.md)** - Parent directory: Root

**Child Directories:**
- **[ARCHIVED/GEMINI.md](ARCHIVED/GEMINI.md)** - Archived
