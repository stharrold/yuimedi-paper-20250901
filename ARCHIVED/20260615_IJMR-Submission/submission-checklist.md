# Interactive Journal of Medical Research (i-JMR) Submission Checklist

**Article type:** Viewpoint
**Manuscript ID:** ms#96541 (R1 major revision; transferred from JMIR Medical Informatics ms#91493)
**Date:** June 2026

## Quick Validation

```bash
# JMIR compliance
uv run python scripts/validate_jmir_compliance.py --article-type viewpoint

# Word count (JMIR method: body through abbreviations, excludes refs + metadata)
cat paper.md | sed '1,/^---$/d' | sed '/^# References/,$d' | wc -w
# Limit: 5,000 (strongly recommended for Viewpoints)

# Reference validation
uv run python scripts/validate_references.py --all

# Em-dash check (prohibited)
grep -n '—' paper.md

# Build all formats
./scripts/build_paper.sh --format all
```

## Manuscript Content

- [x] **Title**: "Healthcare Analytics Challenges: A Three-Pillar Framework Connecting Analytics Maturity, Workforce Agility, and Technical Enablement"
- [x] **Abstract**: Unstructured flowing narrative, ~310/450 words
- [x] **Keywords**: 8 MeSH-aligned keywords
- [x] **Main Body**: Descriptive thematic headers (no "Methods" or "Results" per Viewpoint rules)
- [x] **Figures**: 2 figures (PNG, grayscale, accessible alt text)
- [x] **Tables**: 2 tables (Table 1: Framework alignment, Table 2: Three-Pillar Rubric)
- [x] **Word count**: ~4,952 / 5,000

## Required End Sections

- [x] **Acknowledgments**: AI disclosure (Gemini CLI + Claude Code)
- [x] **Author Contributions**: CRediT taxonomy format
- [x] **Conflicts of Interest**: Dual affiliations disclosed (Yuimedi + Indiana University Health)
- [x] **Data Availability**: Narrative review statement (includes academic theses)
- [x] **Funding**: Yuimedi disclosed
- [x] **Abbreviations**: 13 abbreviations listed alphabetically

## Citations and References

- [x] **Citation format**: Pandoc [@key] (AMA 11th edition via CSL)
- [x] **References**: 76 entries, all with URLs
- [x] **No legacy citations**: No [A#]/[I#] format
- [x] **Broken URL fix**: nashid2023 updated, kalyanasundaram2025 allowlisted

## File Inventory

| File | Purpose | Format |
|------|---------|--------|
| `paper.md` | Manuscript source | Markdown |
| `paper.pdf` | Manuscript PDF | PDF (272K) |
| `paper.docx` | Manuscript for JMIR upload | DOCX (208K) |
| `paper.html` | Manuscript HTML | HTML (312K) |
| `cover-letter.md` | Resubmission cover letter | Markdown |
| `figures/architecture.mmd.png` | Figure 1: HITL-KG Architecture | PNG |
| `figures/knowledge-cycle.mmd.png` | Figure 2: Validated Query Cycle | PNG |
| `multimedia_appendix_1.pdf` | Multimedia Appendix 1: Validated Query Triple Examples | PDF |
| `references.bib` | Bibliography | BibTeX |

## During Submission (i-JMR Resubmission Form)

### Author Metadata
- [ ] **Corresponding Author**: Samuel T Harrold
- [ ] **Email**: samuel.harrold@yuimedi.com
- [ ] **ORCID**: 0009-0008-4596-6921
- [ ] **Highest Academic Degree**: [Enter]
- [ ] **Affiliation**: Yuimedi, Inc., Indianapolis, IN, United States

### Article Metadata
- [ ] **Section**: Select "Advanced Data Analytics in eHealth"
- [ ] **Article Type**: Select "Viewpoint"
- [ ] **Title**: Copy from paper.md YAML frontmatter
- [ ] **Abstract**: Copy unstructured abstract from paper.md
- [ ] **Keywords**: institutional amnesia; medical informatics; socio-technical systems; query governance; natural language processing; knowledge management; personnel turnover; organizational resilience

### File Uploads
- [ ] **Manuscript (section A)**: Upload clean `paper.docx` (no tracked changes)
- [ ] **Figures (section 1)**: Upload each PNG as Figure type
- [ ] **Multimedia Appendix (section 2)**: Upload `multimedia_appendix_1.pdf`
- [ ] **Additional material (section 3)**: Upload the tracked-changes manuscript and the point-by-point response-to-reviewers PDF (the i-JMR revision form has no cover-letter slot)
- [ ] **Editor notification (section B)**: Paste the plain-text point-by-point response

### Response-to-Reviewers Notes
- References ms#96541 (R1 major revision, Decision D)
- Point-by-point response entered in the editor notification (section B) and uploaded as a PDF in section 3
- Discloses AI tools used
- Notes prescriptive Viewpoint stance

## Post-Submission

- [ ] **Verify** submission confirmation email
- [ ] **Monitor** i-JMR submission portal for editor/reviewer assignment
- [ ] **Track** under the i-JMR R1 epic (GitHub issue #529 / milestone "i-JMR R1"); issue #506 is retired/superseded by the i-JMR transfer
