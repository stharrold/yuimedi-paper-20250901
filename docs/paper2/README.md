# Paper 2: Reference Implementation (GCP/Synthea)

This directory contains research, data, and figures for **Paper 2: Reference Implementation**, a proof-of-concept for the three-pillar analytical framework.

## Overview

**Title:** Empirical Validation of a Three-Pillar Framework for Healthcare Analytics: A Reference Implementation using Conversational AI and Synthetic Health Records

**Strategic Purpose:** Demonstrate the technical feasibility and measurable impact of the validated query cycle in overcoming low analytics maturity and institutional memory loss.

## Core Goals

1.  **Technical Validation:** Show that conversational AI can generate accurate SQL against degraded healthcare schemas without extensive documentation.
2.  **Institutional Learning:** Measure the impact of query memoization and expert validation on analytical efficiency over time.
3.  **Reproducibility:** Provide an open-source reference implementation on Google Cloud Platform (GCP) using the Synthea synthetic dataset.

## Technical Architecture (Proposed)

-   **Data Layer:** BigQuery (storing 1M+ Synthea patient records)
-   **Model Layer:** Vertex AI (Gemini 1.5 Pro / Flash)
-   **Application Layer:** Cloud Functions / Python implementation
-   **Validation Loop:** Probabilistic schema matching + expert validation caching

## Key Research Questions

-   How accurately can the system parse natural language queries into executable SQL on Synthea data?
-   What is the precision/recall of the automated PK/FK discovery algorithm?
-   Does vectorized semantic matching outperform traditional keyword matching for column selection?
-   How do cache hit rates improve as the library of validated queries grows?

## Directory Structure

-   `research/`: Literature review notes specific to knowledge portals and SECI models.
-   `data/`: Schemas, benchmark query sets, and experiment results.
-   `figures/`: Architecture diagrams and performance charts.
-   `ARCHIVED/`: Deprecated planning and draft materials.
