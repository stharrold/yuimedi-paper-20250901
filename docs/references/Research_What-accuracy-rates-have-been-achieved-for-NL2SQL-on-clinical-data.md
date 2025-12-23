# Open Source Natural Language to SQL Benchmarks for Healthcare Analytics

*Research compiled from Google Scholar Labs*

---

## Overview

This document summarizes key open-source NL2SQL benchmarks and research for healthcare analytics applications. The search identified 10 relevant papers focusing on text-to-SQL systems for Electronic Health Records (EHR) databases.

PROMPT:
"what are the open source natural language to sql benchmarks for healthcare analytics"

---

## Key Benchmarks

### 1. EHRSQL
**Primary Reference:** Lee G, Hwang H, Bae S, Kwon Y et al. "Ehrsql: A practical text-to-sql benchmark for electronic health records" - Advances in Neural Information Processing Systems, 2022 - proceedings.neurips.cc

A large-scale text-to-SQL dataset linked to open-source EHR databases MIMIC-III and eICU. Dataset constructed from 222 hospital staff utterances. Addresses unique healthcare challenges including complex operations, time expressions, and distinguishing answerable from unanswerable questions.

**Citations:** 73

### 2. MIMICSQL
**Reference:** Wang P, Shi T, Reddy CK. "Text-to-SQL generation for question answering on electronic medical records" - Proceedings of The Web Conference 2020 - dl.acm.org

A 10,000 Question-SQL pair dataset created from MIMIC III database. Includes both template and natural language questions. The TREQS (TRanslate-Edit Model for Question-to-SQL) implementation is publicly available.

**Citations:** 148

### 3. SM3-Text-to-Query
**Reference:** Sivasubramaniam S, Osei-Akoto CE et al. "Sm3-text-to-query: Synthetic multi-model medical text-to-query benchmark" - Advances in Neural Information Processing Systems, 2024 - proceedings.neurips.cc

First multi-model medical Text-to-Query benchmark supporting SQL evaluation with PostgreSQL data representations. Enables evaluation across four popular query languages.

**Citations:** 15

### 4. DrugEHRQA
**Reference:** Bardhan J, Colas A, Roberts K, Wang DZ. "Drugehrqa: A question answering dataset on structured and unstructured electronic health records for medicine related queries" - arXiv, 2022

Multi-modal QA benchmark dataset for medical information extraction from EHRs. Contains natural language questions with corresponding SQL queries. Publicly available via Physionet.

**Citations:** 26

---

## Recent Performance Evaluations

### Performance Evaluation of Open-Source LLMs (2025)
**Authors:** Chadha IK, Gupta A, Sarkar S et al. - IEEE, 2025

Evaluates models including Llama3.1-8B, Llama3.1-70B, Mixtral-8x7b, Gemma2-9b, and Gemma2-2b on MIMICSQL dataset. **Finding:** Llama3.1-70B identified as best-performing model for exact match and logic form accuracy.

### Robust Clinical Querying with Local LLMs (2025)
**Authors:** Blašković L, Tanković N, Lorencin I et al. - Big Data and Cognitive Computing, 2025 - mdpi.com

Benchmarks seven open-source LLMs: DeepSeek V3/V3.1, Llama-3.3-70B, Qwen2.5-32B, Mixtral-8x22B, BioMistral-7B, GPT-OSS-20B.

**Results on MIMICSQL:**
- DeepSeek V3.1: 59.8% execution accuracy (best)
- DeepSeek V3: 58.8%
- Llama-3.3-70B: 54.5%

**Finding:** DeepSeek V3.1 provides best cost-accuracy trade-off.

### Transforming Medical Data Access (2025)
**Authors:** Tanković N, Šajina R, Lorencin I - Algorithms, 2025 - edihadria.eu

Evaluates LLaMA 3.3-70B and Qwen-2.5-72B on MIMIC-3 and TREQS datasets for real-world healthcare scenarios.

**Citations:** 5

---

## Shared Tasks & Competitions

### EHRSQL 2024 Shared Task
**Reference:** Lee G, Kweon S, Bae S, Choi E. "Overview of the ehrsql 2024 shared task on reliable text-to-sql modeling on electronic health records" - arXiv:2405.06673, 2024

Promotes research in question-answering systems for EHRs using text-to-SQL modeling. Dataset linked to MIMIC-III and eICU databases.

**Citations:** 15

### Related Submissions:

**1. Saama Technologies (2024)**
Jabir M, Kanakarajan K et al. - Proceedings of Clinical NLP 2024 - aclanthology.org
- SCAS framework code publicly available

**2. AIRI NLP Team (2024)**
Somov O, Dontsov A, Tutubalina E - Proceedings of Clinical NLP 2024 - aclanthology.org
- T5 and Logistic Regression approach
- Addresses hospital-specific needs and time expressions

---

## Key Databases Used

| Database | Description | Access |
|----------|-------------|--------|
| MIMIC-III | Medical Information Mart for Intensive Care | Open-source |
| eICU | Electronic ICU collaborative research database | Open-source |
| MIMIC-3 | Third version of MIMIC database | Open-source |

---

## Summary Statistics

- **Total papers reviewed:** 10
- **Most cited benchmark:** MIMICSQL (148 citations)
- **Most cited recent benchmark:** EHRSQL (73 citations)
- **Best performing open-source model (2025):** DeepSeek V3.1 (59.8% EX on MIMICSQL)

---

*Source: Google Scholar Labs search results*
*Query: "what are the open source natural language to sql benchmarks for healthcare analytics"*
*Retrieved: December 2025*
