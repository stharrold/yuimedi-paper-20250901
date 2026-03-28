# Research: NL Interface Productivity Gains in Healthcare/Enterprise Analytics

**Question:** What peer-reviewed evidence exists for quantified productivity gains from natural language interfaces or conversational AI for database querying in healthcare or enterprise analytics settings?

**Scope:** Paper1 (supports R9: replace or corroborate @dadi2025 with stronger sources)

**Date searched:** 2026-03-28

**Source:** Google Scholar Labs (surfaced 10 relevant papers)

---

## Key Findings

1. **The 63%/37% statistics originate from Dadi 2025 (al-kindipublisher).** Result #8 confirmed this is the original source. It reports: 63% increase in self-service analytics adoption, 37% reduction in data retrieval time, 42% more analyst time on analysis vs query construction, and 67% reduction in time to obtain business insights.
2. **Criteria2Query (Yuan et al. 2019, JAMIA, cited 206)** is the strongest peer-reviewed healthcare-specific source: 1.22 seconds per criterion for automated cohort query formulation, 80%+ users would adopt the NL interface for future tasks. Published in JAMIA, the target journal's sibling.
3. **Nittala 2024 (cited 34)** provides empirical evidence: LLM-powered NL interface reduced ERP task completion time by 28% with lower cognitive load.
4. **Warrier 2025** reports from healthcare SaaS deployment: 484% increase in queries per user-hour, 99.7% decrease in response time, 90% reduction in support dependency.
5. **Yuluce et al. 2025 (IEEE)** conducted a PRISMA-guided systematic review and found that **meta-analysis was not possible** due to insufficient comparable quantitative outputs across studies. This is an important caveat: the field lacks standardized productivity metrics.

## Recommendation for @dadi2025 Replacement

**Option A (recommended):** Keep @dadi2025 for the specific 63%/37% statistics but add Criteria2Query (Yuan et al. 2019, JAMIA, cited 206) as a corroborating healthcare-specific citation alongside it. Yuan et al. is in JAMIA (high-impact, same publisher family as JMIR) and provides concrete efficiency data for clinical NL querying.

**Option B:** Replace @dadi2025 entirely with Nittala 2024 (cited 34) for the productivity claim (28% task time reduction) and Yuan et al. 2019 for the healthcare NL interface evidence. This drops the specific 63%/37% numbers but uses stronger venues.

**Option C:** Rewrite the sentence to use the Nittala 2024 metric (28% reduction) with Yuan et al. 2019 for healthcare context, avoiding the al-kindipublisher citation entirely.

---

## Sources

### 1. Almusallam M, Iqbal S. The Rise of Conversational BI and NLP's Impact: a Systematic Literature Review. Machines and Algorithms. 2025.

- **URL:** https://knovell.org/MnA/index.php/ojs/article/view/70
- **PDF:** https://knovell.org/MnA/index.php/ojs/article/download/70/58
- **Cited by:** new
- **Key findings:**
  - NLP-driven self-service BI: 30% greater adoption rate over 5 years (system dynamics modeling)
  - Text2SQL framework: sub-2-second response times
  - Conversational interfaces empower non-technical users in finance and healthcare

### 2. Warrier A. Agentic AI for Natural Language Query Interface in Intelligent Customer Success Management. Journal of Artificial Intelligence & Cloud Computing. 2025.

- **URL:** https://www.onlinescientificsresearch.com/articles/agentic-ai-for-natural-language-query-interface-in-intelligent-customer-success-management-conversational-analytics-and-automated-.pdf
- **Cited by:** 2
- **Key findings:**
  - Deployed in healthcare SaaS company and financial services platform (2,300+ queries)
  - **99.7% decrease in query response time**
  - **484% increase in queries answered per user-hour**
  - Report generation: hours -> minutes
  - 90% reduction in support dependency; 45% increase in proactive customer interventions
  - Annual ROI exceeding $1.56M across two deployments

### 3. Nittala EP. Leveraging Large Language Models for Natural Language Interface in ERP Systems: A Case Study in User Productivity and Cognitive Load. International Journal of Emerging Trends in Computer Science and IT. 2024.

- **URL:** https://www.ijetcsit.org/index.php/ijetcsit/article/view/458
- **PDF:** https://www.ijetcsit.org/index.php/ijetcsit/article/download/458/408
- **Cited by:** 34
- **Key findings:**
  - **LLM-powered NLI reduced mean task completion time by 28%** vs traditional ERP navigation
  - Reduced cognitive workload across all dimensions
  - Increased user confidence in performing data tasks
  - Empirical case study with objective (time, accuracy) and subjective (workload) measures

### 4. Yuan C, Ryan PB, Ta C, Guo Y, Li Z, et al. Criteria2Query: a natural language interface to clinical databases for cohort definition. Journal of the American Medical Informatics Association (JAMIA). 2019;26(4):294-305.

- **URL:** https://academic.oup.com/jamia/article-abstract/26/4/294/5308980
- **PDF:** https://academic.oup.com/jamia/article-pdf/26/4/294/34151511/ocy178.pdf
- **Cited by:** 206
- **Key findings:**
  - **Fully automatic query formulation: 1.22 seconds per criterion**
  - Total translation to structured cohort definition: 15.15 seconds per trial
  - Reduces need to master medical terminologies or SQL
  - **80%+ users would use it for future cohort definition tasks**
  - Healthcare-specific (OMOP-CDM formatted EHR databases)

### 5. Akter S, Akhter SMR, Rahman MB, et al. AI-driven business analytics for competitive advantage in service-oriented enterprises. International Journal of Business & Emerging Intelligence. 2025.

- **URL:** https://ijbei-journal.org/index.php/ijbei/article/view/25
- **PDF:** https://ijbei-journal.org/index.php/ijbei/article/download/25/25
- **Cited by:** 1
- **Key findings:**
  - 115 peer-reviewed studies synthesized
  - Conversational AI examined in 22 studies: 63.6% achieved joint efficiency + customer experience gains
  - 27.3% reported efficiency-only improvements (reduced handle time)

### 6. Pashchuk I, Turchenko I, Dombrovskyi M, et al. AI-Driven NLP to SQL Query Generation for Enhanced Human-Machine Interaction. IEEE 13th International Conference. 2025.

- **URL:** https://ieeexplore.ieee.org/abstract/document/11322204/
- **Cited by:** new
- **Key findings:**
  - Organizations adopting NL interfaces: **45-60% increase in tool utilization** among non-technical users (citing OpenAI report)
  - Without NL tools, analysts spend up to 70% of time on query formulation/debugging
  - SQL mastery requires 40-200 hours of training
  - Developed system: 1.8 second average query generation (15% faster than comparable tools)

### 7. Dadi CB. Natural Language Interfaces for Database Management: Bridging the Gap Between Users and Data through Conversational AI. Journal of Computer Science and Technology Studies (al-kindipublisher). 2025.

- **URL:** https://al-kindipublishers.org/index.php/jcsts/article/view/9694
- **PDF:** https://al-kindipublishers.org/index.php/jcsts/article/download/9694/8338
- **Cited by:** new
- **Key findings:**
  - **This is the @dadi2025 reference currently in the paper**
  - Reports 63% increase in self-service analytics adoption among non-technical staff
  - 37% reduction in time spent on data retrieval tasks
  - 42% more analyst time on analysis vs query construction
  - NLIs improved query success rates from 32% to 78%
  - 67% reduction in time to obtain business insights
  - 73% decrease in technical support requests

### 8. Greco AG. AI-Powered Cloud-Native ERP Enterprise Systems with Information Retrieval Decision Analytics. International Journal of Multidisciplinary Research in Science, Engineering, Technology & Management. 2026.

- **URL:** https://ijmrsetm.net/index.php/ijmrsetm/article/view/40
- **PDF:** https://ijmrsetm.net/index.php/ijmrsetm/article/download/40/42
- **Cited by:** new
- **Key findings:**
  - NLP-based system dramatically improved precision, recall, and query response times
  - Enhanced data accessibility across organizational hierarchies via natural language

### 9. Yuluce I, Dagdeviren F, Orun M, Duran I, et al. PRISMA Guided Systematic Review of LLM Applications in Business Intelligence. IEEE 9th International Conference. 2025.

- **URL:** https://ieeexplore.ieee.org/abstract/document/11267912/
- **Cited by:** new
- **Key findings:**
  - **Meta-analysis not possible:** insufficient comparable quantitative outputs across studies
  - Studies used heterogeneous outcomes and tailored developments
  - Synthesis remained descriptive; could not formally test for reporting bias
  - LLM-based NL interfaces have potential to reduce training costs and broaden BI adoption

### 10. Suresh A. Conversational Analytics Using LLMs: Transforming Enterprise Data Consumption through Natural Language Interfaces. American International Journal of Computer Science and Technology. 2025.

- **URL:** https://aijcst.org/index.php/aijcst/article/view/179
- **PDF:** https://aijcst.org/index.php/aijcst/article/download/179/165
- **Cited by:** new
- **Key findings:**
  - Evaluates query accuracy, response latency, and user engagement
  - Conversational analytics improves data accessibility vs traditional dashboards
