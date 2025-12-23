# Healthcare NL2SQL Datasets for Validation

## Overview
This document summarizes datasets available for natural language to SQL validation in the healthcare domain, based on Google Scholar research.

---

## Key Datasets

### 1. MIMICSQL
- **Paper:** Text-to-SQL generation for question answering on electronic medical records
- **Authors:** P Wang, T Shi, CK Reddy
- **Source:** Proceedings of The Web Conference 2020
- **Citations:** 148
- **Description:** Large-scale Question-SQL pair dataset created for Question-to-SQL generation in healthcare, based on the MIMIC III database
- **Size:** 10,000 Question-SQL pairs
- **Database:** MIMIC III (Medical Information Mart for Intensive Care III)
- **Validation:** Crowd-sourcing with medical domain knowledge to filter and paraphrase template questions

### 2. EHRSQL
- **Paper:** Ehrsql: A practical text-to-sql benchmark for electronic health records
- **Authors:** G Lee, H Hwang, S Bae, Y Kwon
- **Source:** Advances in Neural Information Processing Systems, 2022
- **Citations:** 73
- **Description:** Text-to-SQL dataset specifically created for electronic health records (EHRs), linking natural language questions to validated SQL queries
- **Databases:** MIMIC-III and eICU (open-source EHR databases)
- **Features:** Various time expressions, held-out unanswerable questions, wide range of hospital queries

### 3. MedT5SQL / MIMICSQL Dataset
- **Paper:** MedT5SQL: a transformers-based large language model for text-to-SQL conversion in the healthcare domain
- **Authors:** A Marshan, AN Almutairi, A Ioannou, D Bell
- **Source:** Frontiers in Big Data, 2024
- **Citations:** 14
- **Description:** First Text-to-SQL dataset specifically created for the healthcare domain
- **Application:** Fine-tuning the MedT5SQL model for converting medical-related questions to SQL

### 4. BiomedSQL
- **Paper:** BiomedSQL: Text-to-SQL for Scientific Reasoning on Biomedical Knowledge Bases
- **Authors:** MJ Koretsky, M Willey, A Asija, O Bianchi et al.
- **Source:** arXiv preprint, 2025
- **Description:** First benchmark for evaluating scientific reasoning in text-to-SQL generation over biomedical knowledge bases
- **Size:** 68,000 question/SQL query/answer triples
- **Database:** BigQuery knowledge base integrating gene-disease associations, causal inference from omics data, and drug approval records

### 5. DrugEHRQA
- **Paper:** Drugehqa: A question answering dataset on structured and unstructured electronic health records for medicine related queries
- **Authors:** J Bardhan, A Colas, K Roberts, DZ Wang
- **Source:** arXiv preprint, 2022
- **Citations:** 26
- **Description:** Dataset containing natural language questions, corresponding SQL queries, and answers derived from structured tables and unstructured notes within EHRs
- **Database:** MIMIC-III
- **Features:** Template-based QA generation for drug-related questions, validated SQL queries

### 6. OMOP-CDM Epidemiological Dataset
- **Paper:** Retrieval augmented text-to-SQL generation for epidemiological question answering using electronic health records
- **Authors:** A Ziletti, L DAmbrosi
- **Source:** Proceedings of the 6th Clinical Natural Language Processing Workshop, 2024
- **Citations:** 18
- **Description:** Manually annotated natural language question-SQL pairs for epidemiological research
- **Data Model:** OMOP Common Data Model (OMOP-CDM)
- **Features:** Free-form language questions, two paraphrased versions per question-SQL pair, complex nested SQL queries

---

## Database Summary

| Database | Description | Access |
|----------|-------------|--------|
| MIMIC-III | Medical Information Mart for Intensive Care | Open-source |
| eICU | Electronic ICU collaborative research database | Open-source |
| MIMIC-IV | Fourth version of MIMIC database | Open-source |

---

## Citation Statistics

- **Most cited dataset:** MIMICSQL (148 citations)
- **Most cited benchmark:** EHRSQL (73 citations)
- **Newest datasets:** BiomedSQL (2025), Graph-empowered Text-to-SQL (2025)

---

## Related Shared Tasks

### EHRSQL 2024 Shared Task
- **Paper:** Overview of the ehrsql 2024 shared task on reliable text-to-sql modeling on electronic health records
- **Authors:** G Lee, S Kweon, S Bae, E Choi
- **Citations:** 15
- **Databases:** MIMIC-III and MIMIC-IV
- **Features:** Unanswerable questions for testing model reliability, time expressions, varied complexity queries

---

*Source: Google Scholar Labs search results*
*Query: "for natural language to sql validation, what datasets are there for healthcare natural language questions with validated sql query answers"*
*Retrieved: December 2025*
