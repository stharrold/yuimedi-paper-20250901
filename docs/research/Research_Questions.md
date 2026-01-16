# Research Questions

Unified tracking for all literature/research questions supporting the paper series.

**Status:** 28 answered, 13 unanswered/partial

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
Literature Search (see [Scholar Labs Workflow](../guides/scholar-labs-workflow.md))
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
| What NL2SQL systems have been applied to healthcare databases? | Paper1,Paper2 | - | [`Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md`](Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md) |
| What accuracy rates have been achieved for NL2SQL on clinical data? | Paper1,Paper2 | - | [`Research_What-accuracy-rates-have-been-achieved-for-NL2SQL-on-clinical-data.md`](Research_What-accuracy-rates-have-been-achieved-for-NL2SQL-on-clinical-data.md) |
| What NL2SQL datasets exist for healthcare? | Paper2 | - | [`Research_What-NL2SQL-datasets-exist-for-healthcare.md`](Research_What-NL2SQL-datasets-exist-for-healthcare.md) |
| What is the state of the art in semantic table/column matching for NL2SQL? | Paper2 | [#368](https://github.com/stharrold/yuimedi-paper-20250901/issues/368) | [`Research_semantic-table-column-matching-nl2sql.md`](Research_semantic-table-column-matching-nl2sql.md) |
| What healthcare benchmarks exist for latest foundation models (GPT-5, Claude Opus 4.5)? | Paper1 | - | [`Research_What-healthcare-benchmarks-exist-for-latest-foundation-models-2025-2026.md`](Research_What-healthcare-benchmarks-exist-for-latest-foundation-models-2025-2026.md) |

### Schema Discovery

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| What algorithms exist for automatic PK/FK discovery from database metadata? | Paper2 | [#367](https://github.com/stharrold/yuimedi-paper-20250901/issues/367) | [`Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md`](Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md) |
| How do existing approaches validate discovered relationships (precision/recall)? | Paper2 | [#367](https://github.com/stharrold/yuimedi-paper-20250901/issues/367) | [`Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md`](Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md) |
| Has schema discovery been applied to healthcare databases specifically? | Paper2 | [#367](https://github.com/stharrold/yuimedi-paper-20250901/issues/367) | [`Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md`](Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md) |

### Knowledge Management & Workforce

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| What is the knowledge portal paradigm and how has it been implemented? | Paper1,Paper2 | - | [`Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md`](Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md) |
| What core components define an effective institutional knowledge portal? | Paper2 | - | [`Research_What-core-components-define-an-effective-institutional-knowledge-portal.md`](Research_What-core-components-define-an-effective-institutional-knowledge-portal.md) |
| What is the average tenure for IT staff at healthcare provider institutions? | Paper1 | - | [`Research_What-is-the-average-tenure-for-IT-staff-at-healthcare-provider-institutions.md`](Research_What-is-the-average-tenure-for-IT-staff-at-healthcare-provider-institutions.md) |
| What is the cost of turnover in terms of annual salary? | Paper1 | - | [`Research_What-is-the-cost-of-turnover-in-terms-of-annual-salary.md`](Research_What-is-the-cost-of-turnover-in-terms-of-annual-salary.md) |
| What is the average time to train a healthcare IT employee? | Paper1 | - | [`Research_What-is-the-average-time-to-train-a-healthcare-IT-employee.md`](Research_What-is-the-average-time-to-train-a-healthcare-IT-employee.md) |
| How does Nonaka's SECI model apply to organizational knowledge capture in analytics? | Paper1,Paper2 | [#372](https://github.com/stharrold/yuimedi-paper-20250901/issues/372) | [`Research_How-does-Nonakas-SECI-model-apply-to-organizational knowledge-capture-in-analytics.md`](Research_How-does-Nonakas-SECI-model-apply-to-organizational%20knowledge-capture-in-analytics.md) |
| What contemporary empirical research measures healthcare IT turnover rates? | Paper1 | - | [`Research_What-contemporary-empirical-research-measures-healthcare-IT-turnover-rates.md`](Research_What-contemporary-empirical-research-measures-healthcare-IT-turnover-rates.md) |
| How do organizations use procedural artifacts or 'Standard Work' as a ratchet mechanism to prevent organizational forgetting during periods of high employee turnover? | Paper1 | - | [`Research_procedural-artifacts-as-knowledge-ratchet.md`](Research_procedural-artifacts-as-knowledge-ratchet.md) |
| How does the 'passive capture' of a Knowledge Repository compare to the 'active capture' of a conversational interface regarding long-term sustainability? | Paper1 | - | [`Research_passive-vs-active-knowledge-capture-sustainability.md`](Research_passive-vs-active-knowledge-capture-sustainability.md) |
| How has Root Cause Analysis (RCA) been applied to workforce turnover in healthcare to identify systemic drivers? | Paper1 | - | [`Research_RCA-application-to-workforce-turnover.md`](Research_RCA-application-to-workforce-turnover.md) |

### Healthcare Analytics Challenges

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| Do healthcare organizations struggle to keep pace with changes in analytics? | Paper1 | - | [`Research_Do-healthcare-organizations-struggle-to-keep-pace-with-changes-in-analytics.md`](Research_Do-healthcare-organizations-struggle-to-keep-pace-with-changes-in-analytics.md) |
| Why have large-scale efforts to standardize healthcare analytics failed? | Paper1 | - | [`Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md`](Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md) |
| What are the financial benefits of low-code and conversational AI platforms? | Paper1 | - | [`Research_What-are-the-financial-benefits-of-low-code-and-conversational-AI-platforms.md`](Research_What-are-the-financial-benefits-of-low-code-and-conversational-AI-platforms.md) |
| What peer-reviewed evidence exists for cost reductions from healthcare AI/low-code implementations? | Paper1 | [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373) | [`Research_low-code-platform-healthcare-cost-roi-evidence.md`](Research_low-code-platform-healthcare-cost-roi-evidence.md) |
| How have healthcare organizations measured productivity gains from NL2SQL vs. traditional SQL workflows? | Paper1,Paper2 | [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373) | [`Research_How-have-healthcare-organizations-measured-productivity-gains-from-NL2SQL-vs-traditional-SQL.md`](Research_How-have-healthcare-organizations-measured-productivity-gains-from-NL2SQL-vs-traditional-SQL.md) |
| What evidence supports applying code modernization principles to natural language interfaces for legacy data access? | Paper1 | [#377](https://github.com/stharrold/yuimedi-paper-20250901/issues/377) | [`Research_What-evidence-supports-applying-code-modernization-principles-to-natural-language-interfaces-for-legacy-data-access.md`](Research_What-evidence-supports-applying-code-modernization-principles-to-natural-language-interfaces-for-legacy-data-access.md) |
| What Quantitative efficiency metrics have been reported for low-code or conversational AI in healthcare analytics? | Paper1 | [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373) | [`Research_What-efficiency-metrics-have-been-reported-for-NL2SQL-or-conversational-analytics-in-healthcare.md`](Research_What-efficiency-metrics-have-been-reported-for-NL2SQL-or-conversational-analytics-in-healthcare.md) |
| What efficiency metrics have been reported for NL2SQL or conversational analytics in healthcare? | Paper1 | [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373) | [`Research_What-efficiency-metrics-have-been-reported-for-NL2SQL-or-conversational-analytics-in-healthcare.md`](Research_What-efficiency-metrics-have-been-reported-for-NL2SQL-or-conversational-analytics-in-healthcare.md) |
| Do code-based Semantic Layers suffer from 'schema rot' in healthcare environments? | Paper1,Paper2 | - | [`Research_Do-code-based-Semantic-Layers-suffer-from-schema-rot-in-healthcare.md`](Research_Do-code-based-Semantic-Layers-suffer-from-schema-rot-in-healthcare.md) |
| Does the rigidity of centralized semantic models drive analysts toward 'Shadow IT' (extracting raw data to Excel), thereby defeating the governance model? | Paper1 | - | [`Research_Centralized-Semantic-Models-vs-Shadow-IT.md`](Research_Centralized-Semantic-Models-vs-Shadow-IT.md) |

### Knowledge Transfer and Tacit Knowledge

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| What evidence exists that tacit analytical knowledge is difficult to document and transfer through traditional means? | Paper1 | [#378](https://github.com/stharrold/yuimedi-paper-20250901/issues/378) | [`Research_Tacit-Knowledge-Documentation-and-Clinical-Impacts.md`](Research_Tacit-Knowledge-Documentation-and-Clinical-Impacts.md) |

### Clinical Impact and Outcomes

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| What evidence links healthcare analytics maturity gaps to patient care quality and clinical outcomes? | Paper1 | [#379](https://github.com/stharrold/yuimedi-paper-20250901/issues/379) | [`Research_Tacit-Knowledge-Documentation-and-Clinical-Impacts.md`](Research_Tacit-Knowledge-Documentation-and-Clinical-Impacts.md) |
| What evidence links healthcare workforce turnover and institutional knowledge loss to care continuity? | Paper1 | [#380](https://github.com/stharrold/yuimedi-paper-20250901/issues/380) | [`Research_Tacit-Knowledge-Documentation-and-Clinical-Impacts.md`](Research_Tacit-Knowledge-Documentation-and-Clinical-Impacts.md) |
| What evidence demonstrates that analytics challenges have measurable implications for healthcare delivery? | Paper1 | [#381](https://github.com/stharrold/yuimedi-paper-20250901/issues/381) | [`Research_Tacit-Knowledge-Documentation-and-Clinical-Impacts.md`](Research_Tacit-Knowledge-Documentation-and-Clinical-Impacts.md) |

### Testing & Validation

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| What tools exist for degrading data quality for testing? | Paper2 | - | [`Research_What-tools-exist-for-degrading-data-quality-for-testing.md`](Research_What-tools-exist-for-degrading-data-quality-for-testing.md) |

### Synthetic Data and Validation

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| How has Synthea synthetic data been used for healthcare AI/NL2SQL validation? | Paper2 | [#375](https://github.com/stharrold/yuimedi-paper-20250901/issues/375) | [`Research_Synthetic-Data-and-Reproducible-Benchmarking-for-Healthcare-NL2SQL.md`](Research_Synthetic-Data-and-Reproducible-Benchmarking-for-Healthcare-NL2SQL.md) |
| What cloud architecture patterns exist for reproducible NL2SQL benchmarking? | Paper2 | [#375](https://github.com/stharrold/yuimedi-paper-20250901/issues/375) | [`Research_Synthetic-Data-and-Reproducible-Benchmarking-for-Healthcare-NL2SQL.md`](Research_Synthetic-Data-and-Reproducible-Benchmarking-for-Healthcare-NL2SQL.md) |
| How have others validated NL2SQL systems on synthetic vs. real clinical data? | Paper2 | [#375](https://github.com/stharrold/yuimedi-paper-20250901/issues/375) | [`Research_Synthetic-Data-and-Reproducible-Benchmarking-for-Healthcare-NL2SQL.md`](Research_Synthetic-Data-and-Reproducible-Benchmarking-for-Healthcare-NL2SQL.md) |

---

## Unanswered Questions

Questions needing literature search. Mark with "→ Gap" if searched but not found (also add to paper.md "Gaps in Current Literature").

### Comparative Analysis of Alternatives

| Question | Scope | Issue | Status | Notes |
|----------|-------|-------|--------|-------|
| What are the documented long-term maintenance and security risks of 'citizen developer' low-code applications in healthcare? | Paper1 | - | Answered | [`Research_Low-Code-Risks.md`](Research_Low-Code-Risks.md) |
| How does 'time-to-insight' for unanticipated questions compare between visual dashboards and conversational interfaces? | Paper1 | - | Answered | [`Research_Visual-vs-Conversational-Time-to-Insight.md`](Research_Visual-vs-Conversational-Time-to-Insight.md) |
| Do modern 'headless' or AI-maintained semantic layers reduce 'schema rot' compared to code-based layers? | Paper1 | - | Answered | [`Research_Headless-Semantic-Layers-and-Schema-Rot.md`](Research_Headless-Semantic-Layers-and-Schema-Rot.md) |
| Does Shadow IT (Excel) provide agility benefits that formal systems miss, and can these be quantified? | Paper1 | - | Answered | [`Research_Benefits-of-Shadow-IT.md`](Research_Benefits-of-Shadow-IT.md) |

### Knowledge Management & Organizational Memory

### Human-AI Interaction & Validation

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| What frameworks exist for 'provisional validation' or 'human-in-the-loop' systems where domain knowledge is captured incrementally through iterative feedback cycles? | Paper1 | - | [`Research_frameworks-for-provisional-validation-and-hitl.md`](Research_frameworks-for-provisional-validation-and-hitl.md) |

### Schema Discovery and Validation

| Question | Scope | Issue | Status | Notes |
|----------|-------|-------|--------|-------|
| How have vector embeddings been used for schema matching or column selection? | Paper2 | [#368](https://github.com/stharrold/yuimedi-paper-20250901/issues/368) | Partial | [`Research_How-have-vector-embeddings-been-used-for-schema-matching-or-column-selection.md`](Research_How-have-vector-embeddings-been-used-for-schema-matching-or-column-selection.md) |

### Institutional Learning and Query Reuse

| Question | Scope | Issue | Research File |
|----------|-------|-------|---------------|
| How have others measured institutional learning in analytics or BI systems? | Paper2 | [#369](https://github.com/stharrold/yuimedi-paper-20250901/issues/369) | [`Research_How-have-others-measured-institutional-learning-in-analytics-or-BI-systems.md`](Research_How-have-others-measured-institutional-learning-in-analytics-or-BI-systems.md) |
| Have any NL2SQL systems implemented query memoization or caching? | Paper2 | [#369](https://github.com/stharrold/yuimedi-paper-20250901/issues/369) | [`Research_How-have-others-measured-institutional-learning-in-analytics-or-BI-systems.md`](Research_How-have-others-measured-institutional-learning-in-analytics-or-BI-systems.md) |
| How have others measured efficiency gains from query reuse in database systems? | Paper2 | [#369](https://github.com/stharrold/yuimedi-paper-20250901/issues/369) | [`Research_How-have-others-measured-institutional-learning-in-analytics-or-BI-systems.md`](Research_How-have-others-measured-institutional-learning-in-analytics-or-BI-systems.md) |

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
| `Research_Tacit-Knowledge-Documentation-and-Clinical-Impacts.md` | Tacit knowledge and clinical impacts | Paper1 |
| `Research_low-code-platform-healthcare-cost-roi-evidence.md` | Low-code platform healthcare ROI evidence | Paper1 |
| `Research_What-NL2SQL-datasets-exist-for-healthcare.md` | Healthcare NL2SQL datasets | Paper2 |
| `Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md` | Healthcare NL2SQL systems | Paper1,Paper2 |
| `Research_semantic-table-column-matching-nl2sql.md` | Semantic table/column matching for NL2SQL | Paper2 |
| `Research_What-tools-exist-for-degrading-data-quality-for-testing.md` | Data quality degradation tools | Paper2 |
| `Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md` | Standardization failure analysis | Paper1 |
| `Research_How-have-healthcare-organizations-measured-productivity-gains-from-NL2SQL-vs-traditional-SQL.md` | NL2SQL healthcare productivity measurement | Paper1,Paper2 |
| `Research_What-evidence-supports-applying-code-modernization-principles-to-natural-language-interfaces-for-legacy-data-access.md` | Code modernization for NL interfaces | Paper1 |
| `Research_What-evidence-exists-that-tacit-analytical-knowledge-is-difficult-to-document-and-transfer-through-traditional-means.md` | Tacit knowledge documentation difficulty | Paper1 |
| `Research_What-evidence-links-healthcare-analytics-maturity-gaps-to-patient-care-quality-and-clinical-outcomes.md` | Analytics maturity and patient outcomes | Paper1 |
| `Research_What-evidence-links-healthcare-workforce-turnover-and-institutional-knowledge-loss-to-care-continuity.md` | Workforce turnover and care continuity | Paper1 |
| `Research_What-evidence-demonstrates-that-analytics-challenges-have-measurable-implications-for-healthcare-delivery.md` | Analytics challenges and healthcare delivery | Paper1 |
| `Research_Low-Code-Risks.md` | Low-code maintenance and security risks | Paper1 |
| `Research_Visual-vs-Conversational-Time-to-Insight.md` | Time-to-insight comparison | Paper1 |
| `Research_Headless-Semantic-Layers-and-Schema-Rot.md` | Headless semantic layers and schema rot | Paper1 |
| `Research_Synthetic-Data-and-Reproducible-Benchmarking-for-Healthcare-NL2SQL.md` | Synthetic data benchmarking | Paper2 |
| `Research_Benefits-of-Shadow-IT.md` | Benefits of Shadow IT (Agility) | Paper1 |
| `Research_How-have-others-measured-institutional-learning-in-analytics-or-BI-systems.md` | Institutional learning metrics | Paper2 |
| `Research_Clinical-Safety-and-Security-Considerations-for-AI-Assisted-Healthcare-Analytics.md` | Clinical safety and security | Paper2,Paper3 |
| `Research_What-efficiency-metrics-have-been-reported-for-NL2SQL-or-conversational-analytics-in-healthcare.md` | NL2SQL efficiency metrics | Paper1 |
| `Research_RCA-application-to-workforce-turnover.md` | RCA application to workforce turnover | Paper1 |
