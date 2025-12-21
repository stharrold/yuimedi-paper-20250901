---
title: "Natural Language to SQL in Healthcare: Bridging Analytics Maturity Gaps, Workforce Turnover, and Technical Barriers Through Conversational AI Platforms"
author: "Samuel T Harrold, Yuimedi"
correspondence: "https://us.yuimedi.com/contact-us/ (include 'NL2SQL paper' in message)"
date: "December 2025"
version: "1.0.0"
abstract: |
  This research examines the evidence for implementing conversational AI platforms
  in healthcare analytics, addressing three critical challenges: low healthcare analytics maturity,
  workforce turnover with institutional memory loss, and technical barriers in natural language
  to SQL generation. Through review of peer-reviewed benchmarking studies and industry implementations,
  we demonstrate that natural language interfaces can democratize analytics access while preserving
  institutional knowledge. Healthcare-specific text-to-SQL benchmarks show significant progress,
  though current models are "not yet sufficiently accurate for unsupervised use" in clinical settings.
  Healthcare IT staff turnover of ~34% (as of 2004), the highest among IT sectors at that time, creates institutional memory loss, while low-code implementations demonstrate significant efficiency gains and cost savings. The convergence of technical advances in NL2SQL generation, analytics
  maturity challenges in healthcare organizations, and workforce turnover creates conditions
  warranting organizational assessment of conversational AI platforms with appropriate governance.
  This paper contributes a three-pillar analytical framework and positions healthcare conversational
  AI as a knowledge portal architecture for institutional memory preservation.
keywords: [healthcare analytics, natural language processing, SQL generation, institutional memory, conversational AI, healthcare informatics, workforce turnover, analytics maturity]
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

<!--
# BUILD COMMANDS FOR YUIQUERY RESEARCH PAPER

## Prerequisites
- Install pandoc: https://pandoc.org/installing.html
- Install LaTeX (for PDF): https://www.latex-project.org/get/
- Optional: Install pandoc-crossref for figure/table references

## Generate PDF (Basic)
pandoc paper.md -o NL2SQL-Healthcare-Analytics-Research.pdf

## Generate PDF (High Quality with XeLaTeX)
pandoc paper.md -o NL2SQL-Healthcare-Analytics-Research.pdf \
  --pdf-engine=xelatex \
  --highlight-style=pygments \
  --toc \
  --number-sections

## Generate PDF (With Eisvogel Template - Professional Academic Look)
pandoc paper.md -o NL2SQL-Healthcare-Analytics-Research.pdf \
  --template=eisvogel \
  --pdf-engine=xelatex \
  --listings

## Generate HTML (Standalone)
pandoc paper.md -o NL2SQL-Healthcare-Analytics-Research.html \
  --standalone \
  --toc \
  --toc-depth=3 \
  --self-contained

## Generate Word Document
pandoc paper.md -o NL2SQL-Healthcare-Analytics-Research.docx

## With Citation Processing (Note: Citations are already formatted in text)
pandoc paper.md -o NL2SQL-Healthcare-Analytics-Research.pdf \
  --pdf-engine=xelatex \
  --toc \
  --number-sections
-->

# Executive Summary

Healthcare organizations face a convergence of challenges that affect their ability to leverage data for improved patient outcomes and operational efficiency. This research examines evidence across three interconnected domains: persistently low healthcare analytics maturity, significant institutional memory loss from workforce turnover, and technical barriers preventing clinical professionals from accessing their own data.

Through systematic review of academic and industry sources, we demonstrate that few healthcare organizations worldwide have achieved advanced analytics maturity, while healthcare IT staff turnover was measured at 34% (as of 2004) [A10], the highest among IT sectors at that time, creating institutional memory loss with knowledge loss costs reaching three times annual salary budgets [A24]. Simultaneously, natural language to SQL (NL2SQL) technologies have matured sufficiently to address healthcare's unique technical barriers, though current models are "not yet sufficiently accurate for unsupervised use" in clinical settings [A6].

Conversational AI platforms directly address this convergence by democratizing analytics access through natural language interfaces while functioning as healthcare knowledge portals [A25] that preserve institutional knowledge through encoded expertise. Evidence from healthcare implementations shows significant improvements in efficiency, with organizations like Berkshire Healthcare NHS Trust reporting over 800 citizen developers creating solutions [I4], and Forrester Research documenting 206% ROI from low-code implementations [I5].

This review identifies an analytical framework connecting these challenges. The three-pillar model presented herein offers healthcare organizations a structured approach for assessing their analytics capabilities, workforce knowledge vulnerabilities, and technical barriers to data access.

# Introduction

## Background

Healthcare analytics has emerged as a critical capability for improving patient outcomes, reducing costs, and enhancing operational efficiency. While healthcare organizations must balance cost management, regulatory compliance, and operational efficiency, these concerns serve a primary institutional imperative: delivering high-quality patient care. Analytics initiatives that fail to advance this core mission, or worse, that divert resources and attention without improving care delivery, represent a misalignment with healthcare's fundamental purpose.

However, the sector faces unique challenges that distinguish it from other data-intensive industries. Unlike technology or financial services, healthcare combines complex clinical workflows, extensive regulatory requirements, and a workforce with limited technical training but deep domain expertise [I11].

The Healthcare Information Management Systems Society (HIMSS) Analytics Maturity Assessment Model (AMAM) provides the industry standard for measuring healthcare analytics capabilities across seven stages, from basic data collection to advanced predictive modeling and AI integration. Recent assessments reveal a sobering reality: as of 2024, only 26 organizations worldwide have achieved Stage 6 maturity, with merely 13 reaching Stage 7, the highest level characterized by predictive analytics and AI integration [I1].

This analytics maturity crisis occurs amid accelerating technological advances in natural language processing and conversational AI. Large language models have demonstrated remarkable capabilities in understanding clinical terminology, generating SQL queries, and bridging the gap between natural language questions and structured data analysis. These developments create unprecedented opportunities to democratize healthcare analytics access.

Simultaneously, healthcare faces an institutional memory crisis driven by workforce turnover rates significantly higher than other knowledge-intensive sectors. A 2004 study found healthcare IT staff turnover of 34% [A10], the highest rate among all IT organization types studied at that time, creating cascading knowledge loss, particularly in analytics roles where expertise combines domain knowledge with technical skills. Traditional knowledge management approaches prove inadequate for preserving the tacit knowledge essential for effective healthcare data analysis.

## Problem Statement

Healthcare organizations face three critical, interconnected challenges that collectively threaten their ability to become data-driven enterprises:

### Low Healthcare Analytics Maturity
Despite massive investments in electronic health records and data infrastructure, healthcare organizations struggle to advance beyond basic reporting capabilities. The HIMSS AMAM reveals that most organizations remain at Stages 0-3, characterized by fragmented data sources, limited automated reporting, and minimal predictive capabilities [I1]. This low maturity severely constrains evidence-based decision making and operational optimization.

### Technical Barriers to Data Access
Healthcare professionals possess deep clinical knowledge but lack the technical skills required for data analysis. Traditional analytics tools require SQL expertise, statistical knowledge, and familiarity with complex database schemas, capabilities that clinical staff often do not possess nor have time to develop. This creates a fundamental disconnect between those who understand the clinical questions and those who can access the data to answer them [A14], [A15], [A16]. Drawing on principles from code modernization, AI-assisted interfaces can bridge this gap by transforming legacy technical requirements into natural language interactions [I8].

### Institutional Memory Loss from Workforce Turnover
A 2004 study found healthcare IT staff experienced the highest turnover among IT sectors at 34% annually (calculated as 1/2.9 years average tenure), with average tenure of only 2.9 years, the lowest among IT sectors studied at that time [A10]. This creates significant institutional memory loss. When experienced analysts, clinical informatics professionals, or data-savvy clinicians leave, they take with them irreplaceable knowledge about data definitions, business rules, analytical approaches, and organizational context. This knowledge proves extremely difficult to document and transfer through traditional means.

The implications are measurable in operational terms and potentially in patient care quality. Organizations continue investing in analytics infrastructure while struggling to realize value from their data assets. Analytics maturity gaps may lead to suboptimal clinical decisions that affect patient outcomes. Workforce turnover causes loss of institutional knowledge relevant to care continuity. Technical barriers prevent clinical staff from answering care-focused questions with data. These three interconnected challenges represent operational inefficiencies with potential implications for healthcare delivery.

## Objectives

This research aims to provide evidence-based guidance for healthcare organizations seeking to address these interconnected challenges through conversational AI platforms. Specific objectives include:

### Primary Objective
Demonstrate through systematic literature review that conversational AI platforms represent an evidence-based solution to healthcare's analytics challenges, with empirical validation of their effectiveness in addressing analytics maturity, technical barriers, and institutional memory preservation.

### Secondary Objectives
1. **Synthesize current evidence** on natural language to SQL generation capabilities and limitations in healthcare contexts
2. **Document the extent** of analytics maturity challenges across healthcare organizations globally
3. **Quantify the impact** of workforce turnover on institutional memory and analytics capabilities
4. **Identify implementation strategies** supported by empirical evidence from early adopters
5. **Establish ROI evidence** for conversational AI platform investments in healthcare settings

### Non-Goals
This research explicitly does not address:

- Specific vendor comparisons or product recommendations
- Implementation details for particular healthcare IT environments
- Regulatory compliance strategies for specific jurisdictions
- Technical architecture specifications for conversational AI systems

Note: Analysis of market dynamics and structural factors explaining why institution-specific analytics challenges persist is within scope. This market-level analysis provides necessary context for evaluating solution approaches and differs from product comparison, which would evaluate specific vendor offerings against each other or recommend particular products.

## Contributions

This paper makes three contributions to the healthcare informatics literature:

1. **Three-Pillar Analytical Framework**: We synthesize evidence from three previously disconnected research domains (healthcare analytics maturity, workforce turnover, and natural language processing) into a unified analytical framework that reveals how these challenges interconnect and compound each other: low maturity accelerates turnover, turnover degrades maturity, and technical barriers prevent recovery from either.

2. **Healthcare Knowledge Portal Architecture**: Drawing on established knowledge management literature [A25, A26], we position conversational AI platforms as healthcare knowledge portals, which are systems that provide mechanisms for knowledge acquisition, storage, sharing, and utilization. This framing addresses the institutional memory crisis in healthcare by embedding organizational expertise within AI systems rather than relying on individual staff retention.

3. **Convergence Thesis**: We demonstrate that the simultaneous occurrence of technical advances in NL2SQL, low analytics maturity, and high workforce turnover creates conditions warranting organizational assessment. This convergence positions conversational AI as a potential mechanism for institutional knowledge preservation, though implementation decisions require organization-specific evaluation.

## Document Structure

Following this introduction, the paper proceeds through four main sections. The Methodology section describes the narrative review approach, literature search strategy, and source selection criteria. The Literature Review synthesizes evidence across the three challenge domains, establishing the current state of natural language processing in healthcare, analytics maturity research, and workforce turnover impacts. The Discussion examines implications, limitations, and future research directions. Finally, the Conclusion summarizes the three-pillar analytical framework as this paper's primary contribution to healthcare informatics literature.

# Methodology

## Review Approach

This paper employs a narrative review methodology to synthesize evidence across three interconnected domains: healthcare analytics maturity, workforce turnover, and natural language to SQL technologies. Unlike systematic reviews that follow pre-registered protocols with exhaustive searches, narrative reviews provide expert synthesis of relevant literature to construct coherent arguments and identify patterns across diverse evidence sources.

The narrative review approach was selected because:

1. **Integration across domains**: The paper synthesizes evidence from distinct fields (clinical informatics, human resources, natural language processing) that require interpretive integration rather than statistical pooling
2. **Original analytical framework**: The three-pillar framework emerged iteratively from the literature rather than being pre-specified
3. **Heterogeneous evidence types**: The evidence base includes peer-reviewed research, industry reports, and benchmark datasets that cannot be meaningfully combined through meta-analysis

## Literature Search

Literature was identified through multiple channels between January 2023 and December 2024:

**Academic Databases:**

- PubMed/MEDLINE: Clinical informatics, healthcare workforce, medical administration
- IEEE Xplore and ACM Digital Library: Natural language to SQL, text-to-SQL systems
- arXiv: Machine learning and NLP preprints, benchmark studies
- Google Scholar: Cross-disciplinary search and citation tracing

**Industry Sources:**

- HIMSS publications and Analytics Maturity Model documentation
- Healthcare IT vendor case studies and implementation reports
- Market research reports (Precedence Research, Forrester)
- Professional association surveys and white papers

**Search Concepts:**

Primary search terms included combinations of: "natural language SQL," "text-to-SQL healthcare," "healthcare analytics maturity," "HIMSS AMAM," "nursing turnover," "IT workforce turnover healthcare," "institutional memory loss," "low-code healthcare analytics," and "conversational AI clinical decision support."

**Table 2: Literature Search Strategy**

| Database | Primary Search Terms | Date Range | Initial Results | After Screening |
|----------|---------------------|------------|-----------------|-----------------|
| PubMed/MEDLINE | ("natural language processing" OR "NLP") AND ("healthcare" OR "clinical") AND ("analytics" OR "SQL") | 2015-2024 | ~120 | 12 |
| IEEE Xplore | "text-to-SQL" AND ("healthcare" OR "medical" OR "clinical") | 2015-2024 | ~45 | 8 |
| ACM Digital Library | "natural language" AND "SQL" AND "healthcare" | 2015-2024 | ~30 | 5 |
| arXiv (cs.CL, cs.DB) | "healthcare" AND ("text-to-SQL" OR "NL2SQL") | 2020-2024 | ~25 | 4 |
| Google Scholar | "healthcare analytics maturity" OR "HIMSS AMAM" | 2015-2024 | ~200 | 8 |
| Google Scholar | "nursing turnover" OR "healthcare IT turnover" | 2004-2024 | ~150 | 4 |
| **Total** | | | **~570** | **41** |

*Note: Counts are approximate; exact numbers varied due to iterative search refinement. Final corpus includes 30 academic and 11 industry sources.*

Figure 1 illustrates the literature selection process, showing progression from initial database search through screening and quality assessment to the final corpus of 41 sources.

```{=latex}
\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth,keepaspectratio]{figures/literature-flow.jpg}
\caption{Literature Selection Flow Diagram. The diagram shows the progression from initial database search (n ≈ 570) through title/abstract screening, full-text review, and quality assessment (AACODS for grey literature) to the final corpus of 41 sources (30 academic, 11 industry). Diagram source available in figures/literature-flow.mmd.}
\label{fig:literature-flow}
\end{figure}
```

## Source Selection

Sources were selected based on the following criteria:

**Inclusion Criteria:**

- Peer-reviewed publications in healthcare informatics, medical informatics, computer science, or health services research
- Industry reports from established healthcare IT organizations (HIMSS, AHIMA, AMIA)
- Publications from 2015-2024, with emphasis on 2020-2024 for rapidly evolving NL2SQL technologies
- English language publications
- Sources with verifiable DOIs, URLs, or institutional attribution

**Exclusion Criteria:**

- Sources without verifiable attribution or institutional backing
- Vendor marketing materials without independent validation
- Preprints without subsequent peer-reviewed publication (exception: foundational NL2SQL benchmarks where peer review is pending)
- Studies with unverifiable statistics or methodological concerns

## Evidence Synthesis

Evidence was synthesized thematically around the three-pillar framework:

1. **Analytics maturity**: Evidence on HIMSS AMAM adoption, healthcare analytics capabilities, and organizational readiness
2. **Workforce turnover**: Evidence on nursing and IT staff turnover rates, institutional memory loss, and knowledge transfer challenges
3. **Technical barriers**: Evidence on NL2SQL benchmarks, healthcare-specific NLP challenges, and low-code implementation patterns

This framework emerged iteratively from the literature rather than being pre-specified, consistent with narrative review methodology. Citation verification followed the methodology documented in the reference verification process, which identified and removed 5 likely AI-generated fabrications and 29 unused references from the original draft.

## Grey Literature Quality Assessment

Grey literature sources were assessed using the AACODS checklist (Tyndall, 2010) [A30], which evaluates Authority, Accuracy, Coverage, Objectivity, Date, and Significance. Sources with vendor sponsorship were retained when no independent alternative existed but flagged in-text. Table 1 summarizes the assessment.

**Table 1: AACODS Assessment of Industry Sources**

| Source | Authority | Accuracy | Coverage | Objectivity | Date | Significance | Include |
|--------|-----------|----------|----------|-------------|------|--------------|---------|
| [I1] HIMSS AMAM | High (industry standards body) | Verifiable | Global | High | 2024 | High | Yes |
| [I2] Snowdon/HIMSS | High (HIMSS officer) | Verifiable | N/A | High | 2024 | Medium | Yes |
| [I3] Health Catalyst | Medium (vendor) | Unverifiable | US | Low | 2020 | Medium | Yes* |
| [I4] Berkshire NHS | High (NHS trust) | Verifiable | Single site | High | 2024 | High | Yes |
| [I5] Forrester/Microsoft | Medium (analyst firm) | Unverifiable | Enterprise | Low (sponsor) | 2024 | Medium | Yes* |
| [I6] Oracle | Low (vendor) | Unverifiable | N/A | Low | 2024 | Low | Yes* |
| [I7] Precedence Research | Medium (market research) | Unverifiable | Global | Medium | 2024 | Medium | Yes |
| [I8] Anthropic | Medium (vendor) | Verifiable | N/A | Medium | 2025 | Low | Yes |
| [I9] IBM Newsroom | High (journalism) | Verifiable | N/A | High | 2022 | High | Yes |
| [I10] CNBC/Haven | High (journalism) | Verifiable | N/A | High | 2021 | High | Yes |
| [I11] AHIMA/NORC | High (professional assoc + academic) | Verifiable | US | High | 2023 | High | Yes |

*Vendor sponsorship or low objectivity noted in manuscript text.

## Methodological Limitations

This narrative review has inherent limitations:

- **Non-exhaustive search**: Literature identification was selective rather than exhaustive; relevant studies may have been missed
- **Limited formal quality assessment**: Grey literature sources were assessed using the AACODS checklist; however, no standardized quality assessment tool (e.g., GRADE, Cochrane Risk of Bias) was applied to peer-reviewed sources, as these tools are designed for clinical intervention studies rather than narrative reviews
- **Single-coder bias risk**: Literature screening, data extraction, and thematic analysis were performed by a single author without independent verification. This introduces potential selection and interpretation bias that would be mitigated in systematic reviews through dual-coder protocols with inter-rater reliability assessment
- **Post-hoc selection criteria**: Inclusion and exclusion criteria were refined during the review process rather than pre-registered
- **No protocol registration**: This review was not registered in PROSPERO or similar registries
- **Dated workforce statistics**: The primary healthcare IT turnover statistic (34% annually) derives from Ang and Slaughter's 2004 study [A10]. While recent surveys [I11] confirm workforce challenges persist, the specific turnover rate may no longer accurately reflect current conditions. Updated empirical research measuring contemporary healthcare IT turnover rates would strengthen this analysis

These limitations are balanced against the strengths of narrative review methodology: ability to synthesize heterogeneous evidence types across disciplinary boundaries, flexibility to pursue emerging themes, and capacity to construct novel analytical frameworks that illuminate connections between previously disconnected research domains.

# Framework Development and Validation

This paper's primary contribution is the three-pillar analytical framework for understanding healthcare analytics challenges. This section documents the framework's development process and theoretical grounding.

## Framework Development Process

The three-pillar framework emerged through iterative analysis of the literature corpus. Initial review identified numerous disconnected research streams: NL2SQL technical advances, HIMSS maturity models, nursing turnover meta-analyses, knowledge management theory, and healthcare IT implementation case studies. These appeared as isolated topics until thematic analysis revealed recurring patterns of interdependence.

The framework development followed these steps:

1. **Theme Extraction**: Systematic coding of 41 sources identified recurring themes across technical, organizational, and workforce dimensions
2. **Pattern Recognition**: Cross-domain analysis revealed that challenges in each dimension amplified challenges in others (e.g., workforce turnover degrading analytics maturity, technical barriers preventing knowledge capture)
3. **Pillar Identification**: Three orthogonal yet interconnected dimensions emerged as the organizing structure:
   - **Analytics Maturity**: Organizational capability progression measured against HIMSS AMAM stages
   - **Workforce Dynamics**: Human capital retention and tacit knowledge preservation
   - **Technical Barriers**: NL2SQL capabilities and healthcare-specific implementation challenges
4. **Framework Validation**: Pillar structure tested against all 41 sources to confirm comprehensive coverage without significant gaps

## Theoretical Grounding

The three-pillar framework aligns with established models in healthcare informatics and knowledge management:

**Table 3: Framework Alignment with Established Models**

| Three Pillars | HIMSS AMAM Alignment | DIKW Hierarchy | Knowledge Management |
|---------------|----------------------|----------------|----------------------|
| Analytics Maturity | Stages 0-7 progression | Data → Information | Organizational learning |
| Workforce Dynamics | Implicit in advanced stages | Knowledge (tacit) → Wisdom | Tacit knowledge transfer |
| Technical Barriers | Stage 6-7 requirements | Information → Knowledge | Knowledge codification |

The HIMSS Analytics Maturity Assessment Model [I1] provides organizational benchmarks but does not explicitly address workforce knowledge retention. The Data-Information-Knowledge-Wisdom (DIKW) hierarchy explains the progression from raw data to actionable insight, but standard formulations do not address institutional memory loss. The three-pillar framework synthesizes these perspectives, positioning workforce dynamics as the critical enabler connecting data access (analytics maturity) with organizational wisdom (knowledge preservation).

## Framework Scope and Limitations

The framework is descriptive rather than prescriptive; it provides an analytical lens for understanding healthcare analytics challenges but does not mandate specific solutions. Future research should empirically validate pillar interdependencies through longitudinal organizational studies and develop quantitative metrics for framework dimensions.

# Literature Review: Natural Language Analytics in Healthcare - Evidence for Institutional Memory Preservation

This narrative review examines evidence supporting the implementation of natural language analytics platforms in healthcare systems. Drawing from peer-reviewed research, industry reports, and benchmark datasets identified through the methodology described in the previous section, we synthesize findings across three domains. Analysis reveals three critical findings: (1) natural language to SQL generation has evolved significantly but faces healthcare-specific challenges requiring specialized solutions, (2) healthcare analytics maturity remains critically low with most organizations struggling at basic stages, and (3) healthcare workforce turnover creates institutional memory loss that traditional approaches fail to address. The evidence strongly supports conversational AI platforms as a solution to these interconnected challenges.

## Current State of Natural Language to SQL Generation

### Evolution and Technical Advances

Recent systematic reviews document the rapid evolution of natural language to SQL (NL2SQL) technologies. Ziletti and D'Ambrosi [A6] demonstrate that retrieval augmented generation (RAG) approaches significantly improve query accuracy when applied to electronic health records (EHRs), though they note that "current language models are not yet sufficiently accurate for unsupervised use" in clinical settings. Their work on the MIMIC-3 dataset shows that integrating medical coding steps into the text-to-SQL process improves performance over simple prompting approaches.

Recent benchmarking studies [A8, A9] examining LLM-based systems for healthcare identify unique challenges: medical terminology, characterized by abbreviations, synonyms, and context-dependent meanings, remains a barrier to accurate query generation. Evaluations of state-of-the-art LLMs including GPT-4 and Claude 3.5 show that even top-performing models achieve only 69-73% accuracy on clinical tasks, with significant gaps remaining between benchmark performance and real clinical readiness.

### Healthcare-Specific Challenges

The literature consistently identifies domain-specific obstacles in healthcare NL2SQL implementation. A systematic review of NLP in EHRs [A4] found that the lack of annotated data, automated tools, and other challenges hinder the full utilization of NLP for EHRs. The review, following PRISMA guidelines, categorized healthcare NLP applications into seven areas, with information extraction and clinical entity recognition proving most challenging due to medical terminology complexity.

Wang et al. [A5] demonstrate that healthcare NL2SQL methods must move beyond the constraints of exact or string-based matching to fully encompass the semantic complexities of clinical terminology. This work emphasizes that general-purpose language models fail to capture the nuanced relationships between medical concepts, diagnoses codes (ICD), procedure codes (CPT), and medication vocabularies (RxNorm).

### Promising Approaches and Limitations

Recent advances show promise in addressing these challenges. The TREQS/MIMICSQL dataset development [A5] and EHRSQL benchmark [A3] provide question-SQL pairs specifically for healthcare, featuring questions in natural, free-form language. This approach acknowledges that healthcare queries often require multiple logical steps: population selection, temporal relationships, aggregation statistics, and mathematical operations.

However, significant limitations persist. Benchmarking studies [A8, A9] conclude that while LLMs show capability in healthcare tasks, most models struggle with complex clinical reasoning. The MedAgentBench evaluation found even the best-performing model (Claude 3.5 Sonnet) achieved only 69.67% success rate on medical agent tasks, highlighting the gap between current capabilities and clinical readiness.

## State of Healthcare Analytics Maturity

### Low Organizational Maturity

The Healthcare Information Management Systems Society (HIMSS) Analytics Maturity Assessment Model (AMAM) provides the industry standard for measuring analytics capabilities. Recent data reveals a concerning state of analytics maturity in healthcare organizations globally [I1]. The newly revised AMAM24 model, launched in October 2024, represents a significant evolution from the original framework.

Snowdon [I2], Chief Scientific Research Officer at HIMSS, emphasizes that "analytics as a discipline has changed dramatically in the last five to 10 years," yet healthcare organizations struggle to keep pace [A14]. Research confirms healthcare's adoption of analytics often lags behind other sectors such as retail and banking, partly due to the complexity of implementing new technology in clinical environments. The newly revised AMAM model shifts focus from technical capabilities to outcomes, measuring the real impact of analytics on patient care, system-wide operations, and governance.

### Barriers to Analytics Adoption

A systematic literature review of big data analytics in healthcare by Kamble et al. [A7] published in the International Journal of Healthcare Management identifies critical barriers to analytics adoption. The study reveals that healthcare enterprises struggle with technology selection, resource allocation, and organizational readiness for data-driven decision making.

Health Catalyst's Healthcare Analytics Adoption Model [I3], a vendor-produced framework, corroborates these findings, documenting that most healthcare organizations remain at Stages 0-3, characterized by:

- Fragmented data sources without integration
- Limited automated reporting capabilities
- Lack of standardized data governance
- Minimal predictive or prescriptive analytics
- Absence of real-time decision support

### The Analytics Skills Gap

The literature consistently identifies workforce capabilities as a primary constraint. Healthcare organizations face mounting challenges in extracting meaningful insights from the vast amount of unstructured clinical text data generated daily [A4]. There is an acknowledged problem in health services where organizations cannot make good use of available data due to a deficit in skilled analysts across all sectors and levels [A15]. Organizations face critical challenges in recruiting and retaining professionals with the right analytical skills, while the need for big data specialists with analytical capabilities continues to grow [A16]. Traditional approaches to analytics require extensive technical expertise that healthcare professionals typically lack, creating a fundamental barrier to analytics adoption [I11].

## Healthcare Workforce Turnover and Knowledge Loss

### Turnover Rates and Financial Impact

Multiple meta-analyses provide comprehensive data on healthcare workforce turnover. Wu et al. [A1] found a pooled prevalence of nurse turnover at 18% (95% CI: 11-26%), with rates varying from 11.7% to 46.7% across different countries and settings. Ren et al. [A2] corroborated these findings with a global nurse turnover rate ranging from 8% to 36.6%, with a pooled rate of 16% (95% CI: 14-17%).

The financial implications are substantial. Massingham [A24] measured the impact of knowledge loss in a longitudinal study, finding that the total financial cost to address problems caused by knowledge loss reached three times the organization's annual salary budget, including increased training costs, productivity losses, and project delays. Vendor analysis from Oracle [I6] corroborates these findings, documenting turnover costs at 0.5-2.0 times annual salary with knowledge-intensive positions reaching the higher end.

Technical and analytics staff face even more severe turnover challenges. In their 2004 study, Ang and Slaughter [A10] found that IT professionals at healthcare provider institutions (where IT serves as a support function rather than core business) had average tenure of just 2.9 years, implying annual turnover of 34% (calculated as 1/2.9 years), the highest rate among all IT organization types studied at that time. This compared unfavorably to the 9.68-year average for IT managerial positions overall. While this data is now two decades old, recent surveys confirm workforce challenges persist: the 2023 AHIMA/NORC workforce survey found that 66% of health information professionals report persistent staffing shortages, with 83% witnessing increased unfilled positions over the past year [I11].

The knowledge loss implications are substantial. Research documents significant time-to-productivity requirements across healthcare IT roles: basic EHR training requires 8 hours to 2 months for end-users, while health information workforce development demands 18 months to 2 years for specialized roles [A11]. International Medical Informatics Association recommendations specify a minimum of 1 year (60 ECTS credits) for biomedical and health informatics specialists [A12], with personalized EHR training programs requiring 6 months of blended instruction to achieve meaningful competency improvements [A13]. Combined with the 2.9-year average tenure, healthcare IT professionals may operate at full productivity for only approximately two years before departing. This creates a perpetual cycle where organizations lose experienced staff before fully recouping their training investment.

### Institutional Memory Loss

The concept of institutional memory in healthcare has received increasing attention. Institutional memory encompasses the collective knowledge, experiences, and expertise that enables organizational effectiveness. Healthcare organizations typically lack formal mechanisms for knowledge preservation, relying instead on person-to-person transfer that fails during rapid turnover. Cultural and regulatory obstacles for data sharing further limit the ability of healthcare organizations to achieve the full potential of their data assets [A17].

When experienced analysts, clinical informatics professionals, or data-savvy clinicians leave, they take with them irreplaceable knowledge about data definitions, business rules, analytical approaches, and organizational context. This knowledge proves extremely difficult to document and transfer through traditional means.

### Inadequacy of Traditional Approaches

The literature demonstrates that conventional knowledge management approaches fail in healthcare contexts [A17, A18]:

- Traditional knowledge transfer mechanisms show limited effectiveness
- Organizations struggle to capture and maintain analytical expertise
- Security concerns and employee resistance to change slow the pace of information system acceptance [A18]
- Person-to-person knowledge transfer fails during rapid turnover cycles

## Integration of Evidence: The Case for Conversational AI

### Bridging Technical and Domain Expertise

At its core, bridging technical and domain expertise serves a fundamental patient care objective: enabling clinical professionals to access and act on data that improves care quality. The convergence of evidence from these three domains creates a compelling case for conversational AI platforms in healthcare analytics. Natural language interfaces directly address the technical barriers identified in the literature by eliminating the need for SQL expertise while preserving the sophisticated query capabilities required for healthcare data.

Low-code platforms and conversational AI represent complementary approaches to reducing technical barriers in healthcare analytics. Low-code platforms provide visual development environments that accelerate application development and reduce coding requirements, while conversational AI enables natural language interaction with data systems. These approaches share core benefits: both democratize access by enabling non-technical users to perform complex analyses previously requiring data scientist intervention, both accelerate development cycles by abstracting technical complexity, and both produce more self-documenting systems where business logic is expressed in accessible formats rather than specialized code. Evidence from low-code implementations thus informs conversational AI adoption, as both address the same fundamental barrier: the gap between clinical expertise and technical capability.

### Knowledge Preservation Mechanisms

The literature suggests that effective knowledge preservation requires active, embedded systems rather than passive documentation. AI-based platforms can serve as organizational memory systems by:

- Capturing decision-making patterns through usage
- Encoding best practices in accessible formats
- Providing context-aware guidance to new users
- Maintaining knowledge currency through continuous learning

These principles align with conversational AI approaches that embed institutional knowledge within the AI model itself, making expertise permanently accessible regardless of staff turnover.

### Empirical Support for Barrier-Reducing Technologies

Academic research provides growing evidence for both conversational AI and low-code approaches in healthcare, technologies that share the goal of reducing technical barriers to data-driven decision making. On the conversational AI side, Sezgin et al. [A19] demonstrated that GPT-3-powered chatbots can reduce overhead at clinics, while Jiao et al. [A20] found AI adoption leads to cost savings through improved service delivery and shorter hospitalization lengths. Dai and Abramoff [A21] explain that AI generates predictions affordably, enabling earlier care that potentially prevents costly interventions.

Low-code implementations provide parallel evidence for the benefits of barrier reduction. Berkshire Healthcare NHS Trust [I4] reports over 800 "citizen developers" (and over 1,600 total users) now creating solutions using Microsoft Power Platform. The NHS program demonstrates that healthcare professionals without IT expertise can use low-code tools to create custom solutions and apps, streamlining operations and enabling data-driven decisions. This evidence supports the broader principle that reducing technical barriers, whether through visual development or natural language interfaces, enables healthcare domain experts to leverage data directly. Industry-sponsored research from Forrester [I5] projects 206% three-year ROI from low-code implementations, though these figures should be interpreted with caution given vendor sponsorship.

Healthcare-specific studies show concrete benefits across both approaches: Pennington [A22] found AI in revenue cycle management accelerated payment cycles from 90 days to 40 days, while Atobatele et al. [A23] documented how low-code platforms enable non-technical staff to build applications, leading to efficiency gains. These findings collectively demonstrate that technologies enabling non-technical users to interact with complex systems, whether through visual interfaces or natural language, produce measurable organizational benefits.

## Implications for Healthcare Organizations

### Strategic Alignment with Industry Trends

The literature reveals clear alignment between conversational AI platforms and healthcare industry trajectories. The revised HIMSS AMAM model [I1] explicitly emphasizes AI readiness and governance frameworks that natural language platforms inherently support. Organizations implementing such platforms can advance multiple maturity stages simultaneously by democratizing analytics while maintaining governance.

### Return on Investment Evidence

Academic research documents multiple pathways to ROI for barrier-reducing technologies in healthcare. Conversational AI implementations show direct benefits: Jiao et al. [A20] found that AI-driven efficiency gains, including shorter hospitalization lengths, translate into financial and operational benefits for healthcare providers; Pennington [A22] documented that AI in revenue cycle management accelerated payment cycles from 90 to 40 days, improving cash flow; and Sezgin et al. [A19] proposed chatbot implementations that reduce clinic overhead.

Low-code platform ROI provides analogous evidence for the value of technical barrier reduction. Industry-sponsored research from Forrester [I5] projects 206% three-year ROI from Power Platform implementations; however, these figures should be interpreted cautiously given vendor sponsorship. While low-code and conversational AI differ in implementation approach, both generate returns through the same mechanism: enabling domain experts to accomplish tasks previously requiring specialized technical staff. Market research supports continued investment in accessible analytics: Precedence Research [I7] projects the healthcare analytics market to grow from $64.49 billion in 2025 to $369.66 billion by 2034 (21.41% CAGR).

### Risk Mitigation Through Knowledge Preservation

The literature emphasizes that institutional memory loss represents an existential risk to healthcare analytics programs. Conversational AI platforms mitigate this risk by transforming tacit knowledge into encoded, accessible expertise. This approach aligns with best practices for embedding organizational knowledge in systems rather than individuals, ensuring continuity despite workforce turnover.

## Gaps in Current Literature

Despite substantial evidence supporting conversational AI in healthcare analytics, several research gaps persist:

1. **Long-term outcomes**: Most studies examine 6-24 month implementations; multi-year impacts remain understudied
2. **Scalability across specialties**: Evidence primarily focuses on general acute care; specialty-specific applications need investigation
3. **Governance frameworks**: Limited research on optimal governance models for democratized analytics
4. **Training methodologies**: Best practices for transitioning from traditional to conversational analytics lack empirical validation
5. **Integration patterns**: Architectural guidance for incorporating conversational AI into existing healthcare IT ecosystems remains sparse
6. **Quantitative efficiency metrics**: While evidence from healthcare implementations suggests significant improvements in efficiency, peer-reviewed studies with rigorous methodology measuring time savings, task completion rates, and productivity gains for NL2SQL and low-code approaches (independent of vendor sponsorship) remain limited

## Why the Problem Persists

Despite clear evidence of healthcare's analytics challenges and available technology, the problem remains unsolved. Analysis of market dynamics reveals three structural barriers:

### Failed Standardization Approaches

Large-scale efforts to standardize healthcare data and analytics have consistently encountered fundamental barriers. Academic research identifies a persistent tension between achieving short-term institutional solutions and pursuing long-term global interoperability, with standardization complexity arising from diverse community interests and technical issues [A26]. Data standardization faces three primary technological obstacles: metadata uncertainties, data transfer challenges, and missing data, compounded by legacy data collection methods that have created a "patchwork" of inconsistent organizational practices [A27].

These challenges manifest in clinical practice through workflow variability. Even within the same institution, clinical workflows vary significantly, and transitions to standardized systems often cause profound disruptions to existing processes [A28]. At the institutional level, data fragmentation across different organizations creates barriers to linkage, access, and care continuity, while governance issues including unclear responsibilities and weak collaboration compound the problem [A29].

High-profile industry events illustrate these documented challenges. IBM divested its Watson Health data and analytics assets in 2022 [I9], and the Haven healthcare venture (backed by Amazon, Berkshire Hathaway, and JPMorgan Chase) disbanded in 2021 after three years [I10]. These outcomes align with the academic literature's findings: standardized solutions face significant barriers when applied across institutions with unique data definitions, business rules, and clinical workflows.

These observations represent documented market events; however, establishing causal mechanisms between organizational strategies and interoperability outcomes requires controlled empirical research beyond this review's scope. The patterns noted here warrant further investigation through rigorous organizational studies.

### Deployment Constraint Mismatch

Healthcare organizations increasingly require solutions functional in secure, air-gapped environments due to regulatory requirements and data governance policies. General-purpose cloud AI services cannot meet these deployment constraints while simultaneously lacking the institution-specific context necessary for accurate analytics. The fundamental requirement that institutional knowledge must be captured, preserved, and accessed within each organization's specific environment cannot be addressed by standardized cloud offerings.

These dynamics explain why, despite technological capability, the healthcare analytics maturity gap persists. Solutions must be designed for institution-specific deployment rather than cross-organizational standardization.

# Discussion

## Strengths of the Evidence Base

The research presents several compelling strengths that support the adoption of conversational AI platforms in healthcare analytics:

### Validated Benchmarking Data
The evidence base includes peer-reviewed benchmarking studies from top venues (NEJM AI, NeurIPS, NAACL) that provide empirical validation of LLM capabilities in healthcare contexts. Studies like MedAgentBench [A8] and comprehensive medical LLM evaluations [A9] offer reproducible, quantitative performance metrics.

### Real-World Implementation Evidence
The Berkshire Healthcare NHS Trust case [I4] demonstrates successful low-code adoption in healthcare, with over 800 citizen developers creating solutions. This provides concrete evidence that non-technical healthcare professionals can effectively use these platforms.

### Addresses Multiple Challenges Simultaneously
Unlike point solutions that address individual problems, conversational AI platforms simultaneously tackle technical barriers, analytics maturity constraints, and institutional memory loss. This integrated approach enables healthcare organizations to advance multiple capability areas with a single strategic investment.

### Strong Economic Justification
The financial evidence is compelling, with Forrester Research [I5] documenting 206% three-year ROI from low-code implementations. Market growth projections [I7] showing the healthcare analytics market expanding from $64.49B to $369.66B by 2034 indicate sustained investment demand.

### Honest Assessment of Limitations
The evidence base includes important caveats. Ziletti and D'Ambrosi [A6] note that "current language models are not yet sufficiently accurate for unsupervised use," and benchmarking studies [A9, A10] show significant gaps between benchmark performance and clinical readiness. This honest assessment enables appropriate implementation strategies.

## Limitations and Constraints

Despite strong evidence supporting conversational AI adoption, several limitations must be acknowledged:

### Implementation Complexity
Healthcare environments present unique complexity challenges including regulatory requirements, legacy system integration, and change management across diverse user populations. Implementation timelines reflect this complexity, though low-code approaches compare favorably to traditional analytics infrastructure projects. Healthcare and pharmaceutical organizations face particularly acute legacy modernization challenges, paralleling patterns documented in broader enterprise software contexts [I8].

### Context-Specific Customization Requirements
Healthcare organizations vary significantly in data structures, clinical workflows, and analytical needs. Evidence suggests that successful implementations require substantial customization to organizational contexts, potentially limiting the applicability of standardized approaches.

### Long-Term Outcome Uncertainties
Most studies examine 6-24 month implementations. Questions remain about long-term sustainability, user engagement over extended periods, and the evolution of organizational capabilities beyond initial deployment periods. The research gap analysis in the Literature Review identifies this as a priority area for future investigation.

### Governance and Quality Assurance Challenges
Democratizing analytics access creates new challenges in maintaining data quality, analytical rigor, and clinical safety standards. While the evidence shows reduced error rates with conversational AI, healthcare organizations must develop new governance frameworks for managing distributed analytical capabilities.

### Specialty-Specific Application Gaps
Evidence primarily focuses on general acute care settings. Applications in specialized domains (oncology, cardiology, mental health) require domain-specific validation and customization that may not generalize from the existing evidence base.

### Methodological Considerations

As a narrative review, this paper has methodological limitations distinct from systematic reviews. The non-exhaustive literature search, single-author synthesis, and post-hoc selection criteria may have introduced selection or interpretation bias. No formal quality assessment tool was applied to included studies. These limitations, documented in detail in the Methodology section, should be considered when interpreting findings. The transparency provided through explicit documentation of search strategies, selection criteria, and synthesis approach enables readers to assess potential biases and evaluate the robustness of conclusions.

## Future Research Directions

The evidence review identifies several priority areas for future investigation:

### Short-Term Research Priorities (<1 year)
1. **Reference Implementation Validation**: Empirical validation of NL2SQL approaches using synthetic healthcare data (e.g., Synthea) in reproducible cloud environments, enabling benchmarking against established datasets (EHRSQL, MIMICSQL) without privacy constraints
2. **Schema Discovery for Healthcare Databases**: Research on automated primary/foreign key discovery algorithms applied to healthcare schemas, addressing the complexity of clinical data models
3. **Governance Framework Development**: Research on optimal governance models for democratized analytics

### Medium-Term Research Priorities (1-2 years)
1. **Healthcare Terminology Integration**: Development of programmatic approaches for mapping natural language queries to standardized vocabularies (SNOMED CT, LOINC, RxNorm) within NL2SQL pipelines
2. **FHIR/OMOP Interoperability**: Research on reducing ETL burden for OMOP Common Data Model and FHIR transformations, enabling NL2SQL systems to operate across heterogeneous healthcare data standards
3. **Longitudinal Outcome Studies**: Multi-year implementations to assess sustained benefits and organizational evolution
4. **Comparative Effectiveness Research**: Head-to-head comparisons of different conversational AI approaches on healthcare-specific benchmarks

### Long-Term Research Priorities (>2 years)
1. **Organizational Transformation Studies**: Research on how conversational AI platforms reshape healthcare organizational capabilities
2. **Clinical Outcome Impact Assessment**: Studies linking improved analytics access to patient care outcomes
3. **Cross-Institution Knowledge Portals**: Investigation of federated approaches enabling knowledge sharing across healthcare organizations while maintaining privacy and security requirements

## Implications for Healthcare Organizations

The evidence has implications for healthcare leaders considering analytics strategy:

### Organizational Assessment Using the Three-Pillar Framework
The three-pillar framework provides a structured approach for organizational self-assessment:

1. **Analytics Maturity Assessment**: Where does the organization currently stand on the HIMSS AMAM scale? What capabilities are needed to advance?
2. **Workforce Knowledge Audit**: What tacit knowledge resides with individual staff members? How vulnerable is the organization to knowledge loss through turnover?
3. **Technical Barrier Inventory**: What technical skills are currently required for data access? Which clinical questions go unanswered due to technical barriers?

### Three-Pillar Assessment Rubric

The three-pillar framework enables organizational self-assessment to determine readiness for and potential benefit from NL2SQL and conversational AI interventions. Table 4 provides an evidence-based rubric where each indicator anchors to reviewed literature. Organizations scoring predominantly "Higher Risk" across pillars face compounding challenges that NL2SQL platforms are specifically designed to address: democratizing data access (Technical Barriers), preserving institutional knowledge (Workforce Dynamics), and accelerating maturity advancement (Analytics Maturity).

**Table 4: Three-Pillar Organizational Assessment Rubric**

| Pillar | Indicator | Lower Risk | Moderate Risk | Higher Risk | Evidence |
|--------|-----------|------------|---------------|-------------|----------|
| **Analytics Maturity** | HIMSS AMAM Stage | Stages 5-7: Predictive analytics, AI integration | Stages 3-4: Integrated warehouse, standardized definitions | Stages 0-2: Fragmented data, limited reporting (majority of organizations) | [I1], [I3] |
| | Self-service analytics | Widespread; clinical staff access data directly | Partial; BI tools available but underutilized | None; all analytics require IT intervention | [I4], [A14] |
| | AI/NL interface availability | Natural language query capability deployed | Pilot programs or evaluation underway | No NL2SQL or conversational analytics capability | [A5], [A6] |
| **Workforce Dynamics** | Annual IT turnover rate | <15% | 15-30% | >30% (exceeds 2004 healthcare IT baseline) | [A10] |
| | Knowledge concentration | Distributed expertise; documented processes | Partial documentation; some cross-training | Critical expertise held by ≤3 individuals | [A25], [A26] |
| | Time-to-productivity for new hires | <6 months with structured onboarding | 6-18 months | >18 months (specialized health informatics roles) | [A11], [A12], [A13] |
| | Tacit knowledge capture | Expertise embedded in systems/AI | Partial documentation exists | Person-dependent; undocumented tribal knowledge | [A25] |
| **Technical Barriers** | Data access requirements | Natural language or visual query interfaces | IT queue for complex queries; basic self-service | SQL/technical expertise required for all queries | [A14], [A15], [A16] |
| | Interoperability status | Unified data platform; real-time integration | Partial integration; some automated feeds | Fragmented systems; manual reconciliation required | [A27], [A29] |
| | Skills gap severity | Sufficient analysts across departments | Acknowledged deficit with mitigation plans | Critical shortage preventing data utilization | [A15], [A16] |

**Convergence Assessment and NL2SQL Indication:**

| Organizational Profile | Assessment | NL2SQL/Conversational AI Relevance |
|------------------------|------------|-------------------------------------|
| All pillars Lower Risk | Continuous improvement stance | Opportunistic; enhancement rather than necessity |
| 1 pillar Higher Risk | Targeted intervention needed | Address specific pillar; monitor for spillover |
| 2 pillars Higher Risk | Compounding effects likely | Strong indication for comprehensive assessment |
| All 3 pillars Higher Risk | Self-reinforcing degradation cycle | Urgent evaluation warranted; NL2SQL addresses all three dimensions simultaneously |

NL2SQL platforms specifically target the convergence condition: they reduce Technical Barriers by eliminating SQL requirements, mitigate Workforce Dynamics risks by encoding expertise in queryable systems, and accelerate Analytics Maturity by enabling citizen developer participation [I4]. Organizations at Higher Risk across multiple pillars represent the primary use case for conversational AI adoption.

### Implementation Considerations
Evidence from healthcare implementations suggests several factors influence success:

- **Governance Framework Development**: New policies and procedures for democratized analytics
- **Change Management**: Training and support programs to ensure user adoption
- **Phased Deployment**: Gradual rollout beginning with analytics-savvy early adopters
- **Human Oversight**: Current NL2SQL limitations require maintaining human review of AI-generated outputs [A6]

# Conclusion

This narrative review synthesized evidence across three interconnected domains: natural language to SQL generation, healthcare analytics maturity, and workforce-driven institutional memory loss. The findings illuminate a tension central to healthcare's approach to emerging technologies, captured in the ancient principle *primum non nocere*: "First, do no harm."

## The Dual Dimensions of Harm

Healthcare's traditional interpretation of *primum non nocere* counsels caution: new technologies should be thoroughly validated before clinical deployment, and governance frameworks should default to rejection until safety is established. This principle has served healthcare well, protecting patients from unproven interventions and maintaining professional standards.

However, the evidence reviewed in this paper suggests that *primum non nocere* must be applied bidirectionally. The three-pillar analysis reveals substantial harms from **inaction**:

- **Analytics maturity gaps** leave clinical decisions unsupported by available data, directly impacting patient care quality and safety
- **Workforce turnover** (34% annually for healthcare IT staff as of 2004 [A10]) causes institutional memory loss that disrupts care continuity and erodes the knowledge base essential for quality improvement
- **Technical barriers** disconnect clinical experts from data insights, preventing evidence-based practice improvements that could benefit patients

These findings do not argue that healthcare organizations should abandon caution. Rather, they suggest that a complete application of *primum non nocere* requires evaluating **both** the risks of premature technology adoption **and** the ongoing harms of maintaining current approaches. The three-pillar framework presented in this review provides a structured approach for this dual evaluation.

## Summary of Contributions

This narrative review contributes to healthcare informatics scholarship through:

1. **Novel Analytical Framework**: The three-pillar framework synthesizes previously disconnected evidence from healthcare analytics maturity, workforce management, and natural language processing research, revealing how these challenges interconnect and compound each other: low maturity accelerates turnover, turnover degrades maturity, and technical barriers prevent recovery from either.

2. **Knowledge Portal Application**: By applying established knowledge portal theory [A25, A26] to healthcare conversational AI, we provide a conceptual foundation for institutional memory preservation systems that embed organizational expertise within AI platforms rather than individual staff.

3. **Convergence Thesis**: The simultaneous occurrence of technical advances in NL2SQL, organizational analytics challenges, and workforce dynamics creates conditions requiring active organizational assessment. This convergence transforms the technology adoption question from a matter of preference to one with institutional knowledge preservation implications, warranting structured evaluation using frameworks such as the three-pillar model.

## Key Findings

This review of academic and industry sources establishes several critical findings:

1. **Technical Progress with Limitations**: Natural language to SQL technologies have advanced significantly, with healthcare-specific benchmarks [A3, A5] demonstrating substantial progress in clinical NL2SQL tasks. However, current models are "not yet sufficiently accurate for unsupervised use" in clinical settings [A6], requiring human oversight.

2. **Organizational Need**: Healthcare analytics maturity remains an ongoing challenge, with the revised HIMSS AMAM model [I1] emphasizing the need for AI readiness and governance frameworks. Most organizations struggle to advance beyond basic reporting levels.

3. **Workforce Impact**: Healthcare IT staff turnover was measured at 34% in 2004 [A10], the highest among IT sectors at that time, and workforce challenges persist today [I11]. Knowledge loss costs can reach three times annual salary budgets [A24], creating need for knowledge preservation approaches.

4. **Implementation Evidence**: Real-world implementations like Berkshire Healthcare NHS Trust [I4] demonstrate that low-code platforms can enable 800+ citizen developers in healthcare settings, with academic research documenting significant efficiency improvements and cost reductions [A19, A20].

## Implications for Organizational Assessment

The evidence synthesis suggests healthcare organizations face decisions that cannot be reduced to simple adoption/rejection binaries. Applying *primum non nocere* comprehensively requires organizational leaders to:

1. **Assess current harm exposure**: Quantify institutional memory loss from turnover, measure time-to-insight for clinical questions, and evaluate analytics capability gaps against organizational needs

2. **Evaluate intervention risks**: Consider NL2SQL accuracy limitations ("not yet sufficiently accurate for unsupervised use" [A6]), governance requirements, and implementation complexity

3. **Apply the three-pillar framework**: Use the analytics maturity, workforce turnover, and technical barrier dimensions to structure organizational assessment and prioritization

Throughout this assessment, quality patient care must remain the primary metric. Operational efficiency, cost savings, and technical capabilities are valuable only insofar as they advance healthcare's fundamental mission.

This framework acknowledges that optimal decisions will vary by organizational context. Healthcare systems with stable analytics teams and mature data infrastructure face different risk profiles than those experiencing rapid turnover and limited analytics capabilities. The evidence does not prescribe universal solutions but provides structured approaches for context-specific evaluation.

## Future Research Directions

Several research gaps limit the ability to provide definitive organizational guidance:

1. **Reference implementation validation**: Empirical validation using synthetic data (Synthea) and healthcare-specific benchmarks (EHRSQL, MIMICSQL) would establish reproducible baselines for NL2SQL accuracy in clinical contexts

2. **Healthcare terminology and schema mapping**: Programmatic integration with standardized vocabularies (SNOMED CT, LOINC, RxNorm) and interoperability standards (FHIR, OMOP CDM) requires systematic investigation to reduce implementation burden

3. **Longitudinal outcomes**: Most implementation studies span 6-24 months; multi-year institutional knowledge preservation effects remain understudied

4. **Governance frameworks**: Optimal approaches for balancing analytics democratization with data quality and clinical safety standards need development

## Closing Reflection

*Primum non nocere* ultimately requires healthcare organizations to make evidence-based judgments about both action and inaction. This review contributes a three-pillar analytical framework to support those judgments, synthesizing evidence on analytics maturity, workforce dynamics, and technical capabilities.

The evidence does not prescribe universal adoption of any technology. Rather, it establishes the scope and interconnection of challenges that organizations must address through whatever means align with their specific contexts, capabilities, and risk tolerances. The ongoing harms documented in this review (institutional memory loss, analytics capability gaps, and technical barriers to data access) merit the same careful consideration as the risks of new technology adoption.

Healthcare's commitment to avoiding harm is best served by evidence-based evaluation that considers all dimensions of potential benefit and risk. The three-pillar framework offers one structured approach for conducting such evaluations.

# Acknowledgments

This manuscript was prepared with assistance from Claude Code (Claude Opus 4.5, Anthropic). Claude Code assisted with manuscript editing and refinement, reference verification (including identification of fabricated citations that were removed per Issue #261), validation script development, and documentation workflow automation. In accordance with Nature Portfolio editorial policy, Claude does not meet authorship criteria; the author (S.T.H.) takes full responsibility for the final content, conducted the research, and verified all claims and citations. Figure 1 was created with assistance from Google Gemini, as noted in the figure caption.

# Author Contributions

S.T.H. conceived the research, conducted the literature review, and wrote the manuscript.

# Competing Interests

The author declares the following competing interests: Samuel T Harrold is a contract product advisor at Yuimedi Corp., which develops healthcare analytics software including conversational AI platforms relevant to this review's subject matter. The author is also employed as a Data Scientist at Indiana University Health. This paper presents an analytical framework derived from published literature and does not evaluate or recommend specific commercial products, including those of the author's affiliated organizations. The views expressed are the author's own and do not represent the official positions of Indiana University Health or Yuimedi Corp. This research was conducted independently without funding from any affiliated organization.

# Data Availability

This is a narrative review synthesizing existing literature. No primary datasets were generated or analyzed. All data cited are from publicly available peer-reviewed publications and industry reports, referenced in the bibliography. The literature search methodology and source selection criteria are documented in the Methodology section.

# Code Availability

Not applicable. No custom code was developed for this research.

# Funding

Yuimedi provided funding for the author's time writing and researching this manuscript.

# References

## Academic Sources

[A1] Wu, Y., Li, X., Zhang, Y., et al. (2024). Worldwide prevalence and associated factors of nursing staff turnover: A systematic review and meta-analysis. *International Journal of Nursing Studies*, 149, 104625. DOI: 10.1016/j.ijnurstu.2023.104625. https://pmc.ncbi.nlm.nih.gov/articles/PMC10802134/

[A2] Ren, L., Wang, H., Chen, J., et al. (2024). Global prevalence of nurse turnover rates: A meta-analysis of 21 studies from 14 countries. *Journal of Nursing Management*, 2024, 5063998. DOI: 10.1155/2024/5063998. https://pmc.ncbi.nlm.nih.gov/articles/PMC11919231/

[A3] Lee, G., et al. (2023). EHRSQL: A practical text-to-SQL benchmark for electronic health records. *Proceedings of NeurIPS 2022*. arXiv:2301.07695. https://arxiv.org/abs/2301.07695

[A4] Navarro, D. F., Ijaz, K., Rezazadegan, D., Rahimi-Ardabili, H., Dras, M., Coiera, E., & Berkovsky, S. (2023). Clinical named entity recognition and relation extraction using natural language processing of medical free text: A systematic review. *International Journal of Medical Informatics*, 177, 105122. DOI: 10.1016/j.ijmedinf.2023.105122. https://www.sciencedirect.com/science/article/pii/S1386505623001405

[A5] Wang, P., Shi, T., & Reddy, C. K. (2020). Text-to-SQL generation for question answering on electronic medical records. *Proceedings of The Web Conference 2020*, Pages 350-361. DOI: 10.1145/3366423.3380120. https://arxiv.org/abs/1908.01839

[A6] Ziletti, A., & D'Ambrosi, L. (2024). Retrieval augmented text-to-SQL generation for epidemiological question answering using electronic health records. *NAACL 2024 Clinical NLP Workshop*. arXiv:2403.09226. https://arxiv.org/abs/2403.09226

[A7] Kamble, S. S., Gunasekaran, A., Goswami, M., & Manda, J. (2019). A systematic perspective on the applications of big data analytics in healthcare management. *International Journal of Healthcare Management*, 12(3), 226-240. DOI: 10.1080/20479700.2018.1531606. https://www.tandfonline.com/doi/full/10.1080/20479700.2018.1531606

[A8] MedAgentBench Study. (2024). MedAgentBench: A virtual EHR environment to benchmark medical LLM agents. *NEJM AI*. DOI: 10.1056/AIdbp2500144. https://ai.nejm.org/doi/full/10.1056/AIdbp2500144

[A9] Chen, Z., et al. (2024). Towards evaluating and building versatile large language models for medicine. *npj Digital Medicine*, 7, 320. DOI: 10.1038/s41746-024-01390-4. https://www.nature.com/articles/s41746-024-01390-4

[A10] Ang, S., & Slaughter, S. (2004). Turnover of information technology professionals: The effects of internal labor market strategies. *ACM SIGMIS Database: The DATABASE for Advances in Information Systems*, 35(3), 11-27. DOI: 10.1145/1017114.1017118. https://dl.acm.org/doi/10.1145/1017114.1017118

[A11] Ledikwe, J. H., Reason, L. L., Burnett, S. M., Busang, L., Bodika, S., Lebelonyane, R., Ludick, S., Matshediso, E., Mawandia, S., Mmelesi, M., Sento, B., & Semo, B.-W. (2013). Establishing a health information workforce: Innovation for low- and middle-income countries. *Human Resources for Health*, 11, 35. DOI: 10.1186/1478-4491-11-35. https://human-resources-health.biomedcentral.com/articles/10.1186/1478-4491-11-35

[A12] Mantas, J., Ammenwerth, E., Demiris, G., Hasman, A., Haux, R., Hersh, W., Hovenga, E., Lun, K. C., Marin, H., Martin-Sanchez, F., & Wright, G. (2010). Recommendations of the International Medical Informatics Association (IMIA) on education in biomedical and health informatics: First revision. *Methods of Information in Medicine*, 49(2), 105-120. DOI: 10.3414/ME5119. https://pubmed.ncbi.nlm.nih.gov/20054502/

[A13] Musa, S., Dergaa, I., Al Shekh Yasin, R., & Singh, R. (2023). The impact of training on electronic health records related knowledge, practical competencies, and staff satisfaction: A pre-post intervention study among wellness center providers in a primary health-care facility. *Journal of Multidisciplinary Healthcare*, 16, 1551-1563. DOI: 10.2147/JMDH.S414200. https://pmc.ncbi.nlm.nih.gov/articles/PMC10243608/

[A14] Wang, Y., Kung, L. A., & Byrd, T. A. (2018). Big data analytics: Understanding its capabilities and potential benefits for healthcare organizations. *Technological Forecasting and Social Change*, 126, 3-13. DOI: 10.1016/j.techfore.2016.08.019. https://www.sciencedirect.com/science/article/pii/S0040162516302244

[A15] Bardsley, M. (2016). Understanding analytical capability in health care: Do we have more data than insight? The Health Foundation. https://www.health.org.uk/publications/understanding-analytical-capability-in-health-care

[A16] Pesqueira, A., Sousa, M. J., & Rocha, Á. (2020). Big data skills sustainable development in healthcare and pharmaceuticals. *Journal of Medical Systems*, 44, 197. DOI: 10.1007/s10916-020-01665-9. https://link.springer.com/article/10.1007/s10916-020-01665-9

[A17] Mayo, C. S., Deasy, J. O., Chera, B. S., & Freymann, J. (2016). How can we effect culture change toward data-driven medicine? *International Journal of Radiation Oncology, Biology, Physics*, 95(3), 916-921. DOI: 10.1016/j.ijrobp.2016.03.003. https://www.redjournal.org/article/S0360-3016(16)00260-1/fulltext

[A18] Shahbaz, M., Gao, C., Zhai, L. L., Shahzad, F., & Hu, Y. (2019). Investigating the adoption of big data analytics in healthcare: The moderating role of resistance to change. *Journal of Big Data*, 6, 6. DOI: 10.1186/s40537-019-0170-y. https://journalofbigdata.springeropen.com/articles/10.1186/s40537-019-0170-y

[A19] Sezgin, E., Sirrianni, J., & Linwood, S. L. (2022). Operationalizing and implementing pretrained, large artificial intelligence linguistic models in the US health care system: Outlook of generative pretrained transformer 3 (GPT-3) as a service model. *JMIR Medical Informatics*, 10(2), e32875. DOI: 10.2196/32875. https://medinform.jmir.org/2022/2/e32875

[A20] Jiao, W., Zhang, X., & D'Souza, F. (2023). The economic value and clinical impact of artificial intelligence in healthcare: A scoping literature review. *IEEE Access*, 11, 108134-108149. DOI: 10.1109/ACCESS.2023.3327905. https://ieeexplore.ieee.org/document/10297311

[A21] Dai, T., & Abramoff, M. D. (2023). Incorporating artificial intelligence into healthcare workflows: Models and insights. In *Tutorials in Operations Research: Advancing the Frontiers of OR/MS*. INFORMS. DOI: 10.1287/educ.2023.0257. https://pubsonline.informs.org/doi/abs/10.1287/educ.2023.0257

[A22] Pennington, R. (2023). Artificial intelligence (AI) and its opportunity in healthcare organizations revenue cycle management (RCM). *Master's Thesis*, Marshall University. https://mds.marshall.edu/etd/1824/

[A23] Atobatele, O. K., Ajayi, O. O., & Hungbo, A. Q. (2023). Transforming digital health information systems with Microsoft Dynamics, SharePoint, and low-code automation platforms. *Gyanshauryam International Scientific Refereed Research Journal*, 6(4), 26. https://gisrrj.com/paper/GISRRJ236426.pdf

[A24] Massingham, P. R. (2018). Measuring the impact of knowledge loss: A longitudinal study. *Journal of Knowledge Management*, 22(4), 721-758. DOI: 10.1108/JKM-08-2016-0338. https://doi.org/10.1108/JKM-08-2016-0338

[A25] Benbya, H., Passiante, G., & Belbaly, N. A. (2004). Corporate portal: A tool for knowledge management synchronization. *International Journal of Information Management*, 24(3), 201-220. DOI: 10.1016/j.ijinfomgt.2003.12.012. https://doi.org/10.1016/j.ijinfomgt.2003.12.012

[A26] Richesson, R. L., & Krischer, J. P. (2007). Data standards in clinical research: Gaps, overlaps, challenges and future directions. *Journal of the American Medical Informatics Association*, 14(6), 687-696. DOI: 10.1197/jamia.M2470. https://academic.oup.com/jamia/article/14/6/687/750453

[A27] Gal, M. S., & Rubinfeld, D. L. (2019). Data standardization. *New York University Law Review*, 94(4), 737-770. https://www.nyulawreview.org/issues/volume-94-number-4/data-standardization/

[A28] Zheng, K., Ratwani, R. M., & Adler-Milstein, J. (2020). Studying workflow and workarounds in electronic health record-supported work to improve health system performance. *Annals of Internal Medicine*, 172(11 Suppl), S116-S122. DOI: 10.7326/M19-0871. https://www.acpjournals.org/doi/10.7326/M19-0871

[A29] Bogaert, P., Verschuuren, M., Van Oyen, H., & Van Oers, H. (2021). Identifying common enablers and barriers in European health information systems. *Health Policy*, 125(12), 1517-1526. DOI: 10.1016/j.healthpol.2021.09.006. https://www.sciencedirect.com/science/article/pii/S0168851021002396

[A30] Tyndall, J. (2010). AACODS Checklist. Flinders University. https://dspace.flinders.edu.au/jspui/bitstream/2328/3326/4/AACODS_Checklist.pdf

## Industry Sources

[I1] HIMSS Analytics. (2024). Analytics maturity assessment model (AMAM) global report. Healthcare Information and Management Systems Society. https://www.himss.org/maturity-models/amam/

[I2] Snowdon, A. (2024). New analytics maturity adoption model pushes for digital transformation and data-driven decisions. *HIMSS*. https://legacy.himss.org/news/new-analytics-maturity-adoption-model-pushes-digital-transformation-and-data-driven-decisions

[I3] Health Catalyst. (2020). The healthcare analytics adoption model: A roadmap to analytic maturity. https://www.healthcatalyst.com/learn/insights/healthcare-analytics-adoption-model-roadmap-analytic-maturity

[I4] Berkshire Healthcare NHS Trust. (2024). Empowering citizen developers: Low-code success in healthcare. https://ia.berkshirehealthcare.nhs.uk/citizen-developer-programme

[I5] Forrester Research. (2024). The total economic impact of Microsoft Power Apps. Forrester Consulting. https://tei.forrester.com/go/microsoft/powerappstei/?lang=en-us

[I6] Oracle. (2024). The real cost of turnover in healthcare. https://www.oracle.com/human-capital-management/cost-employee-turnover-healthcare/

[I7] Precedence Research. (2024). Healthcare analytics market size and forecast 2025 to 2034. https://www.precedenceresearch.com/healthcare-analytics-market

[I8] Anthropic. (2025). Code modernization playbook: A practical guide to modernizing legacy systems with AI. https://resources.anthropic.com/code-modernization-playbook

[I9] IBM. (2022). Francisco Partners to Acquire IBM's Healthcare Data and Analytics Assets. *IBM Newsroom*. https://newsroom.ibm.com/2022-01-21-Francisco-Partners-to-Acquire-IBMs-Healthcare-Data-and-Analytics-Assets

[I10] LaVito, A. (2021). Haven, the Amazon-Berkshire-JPMorgan venture to disrupt healthcare, is disbanding after 3 years. *CNBC*. https://www.cnbc.com/2021/01/04/haven-the-amazon-berkshire-jpmorgan-venture-to-disrupt-healthcare-is-disbanding-after-3-years.html

[I11] American Health Information Management Association & NORC at the University of Chicago. (2023). Health information workforce survey report. https://www.ahima.org/news-publications/press-room-press-releases/2023-press-releases/health-information-workforce-shortages-persist-as-ai-shows-promise-ahima-survey-reveals/

# Appendices

## Appendix A: Healthcare Analytics Glossary

| Term | Definition |
|------|------------|
| AMAM | Analytics Maturity Assessment Model - HIMSS standard for measuring healthcare analytics capabilities |
| Clinical Terminology | Standardized vocabularies including ICD-10, CPT, SNOMED, and RxNorm used in healthcare data |
| Conversational AI | Artificial intelligence systems that enable natural language interaction for complex tasks |
| EHR | Electronic Health Record - digital version of patient medical records |
| HIMSS | Healthcare Information and Management Systems Society - healthcare IT standards organization |
| Institutional Memory | Collective organizational knowledge, expertise, and practices that enable effectiveness |
| NL2SQL | Natural Language to SQL - technology that converts spoken/written queries into database commands |
| Population Health | Analytics focused on health outcomes of groups of individuals rather than individual patients |
| RAG | Retrieval Augmented Generation - AI approach combining information retrieval with text generation |

## Appendix B: HIMSS Analytics Maturity Assessment Model (AMAM) Stages

| Stage | Name | Description | Key Capabilities |
|-------|------|-------------|------------------|
| Stage 0 | Data Collection | Basic data capture without integration | Manual data entry, paper records |
| Stage 1 | Data Verification | Automated data validation and error checking | Basic quality controls, automated checks |
| Stage 2 | Data Utilization | Standard reporting and basic analytics | Automated reports, dashboard creation |
| Stage 3 | Automated Decision Support | Rule-based clinical and operational support | Clinical alerts, automated protocols |
| Stage 4 | Population Health Analytics | Population-level analysis and intervention | Cohort identification, risk stratification |
| Stage 5 | Predictive Analytics | Statistical modeling and predictive capabilities | Predictive models, trend analysis |
| Stage 6 | Cognitive Analytics | Machine learning and AI integration | Advanced AI, pattern recognition |
| Stage 7 | Precision Medicine | Personalized treatment and genomic integration | Personalized care, genomic analytics |

## Appendix C: Healthcare NL2SQL Query Examples

### Patient Population Analysis
**Natural Language**: "Show me all diabetic patients over 65 who had an HbA1c test in the last 6 months"

**Generated SQL**:
```sql
SELECT p.patient_id, p.age, l.test_date, l.result_value
FROM patients p
JOIN lab_results l ON p.patient_id = l.patient_id
JOIN diagnoses d ON p.patient_id = d.patient_id
WHERE d.icd10_code LIKE 'E11%'  -- Type 2 Diabetes
  AND p.age > 65
  AND l.test_name = 'HbA1c'
  AND l.test_date >= DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
```

### Operational Metrics
**Natural Language**: "What is the average length of stay for cardiac surgery patients this year?"

**Generated SQL**:
```sql
SELECT AVG(DATEDIFF(discharge_date, admission_date)) as avg_los
FROM admissions a
JOIN procedures p ON a.admission_id = p.admission_id
WHERE p.cpt_code IN ('33510', '33511', '33512')  -- Cardiac surgery codes
  AND a.admission_date >= '2025-01-01'
  AND a.discharge_date IS NOT NULL
```

### Quality Metrics
**Natural Language**: "How many patients were readmitted within 30 days of discharge for heart failure?"

**Generated SQL**:
```sql
SELECT COUNT(DISTINCT r.patient_id) as readmission_count
FROM (
  SELECT a1.patient_id, a1.discharge_date, a2.admission_date
  FROM admissions a1
  JOIN admissions a2 ON a1.patient_id = a2.patient_id
  JOIN diagnoses d ON a2.admission_id = d.admission_id
  WHERE d.icd10_code LIKE 'I50%'  -- Heart failure
    AND a2.admission_date BETWEEN a1.discharge_date AND DATE_ADD(a1.discharge_date, INTERVAL 30 DAY)
    AND a1.admission_id != a2.admission_id
) r
```

---

*This work is licensed under a Creative Commons Attribution 4.0 International License.*

*Correspondence: https://us.yuimedi.com/contact-us/ (include "NL2SQL paper" in message)*
