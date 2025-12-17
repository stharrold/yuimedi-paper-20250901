# arXiv Submission Checklist: Paper 1 - Three-Pillar Analytical Framework

## Overview

This checklist guides the arXiv preprint submission for Paper 1. arXiv is the primary preprint target (medRxiv is not eligible for narrative reviews).

**Target Categories:**
- **Primary:** cs.CL (Computation and Language)
- **Cross-list:** cs.DB (Databases), cs.HC (Human-Computer Interaction), cs.CY (Computers and Society)

---

## Pre-Submission Requirements

### 1. Author Registration
- [ ] arXiv account created and verified
- [ ] ORCID linked to arXiv account
- [ ] Institutional affiliation verified (if required)

### 2. Endorsement (if needed)
- [ ] Verified endorsement status for cs.CL
- [ ] Obtained endorsement from qualified researcher (if required)
- [ ] Note: First-time submitters to a category may need endorsement

---

## Manuscript Preparation

### 3. Format Requirements
- [ ] PDF generated from LaTeX or Pandoc
- [ ] File size under 10MB
- [ ] All fonts embedded (Type 1 fonts preferred)
- [ ] No missing figures or references

**Generate PDF:**
```bash
./scripts/build_paper.sh --format pdf
```

### 4. PDF Quality Check
- [ ] All figures render correctly
- [ ] Tables are legible
- [ ] References are formatted consistently
- [ ] Page numbers present
- [ ] No "DRAFT" watermarks

### 5. Metadata Preparation

**Title:**
```
Three-Pillar Analytical Framework for Healthcare Analytics:
A Narrative Review of Natural Language to SQL, Analytics Maturity, and Workforce Turnover
```

**Authors:**
```
Samuel T Harrold
```

**Abstract:** (Copy from paper.md metadata block, ~250 words max)

**Comments:** (Optional, for version notes)
```
Narrative review presenting novel analytical framework for healthcare analytics challenges.
41 sources reviewed (30 academic, 11 industry). Framework connects NL2SQL technology,
HIMSS analytics maturity model, and workforce turnover research.
```

**Report Number:** (Optional)
```
YuiQuery-Paper1-v1.0
```

**DOI:** (Leave blank until Zenodo DOI assigned)

**Journal Reference:** (Leave blank - this is a preprint)

---

## Category Selection

### 6. Primary Category
- [ ] **cs.CL** (Computation and Language)
  - Justification: Paper addresses NL2SQL technology for healthcare

### 7. Cross-List Categories (select all applicable)
- [ ] **cs.DB** (Databases)
  - Justification: NL2SQL and healthcare data warehouse topics
- [ ] **cs.HC** (Human-Computer Interaction)
  - Justification: Natural language interfaces for clinical users
- [ ] **cs.CY** (Computers and Society)
  - Justification: Workforce dynamics and organizational impacts

### 8. ACM Classification (Optional)
- [ ] H.2.3 (Languages - Query languages)
- [ ] J.3 (Life and Medical Sciences)
- [ ] K.6.1 (Project and People Management)

---

## License Selection

### 9. License
- [ ] **CC BY 4.0** (Recommended - allows reuse with attribution)
- [ ] Verify license is consistent with repository LICENSE file
- [ ] Note: This enables broad dissemination and citation

---

## Supporting Files

### 10. Source Files (Optional but recommended)
- [ ] paper.tex (LaTeX source if generated)
- [ ] figures/ directory with all images
- [ ] metadata.yaml

### 11. Ancillary Files (Optional)
- [ ] Supplementary materials
- [ ] Data files (if any)

---

## Submission Process

### 12. Upload
- [ ] Upload PDF as primary file
- [ ] Upload source files (optional)
- [ ] Verify all files uploaded successfully

### 13. Preview and Verify
- [ ] Preview PDF rendering on arXiv
- [ ] Verify all metadata correct
- [ ] Check abstract formatting
- [ ] Verify category selection

### 14. Submit
- [ ] Click "Submit" after verification
- [ ] Note submission ID for tracking
- [ ] Expect 24-48 hour processing time

---

## Post-Submission

### 15. Track Status
- [ ] Monitor email for acceptance notification
- [ ] Check arXiv for paper appearance
- [ ] Note assigned arXiv ID (e.g., arXiv:2512.XXXXX)

### 16. Update References
- [ ] Add arXiv link to OSF registration
- [ ] Add arXiv link to GitHub repository
- [ ] Add arXiv link to Zenodo deposit

### 17. Share
- [ ] Announce on relevant professional networks
- [ ] Add to ORCID profile
- [ ] Update personal/institutional websites

---

## Version Management

### 18. Future Updates
- [ ] Document any revisions needed post-submission
- [ ] Use arXiv "Replace" feature for substantial updates
- [ ] Maintain version history in git tags

---

## Notes

**arXiv ID format:** arXiv:YYMM.NNNNN (e.g., arXiv:2512.12345)

**Processing time:** Typically 24-48 hours, may be longer during peak periods

**Moderation:** arXiv may hold submissions for moderation; this is normal for first submissions to a category

**Cross-listing:** Can add cross-list categories after initial submission if needed

---

## Quick Reference Commands

```bash
# Generate PDF for submission
./scripts/build_paper.sh --format pdf

# Check PDF file size
ls -lh paper.pdf

# Verify fonts are embedded (requires pdffonts)
pdffonts paper.pdf
```

---

**Last Updated:** 2025-12-16
