# Research: Efficiency Metrics for NL2SQL/Conversational Analytics in Healthcare

**Question:** What efficiency metrics have been reported for natural language to SQL or conversational analytics interfaces in healthcare data querying?

**Scope:** Paper1 (primary), Paper2

**Status:** Substantially Answered - User productivity metrics now documented (updated 2025-12-20)

**Search Date:** 2025-12-20

**Search Method:** Google Scholar Labs (samuel.harrold@synavistra.ai)

**Related Issues:** [#373](https://github.com/stharrold/yuimedi-paper-20250901/issues/373)

---

## Summary

Healthcare-specific NL2SQL efficiency metrics are now **substantially documented**. Evidence comes from:
1. Recent papers (2024-2025) on LLM-based text-to-SQL for clinical databases
2. Criteria2Query system for OMOP CDM (2019, well-cited)
3. General conversational BI literature with healthcare mentioned as application domain
4. **NEW:** User productivity studies comparing NL interfaces to traditional SQL (2018-2025)

**Key Quantitative Findings:**
- **76.4% less preparation time** for NL queries vs SQL (Dadi, 2025)
- **70.6% reduction** in complex query formulation time (24.5 min → 7.2 min)
- **37% reduction** in healthcare data retrieval time
- **Hours vs days** for complex clinical queries (Safari & Patrick, 2018)
- **10-30% faster** query completion in user studies (Ipeirotis & Zheng, 2025)

**Gap Assessment:** The gap is now **substantially filled**. User productivity metrics exist for NL vs SQL comparisons, including healthcare-specific studies. Remaining gaps: longitudinal studies, learning curve measurements, and large-scale healthcare analyst cohorts.

---

## Key Findings: Healthcare-Specific NL2SQL

### MedT5SQL (2024) - Healthcare Text-to-SQL
**Citation:** Marshan A, Almutairi AN, Joannou A, Bell D. MedT5SQL: a transformers-based large language model for text-to-SQL conversion in the healthcare domain. Frontiers in Big Data. 2024. Cited by 14.

**Metrics Reported:**
| Metric | MIMICSQL Dataset | WikiSQL Dataset |
|--------|------------------|-----------------|
| Exact Match Accuracy | 80.63% | 44.2% |
| String-Matching Accuracy | 98.937% | 94.26% |
| Manual Evaluation Accuracy | 90% | - |

**Relevance:** Directly addresses healthcare EMR retrieval via NL-to-SQL. MIMICSQL is healthcare-specific benchmark.

---

### Criteria2Query (2019) - NL Interface to Clinical Databases
**Citation:** Yuan C, Ryan PB, Ta C, Guo Y, Li Z, et al. Criteria2Query: a natural language interface to clinical databases for cohort definition. Journal of the American Medical Informatics Association. 2019;26(4):294-305. Cited by 201.

**Metrics Reported:**
| Metric | Value |
|--------|-------|
| Automatic Query Speed | 1.22 seconds per criterion |
| Total Translation Time | 15.15 seconds (trial → OMOP cohort) |

**Relevance:** Highly cited. NL interface to OMOP CDM for clinical trial cohort definition. Time-based efficiency metrics.

---

### SQL Query Automation with LLMs (2025)
**Citation:** Tanković N, Šajina R, Lorencin I. Transforming Medical Data Access: The Role and Challenges of Recent Language Models in SQL Query Automation. Algorithms. 2025. Cited by 5.

**Metrics Reported:**
| Metric | Value |
|--------|-------|
| Cost per Query (GPT-4o-mini) | USD 0.00029 |
| Trade-off Analysis | Accuracy vs. consistency vs. token costs |

**Relevance:** Cost-effectiveness metrics for LLM-based SQL generation from medical questions.

---

### NLP-PIER Clinical Query Tool (2018)
**Citation:** Hultman G, McEwan R, Pakhomov S, et al. Usability evaluation of an unstructured clinical document query tool for researchers. AMIA Summits on Translational Science Proceedings. 2018. Cited by 10.

**Metrics Reported:**
- Time on task
- Task completion rate
- User acceptance (survey scores)

**Relevance:** Usability evaluation of NLP system for querying unstructured clinical notes. Measured efficiency via time-on-task.

---

### NLP Data Entry Efficiency (2019)
**Citation:** Han J, Chen K, Fang L, Zhang S, Wang F. Improving the efficacy of the data entry process for clinical research with a natural language processing–driven medical information extraction system. JMIR Medical Informatics. 2019. Cited by 26.

**Metrics Reported:**
| Metric | Congenital Heart Disease | Pneumonia |
|--------|--------------------------|-----------|
| Time Reduction vs. Manual | 33% | 31% |
| Accuracy Improvement | 15% | 18% |

**Relevance:** RCT evaluation of NLP-driven data entry in Chinese healthcare. Quantitative time savings.

---

## Key Findings: Conversational BI/Analytics (Healthcare Mentioned)

### Conversational BI Systematic Review (2025)
**Citation:** Almusallam M, Iqbal S. The Rise of Conversational BI and NLP's Impact: a Systematic Literature Review. Machines and Algorithms. 2025.

**Metrics Reported:**
| Metric | Value |
|--------|-------|
| Self-Service Adoption Increase | Up to 30% |
| BI Pattern Recommendation Precision (BI-REC) | 91.9% |

**Application to Healthcare:** Notes NLP for instantaneous analytics is relevant to finance, healthcare, and retail sectors.

**Relevance:** Conversational Business Intelligence metrics; healthcare explicitly mentioned as application domain.

---

### NLP for Data Query Systems Survey (2021)
**Citation:** Wong A, Joiner D, Chiu C, Elsayed M. A survey of natural language processing implementation for data query systems. IEEE Recent Advances. 2021. Cited by 21.

**Metrics Reported:**
| Metric | Value |
|--------|-------|
| Query Accuracy (rule-based, limited scope) | 98.89% |
| Test Cases | 2,880 |

**Relevance:** General NL-to-SQL survey covering Spider/WikiSQL benchmarks.

---

## Key Findings: User Productivity Studies (NL vs SQL Comparison)

### NL Interfaces for Database Management (2025) - Comprehensive Metrics
**Citation:** Dadi CB, et al. Natural Language Interfaces for Database Management: Bridging the Gap Between Users and Data through Conversational AI. Journal of Computer Science and Technology Studies. 2025.

**Metrics Reported:**
| Metric | Value | Context |
|--------|-------|---------|
| Preparation Time Reduction | 76.4% less | NLI vs traditional SQL |
| Net Time Savings | 58.2% | Nontechnical users completing analytical tasks |
| Complex Query Time | 24.5 min → 7.2 min (70.6% reduction) | Comparative study |
| Healthcare Data Retrieval | 37% reduction | Organizations implementing NLI |
| Analysis Time Increase | 42% more | Time on analysis vs query construction |

**Relevance:** **Critical paper** - provides comprehensive quantitative comparison with healthcare-specific data retrieval metrics.

---

### NL2SQL User Study (2025) - Controlled Comparison
**Citation:** Ipeirotis P, Zheng H. Natural Language Interfaces for Databases: What Do Users Think? arXiv preprint arXiv:2511.14718. 2025.

**Metrics Reported:**
| Metric | Value |
|--------|-------|
| Query Completion Time Improvement | 10-30% faster |
| Accuracy Improvement | 50% → 75% |
| Error Recovery Speed | 30-40 seconds faster |

**Study Design:** Compared NL2SQL system (SQL-LLM) vs traditional SQL tool (Snowflake) using participants with practical data analysis backgrounds solving realistic BI tasks.

**Relevance:** Controlled user study with practical BI tasks; directly applicable to healthcare analyst workflows.

---

### CliniDAL Clinical Query System (2014, 2018)
**Citation:** Safari L, Patrick JD. Restricted natural language based querying of clinical databases. Journal of Biomedical Informatics. 2014. Cited by 16.

**Citation:** Safari L, Patrick JD. Complex analyses on clinical information systems using restricted natural language querying to resolve time-event dependencies. Journal of Biomedical Informatics. 2018. Cited by 5.

**Metrics Reported:**
| Metric | NL (CliniDAL) | SQL | Comparison |
|--------|---------------|-----|------------|
| Complex Query Time | Few hours | Many days | Orders of magnitude |
| User Feedback | - | "Very tedious and time-consuming" | Qualitative |

**Study Design:** Three computer experts composed research questions using both SQL and CliniDAL.

**Relevance:** **Healthcare-specific** clinical data analytics language with direct NL vs SQL comparison from domain experts.

---

### Query Enterprise Data System (2020)
**Citation:** Joshi SR, Venkatesh B, Thomas D, Jiao Y, et al. A natural language and interactive end-to-end querying and reporting system. Proceedings of the 7th ACM IKDD CoDS and 25th COMAD. 2020. Cited by 6.

**System:** Query Enterprise Data (QED) - enterprise descriptive analytics via NL interfaces.

**Relevance:** Performance comparison against state-of-the-art NLIDB techniques on analytical and reporting queries.

---

## Metrics Framework from Literature

### Technical Metrics for Healthcare Chatbots (2020)
**Citation:** Abd-Alrazaq A, Safi Z, Alajlani M, Warren J, et al. Technical metrics used to evaluate health care chatbots: scoping review. Journal of Medical Internet Research. 2020. Cited by 176.

**Efficiency Metrics Identified:**
- Dialogue efficiency (steps to complete task)
- Number of conversational turns
- Time taken per session
- Task completion rate
- Response speed
- Word/concept error rate

**Relevance:** Provides metrics framework applicable to conversational analytics interfaces.

---

## Gap Analysis (Updated)

| Metric Category | Evidence Status | Notes |
|-----------------|-----------------|-------|
| Query Accuracy | **Available** | MedT5SQL, Criteria2Query, general NL2SQL |
| Query Speed/Latency | **Available** | Criteria2Query (1.22 sec/criterion), 70.6% reduction |
| Cost per Query | **Available** | LLM cost analysis ($0.00029/query) |
| Time Savings vs. Manual | **Available** | 76.4% less prep time, 37% healthcare retrieval reduction |
| User Productivity | **Available** | Dadi (2025): 58.2% net time savings; Ipeirotis (2025): 10-30% faster |
| Task Completion Rate | **Available** | Ipeirotis (2025): improved accuracy 50%→75% |
| Analyst Time-to-Insight | **Available** | 42% more time on analysis vs query construction |
| Learning Curve/Training Time | **Remaining Gap** | No comparative studies found |
| Longitudinal Studies | **Remaining Gap** | No long-term adoption/efficiency studies |
| Large-Scale Healthcare Cohorts | **Remaining Gap** | Most studies have small N (3-11 participants) |

---

## Recommendations for Paper 1

### Primary Citations for Efficiency Claims
1. **Cite Dadi (2025)** - Comprehensive NL vs SQL metrics: 76.4% prep time reduction, 37% healthcare retrieval improvement
2. **Cite Safari & Patrick (2014, 2018)** - Healthcare-specific CliniDAL: hours vs days for clinical queries
3. **Cite Ipeirotis & Zheng (2025)** - Controlled user study: 10-30% faster query completion
4. **Cite Criteria2Query (2019)** - Well-cited NL interface to OMOP CDM with time metrics

### Supporting Citations
5. **Cite MedT5SQL (2024)** for healthcare-specific NL2SQL accuracy benchmarks (80.63% on MIMICSQL)
6. **Cite Conversational BI Review (2025)** for adoption rate improvements (30%)

### Remaining Gaps to Acknowledge
7. **Learning curve studies** - No comparative data on training time for NL vs SQL
8. **Large-scale healthcare cohorts** - Most studies have N=3-11; need larger analyst populations
9. **Longitudinal adoption** - No long-term efficiency studies in healthcare settings

### Paper 2 Opportunity
10. **Synthea-based evaluation** can address remaining gaps with controlled healthcare analyst studies

---

## Search Queries Used

1. "What quantitative efficiency metrics (time savings, task completion rates) have been reported for low-code or conversational AI in healthcare?" → 10 results (mostly patient-facing, not analytics)

2. "What efficiency metrics have been reported for natural language to SQL or conversational analytics interfaces in healthcare data querying?" → 10 results (analytics-specific, more relevant)

3. "What user studies have compared analyst time-to-insight or task completion time between natural language query interfaces and traditional SQL for clinical or healthcare data analysis?" → 10+ results (**key findings: Dadi 2025, Ipeirotis 2025, Safari & Patrick 2014/2018**)

---

## References (BibTeX)

```bibtex
@article{marshan2024medt5sql,
  title={MedT5SQL: a transformers-based large language model for text-to-SQL conversion in the healthcare domain},
  author={Marshan, A and Almutairi, AN and Joannou, A and Bell, D},
  journal={Frontiers in Big Data},
  year={2024},
  publisher={Frontiers}
}

@article{yuan2019criteria2query,
  title={Criteria2Query: a natural language interface to clinical databases for cohort definition},
  author={Yuan, Chi and Ryan, Patrick B and Ta, Casey and Guo, Yixuan and Li, Ziran and others},
  journal={Journal of the American Medical Informatics Association},
  volume={26},
  number={4},
  pages={294--305},
    year={2019},
    publisher={Oxford University Press},
    file={../library/docs/2019_Yuan_JAMIA_Criteria2Query.pdf}
}

@article{tankovic2025transforming,
  title={Transforming Medical Data Access: The Role and Challenges of Recent Language Models in SQL Query Automation},
  author={Tankovi{\'c}, N and {\v{S}}ajina, R and Lorencin, I},
  journal={Algorithms},
  year={2025},
  publisher={MDPI}
}

@article{almusallam2025conversational,
  title={The Rise of Conversational BI and NLP's Impact: a Systematic Literature Review},
  author={Almusallam, M and Iqbal, S},
  journal={Machines and Algorithms},
  year={2025}
}

@article{abd2020technical,
  title={Technical metrics used to evaluate health care chatbots: scoping review},
  author={Abd-Alrazaq, Alaa and Safi, Zeineb and Alajlani, Mohannad and Warren, Jim and others},
  journal={Journal of Medical Internet Research},
  volume={22},
  number={6},
  pages={e18301},
  year={2020}
}

@article{dadi2025natural,
  title={Natural Language Interfaces for Database Management: Bridging the Gap Between Users and Data through Conversational AI},
  author={Dadi, Chaitanya Bharat and Hoque, Md Refadul and Ali, Md Musa and Ferdausi, Shaharia and Fatema, Kanis and Hasan, Md Rakibul},
  journal={Journal of Computer Science and Technology Studies},
  volume={7},
  number={3},
  pages={927--933},
  year={2025},
  publisher={Al-Kindi Center for Research and Development},
  doi={10.32996/jcsts.2025.7.3.103},
  url={https://al-kindipublisher.com/index.php/jcsts/article/view/9694},
  file={../library/docs/2025_Dadi_JCSTS_Natural-Language-Interfaces-Database-Management.pdf}
}

@article{ipeirotis2025natural,
  title={Natural Language Interfaces for Databases: What Do Users Think?},
  author={Ipeirotis, Panagiotis and Zheng, Haochen},
  journal={arXiv preprint arXiv:2511.14718},
  year={2025}
}

@article{safari2014restricted,
  title={Restricted natural language based querying of clinical databases},
  author={Safari, Leila and Patrick, Jon D},
  journal={Journal of Biomedical Informatics},
  volume={52},
  pages={333--353},
  year={2014},
  publisher={Elsevier}
}

@article{safari2018complex,
  title={Complex analyses on clinical information systems using restricted natural language querying to resolve time-event dependencies},
  author={Safari, Leila and Patrick, Jon D},
  journal={Journal of Biomedical Informatics},
  volume={80},
  pages={101--118},
  year={2018},
  publisher={Elsevier}
}

@inproceedings{joshi2020natural,
  title={A natural language and interactive end-to-end querying and reporting system},
  author={Joshi, SR and Venkatesh, B and Thomas, D and Jiao, Y and others},
  booktitle={Proceedings of the 7th ACM IKDD CoDS and 25th COMAD},
  pages={288--292},
  year={2020}
}
```
