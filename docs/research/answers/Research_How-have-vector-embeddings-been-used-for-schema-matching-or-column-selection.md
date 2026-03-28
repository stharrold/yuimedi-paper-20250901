# Research Question: How have vector embeddings been used for schema matching or column selection?

**Source:** Google Scholar Labs
**Date:** December 19, 2025
**Results Found:** 10 relevant papers
**Sorted By:** Relevance
**Search Duration:** ~1 minute

---

## Summary of Findings

The search found 10 relevant papers spanning 2019-2024 that demonstrate diverse applications of vector embeddings for schema matching and column selection tasks. The dominant approaches include using Word2Vec, FastText, BERT, and other pre-trained language models to generate semantic representations of schema elements. Key themes include neural embedding-based similarity comparison, contrastive learning for column representations, and transfer learning from large language models.

---

## 1. It's ai match: A two-step approach for schema matching using embeddings

**Authors:** B Hättasch, M Truong-Ngoc, A Schmidt et al.
**Publication:** arXiv preprint, 2022
**Citations:** 32 (10.67 per year)
**Link:** https://arxiv.org/abs/2203.04366
**PDF:** https://arxiv.org/pdf/2203.04366

**Abstract/Summary:**
Proposes a novel end-to-end approach for schema matching based on neural embeddings, which utilizes a two-step process involving table matching followed by attribute matching.

**Methodology/Approach:** Machine Learning, Neural Embeddings

**Key Points:**
- Uses embeddings at different levels, representing either the entire table or single attributes, to determine correspondences in a robust and reliable manner
- Enables the discovery of non-trivial semantic correspondences through embedding-based comparison
- Word embeddings are well-suited for schema matching because they can compare semantic similarity between strings like attribute names

**Relationship to Other Papers:** Cited by Paper 9 (Zhang 2023) as related embedding approach

---

## 2. REMA: Graph Embeddings-based Relational Schema Matching

**Authors:** C Koutras, M Fragkoulis et al.
**Publication:** EDBT/ICDT, 2020
**Citations:** 39 (7.8 per year)
**Link:** http://star.informatik.rwth-aachen.de/Publications/CEUR-WS/Vol-2578/SEAData5.pdf
**PDF:** http://star.informatik.rwth-aachen.de/Publications/CEUR-WS/Vol-2578/SEAData5.pdf

**Abstract/Summary:**
Introduces the Relational Embeddings MAtcher (REMA), a novel schema matching approach that uses relational embeddings to capture the semantic similarity of attributes.

**Methodology/Approach:** Graph Embeddings, Neural Networks, Word2Vec

**Key Points:**
- Utilizes relational embeddings inspired by word embeddings to embed database rows, columns, and schema information into multidimensional vectors
- Reveals semantic similarity for schema matching through vector representation
- Trains neural networks using skipgram model (Word2Vec) on tokenized sequences of relational data elements

**Relationship to Other Papers:** Cited by Paper 9 (Zhang 2023) as related work leveraging graph embeddings

---

## 3. Semantic schema matching for string attribute with word vectors

**Authors:** K Nozaki, T Hochin, H Nomiya
**Publication:** 2019 6th International Conference, IEEE, 2019
**Citations:** 16 (2.67 per year)
**Link:** https://ieeexplore.ieee.org/abstract/document/8916688/
**PDF:** Not available

**Abstract/Summary:**
Proposes an instance-based schema matching approach that uses Word2Vec to compare attributes of character strings, aiming to consider attributes' semantics.

**Methodology/Approach:** Word2Vec, Instance-based Matching

**Key Points:**
- Calculates vectors for attribute matching by vectorizing instances using Word2Vec
- Determines correspondences by calculating cosine similarity between generated attribute vectors
- Vector representations of words reflect semantic relations, enabling semantic comparison of instances

**Relationship to Other Papers:** Extended version published as Paper 6 (Nozaki 2019 Springer)

---

## 4. Semantics-aware dataset discovery from data lakes with contextualized column-based representation learning

**Authors:** G Fan, J Wang, Y Li, D Zhang, R Miller
**Publication:** arXiv preprint arXiv:2210.01922, 2022
**Citations:** 126 (42 per year)
**Link:** https://arxiv.org/abs/2210.01922
**PDF:** https://arxiv.org/pdf/2210.01922

**Abstract/Summary:**
Introduces Starmie, an end-to-end framework for dataset discovery from data lakes that uses a contrastive learning method to train column encoders from pre-trained language models in an unsupervised manner.

**Methodology/Approach:** Contrastive Learning, Pre-trained Language Models

**Key Points:**
- Applies pre-trained language models (LMs) to obtain semantics-aware representations for columns in data lake tables
- Utilizes cosine similarity between column embedding vectors as the column unionability score
- Uses unsupervised contrastive learning to train column encoders

**Relationship to Other Papers:** Most highly cited paper in results; represents state-of-the-art in column embeddings

---

## 5. Employing word-embedding for schema matching in standard lifecycle management

**Authors:** H Oh, A Jones, T Finin
**Publication:** Journal of Industrial Information Integration, 2024, Elsevier
**Citations:** 7 (7 per year)
**Link:** https://www.sciencedirect.com/science/article/pii/S2452414X23001206
**PDF:** https://www.sciencedirect.com/science/article/am/pii/S2452414X23001206

**Abstract/Summary:**
Explores how word-embedding may be engineered to assist users in a user-interactive, web-based application where schema matching is required for data migration.

**Methodology/Approach:** Word Embeddings, Interactive Tool (SCORE)

**Key Points:**
- Discusses the SCORE tool where word-embedding technique is employed for schema matching
- Assists standard users in updating usage specifications following new standard releases
- Word-embeddings help identify correspondences because they represent words with similar meanings similarly

**Relationship to Other Papers:** Practical application of embedding techniques in industrial context

---

## 6. Semantic schema matching for string attribute with word vectors and its evaluation

**Authors:** K Nozaki, T Hochin, H Nomiya
**Publication:** International Journal of Networked and Distributed Computing, 2019, Springer
**Citations:** 9 (1.5 per year)
**Link:** https://link.springer.com/article/10.2991/ijndc.k.190710.001
**PDF:** https://link.springer.com/content/pdf/10.2991/ijndc.k.190710.001.pdf

**Abstract/Summary:**
Proposes an instance-based schema matching approach that uses Word2Vec to compare the semantic similarity of attribute instances treated as column values in a database.

**Methodology/Approach:** Word2Vec, Instance-based Matching

**Key Points:**
- Calculates attribute vectors using vectors of column values, leveraging the idea that values express semantics of attributes
- Determines attribute correspondence by calculating cosine similarity between generated vectors
- Sets threshold for deciding a match based on similarity score

**Relationship to Other Papers:** Extended version of Paper 3 (same authors)

---

## 7. In situ neural relational schema matcher

**Authors:** X Du, G Yuan, S Wu, G Chen et al.
**Publication:** 2024 IEEE 40th International Conference, 2024
**Citations:** 7 (7 per year)
**Link:** https://ieeexplore.ieee.org/abstract/document/10597805/
**PDF:** Not available

**Abstract/Summary:**
Proposes ISResMat, a framework designed to match schemas of relational tables by fine-tuning a pre-trained language model, which generates column embeddings.

**Methodology/Approach:** Pre-trained Language Models, Fine-tuning, Custom Loss Functions

**Key Points:**
- Designs specific loss functions (Meta-Matching Loss and Agent-Delegating Loss) to learn representations/embeddings of table columns
- Calculates matching scores between different table columns using learned representations
- Fine-tunes pre-trained language models for schema matching task

**Relationship to Other Papers:** Represents recent advances in PLM-based schema matching

---

## 8. Significance of Syntactic Type Identification in Embedding Vector based Schema Matching

**Authors:** FA Satti, M Hussain, S Lee et al.
**Publication:** 2022 16th International Conference, IEEE, 2022
**Citations:** 1 (0.33 per year)
**Link:** https://ieeexplore.ieee.org/abstract/document/9721780/
**PDF:** Not available

**Abstract/Summary:**
Utilizes transformer-based transfer learning techniques to convert semantically enriched attribute suffixes into embedding vectors, which are then compared using cosine similarity to identify similar attributes.

**Methodology/Approach:** BERT, Transfer Learning, NLI Models

**Key Points:**
- Compares approach based on BERT Natural Language Inference (NLI) models for semantic similarity
- Includes naive syntactic similarity in determining schema similarities alongside semantic approach
- State-of-the-art NLP solutions convert words and sentences into embedding vectors for automated schema matching

**Relationship to Other Papers:** Explores BERT-based approaches complementing Word2Vec methods in other papers

---

## 9. Schema matching using pre-trained language models

**Authors:** Y Zhang, A Floratou, J Cahoon et al.
**Publication:** 2023 IEEE 39th International Conference, 2023
**Citations:** 50 (25 per year)
**Link:** https://ieeexplore.ieee.org/abstract/document/10184612/
**PDF:** https://www.microsoft.com/en-us/research/wp-content/uploads/2022/12/273.pdf

**Abstract/Summary:**
Explains that existing approaches to schema matching use embedding similarities as initial scores, specifically mentioning the use of pre-trained word embeddings like FastText.

**Methodology/Approach:** Pre-trained Language Models, FastText

**Key Points:**
- Introduces a word embedding featurizer that calculates cosine similarity between embedding representations of attribute names
- Uses pre-trained FastText embeddings for initial similarity scoring
- References related work including EmbDI for local embeddings and REMA for graph embeddings

**Relationship to Other Papers:** Cites Paper 2 (REMA) as related work; Microsoft Research contribution

---

## 10. Semantic-similarity-based schema matching for management of building energy data

**Authors:** Z Pan, G Pan, A Monti
**Publication:** Energies, 2022, MDPI
**Citations:** 14 (4.67 per year)
**Link:** https://www.mdpi.com/1996-1073/15/23/8894
**PDF:** https://www.mdpi.com/1996-1073/15/23/8894

**Abstract/Summary:**
Applies semantic-similarity methods, combining natural language processing knowledge, to the automatic schema-mapping process, reducing manual effort in heterogeneous data integration.

**Methodology/Approach:** Word2Vec, Sentence-BERT, NLP

**Key Points:**
- Automates schema matching using linguistic-based techniques including Word2Vec and Sentence-BERT
- Employs word embedding which maps words to real vectors as part of corpus-based approach
- Vectors provide representation of meaning and preserve linguistic relationships

**Relationship to Other Papers:** Domain-specific application (building energy) of general embedding techniques

---

## Key Themes and Observations

1. **Word2Vec Dominance:** Word2Vec and similar skipgram models remain the most commonly used embedding technique for schema matching, appearing in Papers 1, 2, 3, 6, and 10.

2. **Pre-trained Language Models:** Recent papers (2022-2024) show increasing use of pre-trained language models like BERT and FastText, representing evolution from simple word embeddings (Papers 4, 7, 8, 9).

3. **Cosine Similarity as Standard:** Nearly all papers use cosine similarity between embedding vectors as the primary method for determining schema correspondences.

4. **Instance vs. Schema-Level Matching:** Papers split between using column value instances (Papers 3, 6) vs. schema metadata (attribute names, table names) for generating embeddings.

5. **Contrastive Learning Emergence:** The most-cited paper (Paper 4, Starmie) introduces contrastive learning methods, suggesting this may be a key direction for future research.

---

## Citation Network

- Paper 3 (Nozaki 2019 IEEE) and Paper 6 (Nozaki 2019 Springer) share the same authors and methodology, with Paper 6 being an extended evaluation
- Paper 9 (Zhang 2023) explicitly references Paper 2 (REMA) as related work using graph embeddings
- Paper 4 (Starmie) represents a highly influential work with 126 citations, significantly more than others
- Papers 7, 8, and 9 represent the most recent (2022-2024) advances using PLM-based approaches

---

## Highly Cited Papers (Relative Impact)

| Rank | Paper | Citations | Year | Citations/Year |
|------|-------|-----------|------|----------------|
| 1 | Starmie (Fan et al.) | 126 | 2022 | 42.0 |
| 2 | Schema matching PLMs (Zhang et al.) | 50 | 2023 | 25.0 |
| 3 | It's ai match (Hättasch et al.) | 32 | 2022 | 10.67 |
| 4 | REMA (Koutras et al.) | 39 | 2020 | 7.8 |
| 5 | Employing word-embedding (Oh et al.) | 7 | 2024 | 7.0 |

---

## Suggested Follow-up Questions

**From Scholar Labs:**
(No specific follow-up questions were suggested by Scholar Labs for this query)

**Based on Literature Gaps:**
1. How do transformer-based embeddings (BERT, GPT) compare to Word2Vec for schema matching accuracy?
2. What benchmark datasets exist for evaluating embedding-based schema matching approaches?
3. How can embedding-based schema matching be applied specifically to NL2SQL column selection?
4. What role does contrastive learning play in improving column embedding quality for data lake applications?

---

## BibTeX Citations

```bibtex
@article{hattasch2022ai,
title={It's ai match: A two-step approach for schema matching using embeddings},
author={H{\"a}ttasch, Benjamin and Truong-Ngoc, Minh and Schmidt, Alexander and others},
journal={arXiv preprint arXiv:2203.04366},
year={2022}
}

@inproceedings{koutras2020rema,
title={REMA: Graph Embeddings-based Relational Schema Matching},
author={Koutras, Christos and Fragkoulis, Marios and others},
booktitle={EDBT/ICDT Workshops},
year={2020}
}

@inproceedings{nozaki2019semantic,
title={Semantic schema matching for string attribute with word vectors},
author={Nozaki, Kohei and Hochin, Teruhisa and Nomiya, Hiroki},
booktitle={2019 6th International Conference on Computational Science and Computational Intelligence},
year={2019},
organization={IEEE}
}

@article{fan2022starmie,
title={Semantics-aware dataset discovery from data lakes with contextualized column-based representation learning},
author={Fan, Grace and Wang, Jin and Li, Yuliang and Zhang, Dan and Miller, Ren{\'e}e},
journal={arXiv preprint arXiv:2210.01922},
year={2022}
}

@article{oh2024employing,
title={Employing word-embedding for schema matching in standard lifecycle management},
author={Oh, Hyun and Jones, Andrew and Finin, Tim},
journal={Journal of Industrial Information Integration},
year={2024},
publisher={Elsevier}
}

@article{nozaki2019evaluation,
title={Semantic schema matching for string attribute with word vectors and its evaluation},
author={Nozaki, Kohei and Hochin, Teruhisa and Nomiya, Hiroki},
journal={International Journal of Networked and Distributed Computing},
year={2019},
}
publisher={Springer}

@inproceedings{du2024situ,
title={In situ neural relational schema matcher},
author={Du, Xiang and Yuan, Ge and Wu, Songyang and Chen, Gang and others},
booktitle={2024 IEEE 40th International Conference on Data Engineering},
year={2024},
organization={IEEE}
}

@inproceedings{satti2022significance,
title={Significance of Syntactic Type Identification in Embedding Vector based Schema Matching},
author={Satti, Farah Asghar and Hussain, Muhammad and Lee, Sungyoung and others},
booktitle={2022 16th International Conference on Ubiquitous Information Management and Communication},
year={2022},
organization={IEEE}
}

@inproceedings{zhang2023schema,
title={Schema matching using pre-trained language models},
author={Zhang, Yunjia and Floratou, Avrilia and Cahoon, Joyce and others},
booktitle={2023 IEEE 39th International Conference on Data Engineering},
year={2023},
organization={IEEE}
}

@article{pan2022semantic,
title={Semantic-similarity-based schema matching for management of building energy data},
author={Pan, Zheng and Pan, Guobin and Monti, Antonello},
journal={Energies},
volume={15},
number={23},
pages={8894},
year={2022},
publisher={MDPI}
}
```1
}}}}}}}}}}
