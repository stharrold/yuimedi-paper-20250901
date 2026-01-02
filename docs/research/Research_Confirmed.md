# Verified Citations Log

This document tracks citations that have been manually verified against their source documents (PDFs) to ensure accuracy of claims, data, and attribution in `paper.md`.

## Verification Status

| Citation Key | Author (Year) | Source PDF | Verification Date | Verified Claims/Notes | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ang2004` | Ang & Slaughter (2004) | `2004_Ang_ACM-SIGMIS_IT-Professional-Turnover.pdf` | 2026-01-01 | **Verified:** 2.9 years new-hire tenure expectancy. **Clarified:** Implied ~34% turnover rate refers to new hires (vs 15.5% general). **Context:** IT Users (Support) category. | ✅ Confirmed |
| `wang2018` | Wang et al. (2018) | `2018_Wang_Tech-Forecasting_Big-Data-Analytics-Healthcare.pdf` | 2026-01-01 | **Verified:** Confirms adoption lag (42% adoption, 16% substantial experience). **Verified:** Confirms architectural complexity and "struggle to gain benefits." **Status:** Citations in `paper.md` are accurate. | ✅ Confirmed |
| `decanio2016` | DeCanio (2016) | `2016_DeCanio_J-Macroeconomics_Robots-and-Humans.pdf` | 2026-01-01 | PDF added to repo. Pending content verification. | ⚠️ Pending |

## Verification Protocol

1.  **Locate Source:** Ensure PDF exists in `docs/references/` with correct naming convention (`YYYY_Author_Journal_Title.pdf`).
2.  **Verify Content:** Read the full text to confirm:
    *   Specific statistics (e.g., turnover rates, sample sizes).
    *   Context of claims (e.g., do they apply to healthcare specifically?).
    *   Caveats or limitations (e.g., "new hire" vs "general" turnover).
3.  **Update `paper.md`:** If discrepancies are found, correct the manuscript.
4.  **Log Status:** Update this table.

## Next Citations to Verify

| `himss2024` | HIMSS Analytics (2024) | `2024_HIMSS_Analytics-Maturity-Adoption-Model.pdf` | 2026-01-01 | **Verified:** Web search confirms exact global counts: 26 at Stage 6, 13 at Stage 7. **Verified:** Solution sheet in repo confirms 0-7 structure and Oct 2024 AMAM24 update. | ✅ Confirmed |
*   `ziletti2024` - Ziletti & D'Ambrosi (2024)
*   `berkshire2024` - Berkshire NHS (2024)
*   `american2023` - AHIMA & NORC (2023)
