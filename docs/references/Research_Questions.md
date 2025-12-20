# Research Questions

Unified tracking for all literature/research questions supporting the paper series.

**Status:** 17 answered, 21 unanswered

**Scope Key:**
- `Paper1` = Three-Pillar Analytical Framework
- `Paper2` = Reference Implementation (GCP/Synthea)
- `Paper3` = FHIR/OMOP Schema Mapping

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

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| What NL2SQL systems have been applied to healthcare databases? | Paper1,Paper2 | — | [`Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md`](Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md) |
| What accuracy rates have been achieved for NL2SQL on clinical data? | Paper1,Paper2 | — | [`Research_What-accuracy-rates-have-been-achieved-for-NL2SQL-on-clinical-data.md`](Research_What-accuracy-rates-have-been-achieved-for-NL2SQL-on-clinical-data.md) |
| What NL2SQL datasets exist for healthcare? | Paper2 | — | [`Research_What-NL2SQL-datasets-exist-for-healthcare.md`](Research_What-NL2SQL-datasets-exist-for-healthcare.md) |
| What is the state of the art in semantic table/column matching for NL2SQL? | Paper2 | [#368](https://github.com/stharrold/yuimedi-paper-20250901/issues/368) | [`Research_semantic-table-column-matching-nl2sql.md`](Research_semantic-table-column-matching-nl2sql.md) |

### Schema Discovery

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| What algorithms exist for automatic PK/FK discovery from database metadata? | Paper2 | [#367](https://github.com/stharrold/yuimedi-paper-20250901/issues/367) | [`Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md`](Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md) |
| How do existing approaches validate discovered relationships (precision/recall)? | Paper2 | [#367](https://github.com/stharrold/yuimedi-paper-20250901/issues/367) | [`Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md`](Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md) |
| Has schema discovery been applied to healthcare databases specifically? | Paper2 | [#367](https://github.com/stharrold/yuimedi-paper-20250901/issues/367) | [`Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md`](Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md) |

### Knowledge Management & Workforce

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| What is the knowledge portal paradigm and how has it been implemented? | Paper1,Paper2 | — | [`Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md`](Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md) |
| What core components define an effective institutional knowledge portal? | Paper2 | — | [`Research_What-core-components-define-an-effective-institutional-knowledge-portal.md`](Research_What-core-components-define-an-effective-institutional-knowledge-portal.md) |
| What is the average tenure for IT staff at healthcare provider institutions? | Paper1 | — | [`Research_What-is-the-average-tenure-for-IT-staff-at-healthcare-provider-institutions.md`](Research_What-is-the-average-tenure-for-IT-staff-at-healthcare-provider-institutions.md) |
| What is the cost of turnover in terms of annual salary? | Paper1 | — | [`Research_What-is-the-cost-of-turnover-in-terms-of-annual-salary.md`](Research_What-is-the-cost-of-turnover-in-terms-of-annual-salary.md) |
| What is the average time to train a healthcare IT employee? | Paper1 | — | [`Research_What-is-the-average-time-to-train-a-healthcare-IT-employee.md`](Research_What-is-the-average-time-to-train-a-healthcare-IT-employee.md) |
| How does Nonaka's SECI model apply to organizational knowledge capture in analytics? | Paper1,Paper2 | [#372](https://github.com/stharrold/yuimedi-paper-20250901/issues/372) | [`Research_How-does-Nonakas-SECI-model-apply-to-organizational knowledge-capture-in-analytics.md`](Research_How-does-Nonakas-SECI-model-apply-to-organizational%20knowledge-capture-in-analytics.md) |

### Healthcare Analytics Challenges

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| Do healthcare organizations struggle to keep pace with changes in analytics? | Paper1 | — | [`Research_Do-healthcare-organizations-struggle-to-keep-pace-with-changes-in-analytics.md`](Research_Do-healthcare-organizations-struggle-to-keep-pace-with-changes-in-analytics.md) |
| Why have large-scale efforts to standardize healthcare analytics failed? | Paper1 | — | [`Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md`](Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md) |
| What are the financial benefits of low-code and conversational AI platforms? | Paper1 | — | [`Research_What-are-the-financial-benefits-of-low-code-and-conversational-AI-platforms.md`](Research_What-are-the-financial-benefits-of-low-code-and-conversational-AI-platforms.md) |

### Testing & Validation

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| What tools exist for degrading data quality for testing? | Paper2 | — | [`Research_What-tools-exist-for-degrading-data-quality-for-testing.md`](Research_What-tools-exist-for-degrading-data-quality-for-testing.md) |

---

## Unanswered Questions

Questions needing literature search. Mark with "→ Gap" if searched but not found (also add to paper.md "Gaps in Current Literature").

### Schema Discovery and Validation

| Question | Scope | Issue | Status | Notes |
|----------|-------|-------|--------|-------|
| How have vector embeddings been used for schema matching or column selection? | Paper2 | [#368](https://github.com/stharrold/yuimedi-paper-20250901/issues/368) | Partial | [`Research_How-have-vector-embeddings-been-used-for-schema-matching-or-column-selection.md`](Research_How-have-vector-embeddings-been-used-for-schema-matching-or-column-selection.md) |

### Institutional Learning and Query Reuse

| Question | Scope | Issue | Status | Notes |
|----------|-------|-------|--------|-------|
| How have others measured institutional learning in analytics or BI systems? | Paper2 | [#369](https://github.com/stharrold/yuimedi-paper-20250901/issues/369) | Unanswered | |
| Have any NL2SQL systems implemented query memoization or caching? | Paper2 | [#369](https://github.com/stharrold/yuimedi-paper-20250901/issues/369) | Unanswered | |
| How have others measured efficiency gains from query reuse in database systems? | Paper2 | [#369](https://github.com/stharrold/yuimedi-paper-20250901/issues/369) | Unanswered | |

### Healthcare Terminology Mapping

| Question | Scope | Issue | Status | Notes |
|----------|-------|-------|--------|-------|
| What approaches exist for programmatic mapping to SNOMED, LOINC, RxNorm? | Paper3 | [#370](https://github.com/stharrold/yuimedi-paper-20250901/issues/370) | Unanswered | |
| What is the reported ETL burden for OMOP/FHIR transformation? | Paper3 | [#370](https://github.com/stharrold/yuimedi-paper-20250901/issues/370) | Unanswered | |

### Healthcare Implementation Efficiency Evidence

| Question | Scope | Issue | Status | Notes |
|----------|-------|-------|--------|-------|
| What quantitative efficiency metrics (time savings, task completion rates) have been reported for low-code or conversational AI in healthcare? | Paper1 | [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373) | → Gap | Added to paper.md "Gaps in Current Literature" |
| What peer-reviewed (non-vendor-sponsored) evidence exists for cost reductions from healthcare AI/low-code implementations? | Paper1 | [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373) | Partial | Healthcare AI evidence found (10 papers); low-code platform evidence = Gap. See [`Research_What-peer-reviewed-evidence-exists-for-cost-reductions-from-healthcare-AI-low-code-implementations.md`](Research_What-peer-reviewed-evidence-exists-for-cost-reductions-from-healthcare-AI-low-code-implementations.md) |
| How have healthcare organizations measured productivity gains from NL2SQL vs. traditional SQL workflows? | Paper1,Paper2 | [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373) | Partial | General NL2SQL productivity evidence found (67% latency reduction, 10K+ users); healthcare-specific measurement = Gap. See [`Research_What-evidence-exists-for-NL2SQL-productivity-gains-compared-to-traditional-SQL.md`](Research_What-evidence-exists-for-NL2SQL-productivity-gains-compared-to-traditional-SQL.md) |
| What methodology has been used to measure "citizen developer" productivity in healthcare contexts? | Paper1 | [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373) | Partial | EUC satisfaction/effectiveness frameworks found (EUCS, TTF, SEM); Callinan & Perry (2024) CSFs most relevant; healthcare-specific citizen developer metrics = Gap. See [`Research_What-methodology-has-been-used-to-measure-citizen-developer-productivity-in-healthcare-contexts.md`](Research_What-methodology-has-been-used-to-measure-citizen-developer-productivity-in-healthcare-contexts.md) |

### Code Modernization and NL Interfaces

| Question | Scope | Issue | Status | Notes |
|----------|-------|-------|--------|-------|
| What evidence supports applying code modernization principles to natural language interfaces for legacy data access? | Paper1 | [#377](https://github.com/stharrold/yuimedi-paper-20250901/issues/377) | Unanswered | Support for claim re: [I8] |

### Knowledge Transfer and Documentation

| Question | Scope | Issue | Status | Notes |
|----------|-------|-------|--------|-------|
| What evidence exists that tacit analytical knowledge is difficult to document and transfer through traditional means? | Paper1 | [#378](https://github.com/stharrold/yuimedi-paper-20250901/issues/378) | Unanswered | Support for institutional memory loss claim |

### Clinical Impact and Healthcare Delivery

| Question | Scope | Issue | Status | Notes |
|----------|-------|-------|--------|-------|
| What evidence links healthcare analytics maturity gaps to patient care quality and clinical outcomes? | Paper1 | [#379](https://github.com/stharrold/yuimedi-paper-20250901/issues/379) | Unanswered | Support for "patient outcomes" claim |
| What evidence links healthcare workforce turnover and institutional knowledge loss to care continuity? | Paper1 | [#380](https://github.com/stharrold/yuimedi-paper-20250901/issues/380) | Unanswered | Support for "care continuity" claim |
| What evidence demonstrates that analytics challenges have measurable implications for healthcare delivery? | Paper1 | [#381](https://github.com/stharrold/yuimedi-paper-20250901/issues/381) | Unanswered | Support for "healthcare delivery" claim |

### Clinical Safety and Security

| Question | Scope | Issue | Status | Notes |
|----------|-------|-------|--------|-------|
| What clinical safety considerations apply to AI-assisted healthcare analytics? | Paper2,Paper3 | [#374](https://github.com/stharrold/yuimedi-paper-20250901/issues/374) | Unanswered | |
| What security architecture patterns exist for NL2SQL systems handling PHI? | Paper2 | [#374](https://github.com/stharrold/yuimedi-paper-20250901/issues/374) | Unanswered | |
| How do NIST, HITRUST, and HIPAA requirements apply to AI-enabled healthcare systems? | Paper2,Paper3 | [#374](https://github.com/stharrold/yuimedi-paper-20250901/issues/374) | Unanswered | |

### Synthetic Data and Validation

| Question | Scope | Issue | Status | Notes |
|----------|-------|-------|--------|-------|
| How has Synthea synthetic data been used for healthcare AI/NL2SQL validation? | Paper2 | [#375](https://github.com/stharrold/yuimedi-paper-20250901/issues/375) | Unanswered | |
| What cloud architecture patterns exist for reproducible NL2SQL benchmarking? | Paper2 | [#375](https://github.com/stharrold/yuimedi-paper-20250901/issues/375) | Unanswered | |
| How have others validated NL2SQL systems on synthetic vs. real clinical data? | Paper2 | [#375](https://github.com/stharrold/yuimedi-paper-20250901/issues/375) | Unanswered | |

---

## Research File Index

All `Research_*.md` files in this directory:

| File | Topic | Scope |
|------|-------|-------|
| `Research_Do-healthcare-organizations-struggle-to-keep-pace-with-changes-in-analytics.md` | Healthcare analytics adoption lag | Paper1 |
| `Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md` | Schema discovery in healthcare | Paper2 |
| `Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md` | Relationship validation methods | Paper2 |
| `Research_How-does-Nonakas-SECI-model-apply-to-organizational knowledge-capture-in-analytics.md` | SECI model for knowledge capture | Paper1,Paper2 |
| `Research_How-have-vector-embeddings-been-used-for-schema-matching-or-column-selection.md` | Vector embeddings for schema matching | Paper2 |
| `Research_What-peer-reviewed-evidence-exists-for-cost-reductions-from-healthcare-AI-low-code-implementations.md` | Healthcare AI cost reduction evidence | Paper1 |
| `Research_What-evidence-exists-for-NL2SQL-productivity-gains-compared-to-traditional-SQL.md` | NL2SQL productivity evidence | Paper1,Paper2 |
| `Research_What-accuracy-rates-have-been-achieved-for-NL2SQL-on-clinical-data.md` | NL2SQL benchmark accuracy | Paper1,Paper2 |
| `Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md` | PK/FK discovery algorithms | Paper2 |
| `Research_What-are-the-financial-benefits-of-low-code-and-conversational-AI-platforms.md` | Low-code/AI ROI evidence | Paper1 |
| `Research_What-core-components-define-an-effective-institutional-knowledge-portal.md` | Knowledge portal architecture | Paper2 |
| `Research_What-is-the-average-tenure-for-IT-staff-at-healthcare-provider-institutions.md` | Healthcare IT tenure/turnover | Paper1 |
| `Research_What-is-the-average-time-to-train-a-healthcare-IT-employee.md` | Healthcare IT training time | Paper1 |
| `Research_What-is-the-cost-of-turnover-in-terms-of-annual-salary.md` | Turnover cost estimates | Paper1 |
| `Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md` | Knowledge portal paradigm | Paper1,Paper2 |
| `Research_What-methodology-has-been-used-to-measure-citizen-developer-productivity-in-healthcare-contexts.md` | Citizen developer productivity measurement | Paper1 |
| `Research_What-NL2SQL-datasets-exist-for-healthcare.md` | Healthcare NL2SQL datasets | Paper2 |
| `Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md` | Healthcare NL2SQL systems | Paper1,Paper2 |
| `Research_semantic-table-column-matching-nl2sql.md` | Semantic table/column matching for NL2SQL | Paper2 |
| `Research_What-tools-exist-for-degrading-data-quality-for-testing.md` | Data quality degradation tools | Paper2 |
| `Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md` | Standardization failure analysis | Paper1 |
