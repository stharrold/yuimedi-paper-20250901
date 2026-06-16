# i-JMR R1 Major Revision Plan (ms#96541)

**Decision:** D (major revision & re-review), Interactive Journal of Medical Research
**Editor:** Matthew Balcarras, PhD
**Received:** 2026-06-05 | **Revision due:** 2026-07-03 (extendable once)
**Source:** `ARCHIVED/20260329_JMIR-Submission/20260605_Editor_Author Correspondence_Major-Revisions-Required.pdf`

This is **not** a rejection. The paper passed external peer review at i-JMR and has a concrete path to acceptance. Two reviewers (Q skeptical, T constructive) plus an editor formatting checklist.

## Key strategic notes

1. **IMRD vs Viewpoint contradiction.** Editor's checklist demands subheadings under Introduction/Methods/Results/Discussion, but i-JMR's own Viewpoint spec forbids "Methods"/"Results" headings (`standards/jmir_submission_article-types.md`). Handle via response-letter pushback citing the article-type rule, *not* by restructuring.
2. **Citation style flip.** i-JMR requires numbered Vancouver square brackets `[1]`. Repo currently uses pandoc author-year `[@key]` + AMA CSL. This is the largest mechanical change; touches `paper.md`, the CSL, `validate_jmir_compliance.py`, and the build.
3. **The 2004 stat = three reviewer points at once.** `@ang2004` at `paper.md:41` and `paper.md:136` is flagged by T#2 (redundancy), T#4 (outdated), Q#6 (>20yr). Consolidate to one location + add 2020+ contemporary evidence alongside (keep the rhetorical "still-a-benchmark" framing).
4. **Q#3 is the strongest threat** (does HITL beat LLMs?). It is exactly the Paper 2 empirical premise. Frame Viewpoint claims as prescriptive-pending-validation; cite existing human-AI error-correction evidence.

## Issue set

### EPIC (tracking)
- **[i-JMR R1] Major revision tracking — ms#96541 (due 2026-07-03)** — checklist linking all child issues; holds response-letter status.

### Group A — Editor compliance (P0-Critical, blocks resubmission)
| ID | Title | Files | Notes |
|----|-------|-------|-------|
| A1 | Convert in-text citations to numbered Vancouver square-bracket style | paper.md, CSL, validate_jmir_compliance.py, build_paper.sh | Swap AMA CSL → numbered (e.g. JMIR/Vancouver CSL); reverify all artifacts |
| A2 | Add mandatory generative-AI disclosure statement | paper.md | Editor-required; currently missing |
| A3 | Verify Funding Statement uses exact required wording | paper.md:238 | Section exists; confirm "The authors declared no financial support was received for this work." distinct from Acknowledgments |
| A4 | Heading/emphasis compliance pass (no numbered headings; no italics/bold as pseudo-subheadings; no single-subheading sections) | paper.md | Reconcile IMRD demand via response letter, not restructure |

### Group B — Reviewer substantive content (P1-High)
| ID | Src | Title | Files |
|----|-----|-------|-------|
| B1 | Q1 | Address self-selection bias in maturity (HIMSS) data; define acronyms at first use | paper.md |
| B2 | Q2 | Add scope conditions: query volume/diversity/frequency; when HITL-KG warranted vs simple documentation | paper.md |
| B3 | Q3 | Frame HITL-vs-LLM efficacy as prescriptive-pending-Paper-2; cite human-AI error-correction evidence | paper.md |
| B4 | Q4 | Address data drift vs expert tenure; add training/awareness as complementary levers | paper.md |
| B5 | T1 | Define the three title constructs (analytics maturity, workforce agility, technical enablement) with cited definitions | paper.md, references.bib |
| B6 | T2 | Consolidate duplicated 2004/tenure stats (paper.md:41 & :136) | paper.md |
| B7 | T3 | Figure 1: add Step 7 (organizational memory) → Step 1 (knowledge base) feedback loop | figures/*.mmd |
| B8 | T4/Q6 | Add contemporary (2020+) tenure evidence alongside @ang2004; replace other >20yr refs | paper.md, references.bib |
| B9 | T-min/ed | Complete bibliographic metadata (volume/issue/pages/DOI) for all references | references.bib |

### Group C — Research support (research, P1/P2; the parallelizable fan-out)
| ID | Title | Feeds |
|----|-------|-------|
| C1 | Recent (2020+) healthcare IT/informatics tenure & turnover evidence | B6, B8 |
| C2 | Cited scholarly definitions: analytics maturity, workforce agility, technical enablement | B5 |
| C3 | Evidence on human-in-the-loop detection/correction of LLM/AI errors | B3 |

### Group D — Process & housekeeping
| ID | Title | Files |
|----|-------|-------|
| D1 | Compile point-by-point response-to-reviewers letter | docs/ (new) |
| D2 | Update records to i-JMR R1 status; close/relabel #506; update project-status.md, CLAUDE.md, memory | repo meta |

## Dependencies
- C1→B6/B8, C2→B5, C3→B3 (research precedes content edits)
- A1 (citation flip) should land after content edits B5–B9 settle (avoid re-numbering churn)
- D1 compiled last; D2 can happen immediately

## Word budget
Body limit 5,000. Current draft ~3,600. Additions (B1–B5) must stay within budget; offset via B6 de-duplication.
