# Research: Does self-selection / non-response bias affect organizational IT-maturity benchmark assessments?

**Scope:** Paper1
**Issue:** [#534](https://github.com/stharrold/yuimedi-paper-20250901/issues/534) (i-JMR R1, Reviewer Q#1)
**Date:** 2026-06-06
**Status:** Answered
**Source:** Google Scholar Labs (10 relevant results)
**Query:** "How does self-selection or non-response bias affect participation in voluntary organizational maturity and benchmarking assessments?"

## Key Findings

Reviewer Q#1 argued that organizations primarily avoid maturity certifications (e.g., HIMSS) due to high cost, so maturity-stage statistics are subject to self-selection bias. The organizational-survey methodology literature strongly supports acknowledging this, and there is a maturity-assessment-specific precedent:

- *Directly in a maturity assessment.* El Emam & Madhavji (1995), "The reliability of measuring organizational maturity," evaluate non-response bias in a maturity-assessment case study by comparing early vs late respondents across demographics (location, budget, personnel, sector), establishing that maturity measurement must account for non-response bias.
- *In a health-services context.* Halbesleben & Whitman (2013, Health Services Research) note non-response bias occurs at the organizational level when organizations choose not to participate; findings from voluntary assessments may not generalize and can shift mean outcomes and measured relationships.
- *Why organizations self-select.* Tomaskovic-Devey, Leiter & Thompson (1994, Administrative Science Quarterly; and 1995) develop an organizational theory of survey response: response probability is systematically tied to organizational authority, capacity, and motive (e.g., dedicated staff, resource dependence), making non-response a non-random, predictable selection bias.
- *Foundational framing.* Rogelberg & Stanton (2007) provide the N-BIAS non-response-bias assessment strategy; Sivo et al. (2006, JAIS) tie low response rates to selection bias in IS questionnaire research; Donald (1960) shows self-selection relates to respondent involvement.

**For the paper (B1, #534):** Add a sentence acknowledging that HIMSS-style maturity-stage data come from voluntary, often costly assessments and are therefore subject to self-selection / non-response bias (organizations that opt in differ systematically from those that do not), citing El Emam & Madhavji (1995) for the maturity-specific case and Tomaskovic-Devey et al. (1994) and/or Halbesleben & Whitman (2013) for the mechanism. Pair this with the broader analytics-maturity construct evidence (see `Research_Defining-Analytics-Maturity-and-Maturity-Models.md`) so the maturity argument does not rest on HIMSS certification data alone.

## Sources

| # | Citation | Venue / Year | URL | Note |
|---|----------|--------------|-----|------|
| 1 | El Emam K, Madhavji NH. The reliability of measuring organizational maturity. | Software Process Improvement and Practice, 1995 | (Citeseer; recover DOI when citing) | Non-response bias evaluated within a maturity assessment. Cited 54 |
| 2 | Halbesleben JRB, Whitman MV. Evaluating survey quality in health services research: a decision framework for assessing nonresponse bias. | Health Services Research, 2013 | https://onlinelibrary.wiley.com/doi/abs/10.1111/1475-6773.12002 | Org-level nonresponse; voluntary assessments may not generalize. Cited 387 |
| 3 | Tomaskovic-Devey D, Leiter J, Thompson S. Organizational survey nonresponse. | Administrative Science Quarterly, 1994 | https://www.jstor.org/stable/2393298 | Org theory of response; why orgs self-select. Cited 637 |
| 4 | Tomaskovic-Devey D, Leiter J, Thompson S. Item nonresponse in organizational surveys. | Sociological Methodology, 1995 | https://www.jstor.org/stable/271062 | Nonresponse tied to authority/capacity/motive; nonrandom. Cited 61 |
| 5 | Rogelberg SG, Stanton JM. Understanding and dealing with organizational survey nonresponse. | Organizational Research Methods, 2007 | https://journals.sagepub.com/doi/abs/10.1177/1094428106294693 | N-BIAS nonresponse-bias assessment strategy. Cited 1599 |
| 6 | Sivo SA, Saunders C, Chang Q, et al. How low should you go? Low response rates and the validity of inference in IS questionnaire research. | J. Association for Information Systems, 2006 | https://aisel.aisnet.org/cgi/viewcontent.cgi?article=1267&context=jais | Selection bias when respondents differ from non-respondents. Cited 710 |
| 7 | Donald MN. Implications of nonresponse for the interpretation of mail questionnaire data. | Public Opinion Quarterly, 1960 | https://academic.oup.com/poq/article-abstract/24/1/99/1824643 | Classic self-selection bias and involvement. Cited 390 |
| 8 | Rogelberg SG, Conway JM, Sederburg ME, et al. Profiling active and passive nonrespondents to an organizational survey. | J. Applied Psychology, 2003 | https://psycnet.apa.org/fulltext/2003-09785-011.html | Active nonrespondents differ systematically. Cited 369 |
| 9 | Reuel A, Connolly P, Meimandi KJ, Tewari S, et al. Responsible AI in the global context: maturity model and survey. | ACM (AIES/FAccT), 2025 | https://dl.acm.org/doi/abs/10.1145/3715275.3732165 | Maturity-model survey explicitly flags self-selection + nonresponse bias |
| 10 | Hirschfeld RR, Cole MS, Bernerth JB, et al. Voluntary survey completion among team members. | J. Applied Psychology, 2013 | https://psycnet.apa.org/fulltext/2013-06781-001.html | Voluntary participation predictable from org factors; biases estimates. Cited 60 |

## Next steps
- Add BibTeX entries for the chosen cites to `references.bib` (feeds #542). Recover a stable DOI/URL for El Emam & Madhavji (1995).
- Use in #534 (B1) to acknowledge HIMSS maturity-data self-selection bias.
