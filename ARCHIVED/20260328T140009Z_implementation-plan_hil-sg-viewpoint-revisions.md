# Implementation Plan: HiL-SG Viewpoint Paper Revisions

**Date:** 2026-03-28
**Implements:** `ARCHIVED/20260328T135652Z_recommendations_hil-sg-viewpoint-revisions-v2.md`
**Target file:** `paper.md`
**Validation:** `scripts/validate_jmir_compliance.py --article-type viewpoint`

---

## Pre-flight Checklist

- [ ] Create feature branch: `feature/paper-revisions-v2`
- [ ] Baseline word count: `cat paper.md | sed '1,/^---$/d' | sed '/^# Acknowledgments/,$d' | wc -w`
- [ ] Run JMIR validator: `uv run python scripts/validate_jmir_compliance.py --article-type viewpoint`
- [ ] Run reference validator: `uv run python scripts/validate_references.py --all`
- [ ] Snapshot current PDF: `./scripts/build_paper.sh --format all`

---

## Pass 1: Language Edits (R1, R6, R10, R11)

**Goal:** Tighten language, reclaim ~120 words from repetition, fix claim/evidence alignment.
**Estimated net change:** -60 words

### Step 1.1: Reduce DSR methodology language (R10)

**File:** `paper.md` line 49
**Action:** Replace the three-step DSR enumeration with lighter framing.

**Current text (line 49):**
```
Using a Design Science Research (DSR) approach, we developed the HiL-SG framework through three steps: (1) a narrative review of the literature (n=139 sources) across healthcare analytics maturity, workforce turnover dynamics, and natural language processing, with grey literature assessed using the AACODS checklist [@tyndall2010]; (2) theoretical grounding in Nonaka's SECI model of knowledge creation [@farnese2019], mapping workforce turnover data to specific failure modes in knowledge transfer; and (3) artifact design of the HiL-SG framework and the "Validated Query Triple" as socio-technical solutions to the identified "Socialization Failure," adhering to "Human-on-the-Loop" principles for AI safety [@bravorocca2023].
```

**Replace with:**
```
We ground our analysis in Nonaka's SECI model of knowledge creation [@farnese2019], informed by a narrative review of the literature (n=139 sources) across healthcare analytics maturity, workforce turnover dynamics, and natural language processing, with grey literature assessed using the AACODS checklist [@tyndall2010]. Grey literature sources were retained only when no peer-reviewed equivalent was available or when the source provided unique industry data not captured in academic literature.
```

**Saves:** ~30 words

### Step 1.2: Add prescriptive stance declaration (R6)

**File:** `paper.md` after line 44 (after the research question)
**Action:** Insert before "We propose that the solution lies not in better documentation":

```
As a Viewpoint, this paper deliberately advances a prescriptive position: that healthcare organizations should shift from passive knowledge management to active, artifact-based governance. The analysis below is grounded in descriptive evidence of why current approaches fail, but the architectural recommendations are intentionally directive.
```

**Adds:** ~45 words

### Step 1.3: Sharpen evidence-claim language (R1)

**File:** `paper.md` multiple locations
**Actions (line-by-line):**

1. **Abstract (line 11):** "HiL-SG shifts the locus" -> "HiL-SG is designed to shift the locus"
2. **Abstract (line 11):** "the framework converts the ephemeral act" -> "the framework aims to convert the ephemeral act"
3. **Abstract (line 11):** "The accompanying Analytics Resilience Index (ARI) provides a measurement instrument that replaces static maturity checklists" -> "The accompanying Analytics Resilience Index (ARI) proposes a measurement instrument that extends static maturity assessments"
4. **Line 101:** Before "The HiL-SG framework is supported by three pillars of empirical evidence", insert: "The evidence presented below supports the existence and severity of the problem HiL-SG addresses, and the maturity of the technologies it requires. It does not constitute empirical validation of the framework itself, which remains a theoretically grounded, testable proposition whose empirical evaluation is the subject of Paper 2."
5. **Abstract (line 13):** After "functioning as a 'knowledge ratchet' that prevents regression", add: "This paper proposes and theoretically motivates the framework; empirical validation is deferred to a companion study."

**Adds:** ~60 words

### Step 1.4: Reduce repetition (R11)

**File:** `paper.md` multiple locations

| Statistic | Keep in | Action |
|-----------|---------|--------|
| 53% CIO tenure < 3 years | Section 2.1 (line 63) | Abstract line 7: change to "high leadership turnover". Section 1 line 34: keep (first body mention). Section 4.2 line 111: replace with "as detailed in Section 2.1" |
| 55% informatics leaving | Section 1 (line 34) | Abstract line 7: keep (abstract must stand alone). Line 40: remove second mention. Section 4.2 line 111: replace with cross-reference |
| 79% provider shortage | Section 4.2 (line 111) | Section 2.2 line 68: remove or replace with "persistent shortages in digital health roles [@himssworkforce2024]" (drop the 79% number here) |
| 30% first-year departure | Section 2.1 (line 63) | Section 1 line 40: keep (supports the narrative). Section 4.2: cross-reference only |
| 18-24 months to fluency | Section 2.1 (line 63) | Section 4.2 line 109: cross-reference only |

**Saves:** ~120 words

### Step 1.5: Verify pass 1

- [ ] Word count delta check (expect ~-60)
- [ ] Run JMIR validator
- [ ] Commit: `fix(paper): tighten language, reduce repetition, clarify evidence-claim boundary`

---

## Pass 2: Port Content from Original Submission (R2, R3, R4, R7, R8)

**Goal:** Add substantive content ported from original January 2026 paper.
**Estimated net change:** +570 words

### Step 2.1: Add framework alignment table (R7)

**File:** `paper.md` after line 58 (after the SECI spiral paragraph, before "## The Broken Cycle")
**Action:** Insert:

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

**Adds:** ~100 words (excluding table markup)
**New references needed:** None (existing refs cover DIKW through existing citations)

### Step 2.2: Add comparative analysis section (R3)

**File:** `paper.md` after line 97 (after "## The Process of Externalization" steps, before "# The Evidence Base")
**Action:** Insert new subsection:

```
## Comparison with Existing Approaches

Organizations have attempted to address institutional memory loss through several strategies, each with limitations that HiL-SG is designed to overcome.

*Code-based semantic layers* (e.g., dbt, LookML) encode business logic in version-controlled repositories. However, these layers suffer from "schema rot" in healthcare environments where EMR data models change frequently (e.g., quarterly upgrades). The maintenance burden often exceeds the capacity of high-turnover teams, leading to misalignment between the layer and the underlying data [@mannapur2025; @battula2025]. HiL-SG's validated query triples share the version-control principle but add the rationale metadata that semantic layers lack: not just *what* the query does, but *why* it was constructed that way.

*Traditional knowledge management* (wikis, data dictionaries, runbooks) relies on passive capture where users must stop working to document. Evidence suggests this negatively impacts participation and produces inaccurate records due to cognitive load [@mayo2016; @goffin2011]. HiL-SG instead implements active capture: the query itself is the documentation, and validation happens at the point of use rather than as a separate maintenance task [@moore2018].

*Unsupervised AI querying* represents the opposite extreme: removing human oversight entirely. Current NL2SQL accuracy levels make this unsafe for clinical analytics [@ziletti2024]. HiL-SG occupies the middle ground, using AI as the generation engine while preserving human judgment as the validation gate.
```

**Adds:** ~190 words

### Step 2.3: Replace NL2SQL "tipping point" with accuracy gradient (R4)

**File:** `paper.md` line 114
**Action:** Replace the first two sentences of Section 4.3:

**Current:**
```
NL2SQL has reached a productivity tipping point. Natural language interfaces report a 63% increase in self-service adoption and 37% reduction in retrieval time [@dadi2025].
```

**Replace with:**
```
NL2SQL technology has matured along a clear accuracy gradient: general-purpose models achieve approximately 65% execution accuracy on healthcare-specific benchmarks such as MIMICSQL; domain-adapted systems like MedT5SQL reach 80% [@marshan2024]; and architecturally specialized approaches combining LLMs with structured knowledge representations achieve over 90% on the same benchmarks. While insufficient for unsupervised clinical deployment [@ziletti2024], this gradient demonstrates that the generation engine required for HiL-SG is viable within a human-validated workflow. Natural language interfaces report a 63% increase in self-service adoption and 37% reduction in retrieval time [@dadi2025].
```

**Adds:** ~40 words net
**References to add to `references.bib`:** Graph-empowered MIMICSQL study (from original paper ref 90). Verify BibTeX key exists or create new entry.

### Step 2.4: Operationalize the Validator Paradox (R2)

**File:** `paper.md` lines 150-151
**Action:** Replace the final paragraph of Section 6 (starting "However, the Validator Paradox is not fully resolved") with:

```
However, the Validator Paradox is not fully resolved. There exists a minimum viable expertise threshold below which validation becomes meaningless. A junior analyst rubber-stamping AI-generated output without genuine comprehension provides no knowledge ratchet; the validation artifact exists, but its epistemic value is nil. Identifying this threshold remains an open empirical question; future work in this series (Paper 2) should measure it via controlled hallucination injection studies, in which AI-generated queries containing deliberate errors are presented to validators of varying experience levels.

We propose a provisional three-tier governance model to degrade gracefully when expertise is scarce. *Full validation*: a domain expert with schema-level knowledge reviews the query triple and confirms semantic alignment; this is the default mode. *Constrained validation*: when no fully qualified validator is available, a less experienced analyst reviews the triple against previously validated queries for the same data domain, flagging deviations for deferred expert review; the triple is stored with "provisional" status. *Automated regression*: for queries that match an existing validated triple with high semantic similarity, the system accepts the match without human review but logs it for periodic audit.

At the organizational level, governance requirements include defining who can validate queries (domain expertise thresholds), establishing review workflows for high-stakes queries, managing query versioning as schemas evolve, and implementing retrieval policies. To prevent conflicting definitions from democratized analytics, organizations can designate specific validated triples as "Golden Queries," certified by a governance committee as the authoritative source of truth for key metrics [@himss2025ucdavis]. While many users can create and validate queries, only these certified triples serve as official standards, mitigating Shadow IT risks while preserving analytical agility.
```

**Adds:** ~170 words net (replaces ~80 words of existing text)

### Step 2.5: Add Continuous Analytic Integration (R8)

**File:** `paper.md` after line 131 (after the ARI complements AMAM paragraph, before Table 1)
**Action:** Insert:

```
The "Schema Coupling" dimension can be operationalized through *Continuous Analytic Integration*: treating validated query triples not as static wiki entries but as software assets within a CI/CD pipeline. When a data warehouse schema is updated (e.g., a quarterly EHR upgrade), the system automatically re-runs the library of stored queries. Queries that fail or return anomalous results are flagged for review. This transforms "Institutional Memory" from a stagnant repository into a living, automated test suite that actively signals when organizational knowledge has drifted from technical reality.
```

**Adds:** ~80 words

### Step 2.6: Verify pass 2

- [ ] Word count delta check (expect ~+570 from pass 2 start)
- [ ] Total body word count check (expect ~4,110)
- [ ] Run JMIR validator: `uv run python scripts/validate_jmir_compliance.py --article-type viewpoint`
- [ ] Run reference validator: `uv run python scripts/validate_references.py --all`
- [ ] Check for any new references needed in `references.bib`
- [ ] Commit: `feat(paper): add comparative analysis, governance tiers, NL2SQL gradient, framework alignment`

---

## Pass 3: Supporting Improvements (R5, R9, R13)

**Goal:** Strengthen ARI, swap weak references, improve acknowledgments.
**Estimated net change:** +200 words

### Step 3.1: Enhance ARI with pillar rubric indicators (R5)

**File:** `paper.md` line 120
**Action:** Replace "replacing static checklists with dynamic resilience metrics" with "extending static maturity assessments with a complementary resilience dimension."

**File:** `paper.md` after line 131 / after the Continuous Analytic Integration paragraph (from step 2.5), before Table 1
**Action:** Insert:

```
For organizations seeking a broader diagnostic, these resilience dimensions can be combined with capability indicators across each pillar. For Analytics Maturity: HIMSS AMAM stage, self-service analytics penetration, and AI/NL interface deployment status. For Workforce Agility: first-year staff turnover rate, leadership tenure, knowledge concentration (how many individuals hold critical expertise), time-to-productivity for new hires, and tacit knowledge capture mechanisms. For Technical Enablement: data access modality (SQL-only vs. natural language), system interoperability, and skills gap impact. Each indicator can be scored as Low, Medium, or High Strength using evidence-based anchors from the literature reviewed in Section 4.

Both the ARI and the broader pillar assessment require psychometric development, including construct validation, inter-rater reliability testing, and discriminant validity assessment against AMAM, before organizational deployment. This development is planned as part of Paper 2.
```

**Adds:** ~130 words

### Step 3.2: Swap weak references (R9)

**File:** `references.bib`
**Actions:**

1. **Replace ref for `@oracle2024` (line 109):**
   Find a peer-reviewed healthcare turnover cost study. Candidate: Waldman JD, Kelly F, Arora S, Smith HL. "The shocking cost of turnover in health care." Health Care Management Review. 2004;29(1):2-7. Add to `references.bib` as `@waldman2004`. Update `paper.md` line 109: `[@massingham2018; @oracle2024]` -> `[@massingham2018; @waldman2004]`.

2. **Replace ref for `@dadi2025` (line 114):**
   Check if a more established NL interface survey exists. If the Dadi et al. claim (63% self-service increase, 37% retrieval reduction) is unique to this source, keep it but add a stronger corroborating reference alongside it.

3. **Replace ref for `@ogunwole2023` (line 116):**
   Replace with a mainstream software engineering source on legacy modernization if available.

- [ ] Validate all new references: `uv run python scripts/validate_references.py --all`

### Step 3.3: Update Acknowledgments (R13)

**File:** `paper.md` line 174
**Action:** If domain expert reviewers can be named, update to:

```
The author (S.T.H.) takes full responsibility for the final content, conducted the research, and verified all claims and citations. [Names] provided critical review of the healthcare informatics and knowledge management components. Gemini CLI (Gemini 3, Google) and Claude Code (Claude Opus 4, Anthropic) assisted with manuscript editing and refinement. Figures were generated using the Mermaid graph language.
```

If no external reviewers, at minimum update AI acknowledgment to reflect current tooling.

### Step 3.4: Verify pass 3

- [ ] Word count delta check (expect ~+200 from pass 3 start)
- [ ] Total body word count check (expect ~4,310)
- [ ] JMIR validator: `uv run python scripts/validate_jmir_compliance.py --article-type viewpoint`
- [ ] Reference validator: `uv run python scripts/validate_references.py --all`
- [ ] Commit: `feat(paper): enhance ARI with pillar indicators, swap weak references`

---

## Pass 4: Figures (R12, independent track)

### Step 4.1: Simplify Figure 1

**File:** `figures/architecture.mmd`
**Action:** Either:
- **Option A:** Split into two figures (data flow + knowledge infrastructure)
- **Option B:** Simplify to higher-level block diagram with fewer boxes

### Step 4.2: Increase Figure 2 font sizes

**File:** `figures/knowledge-cycle.mmd`
**Action:** Increase font sizes in flowchart boxes. Test at 50% zoom for readability.

### Step 4.3: Regenerate figures

```bash
# Regenerate PNGs from Mermaid sources
podman-compose run --rm dev ./scripts/build_paper.sh --format all
```

### Step 4.4: Verify figures

- [ ] Visual inspection at 50% zoom
- [ ] Check DPI >= 300
- [ ] Commit: `fix(paper): improve figure readability for print`

---

## Final Verification

```bash
# 1. Full word count (body only)
cat paper.md | sed '1,/^---$/d' | sed '/^# Acknowledgments/,$d' | wc -w
# Expected: ~4,310 (must be <= 5,000)

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
```

- [ ] All validators pass
- [ ] Word count <= 5,000
- [ ] No em-dashes
- [ ] PDF renders correctly with new table and sections
- [ ] Figures legible at print scale
- [ ] Build artifacts committed (may require two-stage commit per CLAUDE.md)

---

## Commit Sequence

1. `fix(paper): tighten language, reduce repetition, clarify evidence-claim boundary` (Pass 1)
2. `feat(paper): add comparative analysis, governance tiers, NL2SQL gradient, framework alignment` (Pass 2)
3. `feat(paper): enhance ARI with pillar indicators, swap weak references` (Pass 3)
4. `fix(paper): improve figure readability for print` (Pass 4)
5. `build: regenerate paper PDF and HTML` (build artifacts)

---

## Rollback Plan

Each pass is a separate commit. If word count exceeds 5,000 after any pass:
1. Check which additions pushed over the limit
2. Trim the lowest-priority addition from that pass (R8 Continuous Analytic Integration is the first cut candidate at +80 words)
3. If still over, trim the pillar rubric expansion in R5 from prose to a brief parenthetical reference to Paper 2

The 690-word buffer after all passes makes this unlikely.
