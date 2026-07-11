# Interactive Journal of Medical Research (i-JMR) Submission Checklist

**Article type:** Viewpoint
**Manuscript ID:** ms#96541 (R2 minor revision, Decision B 2026-07-07; transferred from JMIR Medical Informatics ms#91493)
**Revision due:** 2026-07-14 (extendable once)
**Date:** July 2026

## Quick Validation

```bash
# JMIR compliance (reports body count AND the authoritative JMIR-Method count)
uv run python scripts/validate_jmir_compliance.py --article-type viewpoint
# JMIR-Method count includes title + abstract + keywords + body incl. tables
# and figure captions + end matter; excludes only references, author
# metadata, figure content, appendices. Limit: 5,000 (Viewpoint).

# Reference validation (URLs) and DOI audit evidence
uv run python scripts/validate_references.py --all
uv run python scripts/audit_references.py --skip-landing

# Em-dash check (prohibited)
grep -n '—' paper.md

# Build all formats (includes both multimedia appendices)
./scripts/build_paper.sh --format all
```

## Manuscript Content (R2 state)

- [x] **Title**: "Healthcare Analytics Challenges: A Three-Pillar Framework Connecting Analytics Maturity, Workforce Agility, and Technical Enablement"
- [x] **Abstract**: Unstructured flowing narrative, 266/450 words
- [x] **Keywords**: 8 MeSH-aligned keywords
- [x] **Main Body**: Descriptive thematic headers (no "Methods" or "Results" per Viewpoint rules)
- [x] **Figures**: 2 figures (PNG), each with a numbered caption ("Figure N.") plus explanatory footnote paragraph (Reviewer T, R2)
- [x] **Tables**: 2 in-text tables with numbered captions above and bordered gridlines (editor, R2); full Three-Pillar rubric moved to Multimedia Appendix 2 for length
- [x] **Word count (JMIR method)**: 4,986 / 5,000 (was ~5,430 at R1 submission)

## Required End Sections

- [x] **Acknowledgments**: AI disclosure (Gemini CLI + Claude Code)
- [x] **Author Contributions**: CRediT taxonomy format
- [x] **Conflicts of Interest**: Dual affiliations disclosed (Yuimedi + Indiana University Health)
- [x] **Data Availability**: Narrative review statement
- [x] **Funding**: Yuimedi disclosed
- [x] **Abbreviations**: Complete, alphabetical

## Citations and References (R2 audit)

- [x] **Citation format**: Pandoc [@key] (AMA 11th edition via CSL); renders as numbered square brackets
- [x] **References**: 84 entries; every DOI registered at doi.org and matched to its Crossref record (title/authors/year/venue/pages)
- [x] **DOI audit**: 8 DOIs corrected, 6 added, 2 duplicates removed, 5 dead/weak sources removed or replaced, 9 author-name corrections (evidence: `bibliography-audit/`, issue #553)
- [x] **No legacy citations**: No [A#]/[I#] format

## File Inventory (package: `ARCHIVED/20260712_IJMR-Submission/`)

| File | Purpose |
|------|---------|
| `paper.docx` | Clean revised manuscript (section A upload) |
| `20260710_tracked-changes_R1-to-R2.docx` | Tracked changes vs R1 submission (section 3 upload) |
| `20260710_response-to-reviewers_sectionB-paste.txt` | Plain-text point-by-point (paste into section B) |
| `20260710_i-jmr-r2-response-to-reviewers.pdf` | Response letter PDF (section 3 upload) |
| `20260711_abstract-plaintext.txt` | Abstract for section D (Unstructured, 270 words) |
| `20260711_title-plaintext.txt` | Title for section D |
| `20260711_keywords-plaintext.txt` | Keywords for section D (semicolon-separated) |
| `figures/architecture.figure.png` | Figure 1 upload (1052x1200 px) |
| `figures/knowledge-cycle.figure.png` | Figure 2 upload (665x1200 px) |
| `figures/*.mmd.caption.txt` | Figure captions + footnotes for the form |
| `multimedia_appendix_1.pdf` + `.caption.txt` | Appendix 1: Validated Query Triple examples (unchanged) |
| `multimedia_appendix_2.pdf` + `.caption.txt` | NEW Appendix 2: full Three-Pillar Assessment Rubric |

## During Submission (i-JMR Resubmission Form)

https://www.i-jmr.org/author/submissionReview/96541

### Author Metadata (database drives final publication metadata, not the DOCX)
- [ ] **Corresponding Author**: Samuel T Harrold
- [ ] **Email**: samuel.harrold@yuimedi.com
- [ ] **ORCID**: 0009-0008-4596-6921
- [ ] **Affiliation**: Yuimedi, Inc., Indianapolis, IN, United States

### Article Metadata (section D)
- [ ] **Article Type**: Viewpoint
- [ ] **Title**: paste from `20260711_title-plaintext.txt`
- [ ] **Abstract**: set to Unstructured; paste from `20260711_abstract-plaintext.txt` (easy-to-miss field)
- [ ] **Keywords**: paste from `20260711_keywords-plaintext.txt`

### File Uploads
- [ ] **Revised Ms (section A)**: clean `paper.docx` (no tracked changes)
- [ ] **Figures (section 1)**: `architecture.figure.png`, `knowledge-cycle.figure.png` (max 1200x1200 px) with captions from the caption files
- [ ] **Multimedia Appendices (section 2)**: BOTH `multimedia_appendix_1.pdf` AND `multimedia_appendix_2.pdf` with their captions
- [ ] **Additional material (section 3)**: `20260710_tracked-changes_R1-to-R2.docx` + response letter PDF + TOC/feature image (`20260615_visual-abstract_toc-image.png`, unchanged from R1) + license/permission proof (`20260615_AJE_Terms-of-Service.pdf`, `20260115_AJE_Invoice_SL73WR5YH_redacted.png`) (no cover-letter slot on the revision form)
- [ ] **Editor notification (section B)**: paste `20260710_response-to-reviewers_sectionB-paste.txt` (plain text, no formatting)

## Pre-Send Verification (against the CI-committed paper.docx, not a local rebuild)

- [ ] Both in-text tables show gridlines in Word
- [ ] Captions read "Figure 1.", "Figure 2.", "Table 1.", "Table 2."
- [ ] Whole-document Word count minus reference list is under 5,000
- [ ] Multimedia Appendix 2 opens with three bordered rubric tables and a resolved numbered reference list
- [ ] Search "disclosure" and "financial" finds the AI-disclosure and funding statements

## Post-Submission

- [ ] **Verify** submission confirmation email; archive it in `ARCHIVED/20260712_IJMR-Submission/`
- [ ] **Rate reviewers** via the authorRating URLs in the decision letter
- [ ] **Release v4.0.0** (integrate -> release; Zenodo concept DOI 10.5281/zenodo.18264359 at the top of the notes; verify Zenodo archival)
- [ ] **Track** under the i-JMR R2 epic (#551 / milestone "i-JMR R2"); close #556 and the epic after submission
