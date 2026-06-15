# Point-by-Point Response to Editor and Reviewers

Manuscript #96541, "Healthcare Analytics Challenges: A Three-Pillar Framework Connecting Analytics Maturity, Workforce Agility, and Technical Enablement"
Interactive Journal of Medical Research (Decision D, major revision)

NOTE FOR SUBMISSION: On the i-JMR resubmission form, paste this point-by-point response into section (B) "Respond to editorial and peer review comments" (the text box that becomes the notification to the editor; the author is copied on it). Use plain text with no formatting (bold/italics). The clean revised manuscript (paper.docx, no tracked changes) is uploaded in section (A); a tracked-changes version and this response are also uploaded as additional material in section 3. In section (D), the Abstract field must be set to Unstructured and the abstract pasted as plain text (max 500 words; the manuscript abstract is 304 words); a plain-text copy is provided in 20260615_abstract-plaintext.txt. The two figures (architecture.figure.png, knowledge-cycle.figure.png) upload in section 1 as PNGs (max 1200x1200 px) and Multimedia Appendix 1 in section 2.

DO NOT SEND UNTIL THE MANUSCRIPT IS REBUILT AND VERIFIED. The responses below describe the revised source files. The editor reads the rebuilt Word document, which must match. Before sending: (1) rebuild all artifacts (paper.docx/pdf and the multimedia appendix) from source; (2) open the rebuilt paper.docx and confirm it reflects every change described here, specifically: in-text citations appear as numbered square brackets (not superscripts), Figure 1 shows the Organizational Memory to Knowledge Base feedback edge, the three Pillar items appear as subheadings, and a search for "disclosure" and "financial" finds the AI-disclosure and funding statements. Citeproc can render to DOCX differently than to LaTeX/HTML, so verify in the DOCX itself, not only in other formats.

---

We thank the editor and both reviewers for their constructive and detailed comments. The revision strengthens the manuscript's engagement with recent peer-reviewed literature, adds explicit definitions of the three core constructs, addresses the scope and human-in-the-loop efficacy concerns with empirical evidence, and brings the formatting into compliance. In total we added 14 references spanning 1994-2026. Most are recent (2016-2026); the few older entries are foundational sources for the constructs and methods cited, each paired with a recent review: for example, Breu et al. 2002 (the origin of the workforce-agility construct) with Tessarini Junior & Saltorato 2021, and Tomaskovic-Devey et al. 1994 (foundational work on organizational survey non-response) with Halbesleben & Whitman 2013. Each comment is addressed below; section names refer to the revised manuscript.

==================================================
EDITORIAL AND CONTENT COMMENTS
==================================================

COMMENT (Editor): The central argument of your viewpoint is interesting and relevant. However the manuscript could be stronger by using better examples and interacting more with relevant and recent literature.

RESPONSE: We have substantially increased engagement with recent peer-reviewed literature throughout. Specifically, we added: cited scholarly definitions of the three title constructs (Reviewer T, comment 1); empirical evidence on the accuracy of human-in-the-loop oversight of AI-generated analytics (Reviewer Q, comment 3); database query-log evidence on query reuse and diversity (Reviewer Q, comment 2); methodological literature on self-selection and non-response bias in voluntary assessments (Reviewer Q, comment 1); and contemporary (2021-2025) workforce-turnover evidence. These additions are detailed in the responses below.

==================================================
FORMATTING AND STRUCTURE COMMENTS (Editor)
==================================================

COMMENT: All in-text references must be numbers in square brackets. Do not use the author-year system, round brackets, or superscripts.

RESPONSE: Done. The in-text citation style has been changed; references are now sequentially numbered and presented in square brackets (for example, [1], [2,3]), with no superscripts, author-year, or round brackets.

COMMENT: Do not number your headings or use italics or bold for emphasis in place of subheadings. Ensure each section has more than one subheading; otherwise, remove it. All subheadings must be under Introduction, Methods, Results, and Discussion.

RESPONSE: We have addressed each element:
- No headings are numbered.
- No section has exactly one subheading; each section has either no subheadings or two or more.
- The three short italic titles that previously labeled the sub-tables of the assessment rubric (Pillar 1, Pillar 2, Pillar 3) have been converted to proper descriptive subheadings, so italics are no longer used in place of subheadings. Remaining italics denote defined terms and list labels (emphasis), consistent with journal style.
- Regarding the requirement that all subheadings fall under Introduction, Methods, Results, and Discussion: this manuscript is a Viewpoint, and JMIR's own article-type instructions specify a different structure for Viewpoints than for Original Papers. Per "What are the article types for JMIR Publications journals?" (https://support.jmir.org/hc/en-us/articles/115004950787-What-are-the-article-types-for-JMIR-Publications-journals), the Viewpoint manuscript structure is: "Unstructured; using descriptive section headers that organize the work according to the content presented is strongly recommended. Headings such as 'Methods' and 'Results' are not allowed in Viewpoints." We have therefore used descriptive thematic headers throughout, as the Viewpoint article type requires, rather than IMRD headings. We would of course be glad to adjust if the editor prefers, recognizing that adopting an IMRD structure with Methods and Results headings would entail re-designating the article type away from Viewpoint.

COMMENT (required): Add a funding statement, distinct from the Acknowledgements.

RESPONSE: A Funding section is present and is distinct from the Acknowledgments. Because financial support was received, the "no financial support" statement does not apply; the Funding statement reads: "Yuimedi, Inc. provided financial support for the author's time researching and writing this manuscript." This is consistent with the Conflicts of Interest disclosure of the author's role at Yuimedi.

COMMENT (required): Disclose whether generative AI was used in any portion of the manuscript generation.

RESPONSE: A generative AI disclosure is included in the manuscript (within Acknowledgments). It states that generative AI (Gemini CLI and Claude Code) was used to assist manuscript editing, language refinement, and literature search; that it was not used to generate research findings, data, or conclusions; and that the author conducted the research and verified all claims, citations, and AI-assisted text.

==================================================
REVIEWER Q
==================================================

COMMENT (Major 1): The manuscript frequently claims low maturity by referring to certifications such as HIMSS. Organizations primarily avoid such assessments due to high costs, so self-selection bias requires attention. In addition, acronyms are used without proper explanation.

RESPONSE: We added a self-selection-bias caveat in the Pillar 1 (Analytics Maturity) evidence: because HIMSS AMAM assessment is voluntary and self-selected, the reported figures likely over-represent analytics-committed organizations, so low maturity may be even more widespread than the counts suggest. This is supported by the organizational-survey methodology literature on non-response and self-selection bias [Halbesleben & Whitman 2013, Health Services Research; Tomaskovic-Devey et al. 1994, Administrative Science Quarterly]. We also broadened the maturity discussion beyond HIMSS by defining analytics maturity through the wider maturity-model literature (see Reviewer T, comment 1). Regarding cost as the specific mechanism of avoidance: we did not find an authoritative source attributing assessment avoidance specifically to cost, so we have framed the issue as self-selection bias grounded in the methodology literature rather than asserting an unsupported cost mechanism. On acronyms: all domain acronyms (HIMSS, AMAM, NL2SQL, EMR, EMRAM, LLM, ACO, EHR, CMS, CIO, DIKW, AACODS) are now defined at first use in the running text, and the Abbreviations list has been completed.

COMMENT (Major 2): The practicality of the framework depends on the volume, diversity, and frequency of queries. If an organization requires only 50 frequent queries, the problem can be addressed by documentation or an industry-level knowledge base.

RESPONSE: We added a scope-conditions discussion to the Comparison of Existing Approaches. Empirical query-log studies show that organizational analytical workloads are neither small nor static: more than half of analytical queries recur in large production workloads [Jindal et al. 2019], yet even small databases log thousands of distinct query strings [Kul et al. 2018]. A fixed set of documented queries therefore captures neither the large recurring core nor the evolving ad-hoc tail. HITL-KG addresses both regimes, reusing validated triples for recurring queries and capturing new ones at the point of use. This directly answers the "50 queries" objection: the recurring set is real but neither tiny nor static, and the diverse tail is exactly where documentation fails. The reviewer also raised the alternative of an industry-level knowledge base; the manuscript's Structural Barriers section addresses this, arguing that institution-specific business logic (local billing rules, coding conventions, and schema idiosyncrasies) is precisely what shared or industry-level knowledge bases cannot capture, as the failures of centralized efforts such as IBM Watson Health and Haven illustrate. HITL-KG captures this local logic rather than enforcing global standards.

COMMENT (Major 3): A central concern is whether the human-in-the-loop can actually perform better than AI or LLMs. An empirical investigation of experts detecting and correcting AI errors would significantly add value; otherwise the model's effectiveness is debatable.

RESPONSE: We agree this is the pivotal question. We have added empirical evidence to the Safety as Cognitive Forcing section showing that human oversight measurably improves AI-generated analytics: in a prospective study across six systematic reviews, large-language-model output verified by a human reviewer outperformed a human-only workflow (91.0% versus 89.0% accuracy) [Gartlehner et al. 2025, Annals of Internal Medicine]; in text-to-SQL specifically, an expert validation gate improved semantic correctness by 28.4% over end-to-end model output [Benzarti & Berrabah 2026]. We also cite balancing evidence that these gains are conditional on well-designed interaction [Ning et al. 2024]. Because this is a Viewpoint, we do not present an original empirical study; instead, we now frame HITL-KG explicitly as a prescriptive design whose comparative effectiveness is the subject of planned empirical validation, and the Implications section identifies the controlled evaluation (error rates, recovery time, and rework versus baseline tooling) as a priority for that future work.

COMMENT (Major 4): If data is constantly changing, the tenure of informatics experts may not be enough to address the maturity issue; training and awareness will be key players too.

RESPONSE: We added a paragraph to Limitations acknowledging both points. HITL-KG complements rather than replaces workforce development: it decouples institutional knowledge from individual tenure but still presumes investment in training and analytics literacy [Konrad et al. 2022]. Moreover, precisely because retained expertise cannot manually keep pace with continual change in data models and business rules, knowledge must be externalized into curated artifacts; we also acknowledge that the validated query library itself requires active maintenance, which the Continuous Analytic Integration mechanism supports but does not eliminate.

COMMENT (Minor 5): Please clearly explain the acronyms used throughout the manuscript.

RESPONSE: Addressed as in comment 1: acronyms are now defined at first use, and the Abbreviations list is complete.

COMMENT (Minor 6): Some references, especially those on the tenure of healthcare IT workers, are more than 20 years old and should be replaced.

RESPONSE: The Workforce Agility evidence now relies on contemporary (2021-2025) data, including replacement-cost figures and current intent-to-leave and turnover statistics [for example, Rajamani et al. 2025; National Healthcare Retention report 2025]. The single remaining reference to the 2004 study (Ang & Slaughter) appears only once, in the Introduction, where it is explicitly framed as a two-decade-old benchmark whose continued use is itself evidence of the field's instability; the duplicate prior mention was removed.

==================================================
REVIEWER T
==================================================

COMMENT (Major 1): Please clearly define the key terms in the title (analytics maturity, workforce agility, technical enablement), ideally grounded in existing literature.

RESPONSE: We added explicit, cited definitions at the head of each evidence pillar. Analytics maturity is defined as an organization's progression in using data and quantitative models for fact-based decisions [Davenport & Harris 2007], operationalized through staged maturity models beyond the HIMSS model [Grossman 2018; Langer 2025]. Workforce agility is defined as a workforce's capacity for proactivity, adaptability, and resilience under change [Breu et al. 2002; Tessarini Junior & Saltorato 2021]. Technical enablement is defined as the technologies and practices that let non-specialist domain users access and analyze data without heavy reliance on central IT [Alpar & Schulz 2016; Bani-Hani et al. 2020].

COMMENT (Major 2): Some content is repetitive; for example, CIO tenure and turnover statistics are introduced in the Introduction and reiterated in Section 2.1. Consider consolidating.

RESPONSE: We removed the repeated statistics (the 53% CIO short-tenure figure and the 55% public-health-informatics intent-to-leave figure) from the "Broken Cycle" section, where they had duplicated the Introduction. These statistics are now stated once, at first mention in the Introduction, and the "Broken Cycle" section refers back to them while retaining only the figures unique to its argument.

COMMENT (Major 3): Figure 1 depicts a static knowledge base and best practices. Step 7 (organizational memory) should feed back into Step 1 (knowledge base and best practices) to illustrate continuous learning and system updating.

RESPONSE: We revised Figure 1 to add a feedback edge from Organizational Memory to the Knowledge Base, labeled "Curates best practices" (step 8). Validated query triples now update the ontologies and best practices that in turn provide context to future queries, closing a continuous-learning loop so that best practices evolve as new knowledge is validated rather than remaining static. The figure caption was updated to describe this loop.

COMMENT (Major 4): Section 4.2 references a statistic from 2004; please update with more recent evidence.

RESPONSE: Addressed together with Reviewer Q, comment 6. The 2004 statistic was removed from that section, which now relies on contemporary (2021-2025) evidence; the only remaining mention is in the Introduction, explicitly framed as a historical benchmark.

COMMENT (Minor): Please provide complete reference details for all citations, including volume, issue number, and page ranges (for example, the Ang & Slaughter 2004 reference).

RESPONSE: The Ang & Slaughter (2004) reference is now complete: ACM SIGMIS Database, 35(3), 11-27, doi:10.1145/1017114.1017118. The newly added references were entered with full author lists, volume, issue, pages, and DOIs verified against Crossref. References that lack volume or page ranges are non-paginated sources (industry reports, institutional web resources, and press releases), cited with publisher and URL as appropriate.

==================================================

We thank the editor and reviewers again for their time. We believe the revisions materially strengthen the manuscript's evidentiary grounding, conceptual clarity, and formatting compliance, and we welcome any further guidance.
