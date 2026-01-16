# Empirical Validation Framework (Paper 2)

This document outlines the experimental design and success metrics for validating the Paper 2 reference implementation.

## 1. NL2SQL Accuracy Evaluation

**Objective:** Measure the system's ability to generate executable SQL that matches ground truth results.

-   **Test Set:** 50+ natural language questions ranging from simple (single table) to complex (multiple joins, nested subqueries, haversine calculations).
-   **Ground Truth:** Manually verified SQL queries executed against the "clean" Synthea schema.
-   **Metric:** Execution Accuracy (EX) - Percentage of queries where the generated SQL results match the ground truth results.
-   **Target:** > 85% accuracy.

## 2. Schema Inference Evaluation

**Objective:** Assess the robustness of the automated primary/foreign key (PK/FK) discovery algorithm.

-   **Test Environment:** Intentional "degraded schema" (obfuscated names, no constraints).
-   **Metric:** Precision and Recall of discovered PK/FK relationships compared to the original Synthea schema definitions.
-   **Target:** > 90% Recall for critical clinical relationships (Patient-Encounter, Encounter-Observation).

## 3. Institutional Learning Measurement

**Objective:** Quantify the impact of query memoization and expert validation.

-   **Scenario:** Simulated sequence of 200 analytical queries over multiple "work sessions."
-   **Metric:** Cache Hit Rate - Percentage of queries satisfied by existing "Validated Query Triples."
-   **Metric:** Time-to-Insight - Estimated time reduction per query using cached results vs. fresh generation.
-   **Target:** Measurable increase in cache hits over time; > 40% efficiency gain by end of simulation.

## 4. Probabilistic Column Matching

**Objective:** Validate semantic matching using vector embeddings.

-   **Test:** Map 100 ambiguous natural language terms (e.g., "sugar levels", "heart medication") to correct Synthea columns.
-   **Metric:** Mean Reciprocal Rank (MRR) - Average rank of the correct column in the semantic search results.
-   **Target:** Correct column in top 3 results for 95% of terms.
