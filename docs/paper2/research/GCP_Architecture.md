# GCP Architecture Design (Paper 2)

This document outlines the proposed architecture for the Paper 2 reference implementation on Google Cloud Platform (GCP).

## Components

1.  **Data Warehouse (BigQuery):**
    -   Stores the Synthea SyntheticMass dataset (1M+ patient records).
    -   Hosts the intentional "degraded schema" (missing metadata, obfuscated names) to test algorithm robustness.
2.  **Model Layer (Vertex AI):**
    -   **Gemini 1.5 Pro:** Used for natural language reasoning, schema inference, and SQL generation.
    -   **Text Embeddings (text-embedding-004):** Powers the vectorized data catalog for semantic column matching.
3.  **Application Layer (Cloud Functions):**
    -   Python-based backend orchestrating the NL2SQL pipeline.
    -   Handles PK/FK discovery, probabilistic matching, and SQL execution.
4.  **Validation & Learning Loop:**
    -   **Cloud SQL (PostgreSQL) or BigQuery Table:** Stores "Validated Query Triples" (NL Question, SQL Query, Rationale).
    -   Enables institutional memory through query memoization and retrieval.

## Data Flow

1.  **Query Input:** Domain expert provides a natural language question.
2.  **Semantic Search:** System retrieves relevant schema metadata from the vectorized catalog.
3.  **Prompt Construction:** Dynamic prompt including schema context and relevant validated query examples.
4.  **SQL Generation:** Gemini 1.5 generates candidate SQL.
5.  **Expert Validation:** (Simulated/Human-in-the-loop) User confirms query intent and results.
6.  **Knowledge Capture:** Validated triple is stored in the learning loop for future reuse.

## Security & Compliance

-   **IAM:** Least-privilege access control for all GCP services.
-   **VPC Service Controls:** Ensuring data remains within the defined security perimeter.
-   **Anonymization:** Use of synthetic data (Synthea) ensures no HIPAA PII exposure.
