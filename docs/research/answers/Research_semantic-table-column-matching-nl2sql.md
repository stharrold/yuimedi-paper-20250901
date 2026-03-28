# Research: Semantic Table/Column Matching for NL2SQL

**Question:** What is the state of the art in semantic table/column matching for NL2SQL?

**Scope:** Paper2

**GitHub Issue:** #368

**Search Date:** 2025-12-20

**Source:** Google Scholar Labs

**Results Found:** 10

---

## Summary

Schema linking (semantic table/column matching) is identified as a **critical step** in NL2SQL systems. The field has evolved from string-matching approaches to neural network-based methods, and most recently to LLM-based in-context learning approaches. Key challenges remain around handling non-descriptive column names, cross-domain generalization, and the semantic gap between natural language and database schemas.

### Key Findings

1. **Schema linking is crucial** for both complex SQL generation and cross-domain generalization
2. **Three main approaches** exist: string matching-based, neural network-based, and in-context learning-based (LLMs)
3. **Graph Neural Networks (GNNs)** are increasingly used for joint encoding of NL queries and database schemas
4. **LLMs still struggle** with precise table/column identification compared to fine-tuned models
5. **Semantic gap** between user language and messy database schemas (e.g., "col_1") remains a key challenge

---

## Results

### 1. Natural language to sql: State of the art and open problems

**Authors:** Y Luo, G Li, J Fan, C Chai, N Tang

**Source:** Proceedings of the VLDB, 2025 - dl.acm.org

**Citations:** 7

**PDF:** [tsinghua.edu.cn]

**Key Points:**
- Schema linking explicitly maps elements of the natural language query to database schema components
- State of the art improved with emergence of LLMs and tunable pre-trained language models (PLMs)
- Incorporating database content further improves schema understanding and query accuracy

---

### 2. A survey on text-to-sql parsing: Concepts, methods, and future directions

**Authors:** B Qin, B Hui, L Wang, M Yang, J Li, B Li

**Source:** arXiv preprint, 2022 - arxiv.org

**Citations:** 139

**PDF:** [arxiv.org]

**Key Points:**
- Schema linking identifies references to columns, tables, and condition values in NL questions
- Crucial for complex SQL generation and cross-domain generalization
- Pre-training objectives (e.g., Grappa) designed to model schema linking information
- Grappa's SQL Semantic Prediction (SSP) objective predicts column appearances and SQL operations

---

### 3. Graph neural networks for databases: A survey

**Authors:** Z Li, Y Li, Y Luo, G Li, C Zhang

**Source:** arXiv preprint arXiv:2502.12908, 2025 - arxiv.org

**Citations:** 6

**PDF:** [arxiv.org]

**Key Points:**
- GNNs utilized for text-to-SQL conversion tasks
- GLOBAL-GNN uses GNNs for: relevance scoring, representation learning, re-ranking candidate queries
- SADGA uses unified Gated Graph Neural Network (GGNN) encoder to model both NL question and database schema

---

### 4. Recent advances in text-to-SQL: A survey of what we have and what we expect

**Authors:** N Deng, Y Chen, Y Zhang

**Source:** arXiv preprint arXiv:2208.10099, 2022 - arxiv.org

**Citations:** 77

**PDF:** [arxiv.org]

**Key Points:**
- Major challenge is translating semantics between natural utterances and SQL queries
- Graph structures provide unified encoding for natural utterances and database schemas
- S2SQL uses abstract schemas with graph projection neural network for delexicalized representations

---

### 5. A survey of text-to-sql in the era of LLMs: Where are we, and where are we going?

**Authors:** X Liu, S Shen, B Li, P Ma, R Jiang

**Source:** IEEE Transactions on Knowledge and Data Engineering, 2025 - ieeexplore.ieee.org

**Citations:** 23

**Key Points:**
- **Three categories** of schema linking strategies:
  1. String matching-based
  2. Neural network-based
  3. In-context learning-based
- LLM-powered schema linking uses In-Context Learning (ICL) for dynamic, flexible linking
- Examples: C3-SQL, MAC-SQL, CHESS
- Schema linking essential for capturing NL semantics and mapping user intent to SQL

---

### 6. From natural language to SQL: Review of LLM-based text-to-SQL systems

**Authors:** A Mohammadjafari, AS Maida

**Source:** arXiv preprint, 2024 - arxiv.org

**Citations:** 31

**PDF:** [arxiv.org]

**Key Points:**
- Schema linking maps parsed NL components to tables, columns, and relationships
- Example: "gas stations" links to GasStations table, "power" matches PowerAvailable column
- Graph Retrieval Augmented Generation (RAG) studied for better contextual accuracy
- Critical for handling complex, cross-domain databases

---

### 7. Converting Natural Language to Query Languages Using Large Language Models: A Systematic Literature Review

**Authors:** RR Lima, KC Vasconcelos

**Source:** Brazilian Symposium on Databases, 2025 - sol.sbc.org.br

**PDF:** [sbc.org.br]

**Key Points:**
- Explores impact of LLMs on NL-to-QL task using fine-tuning or prompt engineering
- **LLMs have limitations** in precisely identifying tables, columns, and constraints
- Many models struggle with schema linking leading to incorrect associations

---

### 8. A review of NLIDB with deep learning: findings, challenges and open issues

**Authors:** S Abbas, MU Khan, SUJ Lee, A Abbas

**Source:** IEEE Access, 2022 - ieeexplore.ieee.org

**Citations:** 35

**PDF:** [ieee.org]

**Key Points:**
- Semantic problem involves terminology mapping between NL questions and database entities
- Semantic gap arises from misinterpreted column names and incorrect cell/column values
- Schema linking with GNNs and self-attention mechanisms consider additional context

---

### 9. State of the art and open challenges in natural language interfaces to data

**Authors:** F Ozcan, A Quamar, J Sen, C Lei

**Source:** Proceedings of the 2020 ACM SIGMOD, 2020 - dl.acm.org

**Citations:** 68

**PDF:** [academia.edu]

**Key Points:**
- Entity-based interpretation identifies entities in NL query and understands intended relationships
- Neural approaches: SQLNet, TypeSQL use column attention, sketch-based methods, type utilization
- BERT-based utterance-table encoder jointly encodes user utterance and column headers with co-attention
- Table-aware decoder for SQL generation addresses semantic table/column matching

---

### 10. Conversational Text-to-SQL: A Comprehensive Survey of Paradigms, Challenges, and Future Directions

**Authors:** Y Yang, Z Peng, F Zhou, X Yao, Y Zhang

**Source:** Workshop on Agents and AI, 2025 - Springer

**Key Points:**
- Schema linking is critical process of mapping entities to corresponding tables and columns
- **Key challenge:** "semantic gap" between user language and complex, messy schemas
- Non-descriptive table/column names (e.g., "col_1") exacerbate the problem
- Future direction: better schema linking in noisy environments, clarification dialogues for ambiguity

---

## Implications for Paper 2

1. **Schema linking is a mandatory component** for any NL2SQL reference implementation
2. **Consider hybrid approach:** Combine string matching for simple cases with neural methods for complex schemas
3. **LLM limitations acknowledged:** Fine-tuned models may still outperform general LLMs for precise schema matching
4. **Graph-based encoding** (GNNs) shows promise for unified NL-schema representation
5. **Healthcare context challenge:** Medical schemas often have non-descriptive column names (from EHR vendors)
6. **Database content integration** improves accuracy - relevant for Synthea sample data approach

---

## Status

**Answered** - Comprehensive coverage of state-of-the-art approaches found with 10 highly relevant papers spanning 2020-2025.
