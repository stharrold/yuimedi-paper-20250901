# Research: Graph-Enhanced NL2SQL on Healthcare Benchmarks

**Question:** What accuracy have graph-enhanced, knowledge-graph-augmented, or structured-knowledge-representation NL2SQL systems achieved on healthcare-specific benchmarks such as MIMICSQL, EHRSQL, or other clinical database question-answering tasks?

**Scope:** Paper1 (supports R4: NL2SQL accuracy gradient replacing "tipping point" claim)

**Date searched:** 2026-03-28

**Source:** Google Scholar Labs (evaluated results, surfaced 10 relevant papers)

---

## Key Findings

### Accuracy Gradient on MIMICSQL (the key benchmark)

| Approach | Execution Accuracy | Source |
|----------|-------------------|--------|
| Zero-shot cross-domain (GAP) | 16.4% | Lee et al. 2022 (EHRSQL, NeurIPS) |
| Seq2seq baseline (TREQS) | 55% | Blaskovic et al. 2025 |
| Open-weight LLM (DeepSeek V3.1) | 59.8% | Blaskovic et al. 2025 |
| General-purpose LLM (GPT-4o) | 66.1% | Blaskovic et al. 2025 |
| General-purpose LLM (GPT-5) | 64.6% | Blaskovic et al. 2025 |
| Domain-adapted (BioMistral-7B) | 11.8% | Blaskovic et al. 2025 |
| Specialized BERT-based (MedTS) | 89.9% | Pan et al. 2021 (JMIR Medical Informatics) |
| Linking-enhanced graph parser (LI-EMRSQL) | 98.0% (exact match) | Li et al. 2023 (IEEE Trans, cited 88) |
| **Graph-empowered LLM (Chen et al.)** | **94.2%** | **Chen et al. 2026 (Pattern Recognition, cited 5)** |

### Key Insights

1. **The 94.2% figure from the original paper is confirmed.** Chen et al. (2026) achieve 94.2% execution accuracy on MIMICSQL using graph structure injection into LLMs, published in Pattern Recognition (Elsevier). This is the specific citation needed for R4.
2. **The accuracy gradient is dramatic:** from ~16% (zero-shot) to ~65% (general-purpose LLMs) to ~90-94% (architecturally specialized). This supports the R4 recommendation to replace "tipping point" with a nuanced accuracy gradient.
3. **Domain adaptation alone is insufficient:** BioMistral-7B (biomedical domain-adapted) achieves only 11.8% on MIMICSQL, much worse than general-purpose models. The architecture matters more than domain pre-training for NL2SQL.
4. **Generalization remains a challenge:** Tarbell et al. (2024, AMIA) show that accuracy drops from ~92% to 28% on a more challenging MIMICSQL split, demonstrating that high benchmark scores may not transfer to real-world clinical queries.
5. **EHRSQL (NeurIPS 2022, cited 101)** is the established benchmark for practical clinical text-to-SQL, linked to MIMIC-III and eICU databases.

## Relevance to Paper

- **R4 (NL2SQL accuracy gradient):** Chen et al. 2026 confirms the 94.2% figure. The gradient from 65% (GPT-4o/5) to 94.2% (graph-empowered) directly supports the claim that architecturally specialized approaches substantially outperform general-purpose models on healthcare NL2SQL.
- **R4:** Blaskovic et al. 2025 provides the most comprehensive head-to-head comparison of 9 LLMs on MIMICSQL, making it the best single citation for the accuracy range.
- **Section 7 (Safety):** Tarbell et al. 2024's finding that accuracy drops dramatically on harder splits reinforces the need for human validation (HiL-SG) even when benchmark scores are high.

---

## Sources

### 1. Chen Q, Peng J, Song B, Zhou Y, Ji R. Graph-empowered Text-to-SQL generation on Electronic Medical Records. Pattern Recognition. 2026.

- **URL:** https://www.sciencedirect.com/science/article/pii/S0031320325004601
- **Cited by:** 5
- **Key findings:**
  - **Execution accuracy: 0.942 (94.2%) on MIMICSQL** -- new SOTA
  - LLMs combined with graph structure injection
  - Graph representations capture intricate relationships between medical entities
  - Graph structure embedding injected into LLM enhances NL-to-SQL conversion on EMR databases

### 2. Blaskovic L, Tankovic N, Lorencin I, et al. Robust Clinical Querying with Local LLMs: Lexical Challenges in NL2SQL and Retrieval-Augmented QA on EHRs. Big Data and Cognitive Computing. 2025;9(10):256.

- **URL:** https://www.mdpi.com/2504-2289/9/10/256
- **Cited by:** 1
- **Key findings:**
  - Benchmarks **9 LLMs** on MIMICSQL: sparse MoE, dense general-purpose, domain-adapted, proprietary
  - **GPT-4o: 66.1% EX; GPT-5: 64.6% EX; DeepSeek V3.1: 59.8% EX**
  - **BioMistral-7B (domain-adapted): only 11.8% EX** -- domain pre-training alone insufficient
  - Prior seq2seq model (TREQS): 55% on paraphrased questions

### 3. Ni P, Okhrati R, Guan S, Chang V. Knowledge graph and deep learning-based text-to-GraphQL model for intelligent medical consultation chatbot. Information Systems Frontiers. 2024;26:137-156.

- **URL:** https://link.springer.com/article/10.1007/s10796-022-10295-0
- **PDF:** https://link.springer.com/content/pdf/10.1007/s10796-022-10295-0.pdf
- **Cited by:** 75
- **Key findings:**
  - Text-to-GraphQL (Text2GraphQL) pipeline for medical knowledge graph querying
  - Knowledge graph provides continuously updated external knowledge
  - Tested on 39.net medical Q&A knowledge graph

### 4. Li Q, You T, Chen J, Zhang Y, et al. LI-EMRSQL: linking information enhanced Text2SQL parsing on complex electronic medical records. IEEE Transactions on Knowledge and Data Engineering. 2023.

- **URL:** https://ieeexplore.ieee.org/abstract/document/10351031/
- **Cited by:** 88
- **Key findings:**
  - **98.0% exact match accuracy** on MIMICSQL (structural parsing, not execution accuracy)
  - LI-EMRSQL: Poincare distance metric + induced relations for schema linkage
  - 5.1% improvement over RAT-SQL baseline on EMR datasets
  - Outperforms RAT-SQL and RAT-SQL + GAP

### 5. Lee G, Hwang H, Bae S, Kwon Y, et al. EHRSQL: A practical text-to-SQL benchmark for electronic health records. Advances in Neural Information Processing Systems (NeurIPS). 2022.

- **URL:** https://proceedings.neurips.cc/paper_files/paper/2022/hash/643e347250cf9289e5a2a6c1ed5ee42e-Abstract-Datasets_and_Benchmarks.html
- **PDF:** https://proceedings.neurips.cc/paper_files/paper/2022/file/643e347250cf9289e5a2a6c1ed5ee42e-Paper-Datasets_and_Benchmarks.pdf
- **Cited by:** 101
- **Key findings:**
  - EHRSQL benchmark linked to MIMIC-III and eICU open-source databases
  - Questions collected from actual hospital staff
  - Handles complex operations and time expressions
  - Zero-shot GAP model: 16.4% on MIMICSQL, 5.8% on EHRSQL validation

### 6. Liang Y, Tan K, Xie T, Tao W, Wang S, Lan Y, et al. Aligning large language models to a domain-specific graph database for NL2GQL. Proceedings of the 33rd ACM International Conference on Information and Knowledge Management (CIKM). 2024.

- **URL:** https://dl.acm.org/doi/abs/10.1145/3627673.3679713
- **PDF:** https://dl.acm.org/doi/pdf/10.1145/3627673.3679713
- **Cited by:** 13
- **Key findings:**
  - MediGQL: medical-domain graph database benchmark
  - Alignment method: +6.36 EM, +7.09 EX over baselines
  - Domain-specific medical LLMs (HuatuoGPT2-7B, BianQue-2) performed poorly vs general-domain LLMs on NL2GQL

### 7. Pan Y, Wang C, Hu B, Xiang Y, Wang X, et al. A BERT-based generation model to transform medical texts to SQL queries for electronic medical records: model development and validation. JMIR Medical Informatics. 2021;9(12):e32698.

- **URL:** https://medinform.jmir.org/2021/12/e32698/
- **Cited by:** 16
- **Key findings:**
  - **MedTS model: 89.9% execution accuracy on MIMICSQL**
  - BERT-based encoder + grammar-based LSTM decoder
  - Tree-structured intermediate representation aligned to SQL structure
  - Outperformed best competitor by 27% EX and 29% LF accuracy

### 8. Huang Y, Guo J, Mao W, Gao C, Han P, Liu C, et al. Exploring the landscape of text-to-SQL with large language models: Progresses, challenges and opportunities. arXiv preprint arXiv:2505.23838. 2025.

- **URL:** https://arxiv.org/abs/2505.23838
- **PDF:** https://arxiv.org/pdf/2505.23838
- **Cited by:** 6
- **Key findings:**
  - Comprehensive survey of LLM-based text-to-SQL
  - Reviews EHRSQL and other healthcare benchmarks
  - Categorizes methodologies: pre-processing, in-context learning, fine-tuning, post-processing

### 9. Tarbell R, Choo KKR, Dietrich G, et al. Towards understanding the generalization of medical text-to-SQL models and datasets. AMIA Annual Symposium Proceedings. 2024.

- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC10785918/
- **PDF:** https://pmc.ncbi.nlm.nih.gov/articles/PMC10785918/pdf/1098.pdf
- **Cited by:** 11
- **Key findings:**
  - SOTA models on MIMICSQL achieve ~90%+ accuracy on standard splits
  - **On more challenging split: accuracy drops from 92% to 28%**
  - MedTS: 89.9% EX on paraphrased test set
  - Demonstrates generalization gap: high benchmark != real-world readiness

### 10. Alexander N. Towards answering unanswerable questions: data augmentation for enhanced medical domain question answering. University of Cape Town. 2025.

- **URL:** https://open.uct.ac.za/items/2c72ad40-a69e-4f19-ab39-5058100abd8d
- **PDF:** https://open.uct.ac.za/bitstreams/c9904da0-7e0a-48cf-a2f3-328d3eca6d53/download
- **Cited by:** new
- **Key findings:**
  - T5-Large fine-tuned with RAG incorporating SNOMED CT and RxNorm medical vocabularies
  - Addresses out-of-schema questions in medical text-to-SQL
  - Uses execution accuracy (EX) as evaluation metric
