# Research: How have others measured institutional learning in analytics or BI systems?

**Issue:** [#369](https://github.com/stharrold/yuimedi-paper-20250901/issues/369)
**Scope:** Paper 2 (Reference Implementation)
**Status:** Answered

## Executive Summary
Institutional learning in analytics is measured through a combination of **Learning Organization Capacity (LOC)** frameworks, financial impact analysis of **knowledge loss**, and quantitative efficiency gains in **operational and clinical outcomes**. While specific technical terms like "query memoization" are rare in management literature, the concept is addressed through **organizational memory reservoirs** and **Standard Operating Procedures (SOPs)**.

---

## Key Frameworks and Metrics

### 1. Learning Organization Capacity (LOC)
Massingham (2018) defines LOC through three primary concepts, each with specific constructs:
- **People:** Managing knowledge resources, respect for colleagues, and motivation/initiative.
- **Purpose:** Organizational direction, results focus (benchmarking), mission/values awareness, and role clarity.
- **Enablers:** Learning from experience, systems for capturing lessons learned.

**Metric:** Massingham reports a **10.4% increase** in "people" scores in organizations successfully managing knowledge loss, specifically noting improvements in staff motivation and initiative.

### 2. Knowledge Accounts Model
Tacit knowledge is valued using the **Knowledge Accounts Model (Massingham, 2016)**, which tracks four types of capital:
- **Human Capital:** Employee capability and affective attachment.
- **Social Capital:** Internal/external connectivity and corporate leadership.
- **Structural Capital:** Usage of firm resources and contribution to repositories (reports, procedures).
- **Relational Capital:** Customer/partner relationships.

**Metric:** **Table III (Massingham, 2018)** shows that new employees typically reach only **91.8%** of the knowledge account score of exiting employees, representing a persistent "knowledge gap" until competence is reached.

### 3. Financial Impact of Organizational Forgetting
Organizational learning is not always cumulative; it can decay or "depreciate" (Rao & Argote, 2006).
- **Time to Competence:** Massingham identifies a **6-month time to competence** for healthcare IT workers.
- **Financial Metric:** At an average salary of $100,000, this period of "decreased learning" represents a **$50,000 sunk cost** per new hire in lost productivity and supervision (Massingham, 2018, Table XII).

### 4. Operational and Clinical Efficiency Gains
Nashid (2023) measured the impact of advanced business analytics adoption in healthcare:
- **Operational Efficiency Gains:** **21.3%**
- **Staff Productivity:** Correlation of **r = 0.60** with analytics adoption.
- **Clinical Decision Support (CDS) Efficiency:** Correlation of **r = 0.72** with measured clinical benefits.

---

## Technical Mechanisms (Query Reuse)
While management literature focuses on human capital, technical systems address learning through:
- **Organizational Memory Reservoirs:** SOPs, routines, and repositories (Rao, 2006).
- **Two-Stage Recovery:** Wang (2020) uses **look-up tables** and **strict SQL templates** to "learn" and recover exact information from rough NL2SQL drafts.
- **Retrieval Augmented Generation (RAG):** Ziletti (2024) demonstrates that RAG is effective for "learning" from small, domain-specific biomedical datasets to improve NL2SQL performance.

---

## References
- Massingham, P. R. (2018). Measuring the impact of knowledge loss: a longitudinal study. *Journal of Knowledge Management*, 22(4), 721-758.
- Nashid, S., et al. (2023). Advanced Business Analytics in Healthcare Enhancing Clinical Decision Support and Operational Efficiency. *Business and Social Sciences*, 1(1), 1-8.
- Rao, R. D., & Argote, L. (2006). Organizational learning and forgetting. *European Management Review*, 3, 77-85.
- Wang, P., Shi, T., & Reddy, C. K. (2020). Text-to-SQL Generation for Question Answering on Electronic Medical Records. *Proceedings of The Web Conference 2020*, 11 pages.
- Ziletti, A., et al. (2024). EHR-RAG: Natural Language Interfaces to Electronic Health Records via Retrieval-Augmented Generation. *arXiv preprint*.
