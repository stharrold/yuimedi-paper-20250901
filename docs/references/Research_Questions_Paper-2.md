# Research Questions: Paper 2 (Reference Implementation)

Research questions for Google Scholar literature search supporting Paper 2.

**Status:** 9/17 core questions answered, 8 gaps remaining.

---

## Answered Questions

### NL2SQL in Healthcare (Q1-3)

| # | Question | Source |
|---|----------|--------|
| 1 | What NL2SQL systems have been applied to healthcare databases? | `Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md`: MedT5SQL, TREQS, Criteria2Query, MedTS, CliniDAL (10 papers) |
| 2 | What accuracy rates have been achieved on clinical data? | `Research_Analytics_NL2SQL-Benchmarks.md`: DeepSeek V3.1 59.8%, Llama-3.3-70B 54.5% on MIMICSQL |
| 3 | Are there healthcare-specific NL2SQL benchmarks? | `Research_Analytics_NL2SQL-Benchmarks.md`: EHRSQL, MIMICSQL, SM3-Text-to-Query, EHRSQL 2024 Shared Task |

### Schema Discovery (Q4-6)

| # | Question | Source |
|---|----------|--------|
| 4 | What algorithms exist for automatic PK/FK discovery from database metadata? | `Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md`: HoPF, SPIDER, ML approaches (10 papers) |
| 5 | How do existing approaches validate discovered relationships (precision/recall)? | `Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md`: F-measure, gold standard comparisons (10 papers) |
| 6 | Has schema discovery been applied to healthcare databases specifically? | `Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md`: transformer-based, OMOP CDM mapping (10 papers) |

### Knowledge Management (Q10, Q16-17)

| # | Question | Source |
|---|----------|--------|
| 10 | What is the knowledge portal paradigm and how has it been implemented? | `Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md`: SEAL framework, Firestone (2007), Benbya (2004) (10 papers) |
| 16 | What is the documented impact of analyst turnover on healthcare analytics? | `Research_Workforce_Turnover.md`: 34% rate, 2.9yr tenure; `Research_Workforce_Turnover-Cost.md`: 1.2-1.3x salary, 3x for knowledge loss |
| 17 | How have others addressed knowledge preservation in data teams? | `Research_Knowledge-Portal_Effective-Components.md`: portal mechanisms (partial - not specific to data teams) |

---

## Remaining Gaps

### Schema Discovery and Validation

7. How have vector embeddings been used for schema matching or column selection? | /Users/stharrold/Documents/GitHub/yuimedi-paper-20250901/docs/references/Research_How-have-vector-embeddings-been-used-for-schema-matching-or-column-selection.md
8. What is the state of the art in semantic table/column matching for NL2SQL?

### Knowledge Management Theory

9. How does Nonaka's SECI model apply to organizational knowledge capture in analytics?
   - Follow-up: How have others operationalized tacit-to-explicit knowledge conversion in software systems?

### Institutional Learning and Query Reuse

11. How have others measured institutional learning in analytics or BI systems?
12. Have any NL2SQL systems implemented query memoization or caching?
13. How have others measured efficiency gains from query reuse in database systems?

### Healthcare Terminology Mapping

14. What approaches exist for programmatic mapping to SNOMED, LOINC, RxNorm?
15. What is the reported ETL burden for OMOP/FHIR transformation?

---

## Additional Research Questions (Lower Priority)

### Clinical Safety and Security

- What clinical safety considerations apply to AI-assisted healthcare analytics?
- What security architecture patterns exist for NL2SQL systems handling PHI?
- How do NIST, HITRUST, and HIPAA requirements apply to AI-enabled healthcare systems?

### Synthetic Data and Validation

- How has Synthea synthetic data been used for healthcare AI/NL2SQL validation?
- What cloud architecture patterns exist for reproducible NL2SQL benchmarking?
- How have others validated NL2SQL systems on synthetic vs. real clinical data?

---

## Related Research Files

| File | Topic |
|------|-------|
| `Research_Analytics_NL2SQL-Datasets.md` | NL2SQL datasets (MIMICSQL, EHRSQL, etc.) |
| `Research_Analytics_NL2SQL-Benchmarks.md` | Benchmark accuracy rates |
| `Research_Analytics_Database-Make-Messy.md` | Tools for degrading data quality |
| `Research_Analytics_Low-Code-ROI.md` | Low-code/AI platform ROI |
| `Research_Analytics_Pace-Skills.md` | Healthcare analytics skills gap |
| `Research_Analytics_Failed-Standardization.md` | OMOP/FHIR challenges |
| `Research_Knowledge-Portal_Effective-Components.md` | Knowledge portal components |
| `Research_Workforce_Turnover.md` | Analyst turnover rates |
| `Research_Workforce_Turnover-Cost.md` | Cost of turnover |
| `Research_Workforce_Training.md` | Training time requirements |
