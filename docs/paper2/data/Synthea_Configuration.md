# Synthea Dataset Configuration (Paper 2)

This document describes the configuration and loading process for the Synthea synthetic dataset.

## Dataset Specifications

-   **Source:** Synthea™ SyntheticMass (1M+ Patients)
-   **URL:** https://synthea.mitre.org/downloads
-   **Schema:** 19 relational tables (CSV format)
-   **Tables Include:** `patients`, `encounters`, `observations`, `conditions`, `medications`, `procedures`, `immunizations`, `careplans`, `imaging_studies`, etc.

## Configuration Steps

1.  **Download:** Fetch the 1M patient SyntheticMass dataset from the MITRE repository.
2.  **Schema Degradation (Intentional):**
    -   Remove all database-level Foreign Key constraints.
    -   Rename key columns with inconsistent prefixes (e.g., `id` → `pid` in some tables, `patient_uuid` in others).
    -   Remove all column-level descriptions and comments.
3.  **Loading to BigQuery:**
    -   Bucket: `gs://yuimedi-paper-2-data/`
    -   Load CSVs into a dedicated BigQuery dataset (`synthea_mass_1m`).
    -   Enable schema auto-detection to simulate real-world data ingest.

## Data Verification

-   **Patient Count:** Confirm > 1,170,000 unique patient records.
-   **Row Counts:** Baseline row counts for all 19 tables to ensure full load.
-   **Integrity Checks:** Verify date ranges and categorical value distributions match expected SyntheticMass patterns.
