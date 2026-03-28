# Research: CI/CD and Automated Testing for Analytics Queries in Healthcare

**Question:** What evidence exists for applying continuous integration, automated regression testing, or schema drift detection to analytical queries, data pipelines, or BI artifacts in healthcare data warehouses?

**Scope:** Paper1 (supports R8: Continuous Analytic Integration concept)

**Date searched:** 2026-03-28

**Source:** Google Scholar Labs (evaluated results, surfaced 10 relevant papers)

---

## Key Findings

1. **CI/CD pipelines for healthcare data warehousing** are documented (Devi 2024): test automation covers data integration, data quality, and performance testing, removing human error from validation processes.
2. **DataOps frameworks with embedded validation** exist (Valiaiev 2025): centralized SQL governance, embedded validation workflows, and observability features using CI/CD pipelines to enforce organizational standards. Explicitly recommends treating analytics pipelines as production systems and governing a "single source of truth SQL repository."
3. **Schema drift handling** in clinical data is addressed by late-binding ELT patterns (Yang et al. 2019): deferring data mapping until query time allows schema evolution without rebuilding the warehouse. Also, Kottam et al. (2025) note existing NL2SQL systems are "not resilient to vocabulary drift or OMOP CDM schema changes."
4. **Data quality frameworks using Great Expectations** have been validated in healthcare contexts (Johnson Mary 2025): automated validation layers, quality monitoring agents, and feedback loops for real-time anomaly detection.
5. **Self-healing data pipelines** for healthcare analytics providers (Betha 2023): automated detection, diagnosis, and remediation of data quality issues in clinical data pipelines, with case study demonstrating reduced data downtime.
6. **Healthcare-specific DataOps** (Chinta 2025): automated validation mechanisms operating continuously throughout data lifecycles, examining completeness, consistency, format adherence, structural integrity, and chronological coherence.

## Relevance to Paper

- **R8 (Continuous Analytic Integration):** Valiaiev 2025 directly supports the concept: "centralized SQL governance, embedded validation workflows... governing a single source of truth SQL repository." This is exactly what the paper proposes for validated query triples.
- **R8:** Betha 2023's healthcare self-healing pipeline case study provides real-world evidence that automated query/pipeline validation works in clinical settings.
- **Section 5 (ARI Schema Coupling):** Kottam et al. 2025's finding that NL2SQL systems lack resilience to schema drift directly supports the need for the Schema Coupling dimension in the ARI.

---

## Sources

### 1. Devi AKRS. AI-Driven Test Automation for Healthcare Data Warehousing Projects. TechRxiv / Authorea Preprints. 2024.

- **URL:** https://www.techrxiv.org/doi/full/10.36227/techrxiv.173198448.81820534
- **PDF:** https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.173198448.81820534
- **Cited by:** 1
- **Key findings:**
  - CI/CD pipelines for healthcare data warehousing test automation
  - Automated testing for data integration, data quality, and performance
  - AI-driven anomaly detection and data profiling to flag outliers and missing values

### 2. Johnson Mary B. Unified Data Quality Frameworks for Real-Time ML Pipelines: Bridging DataOps, MLOps, and Streaming Architectures. SSRN. 2025.

- **URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5216257
- **PDF:** https://papers.ssrn.com/sol3/Delivery.cfm?abstractid=5216257
- **Cited by:** 1
- **Key findings:**
  - Unified data quality framework integrating DataOps, MLOps, and streaming architectures
  - Automated validation layers, quality monitoring agents, and feedback loops for real-time anomaly detection
  - Reference architecture using Apache Kafka, Apache Flink, **Great Expectations**, and MLflow
  - Validated across multiple use cases including healthcare

### 3. Kottam S, Annem S, Sun Y. Error-Aware Text-to-SQL Generation for Clinical Trial Eligibility Criteria Querying in EHR Databases. IEEE International Conference. 2025.

- **URL:** https://ieeexplore.ieee.org/abstract/document/11402102/
- **PDF:** https://yingchengsun.github.io/academic/files/SP02215.pdf
- **Cited by:** new
- **Key findings:**
  - Multi-stage validation pipeline: Knowledge-Augmented NER Verifier, Hybrid Relation Validator, Editable SQL Generation Engine
  - Identifies illogical SQL fragments and prevents cascading failures
  - **Notes existing systems are not resilient to vocabulary drift or OMOP CDM schema changes**

### 4. Yang E, Scheff JD, Shen SC, Farnum MA, Sefton J, et al. A late-binding, distributed, NoSQL warehouse for integrating patient data from clinical trials. Database. 2019.

- **URL:** https://academic.oup.com/database/article-abstract/doi/10.1093/database/baz032/5372332
- **PDF:** https://academic.oup.com/database/article-pdf/doi/10.1093/database/baz032/28032830/baz032.pdf
- **Cited by:** 14
- **Key findings:**
  - ELT design pattern deferring data mapping until query time
  - Schema evolution handled without rebuilding warehouse; supports multiple data representations concurrently
  - Automated data mapping minimizes delays from investigational site data

### 5. Valiaiev D. Implementing Dataops: A Scalable Framework for Modern Data Warehousing. ProQuest Dissertations. 2025.

- **URL:** https://search.proquest.com/openview/aa9acce88c488cbb8c6b3c8339062319/1
- **Cited by:** new
- **Key findings:**
  - **Centralized SQL governance, embedded validation workflows, and observability features**
  - **CI/CD pipeline enforcing validation according to organizational standards**
  - Python-based modular checks
  - Treats analytics pipeline as production system; governs **single source of truth (SSOT) SQL repository**

### 6. Edapurath VN. Automating Data Quality Monitoring In Machine Learning Pipelines. PhilArchive. 2023.

- **URL:** https://philpapers.org/rec/NAVADQ
- **PDF:** https://philarchive.org/archive/NAVADQ
- **Cited by:** 1
- **Key findings:**
  - Automated data quality monitoring within MLOps pipelines
  - Continuous monitoring at data ingestion, pre-training validation, and post-deployment data drift detection
  - Healthcare data context: data reliability impacts safety and regulatory compliance

### 7. Devi AKRS. AI-Enabled ETL Testing Frameworks on Data Warehousing Testing automation using ML. TechRxiv / Authorea Preprints. 2024.

- **URL:** https://www.techrxiv.org/doi/full/10.36227/techrxiv.172840589.91305850
- **PDF:** https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.172840589.91305850
- **Cited by:** 1
- **Key findings:**
  - AI-enabled ETL testing for healthcare data warehousing
  - Continuous monitoring of data quality and integrity through automated frameworks
  - Generates alerts for proactive data governance issue resolution

### 8. Mehta D, Saini D, Jain B, Wainaina L, et al. AI-driven data quality and dataops management. ACM ICAIF 2024 (OpenReview). 2024.

- **URL:** https://openreview.net/forum?id=1JqvIvMNwl
- **PDF:** https://openreview.net/pdf?id=1JqvIvMNwl
- **Cited by:** 1
- **Key findings:**
  - Platform-agnostic, scalable Python-based Advanced QC framework for data quality checks and anomaly detection
  - ML-based data drift detection using algorithms to identify patterns indicative of quality issues
  - DataOps enhances quality control by automating and streamlining data pipelines

### 9. Chinta B. DataOps Automation for Healthcare Pipelines Using Cloud-Native Architectures. Journal of Engineering and Computer Sciences. 2025.

- **URL:** https://sarcouncil.com/2025/08/dataops-automation-for-healthcare-pipelines-using-cloud-native-architectures
- **PDF:** https://sarcouncil.com/download-article/SJECS-356-2025-761-774.pdf
- **Cited by:** new
- **Key findings:**
  - DataOps framework specifically for healthcare information management
  - Automated validation mechanisms operating continuously throughout data lifecycles
  - Multifaceted assessment: completeness, consistency, format adherence, structural integrity, chronological coherence

### 10. Betha R. Data Observability and Data Quality Automation: Building Self-Healing Data Pipelines. IJAIDR. 2023.

- **URL:** https://www.ijaidr.com/papers/2023/1/1299.pdf
- **Cited by:** new
- **Key findings:**
  - Evolution from DevOps to DataOps for data engineering and analytics pipelines
  - Automated detection, diagnosis, and remediation within data pipelines
  - **Healthcare analytics provider case study:** self-healing pipelines for clinical data, reduced data downtime
  - Addresses challenges of ingesting and standardizing clinical data from multiple healthcare organizations
