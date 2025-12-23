# Research Question: What algorithms exist for automatic primary key/foreign key discovery from database metadata?

**Source:** Google Scholar Labs
**Date:** December 18, 2025
**Results Found:** 10 relevant papers
**Sorted By:** Relevance

---

## Summary of Findings

The literature reveals a rich body of work on automatic primary key and foreign key discovery algorithms, spanning from 2002 to 2023. The dominant approaches include machine learning-based classification methods (using algorithms like Naïve Bayes, SVM, and gradient boosted trees), inclusion dependency (IND) analysis as a precursor to foreign key detection, and score-based ranking functions. Key contributions include the SPIDER algorithm for IND discovery, the HoPF algorithm for holistic PK/FK detection, and various heuristic rules like the "Randomness" rule for multi-column foreign key discovery.

---

## 1. A machine learning approach to foreign key discovery

**Authors:** A Rostin, O Albrecht, J Bauckmann, F Naumann
**Publication:** WebDB, 2009
**Citations:** 99
**Link:** https://hpi.de (PDF available)

**Key Points:**
- Presents a machine learning approach that first computes all inclusion dependencies (INDs) and then uses a binary classification algorithm to determine if an IND is a foreign key constraint (FKC)
- Evaluates classification using several state-of-the-art algorithms including Naïve Bayes (NB), Support Vector Machines (SVM), J48, and Decision Tables (DT)
- Mentions the SPIDER algorithm for efficiently determining all inclusion dependencies in a relational database as a necessary preprocessing step

---

## 2. Holistic primary key and foreign key detection

**Authors:** L Jiang, F Naumann
**Publication:** Journal of Intelligent Information Systems, 2020 (Springer)
**Citations:** 56
**Link:** https://link.springer.com

**Key Points:**
- Proposes the HoPF (Holistic Primary Key and Foreign Key Detection) algorithm for automatically discovering both primary and foreign keys simultaneously
- Uses score functions to extract true primary and foreign keys from the vast sets of valid Unique Column Combinations (UCCs) and Inclusion Dependencies (INDs)
- Employs pruning rules to accelerate the detection process and improve performance

---

## 3. On multi-column foreign key discovery

**Authors:** M Zhang, M Hadjieleftheriou, BC Ooi
**Publication:** Proceedings of the ACM, 2010
**Citations:** 154
**Link:** https://dl.acm.org (PDF on researchgate.net)

**Key Points:**
- Proposes a robust algorithm for discovering single-column and multi-column foreign keys that are often not explicitly specified in the data
- Introduces a general rule called "Randomness" that serves as the basis for the foreign key discovery algorithm and encompasses various other rules previously used
- Develops efficient approximation algorithms for evaluating randomness using only two passes over the data, resulting in an I/O efficient method

---

## 4. Protecting data integrity of web applications with database constraints inferred from application code

**Authors:** H Huang, B Shen, L Zhong, Y Zhou
**Publication:** Proceedings of the 28th ACM, 2023
**Citations:** 24
**Link:** https://dl.acm.org (PDF on acm.org)

**Key Points:**
- Introduces CFinder, a tool that automatically infers missing database constraints, including foreign key constraints, from application source code
- Explains that existing works for discovering constraints traverse the search space of a powerset of column combinations and validate data satisfaction
- Notes that many existing constraint discovery methods relying on data validation produce a large majority of false positives

---

## 5. Approximate key and foreign key discovery in relational databases

**Authors:** C Vilarem
**Publication:** Master's thesis, Department of Computer Science, University of Toronto, 2002
**Citations:** 4
**Link:** https://cs.toronto.edu (PDF available)

**Key Points:**
- Reviews methods used in functional dependency/key discovery and approaches for inclusion dependency/foreign key discovery
- Proposes a concrete algorithm for extracting foreign keys from a database with no previous knowledge
- Presents a general architecture (Algorithm 1) for discovering approximate keys and foreign keys from a database

---

## 6. Automatization of foreign keys construction

**Authors:** V Zykin
**Publication:** 2016 Dynamics of Systems, Mechanisms and Machines (IEEE)
**Citations:** 1
**Link:** https://ieeexplore.ieee.org

**Key Points:**
- Presents an algorithm for automatic removal of excessive reference constraints founded on the primary key of relations
- Discusses a relationship generation algorithm that compares pairs of relations with polynomial complexity
- Describes an adaptation of the closure relations algorithm for removing redundant relationships without an inclusion dependencies graph

---

## 7. Efficient foreign key discovery based on nearest neighbor search

**Authors:** X Yuan, X Cai, M Yu, C Wang, Y Zhang
**Publication:** Conference on Web-Age Information Management, 2015 (Springer)
**Citations:** 5
**Link:** https://link.springer.com

**Key Points:**
- Formulates foreign key discovery as a nearest neighbor search problem
- Proposes a fast foreign key discovery algorithm that uses inclusion dependencies to reduce foreign key candidates
- Selects statistical features (average, variance, average length) to represent attributes and define distance between two attributes

---

## 8. Foreign Key Constraint Identification in Relational Databases

**Authors:** J Motl, P Kordík
**Publication:** ITAT, 2017
**Citations:** 5
**Link:** https://ceur-ws.org (PDF available)

**Key Points:**
- Presents a method for automatically and quickly identifying primary and foreign key constraints using machine learning techniques on database metadata
- Decomposes the relationship identification problem into two subproblems: primary key identification and foreign key constraint identification
- Tests various classification algorithms including decision tree, gradient boosted trees (best results), naive Bayes, neural network, and logistic regression

---

## 9. Discovering metadata in data files

**Authors:** L Jiang
**Publication:** PhD thesis, University of Potsdam, 2022
**Citations:** 3
**Link:** https://publishup.uni-potsdam.de (PDF available)

**Key Points:**
- Proposes the HoPF algorithm specifically to holistically detect both Primary Keys (PKs) and Foreign Keys (FKs) in relational databases
- The HoPF algorithm takes Unique Column Combinations (UCC) and Inclusion Dependencies (IND) as input, detected by previous data profiling algorithms
- Contrasts the holistic approach with previous works that often focused on detecting either primary keys or foreign keys individually

---

## 10. Profiling relational data: a survey

**Authors:** Z Abedjan, L Golab, F Naumann
**Publication:** The VLDB Journal, 2015 (Springer)
**Citations:** 474
**Link:** https://link.springer.com (PDF on mit.edu)

**Key Points:**
- Explains that foreign key discovery is frequently a real-world use case of multi-column profiling and is often addressed using inclusion dependencies
- Notes that inclusion dependency discovery is a precursor to foreign key detection, after which additional heuristics rank discovered dependencies by likelihood of being foreign keys
- Mentions that many dependency discovery algorithms are based on classical data mining solutions, such as the Apriori algorithm

---

## Key Themes and Observations

1. **Inclusion Dependencies as Foundation:** Nearly all approaches use Inclusion Dependency (IND) discovery as a prerequisite step before foreign key detection, with algorithms like SPIDER being commonly referenced.

2. **Machine Learning Classification:** Multiple papers employ machine learning classifiers (SVM, Naïve Bayes, Decision Trees, Gradient Boosted Trees) to distinguish true foreign keys from spurious inclusion dependencies.

3. **Holistic vs. Individual Detection:** Recent work (HoPF algorithm) advocates for simultaneously detecting both primary keys and foreign keys rather than treating them as separate problems.

4. **Score-Based Ranking:** Several approaches use scoring functions and heuristics to rank candidate foreign keys by their likelihood of being true constraints.

5. **Scalability Concerns:** Papers address computational efficiency through pruning rules, approximation algorithms, and formulating the problem as nearest neighbor search.

---

## Suggested Follow-up Questions

1. What precision and recall metrics have been reported for automatic foreign key discovery algorithms?
2. How do inclusion dependency discovery algorithms (like SPIDER) work, and what are their computational complexities?
3. What features or heuristics are most effective for distinguishing true foreign keys from spurious inclusion dependencies?
