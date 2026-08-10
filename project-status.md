# Project Status

**Last updated:** 2026-08-10
**Tracking:** [GitHub Issues](https://github.com/stharrold/yuimedi-paper-20250901/issues)
**Version:** 4.0.0

---

## Paper Series Overview

| Paper | Title | Status | Target | Issues |
|-------|-------|--------|--------|--------|
| **Paper 1** | Healthcare Analytics Challenges (Viewpoint) | i-JMR: R2 submitted 2026-07-11, awaiting decision | 2026 | [paper-1](https://github.com/stharrold/yuimedi-paper-20250901/labels/paper-1) |
| **Paper 2** | Empirical Validation of HITL-KG (Synthea/GCP) | Not started | TBD | [paper-2](https://github.com/stharrold/yuimedi-paper-20250901/labels/paper-2) |
| **Paper 3** | FHIR/OMOP Interoperability + Safety | Not started | TBD | [paper-3](https://github.com/stharrold/yuimedi-paper-20250901/labels/paper-3) |

---

## Paper 1: Viewpoint (Interactive Journal of Medical Research, i-JMR)

**Status:** ACCEPTED 2026-07-13 (Decision A). Copyediting completed and approved 2026-08-10. **Publication scheduled 21.Aug.2026.**
**Manuscript ID:** ms#96541 (transferred from JMIR Medical Informatics)
**Citation:** Interact J Med Res 2026;15:e96541 | doi [10.2196/96541](https://doi.org/10.2196/96541) | https://www.i-jmr.org/2026/1/e96541
**Editor:** Matthew Balcarras | **Peer reviewers:** Moez Hamedani, Xiaoni Zhang
**Tracking:** [#551 epic](https://github.com/stharrold/yuimedi-paper-20250901/issues/551) (closed), milestone "i-JMR R2" (closed)

**History:** Submitted to JMIR Medical Informatics; desk-rejected pre-review (Decision E2, 2026-04-17); transferred to i-JMR (2026-04-22); externally peer-reviewed; major revision (Decision D, 2026-06-05); R1 resubmitted 2026-06-15; minor revision (Decision B, 2026-07-07; both reviewers signed off on content); R2 submitted 2026-07-11 (system file 96541-1518835-1-ED.docx); accepted 2026-07-13; copyedited and approved 2026-08-10.

| Metric | Value |
|--------|-------|
| Word count (JMIR method) | 5,065 / 5,000 (overage accepted by the copyeditor) |
| References | 84 (59 DOI-verified; 24 no-DOI entries title-verified 2026-08-10, 5 corrected) |
| Figures | 2 (regenerated 2026-08-10 for sentence case and "health care") |
| Tables | 2 in-text (bordered) + rubric in Multimedia Appendix 2 |
| Multimedia appendices | 2 |
| JMIR compliance | Pass except word count (accepted deviation; commit with `SKIP=validate-jmir-compliance`) |

**Copyediting round (2026-08-10, all queries resolved, package `ARCHIVED/20260810_IJMR-Copyediting/`):**
- [x] Defined the 3 pillars at first use in the body; named the conversational AI at first use
- [x] "healthcare" to "health care" throughout (HIMSS legal name preserved; bibliography exempt)
- [x] AMAM expansion corrected to the current HIMSS name, "Analytics Maturity Assessment Model"
- [x] Both figures regenerated: sentence case, "Health care database", plus signs replaced with "and", "3 pillars"
- [x] JMIR data availability template 4 adopted, code deposit disclosure retained
- [x] 5 bibliography corrections from a sweep of all no-DOI entries
- [x] Reply to copyeditor archived at `20260810_Email-Reply_IJMR-96541_Copyediting.txt`

**Remaining (post-publication, non-blocking):**
- [ ] Style sync `paper.md` to the published version (numerals, lowercase coined terms) after 2026-08-21
- [ ] Propagate the title change to `CITATION.cff`, `.zenodo.json`, `README.md` at the next release
- [ ] Repair 11 stale `file =` paths in `references.bib` (library reorganized its directory naming)
- [ ] JMIR visual abstract: draft expected late Aug 2026, ONE author review round

**R2 revision status (all Decision-B items resolved and submitted):**
- [x] Editor: length (5,430 -> 4,990 under JMIR's counting method; rubric to Appendix 2)
- [x] Editor: reference DOI audit (8 corrected, 9 added, 2 duplicates removed, 7 removed/replaced, 29 author corrections)
- [x] Editor: table/figure formatting (bordered Table style; numbered captions)
- [x] Reviewer T: figure captions + footnotes
- [x] Reviewer Q: future-work directions mapped to Conclusion + planned companion study
- [x] Submission package of record: `ARCHIVED/20260712_IJMR-Submission/`
- [x] Released as v4.0.0 (Zenodo archival verified)
- [ ] Author action: archive the confirmation email; rate reviewers via the Decision-B links

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
