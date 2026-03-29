# JMIR Medical Informatics Submission Archive

**Date:** 2026-03-29
**Manuscript ID:** ms#91493 (resubmission)
**Article type:** Viewpoint
**Journal:** JMIR Medical Informatics
**Version:** 2.0.0

## Title

Healthcare Analytics Challenges: A Three-Pillar Framework Connecting Analytics Maturity, Workforce Agility, and Technical Enablement

## Author

Samuel T Harrold, Yuimedi, Inc.
ORCID: 0009-0008-4596-6921

## Submission History

- **2026-01-15:** Original submission as Original Paper (~12,730 words)
- **2026-01-20:** Rejected for length (editor noted work was "interesting")
- **2026-03-29:** Resubmission as Viewpoint (~4,952 words)

## Manuscript Metrics

| Metric | Value |
|--------|-------|
| Word count (JMIR method) | ~4,952 / 5,000 |
| References | 73 |
| Figures | 2 |
| Tables | 2 |
| Multimedia appendices | 1 |
| JMIR compliance | Pass |

## File Inventory

### Manuscript
| File | Description |
|------|-------------|
| `paper.md` | Source (Markdown + pandoc-citeproc) |
| `paper.pdf` | PDF output (272K) |
| `paper.docx` | Word output for JMIR upload (204K) |
| `paper.html` | HTML output (312K) |
| `paper.tex` | LaTeX output (92K) |

### Supporting Files
| File | Description |
|------|-------------|
| `metadata.yaml` | Pandoc metadata for PDF generation |
| `references.bib` | BibTeX bibliography (73 entries) |
| `citation-style-ama.csl` | AMA 11th edition citation style |
| `reference.docx` | Custom Word template (Times New Roman 12pt, double-spaced) |
| `cover-letter.md` | Resubmission cover letter |
| `submission-checklist.md` | JMIR submission checklist |

### Figures
| File | Description |
|------|-------------|
| `figures/architecture.mmd` | Figure 1 source (Mermaid) |
| `figures/architecture.mmd.png` | Figure 1 rendered (HITL-KG Architecture) |
| `figures/architecture.mmd.svg` | Figure 1 vector |
| `figures/architecture.mmd.caption.txt` | Figure 1 caption |
| `figures/knowledge-cycle.mmd` | Figure 2 source (Mermaid) |
| `figures/knowledge-cycle.mmd.png` | Figure 2 rendered (Validated Query Cycle) |
| `figures/knowledge-cycle.mmd.svg` | Figure 2 vector |
| `figures/knowledge-cycle.mmd.caption.txt` | Figure 2 caption |
| `figures/mermaid-styles.css` | Mermaid theme styles |
| `figures/puppeteer-config.json` | Puppeteer config for figure rendering |

### Multimedia Appendix
| File | Description |
|------|-------------|
| `multimedia_appendix_1.md` | Source (Validated Query Triple examples) |
| `multimedia_appendix_1.pdf` | PDF output |
| `multimedia_appendix_1.html` | HTML output |
| `multimedia_appendix_1.docx` | Word output |
| `multimedia_appendix_1.caption.txt` | Caption |

### Build Infrastructure
| File | Description |
|------|-------------|
| `build_paper.sh` | Build script (pandoc pipeline) |
| `Containerfile` | Container with Python 3.11, pandoc, texlive |
| `pyproject.toml` | Python project config |
| `uv.lock` | Dependency lock file |

### Project Metadata
| File | Description |
|------|-------------|
| `CITATION.cff` | Citation metadata for Zenodo |
| `.zenodo.json` | Zenodo deposit metadata |
| `LICENSE` | Apache 2.0 |
| `NOTICE` | Copyright notice |

## Reproduction

To rebuild all artifacts from source:

```bash
# Install dependencies
uv sync

# Build all formats (requires pandoc + texlive)
./build_paper.sh --format all

# Or use container
podman build -t yuimedi-paper -f Containerfile .
podman run --rm -v "$(pwd)":/app -v yuimedi_venv_cache:/app/.venv -w /app yuimedi-paper ./build_paper.sh --format all
```

## Key Framework Contributions

1. **HITL-KG** (Human-in-the-Loop Knowledge Governance): Socio-technical governance framework
2. **Validated Query Triple**: NL Intent + Executable SQL + Rationale Metadata
3. **Three-Pillar Assessment Rubric**: 9 indicators across Analytics Maturity, Workforce Agility, Technical Enablement
4. **Knowledge Ratchet**: Lean Standard Work mechanism preventing knowledge regression
5. **Three-tier validation governance**: Full / Constrained / Automated matching
6. **Golden Queries**: Certified authoritative data definitions
7. **Continuous Analytic Integration**: CI/CD for validated query triples
