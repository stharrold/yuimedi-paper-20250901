# JMIR Medical Informatics Submission Checklist

## Quick Validation

Run before submission to verify JMIR compliance:

```bash
python scripts/validate_jmir_compliance.py
```

Expected output: `✓ COMPLIANT - Ready for JMIR submission`

## Pre-Submission (Completed)

### Manuscript Content
- [x] **Title**: Descriptive, no results revealed, "Issue: Method" format
- [x] **Abstract**: 5-section structured (BOMRC), 289/450 words
- [x] **Keywords**: 8 keywords (5-10 required)
- [x] **Main Body**: IMRD structure (Introduction, Methodology, Literature Review, Discussion)
- [x] **Funding**: Section present
- [x] **Conflicts of Interest**: Section present (not "Competing Interests")
- [x] **Data Availability**: Section present
- [x] **Author Contributions**: Section present
- [x] **Abbreviations**: 17 abbreviations listed alphabetically
- [x] **AI Disclosure**: Gemini disclosed in Acknowledgments

### Citations & References
- [x] **Citation Format**: Pandoc [@key] format (186 citations)
- [x] **Citation Style**: AMA 11th edition via CSL
- [x] **Bibliography**: references.bib (108 unique references)
- [x] **No Legacy Citations**: No [A#]/[I#] format

### Figures
- [x] **Format**: PNG files (3 figures used in paper)
- [x] **Architecture diagram**: `figures/architecture.mmd.png`
- [x] **Knowledge cycle**: `figures/knowledge-cycle.mmd.png`
- [x] **Literature flow**: `figures/literature-flow.mmd.png`
- [ ] **Captions**: Verify captions in JMIR metadata system (sentence case, no "Figure X" prefix)
- [ ] **Upload**: Upload PNG files as supplementary figures in JMIR system

### Cover Letter
- [x] **Created**: submission/cover-letter.md
- [x] **Content**: Background, methodology, findings, COI, AI disclosure, APF acknowledgment, transfer preference

## During Submission (JMIR System)

### Author Metadata
- [ ] **Corresponding Author**:
  - Full name: Samuel T Harrold
  - Email: samuel.harrold@yuimedi.com
  - Telephone: [Enter]
  - Full address: [Enter]
- [ ] **ORCID**: [Enter ORCID if available]
- [ ] **Highest Academic Degree**: [Enter]
- [ ] **Affiliation**: Yuimedi, Inc., [City], [Country]

### Article Metadata
- [ ] **Article Type**: Select "Review"
- [ ] **Title**: Copy from paper.md YAML
- [ ] **Abstract**: Copy 5-section abstract from paper.md
- [ ] **Keywords**: healthcare analytics; natural language processing; SQL generation; institutional memory; conversational AI; healthcare informatics; workforce turnover; analytics maturity

### File Uploads
- [ ] **Manuscript**: Upload paper.docx (generated from paper.md)
- [ ] **Figures**: Upload each PNG as Figure type
- [ ] **Cover Letter**: Paste content from submission/cover-letter.md

### Optional Uploads
- [ ] **TOC Image**: Create and upload (300x225 to 1200x900 pixels, PNG)
- [ ] **Multimedia Appendix**: Not required for this narrative review

## Post-Acceptance (If Accepted)

- [ ] **License to Publish**: Sign and upload
- [ ] **Copyediting**: Respond to copyeditor queries
- [ ] **Proofreading**: Review final proof
- [ ] **APF Payment**: Process article processing fee

## Notes

### Article Type Justification
This is a **narrative literature review** (not systematic review), which:
- Synthesizes evidence across multiple domains
- Presents an original analytical framework
- Does not require PRISMA checklist (narrative reviews exempt)
- Uses IMRD structure as required for Review articles

### Word Count
Current manuscript exceeds 10,000 words. Per JMIR policy, additional editorial fees may apply. Author has acknowledged this in the cover letter.

### Preprint
Consider posting to arXiv (cs.CL, cross-list cs.DB, cs.HC) before or after submission.
