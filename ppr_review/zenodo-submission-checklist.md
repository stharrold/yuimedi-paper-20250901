# Zenodo Submission Checklist: Paper 1 - Three-Pillar Analytical Framework

## Overview

This checklist guides the Zenodo archive submission for Paper 1. Zenodo provides a DOI for the paper and supplementary materials, enabling formal citation.

**Purpose:**
- Archive paper with permanent DOI
- Enable citation in formats that require DOI
- Preserve supplementary materials (code, data, figures)
- Establish version history for the paper

---

## Pre-Submission Requirements

### 1. Account Setup
- [ ] Zenodo account created (https://zenodo.org)
- [ ] ORCID linked to Zenodo account
- [ ] GitHub integration enabled (optional, for automatic archiving)

### 2. DOI Reservation (Optional)
- [ ] Reserve DOI before submission if needed for cross-references
- [ ] Note: DOI is assigned automatically upon publication

---

## Deposit Preparation

### 3. Upload Type
- [ ] Select **"Publication"** as upload type
- [ ] Select **"Preprint"** as publication type

### 4. Files to Upload

**Required:**
- [ ] `paper.pdf` - Main manuscript PDF
- [ ] `LICENSE` - License file (CC BY 4.0)

**Recommended:**
- [ ] `paper.tex` - LaTeX source (if generated)
- [ ] `paper.md` - Markdown source
- [ ] `metadata.yaml` - Paper metadata

**Optional:**
- [ ] `figures/` - Directory with source figures (as ZIP)
- [ ] `ppr_review/` - Review materials (as ZIP)
- [ ] `README.md` - Repository documentation

**File Preparation:**
```bash
# Generate PDF
./scripts/build_paper.sh --format pdf

# Create supplementary ZIP
zip -r paper1-supplementary.zip figures/ ppr_review/ metadata.yaml README.md
```

---

## Metadata Entry

### 5. Basic Information

**Title:**
```
Three-Pillar Analytical Framework for Healthcare Analytics:
A Narrative Review of Natural Language to SQL, Analytics Maturity, and Workforce Turnover
```

**Authors:**
| Name | Affiliation | ORCID |
|------|-------------|-------|
| Samuel T Harrold | Indiana University Health; Yuimedi Corp. | [ORCID ID] |

**Description/Abstract:**
(Copy from paper.md metadata block)

**Version:** v1.0.0

**Publication Date:** [Submission date]

**Language:** English

### 6. License
- [ ] **CC BY 4.0** (Creative Commons Attribution 4.0 International)
- [ ] Verify consistency with repository LICENSE file
- [ ] Add license text or link in description if desired

### 7. Keywords
```
healthcare analytics
natural language processing
SQL generation
institutional memory
conversational AI
healthcare informatics
workforce turnover
analytics maturity
HIMSS AMAM
NL2SQL
```

### 8. Additional Identifiers

**DOI:** (Auto-assigned by Zenodo)

**arXiv ID:** (Add after arXiv submission)
```
arXiv:2512.XXXXX
```

**GitHub Repository:**
```
https://github.com/stharrold/yuimedi-paper-20250901
```

### 9. Related Identifiers

| Type | Identifier | Relation |
|------|------------|----------|
| GitHub | https://github.com/stharrold/yuimedi-paper-20250901 | isSupplementedBy |
| arXiv | arXiv:2512.XXXXX | isIdenticalTo |
| OSF | [OSF URL] | isDocumentedBy |

### 10. Funding
- [ ] Mark "No" if self-funded research
- [ ] Add funding acknowledgment if applicable

### 11. Communities (Optional)
Consider joining relevant Zenodo communities:
- [ ] Healthcare Informatics
- [ ] Natural Language Processing
- [ ] Health IT

---

## Access and Sharing

### 12. Access Rights
- [ ] Select **"Open Access"**
- [ ] This enables maximum visibility and citation

### 13. Embargo (if needed)
- [ ] Generally not needed for preprints
- [ ] May add embargo if journal submission requires it

---

## Submission Process

### 14. Save Draft
- [ ] Complete all metadata fields
- [ ] Upload all files
- [ ] Save as draft before publishing

### 15. Preview
- [ ] Review all metadata for accuracy
- [ ] Verify files uploaded correctly
- [ ] Check DOI preview

### 16. Publish
- [ ] Click "Publish" to make deposit public
- [ ] Note: Once published, DOI is permanent
- [ ] Note: Metadata can be edited, but files require new version

---

## Post-Submission

### 17. Record DOI
**Zenodo DOI:** 10.5281/zenodo.XXXXXXX

Update the following with DOI:
- [ ] GitHub repository README
- [ ] arXiv submission metadata
- [ ] OSF registration
- [ ] Paper PDF (if version update possible)
- [ ] ORCID profile

### 18. Citation Format
Zenodo generates citation in multiple formats. Verify:
- [ ] APA citation correct
- [ ] BibTeX entry complete
- [ ] DOI link resolves correctly

### 19. Badge (Optional)
Add Zenodo badge to GitHub README:
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

---

## Version Management

### 20. New Versions
When updating the paper:
- [ ] Use "New Version" button (not "Edit")
- [ ] Upload updated files
- [ ] Update version number (v1.0.0 → v1.1.0)
- [ ] Document changes in description
- [ ] Concept DOI remains stable across versions

### 21. Version Numbering Convention
- **v1.0.0** - Initial preprint
- **v1.1.0** - Minor revisions (e.g., typos, clarifications)
- **v2.0.0** - Major revisions (e.g., post peer review)

---

## Checklist Summary

### Before Publishing
- [ ] Account setup complete
- [ ] All files uploaded
- [ ] Title and abstract accurate
- [ ] Authors and affiliations correct
- [ ] Keywords appropriate
- [ ] License set to CC BY 4.0
- [ ] Access set to Open Access
- [ ] Related identifiers added (GitHub, arXiv if available)

### After Publishing
- [ ] DOI recorded
- [ ] Cross-references updated (arXiv, OSF, GitHub)
- [ ] Citation verified
- [ ] Badge added to repository

---

## Quick Reference

**Zenodo URL:** https://zenodo.org

**DOI prefix:** 10.5281/zenodo.

**Support:** https://zenodo.org/support

**API:** https://developers.zenodo.org/

---

**Last Updated:** 2025-12-16
