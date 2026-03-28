# Recommendations v2: Addressing Weaknesses in the HiL-SG Viewpoint Paper

**Date:** 2026-03-28
**Supersedes:** `ARCHIVED/20260328T134827Z_recommendations_hil-sg-viewpoint-revisions.md`
**References:**
- `ARCHIVED/20260328T130105Z_critical-assessment_hil-sg-viewpoint-paper.md`
- `ARCHIVED/20260115_JMIR-Submission/paper.pdf` (original rejected submission, ~12,730 words)
**Target:** `paper.md` (JMIR Viewpoint resubmission, ms#91493)

---

## What Changed in v2

v1 recommendations were based solely on the current Viewpoint. This revision incorporates material from the original January 2026 submission that was cut during the rewrite. Several recommendations now include specific text that can be ported from the original, reducing the authoring burden and improving evidence density.

---

## Word Budget

| Item | Words |
|------|-------|
| Current body estimate | ~3,600 |
| JMIR Viewpoint limit | 5,000 |
| Available headroom | ~1,400 |
| R11 (repetition reduction) | -120 |
| **Total available for additions** | **~1,520** |

---

## R1. Sharpen the Evidence-Claim Boundary (Weakness 3.1)

**Problem:** The three evidence pillars prove the problem and component maturity, not the framework itself. The text sometimes implies HiL-SG is validated.

**Action:**

1. Add an explicit paragraph at the start of Section 4:

   > "The evidence presented below supports the existence and severity of the problem HiL-SG is designed to address, and the maturity of the technologies it requires. It does not constitute empirical validation of the framework itself. HiL-SG remains a theoretically grounded, testable proposition; its empirical evaluation is the subject of Paper 2 in this series."

2. Audit claim language throughout. Replace passive constructions that imply validation:
   - "HiL-SG shifts the locus" -> "HiL-SG is designed to shift"
   - "the framework converts the ephemeral act" -> "the framework aims to convert"
   - "the ARI provides a measurement instrument" -> "the ARI proposes a measurement instrument"

3. In the abstract, add: "This paper proposes and theoretically motivates a framework; empirical validation is deferred to a companion study."

**Word cost:** +40 (net neutral after language tightening elsewhere)

---

## R2. Operationalize the Validator Paradox with Governance Tiers (Weakness 3.2)

**Problem:** The Lean "Standard Work" resolution is philosophically sound but operationally empty.

**Source material from original paper:**
- Section 5.4 (p34): governance requirements paragraph
- Section 5.5.4 (p39): "Golden Query" governance concept
- Section 5.4.1 (p34): "Even provisional validation by mid-level analysts captures operational logic into a procedural artifact"

**Action:** Replace the current final paragraph of Section 6 (beginning "However, the Validator Paradox is not fully resolved") with:

> However, the Validator Paradox is not fully resolved. There exists a minimum viable expertise threshold below which validation becomes meaningless. A junior analyst rubber-stamping AI-generated output without genuine comprehension provides no knowledge ratchet; the validation artifact exists, but its epistemic value is nil. Identifying this threshold remains an open empirical question for future work (Paper 2).
>
> We propose a provisional three-tier governance model to degrade gracefully when expertise is scarce. *Full validation*: a domain expert with schema-level knowledge reviews the query triple and confirms semantic alignment; this is the default mode. *Constrained validation*: when no fully qualified validator is available, a less experienced analyst reviews the triple against previously validated queries for the same data domain, flagging deviations for deferred expert review; the triple is stored with a "provisional" status. *Automated regression*: for queries that match an existing validated triple with high semantic similarity, the system accepts the match without human review but logs it for periodic audit.
>
> At the organizational level, governance requirements include defining who can validate queries (domain expertise thresholds), establishing review processes for high-stakes queries, managing query versioning as schemas evolve, and implementing retrieval policies for when to return exact matches versus generate new SQL. To prevent the "chaos of conflicting definitions" that can arise from democratized analytics, organizations can designate specific validated triples as "Golden Queries," certified by a central committee as the authoritative source of truth for key metrics. While many users can create and validate queries, only these certified triples serve as official organizational standards, mitigating the risks of Shadow IT while preserving analytical agility.

**Word cost:** +250 (replaces ~80 words of existing text, net +170)

---

## R3. Add Comparative Analysis of Knowledge Preservation Strategies (Weakness 3.1)

**Problem:** The paper proposes HiL-SG without comparing it to existing alternatives. Reviewers will ask: "Why not just use dbt/LookML/wikis?"

**Source material from original paper:**
- Section 5.4.2 (pp35-36): comparative analysis of semantic layers, passive vs. active capture, Shadow IT

**Action:** Add a new subsection 3.3 ("Comparison with Existing Approaches") after the current Section 3.2:

> **3.3 Comparison with Existing Approaches**
>
> Organizations have attempted to address institutional memory loss through several strategies, each with characteristic limitations that HiL-SG is designed to overcome.
>
> *Code-based semantic layers* (e.g., dbt, LookML) encode business logic in version-controlled repositories. However, research indicates these layers suffer from "schema rot" in healthcare environments where EMR data models change frequently (e.g., quarterly upgrades). The maintenance burden often exceeds the capacity of high-turnover teams, leading to misalignment between the semantic layer and the underlying data [49,50]. HiL-SG's validated query triples share the version-control principle but add the rationale metadata that semantic layers lack: not just *what* the query does, but *why* it was constructed that way.
>
> *Traditional knowledge management* (wikis, data dictionaries, runbooks) relies on passive capture where users must stop working to document. Evidence suggests this negatively impacts participation and leads to inaccurate records due to cognitive load [12,26]. HiL-SG instead implements active capture, where the query itself is the documentation and validation happens at the point of use rather than as a separate maintenance task [27].
>
> *Unsupervised AI querying* represents the opposite extreme: removing human oversight entirely. Current NL2SQL accuracy levels make this approach unsafe for clinical analytics [29]. HiL-SG occupies the middle ground, using AI as the generation engine while preserving human judgment as the validation gate.

**Word cost:** +200

---

## R4. Replace "Tipping Point" with NL2SQL Accuracy Gradient (Weakness 3.4)

**Problem:** Calling 80% accuracy a "tipping point" undermines credibility.

**Source material from original paper:**
- Section 4.3.1-4.3.3 (pp23-24): GPT-5 64.6% on MIMICSQL, graph-empowered 94.2%, SCARE benchmark details

**Action:** In Section 4.3, replace "NL2SQL has reached a productivity tipping point" with:

> NL2SQL technology has matured along a clear accuracy gradient. General-purpose models achieve approximately 65% execution accuracy on healthcare-specific benchmarks such as MIMICSQL [44]; domain-adapted systems like MedT5SQL reach 80% [44]; and architecturally specialized approaches combining LLMs with structured knowledge representations achieve 94% on the same benchmarks. While current models remain insufficient for unsupervised clinical deployment [29], this accuracy gradient demonstrates that the generation engine required for HiL-SG is viable within a human-validated workflow. Indeed, the remaining error rate is precisely what makes the validation step load-bearing rather than ceremonial: at current accuracy levels, unsupervised NL2SQL would introduce errors into a significant fraction of queries, reinforcing the necessity of the human-in-the-loop architecture.

**Word cost:** +60 (replaces ~80 words, net -20)

---

## R5. Strengthen the ARI with the Three-Pillar Rubric (Weakness 3.5)

**Problem:** The ARI has only four dimensions with no psychometric grounding or operational specificity.

**Source material from original paper:**
- Table 4 (pp36-38): Three-Pillar Organizational Assessment Rubric with Low/Medium/High indicators and evidence citations

**Action:**

1. In Section 5, replace "replacing static checklists with dynamic resilience metrics" with "extending static maturity assessments with a complementary resilience dimension."

2. After the current Table 1, add a paragraph connecting ARI to the original paper's more developed rubric:

   > The ARI dimensions above measure resilience under workforce stress. For organizations seeking a broader diagnostic, these resilience dimensions can be combined with capability indicators across each pillar. For Analytics Maturity: HIMSS AMAM stage, self-service analytics penetration, and AI/NL interface deployment status. For Workforce Agility: first-year staff turnover rate, leadership tenure, knowledge concentration (how many individuals hold critical expertise), time-to-productivity, and tacit knowledge capture mechanisms. For Technical Enablement: data access modality (SQL-only vs. natural language), system interoperability, and skills gap impact. Each indicator can be scored as Low, Medium, or High Strength using evidence-based anchors from the literature reviewed in Section 4. An organization scoring predominantly "Low Strength" across multiple pillars faces the compounding degradation cycle that the framework identifies as the central threat.

3. Add the psychometric caveat:

   > Both the ARI and the broader pillar assessment require psychometric development (construct validation, inter-rater reliability, discriminant validity against AMAM) before organizational deployment. This development is planned as part of Paper 2.

**Word cost:** +150

---

## R6. Resolve the Descriptive vs. Prescriptive Tension (Weakness 3.3)

**Problem:** The paper oscillates between describing interconnections and recommending actions.

**Action:** Add a sentence early in Section 1, after the research question:

> As a Viewpoint, this paper deliberately advances a prescriptive position: that healthcare organizations should shift from passive knowledge management to active, artifact-based governance. The framework we propose is grounded in descriptive analysis of why current approaches fail, but the architectural recommendations that follow are intentionally directive.

This aligns with JMIR Viewpoint norms. A Viewpoint that hedges reads as uncertain, not careful.

**Word cost:** +50

---

## R7. Add Framework Alignment Table (addresses genre fit, Weakness 4.1)

**Problem:** The paper reads like a compressed Original Paper. Adding theoretical breadth (rather than methodological depth) is the Viewpoint-appropriate way to strengthen the foundation.

**Source material from original paper:**
- Table 3 (p17): Framework Alignment with Established Models

**Action:** Add a compact table in Section 2 after the SECI discussion:

> The three-pillar structure aligns with established models across healthcare informatics and knowledge management:
>
> | Pillar | HIMSS AMAM | DIKW Hierarchy | Knowledge Management |
> |--------|-----------|----------------|---------------------|
> | Analytics Maturity | Stages 0-7 progression | Data -> Information | Organizational Learning |
> | Workforce Agility | Implicit in advanced stages | Knowledge (tacit) -> Wisdom | Tacit Knowledge Transfer |
> | Technical Enablement | Stages 6-7 requirements | Information -> Knowledge | Knowledge Codification |
>
> This alignment demonstrates that the three pillars are not arbitrary categories but map to recognized theoretical constructs. HIMSS AMAM provides organizational benchmarks but does not address workforce knowledge retention. The DIKW hierarchy explains progression from raw data to actionable insight but does not address institutional memory loss. The three-pillar framework synthesizes these perspectives, positioning workforce dynamics as the critical enabler connecting data access (analytics maturity) with organizational wisdom (knowledge preservation).

**Word cost:** +130

---

## R8. Add Continuous Analytic Integration Concept (strengthens ARI Schema Coupling)

**Source material from original paper:**
- Section 5.4.3 (pp35-36): CI/CD for validated queries

**Action:** Add to Section 5.2 (Operationalizing the ARI), under the Schema Coupling dimension:

> The "Schema Coupling" dimension can be operationalized through what we term *Continuous Analytic Integration*: treating validated query triples not as static wiki entries but as software assets within a CI/CD pipeline. When a data warehouse schema is updated (e.g., a quarterly EHR upgrade), the system automatically re-runs the library of stored queries. Queries that fail or return anomalous results are flagged for review. This transforms "Institutional Memory" from a stagnant repository into a living, automated test suite that actively signals when organizational knowledge has drifted from technical reality.

**Word cost:** +90

---

## R9. Strengthen the Reference Base (Weakness 3.6)

**Problem:** Several references are from low-impact or grey-literature sources.

**Action:**

1. **Priority replacements:**
   - Ref 41 (Oracle vendor white paper): Replace with Waldman et al. (2004) "The shocking cost of turnover in health care," Health Care Management Review. Already cited in the original paper (ref 72).
   - Ref 42 (al-kindipublisher): Replace with a more established NL interface survey.
   - Ref 47 (Int'l Journal of Multidisciplinary Research): Replace with mainstream software engineering source on legacy modernization.

2. **Add AACODS transparency sentence** to Section 2:
   > Grey literature sources (industry reports, white papers) were assessed using the AACODS checklist [17] and retained only when no peer-reviewed equivalent was available or when the source provided unique industry data not captured in academic literature.

3. **Add NL2SQL benchmark references from original paper** where they strengthen Section 4.3: SCARE benchmark, MIMICSQL graph-empowered results, Criteria2Query 3.0.

**Word cost:** +30 (sentence); references swapped (no word impact)

---

## R10. Reduce DSR Methodology Language (Weakness 4.1)

**Problem:** Section 2 reads as a Methods section, which is a genre mismatch for a Viewpoint.

**Action:** Replace the three-step DSR enumeration in Section 2 with:

> We ground our analysis in Nonaka's SECI model of knowledge creation [18], informed by a narrative review of the literature (n=139 sources) across healthcare analytics maturity, workforce turnover, and natural language processing, with grey literature assessed using the AACODS checklist [17].

Remove: "(1) a narrative review of the literature... (2) theoretical grounding in Nonaka's SECI model... (3) artifact design of the HiL-SG framework."

**Word cost:** -30

---

## R11. Reduce Repetition to Fund Additions

**Problem:** Key statistics appear 3-4 times each.

**Action:**

| Statistic | Keep in | Remove/condense in |
|-----------|---------|-------------------|
| 53% CIO tenure < 3 years | Section 2.1 | Abstract (-> "high CIO turnover"), Section 4.2 (cross-ref) |
| 55% informatics specialists leaving | Section 1 | Abstract (condense), Section 4.2 (cross-ref) |
| 79% provider shortage | Section 4.2 | Section 2.2 (remove) |
| 30% first-year departure | Section 2.1 | Section 4.2 (cross-ref) |
| 18-24 months to fluency | Section 2.1 | Section 4.2 (cross-ref) |

**Word cost:** -120

---

## R12. Improve Figure Readability (Weakness 4.2)

**Action:**

1. **Figure 1:** Split into two figures or simplify to a higher-level block diagram. The left-side flow (User Interaction -> Insight Delivery) and right-side Knowledge Infrastructure are hard to parse as a single dense diagram at journal print scale.

2. **Figure 2:** Increase font size in flowchart boxes. Test at 50% zoom; if unreadable, fonts must increase.

3. Ensure 300+ DPI output for print. Check JMIR figure submission requirements.

**Word cost:** 0

---

## R13. Acknowledge Single-Author Scope (Weakness 3.7)

**Action (choose one):**

1. **Best:** Add a co-author with healthcare informatics domain expertise before resubmission.

2. **If not feasible:** Strengthen the Acknowledgments to name domain experts who provided feedback:
   > "The author thanks [names] for critical review of the healthcare informatics and knowledge management components of this framework."

**Word cost:** +20

---

## Implementation Priority and Sequencing

### Pass 1: Language edits (low effort, high impact)

| # | Recommendation | Words | Addresses |
|---|---------------|-------|-----------|
| R1 | Evidence-claim boundary | +40 | Weakness 3.1 |
| R6 | Own prescriptive stance | +50 | Weakness 3.3 |
| R10 | Reduce DSR language | -30 | Weakness 4.1 |
| R11 | Reduce repetition | -120 | Funds other changes |
| | **Pass 1 subtotal** | **-60** | |

### Pass 2: Port content from original (medium effort, high impact)

| # | Recommendation | Words | Addresses |
|---|---------------|-------|-----------|
| R2 | Validator Paradox governance tiers + Golden Queries | +170 | Weakness 3.2 |
| R3 | Comparative analysis (semantic layers, active capture, Shadow IT) | +200 | Weakness 3.1 |
| R4 | NL2SQL accuracy gradient | -20 | Weakness 3.4 |
| R7 | Framework alignment table | +130 | Weakness 4.1 |
| R8 | Continuous Analytic Integration | +90 | Weakness 3.5 |
| | **Pass 2 subtotal** | **+570** | |

### Pass 3: Supporting improvements (medium effort, medium impact)

| # | Recommendation | Words | Addresses |
|---|---------------|-------|-----------|
| R5 | ARI enhancement + pillar rubric | +150 | Weakness 3.5 |
| R9 | Reference swaps + AACODS sentence | +30 | Weakness 3.6 |
| R13 | Single-author acknowledgment | +20 | Weakness 3.7 |
| | **Pass 3 subtotal** | **+200** | |

### Pass 4: Figures (independent, parallel track)

| # | Recommendation | Words | Addresses |
|---|---------------|-------|-----------|
| R12 | Figure readability | 0 | Weakness 4.2 |

---

## Final Word Budget

| Item | Words |
|------|-------|
| Starting body | ~3,600 |
| Pass 1 | -60 |
| Pass 2 | +570 |
| Pass 3 | +200 |
| **Final estimate** | **~4,310** |
| JMIR Viewpoint limit | 5,000 |
| **Remaining headroom** | **~690** |

The revised paper would use ~86% of the available word budget, leaving comfortable margin for editorial adjustments during review.

---

## Summary of Changes from v1

| v1 Recommendation | v2 Status |
|---|---|
| R1 (evidence-claim boundary) | Retained as R1 |
| R2 (provisional three-tier protocol) | **Expanded** as R2: now includes governance requirements and Golden Query concept from original paper |
| R3 (descriptive vs. prescriptive) | Retained as R6 |
| R4 (NL2SQL tipping point) | **Strengthened** as R4: now uses specific accuracy gradient numbers from original paper |
| R5 (ARI reframing) | **Expanded** as R5: now includes three-pillar rubric content from original Table 4 |
| R6 (reference base) | **Expanded** as R9: now includes specific replacement references from original paper's bibliography |
| R7 (reduce repetition) | Retained as R11 |
| R8 (article type framing) | **Split** into R7 (add framework alignment table from original) + R10 (reduce DSR language) |
| R9 (figures) | Retained as R12 |
| R10 (single author) | Retained as R13 |
| -- | **New R3**: Comparative analysis of knowledge preservation strategies (from original Section 5.4.2) |
| -- | **New R8**: Continuous Analytic Integration concept (from original Section 5.4.3) |
