# JMIR Medical Informatics Submission Checklist

**Article type:** Viewpoint
**Manuscript ID:** ms#91493 (resubmission)
**Date:** March 2026

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
| `multimedia_appendix_1.pdf` | Multimedia Appendix 1 | PDF |
| `multimedia_appendix_2.pdf` | Multimedia Appendix 2 | PDF |
| `references.bib` | Bibliography | BibTeX |

## During Submission (JMIR System)

### Author Metadata
- [ ] **Corresponding Author**: Samuel T Harrold
- [ ] **Email**: samuel.harrold@yuimedi.com
- [ ] **ORCID**: [Enter]
- [ ] **Highest Academic Degree**: [Enter]
- [ ] **Affiliation**: Yuimedi, Inc., Indianapolis, IN, United States

### Article Metadata
- [ ] **Article Type**: Select "Viewpoint"
- [ ] **Title**: Copy from paper.md YAML frontmatter
- [ ] **Abstract**: Copy unstructured abstract from paper.md
- [ ] **Keywords**: institutional amnesia; medical informatics; socio-technical systems; query governance; natural language processing; knowledge management; personnel turnover; organizational resilience

### File Uploads
- [ ] **Manuscript**: Upload `paper.docx`
- [ ] **Figures**: Upload each PNG as Figure type
- [ ] **Cover Letter**: Paste content from `cover-letter.md`
- [ ] **Multimedia Appendices**: Upload `multimedia_appendix_1.pdf` and `multimedia_appendix_2.pdf`

### Cover Letter Notes
- References ms#91493 (resubmission)
- Explains conversion from Original Paper to Viewpoint per editor guidance
- Discloses AI tools used
- Notes prescriptive Viewpoint stance

## Post-Submission

- [ ] **Verify** submission confirmation email
- [ ] **Monitor** JMIR submission portal for reviewer assignment
- [ ] **Track** in GitHub issue #506
