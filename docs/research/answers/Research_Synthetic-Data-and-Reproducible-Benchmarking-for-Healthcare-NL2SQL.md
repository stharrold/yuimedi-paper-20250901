# Research: Synthetic Data and Reproducible Benchmarking for Healthcare NL2SQL

**Issue:** [#375](https://github.com/stharrold/yuimedi-paper-20250901/issues/375)
**Scope:** Paper 2 (Reference Implementation)
**Status:** Answered

## Executive Summary
Validation of healthcare NL2SQL systems relies on a combination of **publicly available de-identified datasets** (MIMIC-III, eICU) and **synthetic datasets** (DE-SynPUF, Synthea). Reproducible benchmarking is increasingly achieved through **containerized deployment** on cloud infrastructure (GCP), using single-attempt constraints (**pass@1**) to mirror clinical accuracy requirements.

---

## Synthetic Data in Healthcare AI

### 1. Synthea and DE-SynPUF
- **DE-SynPUF (Data Entrepreneurs’ Synthetic Public Use File):** Ziletti (2024) uses DE-SynPUF to emulate the structure of actual Medicare claims data. It includes 6.8M beneficiary records and >100M claims/prescription records.
- **Synthea Utility:** Gonzales (2023) provides a narrative review highlighting synthetic data's utility in generating patient cases based on public data patterns, allowing for validation without PHI exposure.
- **OMOP-CDM Alignment:** Synthetic data analysis is often applied to any database conforming to the **OMOP Common Data Model**, potentially scaling to billions of records (Ziletti, 2024).

### 2. Validation: Synthetic vs. Real Data
- **Real Patient Trajectories:** Jiang (2025) argues that while synthetic data (like AIPatient) is useful, benchmarks should ideally leverage **real patient trajectories** across diverse clinical settings (extracted from deidentified clinical data warehouses like Stanford's STARR) to provide realistic contexts.
- **Jittering and De-identification:** Real clinical data for benchmarking is typically "jittered" at the patient level (time stamps) and further corrupted to prevent identity recovery from deriving questions (Lee, 2023).

---

## Cloud Architecture Patterns for Benchmarking

### 1. Containerized Environments
- **Docker on GCP:** Jiang (2025) deployed Docker containers on **Google Cloud Platform (GCP)** virtual machines (c2d-standard-2) to create a FHIR-compliant interactive environment for benchmarking.
- **HTTP Interaction:** This architecture allows any agentic AI system to interact with the environment via **HTTP requests**, facilitating reproducible evaluation across different LLMs.

### 2. Standardized Frameworks
- **MedAgentBench:** Uses the framework proposed by **AgentBench** to add various LLMs as agents, ensuring a consistent evaluation setup (Jiang, 2025).
- **Single-Attempt (pass@1) Metrics:** Reflecting clinical environments' low tolerance for error, benchmarks like MedAgentBench exclusively adopt pass@1 to assess models under realistic deployment constraints.

---

## Reproducibility Resources
Researchers are increasingly sharing datasets and codebases to catalyze community-driven efforts:
- **Bayer EHR-RAG:** Ziletti (2024) shared the dataset, code, and prompts on [GitHub](https://github.com/Bayer-Group/text-to-sql-epi-ehr-naacl2024).
- **EHRSQL:** Lee (2023) provided a large-scale human-labeled dataset linked to MIMIC-III and eICU.

---

## References
- Gonzales, A., et al. (2023). Synthetic data in health care: A narrative review. *PLOS Digital Health*.
- Jiang, Y., et al. (2025). MedAgentBench: Benchmarking LLM Agents on EHR Data. *NEJM AI*.
- Lee, J., et al. (2023). EHRSQL: A New Text-to-SQL Benchmark for Electronic Health Records. *arXiv preprint*.
- Ziletti, A., et al. (2024). EHR-RAG: Natural Language Interfaces to Electronic Health Records via Retrieval-Augmented Generation. *arXiv preprint*.
