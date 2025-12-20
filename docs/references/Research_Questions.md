# Research Questions

Unified tracking for all literature/research questions supporting the paper series.

**Status:** 15 answered, 14 unanswered

---

## Workflow

```
New Question
    ↓
Add to "Unanswered Questions" below
    ↓
Literature Search
    ↓
┌──────────────────┴──────────────────┐
↓                                     ↓
NOT FOUND IN LITERATURE              FOUND IN LITERATURE
↓                                     ↓
1. Add to paper.md                   1. Add citations to paper.md
   "Gaps in Current Literature"      2. Create Research_<phrase>.md
2. Keep here as "Unanswered"         3. Move to "Answered Questions"
   (mark with "→ Gap")                  with path to research file
```

---

## Answered Questions

Questions with literature support found. Each links to a `Research_*.md` file containing sources.

### NL2SQL in Healthcare

| Question | Research File |
|----------|---------------|
| What NL2SQL systems have been applied to healthcare databases? | [`Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md`](Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md) |
| What accuracy rates have been achieved for NL2SQL on clinical data? | [`Research_What-accuracy-rates-have-been-achieved-for-NL2SQL-on-clinical-data.md`](Research_What-accuracy-rates-have-been-achieved-for-NL2SQL-on-clinical-data.md) |
| What NL2SQL datasets exist for healthcare? | [`Research_What-NL2SQL-datasets-exist-for-healthcare.md`](Research_What-NL2SQL-datasets-exist-for-healthcare.md) |

### Schema Discovery

| Question | Research File |
|----------|---------------|
| What algorithms exist for automatic PK/FK discovery from database metadata? | [`Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md`](Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md) |
| How do existing approaches validate discovered relationships (precision/recall)? | [`Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md`](Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md) |
| Has schema discovery been applied to healthcare databases specifically? | [`Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md`](Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md) |

### Knowledge Management & Workforce

| Question | Research File |
|----------|---------------|
| What is the knowledge portal paradigm and how has it been implemented? | [`Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md`](Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md) |
| What core components define an effective institutional knowledge portal? | [`Research_What-core-components-define-an-effective-institutional-knowledge-portal.md`](Research_What-core-components-define-an-effective-institutional-knowledge-portal.md) |
| What is the average tenure for IT staff at healthcare provider institutions? | [`Research_What-is-the-average-tenure-for-IT-staff-at-healthcare-provider-institutions.md`](Research_What-is-the-average-tenure-for-IT-staff-at-healthcare-provider-institutions.md) |
| What is the cost of turnover in terms of annual salary? | [`Research_What-is-the-cost-of-turnover-in-terms-of-annual-salary.md`](Research_What-is-the-cost-of-turnover-in-terms-of-annual-salary.md) |
| What is the average time to train a healthcare IT employee? | [`Research_What-is-the-average-time-to-train-a-healthcare-IT-employee.md`](Research_What-is-the-average-time-to-train-a-healthcare-IT-employee.md) |

### Healthcare Analytics Challenges

| Question | Research File |
|----------|---------------|
| Do healthcare organizations struggle to keep pace with changes in analytics? | [`Research_Do-healthcare-organizations-struggle-to-keep-pace-with-changes-in-analytics.md`](Research_Do-healthcare-organizations-struggle-to-keep-pace-with-changes-in-analytics.md) |
| Why have large-scale efforts to standardize healthcare analytics failed? | [`Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md`](Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md) |
| What are the financial benefits of low-code and conversational AI platforms? | [`Research_What-are-the-financial-benefits-of-low-code-and-conversational-AI-platforms.md`](Research_What-are-the-financial-benefits-of-low-code-and-conversational-AI-platforms.md) |

### Testing & Validation

| Question | Research File |
|----------|---------------|
| What tools exist for degrading data quality for testing? | [`Research_What-tools-exist-for-degrading-data-quality-for-testing.md`](Research_What-tools-exist-for-degrading-data-quality-for-testing.md) |

---

## Unanswered Questions

Questions needing literature search. Mark with "→ Gap" if searched but not found (also add to paper.md "Gaps in Current Literature").

### Schema Discovery and Validation

| Question | Status | Notes |
|----------|--------|-------|
| How have vector embeddings been used for schema matching or column selection? | Partial | [`Research_How-have-vector-embeddings-been-used-for-schema-matching-or-column-selection.md`](Research_How-have-vector-embeddings-been-used-for-schema-matching-or-column-selection.md) |
| What is the state of the art in semantic table/column matching for NL2SQL? | Unanswered | |

### Knowledge Management Theory

| Question | Status | Notes |
|----------|--------|-------|
| How does Nonaka's SECI model apply to organizational knowledge capture in analytics? | Unanswered | Follow-up: How have others operationalized tacit-to-explicit knowledge conversion in software systems? |

### Institutional Learning and Query Reuse

| Question | Status | Notes |
|----------|--------|-------|
| How have others measured institutional learning in analytics or BI systems? | Unanswered | |
| Have any NL2SQL systems implemented query memoization or caching? | Unanswered | |
| How have others measured efficiency gains from query reuse in database systems? | Unanswered | |

### Healthcare Terminology Mapping

| Question | Status | Notes |
|----------|--------|-------|
| What approaches exist for programmatic mapping to SNOMED, LOINC, RxNorm? | Unanswered | |
| What is the reported ETL burden for OMOP/FHIR transformation? | Unanswered | |

### Healthcare Implementation Efficiency Evidence

| Question | Status | Notes |
|----------|--------|-------|
| What quantitative efficiency metrics (time savings, task completion rates) have been reported for low-code or conversational AI in healthcare? | → Gap | Added to paper.md "Gaps in Current Literature" |
| What peer-reviewed (non-vendor-sponsored) evidence exists for cost reductions from healthcare AI/low-code implementations? | Unanswered | |
| How have healthcare organizations measured productivity gains from NL2SQL vs. traditional SQL workflows? | Unanswered | |
| What methodology has been used to measure "citizen developer" productivity in healthcare contexts? | Unanswered | |

### Clinical Safety and Security (Lower Priority)

| Question | Status | Notes |
|----------|--------|-------|
| What clinical safety considerations apply to AI-assisted healthcare analytics? | Unanswered | |
| What security architecture patterns exist for NL2SQL systems handling PHI? | Unanswered | |
| How do NIST, HITRUST, and HIPAA requirements apply to AI-enabled healthcare systems? | Unanswered | |

### Synthetic Data and Validation (Lower Priority)

| Question | Status | Notes |
|----------|--------|-------|
| How has Synthea synthetic data been used for healthcare AI/NL2SQL validation? | Unanswered | |
| What cloud architecture patterns exist for reproducible NL2SQL benchmarking? | Unanswered | |
| How have others validated NL2SQL systems on synthetic vs. real clinical data? | Unanswered | |

---

## Research File Index

All `Research_*.md` files in this directory:

| File | Topic |
|------|-------|
| `Research_Do-healthcare-organizations-struggle-to-keep-pace-with-changes-in-analytics.md` | Healthcare analytics adoption lag |
| `Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md` | Schema discovery in healthcare |
| `Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md` | Relationship validation methods |
| `Research_How-have-vector-embeddings-been-used-for-schema-matching-or-column-selection.md` | Vector embeddings for schema matching |
| `Research_What-accuracy-rates-have-been-achieved-for-NL2SQL-on-clinical-data.md` | NL2SQL benchmark accuracy |
| `Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md` | PK/FK discovery algorithms |
| `Research_What-are-the-financial-benefits-of-low-code-and-conversational-AI-platforms.md` | Low-code/AI ROI evidence |
| `Research_What-core-components-define-an-effective-institutional-knowledge-portal.md` | Knowledge portal architecture |
| `Research_What-is-the-average-tenure-for-IT-staff-at-healthcare-provider-institutions.md` | Healthcare IT tenure/turnover |
| `Research_What-is-the-average-time-to-train-a-healthcare-IT-employee.md` | Healthcare IT training time |
| `Research_What-is-the-cost-of-turnover-in-terms-of-annual-salary.md` | Turnover cost estimates |
| `Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md` | Knowledge portal paradigm |
| `Research_What-NL2SQL-datasets-exist-for-healthcare.md` | Healthcare NL2SQL datasets |
| `Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md` | Healthcare NL2SQL systems |
| `Research_What-tools-exist-for-degrading-data-quality-for-testing.md` | Data quality degradation tools |
| `Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md` | Standardization failure analysis |
