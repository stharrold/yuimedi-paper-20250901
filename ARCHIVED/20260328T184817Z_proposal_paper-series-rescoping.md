# Proposal: Paper Series Rescoping

**Date:** 2026-03-28
**Problem:** Paper 2 has 26 open issues spanning 3 distinct scopes, making it too broad for a single publication.

---

## Current State

**CLAUDE.md defines the series as:**
- Paper 1 (Viewpoint): Theoretical framework (resubmitting to JMIR ms#91493)
- Paper 2: Empirical validation (Synthea/GCP)
- Paper 3: FHIR/OMOP interoperability

**Paper 1 defers three things to "Paper 2":**
1. Empirical validation of HiL-SG framework
2. ARI psychometric development
3. Validator Paradox threshold measurement via hallucination injection studies

**Paper 2 issues actually span three clusters:**

### Cluster A: Reference Implementation & Benchmarking (original Paper 2 scope)
| Issue | Title | Priority |
|-------|-------|----------|
| #328 | Download and configure Synthea SyntheticMass dataset | P0 |
| #329 | Design GCP architecture (Vertex AI, BigQuery, Cloud Functions) | P0 |
| #330 | Load Synthea data to BigQuery | P1 |
| #331 | Implement query memoization system | P0 |
| #332 | Implement institutional learning loop | P0 |
| #333 | Define cache hit rate metrics | P1 |
| #337 | Setup open-source repository | P1 |
| #338 | Design empirical validation framework | P0 |
| #339 | Create test query set (50+ queries) | P1 |
| #340 | Execute benchmarking experiments | P0 |
| #341 | Statistical analysis for Paper 2 | P1 |
| #342 | Quantify success metrics | P1 |
| #343 | Draft Paper 2 manuscript | P1 |
| #344 | Paper 2 expert review | P2 |
| #375 | Literature review: Synthea and synthetic data | P2 |

**15 issues. This is a full paper.**

### Cluster B: Clinical Safety & Security
| Issue | Title | Priority |
|-------|-------|----------|
| #334 | Add Clinical Safety Considerations section | P0 |
| #335 | Add Security Architecture section | P0 |
| #336 | Reference security standards (NIST, HITRUST, HIPAA) | P1 |
| #374 | Literature review: Clinical safety and security | P1 |

**4 issues. Could be a standalone section in Paper 2 or Paper 3, or expanded to its own paper.**

### Cluster C: Theoretical/Terminology (may be resolved by Paper 1)
| Issue | Title | Priority | Status |
|-------|-------|----------|--------|
| #325 | Literature review: Knowledge portal paradigm | P0 | Paper 1 uses "Validated Query Triple" instead |
| #326 | Replace terminology: Conversational AI -> Healthcare Knowledge Portal | P1 | Paper 1 uses "HiL-SG" terminology throughout |
| #327 | Add theoretical grounding: SECI model | P1 | **Already done in Paper 1** (6 SECI references) |
| #369 | Literature review: Institutional learning metrics | P2 | Research file exists |

**4 issues. #327 is done. #325 and #326 are terminology decisions that Paper 1 has superseded. #369 is research.**

### Cross-Paper Issues
| Issue | Title | Labels |
|-------|-------|--------|
| #353 | Draft Paper 3 manuscript | paper-2, paper-3 |
| #355 | Extend Paper 2 codebase for Paper 3 | paper-2, paper-3 |
| #371 | Add competing interests disclosure | paper-1, paper-2 |

**3 issues. #371 is already done in Paper 1. #353 and #355 are Paper 3 scope.**

---

## Proposed Rescoping

### Paper 2: "Empirical Validation of HiL-SG Using Synthetic Healthcare Data"
**Focus:** Build it, benchmark it, measure it.

**Keep (Cluster A core):**
- #328, #329, #330 (Synthea/GCP infrastructure)
- #331, #332, #333 (query memoization / institutional learning)
- #337 (open-source repository)
- #338, #339, #340, #341 (empirical validation framework + benchmarking)
- #342 (quantify success metrics)
- #343, #344 (manuscript + review)
- #375 (Synthea literature review)

**Add (new issues for Paper 1 deferrals that fit Paper 2's empirical scope):**
- ARI pilot validation: score 3-5 organizations using the ARI dimensions, report inter-rater agreement. Not full psychometric development, but enough to demonstrate feasibility.
- Hallucination injection study: embedded in the benchmarking experiments (#340). Present deliberately erroneous AI-generated queries to validators, measure detection rates by expertise level.

**Move to Paper 3:**
- #334, #335, #336, #374 (Clinical safety & security cluster). Safety is best addressed after the reference implementation exists and can be evaluated against safety criteria. Paper 3's FHIR/OMOP focus naturally leads to regulatory/compliance/safety discussions.
- #353, #355 (already labeled paper-3)

**Close or relabel:**
- #327 (SECI model): **Close.** Already done in Paper 1. Add comment referencing Paper 1 Section 2.
- #325 (Knowledge portal paradigm): **Relabel to paper-2 only.** The terminology decision is made (HiL-SG), but the knowledge portal literature review may inform Paper 2's architecture design.
- #326 (Replace terminology): **Close.** Paper 1 establishes HiL-SG terminology; Paper 2 inherits it.
- #371 (Competing interests): **Close for paper-2 label.** Already done in Paper 1. Paper 2 will need its own COI but that's part of #343 (draft manuscript).
- #369 (Institutional learning metrics): **Keep on paper-2.** Research file exists; relevant to #332 and #333.

### Paper 3: "FHIR/OMOP Interoperability and Safety Governance for HiL-SG"
**Focus:** Standards compliance, interoperability, clinical safety.

**Inherits:**
- #334, #335, #336, #374 (safety & security)
- #353 (draft Paper 3 manuscript)
- #355 (extend Paper 2 codebase for FHIR/OMOP)
- #330 (Synthea data loading, shared with Paper 2)

**Rationale for moving safety to Paper 3:**
- Safety evaluation requires a working system to evaluate (Paper 2 builds it)
- FHIR/OMOP interoperability inherently involves regulatory compliance contexts
- Separating safety from benchmarking keeps Paper 2 focused on "does it work?" while Paper 3 asks "is it safe and standards-compliant?"

### Full Psychometric ARI Validation: Deferred (Paper 4 or standalone)
Full construct validation, inter-rater reliability, discriminant validity against AMAM requires multi-site data collection and is a psychometric methods paper, not a systems paper. Paper 1 proposes the ARI; Paper 2 pilots it; full validation is a separate study.

**Paper 1's current language ("This development is planned as part of Paper 2") should be softened to "This development is planned for future work in this series."**

---

## Summary of Issue Actions

| Issue | Action | Rationale |
|-------|--------|-----------|
| #325 | Keep paper-2 | Knowledge portal lit review informs architecture |
| #326 | **Close** | Terminology decided in Paper 1 (HiL-SG) |
| #327 | **Close** | SECI model already in Paper 1 |
| #328-333 | Keep paper-2 | Core scope |
| #334-336 | **Move to paper-3** | Safety after implementation |
| #337-342 | Keep paper-2 | Core scope |
| #343-344 | Keep paper-2 | Manuscript/review |
| #353, #355 | **Remove paper-2 label** | Already paper-3 |
| #369 | Keep paper-2 | Supports #332/#333 |
| #371 | **Close** | Done in Paper 1 |
| #374 | **Move to paper-3** | Safety literature |
| #375 | Keep paper-2 | Synthea literature |
| (new) | **Create** on paper-2 | ARI pilot validation |
| (new) | **Create** on paper-2 | Hallucination injection study (part of #340) |

**Net result:** Paper 2 goes from 26 issues to ~18 focused issues. Paper 3 gains 5 issues.

---

## Paper 1 Text Change Required

In `paper.md` line 158, change:
> "This development is planned as part of Paper 2."

To:
> "This development is planned for future work in this series."

This avoids over-promising what Paper 2 will deliver for ARI psychometrics.
