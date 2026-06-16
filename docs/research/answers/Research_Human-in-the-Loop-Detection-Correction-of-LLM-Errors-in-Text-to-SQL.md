# Research: Do human experts reliably detect and correct LLM errors in text-to-SQL / data analytics, and do human-in-the-loop reviewers outperform the model alone?

**Scope:** Paper1
**Issue:** [#544](https://github.com/stharrold/yuimedi-paper-20250901/issues/544) (i-JMR R1, Reviewer Q#3)
**Date:** 2026-06-06
**Status:** Answered
**Source:** Google Scholar Labs (session evaluated 10 relevant results)
**Query:** "Empirical evidence that human experts detect and correct large language model errors in text-to-SQL or data analytics tasks; do human-in-the-loop reviewers outperform the model alone?"

## Key Findings

Multiple recent peer-reviewed studies provide direct empirical evidence that human-in-the-loop (HITL) review improves the accuracy of LLM-generated SQL and data-analytics outputs, with several reporting quantified gains over model-alone baselines:

- *LLM + human reviewer outperforms model-alone and human-alone.* Gartlehner et al. (Annals of Internal Medicine, 2025), a prospective parallel-group study across six systematic reviews, found AI-assisted extraction (LLM output verified by a human) reached 91.0% accuracy / 89.4% sensitivity vs 89.0% / 86.5% for the human-only method, with a lower incorrect-extraction rate (9.0% vs 11.0%).
- *Quantified HITL gain over end-to-end LLM.* Benzarti & Berrabah (Springer, 2026) report a 28.4% improvement in semantic correctness over end-to-end LLM approaches via a validation-gate mechanism where experts review/modify generated SQL before execution.
- *Expert corrections raise accuracy.* HITSQL (Al-Turki et al., IEEE, 2025) combines HITL with progressive active learning and expert corrections, reaching 97% average accuracy on unseen queries. HLR-SQL (Eckmann et al., Information Systems, 2026) shows targeted human help (model selectively asks when facing ambiguity/execution errors) yields significantly higher accuracy, especially on complex queries.
- *Expert verification improves the data itself.* ReViSQL (Zhu et al., arXiv 2026) had SQL experts detect/correct annotation errors in 52.1% of queries in a BIRD-Train subset; training on the expert-verified data alone boosted single-generation accuracy by 8.2-13.9%.

Important counter-evidence to keep the Viewpoint balanced (and to cite honestly per Q#3):

- *Human error-handling is not automatically effective.* Ning et al. (ACM TiiS, 2024) and Ning et al. (Proc. 2023), via controlled user studies with 26 participants of varying SQL expertise, found that existing interactive error-handling mechanisms had limited impact on the efficiency and accuracy of error discovery and repair for state-of-the-art NL2SQL models. This qualifies the HITL claim: the loop helps only when the interaction is well-designed and targeted.
- *Human expert review still finds substantial residual error.* Chen et al. (arXiv 2025, enterprise Text-to-SQL) report human experts rated only 53% of chatbot responses 4-5 on a 1-5 rubric, evidence that human review is necessary precisely because model-alone output is frequently wrong.

**Bottom line for the paper:** The evidence supports framing HITL-KG prescriptively: HITL review measurably improves NL-to-SQL/data-analytics accuracy over model-alone in several 2025-2026 studies (including a high-impact medical journal), but the gain is conditional on targeted, well-designed human interaction. This both answers Reviewer Q#3 and motivates the Paper 2 empirical validation rather than overclaiming.

## Sources

| # | Citation | Venue / Year | URL | Relevance |
|---|----------|--------------|-----|-----------|
| 1 | Eckmann T, Urban M, Bodensohn JM, Binnig C. HLR-SQL: Human-like reasoning for Text-to-SQL with the human in the loop. | Information Systems (Elsevier), 2026 | https://www.sciencedirect.com/science/article/pii/S0306437925001565 | HITL yields significantly higher accuracy; model selectively asks for human help on ambiguity/execution errors |
| 2 | Benzarti S, Berrabah C. Generative AI for Intelligent Data Extraction: A Case Study in Automated Excel-to-SQL with Human Oversight. | Springer (EAI Intl. Conf.), 2026 | https://link.springer.com/chapter/10.1007/978-3-032-16638-8_11 | Validation-gate HITL; +28.4% semantic correctness over end-to-end LLM |
| 3 | Ning Z, Tian Y, Zhang Z, Zhang T, Li TJJ. Insights into natural language database query errors: from attention misalignment to user handling strategies. | ACM Trans. Interact. Intell. Syst., 2024 | https://dl.acm.org/doi/abs/10.1145/3650114 | 26-participant user study; existing error-handling mechanisms have limited effectiveness (counter-evidence) |
| 4 | Al-Turki D, Basurra S, Gaber M, Attasi B, et al. HITSQL: Human-In-The-Loop Techniques for Enhancing Text-to-SQL Query Generation with LLMs. | IEEE IJCNN(?), 2025 | https://ieeexplore.ieee.org/abstract/document/11227910/ | HITL + active learning + expert corrections; 97% accuracy on unseen queries |
| 5 | Ning Z, Zhang Z, Sun T, Tian Y, Zhang T, et al. An empirical study of model errors and user error discovery and repair strategies in natural language database queries. | Proc. 28th Intl. Conf. (ACM), 2023 | https://dl.acm.org/doi/abs/10.1145/3581641.3584067 | Taxonomy of NL2SQL model errors; 26-participant repair study |
| 6 | Zhu Y, Jin T, Choi Y, Kang D. ReViSQL: Achieving Human-Level Text-to-SQL. | arXiv:2603.20004, 2026 | https://arxiv.org/abs/2603.20004 | Experts corrected 52.1% of queries; expert-verified data boosts accuracy 8.2-13.9% |
| 7 | Nejjar M, Zacharias L, Stiehle F, et al. LLMs for science: usage for code generation and data analysis. | J. Software: Evolution and Process (Wiley), 2025 | https://onlinelibrary.wiley.com/doi/abs/10.1002/smr.2723 | Empirical LLM code/data-analytics study; human intervention required to correct outputs |
| 8 | Gartlehner G, Kugley S, Crotty K, et al. Artificial Intelligence-Assisted Data Extraction With a Large Language Model: A Study Within Reviews. | Annals of Internal Medicine, 2025 | https://www.acpjournals.org/doi/abs/10.7326/ANNALS-25-00739 | LLM+human 91.0%/89.4% vs human-only 89.0%/86.5%; high-impact medical journal |
| 9 | Chen A, Bundele M, Ahlawat G, Stetz P, Wang Z, et al. Text-to-SQL for enterprise data analytics. | arXiv:2507.14372, 2025 | https://arxiv.org/abs/2507.14372 | Human-expert rubric evaluation; only 53% rated 4-5, motivating human review |

_Note: Benzarti & Berrabah appeared twice in the result set (Springer chapter + Google Books edition of the same Excel-to-SQL case study); recorded once. Author lists truncated by Scholar Labs are marked "et al." and should be completed from the DOI when adding BibTeX entries (see #542)._

## Next steps
- Add BibTeX entries (full author lists, volume/issue/pages/DOI) for the cited subset to `references.bib` (feeds #542).
- Use in #536 (B3) to frame HITL-KG as prescriptive-pending-validation, citing both the supporting gains and the Ning et al. caveat for balance.
