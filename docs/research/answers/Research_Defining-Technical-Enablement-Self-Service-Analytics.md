# Research: How is "technical enablement" (analytics/data enablement) defined in the literature?

**Scope:** Paper1
**Issue:** [#547](https://github.com/stharrold/yuimedi-paper-20250901/issues/547) (i-JMR R1, Reviewer T#1)
**Date:** 2026-06-06
**Status:** Answered
**Source:** Google Scholar Labs (10 relevant results)
**Query:** "technical enablement and self-service analytics in enterprise organizations"

## Key Findings

"Technical enablement" is best grounded in the established self-service business intelligence / analytics (SSBI / SSBA) literature, where "enablement" is a recognized term for the technologies, tools, and support that let non-specialist users perform analytics without heavy reliance on central IT/BI teams:

- *Direct use of the term.* Bani-Hani, Tona & Carlsson (2020) include a "Technical Enablement" theme: the technical department "provides data, tools, and technologies specifically optimized to lower the operational complexity of processing data into information" in a self-service business analytics environment. This is the closest literal anchor for the paper's construct.
- *Self-service analytics as technologies + processes + governance.* Oladimeji et al. (2023) define self-service analytics as "the set of technologies, processes, and governance models that enable non-technical users to access, explore, and analyze data without heavy reliance on centralized data teams," and catalog technical enablers (data catalogs, semantic layers, lineage tracking, monitoring).
- *Foundational SSBI definitions.* Alpar & Schulz (2016) define SSBI as empowering casual and power users to perform custom analytics without BI specialists, with graded levels of self-service and corresponding technical support. Imhoff & White (2011) define self-service BI as the facilities enabling users to be more self-reliant and less dependent on IT for reports, queries, and analytics.
- *Enablement as an organizational shift.* Kadakia (2025) frames successful self-service BI transformation as an "organizational evolution from gatekeeping to enablement" plus a "stakeholder enablement program" and an Analytics Center of Excellence, useful for connecting technical enablement to the paper's governance themes.
- *The bottleneck enablement addresses.* Hellerstein, Heer & Kandel (2018) identify the lack of technology enabling domain experts to do end-to-end data preparation without programming as the primary bottleneck, directly motivating "technical enablement."

**For the paper (T#1):** Define technical enablement as the technologies, tools, and supporting practices that enable non-specialist domain users to access and analyze data without heavy reliance on central IT, citing the SSBI/SSBA literature (Alpar & Schulz 2016; Bani-Hani et al. 2020 for the term itself; Oladimeji et al. 2023 for the technologies+processes+governance framing). This also dovetails with HITL-KG, since enablement without governance is the failure mode these sources flag.

## Sources

| # | Citation | Venue / Year | URL | Note |
|---|----------|--------------|-----|------|
| 1 | Alpar P, Schulz M. Self-service business intelligence. | Business & Information Systems Engineering, 2016 | https://link.springer.com/article/10.1007/s12599-016-0424-6 | SSBI empowers users without BI specialists; levels of self-service + technical support. Cited 302 |
| 2 | Bani-Hani I, Tona O, Carlsson S. Patterns of resource integration in the self-service approach to business analytics. | HICSS, 2020 | https://scholarspace.manoa.hawaii.edu/bitstreams/b903b5be-7c88-4779-ad12-3ae86418926a/download | Explicit "Technical Enablement" theme: dept provides data/tools/tech to lower processing complexity |
| 3 | Oladimeji O, Ayodeji DC, Erigha ED, Eboseremen BO, et al. Governance models for scalable self-service analytics. | Intl. J. (review), 2023 | (search title; no stable URL captured) | Defines self-service analytics as technologies+processes+governance; catalogs technical enablers |
| 4 | Imhoff C, White C. Self-service business intelligence: empowering users to generate insights. | TDWI / Tableau whitepaper, 2011 | https://origin-tableau-www.tableau.com/sites/default/files/whitepapers/ssbi-jul12-11.pdf | SSBI = facilities making users self-reliant, less dependent on IT |
| 5 | Michalczyk S, Nadj M, Azarfar D, Maedche A, Gröger C. A state-of-the-art overview and future research avenues of SSBIA. | ECIS, 2020 | https://aisel.aisnet.org/ecis2020_rp/46/ | SSBIA state-of-the-art; levels of self-service from usage to resource creation |
| 6 | Hellerstein JM, Heer J, Kandel S. Self-service data preparation: research to practice. | IEEE Data Eng. Bull., 2018 | http://sites.computer.org/debull/A18june/p23.pdf | Lack of enabling technology for non-programmers is the data-prep bottleneck |
| 7 | Schlesinger PA, Rahman N. Self-service business intelligence resulting in disruptive technology. | J. Computer Information Systems, 2016 | https://www.tandfonline.com/doi/abs/10.1080/08874417.2015.11645796 | SSBI enables users to access/manipulate data without heavy IT; raises enterprise agility |
| 8 | Passlick J, Lebek B, Breitner MH. A self-service supporting BI and big data analytics architecture. | WI, 2017 | https://aisel.aisnet.org/wi2017/track12/paper/5/ | Technical architecture enabling casual users to build analyses independently |
| 9 | Syed S, Nampally RCR. Empowering users: the role of AI in enhancing self-service BI. | SSRN, 2021 | https://papers.ssrn.com/sol3/Delivery.cfm?abstractid=5017971 | AI (NLP/ML) democratizes data access for non-technical users |
| 10 | Kadakia JJ. From legacy to leadership: a case study in self-service BI transformation. | J. Computer Science and Technology Studies, 2025 | https://al-kindipublishers.org/index.php/jcsts/article/view/10754 | "Organizational evolution from gatekeeping to enablement"; stakeholder enablement program + Analytics CoE |

## Next steps
- Add BibTeX entries (full author lists, volume/issue/pages/DOI) for the chosen cites to `references.bib` (feeds #542). For #3 (Oladimeji et al.), recover a stable DOI/URL when adding the entry.
- Use in #538 (B5) to define technical enablement, one of the three title constructs.
