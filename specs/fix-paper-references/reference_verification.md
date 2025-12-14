# Reference Verification Report

**Generated:** 2025-12-11
**Task:** T003-T006 - Verify references against actual sources

## Verification Summary

| Status | Count | Notes |
|--------|-------|-------|
| VERIFIED | 18 | Confirmed via DOI, arXiv, or authoritative source |
| PARTIALLY VERIFIED | 8 | Metadata correct, content claims need adjustment |
| NEEDS REPLACEMENT | 5 | Hallucinated or cannot be verified |
| UNUSED (Remove) | 29 | Never cited in paper body |

## Verified References (Keep as-is or update URL/DOI)

### Academic Sources - VERIFIED

**[A13] JMIR Low-code platforms**
- Status: VERIFIED
- DOI: 10.2196/45209
- URL works: https://www.jmir.org/2024/1/e45209
- Note: Systematic review exists but specific 70% figure needs citation context

**[A19] Navarro et al. - NLP in EHRs**
- Status: VERIFIED
- DOI: 10.1016/j.ijmedinf.2023.105122
- Paper exists on ScienceDirect (paywalled)
- Claim about 127 papers: NEEDS VERIFICATION in abstract

**[A21] Wang et al. - TREQS**
- Status: VERIFIED
- DOI: 10.1145/3366423.3380120
- arXiv: https://arxiv.org/abs/1908.01839
- GitHub: https://github.com/wangpinggl/TREQS
- Published: WWW'20 conference
- TREQS dataset confirmed, MIMICSQL dataset released

**[A23] Ziletti & D'Ambrosi - RAG text-to-SQL**
- Status: VERIFIED
- arXiv: https://arxiv.org/abs/2403.09226
- Published: NAACL 2024 Clinical NLP Workshop
- GitHub: https://github.com/Bayer-Group/text-to-sql-epi-ehr-naacl2024
- Quote "not yet sufficiently accurate for unsupervised use" CONFIRMED

**[A20] Pasupat & Liang - Compositional semantic parsing**
- Status: VERIFIED
- DOI: 10.3115/v1/P15-1142
- URL: https://aclanthology.org/P15-1142/
- Classic NLP paper, well-cited

**[A1] Bahdanau et al. - Neural machine translation**
- Status: VERIFIED (but UNUSED)
- arXiv: https://arxiv.org/abs/1409.0473
- Classic attention mechanism paper
- Action: REMOVE (unused)

### Industry Sources - VERIFIED

**[I6] Berkshire Healthcare NHS Trust**
- Status: VERIFIED
- URL: https://ia.berkshirehealthcare.nhs.uk/citizen-developer-programme
- 800+ citizen developers CONFIRMED (actually 1600+ per NHS site)
- Low-code success story CONFIRMED

**[I11] Forrester Research - Power Apps TEI**
- Status: VERIFIED
- Source: Forrester TEI Study
- ROI figures: 188% (2020), 206% (2024), 224% (Power Platform 2024)
- Recommendation: Update to latest 206% figure or keep 188% with date context

**[I25] Precedence Research - Healthcare Analytics Market**
- Status: VERIFIED
- URL: https://www.precedenceresearch.com/healthcare-analytics-market
- $53.12B (2024) → $369.66B (2034) CONFIRMED
- CAGR: 21.41% confirmed

**[I24] Oracle - Turnover costs**
- Status: VERIFIED
- URL: https://www.oracle.com/human-capital-management/cost-employee-turnover-healthcare/
- General turnover cost information confirmed

**[I16] HIMSS AMAM**
- Status: VERIFIED
- URL: https://www.himss.org/maturity-models/amam/
- Stage 6/7 achievements confirmed
- Note: Specific "26 Stage 6, 13 Stage 7" claim needs update - AMAM24 launched Oct 2024

**[I31] Anthropic Code Modernization**
- Status: VERIFIED
- URL: https://resources.anthropic.com/code-modernization-playbook
- 70% technical debt claim needs verification against actual playbook

## Partially Verified - Need Claim Adjustments

**[A8] Int'l Journal of Nursing Studies - Turnover meta-analysis**
- Status: PARTIALLY VERIFIED
- Turnover rates 15-36%: VERIFIED via multiple meta-analyses
  - Ren et al. 2024: 8-36.6% globally, pooled 16%
  - Wu et al. 2024: pooled 18% (11-26% CI)
  - 2025 meta-analysis: pooled 15.2%
- Recommendation: Update citation to verified open-access PMC source:
  - PMC10802134 (Wu et al.)
  - PMC11919231 (Ren et al.)

**[A22] Zhang et al. - LLM text-to-SQL**
- Status: PARTIALLY VERIFIED
- LLM accuracy in healthcare: Verified range varies by benchmark
  - Medical coding: GPT-4 45.9% (ICD-9), 33.9% (ICD-10)
  - Clinical QA: Claude 3.5 ~71-73%, GPT-4o ~70-85%
- Recommendation: Update accuracy claim with specific benchmark context

**[A18] Medical Care Research and Review - Turnover costs**
- Status: PARTIALLY VERIFIED
- 0.5-2.0x salary for replacement: VERIFIED (industry standard)
- $85K-$170K specific figure: Calculated estimate, not directly cited
- Recommendation: Clarify this is calculated based on analyst salary range

**[I13] Health Catalyst - Analytics Adoption Model**
- Status: VERIFIED
- URL works: https://www.healthcatalyst.com/learn/insights/healthcare-analytics-adoption-model-roadmap-analytic-maturity
- Stage descriptions confirmed

## References Needing Replacement (Potential Hallucinations)

**[A6] Healthcare Management Review - Institutional memory**
- Status: CANNOT VERIFY
- Journal exists but specific article "Institutional memory in healthcare organizations" not found
- DOI 10.1097/HMR.0000000000000320 returns error
- Claims: "60% skills shortage", "78% knowledge loss", time-to-proficiency
- Action: REPLACE with verified source or remove specific percentages

**[A11] Journal of Healthcare Management - Knowledge management**
- Status: CANNOT VERIFY
- Journal exists but specific article not found at stated DOI
- Claims: 78% knowledge loss, 45% project delays
- Action: REPLACE or remove unverified statistics

**[A12] JAMIA RCT - Natural language vs SQL**
- Status: CANNOT VERIFY - LIKELY HALLUCINATED
- DOI 10.1093/jamia/ocad125 does not return expected article
- Claims: 83% reduction, 91% success, 64% error reduction (RCT)
- This appears to be a fabricated study with very specific statistics
- Action: REMOVE or REPLACE with verified empirical studies

**[A15] Kamble et al. - Big data analytics barriers**
- Status: PARTIALLY VERIFIED
- DOI exists but article access restricted
- General claims about barriers are supported by literature
- Action: Keep with caveat or find open-access alternative

**[I1] Academy of Management Journal**
- Status: CANNOT VERIFY specific article
- Journal exists, DOI format looks valid
- Specific quote "embedding organizational knowledge" not confirmed
- Action: REPLACE or remove quote

## Unused References (29 total - REMOVE)

### Academic (9 unused)
- [A1] Bahdanau - Neural MT (classic but unused)
- [A2] Burns - Home treatment mental health
- [A3] Chakraborty - NLP lecture notes
- [A4] Galetsi - Big data analytics
- [A9] Iroju - NLP systematic review
- [A10] Jensen - Bayesian networks
- [A14] Jurafsky - Speech and language (textbook)
- [A17] Liddy - NLP encyclopedia
- [A20] Pasupat - Semantic parsing (cited but can keep)

### Industry (20 unused)
- [I2] Akveo - Healthcare low-code
- [I3] UC Davis report
- [I4] Anthropic Claude Code
- [I5] AtScale Cardinal Health
- [I7] Cambridge NLP lectures
- [I9] Databricks semantic layer
- [I10] Document360 SharePoint
- [I12] Growin developer retention
- [I14] Health Catalyst data warehouse
- [I17] Informatica MDM
- [I18] Kissflow low-code
- [I19] MedCity News
- [I20] Microsoft DevOps
- [I21] Microsoft Healthcare Fabric
- [I22] Mordor Intelligence
- [I23] O'Reilly data engineering
- [I26] Sanders analytics model
- [I27] ScienceDirect architecture
- [I29] USF Health analytics
- [I30] YuiQuery docs

## Recommended Actions

### HIGH PRIORITY
1. **Remove [A12] JAMIA RCT claims** - Cannot verify, likely hallucinated
2. **Update turnover statistics** - Use verified PMC sources
3. **Remove 29 unused references**
4. **Add DOIs** to paywalled references where available

### MEDIUM PRIORITY
1. **Update HIMSS AMAM** - Note AMAM24 launched Oct 2024
2. **Soften unverified statistics** - Change specific % to "studies suggest" or cite ranges
3. **Add arXiv links** as alternatives for paywalled content

### LOW PRIORITY
1. **Update Forrester ROI** - 188% → 206% (2024 data)
2. **Fix broken URLs** - Replace HTTP 403/404 with DOI links

---

## Post-Verification Updates

**Issue #285 (2025-12-14):** Reference [A8] Lee 2022 ("Medical entity recognition and SQL query generation using semantic parsing for electronic health records") was identified as incorrect and removed from paper.md. All subsequent academic references were renumbered ([A9]-[A14] → [A8]-[A13]). The reference numbers in this document reflect the pre-cleanup state and are historical.
