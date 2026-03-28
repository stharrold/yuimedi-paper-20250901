# Research Question 1: What NL2SQL systems have been applied to healthcare databases?

**Source:** Google Scholar Labs
**Date:** December 18, 2025
**Results Found:** 10 relevant papers

---

## Summary of Findings

This search identified 10 relevant academic papers describing NL2SQL (Natural Language to SQL) systems applied to healthcare databases. The key systems and approaches include:

---

## 1. MedT5SQL: A transformers-based large language model for text-to-SQL conversion in the healthcare domain

**Authors:** A Marshan, AN Almutairi, A Ioannou, D Bell et al.
**Publication:** Frontiers in Big Data, 2024
**Citations:** 14

**Key Points:**
- Proposes the MedT5SQL model, a fine-tuned Text-to-Text Transfer Transformer (T5) model designed specifically for Text-to-SQL conversion within the healthcare domain
- Utilizes a Large Language Model (LLM) based on a transformers-based architecture to convert medical-related questions written in natural language into SQL
- Fine-tunes the proposed model using the MIMICSQL dataset, which is the first Text-to-SQL dataset developed for the healthcare domain

---

## 2. Text-to-SQL generation for question answering on electronic medical records

**Authors:** P Wang, T Shi, CK Reddy
**Publication:** Proceedings of The Web Conference 2020
**Citations:** 148

**Key Points:**
- Introduces a deep learning-based TRanslate-Edit Model for Question-to-SQL (TREQS) generation, specifically designed for the healthcare domain
- Creates a new large-scale Question-SQL pair dataset, MIMICSQL, for the Question-to-SQL generation task using the publicly available MIMIC III database
- Notes previous research efforts in the healthcare domain that have used semantic parsing and named entity extraction for Question-to-SQL generation tasks

---

## 3. Criteria2Query: A natural language interface to clinical databases for cohort definition

**Authors:** C Yuan, PB Ryan, C Ta, Y Guo, Z Li et al.
**Publication:** Journal of the American Medical Informatics Association, 2019
**Citations:** 201

**Key Points:**
- Introduces Criteria2Query as a novel natural language interface that translates eligibility criteria text into executable clinical data queries (SQL) conforming to the OMOP Common Data Model
- Facilitates human-computer collaboration for cohort definition and execution using clinical databases
- Notes that the medical domain has few studies on Natural Language Interfaces (NLIs) to patient-level databases

---

## 4. A BERT-based generation model to transform medical texts to SQL queries for electronic medical records

**Authors:** Y Pan, C Wang, B Hu, Y Xiang, X Wang et al.
**Publication:** JMIR Medical Informatics, 2021
**Citations:** 15

**Key Points:**
- Proposes a medical text-to-SQL model (MedTS) that automatically transforms medical texts into SQL queries for Electronic Medical Records (EMRs)
- Achieves state-of-the-art performance on the MIMICSQL dataset
- Discusses the TREQS model as an existing Seq2Seq-based model and mentions earlier rule-based methods

---

## 5. Restricted natural language based querying of clinical databases

**Authors:** L Safari, JD Patrick
**Publication:** Journal of Biomedical Informatics, 2014
**Citations:** 16

**Key Points:**
- Introduces CliniDAL, a restricted natural language query (RNLQ) system with a generic translation algorithm to convert queries into SQL for Clinical Information Systems (CISs)
- Describes implementation for clinical databases utilizing Entity-Relationship (ER) and Entity-Attribute-Value (EAV) design models
- Uses a similarity-based Top-k algorithm for mapping RNLQ terms to the underlying data models

---

## 6. Retrieval augmented text-to-SQL generation for epidemiological question answering using electronic health records

**Authors:** A Ziletti, L D'Ambrosi
**Publication:** Proceedings of the 6th Clinical Natural Language Processing Workshop, 2024
**Citations:** 18

**Key Points:**
- Introduces an end-to-end methodology that combines text-to-SQL generation with Retrieval Augmented Generation (RAG) to answer epidemiological questions using EHR and claims data
- Integrates a medical coding step into the text-to-SQL process, significantly improving performance
- Presents a dataset of manually annotated natural language question-SQL pairs designed for epidemiological research, adhering to OMOP-CDM

---

## 7. Graph-empowered Text-to-SQL generation on Electronic Medical Records

**Authors:** Q Chen, J Peng, B Song, Y Zhou, R Ji
**Publication:** Pattern Recognition, 2025
**Citations:** 3

**Key Points:**
- Proposes a Text-to-SQL method leveraging Large Language Models (LLMs) and graph-empowered techniques to enhance natural language querying capabilities in EMR systems
- Focuses on developing a Text-to-SQL generation method specifically for EMR databases to enable non-technical users to query complex structured medical data
- Achieves 0.942 execution accuracy on the MIMICSQL dataset

---

## 8. Combining human and machine intelligence for clinical trial eligibility querying

**Authors:** Y Fang, B Idnay, Y Sun, H Liu, Z Chen et al.
**Publication:** Journal of the American Medical Informatics Association, 2022
**Citations:** 34

**Key Points:**
- Introduces Criteria2Query (C2Q) 2.0, a natural language processing system designed to convert complex clinical trial eligibility criteria text into cohort queries against medical records data
- Enables the generation of portable cohort SQL queries based on the OMOP CDM version 5
- Builds on previous work on C2Q 1.0 for cohort definition

---

## 9. Criteria2Query 3.0: Leveraging generative large language models for clinical trial eligibility query generation

**Authors:** J Park, Y Fang, C Ta, G Zhang, B Idnay, F Chen et al.
**Publication:** Journal of Biomedical Informatics, 2024
**Citations:** 35

**Key Points:**
- Proposes Criteria2Query (C2Q) 3.0, a system that transforms clinical trial eligibility criteria text into executable clinical database queries using GPT-4
- Focuses on generating sharable cohort identification queries using GPT
- Executes the formulated SQL query to the OMOP-CDM formatted database

---

## 10. Knowledge discovery and knowledge reuse in clinical information systems

**Authors:** JD Patrick, L Safari, Y Cheng
**Publication:** Proceedings of the 10th IASTED International Conference, 2013
**Citations:** 8

**Key Points:**
- Introduces Clinical Data Analytics Language (CliniDAL), a special purpose query language that converts restricted natural language statements into SQL queries
- Details the CliniDAL engine's function of translating natural language input to SQL query, abstracting the clinical database schema from users
- Reports implementation and testing on operational clinical information systems, such as RPAH-ICU

---

## Key Themes and Observations

1. **MIMICSQL Dataset:** Multiple papers (MedT5SQL, TREQS, MedTS, Graph-empowered) use the MIMICSQL dataset, which appears to be the primary benchmark for healthcare NL2SQL evaluation

2. **OMOP Common Data Model:** Several systems (Criteria2Query series, RAG-based approach) target the OMOP CDM, indicating its importance as a standard for clinical data

3. **Evolution of Approaches:** The field has evolved from rule-based methods (CliniDAL, 2013-2014) to deep learning (TREQS, 2020) to transformer-based models (MedT5SQL, C2Q 3.0, 2024)

4. **Clinical Trial Applications:** A significant subset focuses on clinical trial eligibility querying (Criteria2Query 1.0, 2.0, 3.0)

5. **LLM Integration:** Recent work (2024-2025) increasingly leverages large language models like GPT-4 and T5 for improved performance
