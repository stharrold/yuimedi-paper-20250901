# Implementation Plan: Replace ARI with Three-Pillar Assessment

**Date:** 2026-03-29
**Target file:** `paper.md`
**Rationale:** The Analytics Resilience Index (ARI) is the paper's weakest artifact: underdeveloped (4 abstract dimensions, no validation), competes with 23 existing instruments (Ignatowicz 2023), and doesn't map to the paper's three-pillar framework. The Three-Pillar Assessment from the original submission (Table 4, pp36-38) is more concrete, directly aligned with the framework, and less vulnerable to reviewer critique.

---

## Scope of Change

### What's being replaced

The entire Section 5 ("The Analytics Resilience Index") including:
- Section 5.1 "Why Resilience, Not Maturity" (line 146-148)
- Section 5.2 "Operationalizing the ARI" (lines 150-158)
- Table 2: ARI dimensions (lines 160-167)
- Continuous Analytic Integration paragraph (line 154)
- Resilience literature positioning (line 156)
- All "ARI" references throughout the paper (abstract, limitations, future research, abbreviations)

### What's being added

- Renamed Section 5: "Organizational Self-Assessment: The Three-Pillar Rubric"
- Three-Pillar Assessment Rubric table (condensed from original Table 4)
- Brief convergence assessment description
- Continuous Analytic Integration paragraph (moved, not lost)

### What's being preserved

- The "why resilience, not maturity" argument (valuable, just reframed)
- Continuous Analytic Integration concept (moved into Section 3 or kept in Section 5)
- Resilience literature citations (Ignatowicz, Ratliff, Ellis -- repositioned)
- The AMAM complementarity argument

---

## Word Budget

| Item | Words |
|------|-------|
| Current body word count | ~4,726 |
| Current Section 5 (to remove) | ~450 |
| New Section 5 (to add) | ~350 |
| Other edits (abstract, limitations, future research, abbreviations) | net -20 |
| **Estimated final** | **~4,606** |
| JMIR limit | 5,000 |

---

## Step 1: Replace Section 5 heading and intro

**Current (lines 142-144):**
```
# The Analytics Resilience Index

To measure success, we propose the **Analytics Resilience Index (ARI)**, extending static maturity assessments with a complementary resilience dimension.
```

**Replace with:**
```
# Organizational Self-Assessment

To operationalize the framework, we propose a **Three-Pillar Assessment Rubric** (Table 2) that enables healthcare organizations to evaluate their current position across each pillar and identify compounding vulnerabilities.
```

## Step 2: Replace Section 5.1 "Why Resilience, Not Maturity"

**Current (lines 146-148):** Full paragraph about AMAM assuming linear progression, resilience vs maturity distinction.

**Replace with:**
```
## Why Assessment, Not Just Maturity

Existing maturity models such as AMAM, the DIKW hierarchy, and established knowledge management frameworks (see Table 1) assume linear progression through discrete stages and implicitly presuppose a stable workforce [@himss2024; @wang2018]. In practice, an organization that reaches AMAM Stage 5 but regresses to Stage 3 after the departure of two senior analysts has not failed to mature; it has failed to be *resilient*. The Three-Pillar Assessment addresses this gap by measuring not just where an organization stands, but how vulnerable it is to the compounding effects identified in Section 1. A recent systematic review identified 23 distinct organizational resilience instruments applied in health facilities, yet found no consensus on what to measure [@ignatowicz2023]. Only four instruments have been developed specifically for healthcare, and only two have been validated [@ratliff2025]. The Three-Pillar Assessment extends this tradition by organizing indicators around the specific domains where institutional amnesia operates.
```

## Step 3: Replace Section 5.2 and Table 2

**Current (lines 150-167):** "Operationalizing the ARI" + Continuous Analytic Integration + resilience literature + ARI table (4 dimensions).

**Replace with:**
```
## The Three-Pillar Rubric

Each indicator is scored as Low, Medium, or High Strength using evidence-based anchors from the literature reviewed in Section 4. Organizations scoring predominantly "Low Strength" across multiple pillars face the self-reinforcing degradation cycle that the framework identifies as the central threat.

**Pillar 1: Analytics Maturity**

| Indicator | Low Strength | Med. Strength | High Strength | Evidence |
|:---|:---|:---|:---|:---|
| HIMSS AMAM Stage | Stages 0-2: Fragmented data, limited reporting | Stages 3-4: Integrated warehouse, standardized definitions | Stages 5-7: Predictive analytics, AI integration | [@himss2024; @himss2024news] |
| Self-service analytics | None; all analytics require IT intervention | Partial; BI tools available but underutilized | Widespread; clinical staff access data directly | [@health2020; @shahbaz2019] |
| AI/NL interface | No NL2SQL or conversational analytics | Pilot programs or evaluation underway | Natural language query capability deployed | [@ziletti2024; @yuan2019] |

**Pillar 2: Workforce Agility**

| Indicator | Low Strength | Med. Strength | High Strength | Evidence |
|:---|:---|:---|:---|:---|
| First-year staff turnover | >30% (High instability) | 15-30% | <15% (High stability) | [@nsi2025] |
| Leadership stability (CIO) | Tenure < 3 years | Tenure 3-5 years | Tenure > 5 years | [@wittkieffer2024] |
| Knowledge concentration | Critical expertise held by 3 or fewer individuals | Partial documentation; some cross-training | Distributed expertise; documented processes | [@massingham2018; @foss2007] |

**Pillar 3: Technical Enablement**

| Indicator | Low Strength | Med. Strength | High Strength | Evidence |
|:---|:---|:---|:---|:---|
| Data access | SQL/technical expertise required for all queries | IT queue for complex queries; basic self-service | Natural language or visual query interfaces | [@shahbaz2019; @yuan2019] |
| Schema coupling | Hard-coded reports break on schema change | Partial semantic layer; some automated feeds | Semantic layer adapts; CI/CD detects drift | [@mannapur2025; @battula2025] |

: Three-Pillar Organizational Assessment Rubric. \label{tab:rubric}

The "Schema Coupling" indicator can be operationalized through *Continuous Analytic Integration*: treating validated query triples as software assets within a CI/CD pipeline [@valiaiev2025]. When a data warehouse schema is updated, the system automatically re-runs stored queries and flags failures, transforming institutional memory into a living test suite [@betha2023; @kottam2025].

The rubric complements rather than replaces AMAM. Where AMAM measures the sophistication of analytical capabilities at a point in time, the Three-Pillar Assessment reveals how vulnerable those capabilities are to the compounding effects of turnover, low maturity, and technical barriers. Used together, they provide a two-dimensional view of analytics health.
```

## Step 4: Update abstract (line 11)

**Current:**
```
The accompanying Analytics Resilience Index (ARI) proposes a measurement instrument that extends static maturity assessments with a complementary resilience dimension, quantifying an organization's ability to sustain analytical capability despite staff churn.
```

**Replace with:**
```
The accompanying Three-Pillar Assessment Rubric provides a structured self-assessment tool that enables organizations to identify compounding vulnerabilities across analytics maturity, workforce agility, and technical enablement.
```

## Step 5: Update Limitations (line 196)

**Current:**
```
The HITL-KG architecture and the proposed Analytics Resilience Index (ARI) are conceptual artifacts
```

**Replace with:**
```
The HITL-KG architecture and the proposed Three-Pillar Assessment Rubric are conceptual artifacts
```

## Step 6: Update Future Research (line 202)

**Current:**
```
Future research should empirically validate and refine the HITL-KG framework and the proposed Analytics Resilience Index. Priority questions include: how ARI scores correlate with observed continuity of analytics performance during leadership and staff turnover;
```

**Replace with:**
```
Future research should empirically validate and refine the HITL-KG framework and the proposed Three-Pillar Assessment Rubric. Priority questions include: how pillar scores correlate with observed continuity of analytics performance during leadership and staff turnover;
```

## Step 7: Update Abbreviations

**Remove:**
```
ARI: Analytics Resilience Index
```

**No new abbreviation needed** (Three-Pillar Assessment Rubric is not abbreviated).

## Step 8: Update references needed in Table 2

All citations in the new table already exist in `references.bib`:
- `@himss2024`, `@himss2024news`, `@health2020`, `@shahbaz2019`
- `@ziletti2024`, `@yuan2019`, `@nsi2025`, `@wittkieffer2024`
- `@massingham2018`, `@foss2007`, `@mannapur2025`, `@battula2025`
- `@valiaiev2025`, `@betha2023`, `@kottam2025`

No new references needed.

**References that may become unused after removing ARI:**
- `@ignatowicz2023` -- kept (used in new Section 5.1)
- `@ratliff2025` -- kept (used in new Section 5.1)
- `@ellis2026` -- **may become unused** if not referenced elsewhere. Check and remove from bib if so.

## Step 9: Verify

```bash
# Word count
cat paper.md | sed '1,/^---$/d' | sed '/^# Acknowledgments/,$d' | wc -w

# JMIR compliance
uv run python scripts/validate_jmir_compliance.py --article-type viewpoint

# No ARI references remain
grep -n 'ARI\b' paper.md

# No orphaned references
grep -o '@[a-zA-Z0-9_]*' paper.md | sort -u | while read ref; do
  key="${ref#@}"; grep -q "{${key}," references.bib || echo "MISSING: $key"
done

# Rebuild
./scripts/build_paper.sh --format all
```

## Step 10: Commit

```
feat(paper): replace ARI with Three-Pillar Assessment Rubric

The Analytics Resilience Index (4 abstract dimensions, no validation)
was the paper's weakest artifact. The Three-Pillar Assessment Rubric
from the original submission is more concrete (11 indicators with
evidence-based anchors), directly maps to the paper's framework,
and is less vulnerable to "where's your validation?" critique.

Refs #506
```

---

## Risks

1. **Word count**: New table is longer than old table, but surrounding prose is shorter. Net change should be roughly neutral.
2. **Original paper reference numbers**: The citations in the original Table 4 use the original paper's numbering. All must be mapped to current `references.bib` keys.
3. **Ellis 2026 may become orphaned**: Check if it's still cited after removing ARI resilience literature paragraph. If not, remove from bib.
4. **GitHub issue #513** ("ARI pilot validation"): Should be updated to reference Three-Pillar Assessment instead of ARI.
