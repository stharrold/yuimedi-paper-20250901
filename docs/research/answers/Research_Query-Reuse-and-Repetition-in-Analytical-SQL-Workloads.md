# Research: How repetitive or reusable are analytical SQL queries in real-world database workloads?

**Scope:** Paper1
**Issue:** [#535](https://github.com/stharrold/yuimedi-paper-20250901/issues/535) (i-JMR R1, Reviewer Q#2)
**Date:** 2026-06-06
**Status:** Answered
**Source:** Google Scholar Labs (10 relevant results; first phrasing bounced, succeeded as a research question)
**Query:** "How repetitive or reusable are analytical SQL queries in real-world database query logs?"

## Key Findings

Reviewer Q#2 argued that if an organization needs "only ~50 frequent queries," documentation or an industry knowledge base would suffice, so the framework's value depends on query volume/diversity/frequency. The database-systems literature on query-log analysis lets the paper answer this concretely: real analytical workloads have a large recurring core AND a substantial ad-hoc long tail, which is exactly the regime where capturing Validated Query Triples pays off.

Evidence that workloads are highly repetitive (supports capturing reusable knowledge):
- Jindal et al. (Peregrine, Microsoft, 2019): "more than half of big data analytical workloads at Microsoft are repetitive" (same queries run periodically with new parameters).
- Marcus et al. (CIDR 2026): OLAP query repetition rates of 58%-75% across vendor platforms.
- Jain (2019): in the Sloan Digital Sky Survey workload, over 97% of ~7 million queries were duplicates.
- Jain et al. (SQLShare, 2016): 37% of total runtime attributable to duplicate queries; recurring SQL "idioms"/design patterns for curation, cleaning, integration.
- de Souza & Guedes (2023): 50% of queries in a real financial organization's database had medium-to-high structural similarity.

Evidence that diversity/ad-hoc volume is also large (so static documentation alone is insufficient, motivating NL-to-SQL + validation):
- Kul et al. (2018): even comparatively small production databases log hundreds-to-thousands of distinct query strings.
- SQLShare (Jain et al. 2016; Moreau & Peralta 2021): the workload is primarily ad-hoc, hand-written queries reflecting genuine interactive human exploration.

Caveat to cite for balance:
- Marcus et al. (2026) argue high repetition may be partly an artifact of systems with high ad-hoc "startup costs" that discourage exploratory queries, not a fundamental property of analytical work.

**For the paper (B2, #535):** Add a scope-conditions paragraph: analytical workloads combine a heavily recurring core (50-97% repetition/duplication reported) with a long tail of distinct ad-hoc queries (hundreds-to-thousands of distinct strings even in small DBs). Pure documentation captures only the static core and decays; HITL-KG is warranted precisely because the recurring core is large enough to be worth validating and reusing, while the ad-hoc tail needs NL-to-SQL with human validation rather than pre-written docs. This reframes Q#2's "~50 queries" objection: the recurring set is real, but it is neither tiny nor static.

## Sources

| # | Citation | Venue / Year | URL | Key datum |
|---|----------|--------------|-----|-----------|
| 1 | Jindal A, Patel H, Roy A, Qiao S, Yin Z, Sen R, et al. Peregrine: workload optimization for cloud query engines. | ACM SoCC, 2019 | https://dl.acm.org/doi/abs/10.1145/3357223.3362726 | >50% of Microsoft big-data analytical workloads are repetitive. Cited 42 |
| 2 | Marcus R, Tao J, Wu P, Zhao Z. Survivorship bias in industrial database workloads. | CIDR, 2026 | https://mail.vldb.org/cidrdb/papers/2026/p22-marcus.pdf | OLAP repetition 58%-75%; may be a systems artifact |
| 3 | Jain S. Learning from SQL: database-agnostic workload management. | Univ. Washington thesis, 2019 | https://digital.lib.washington.edu/researchworks/items/982f062d-f9e2-4d40-b2a9-16138851fa77 | SDSS: >97% of 7M queries duplicates; recurring SQL idioms |
| 4 | Jain S, Moritz D, Halperin D, Howe B, et al. SQLShare: results from a multi-year SQL-as-a-service experiment. | ACM SIGMOD, 2016 | https://dl.acm.org/doi/abs/10.1145/2882903.2882957 | 37% runtime from duplicates; ad-hoc workload; recurring idioms. Cited 113 |
| 5 | Kul G, Luong DTA, Xie T, Chandola V, et al. Similarity metrics for SQL query clustering. | IEEE TKDE, 2018 | https://ieeexplore.ieee.org/abstract/document/8352666/ | Small production DBs log hundreds-thousands of distinct queries. Cited 81 |
| 6 | de Souza BS, Guedes LA. Application of graph theory in the analysis of query similarity and complexity in relational databases. | CBIC, 2023 | https://sbia.org.br/wp-content/uploads/2023/10/pdf/CBIC_2023_paper084.pdf | 50% of queries in a financial org DB had medium-high similarity |
| 7 | Moreau C, Peralta V. Learning analysis behavior in SQL workloads. | DOLAP/Big Data, 2021 | https://hal.science/hal-03457775/document | SQLShare ad-hoc exploration; recurring analysis patterns |
| 8 | Arzamasova N, Schäler M, et al. Cleaning antipatterns in an SQL query log. | IEEE TKDE, 2017 | https://ieeexplore.ieee.org/abstract/document/8103787/ | Antipatterns/redundancy prevalent in real query logs. Cited 33 |
| 9 | Wang J, Li T, Wang A, Liu X, Chen L, Chen J, et al. Real-time workload pattern analysis for large-scale cloud databases. | arXiv, 2023 | https://arxiv.org/abs/2307.02626 | Alibaba Workload Miner; SQL pattern discovery/reuse. Cited 26 |
| 10 | Yang X, Procopiuc CM, et al. Recommending join queries via query log analysis. | IEEE ICDE, 2009 | https://ieeexplore.ieee.org/abstract/document/4812469/ | Reusable query "slices" recombined for new queries. Cited 61 |

## Next steps
- Add BibTeX entries for the chosen cites to `references.bib` (feeds #542).
- Use in #535 (B2) for the scope-conditions paragraph (recurring core vs ad-hoc tail).
