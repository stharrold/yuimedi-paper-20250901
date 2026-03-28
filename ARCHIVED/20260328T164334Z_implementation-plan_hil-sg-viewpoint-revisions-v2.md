# Implementation Plan v2: HiL-SG Viewpoint Paper Revisions

**Date:** 2026-03-28
**Supersedes:** `ARCHIVED/20260328T140009Z_implementation-plan_hil-sg-viewpoint-revisions.md`
**Implements:** `ARCHIVED/20260328T135652Z_recommendations_hil-sg-viewpoint-revisions-v2.md`
**Target file:** `paper.md`
**Validation:** `scripts/validate_jmir_compliance.py --article-type viewpoint`

**Research completed:** 7 Scholar Labs searches, 7 research files created. All recommendations now have peer-reviewed backing.

---

## Pre-flight Checklist

- [ ] Create feature branch: `feature/paper-revisions-v2`
- [ ] Baseline word count: `cat paper.md | sed '1,/^---$/d' | sed '/^# Acknowledgments/,$d' | wc -w`
- [ ] Run JMIR validator: `uv run python scripts/validate_jmir_compliance.py --article-type viewpoint`
- [ ] Run reference validator: `uv run python scripts/validate_references.py --all`
- [ ] Snapshot current PDF: `./scripts/build_paper.sh --format all`

---

## New References to Add to `references.bib`

These references were identified through 7 Google Scholar Labs searches and documented in `docs/research/Research_*.md` files. Add all to `references.bib` before editing `paper.md`.

| BibTeX Key | Citation | Used In | Research File |
|---|---|---|---|
| `@ignatowicz2023` | Ignatowicz A, et al. "Organizational resilience in healthcare: a review..." BMC Health Services Research. 2023. Cited 68. | R5 (ARI) | `Research_Organizational-Resilience-Measurement-Instruments-Healthcare.md` |
| `@ellis2026` | Ellis LA, et al. "From theory to measurement: Development and initial validation of the RHCA." Applied Ergonomics. 2026. | R5 (ARI) | same |
| `@kumar2025caos` | Kumar R, et al. "Navigating healthcare AI governance: the CAOS framework." Health Care Analysis. 2025. Cited 6. | R2 (Validator Paradox) | `Research_Tiered-Validation-Governance-Healthcare-AI.md` |
| `@labkoff2024` | Labkoff S, et al. "Toward a responsible future: recommendations for AI-enabled CDS." JAMIA. 2024;31(11):2730. Cited 152. | R2 (Validator Paradox) | same |
| `@kalyanasundaram2025` | Kalyanasundaram S. "Data Lake Governance: Establishing a SSOT in Healthcare Enterprises." IJETCSIT. 2025. | R2 (Golden Query) | `Research_Golden-Record-Master-Data-Governance-Healthcare.md` |
| `@loshin2010` | Loshin D. Master Data Management. Morgan Kaufmann. 2010. Cited 590. | R2 (Golden Query) | same |
| `@valiaiev2025` | Valiaiev D. "Implementing DataOps: A Scalable Framework for Modern Data Warehousing." ProQuest. 2025. | R8 (Continuous Analytic Integration) | `Research_CI-CD-Automated-Testing-Analytics-Queries-Healthcare.md` |
| `@betha2023` | Betha R. "Data Observability and Data Quality Automation: Building Self-Healing Data Pipelines." IJAIDR. 2023. | R8 (Continuous Analytic Integration) | same |
| `@kottam2025` | Kottam S, et al. "Error-Aware Text-to-SQL Generation for Clinical Trial Eligibility Criteria Querying in EHR Databases." IEEE. 2025. | R4 (Schema drift) | same |
| `@wynendaele2025` | Wynendaele H, et al. "Understanding turnover in healthcare..." BMC Health Services Research. 2025. Cited 17. | R9 (replaces @oracle2024) | `Research_Healthcare-Turnover-Cost-Peer-Reviewed.md` |
| `@halter2017` | Halter M, et al. "The determinants and consequences of adult nursing staff turnover." BMC Health Services Research. 2017. Cited 602. | R9 (corroborates) | same |
| `@hackney2024` | Hackney A. "Onboarding New Hires in CIPS Department with TSAM." ProQuest. 2024. | R9 (informatics-specific) | same |
| `@chen2026graph` | Chen Q, et al. "Graph-empowered Text-to-SQL generation on EMR." Pattern Recognition. 2026. Cited 5. | R4 (94.2% MIMICSQL) | `Research_Graph-Enhanced-NL2SQL-Healthcare-Benchmarks.md` |
| `@blaskovic2025` | Blaskovic L, et al. "Robust Clinical Querying with Local LLMs..." Big Data and Cognitive Computing. 2025. | R4 (9-LLM benchmark) | same |
| `@tarbell2024` | Tarbell R, et al. "Towards understanding the generalization of medical text-to-SQL..." AMIA. 2024. Cited 11. | R4/Section 7 (generalization gap) | same |
| `@yuan2019` | Yuan C, et al. "Criteria2Query: a natural language interface to clinical databases." JAMIA. 2019;26(4):294. Cited 206. | R9 (replaces @dadi2025) | `Research_NL-Interface-Productivity-Gains-Healthcare-Enterprise.md` |
| `@nittala2024` | Nittala EP. "Leveraging LLMs for NLI in ERP Systems: User Productivity and Cognitive Load." IJETCSIT. 2024. Cited 34. | R9 (corroborates) | same |

**Total new references:** 17

---

## Pass 1: Language Edits (R1, R6, R10, R11)

**Goal:** Tighten language, reclaim ~120 words from repetition, fix claim/evidence alignment.
**Estimated net change:** -60 words

### Step 1.1: Reduce DSR methodology language (R10)

**File:** `paper.md` line 49
**Current:**
```
Using a Design Science Research (DSR) approach, we developed the HiL-SG framework through three steps: (1) a narrative review of the literature (n=139 sources) across healthcare analytics maturity, workforce turnover dynamics, and natural language processing, with grey literature assessed using the AACODS checklist [@tyndall2010]; (2) theoretical grounding in Nonaka's SECI model of knowledge creation [@farnese2019], mapping workforce turnover data to specific failure modes in knowledge transfer; and (3) artifact design of the HiL-SG framework and the "Validated Query Triple" as socio-technical solutions to the identified "Socialization Failure," adhering to "Human-on-the-Loop" principles for AI safety [@bravorocca2023].
```

**Replace with:**
```
We ground our analysis in Nonaka's SECI model of knowledge creation [@farnese2019], informed by a narrative review of the literature (n=139 sources) across healthcare analytics maturity, workforce turnover dynamics, and natural language processing, with grey literature assessed using the AACODS checklist [@tyndall2010]. Grey literature sources were retained only when no peer-reviewed equivalent was available or when the source provided unique industry data not captured in academic literature.
```

**Saves:** ~30 words

### Step 1.2: Add prescriptive stance declaration (R6)

**File:** `paper.md` after line 44 (after the research question, before "We propose that the solution...")
**Insert:**
```
As a Viewpoint, this paper deliberately advances a prescriptive position: that healthcare organizations should shift from passive knowledge management to active, artifact-based governance. The analysis below is grounded in descriptive evidence of why current approaches fail, but the architectural recommendations are intentionally directive.
```

**Adds:** ~45 words

### Step 1.3: Sharpen evidence-claim language (R1)

**File:** `paper.md` multiple locations

| Location | Current | Replace with |
|---|---|---|
| Abstract line 11 | "HiL-SG shifts the locus" | "HiL-SG is designed to shift the locus" |
| Abstract line 11 | "the framework converts the ephemeral act" | "the framework aims to convert the ephemeral act" |
| Abstract line 11 | "The accompanying Analytics Resilience Index (ARI) provides a measurement instrument that replaces static maturity checklists" | "The accompanying Analytics Resilience Index (ARI) proposes a measurement instrument that extends static maturity assessments" |
| Abstract line 13 (end) | Add after "...workforce evolves." | "This paper proposes and theoretically motivates the framework; empirical validation is deferred to a companion study." |
| Line 101 (Section 4 opening) | Before "The HiL-SG framework is supported by three pillars" | Insert: "The evidence presented below supports the existence and severity of the problem HiL-SG addresses, and the maturity of the technologies it requires. It does not constitute empirical validation of the framework itself, which remains a theoretically grounded, testable proposition whose empirical evaluation is the subject of Paper 2." |

**Adds:** ~60 words

### Step 1.4: Reduce repetition (R11)

| Statistic | Keep in | Action |
|---|---|---|
| 53% CIO tenure < 3 years | Section 2.1 (line 63) | Abstract line 7: change to "high leadership turnover". Section 4.2 line 111: replace with cross-reference |
| 55% informatics leaving | Section 1 (line 34) | Line 40: remove second mention. Section 4.2 line 111: cross-reference |
| 79% provider shortage | Section 4.2 (line 111) | Section 2.2 line 68: drop the "79%" number, keep general claim with citation |
| 30% first-year departure | Section 2.1 (line 63) | Section 4.2: cross-reference only |
| 18-24 months to fluency | Section 2.1 (line 63) | Section 4.2 line 109: cross-reference only |

**Saves:** ~120 words

### Step 1.5: Verify pass 1

```bash
cat paper.md | sed '1,/^---$/d' | sed '/^# Acknowledgments/,$d' | wc -w
# Expected: ~3,540 (baseline ~3,600 minus ~60)
uv run python scripts/validate_jmir_compliance.py --article-type viewpoint
```

- [ ] Word count delta check
- [ ] JMIR validator passes
- [ ] Commit: `fix(paper): tighten language, reduce repetition, clarify evidence-claim boundary`

---

## Pass 2: Port Content from Original Submission + New Research (R2, R3, R4, R7, R8)

**Goal:** Add substantive content with full research backing.
**Estimated net change:** +570 words

### Step 2.1: Add framework alignment table (R7)

**File:** `paper.md` after line 58 (after SECI spiral paragraph, before "## The Broken Cycle")
**Insert:**

```
The three-pillar structure aligns with established models across healthcare informatics and knowledge management:

| Pillar | HIMSS AMAM Alignment | DIKW Hierarchy | Knowledge Management |
|:---|:---|:---|:---|
| Analytics Maturity | Stages 0-7 progression | Data -> Information | Organizational Learning |
| Workforce Agility | Implicit in advanced stages | Knowledge (tacit) -> Wisdom | Tacit Knowledge Transfer |
| Technical Enablement | Stages 6-7 requirements | Information -> Knowledge | Knowledge Codification |

: Framework alignment with established models. \label{tab:alignment}

HIMSS AMAM provides organizational benchmarks but does not address workforce knowledge retention. The DIKW hierarchy explains progression from raw data to actionable insight but does not account for institutional memory loss. The three-pillar framework synthesizes these perspectives, positioning workforce dynamics as the critical enabler connecting data access (analytics maturity) with organizational wisdom (knowledge preservation) [@farnese2019; @rao2006].
```

**Adds:** ~100 words

### Step 2.2: Add comparative analysis section (R3)

**File:** `paper.md` after line 97 (after "## The Process of Externalization", before "# The Evidence Base")
**Insert new subsection:**

```
## Comparison with Existing Approaches

Organizations have attempted to address institutional memory loss through several strategies, each with limitations that HiL-SG is designed to overcome.

*Code-based semantic layers* (e.g., dbt, LookML) encode business logic in version-controlled repositories. However, these layers suffer from "schema rot" in healthcare environments where EMR data models change frequently (e.g., quarterly upgrades). The maintenance burden often exceeds the capacity of high-turnover teams, leading to misalignment between the layer and the underlying data [@mannapur2025; @battula2025]. HiL-SG's validated query triples share the version-control principle but add the rationale metadata that semantic layers lack: not just *what* the query does, but *why* it was constructed that way.

*Traditional knowledge management* (wikis, data dictionaries, runbooks) relies on passive capture where users must stop working to document. Evidence suggests this negatively impacts participation and produces inaccurate records due to cognitive load [@mayo2016; @goffin2011]. HiL-SG instead implements active capture: the query itself is the documentation, and validation happens at the point of use rather than as a separate maintenance task [@moore2018].

*Unsupervised AI querying* represents the opposite extreme: removing human oversight entirely. Current NL2SQL accuracy levels make this unsafe for clinical analytics [@ziletti2024]. HiL-SG occupies the middle ground, using AI as the generation engine while preserving human judgment as the validation gate.
```

**Adds:** ~190 words
**References:** All already in `references.bib`

### Step 2.3: Replace NL2SQL "tipping point" with accuracy gradient (R4)

**File:** `paper.md` line 114
**Current:**
```
NL2SQL has reached a productivity tipping point. Natural language interfaces report a 63% increase in self-service adoption and 37% reduction in retrieval time [@dadi2025].
```

**Replace with:**
```
NL2SQL technology has matured along a clear accuracy gradient: general-purpose models achieve approximately 65% execution accuracy on healthcare-specific benchmarks such as MIMICSQL [@blaskovic2025]; domain-adapted systems like MedT5SQL reach 80% [@marshan2024]; and architecturally specialized approaches combining LLMs with structured knowledge representations achieve 94% on the same benchmarks [@chen2026graph]. While insufficient for unsupervised clinical deployment [@ziletti2024], this gradient demonstrates that the generation engine required for HiL-SG is viable within a human-validated workflow. Notably, high benchmark accuracy does not guarantee real-world generalization: evaluation on more challenging dataset splits reveals accuracy drops from 92% to 28% [@tarbell2024], reinforcing the necessity of the human-in-the-loop architecture. Healthcare-specific natural language interfaces such as Criteria2Query achieve fully automated cohort query formulation in 1.22 seconds per criterion [@yuan2019], with over 80% of clinical users indicating willingness to adopt such tools, and LLM-powered interfaces reduce task completion time by 28% compared to traditional methods [@nittala2024].
```

**Adds:** ~80 words net (replaces ~30 words)
**New references:** `@blaskovic2025`, `@chen2026graph`, `@tarbell2024`, `@yuan2019`, `@nittala2024`
**Removed reference:** `@dadi2025` (al-kindipublisher, replaced with stronger sources)

### Step 2.4: Operationalize the Validator Paradox (R2)

**File:** `paper.md` lines 150-151
**Replace** the final paragraph of Section 6 (starting "However, the Validator Paradox is not fully resolved") with:

```
However, the Validator Paradox is not fully resolved. There exists a minimum viable expertise threshold below which validation becomes meaningless. A junior analyst rubber-stamping AI-generated output without genuine comprehension provides no knowledge ratchet; the validation artifact exists, but its epistemic value is nil. Identifying this threshold remains an open empirical question; future work in this series (Paper 2) should measure it via controlled hallucination injection studies, in which AI-generated queries containing deliberate errors are presented to validators of varying experience levels.

We propose a provisional three-tier governance model, informed by risk-stratified AI oversight frameworks [@kumar2025caos; @labkoff2024], to degrade gracefully when expertise is scarce. *Full validation*: a domain expert with schema-level knowledge reviews the query triple and confirms semantic alignment; this is the default mode. *Constrained validation*: when no fully qualified validator is available, a less experienced analyst reviews the triple against previously validated queries for the same data domain, flagging deviations for deferred expert review; the triple is stored with "provisional" status. *Automated regression*: for queries that match an existing validated triple with high semantic similarity, the system accepts the match without human review but logs it for periodic audit.

At the organizational level, governance requirements include defining who can validate queries (domain expertise thresholds), establishing review workflows for high-stakes queries, managing query versioning as schemas evolve, and implementing retrieval policies. Drawing on established master data governance practice [@loshin2010; @kalyanasundaram2025], organizations can designate specific validated triples as "Golden Queries," certified by a governance committee as the authoritative source of truth for key metrics. While many users can create and validate queries, only these certified triples serve as official standards, mitigating Shadow IT risks while preserving analytical agility.
```

**Adds:** ~170 words net (replaces ~80 words)
**New references:** `@kumar2025caos`, `@labkoff2024`, `@loshin2010`, `@kalyanasundaram2025`

### Step 2.5: Add Continuous Analytic Integration (R8)

**File:** `paper.md` after line 131 (after ARI complements AMAM paragraph, before Table 1)
**Insert:**

```
The "Schema Coupling" dimension can be operationalized through *Continuous Analytic Integration*: treating validated query triples not as static wiki entries but as software assets within a CI/CD pipeline [@valiaiev2025]. When a data warehouse schema is updated (e.g., a quarterly EHR upgrade), the system automatically re-runs the library of stored queries. Queries that fail or return anomalous results are flagged for review. This transforms "Institutional Memory" from a stagnant repository into a living, automated test suite that actively signals when organizational knowledge has drifted from technical reality [@betha2023]. Existing NL2SQL systems are known to lack resilience to vocabulary drift and OMOP CDM schema changes [@kottam2025], making such automated regression essential.
```

**Adds:** ~100 words
**New references:** `@valiaiev2025`, `@betha2023`, `@kottam2025`

### Step 2.6: Verify pass 2

```bash
cat paper.md | sed '1,/^---$/d' | sed '/^# Acknowledgments/,$d' | wc -w
# Expected: ~4,110 (pass 1 result ~3,540 + ~570)
uv run python scripts/validate_jmir_compliance.py --article-type viewpoint
uv run python scripts/validate_references.py --all
```

- [ ] Word count check
- [ ] JMIR validator passes
- [ ] Reference validator passes (all new BibTeX keys resolve)
- [ ] Commit: `feat(paper): add comparative analysis, governance tiers, NL2SQL gradient, framework alignment`

---

## Pass 3: Supporting Improvements (R5, R9, R13)

**Goal:** Strengthen ARI, swap weak references, improve acknowledgments.
**Estimated net change:** +200 words

### Step 3.1: Enhance ARI with pillar rubric and psychometric context (R5)

**File:** `paper.md` line 120
**Replace:** "replacing static checklists with dynamic resilience metrics"
**With:** "extending static maturity assessments with a complementary resilience dimension"

**File:** `paper.md` after the Continuous Analytic Integration paragraph (Step 2.5), before Table 1
**Insert:**

```
For organizations seeking a broader diagnostic, these resilience dimensions can be combined with capability indicators across each pillar. For Analytics Maturity: HIMSS AMAM stage, self-service analytics penetration, and AI/NL interface deployment status. For Workforce Agility: first-year staff turnover rate, leadership tenure, knowledge concentration (how many individuals hold critical expertise), time-to-productivity for new hires, and tacit knowledge capture mechanisms. For Technical Enablement: data access modality (SQL-only vs. natural language), system interoperability, and skills gap impact. Each indicator can be scored as Low, Medium, or High Strength using evidence-based anchors from the literature reviewed in Section 4.

A recent systematic review identified 23 distinct organizational resilience instruments applied in health facilities, yet found no consensus on what to measure or which indicators to use [@ignatowicz2023]. Only four instruments have been developed specifically for healthcare, and only two have been validated [@ratliff2025]. The newest, the Resilience in Healthcare Capacities Assessment (RHCA), demonstrates significant correlations between organizational resilience and both staff turnover intention and patient safety outcomes [@ellis2026]. The ARI extends this emerging measurement tradition into the specific domain of analytics capability resilience, which no existing instrument addresses. Both the ARI and the broader pillar assessment require psychometric development, including construct validation, inter-rater reliability testing, and discriminant validity assessment against AMAM, before organizational deployment. This development is planned as part of Paper 2.
```

**Adds:** ~200 words
**New references:** `@ignatowicz2023`, `@ellis2026`
**Note:** Need to add `@ratliff2025` to `references.bib`:
- Ratliff HC, Lee KA, Buchbinder M, Kelly LA, et al. "Organizational resilience in healthcare: a scoping review." Journal of Healthcare Management. 2025;70(3). URL: https://journals.lww.com/jhmonline/fulltext/2025/05000/organizational_resilience_in_healthcare__a_scoping.4.aspx

### Step 3.2: Swap weak references (R9)

**File:** `references.bib` + `paper.md`

| Current Ref | Action | New Ref | Rationale |
|---|---|---|---|
| `@oracle2024` (line 109) | Replace | `@wynendaele2025` | Peer-reviewed umbrella review (BMC Health Services Research, cited 17): "3x salary of a nurse." Add `@hackney2024` for informatics-specific data ($50K-$230K per informaticist). |
| `@dadi2025` (line 114) | Remove | `@yuan2019` + `@nittala2024` | Already handled in Step 2.3. Yuan 2019 (JAMIA, cited 206) + Nittala 2024 (cited 34) replace al-kindipublisher source. |
| `@ogunwole2023` (line 116) | Replace | Keep or replace with mainstream software engineering legacy modernization ref | Low priority. If kept, it's one of several refs in a list; the sentence still holds without it. |

**Specific edit for line 109:**
**Current:** `[@massingham2018; @oracle2024]`
**Replace with:** `[@massingham2018; @wynendaele2025]`

**Add sentence after "three times annual salary" claim:**
```
In clinical informatics specifically, replacement costs range from $50,000 to $230,000 per departing employee, with a single department losing 39 staff in one year at a total cost of up to $8.97 million [@hackney2024].
```

**Adds:** ~30 words

### Step 3.3: Update Acknowledgments (R13)

**File:** `paper.md` line 174
**Replace:**
```
The author (S.T.H.) takes full responsibility for the final content, conducted the research, and verified all claims and citations. Gemini CLI (Gemini 3, Google) assisted with manuscript editing and refinement. Figures were generated using the Mermaid graph language.
```

**With:**
```
The author (S.T.H.) takes full responsibility for the final content, conducted the research, and verified all claims and citations. Gemini CLI (Gemini 3, Google) and Claude Code (Claude Opus 4, Anthropic) assisted with manuscript editing, refinement, and literature search. Figures were generated using the Mermaid graph language.
```

**Adds:** ~10 words

### Step 3.4: Verify pass 3

```bash
cat paper.md | sed '1,/^---$/d' | sed '/^# Acknowledgments/,$d' | wc -w
# Expected: ~4,350 (pass 2 result ~4,110 + ~240)
uv run python scripts/validate_jmir_compliance.py --article-type viewpoint
uv run python scripts/validate_references.py --all
```

- [ ] Word count check (must be <= 5,000)
- [ ] JMIR validator passes
- [ ] Reference validator passes
- [ ] No em-dashes: `grep -n '—' paper.md`
- [ ] Commit: `feat(paper): enhance ARI with resilience literature, swap weak references`

---

## Pass 4: Figures (R12, independent track)

### Step 4.1: Simplify Figure 1

**File:** `figures/architecture.mmd`
**Options:**
- **A (preferred):** Split into two figures (data flow + knowledge infrastructure)
- **B:** Simplify to higher-level block diagram

### Step 4.2: Increase Figure 2 font sizes

**File:** `figures/knowledge-cycle.mmd`
**Action:** Increase font sizes. Test at 50% zoom.

### Step 4.3: Regenerate and verify

```bash
podman-compose run --rm dev ./scripts/build_paper.sh --format all
```

- [ ] Visual inspection at 50% zoom
- [ ] DPI >= 300
- [ ] Commit: `fix(paper): improve figure readability for print`

---

## Final Verification

```bash
# 1. Word count (body only)
cat paper.md | sed '1,/^---$/d' | sed '/^# Acknowledgments/,$d' | wc -w
# Expected: ~4,350 (must be <= 5,000)

# 2. JMIR compliance
uv run python scripts/validate_jmir_compliance.py --article-type viewpoint

# 3. Reference validation
uv run python scripts/validate_references.py --all

# 4. Linting
uv run ruff format . && uv run ruff check --fix .

# 5. Build all formats
./scripts/build_paper.sh --format all

# 6. Em-dash check (prohibited per CLAUDE.md)
grep -n '—' paper.md

# 7. Full test suite
uv run pytest

# 8. Verify no @dadi2025 or @oracle2024 remain
grep -n 'dadi2025\|oracle2024' paper.md
```

- [ ] All validators pass
- [ ] Word count <= 5,000
- [ ] No em-dashes
- [ ] No removed references remaining
- [ ] PDF renders correctly with new tables and sections
- [ ] Figures legible at print scale
- [ ] Build artifacts committed (two-stage commit per CLAUDE.md)

---

## Commit Sequence

1. `build(refs): add 18 new references from literature search` (references.bib only)
2. `fix(paper): tighten language, reduce repetition, clarify evidence-claim boundary` (Pass 1)
3. `feat(paper): add comparative analysis, governance tiers, NL2SQL gradient, framework alignment` (Pass 2)
4. `feat(paper): enhance ARI with resilience literature, swap weak references` (Pass 3)
5. `fix(paper): improve figure readability for print` (Pass 4)
6. `build: regenerate paper PDF and HTML` (build artifacts)

---

## Word Budget Summary

| Change | Words |
|---|---|
| Starting body | ~3,600 |
| Pass 1 (R1, R6, R10, R11) | -60 |
| Pass 2 (R2, R3, R4, R7, R8) | +640 |
| Pass 3 (R5, R9, R13) | +240 |
| **Final estimate** | **~4,420** |
| JMIR Viewpoint limit | 5,000 |
| **Remaining headroom** | **~580** |

---

## Rollback Plan

Each pass is a separate commit. If word count exceeds 5,000 after any pass:
1. First cut: Trim the pillar rubric expansion in R5 from prose to a brief parenthetical (saves ~100 words)
2. Second cut: Remove Continuous Analytic Integration paragraph (saves ~100 words)
3. Third cut: Condense comparative analysis to two alternatives instead of three (saves ~60 words)

The 580-word buffer makes this unlikely.

---

## Research Provenance

Every new claim or citation added in this plan traces to a documented research file:

| Recommendation | New Citations | Research File |
|---|---|---|
| R2 (Validator Paradox governance) | `@kumar2025caos`, `@labkoff2024`, `@loshin2010`, `@kalyanasundaram2025` | `Research_Tiered-Validation-Governance-Healthcare-AI.md`, `Research_Golden-Record-Master-Data-Governance-Healthcare.md` |
| R4 (NL2SQL gradient) | `@chen2026graph`, `@blaskovic2025`, `@tarbell2024`, `@yuan2019`, `@nittala2024` | `Research_Graph-Enhanced-NL2SQL-Healthcare-Benchmarks.md`, `Research_NL-Interface-Productivity-Gains-Healthcare-Enterprise.md` |
| R5 (ARI resilience literature) | `@ignatowicz2023`, `@ellis2026`, `@ratliff2025` | `Research_Organizational-Resilience-Measurement-Instruments-Healthcare.md` |
| R8 (Continuous Analytic Integration) | `@valiaiev2025`, `@betha2023`, `@kottam2025` | `Research_CI-CD-Automated-Testing-Analytics-Queries-Healthcare.md` |
| R9 (Reference swaps) | `@wynendaele2025`, `@hackney2024` | `Research_Healthcare-Turnover-Cost-Peer-Reviewed.md` |
