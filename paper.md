---
title: "Mitigating Institutional Amnesia: A Design Science Framework for Socio-Technical Query Governance in Healthcare"
author: "Samuel T Harrold, Yuimedi, Inc."
correspondence: "samuel.harrold@yuimedi.com"
date: "January 2026"
version: "2.1.0"
abstract: |
  **Background:** Healthcare organizations face a "Triple Threat" of low analytics maturity, high workforce instability, and semantic technical barriers. Recent data reveals a crisis of "Institutional Amnesia," where 53% of healthcare CIOs have less than three years' tenure and 55% of informatics specialists intend to leave their roles. This churn erases the tacit knowledge required to navigate complex clinical data schemas, trapping organizations in a cycle of low maturity.

  **Objective:** This article proposes a socio-technical framework to mitigate institutional amnesia by decoupling organizational analytical capability from individual staff tenure. We aim to answer the research question: *How can health systems maintain analytics maturity when workforce turnover exceeds the speed of documentation?*

  **Methods:** We employed a Design Science Research (DSR) approach, synthesizing evidence from healthcare informatics, knowledge management, and natural language processing. The framework is grounded in Nonaka’s SECI model of knowledge creation, reinterpreting "Socialization" vulnerabilities through the lens of workforce turnover data (2024-2025).

  **Results:** We present the "Human-in-the-Loop Semantic Governance" (HiL-SG) framework. This architecture functions as a socio-technical artifact that converts tacit domain expertise into explicit, executable "Validated Query Triples" (Natural Language + SQL + Rationale). By shifting the locus of knowledge from volatile human memory to durable semantic artifacts, the framework enables an "Analytics Resilience Index" (ARI) that measures an organization's ability to sustain insights despite staff churn.

  **Conclusions:** The "Validator Paradox"—who validates the AI when experts leave?—is resolved by treating validation as "standard work" rather than eternal truth. By embedding knowledge capture into the daily workflow of query generation, healthcare systems can build a "knowledge ratchet" that prevents the regression of capabilities, ensuring that analytics maturity advances even as the workforce evolves.
keywords: [institutional amnesia, healthcare analytics, socio-technical systems, query governance, natural language to SQL, SECI model, workforce turnover, design science research]
license: "CC BY 4.0"
license-url: "https://creativecommons.org/licenses/by/4.0/"
lang: en-US
toc: true
toc-depth: 3
numbersections: true
geometry: margin=1in
fontsize: 11pt
linestretch: 1.15
colorlinks: true
linkcolor: blue
urlcolor: blue
citecolor: blue
---

# Introduction

## The Triple Threat: A Crisis of Institutional Amnesia

The healthcare analytics landscape is currently paralyzed by a "Triple Threat" of compounding failures: (1) persistently **Low Analytics Maturity**, where despite decades of investment, only 39 organizations globally, 26 at HIMSS AMAM Stage 6 and 13 at Stage 7, have achieved these maturity levels [@himss2024]; (2) a **Semantic Gap** between clinical intent and technical schema implementation [@gal2019; @zhang2024]; and (3) a profound crisis of **Workforce Instability** that creates "Institutional Amnesia" [@hong2025].

While technical barriers and maturity models are well-documented, the workforce dimension has shifted from a management concern to an existential threat. Modern longitudinal data on analytics staff is fragmented, but the available signals are alarming. As of 2024, 53% of healthcare CIOs have held their roles for less than three years [@wittkieffer2024], creating a strategic vacuum at the top. At the operational level, the situation is equally precarious: 79% of provider organizations report persistent shortages in digital health roles [@himssworkforce2024], and a 2025 study found that 55% of public health informatics specialists intend to leave their positions [@rajamani2025].

This turnover creates a phenomenon we define as **Institutional Amnesia**: the systematic erasure of the tacit knowledge required to interpret complex health data. In healthcare, "data" is never raw; it is wrapped in layers of institutional context—billing rules, workflow workarounds, and unwritten exclusions [@american2023]. When the analyst who knows that "exclusion code 99" actually means "hospice transfer" leaves, that knowledge evaporates. The organization does not just lose an employee; it loses the ability to accurately measure its own performance.

## Gap Analysis: The Speed of Forgetting

Current literature approaches these problems in isolation. Analytics maturity models (e.g., HIMSS AMAM) assume a stable workforce capable of linear progression [@himss2024; @wang2018]. Technical solutions (e.g., NL2SQL) assume a stable schema and clear intent [@wang2020]. Neither accounts for the reality of the "Great Resignation," where the rate of knowledge loss ("organizational forgetting") often exceeds the rate of knowledge capture [@rao2006].

Traditional knowledge management strategies—wikis, data dictionaries, and documentation—have failed because they are *passive* [@mayo2016]. They require overworked staff to stop working and write down what they know. In a high-burnout environment, this documentation is the first casualty. As a result, healthcare systems are trapped in a Sisyphus-like cycle: hiring new analysts who spend their average 2.9-year tenure [@ang2004] relearning the same institutional secrets, only to leave just as they become productive [@ledikwe2013; @mantas2010].

## Research Question

This viewpoint article addresses a critical socio-technical gap:
*How can health systems maintain analytics maturity when workforce turnover exceeds the speed of documentation?*

We propose that the solution lies not in better documentation, but in a fundamental architectural shift: moving from *passive* knowledge management to **Human-in-the-Loop Semantic Governance (HiL-SG)**.

# Methods

We employed a Design Science Research (DSR) approach to develop the HiL-SG framework. DSR involves the creation and evaluation of innovative artifacts (constructs, models, methods, and instantiations) to solve identified organizational problems.

Our methodology followed three steps:
1.  **Problem Identification**: We conducted a narrative review of the literature (n=139 sources) across three domains: healthcare analytics maturity, workforce turnover dynamics, and natural language processing. Grey literature was assessed using the AACODS checklist [@tyndall2010].
2.  **Theoretical Grounding**: We analyzed the identified problem ("Institutional Amnesia") through the lens of Nonaka’s SECI model of knowledge creation [@farnese2019], mapping workforce turnover data to specific failure modes in knowledge transfer.
3.  **Artifact Design**: We designed the HiL-SG framework and the "Validated Query Triple" artifact as socio-technical solutions to the identified "Socialization Failure," adhering to "Human-on-the-Loop" principles for AI safety [@bravorocca2023].

# Results

## Theoretical Framework: SECI for the Unstable Workforce

We ground our approach in Nonaka’s SECI Model of knowledge creation (Socialization, Externalization, Combination, Internalization), reinterpreted for the crisis of the modern healthcare workforce.

### The Broken Cycle: Socialization Failure
In Nonaka’s model, **Socialization** is the transfer of tacit knowledge (experience, context) between individuals through shared experience [@farnese2019]. In the current healthcare environment, this mechanism has collapsed. High turnover rates fracture the social networks required for mentorship [@wu2024; @ren2024]. When a senior analyst leaves every 3 years, the "apprenticeship" model of informatics breaks down. Socialization is no longer a viable strategy for resilience [@massingham2018].

### The Solution: Externalization via Socio-Technical Artifacts
To survive, organizations must shift reliance from Socialization to **Externalization**: converting tacit knowledge into explicit, durable artifacts [@zhang2025]. However, traditional externalization (writing reports) is too slow and low-fidelity [@goffin2011; @foos2006].

We propose a new socio-technical artifact: the **Validated Query Triple**.
This artifact consists of:
1.  **Natural Language Intent**: The clinical business question (e.g., "Hypertension readmissions excluding planned transfers").
2.  **Executable SQL**: The technical implementation.
3.  **Rationale Metadata**: The "why" behind the logic (e.g., "Excluding status 02 per CMS 2025 rule").

By capturing these three components *during the act of analytics*, we transform the ephemeral work of query generation into a permanent institutional asset [@moore2018].

## Human-in-the-Loop Semantic Governance (HiL-SG)

We rename the traditional "Validated Query Cycle" to **Human-in-the-Loop Semantic Governance (HiL-SG)** to reflect its role as a governance mechanism rather than just a productivity tool.

### The HiL-SG Architecture

The HiL-SG architecture (Figure 1) functions as a **Governance Forcing Function**. It inserts a mandatory validation step into the analytics workflow, preventing the "laundering" of hallucinations while simultaneously capturing expert knowledge.

![Healthcare Analytics Architecture as a Socio-Technical System. The architecture flows from Clinical Users through a Conversational AI interface to a healthcare NLP engine for context-aware SQL generation. Bi-directional arrows represent the iterative 'Query & Refine' loop. The critical validation step (dotted line) shows domain experts confirming SQL before results flow to 'Organizational Memory' (dashed line), where they persist independent of staff tenure.](figures/architecture.mmd.png){width=95%}

The corresponding six step Validated Query Cycle is summarized in Figure 2, which shows how queries move from initial clinical intent through expert validation into durable organizational memory.

![Six step validated query cycle for Human-in-the-Loop Semantic Governance. The cycle progresses from Natural Language Intent to AI-generated SQL, expert review and correction, creation of a Validated Query Triple, storage in organizational memory, and reuse for future queries.](figures/knowledge-cycle.mmd.png){width=80%}

### The Process of Externalization
1.  **Query Generation**: A user asks a question. The AI proposes SQL based on schema knowledge [@lee2023; @wang2020].
2.  **Semantic Translation**: The AI translates the SQL back into a natural language explanation [@ziletti2024].
3.  **Expert Validation**: The domain expert confirms or corrects this interpretation. *This is the critical moment of Externalization.* This "Human-on-the-Loop" (HotL) step transforms validation into an iterative knowledge capture process [@bravorocca2023; @mosqueirarey2023].
4.  **Artifact Storage**: The validated triple is hashed and stored in organizational memory [@benbya2004].
5.  **Retrieval**: Future queries semantically match against this repository first, retrieving *trusted* human knowledge before attempting *probabilistic* generation [@whittaker2008].

## Empirical Grounding: The Evidence Base

The HiL-SG framework is supported by three pillars of empirical evidence synthesized from over 130 sources.

### Pillar 1: Analytics Maturity Evidence
Healthcare maturity remains chronically low. Assessments reveal only 26 organizations achieved Stage 6 and 13 reached Stage 7 by late 2024 [@himss2024; @himss2024news]. Most organizations remain at Stages 0-3, characterized by fragmented data and limited predictive capabilities [@health2020]. However, maturity is not merely an IT metric; it is a clinical safety predictor. EMRAM levels 6-7 correlate with 3.25 times higher odds of better Leapfrog Safety Grades [@snowdon2024]. Low maturity creates a "low-maturity trap" where data quality issues—such as the 39-71% missing data rates in cancer databases [@yang2021]—remain uncorrected because the experts who understand the context are leaving.

### Pillar 2: Workforce Agility Evidence
The cost of turnover in informatics is higher than standard IT. Knowledge loss can cost up to three times annual salary [@massingham2018; @oracle2024]. With 30% of new employees leaving within their first year [@nsi2025], healthcare IT professionals spend a limited portion of their employment at full productivity, as specialized roles require 18-24 months to reach fluency [@ledikwe2013; @konrad2022]. This "revolving door" prevents the accumulation of the "Collective Knowledge Structures" required for complex task performance [@rao2006].

### Pillar 3: Technical Enablement Evidence
NL2SQL has reached a productivity tipping point. Natural language interfaces report a 63% increase in self-service adoption and 37% reduction in retrieval time [@dadi2025]. Precision medicine platforms achieve 92.5% accuracy in parsing complex queries [@yang2025]. While current models are "not yet sufficiently accurate for unsupervised use" [@ziletti2024], domain-adapted systems like MedT5SQL reach 80% accuracy on benchmarks [@marshan2024]. These tools function as the "externalization engine" required for the HiL-SG framework.

## Analytics Resilience Index (ARI)

To measure success, we propose the **Analytics Resilience Index (ARI)**, replacing static checklists with dynamic resilience metrics.

| Dimension | Low Resilience (Fragile) | High Resilience (Antifragile) | Evidence |
|:---|:---|:---|:---|
| **Knowledge Locus** | Knowledge resides in "Hero" analysts. | Knowledge resides in the System/Repository. | [@hong2025; @benbya2004] |
| **Turnover Impact** | Departure of 1 staff member stops reporting. | Departure causes minimal disruption; successors inherit queries. | [@massingham2018; @rao2006] |
| **Validation Mode** | Ad-hoc, email-based, ephemeral. | Systematic, artifact-based, durable (HiL-SG). | [@moore2018; @mosqueirarey2023] |
| **Schema Coupling** | Hard-coded reports break on schema change. | Semantic layer adapts; CI/CD detects drift. | [@mannapur2025; @battula2025] |

: The Analytics Resilience Index (ARI). \label{tab:ari}

# Discussion

## The Validator Paradox and Standard Work
A critical criticism of HiL-SG is the **Validator Paradox**: *If the experts are leaving, who is left to validate the AI?* We resolve this by reframing validation through Lean "Standard Work" [@alukal2006]. Validation is the establishment of the *current known standard*. When an analyst validates a query, they act as a **Knowledge Ratchet** [@rao2006], preventing the organization from sliding back to zero. This aligns with UC Davis Health's success in moving from AMAM Stage 0 to 6 by establishing standardized "S.M.A.R.T." definitions [@himss2025ucdavis].

## Safety: Cognitive Forcing Functions
Automating analytics risks "laundering hallucinations." HiL-SG mitigates this via **Cognitive Forcing Functions** [@ziletti2024]. By requiring AI to explain logic *before* results, we force the user to engage analytical thinking. User studies show this reduces error recovery time by 30-40 seconds [@ipeirotis2025].

## Structural Barriers: Why the Problem Persists
Failed standardization approaches (e.g., IBM Watson Health [@ibm2022; @strickland2019], Haven [@lavito2021; @acchiardo2021]) demonstrate that centralized models fail clinical reality. Metadata uncertainties and "messy" institution-specific business logic require localized solutions [@gal2019; @yang2020]. HiL-SG addresses this by capturing *local* logic rather than enforcing *global* standards.

## Limitations
This work is a narrative, design science informed framework rather than a systematic review or multi-site empirical evaluation. The literature base is concentrated on English-language sources and recent (2024–2025) workforce and NL2SQL studies, so findings may not capture all regional, specialty-specific, or technological contexts. The HiL-SG architecture and the proposed Analytics Resilience Index (ARI) are conceptual artifacts that require future implementation and validation in diverse health systems before their effectiveness and generalizability can be fully established.

# Conclusion

## Strategic Implications
The crisis of Institutional Amnesia in healthcare requires a structural shift. As long as analytical maturity is tied to individual tenure, organizations will remain fragile. By implementing **Human-in-the-Loop Semantic Governance**, health systems can decouple intelligence from turnover, building a library of validated knowledge that ensures maturity advances even as the workforce evolves.

Future research should empirically validate and refine the HiL-SG framework and the proposed Analytics Resilience Index. Priority questions include: how ARI scores correlate with observed continuity of analytics performance during leadership and staff turnover; whether HiL-SG mediated natural language to SQL workflows reduce error rates, recovery time, and rework compared to baseline tooling; and which governance patterns most effectively balance safety, transparency, and equity when human validators operate at scale. Prospective multi-site implementation studies, controlled user experiments, and qualitative implementation research across diverse health systems will be needed to test these claims and adapt the framework to varying organizational, regulatory, and data environments.

# Acknowledgments

The author (S.T.H.) takes full responsibility for the final content, conducted the research, and verified all claims and citations. Gemini CLI (Gemini 3, Google) assisted with manuscript editing and refinement. Figures were generated using the Mermaid graph language.

# Author Contributions

S.T.H. conceived the research, conducted the literature review, and wrote the manuscript.

# Conflicts of Interest

The author declares the following competing interests: Samuel T Harrold is a contract product advisor at Yuimedi, Inc., which develops healthcare analytics software including conversational AI platforms relevant to this review's subject matter. The author is also employed as a Data Scientist at Indiana University Health. This paper presents an analytical framework derived from published literature and does not evaluate or recommend specific commercial products, including those of the author's affiliated organizations. The views expressed are the author's own and do not represent the official positions of Indiana University Health or Yuimedi, Inc.

# Data Availability

This is a narrative review synthesizing existing literature. No primary datasets were generated or analyzed. All data cited are from publicly available peer-reviewed publications and industry reports, referenced in the bibliography.

# Funding

Yuimedi provided funding for the author's time writing and researching this manuscript.

# Abbreviations

AACODS: Authority, Accuracy, Coverage, Objectivity, Date, Significance
AI: Artificial Intelligence
AMAM: Analytics Maturity Assessment Model
ARI: Analytics Resilience Index
CIO: Chief Information Officer
DSR: Design Science Research
EMRAM: Electronic Medical Record Adoption Model
HiL-SG: Human-in-the-Loop Semantic Governance
HIMSS: Healthcare Information Management Systems Society
HotL: Human-on-the-Loop
IT: Information Technology
NL2SQL: Natural Language to SQL
SECI: Socialization, Externalization, Combination, Internalization
SQL: Structured Query Language

# References

::: {#refs}
:::
