# Research Questions

Unified tracking for all literature/research questions supporting the paper series.

**Status:** 38 answered (6 merged), 14 unanswered/partial

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

| Question | Scope | Issue | Research File | Merged |
|----------|-------|-------|---------------|--------|
| What NL2SQL systems have been applied to healthcare databases? | Paper1,Paper2 | - | [`Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md`](Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md) | [A75]-[A76] |
| What accuracy rates have been achieved for NL2SQL on clinical data? | Paper1,Paper2 | - | [`Research_What-accuracy-rates-have-been-achieved-for-NL2SQL-on-clinical-data.md`](Research_What-accuracy-rates-have-been-achieved-for-NL2SQL-on-clinical-data.md) | [A77] |
| What NL2SQL datasets exist for healthcare? | Paper2 | - | [`Research_What-NL2SQL-datasets-exist-for-healthcare.md`](Research_What-NL2SQL-datasets-exist-for-healthcare.md) | - |
| What is the state of the art in semantic table/column matching for NL2SQL? | Paper2 | [#368](https://github.com/stharrold/yuimedi-paper-20250901/issues/368) | [`Research_semantic-table-column-matching-nl2sql.md`](Research_semantic-table-column-matching-nl2sql.md) | - |
| What healthcare benchmarks exist for latest foundation models (GPT-5, Claude Opus 4.5)? | Paper1 | - | [`Research_What-healthcare-benchmarks-exist-for-latest-foundation-models-GPT5-Claude-Opus-4.5.md`](Research_What-healthcare-benchmarks-exist-for-latest-foundation-models-GPT5-Claude-Opus-4.5.md) | [A69]-[A72] |

### Schema Discovery

| Question | Scope | Issue | Research File | Merged |
|----------|-------|-------|---------------|--------|
| What algorithms exist for automatic PK/FK discovery from database metadata? | Paper2 | [#367](https://github.com/stharrold/yuimedi-paper-20250901/issues/367) | [`Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md`](Research_What-algorithms-exist-for-automatic-primary-foreign-key-discovery-from-database-metadata.md) | - |
| How do existing approaches validate discovered relationships (precision/recall)? | Paper2 | [#367](https://github.com/stharrold/yuimedi-paper-20250901/issues/367) | [`Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md`](Research_How-do-existing-approaches-validate-discovered-database-relationships-precision-recall.md) | - |
| Has schema discovery been applied to healthcare databases specifically? | Paper2 | [#367](https://github.com/stharrold/yuimedi-paper-20250901/issues/367) | [`Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md`](Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md) | - |

### Knowledge Management & Workforce

| Question | Scope | Issue | Research File | Merged |
|----------|-------|-------|---------------|--------|
| What is the knowledge portal paradigm and how has it been implemented? | Paper1,Paper2 | - | [`Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md`](Research_What-is-the-knowledge-portal-paradigm-and-how-has-it-been-implemented.md) | [A25] |
| What core components define an effective institutional knowledge portal? | Paper2 | - | [`Research_What-core-components-define-an-effective-institutional-knowledge-portal.md`](Research_What-core-components-define-an-effective-institutional-knowledge-portal.md) | - |
| What is the average tenure for IT staff at healthcare provider institutions? | Paper1 | - | [`Research_What-is-the-average-tenure-for-IT-staff-at-healthcare-provider-institutions.md`](Research_What-is-the-average-tenure-for-IT-staff-at-healthcare-provider-institutions.md) | [A10] |
| What is the cost of turnover in terms of annual salary? | Paper1 | - | [`Research_What-is-the-cost-of-turnover-in-terms-of-annual-salary.md`](Research_What-is-the-cost-of-turnover-in-terms-of-annual-salary.md) | [A78] |
| What is the average time to train a healthcare IT employee? | Paper1 | - | [`Research_What-is-the-average-time-to-train-a-healthcare-IT-employee.md`](Research_What-is-the-average-time-to-train-a-healthcare-IT-employee.md) | [A79] |
| How does Nonaka's SECI model apply to organizational knowledge capture in analytics? | Paper1,Paper2 | [#372](https://github.com/stharrold/yuimedi-paper-20250901/issues/372) | [`Research_How-does-Nonakas-SECI-model-apply-to-organizational knowledge-capture-in-analytics.md`](Research_How-does-Nonakas-SECI-model-apply-to-organizational%20knowledge-capture-in-analytics.md) | [A80]-[A81] |
| What contemporary empirical research measures healthcare IT turnover rates? | Paper1 | - | [`Research_What-contemporary-empirical-research-measures-healthcare-IT-turnover-rates.md`](Research_What-contemporary-empirical-research-measures-healthcare-IT-turnover-rates.md) | [A66] |

### Healthcare Analytics Challenges

| Question | Scope | Issue | Research File | Merged |
|----------|-------|-------|---------------|--------|
| Do healthcare organizations struggle to keep pace with changes in analytics? | Paper1 | - | [`Research_Do-healthcare-organizations-struggle-to-keep-pace-with-changes-in-analytics.md`](Research_Do-healthcare-organizations-struggle-to-keep-pace-with-changes-in-analytics.md) | [A74] |
| Why have large-scale efforts to standardize healthcare analytics failed? | Paper1 | - | [`Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md`](Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md) | [A26]-[A28], [I10] |
| Why did Haven, the Amazon-Berkshire-JPMorgan healthcare venture, disband in 2021? | Paper1 | - | [`Research_Why-did-Haven-the-Amazon-Berkshire-JPMorgan-healthcare-venture-disband-in-2021.md`](Research_Why-did-Haven-the-Amazon-Berkshire-JPMorgan-healthcare-venture-disband-in-2021.md) | [@acchiardo2021; @ozalp2022] |
| What are the financial benefits of low-code and conversational AI platforms? | Paper1 | - | [`Research_What-are-the-financial-benefits-of-low-code-and-conversational-AI-platforms.md`](Research_What-are-the-financial-benefits-of-low-code-and-conversational-AI-platforms.md) | [A19]-[A23], [A31]-[A34] |
| What peer-reviewed evidence exists for cost reductions from healthcare AI/low-code implementations? | Paper1 | [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373) | [`Research_low-code-platform-healthcare-cost-roi-evidence.md`](Research_low-code-platform-healthcare-cost-roi-evidence.md) | [A31]-[A34] |
| How have healthcare organizations measured productivity gains from NL2SQL vs. traditional SQL workflows? | Paper1,Paper2 | [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373) | [`Research_How-have-healthcare-organizations-measured-productivity-gains-from-NL2SQL-vs-traditional-SQL.md`](Research_How-have-healthcare-organizations-measured-productivity-gains-from-NL2SQL-vs-traditional-SQL.md) | [A35]-[A38] |
| What evidence supports applying code modernization principles to natural language interfaces for legacy data access? | Paper1 | [#377](https://github.com/stharrold/yuimedi-paper-20250901/issues/377) | [`Research_What-evidence-supports-applying-code-modernization-principles-to-natural-language-interfaces-for-legacy-data-access.md`](Research_What-evidence-supports-applying-code-modernization-principles-to-natural-language-interfaces-for-legacy-data-access.md) | [A46]-[A49], [A73] |
| What quantitative efficiency metrics have been reported for low-code or conversational AI in healthcare analytics? | Paper1 | [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373) | [`Research_What-quantitative-efficiency-metrics-have-been-reported-for-low-code-or-conversational-AI-in-healthcare-analytics.md`](Research_What-quantitative-efficiency-metrics-have-been-reported-for-low-code-or-conversational-AI-in-healthcare-analytics.md) | [A39]-[A42] |
| What efficiency metrics have been reported for NL2SQL or conversational analytics in healthcare? | Paper1 | [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373) | [`Research_What-efficiency-metrics-have-been-reported-for-NL2SQL-or-conversational-analytics-in-healthcare.md`](Research_What-efficiency-metrics-have-been-reported-for-NL2SQL-or-conversational-analytics-in-healthcare.md) | [A43]-[A45] |

### Knowledge Transfer and Tacit Knowledge

| Question | Scope | Issue | Research File | Merged |
|----------|-------|-------|---------------|--------|
| What evidence exists that tacit analytical knowledge is difficult to document and transfer through traditional means? | Paper1 | [#378](https://github.com/stharrold/yuimedi-paper-20250901/issues/378) | [`Research_What-evidence-exists-that-tacit-analytical-knowledge-is-difficult-to-document-and-transfer-through-traditional-means.md`](Research_What-evidence-exists-that-tacit-analytical-knowledge-is-difficult-to-document-and-transfer-through-traditional-means.md) | [A50]-[A53] |

### Clinical Impact and Outcomes

| Question | Scope | Issue | Research File | Merged |
|----------|-------|-------|---------------|--------|
| What evidence links healthcare analytics maturity gaps to patient care quality and clinical outcomes? | Paper1 | [#379](https://github.com/stharrold/yuimedi-paper-20250901/issues/379) | [`Research_What-evidence-links-healthcare-analytics-maturity-gaps-to-patient-care-quality-and-clinical-outcomes.md`](Research_What-evidence-links-healthcare-analytics-maturity-gaps-to-patient-care-quality-and-clinical-outcomes.md) | [A54]-[A57] |
| What evidence links healthcare workforce turnover and institutional knowledge loss to care continuity? | Paper1 | [#380](https://github.com/stharrold/yuimedi-paper-20250901/issues/380) | [`Research_What-evidence-links-healthcare-workforce-turnover-and-institutional-knowledge-loss-to-care-continuity.md`](Research_What-evidence-links-healthcare-workforce-turnover-and-institutional-knowledge-loss-to-care-continuity.md) | [A58]-[A61] |
| What evidence demonstrates that analytics challenges have measurable implications for healthcare delivery? | Paper1 | [#381](https://github.com/stharrold/yuimedi-paper-20250901/issues/381) | [`Research_What-evidence-demonstrates-that-analytics-challenges-have-measurable-implications-for-healthcare-delivery.md`](Research_What-evidence-demonstrates-that-analytics-challenges-have-measurable-implications-for-healthcare-delivery.md) | [A67]-[A68] |

### Data Quality and Schema Documentation

| Question | Scope | Issue | Research File | Merged |
|----------|-------|-------|---------------|--------|
| What is the relationship between healthcare analytics maturity levels and data quality metrics? | Paper1 | — | [`Research_what-is-the-relationship-between-healthcare-analytics-maturity-levels-and-data-quality-metrics.md`](Research_what-is-the-relationship-between-healthcare-analytics-maturity-levels-and-data-quality-metrics.md) | [@carvalho2019; @pintovalverde2013; @gokalp2023; @lismont2017] |
| What is the prevalence of data quality issues (incorrect values, missing data, duplicate records) in healthcare databases, and how does this vary by organizational analytics maturity? | Paper1 | — | [`Research_what-is-the-prevalence-of-data-quality-issues-in-healthcare-databases-and-how-does-this-vary-by-organizational-analytics-maturity.md`](Research_what-is-the-prevalence-of-data-quality-issues-in-healthcare-databases-and-how-does-this-vary-by-organizational-analytics-maturity.md) | [@yang2021; @arts2002; @mccoy2013; @zhang2024] |
| What evidence exists that domain expertise (clinical knowledge) is required to identify and correct data quality issues in healthcare databases that automated tools cannot detect? | Paper1 | — | [`Research_what-evidence-exists-that-domain-expertise-is-required-to-identify-data-quality-issues-in-healthcare-databases.md`](Research_what-evidence-exists-that-domain-expertise-is-required-to-identify-data-quality-issues-in-healthcare-databases.md) | [@rahman2020; @sirgo2018; @shi2021] |
| How common are undocumented or poorly documented database schemas (missing metadata, business rules, PK/FK relationships) in healthcare organizations? | Paper1,Paper2 | — | [`Research_how-common-are-undocumented-database-schemas-in-healthcare-organizations.md`](Research_how-common-are-undocumented-database-schemas-in-healthcare-organizations.md) | [@dugas2016; @bokov2017; @ulrich2022; @lucyk2017; @hovenga2013] |

### Testing & Validation

| Question | Scope | Issue | Research File | Merged |
|----------|-------|-------|---------------|--------|
| What tools exist for degrading data quality for testing? | Paper2 | - | [`Research_What-tools-exist-for-degrading-data-quality-for-testing.md`](Research_What-tools-exist-for-degrading-data-quality-for-testing.md) | - |

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
| What methodology has been used to measure "citizen developer" productivity in healthcare contexts? | Paper1 | [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373) | Partial | **UPDATED 2025-12-20:** 20 papers found. Gap CONFIRMED: No validated healthcare-specific citizen developer productivity instrument. See [`Research_What-methodology-has-been-used-to-measure-citizen-developer-productivity-in-healthcare-contexts.md`](Research_What-methodology-has-been-used-to-measure-citizen-developer-productivity-in-healthcare-contexts.md) |

### Failed Standardization Case Studies

| Question | Scope | Issue | Status | Notes |
|----------|-------|-------|--------|-------|
| Why did IBM sell Watson Health to Francisco Partners in 2022? | Paper1 | - | Answered | [@strickland2019; @yang2020] merged to paper.md |

### Analytics Maturity and Outcomes

| Question | Scope | Issue | Status | Notes |
|----------|-------|-------|--------|-------|
| What quantitative evidence links HIMSS AMAM stages to patient outcomes or organizational performance? | Paper1 | — | Partial | **UPDATED 2026-01-01:** Searched Scholar Labs. Found Snowdon et al. (2024) linking EMRAM to Leapfrog Safety Grades (3.25x odds). No AMAM-specific outcome studies found. Gap CONFIRMED. See [`Research_what-quantitative-evidence-links-himss-amam-stages-to-patient-outcomes-or-organizational-performance.md`](Research_what-quantitative-evidence-links-himss-amam-stages-to-patient-outcomes-or-organizational-performance.md) |

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
| `Research_low-code-platform-healthcare-cost-roi-evidence.md` | Low-code platform healthcare ROI evidence | Paper1 |
| `Research_What-NL2SQL-datasets-exist-for-healthcare.md` | Healthcare NL2SQL datasets | Paper2 |
| `Research_What-NL2SQL-systems-have-been-applied-to-healthcare-databases.md` | Healthcare NL2SQL systems | Paper1,Paper2 |
| `Research_semantic-table-column-matching-nl2sql.md` | Semantic table/column matching for NL2SQL | Paper2 |
| `Research_What-tools-exist-for-degrading-data-quality-for-testing.md` | Data quality degradation tools | Paper2 |
| `Research_Why-have-large-scale-efforts-to-standardize-healthcare-analytics-failed.md` | Standardization failure analysis | Paper1 |
| `Research_Why-did-Haven-the-Amazon-Berkshire-JPMorgan-healthcare-venture-disband-in-2021.md` | Haven healthcare venture dissolution | Paper1 |
| `Research_Why-did-IBM-sell-Watson-Health-to-Francisco-Partners-in-2022.md` | IBM Watson Health divestiture | Paper1 |
| `Research_How-have-healthcare-organizations-measured-productivity-gains-from-NL2SQL-vs-traditional-SQL.md` | NL2SQL healthcare productivity measurement | Paper1,Paper2 |
| `Research_What-evidence-supports-applying-code-modernization-principles-to-natural-language-interfaces-for-legacy-data-access.md` | Code modernization for NL interfaces | Paper1 |
| `Research_What-evidence-exists-that-tacit-analytical-knowledge-is-difficult-to-document-and-transfer-through-traditional-means.md` | Tacit knowledge documentation difficulty | Paper1 |
| `Research_What-evidence-links-healthcare-analytics-maturity-gaps-to-patient-care-quality-and-clinical-outcomes.md` | Analytics maturity and patient outcomes | Paper1 |
| `Research_What-evidence-links-healthcare-workforce-turnover-and-institutional-knowledge-loss-to-care-continuity.md` | Workforce turnover and care continuity | Paper1 |
| `Research_What-evidence-demonstrates-that-analytics-challenges-have-measurable-implications-for-healthcare-delivery.md` | Analytics challenges and healthcare delivery | Paper1 |
| `Research_what-quantitative-evidence-links-himss-amam-stages-to-patient-outcomes-or-organizational-performance.md` | HIMSS AMAM/EMRAM stages and patient outcomes | Paper1 |
| `Research_what-is-the-relationship-between-healthcare-analytics-maturity-levels-and-data-quality-metrics.md` | Analytics maturity and data quality relationship | Paper1 |
| `Research_what-is-the-prevalence-of-data-quality-issues-in-healthcare-databases-and-how-does-this-vary-by-organizational-analytics-maturity.md` | Data quality issues prevalence in healthcare | Paper1 |
| `Research_what-evidence-exists-that-domain-expertise-is-required-to-identify-data-quality-issues-in-healthcare-databases.md` | Domain expertise for healthcare data quality | Paper1 |
| `Research_how-common-are-undocumented-database-schemas-in-healthcare-organizations.md` | Undocumented schemas prevalence in healthcare | Paper1,Paper2 |
