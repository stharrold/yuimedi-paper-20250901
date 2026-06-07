# Project Status

**Last updated:** 2026-06-07
**Tracking:** [GitHub Issues](https://github.com/stharrold/yuimedi-paper-20250901/issues)
**Version:** 2.0.0

---

## Paper Series Overview

| Paper | Title | Status | Target | Issues |
|-------|-------|--------|--------|--------|
| **Paper 1** | Healthcare Analytics Challenges (Viewpoint) | i-JMR: R1 major revision (due 2026-07-03) | 2026 | [paper-1](https://github.com/stharrold/yuimedi-paper-20250901/labels/paper-1) |
| **Paper 2** | Empirical Validation of HITL-KG (Synthea/GCP) | Not started | TBD | [paper-2](https://github.com/stharrold/yuimedi-paper-20250901/labels/paper-2) |
| **Paper 3** | FHIR/OMOP Interoperability + Safety | Not started | TBD | [paper-3](https://github.com/stharrold/yuimedi-paper-20250901/labels/paper-3) |

---

## Paper 1: Viewpoint (Interactive Journal of Medical Research, i-JMR)

**Status:** Major revision (Decision D), revisions complete; pending author resubmission
**Manuscript ID:** ms#96541 (transferred from JMIR Medical Informatics)
**Revision due:** 2026-07-03 (extendable once)
**Tracking:** [#529 epic](https://github.com/stharrold/yuimedi-paper-20250901/issues/529), milestone "i-JMR R1"

**History:** Submitted to JMIR Medical Informatics; desk-rejected pre-review (Decision E2, 2026-04-17); transferred to i-JMR (2026-04-22); externally peer-reviewed; major revision returned (Decision D, 2026-06-05).

| Metric | Value |
|--------|-------|
| Word count (validator) | 4,469 / 5,000 |
| References | 89 |
| Figures | 2 |
| Tables | 2 |
| JMIR compliance | Pass |

**R1 revision status (all reviewer/editor points addressed and verified in built artifacts):**
- [x] Reviewer Q (self-selection bias + acronyms, query reuse, HITL-vs-LLM, drift/training, refresh refs)
- [x] Reviewer T (define constructs, de-duplicate, Figure 1 feedback loop, replace 2004 stat, complete metadata)
- [x] Editor (in-text square-bracket citations, no numbered headings, funding statement, generative-AI disclosure)
- [x] Artifacts rebuilt and verified end-to-end (DOCX + PDF)
- [x] Point-by-point response letter drafted (`docs/20260607_i-jmr-r1-response-to-reviewers.md`)
- [ ] Author action: upload clean DOCX + tracked-changes supplementary file, paste response letter, resubmit

---

## Paper 2: Empirical Validation (Synthea/GCP)

**Status:** Not started (19 open issues)
**Scope:** Build reference implementation, benchmark HITL-KG, pilot Three-Pillar Assessment
**Rescoping doc:** `ARCHIVED/20260328T184817Z_proposal_paper-series-rescoping.md`

### Dependencies (execution order)

```
Phase 1: Infrastructure
  #328 Download Synthea dataset
  #329 Design GCP architecture
  #330 Load Synthea to BigQuery
  #337 Setup open-source repository

Phase 2: Implementation
  #331 Query memoization system
  #332 Institutional learning loop
  #333 Cache hit rate metrics
  #325 Knowledge portal lit review (informs architecture)

Phase 3: Validation
  #338 Design empirical validation framework
  #339 Create test query set (50+ queries)
  #340 Execute benchmarking experiments
  #513 Three-Pillar Assessment pilot (3-5 orgs)
  #514 Hallucination injection study

Phase 4: Analysis & Writing
  #341 Statistical analysis
  #342 Quantify success metrics
  #343 Draft manuscript
  #344 Expert review

Research (parallel):
  #369 Institutional learning metrics lit review
  #375 Synthea/synthetic data lit review
```

---

## Paper 3: FHIR/OMOP + Safety

**Status:** Not started (17 open issues)
**Depends on:** Paper 2 reference implementation
**Scope:** FHIR/OMOP interoperability, clinical safety, security governance

Key issues: #334 (clinical safety), #335 (security architecture), #346 (mapping architecture), #348 (query translation layer)

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-28 | Rename HiL-SG to HITL-KG | Industry-standard acronym; "knowledge governance" is established field (Foss 2007) |
| 2026-03-29 | Replace ARI with Three-Pillar Assessment Rubric | ARI was underdeveloped; rubric maps directly to framework, more concrete |
| 2026-03-28 | Rescope Paper 2 (26 to 19 issues) | Move safety/security to Paper 3; close issues already done in Paper 1 |
| 2026-03-28 | Prescriptive Viewpoint stance | Descriptive framing too hedging for a Viewpoint article |
| 2026-03-28 | Restore original title | Match JMIR ms#91493, AJE visual abstract, video byte |
