# Interactive Journal of Medical Research (i-JMR) Submission Archive

**Date:** 2026-06-15
**Manuscript ID:** ms#96541 (R1, major revision)
**Article type:** Viewpoint
**Journal:** Interactive Journal of Medical Research (i-JMR)
**Version:** 3.0.0

## Title

Healthcare Analytics Challenges: A Three-Pillar Framework Connecting Analytics Maturity, Workforce Agility, and Technical Enablement

## Author

Samuel T Harrold, Yuimedi, Inc.
ORCID: 0009-0008-4596-6921

## Submission History

- **2026-01-15:** Original submission to JMIR Medical Informatics as Original Paper (~12,730 words)
- **2026-01-20:** Rejected for length
- **2026-03-29:** Resubmission to JMIR Medical Informatics as Viewpoint (~4,952 words; ms#91493)
- **2026-04-17:** Decision E2 (desk-reject before peer review): "low impact" + methodological weaknesses
- **2026-04-19:** Transfer/reinstatement requested
- **2026-04-22:** Transfer to Interactive Journal of Medical Research (i-JMR) chosen; manuscript becomes ms#96541
- **2026-06-05:** Decision D (major revision and re-review) returned after external peer review (editor: Matthew Balcarras); two reviewers (Q and T). Revision due 2026-07-03
- **2026-06-15:** R1 revision archived here (this snapshot)

## Manuscript Metrics

| Metric | Value |
|--------|-------|
| Body word count (JMIR method) | 4,532 / 5,000 |
| Abstract word count | 304 / 450 |
| Keywords | 8 |
| References | 89 |
| Figures | 2 |
| Tables | 2 |
| Multimedia appendices | 1 |
| JMIR compliance | Pass |

## What Changed in R1

This revision addresses all editor and reviewer comments from Decision D. The
point-by-point response is in `20260607_response-to-reviewers.md`; the original
decision letter is `20260605_Editor-Decision-D_Major-Revisions.pdf`.

### Editor (formatting/content)
- In-text citations converted to numbered square brackets (`[1]`, `[2,3]`); no
  author-year, round brackets, or superscripts.
- Headings unnumbered; the three italic Pillar sub-table titles converted to
  proper subheadings (no italics in place of subheadings).
- Funding statement added as a section distinct from Acknowledgments.
- Generative-AI disclosure included in the manuscript.
- Engagement with recent (2021-2026) peer-reviewed literature substantially
  increased.

### Reviewer Q
1. Self-selection-bias caveat added to the Analytics Maturity evidence; all
   domain acronyms defined at first use plus a completed Abbreviations list.
2. Scope-conditions paragraph added (query-reuse evidence: Jindal 2019, Kul 2018)
   answering the "50 queries" objection.
3. Empirical human-in-the-loop efficacy evidence added (Gartlehner 2025: 91.0% vs
   89.0%; Benzarti 2026: +28.4%; Ning 2024 as balancing evidence).
4. Limitations paragraph added on data drift, training, and analytics literacy.
5. Acronyms clarified (see comment 1).
6. Aging references replaced with 2021-2025 evidence; the single 2004 study now
   appears once, framed as a historical benchmark.

### Reviewer T
1. Explicit, cited definitions added for analytics maturity, workforce agility,
   and technical enablement at the head of each evidence pillar.
2. Redundant CIO-tenure / turnover statistics consolidated to a single mention.
3. Figure 1 revised with an Organizational Memory to Knowledge Base feedback edge
   (step 8, "Curates best practices") to depict continuous learning.
4. The 2004 statistic removed from the workforce section; contemporary evidence used.
5. Complete bibliographic details (volume, issue, pages, DOI) supplied; Ang &
   Slaughter (2004) completed to 35(3):11-27.

## File Inventory

### Manuscript
| File | Description |
|------|-------------|
| `paper.md` | Source (Markdown + pandoc-citeproc) |
| `paper.pdf` | PDF output |
| `paper.docx` | Word output for i-JMR upload ("Revised Ms", clean) |
| `paper.html` | HTML output |
| `paper.tex` | LaTeX output |

### i-JMR Correspondence and Response
| File | Description |
|------|-------------|
| `20260605_Editor-Decision-D_Major-Revisions.pdf` | Editor decision letter + both reviewer reports |
| `20260607_response-to-reviewers.md` | Point-by-point response (paste-ready, plain text) |
| `cover-letter.md` / `.docx` / `.pdf` | Cover letter |
| `submission-checklist.md` | JMIR submission checklist |

### Supporting Files
| File | Description |
|------|-------------|
| `metadata.yaml` | Pandoc metadata for PDF generation |
| `references.bib` | BibTeX bibliography (89 entries) |
| `citation-style-ama.csl` | AMA 11th edition style, customized for `[N]` in-text rendering |
| `reference.docx` | Custom Word template (Times New Roman 12pt, double-spaced) |

### Figures
| File | Description |
|------|-------------|
| `figures/architecture.mmd` (+ `.png`, `.svg`, `.caption.txt`) | Figure 1: HITL-KG Architecture (with R1 step-8 feedback loop) |
| `figures/knowledge-cycle.mmd` (+ `.png`, `.svg`, `.caption.txt`) | Figure 2: Validated Query Cycle |
| `figures/mermaid-styles.css` | Mermaid theme styles |
| `figures/puppeteer-config.json` | Puppeteer config for figure rendering |

### Multimedia Appendix
| File | Description |
|------|-------------|
| `multimedia_appendix_1.md` (+ `.pdf`, `.html`, `.docx`, `.caption.txt`) | Validated Query Triple examples + Externalization process |

### Build Infrastructure
| File | Description |
|------|-------------|
| `build_paper.sh` | Build script (pandoc pipeline) |
| `Containerfile` | Container with Python 3.12, pandoc, texlive |
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
uv sync
./build_paper.sh --format all
# Or use the container:
podman build -t yuimedi-paper -f Containerfile .
podman run --rm -v "$(pwd)":/app -v yuimedi_venv_cache:/app/.venv -w /app yuimedi-paper ./build_paper.sh --format all
```

## Submission Actions (author)

At https://www.i-jmr.org/author/submissionReview/96541, before 2026-07-03:
1. Upload the clean `paper.docx` under "Revised Ms".
2. Attach a tracked-changes version as a supplementary file (Word Review to Compare
   against the pre-revision DOCX in `../20260329_JMIR-Submission/`).
3. Paste `20260607_response-to-reviewers.md` into the editor notification (plain
   text, no formatting).

## Key Framework Contributions

1. **HITL-KG** (Human-in-the-Loop Knowledge Governance): Socio-technical governance framework
2. **Validated Query Triple**: NL Intent + Executable SQL + Rationale Metadata
3. **Three-Pillar Assessment Rubric**: 9 indicators across Analytics Maturity, Workforce Agility, Technical Enablement
4. **Knowledge Ratchet**: Lean Standard Work mechanism preventing knowledge regression
5. **Three-tier validation governance**: Full / Constrained / Automated matching
6. **Golden Queries**: Certified authoritative data definitions
7. **Continuous Analytic Integration**: CI/CD for validated query triples
