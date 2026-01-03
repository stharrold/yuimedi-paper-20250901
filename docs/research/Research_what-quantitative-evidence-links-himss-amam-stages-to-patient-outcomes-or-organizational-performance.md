# Research: What quantitative evidence links HIMSS AMAM stages to patient outcomes or organizational performance?

**Scope:** Paper1 (Framework Development - Maturity Pillar)
**Date:** 2026-01-01
**Status:** Partial (AMAM Gap Confirmed; EMRAM/DHI Evidence Found)

## Key Findings

### 1. The AMAM Evidence Gap
*   **Gap Confirmed:** A search of Google Scholar Labs on 2026-01-01 returned 10 relevant studies. **None** explicitly used the **HIMSS AMAM** (Analytics Maturity Adoption Model) as the independent variable.
*   **Proxies Used:** Research overwhelmingly relies on **HIMSS EMRAM** (Electronic Medical Record Adoption Model) or the **HIMSS DHI** (Digital Health Indicator) to measure "maturity."

### 2. Evidence from Proxy Models (EMRAM/DHI)

#### Positive Associations
*   **Safety & Quality (EMRAM):** Snowdon et al. (2024) found hospitals with EMRAM Stages 6-7 had **3.25x higher odds** of achieving a better Leapfrog Safety Grade and significantly reduced infection rates/adverse events.
*   **Patient Experience (EMRAM):** A separate Snowdon et al. (2024) study found EMRAM 6-7 associated with **1.8-2.24x higher odds** of positive patient experience ratings (communication).
*   **Process Scores (EMRAM):** Jarvis et al. (2013) found Stage 7 linked to significantly higher clinical process of care scores (+4.2 points).
*   **Staff & Costs (DHI):** Woods et al. (2024) used the **HIMSS Digital Health Indicator (DHI)** and found associations with **lower staff turnover**, reduced medication errors (12.9%), and reduced infections (14.3%). *This is the closest proxy to AMAM as DHI includes analytics.*

#### Null or Mixed Associations
*   **Readmissions (EMRAM):** Saint-Ulysse (2021) found **no significant association** between EMRAM maturity and excess readmission ratios for specific conditions.
*   **Mortality (NHS CDMI):** Martin et al. (2019) found **no relationship** between organizational digital maturity (using UK NHS CDMI) and risk-adjusted mortality or readmission.
*   **Financials (EHR/HIE):** Pai et al. (SSRN) found organizational factors (size, payer mix) were stronger predictors of outcomes/margins than HIT maturity.

## Implications for Framework
*   **Transitivity Argument:** The framework must argue that if EMRAM (data capture) drives outcomes, AMAM (data utility) is the necessary next step. The Woods (2024) finding on DHI supports this, as DHI encompasses analytics.
*   **Risk:** The "Null" findings (Saint-Ulysse, Martin) suggest maturity models alone are insufficient. This reinforces the framework's "Three-Pillar" approach: Maturity + **Workforce** + **Technical Barriers**. High maturity without workforce (turnover) or technical capability might explain the null results.

## Sources

### [A82] Snowdon et al. (2024a) - Safety
*   **Title:** Digital maturity as a predictor of quality and safety outcomes in US hospitals: Cross-sectional observational study
*   **Journal:** JMIR
*   **Metric:** EMRAM 6-7
*   **Finding:** 3.25x odds of better Leapfrog Safety Grade; reduced infection rates; fewer adverse events.
*   **URL:** https://www.jmir.org/2024/1/e56316/

### [A83] Snowdon et al. (2024b) - Experience
*   **Title:** Digital maturity as a strategy for advancing patient experience in US hospitals
*   **Journal:** Journal of Patient Experience
*   **Metric:** EMRAM 6-7
*   **Finding:** 1.8-2.24x higher odds of positive ratings for communication with nurses/doctors and about medicines.
*   **URL:** https://journals.sagepub.com/doi/abs/10.1177/23743735241228931

### [A84] Woods et al. (2024) - DHI & Workforce
*   **Title:** Impact of digital health on the quadruple aims of healthcare: A correlational and longitudinal study (Digimat Study)
*   **Journal:** International Journal of Medical Informatics
*   **Metric:** HIMSS Digital Health Indicator (DHI)
*   **Finding:** Digital capability associated with **lower staff turnover**, decreased medication errors (12.87%), and reduced nosocomial infections (14.27%).
*   **URL:** https://www.sciencedirect.com/science/article/pii/S1386505624001916

### [A85] Saint-Ulysse (2021)
*   **Title:** The Relationship between Hospitals' Electronic Health Records Maturity and Excess Readmission Ratio
*   **Source:** Walden University / ProQuest
*   **Metric:** EMRAM
*   **Finding:** No significant association between EHR maturity and excess readmission ratio (ERR) for coronary artery bypass or hip/knee arthroplasty.
*   **URL:** https://search.proquest.com/openview/f4622b90ebf7c5ef34b247c0d92dd4fa/1?pq-origsite=gscholar&cbl=18750&diss=y

### [A86] Martin et al. (2019)
*   **Title:** Evaluating the impact of organisational digital maturity on clinical outcomes in secondary care in England
*   **Journal:** npj Digital Medicine
*   **Metric:** NHS CDMI
*   **Finding:** No significant relationship between digital maturity and risk-adjusted mortality or readmission. Found association with "harm-free care" but increased length of stay.
*   **URL:** https://www.nature.com/articles/s41746-019-0118-9
