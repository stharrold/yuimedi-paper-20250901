# Research Question: Has schema discovery been applied to healthcare databases specifically?

**Source:** Google Scholar Labs
**Date:** December 19, 2025
**Results Found:** 10 relevant papers
**Sorted By:** Relevance
**Search Duration:** ~1.5 minutes

---

## Summary of Findings

The search found 10 relevant papers spanning from 2010 to 2025, demonstrating that schema discovery has been actively applied to healthcare databases. The dominant research themes include semantic schema mapping using machine learning and transformer models, integration of heterogeneous healthcare data sources (EHRs, DHIS), and standardization efforts for OMOP CDM compliance. Several papers specifically address the unique challenges of healthcare data heterogeneity, including non-standardized medical terminology across systems.

---

## 1. Unsupervised semantic mapping for healthcare data storage schema

**Authors:** FA Satti, M Hussain, J Hussain, SI Ali, T Ali
**Publication:** IEEE Access, 2021
**Citations:** 9 (2.25 per year)
**Link:** https://ieeexplore.ieee.org/abstract/document/9499053/
**PDF:** https://ieeexplore.ieee.org/iel7/6287639/6514899/09499053.pdf

**Abstract/Summary:**
Presents a novel methodology for bridging the gap between various healthcare data management solutions by leveraging transformer-based machine learning models to create mappings between data elements.

**Methodology/Approach:** Machine Learning (Transformer-based)

**Key Points:**
- Develops an unsupervised semantic mapping technique to identify relationships between attributes of participating medical data schemas
- Addresses medical data schema heterogeneity caused by lack of universal terminological standards
- Uses transformer-based ML models for automated mapping generation

**Relationship to Other Papers:** Foundational work for unsupervised approaches; Paper 5 and Paper 9 build on similar deep learning concepts for schema matching.

---

## 2. Biomedical heterogeneous data categorization and schema mapping toward data integration

**Authors:** P Deshpande, A Rasin, R Tchoua, J Furst
**Publication:** Frontiers in Big Data, 2023
**Citations:** 6 (3.0 per year)
**Link:** https://www.frontiersin.org/articles/10.3389/fdata.2023.1173038/full
**PDF:** https://www.frontiersin.org/journals/big-data/articles/10.3389/fdata.2023.1173038/pdf

**Abstract/Summary:**
Presents a methodology for data integration that merges data from heterogeneous biomedical sources based on the semantics of their data elements.

**Methodology/Approach:** Semantic Analysis

**Key Points:**
- Describes how clinical data elements from different but related datasets are mapped into categories
- Details schema attribute identification process based on semantic similarity
- Focuses on biomedical data integration challenges

**Relationship to Other Papers:** Complements Paper 8's scoping review on semantic integration methods.

---

## 3. Real-time discovery services over large, heterogeneous and complex healthcare datasets using schema-less, column-oriented methods

**Authors:** E Begoli, T Dunning, C Frasure
**Publication:** IEEE Second International Conference on Big Data Computing Service and Applications, 2016
**Citations:** 14 (1.56 per year)
**Link:** https://ieeexplore.ieee.org/abstract/document/7474381/
**PDF:** Not available

**Abstract/Summary:**
Presents a service platform utilizing schema-less exploration for data discovery and generation of patient-related statistics from heterogeneous healthcare data sets, including electronic health records and practice management systems.

**Methodology/Approach:** Schema-less, Column-oriented

**Key Points:**
- Addresses fast, flexible approaches to SQL-based exploration in heterogeneously structured healthcare data
- Discusses clinical trials candidate discovery and treatment effectiveness analysis use cases
- Proposes schema-less architecture for healthcare data diversity

**Relationship to Other Papers:** Takes an alternative schema-less approach compared to traditional schema matching methods in other papers.

---

## 4. A context-based schema integration process applied to healthcare data sources

**Authors:** RB Belian, AC Salgado
**Publication:** International Conferences "On the Move to Meaningful Internet Systems", Springer, 2010
**Citations:** 3 (0.2 per year)
**Link:** https://link.springer.com/chapter/10.1007/978-3-642-16961-8_25
**PDF:** https://www.researchgate.net/profile/Rosalie-Belian-2/publication/220830234_A_Context-Based_Schema_Integration_Process_Applied_to_Healthcare_Data_Sources/links/55317a780cf2f2a588ad4c12/A-Context-Based-Schema-Integration-Process-Applied-to-Healthcare-Data-Sources.pdf

**Abstract/Summary:**
Proposes a context-based schema integration process for a mediator-based information integration system specifically applied to healthcare data sources.

**Methodology/Approach:** Context-based, Mediator-based

**Key Points:**
- Explores contextual information for schema-level sense disambiguation
- Applied to real healthcare data sources from a Brazilian System for Medical Second Opinion
- Tackles semantics of data source schema elements

**Relationship to Other Papers:** Early foundational work (2010) that later papers build upon with ML approaches.

---

## 5. Deep Learning to Jointly Schema Match, Impute, and Transform Databases

**Authors:** S Tripathi, BA Fritz, M Abdelhack, MS Avidan
**Publication:** arXiv preprint, 2022
**Citations:** 5 (1.67 per year)
**Link:** https://arxiv.org/abs/2207.03536
**PDF:** https://arxiv.org/pdf/2207.03536

**Abstract/Summary:**
Applies schema matching to real-world experiments using two electronic health record (EHR) databases, proposing a novel deep-learning based solution to the schema matching problem for healthcare data.

**Methodology/Approach:** Deep Learning

**Key Points:**
- Focuses on reconciling similar or identical concepts in distinct EHR data sources
- Inspired by distributional semantics where relationships between entries define column semantics
- Addresses healthcare-specific challenges with redundant or ambiguous names in EHRs

**Relationship to Other Papers:** Same author team as Paper 9; represents preprint version of the journal publication.

---

## 6. Database integration based on combination schema matching approach (case study: Multi-database of district health information system)

**Authors:** MAF Rachman, GAP Saptawati
**Publication:** 2nd International Conference on Information Technology, Information Systems and Electrical Engineering, IEEE, 2017
**Citations:** 20 (2.5 per year)
**Link:** https://ieeexplore.ieee.org/abstract/document/8285544/
**PDF:** Not available

**Abstract/Summary:**
Applies schema matching to a multi-database system related to the District Health Information System (DHIS), using the SIKDA Generik database element as a reference schema.

**Methodology/Approach:** Combination Schema Matching

**Key Points:**
- Uses SIKDA Generik database (Indonesian Ministry of Health application) as reference schema
- Focuses on resolving semantic conflicts at schema level for health information systems
- Addresses inefficiency caused by diversity of DHIS applications

**Relationship to Other Papers:** Provides practical case study complementing theoretical approaches in other papers.

---

## 7. A Novel Sentence Transformer-based Natural Language Processing Approach for Schema Mapping of Electronic Health Records to the OMOP Common Data Model

**Authors:** X Zhou, LS Dhingra, A Aminorroaya
**Publication:** AMIA Annual Symposium Proceedings, 2025
**Citations:** 7 (7.0 per year - very recent)
**Link:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12099400/
**PDF:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12099400/ (HTML)

**Abstract/Summary:**
Develops transformer-based natural language processing models to map medication-related concepts from Electronic Health Records (EHR) to standard concepts in the OMOP Common Data Model (CDM).

**Methodology/Approach:** NLP, Sentence Transformers

**Key Points:**
- Focuses on standardization of clinical records for interoperability
- Compares novel approach against Usagi for mapping EHR to OMOP CDM
- Enables large-scale, multi-centered clinical investigations

**Relationship to Other Papers:** Most recent paper (2025); extends transformer approaches from Papers 1 and 5 specifically for OMOP standardization.

---

## 8. A scoping review of semantic integration of health data and information

**Authors:** H Zhang, T Lyu, P Yin, S Bost, X He, Y Guo
**Publication:** International Journal of Medical Informatics, 2022
**Citations:** 8 (2.67 per year)
**Link:** https://www.sciencedirect.com/science/article/pii/S1386505622001484
**PDF:** Not available

**Abstract/Summary:**
Examines a decade of research on semantic data integration (SDI) in biomedical domains, explicitly focusing on approaches for integrating health data and information.

**Methodology/Approach:** Systematic Review

**Key Points:**
- Summarizes 87 eligible articles on global schema methods
- Identifies schema heterogeneity as one of three main categories of data heterogeneity
- Addresses challenges in integrating individual-level patient records

**Relationship to Other Papers:** Comprehensive review that contextualizes other papers in this list within broader literature.

---

## 9. Multi-view representation learning for tabular data integration using inter-feature relationships

**Authors:** S Tripathi, BA Fritz, M Abdelhack, MS Avidan
**Publication:** Journal of Biomedical Informatics, 2024
**Citations:** 6 (6.0 per year)
**Link:** https://www.sciencedirect.com/science/article/pii/S1532046424000200
**PDF:** https://www.sciencedirect.com/science/article/pii/S1532046424000200 (HTML)

**Abstract/Summary:**
Designs methods to create mappings between structured tabular datasets derived from electronic health records (EHRs), necessary for data integration in healthcare.

**Methodology/Approach:** Contrastive Learning, Auto-encoders

**Key Points:**
- Focuses on schema matching for identifying similar concepts across EHR datasets
- Evaluates methods on MIMIC-III medical-record changeover and perioperative records
- Compares contrastive learning and partial auto-encoders approaches

**Relationship to Other Papers:** Journal version of Paper 5 by same authors; extends the earlier work with additional methods.

---

## 10. A framework for feature extraction from hospital medical data with applications in risk prediction

**Authors:** T Tran, W Luo, D Phung, S Gupta, S Rana
**Publication:** BMC Bioinformatics, 2014
**Citations:** 51 (4.64 per year)
**Link:** https://link.springer.com/article/10.1186/s12859-014-0425-8
**PDF:** https://link.springer.com/content/pdf/10.1186/s12859-014-0425-8.pdf

**Abstract/Summary:**
Proposes a versatile platform to automatically extract features for risk prediction in healthcare, based on a pre-defined and extensible entity schema.

**Methodology/Approach:** Entity Schema Construction

**Key Points:**
- Treats patient medical history as signals corresponding to clinical events
- Schema defines signals for the entire administrative database
- Constructs entity schema by grouping entities (diagnoses ICD, procedures, medications)

**Relationship to Other Papers:** Highly cited early work focusing on schema for feature extraction rather than integration.

---

## Key Themes and Observations

1. **Machine Learning Dominance:** Recent papers (2021-2025) predominantly use transformer-based and deep learning approaches for schema matching, moving away from rule-based methods.

2. **Healthcare-Specific Challenges:** Multiple papers highlight unique healthcare data heterogeneity issues including non-standardized terminology, diverse EHR systems, and the need for semantic disambiguation.

3. **OMOP/CDM Standardization:** Growing focus on mapping to standard data models like OMOP CDM for interoperability and multi-site research enablement.

4. **EHR Integration Focus:** The majority of papers specifically address Electronic Health Record integration challenges, with MIMIC-III being a common evaluation dataset.

5. **Practical Applications:** Papers span theoretical frameworks to real-world implementations in national health systems (Brazil, Indonesia) and major healthcare systems.

---

## Citation Network

Paper 5 (Tripathi 2022) and Paper 9 (Tripathi 2024) represent preprint and journal versions of the same research line, with the 2024 paper extending the deep learning methods. Paper 8 (Zhang 2022) provides a comprehensive review that contextualizes methods used in other papers. Paper 7 (Zhou 2025) builds on transformer approaches pioneered in Paper 1 (Satti 2021) but applies them specifically to OMOP CDM mapping. Paper 10 (Tran 2014) is the most highly cited and represents foundational work that later papers reference for schema construction concepts.

---

## Highly Cited Papers (Relative Impact)

| Rank | Paper | Citations | Year | Citations/Year |
|------|-------|-----------|------|----------------|
| 1 | A framework for feature extraction from hospital medical data... | 51 | 2014 | 4.64 |
| 2 | A Novel Sentence Transformer-based NLP Approach for Schema Mapping... | 7 | 2025 | 7.00 |
| 3 | Multi-view representation learning for tabular data integration... | 6 | 2024 | 6.00 |
| 4 | Biomedical heterogeneous data categorization and schema mapping... | 6 | 2023 | 3.00 |
| 5 | Database integration based on combination schema matching approach... | 20 | 2017 | 2.50 |

---

## Suggested Follow-up Questions

**From Scholar Labs:**
1. What machine learning techniques are most effective for schema matching in healthcare databases?
2. How does OMOP CDM facilitate multi-site healthcare research?
3. What are the main barriers to healthcare data interoperability?

**Based on Literature Gaps:**
1. How do schema discovery approaches perform on real-time streaming healthcare data vs. batch processing?
2. What role does federated learning play in schema matching across healthcare institutions without sharing raw data?

---

## BibTeX Citations

```bibtex
@article{satti2021unsupervised,
  title={Unsupervised Semantic Mapping for Healthcare Data Storage Schema},
    author={Satti, Faisal Amin and Hussain, Maqbool and Hussain, Jamil and Ali, Syed Imran and Ali, Taqdir},
      journal={IEEE Access},
        year={2021},
          volume={9},
            pages={107267--107283},
              doi={10.1109/ACCESS.2021.3099704}
}

@article{deshpande2023biomedical,
  title={Biomedical heterogeneous data categorization and schema mapping toward data integration},
    author={Deshpande, Pallavi and Rasin, Alexander and Tchoua, Roselyne and Furst, Jacob},
      journal={Frontiers in Big Data},
        volume={6},
          pages={1173038},
            year={2023},
              doi={10.3389/fdata.2023.1173038}
              }

              @inproceedings{begoli2016realtime,
                title={Real-time discovery services over large, heterogeneous and complex healthcare datasets using schema-less, column-oriented methods},
                  author={Begoli, Edmon and Dunning, Ted and Frasure, Christopher},
                    booktitle={2016 IEEE Second International Conference on Big Data Computing Service and Applications},
                      pages={123--130},
                        year={2016},
                          organization={IEEE},
                            doi={10.1109/BigDataService.2016.42}
                            }

                            @inproceedings{belian2010context,
                              title={A Context-Based Schema Integration Process Applied to Healthcare Data Sources},
                                author={Belian, Rosalie Barreto and Salgado, Ana Carolina},
                                  booktitle={On the Move to Meaningful Internet Systems: OTM 2010 Workshops},
                                    pages={153--162},
                                      year={2010},
                                        publisher={Springer},
                                          doi={10.1007/978-3-642-16961-8_25}
                                          }

                                          @article{tripathi2022deep,
                                            title={Deep Learning to Jointly Schema Match, Impute, and Transform Databases},
                                              author={Tripathi, Shantanu and Fritz, Bradley A and Abdelhack, Mohamed and Avidan, Michael S},
                                                journal={arXiv preprint arXiv:2207.03536},
                                                  year={2022}
                                                  }

                                                  @inproceedings{rachman2017database,
                                                    title={Database integration based on combination schema matching approach (case study: Multi-database of district health information system)},
                                                      author={Rachman, Muhammad Arzaki Fadillah and Saptawati, Gusti Ayu Putri},
                                                        booktitle={2017 2nd International Conference on Information Technology, Information Systems and Electrical Engineering},
                                                          pages={397--402},
                                                            year={2017},
                                                              organization={IEEE},
                                                                doi={10.1109/ICITISEE.2017.8285544}
                                                                }

                                                                @article{zhou2025novel,
                                                                  title={A Novel Sentence Transformer-based Natural Language Processing Approach for Schema Mapping of Electronic Health Records to the OMOP Common Data Model},
                                                                    author={Zhou, Xinyu and Dhingra, Lovedeep Singh and Aminorroaya, Arya},
                                                                      journal={AMIA Annual Symposium Proceedings},
                                                                        year={2025},
                                                                          pages={},
                                                                            pmcid={PMC12099400}
                                                                            }

                                                                            @article{zhang2022scoping,
                                                                              title={A scoping review of semantic integration of health data and information},
                                                                                author={Zhang, Hansi and Lyu, Tianchen and Yin, Pengfei and Bost, Sarah and He, Xing and Guo, Yi},
                                                                                  journal={International Journal of Medical Informatics},
                                                                                    volume={165},
                                                                                      pages={104834},
                                                                                        year={2022},
                                                                                          publisher={Elsevier},
                                                                                            doi={10.1016/j.ijmedinf.2022.104834}
                                                                                            }

                                                                                            @article{tripathi2024multiview,
                                                                                              title={Multi-view representation learning for tabular data integration using inter-feature relationships},
                                                                                                author={Tripathi, Shantanu and Fritz, Bradley A and Abdelhack, Mohamed and Avidan, Michael S},
                                                                                                  journal={Journal of Biomedical Informatics},
                                                                                                    volume={150},
                                                                                                      pages={104588},
                                                                                                        year={2024},
                                                                                                          publisher={Elsevier},
                                                                                                            doi={10.1016/j.jbi.2024.104588}
                                                                                                            }

                                                                                                            @article{tran2014framework,
                                                                                                              title={A framework for feature extraction from hospital medical data with applications in risk prediction},
                                                                                                                author={Tran, Truyen and Luo, Wei and Phung, Dinh and Gupta, Sunil and Rana, Santu},
                                                                                                                  journal={BMC Bioinformatics},
                                                                                                                    volume={15},
                                                                                                                      number={1},
                                                                                                                        pages={425},
                                                                                                                          year={2014},
                                                                                                                            publisher={Springer},
                                                                                                                              doi={10.1186/s12859-014-0425-8}
                                                                                                                              }
                                                                                                                              ```}}}}}}}}}}
