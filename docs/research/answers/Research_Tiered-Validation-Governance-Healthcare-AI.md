# Research: Tiered Validation Governance for Healthcare AI

**Question:** What governance frameworks exist for tiered or graduated human validation of AI-generated outputs in healthcare, where validation rigor scales with risk level or validator expertise? Include research on risk-stratified human-AI collaboration, provisional validation in clinical decision support, and FDA oversight tiers for AI/ML medical devices.

**Scope:** Paper1 (supports R2: Validator Paradox operationalization)

**Date searched:** 2026-03-28

**Source:** Google Scholar Labs (evaluated 60 top results, surfaced 10 relevant papers)

---

## Key Findings

1. **Tiered risk stratification frameworks exist** for healthcare AI governance. The CAOS framework (Kumar et al. 2025) proposes a 5-tier system (SARAP, Tier 0-4) where scrutiny scales with potential for patient harm, and includes tiered certification for validator expertise.
2. **Risk-based human oversight models** map AI risk levels to graduated human involvement: Human-in-Command (HIC), Human-in-the-Loop (HITL), and Human-on-the-Loop (HOTL) (Kandikatla & Radeljic 2025).
3. **FDA regulatory pathways** already implement tiered validation through Class I/II/III device categorization, with increasing rigor requirements (Pantanowitz et al. 2024). The FDA is moving toward adaptive frameworks with Predetermined Change Control Plans (PCCPs) for AI/ML devices (Saini et al. 2025).
4. **AI governance maturity models** (HAIRA, Hussein et al. 2026) provide 5-level progressions from ad hoc to leading governance, paralleling the paper's ARI concept.
5. **No framework specifically addresses tiered validation for analytics query governance.** The closest analogs are clinical decision support validation frameworks and FDA device tiers. This confirms the paper's R2 proposal (three-tier validation) fills a gap.

## Relevance to Paper

- **R2 (Validator Paradox):** Kumar et al. 2025 (CAOS/SARAP) directly supports the three-tier governance model by providing peer-reviewed precedent for tiered risk stratification with expertise-based validation in healthcare AI. Cite as: "Risk-stratified governance frameworks for healthcare AI have been proposed [Kumar et al. 2025], in which the level of human oversight scales with potential for patient harm."
- **R2 (Validator Paradox):** Kandikatla & Radeljic 2025 provides the HIC/HITL/HOTL taxonomy that maps directly to HiL-SG's full/constrained/automated tiers.
- **R5 (ARI):** Hussein et al. 2026 (HAIRA) is a peer-reviewed AI governance maturity model from npj Digital Medicine that validates the concept of staged governance assessment, supporting ARI as a complementary instrument.

---

## Sources

### 1. Ho CWL. Implementing the human right to science in the regulatory governance of artificial intelligence in healthcare. Journal of Law and the Biosciences. 2023.

- **URL:** https://academic.oup.com/jlb/article-pdf/doi/10.1093/jlb/lsad026/52191094/lsad026.pdf
- **Cited by:** 18
- **Key findings:**
  - Examines FDA implementation of IMDRF principles for risk-categorization of AI-based medical devices
  - Proposes rights-based governance approach centered on human right to science (HRS)
  - Discusses IDx-DR as fully autonomous AI diagnostic (no clinician interpretation required), illustrating distinction between autonomous and CDS systems

### 2. Kumar R, Sporn K, Waisberg E, Ong J, Paladugu P, et al. Navigating healthcare AI governance: the comprehensive algorithmic oversight and stewardship framework for risk and equity. Health Care Analysis. 2025.

- **URL:** https://link.springer.com/article/10.1007/s10728-025-00537-y
- **PDF:** https://link.springer.com/content/pdf/10.1007/s10728-025-00537-y.pdf
- **Cited by:** 6
- **Key findings:**
  - Proposes CAOS (Comprehensive Algorithmic Oversight and Stewardship) Framework
  - **SARAP tiered risk evaluation:** Tier 0 to Tier 4, scrutiny scales with potential for patient harm, parallels FDA risk-based credibility framework
  - **AI-CSEP tiered certification:** training depth aligns with system interaction levels and risk classifications, supporting expertise-based validation

### 3. Kandikatla L, Radeljic B. AI and Human Oversight: A Risk-Based Framework for Alignment. arXiv preprint arXiv:2510.09090. 2025.

- **URL:** https://arxiv.org/abs/2510.09090
- **PDF:** https://arxiv.org/pdf/2510.09090
- **Cited by:** 4
- **Key findings:**
  - Links AI model risk to appropriate human oversight: Human-in-Command (HIC), Human-in-the-Loop (HITL), Human-on-the-Loop (HOTL)
  - HITL crucial for clinical decision support where real-time human judgment prevents harm
  - Actionable methodology: identify AI scenarios by impact, perform risk assessment, map to oversight levels

### 4. Labkoff S, Oladimeji B, Kannry J, et al. Toward a responsible future: recommendations for AI-enabled clinical decision support. Journal of the American Medical Informatics Association. 2024;31(11):2730.

- **URL:** https://academic.oup.com/jamia/article-abstract/31/11/2730/7776823
- **PDF:** https://academic.oup.com/jamia/article-pdf/31/11/2730/59813542/ocae209.pdf
- **Cited by:** 152
- **Key findings:**
  - Comprehensive framework for AI-enabled CDS development, implementation, and regulation
  - Recommends systematic validation/verification/certification processes
  - Emphasizes data validation, algorithmic validation, and clinical validation layers
  - Calls for national safety monitoring and reporting

### 5. Hussein R, Zink A, Ramadan B, Howard FM, et al. Advancing healthcare AI governance through a comprehensive maturity model based on systematic review. npj Digital Medicine. 2026.

- **URL:** https://www.nature.com/articles/s41746-026-02418-7
- **PDF:** https://www.nature.com/articles/s41746-026-02418-7.pdf
- **Cited by:** 1
- **Key findings:**
  - HAIRA (Healthcare AI Governance Readiness Assessment): 5-level maturity model
  - Level 1 (Initial/Ad Hoc) to Level 5 (Leading)
  - Seven critical governance domains from systematic review of 35 frameworks
  - Provides actionable governance pathways based on organizational resources

### 6. Saini M, Kc G, Williams AJ, Coplan PM, et al. Regulatory Challenges and Opportunities: A Review of US FDA-Approved AI/ML-Enabled Cardiovascular Medical Devices. Therapeutic Innovation & Regulatory Science. 2025.

- **URL:** https://link.springer.com/article/10.1007/s43441-025-00896-7
- **Cited by:** 2
- **Key findings:**
  - Reviews FDA regulatory pathways for AI/ML cardiovascular devices
  - Premarket evaluations include clinical validation, bench testing, algorithm performance assessments
  - FDA transitioning to adaptive framework with Predetermined Change Control Plans (PCCPs)
  - PCCPs enable managed device modifications while maintaining human oversight

### 7. Abd-Alrazaq A, Solaiman B, Mekki YM, et al. Hype vs reality in the integration of artificial intelligence in clinical workflows. JMIR Formative Research. 2025;9(1):e70921.

- **URL:** https://formative.jmir.org/2025/1/e70921
- **Cited by:** 3
- **Key findings:**
  - Advocates validation parity: AI systems should meet evidence standards comparable to drugs/devices
  - Recommends FDA develop validation processes for AI analogous to drug approval
  - Calls for national guidelines on human oversight and AI confidence thresholds
  - Positions AI strictly as decision support with clear usage protocols

### 8. Pantanowitz L, Hanna M, Pantanowitz J, Lennerz J, et al. Regulatory aspects of artificial intelligence and machine learning. Modern Pathology. 2024.

- **URL:** https://www.sciencedirect.com/science/article/pii/S0893395224001893
- **Cited by:** 119
- **Key findings:**
  - FDA categorizes SaMD based on 3 risk levels (Class I, II, III) determining regulatory control rigor
  - EU regulatory controls also risk-based, similar to FDA approach
  - IRBs provide ethics oversight including risk-benefit analysis for AI research involving human data

### 9. Sharma KH, Sharma P, Sharma P. From Human Oversight to Human-in-the-Loop: Evolving Governance of Human-AI Interaction in Healthcare and AI Development. Preprints.org. 2026.

- **URL:** https://www.preprints.org/manuscript/202602.1949
- **PDF:** https://www.preprints.org/frontend/manuscript/ee9f6d80c00b9786064bff1b79aa7681/download_pub
- **Cited by:** new
- **Key findings:**
  - Synthesizes EU AI Act, WHO, OECD, ICMR, and FDA/GMLP governance instruments
  - Reviews FUTURE-AI, CHAI, and Joint Commission guidance for healthcare AI HITL governance
  - FDA GMLP requires robust model development, predetermined change-control plans, real-world monitoring

### 10. Higgins DC, Johner C. Validation of artificial intelligence containing products across the regulated healthcare industries. Therapeutic Innovation & Regulatory Science. 2023.

- **URL:** https://link.springer.com/article/10.1007/s43441-023-00530-4
- **PDF:** https://arxiv.org/pdf/2302.07103
- **Cited by:** 35
- **Key findings:**
  - Distinguishes "broad validation" vs "narrow validation" for AI products
  - Proposes common AI software validation methodology across pharma R&D, manufacturing, and MD/IVD
  - Risk impact differs by domain: MD/IVD has more direct adverse health potential than pharma AI applications
