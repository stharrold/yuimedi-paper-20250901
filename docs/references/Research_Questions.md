# Research Questions

Unified tracking for all literature/research questions supporting the paper series.

**Status:** 15 answered, 14 unanswered

**Scope Key:**
- `P1` = Paper 1 (Three-Pillar Analytical Framework)
- `P2` = Paper 2 (Reference Implementation - GCP/Synthea)
- `P3` = Paper 3 (FHIR/OMOP Schema Mapping)

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

| Question | Scope | Research File |
|----------|-------|---------------|
| What NL2SQL systems have been applied to healthcare databases? | P1,P2 | [`Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md`](Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md) |
| What accuracy rates have been achieved for NL2SQL on clinical data? | P1,P2 | [`Research_What-accuracy-rates-have-been-achieved-for-NL2SQL-on-clinical-data.md`](Research_What-accuracy-rates-have-been-achieved-for-NL2SQL-on-clinical-data.md) |
| What NL2SQL datasets exist for healthcare? | P2 | [`Research_What-NL2SQL-datasets-exist-for-healthcare.md`](Research_What-NL2SQL-datasets-exist-for-healthcare.md) |

### Schema Discovery

| Question | Scope | Research File |
|----------|-------|---------------|
| What algorithms exist for automatic PK/FK discovery from database metadata? | P2 | [`Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md`](Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md) |
| How do existing approaches validate discovered relationships (precision/recall)? | P2 | [`Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md`](Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md) |
| Has schema discovery been applied to healthcare databases specifically? | P2 | [`Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md`](Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md) |

### Knowledge Management & Workforce

| Question | Scope | Research File |
|----------|-------|---------------|
| What is the knowledge portal paradigm and how has it been implemented? | P1,P2 | [`Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md`](Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md) |
| What core components define an effective institutional knowledge portal? | P2 | [`Research_What-core-components-define-an-effective-institutional-knowledge-portal.md`](Research_What-core-components-define-an-effective-institutional-knowledge-portal.md) |
| What is the average tenure for IT staff at healthcare provider institutions? | P1 | [`Research_What-is-the-average-tenure-for-IT-staff-at-healthcare-provider-institutions.md`](Research_What-is-the-average-tenure-for-IT-staff-at-healthcare-provider-institutions.md) |
| What is the cost of turnover in terms of annual salary? | P1 | [`Research_What-is-the-cost-of-turnover-in-terms-of-annual-salary.md`](Research_What-is-the-cost-of-turnover-in-terms-of-annual-salary.md) |
| What is the average time to train a healthcare IT employee? | P1 | [`Research_What-is-the-average-time-to-train-a-healthcare-IT-employee.md`](Research_What-is-the-average-time-to-train-a-healthcare-IT-employee.md) |

### Healthcare Analytics Challenges

| Question | Scope | Research File |
|----------|-------|---------------|
| Do healthcare organizations struggle to keep pace with changes in analytics? | P1 | [`Research_Do-healthcare-organizations-struggle-to-keep-pace-with-changes-in-analytics.md`](Research_Do-healthcare-organizations-struggle-to-keep-pace-with-changes-in-analytics.md) |
| Why have large-scale efforts to standardize healthcare analytics failed? | P1 | [`Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md`](Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md) |
| What are the financial benefits of low-code and conversational AI platforms? | P1 | [`Research_What-are-the-financial-benefits-of-low-code-and-conversational-AI-platforms.md`](Research_What-are-the-financial-benefits-of-low-code-and-conversational-AI-platforms.md) |

### Testing & Validation

| Question | Scope | Research File |
|----------|-------|---------------|
| What tools exist for degrading data quality for testing? | P2 | [`Research_What-tools-exist-for-degrading-data-quality-for-testing.md`](Research_What-tools-exist-for-degrading-data-quality-for-testing.md) |

---

## Unanswered Questions

Questions needing literature search. Mark with "→ Gap" if searched but not found (also add to paper.md "Gaps in Current Literature").

### Schema Discovery and Validation

| Question | Scope | Status | Notes |
|----------|-------|--------|-------|
| How have vector embeddings been used for schema matching or column selection? | P2 | Partial | [`Research_How-have-vector-embeddings-been-used-for-schema-matching-or-column-selection.md`](Research_How-have-vector-embeddings-been-used-for-schema-matching-or-column-selection.md) |
| What is the state of the art in semantic table/column matching for NL2SQL? | P2 | Unanswered | |

### Knowledge Management Theory

| Question | Scope | Status | Notes |
|----------|-------|--------|-------|
| How does Nonaka's SECI model apply to organizational knowledge capture in analytics? | P1,P2 | Unanswered | Follow-up: How have others operationalized tacit-to-explicit knowledge conversion in software systems? |

### Institutional Learning and Query Reuse

| Question | Scope | Status | Notes |
|----------|-------|--------|-------|
| How have others measured institutional learning in analytics or BI systems? | P2 | Unanswered | |
| Have any NL2SQL systems implemented query memoization or caching? | P2 | Unanswered | |
| How have others measured efficiency gains from query reuse in database systems? | P2 | Unanswered | |

### Healthcare Terminology Mapping

| Question | Scope | Status | Notes |
|----------|-------|--------|-------|
| What approaches exist for programmatic mapping to SNOMED, LOINC, RxNorm? | P3 | Unanswered | |
| What is the reported ETL burden for OMOP/FHIR transformation? | P3 | Unanswered | |

### Healthcare Implementation Efficiency Evidence

| Question | Scope | Status | Notes |
|----------|-------|--------|-------|
| What quantitative efficiency metrics (time savings, task completion rates) have been reported for low-code or conversational AI in healthcare? | P1 | → Gap | Added to paper.md "Gaps in Current Literature" |
| What peer-reviewed (non-vendor-sponsored) evidence exists for cost reductions from healthcare AI/low-code implementations? | P1 | Unanswered | |
| How have healthcare organizations measured productivity gains from NL2SQL vs. traditional SQL workflows? | P1,P2 | Unanswered | |
| What methodology has been used to measure "citizen developer" productivity in healthcare contexts? | P1 | Unanswered | |

### Clinical Safety and Security

| Question | Scope | Status | Notes |
|----------|-------|--------|-------|
| What clinical safety considerations apply to AI-assisted healthcare analytics? | P2,P3 | Unanswered | |
| What security architecture patterns exist for NL2SQL systems handling PHI? | P2 | Unanswered | |
| How do NIST, HITRUST, and HIPAA requirements apply to AI-enabled healthcare systems? | P2,P3 | Unanswered | |

### Synthetic Data and Validation

| Question | Scope | Status | Notes |
|----------|-------|--------|-------|
| How has Synthea synthetic data been used for healthcare AI/NL2SQL validation? | P2 | Unanswered | |
| What cloud architecture patterns exist for reproducible NL2SQL benchmarking? | P2 | Unanswered | |
| How have others validated NL2SQL systems on synthetic vs. real clinical data? | P2 | Unanswered | |

---

## Research File Index

All `Research_*.md` files in this directory:

| File | Topic | Scope |
|------|-------|-------|
| `Research_Do-healthcare-organizations-struggle-to-keep-pace-with-changes-in-analytics.md` | Healthcare analytics adoption lag | P1 |
| `Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md` | Schema discovery in healthcare | P2 |
| `Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md` | Relationship validation methods | P2 |
| `Research_How-have-vector-embeddings-been-used-for-schema-matching-or-column-selection.md` | Vector embeddings for schema matching | P2 |
| `Research_What-accuracy-rates-have-been-achieved-for-NL2SQL-on-clinical-data.md` | NL2SQL benchmark accuracy | P1,P2 |
| `Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md` | PK/FK discovery algorithms | P2 |
| `Research_What-are-the-financial-benefits-of-low-code-and-conversational-AI-platforms.md` | Low-code/AI ROI evidence | P1 |
| `Research_What-core-components-define-an-effective-institutional-knowledge-portal.md` | Knowledge portal architecture | P2 |
| `Research_What-is-the-average-tenure-for-IT-staff-at-healthcare-provider-institutions.md` | Healthcare IT tenure/turnover | P1 |
| `Research_What-is-the-average-time-to-train-a-healthcare-IT-employee.md` | Healthcare IT training time | P1 |
| `Research_What-is-the-cost-of-turnover-in-terms-of-annual-salary.md` | Turnover cost estimates | P1 |
| `Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md` | Knowledge portal paradigm | P1,P2 |
| `Research_What-NL2SQL-datasets-exist-for-healthcare.md` | Healthcare NL2SQL datasets | P2 |
| `Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md` | Healthcare NL2SQL systems | P1,P2 |
| `Research_What-tools-exist-for-degrading-data-quality-for-testing.md` | Data quality degradation tools | P2 |
| `Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md` | Standardization failure analysis | P1 |
