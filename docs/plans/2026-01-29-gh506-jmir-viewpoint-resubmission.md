# GH#506: Resubmit Paper 1 to JMIR Medical Informatics (Viewpoint, ≤5000 words) Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform the current `paper.md` (~2,549 body words, IMRD structure) into a JMIR Viewpoint article (~4,000-5,000 body words) with descriptive headers, unstructured abstract, and strengthened content selectively reincorporated from the archived long version.

**Architecture:** The paper is restructured from IMRD (Introduction/Methods/Results/Discussion) to descriptive thematic sections as required by JMIR Viewpoint rules. Content expansion draws from `ARCHIVED/20260115_JMIR-Submission/paper.md` (the rejected ~12,730-word version) and from the `../library` knowledge graph for updated workforce statistics. The JMIR compliance validator (`scripts/validate_jmir_compliance.py`) is updated to support Viewpoint article type validation.

**Tech Stack:** Markdown (paper.md), YAML (metadata.yaml), Python (validate_jmir_compliance.py), BibTeX (references.bib), Pandoc, uv

---

## Context for Implementer

### Key files

| File | Role |
|------|------|
| `paper.md` | Current paper (~2,549 body words). **This is the file you edit.** |
| `metadata.yaml` | Pandoc frontmatter. Must reflect Viewpoint type. |
| `ARCHIVED/20260115_JMIR-Submission/paper.md` | Rejected long version (~12,730 words). Source for content reincorporation. |
| `references.bib` | BibTeX bibliography. May need new entries. |
| `scripts/validate_jmir_compliance.py` | JMIR compliance checks. Must be updated for Viewpoint rules. |
| `standards/jmir_submission_article-types.md` | JMIR Viewpoint spec (lines 60-73). |
| `standards/jmir_submission_maximum-word-count.md` | Word count policy. |

### JMIR Viewpoint constraints (non-negotiable)

1. **No "Methods" or "Results" headings.** Use descriptive section headers only.
2. **Unstructured abstract** (max 450 words). No Background/Objective/Methods/Results/Conclusions headers.
3. **Max 5,000 words** (strongly recommended). Excludes abstract, references, figures, tables, abbreviations, acknowledgments, author contributions, data availability, funding.
4. **Evidence-based opinion** citing peer-reviewed literature. Consider counterarguments.
5. **No IMRD structure.** Descriptive headers that organize content by theme.

### Writing rules (from CLAUDE.md)

- No em-dashes. Use commas, colons, semicolons, or parentheses.
- Citations: `[@key]`, multiple: `[@key1; @key2]`
- Framework is **descriptive** (reveals interconnections), not **prescriptive**
- Conversational AI is a "Governance Forcing Function," not a standalone solution

### Word budget

Current body: ~1,928 words (excluding frontmatter + end sections).
Target body: 4,000-5,000 words.
Budget to add: ~2,000-3,000 words across Tasks 3-8.

---

## Phase 1: Structural Compliance

### Task 1: Update JMIR compliance validator for Viewpoint

The current `validate_jmir_compliance.py` enforces IMRD structure and structured abstracts, which are **wrong for Viewpoint**. Update it before making paper changes so we can validate continuously.

**Files:**
- Modify: `scripts/validate_jmir_compliance.py`
- Test: `uv run python scripts/validate_jmir_compliance.py` (manual run)

**Step 1: Write a failing test by running the current validator**

Run: `uv run python scripts/validate_jmir_compliance.py`

Expected: Currently passes (IMRD is present). After paper restructuring it will fail. We need to make validator Viewpoint-aware first.

**Step 2: Add `--article-type` flag and Viewpoint validation mode**

Modify `scripts/validate_jmir_compliance.py` to:

1. Add a CLI argument: `--article-type {original,review,viewpoint}` (default: `viewpoint` for this project).
2. In `validate_abstract_structure()`: When article_type is `viewpoint`, check that the abstract does **NOT** contain structured headers (`**Background:**`, etc.). Check word count is ≤450. Return valid if abstract is a single flowing paragraph.
3. In `validate_imrd_structure()`: When article_type is `viewpoint`, **invert the check**: FAIL if `# Methods` or `# Results` headings are present. PASS if they are absent.
4. Add `validate_word_count()`: Count words in body text (between end of YAML frontmatter `---` and `# Acknowledgments`). FAIL if >5,000.
5. Add `validate_no_imrd_headers()`: For Viewpoint, check that none of `# Methods`, `# Results`, `# Discussion` appear as H1 headers. Warn on `# Introduction` (acceptable but not required).

**Step 3: Run updated validator against current paper**

Run: `uv run python scripts/validate_jmir_compliance.py --article-type viewpoint`

Expected: FAIL on structured abstract and IMRD headers. This confirms the validator correctly detects Viewpoint violations.

**Step 4: Commit**

```bash
git add scripts/validate_jmir_compliance.py
git commit -m "feat(scripts): update JMIR validator for Viewpoint article type

Add --article-type flag with viewpoint mode that checks:
- Unstructured abstract (no section headers)
- No IMRD headings (Methods/Results/Discussion forbidden)
- Body word count ≤5,000

Closes part of #506"
```

---

### Task 2: Convert paper structure from IMRD to descriptive headers

**Files:**
- Modify: `paper.md` (YAML frontmatter + H1 headers)
- Modify: `metadata.yaml` (title, article type)
- Reference: `ARCHIVED/20260115_JMIR-Submission/paper.md` (for long-version structure ideas)

**Step 1: Rewrite the YAML frontmatter abstract as unstructured**

Replace the current structured abstract (with `**Background:**`, `**Objective:**`, etc.) with a single flowing narrative abstract. Keep it ≤450 words.

The unstructured abstract should cover:
- The problem (Institutional Amnesia, Triple Threat, workforce stats)
- The theoretical lens (SECI model, Socialization Failure)
- The proposed solution (HiL-SG, Validated Query Triples)
- The key insight (Validator Paradox resolved via Standard Work)
- The measurement approach (ARI)

Remove the `version:` field from YAML frontmatter (not needed for journal submission).

**Step 2: Replace IMRD H1 headers with descriptive headers**

Replace the current H1 structure:
```
# Introduction
# Methods
# Results
# Discussion
# Conclusion
```

With descriptive Viewpoint headers:
```
# The Triple Threat: Institutional Amnesia in Healthcare Analytics
# Theoretical Grounding: SECI and the Unstable Workforce
# Human-in-the-Loop Semantic Governance
# The Evidence Base: Three Pillars
# The Analytics Resilience Index
# The Validator Paradox and Standard Work
# Safety as Cognitive Forcing
# Structural Barriers: Why the Problem Persists
# Limitations
# Implications and Future Research
```

Keep all existing content under each section. Move content from old headers to new ones logically:
- `# Introduction` content → `# The Triple Threat: Institutional Amnesia in Healthcare Analytics`
- `# Methods` content (DSR paragraph) → Integrate briefly into the "Theoretical Grounding" section as a methodological note, not a standalone section
- `# Results` subsections → Distribute across `# Theoretical Grounding`, `# Human-in-the-Loop Semantic Governance`, `# The Evidence Base`, `# The Analytics Resilience Index`
- `# Discussion` subsections → `# The Validator Paradox and Standard Work`, `# Safety as Cognitive Forcing`, `# Structural Barriers`
- `# Conclusion` → `# Implications and Future Research`

**Step 3: Update `metadata.yaml`**

- Change `title:` to match `paper.md` YAML frontmatter title
- Ensure `header-left:` reflects new short title

**Step 4: Run the Viewpoint validator**

Run: `uv run python scripts/validate_jmir_compliance.py --article-type viewpoint`

Expected: Abstract check PASS (unstructured). IMRD check PASS (no forbidden headers). Word count PASS (still ~1,928 words, well under 5,000).

**Step 5: Build paper to verify rendering**

Run: `./scripts/build_paper.sh --format all`

Expected: PDF/HTML/DOCX build successfully. Verify figures still render, citations resolve, TOC reflects new headers.

**Step 6: Commit**

```bash
git add paper.md metadata.yaml
git commit -m "feat(paper): convert from IMRD to Viewpoint descriptive headers

- Rewrite abstract as unstructured narrative (≤450 words)
- Replace Introduction/Methods/Results/Discussion with thematic headers
- Update metadata.yaml to match

Addresses #506 Phase 1"
```

---

## Phase 2: Content Expansion (~2,000-3,000 words)

### Task 3: Strengthen SECI theoretical grounding (+300-500 words)

**Files:**
- Modify: `paper.md` (Theoretical Grounding section)
- Reference: `ARCHIVED/20260115_JMIR-Submission/paper.md` (search for "SECI", "Nonaka", "Socialization", "Externalization")

**Step 1: Read the archived version's SECI treatment**

Read `ARCHIVED/20260115_JMIR-Submission/paper.md` and search for all SECI-related passages. The archived version had richer treatment of:
- Why Socialization (tacit-to-tacit transfer via mentorship) fails when average tenure is <3 years
- How Externalization (tacit-to-explicit via artifacts) becomes the survival strategy
- The specific mapping of SECI quadrants to healthcare workforce failure modes

**Step 2: Expand the "Theoretical Grounding" section**

Add ~300-500 words covering:
1. Brief explanation of all four SECI quadrants (Socialization, Externalization, Combination, Internalization) so readers unfamiliar with Nonaka can follow
2. The specific failure mode: Socialization requires co-location and time (mentorship). With 53% CIO tenure <3 years and 55% informatics staff intending to leave, the "apprenticeship window" is shorter than the knowledge transfer cycle
3. Why traditional Externalization (writing wikis) fails: it's passive and low-fidelity in high-burnout environments
4. The Validated Query Triple as *active* Externalization: knowledge capture embedded in the daily workflow of analytics

Use citations: `[@farnese2019]` (SECI model), `[@massingham2018]` (knowledge loss), `[@goffin2011]` (externalization fidelity), `[@foos2006]` (tacit knowledge barriers)

**Step 3: Verify word count**

Run: `cat paper.md | sed '1,/^---$/d' | sed '/^# Acknowledgments/,$d' | wc -w`

Expected: ~2,200-2,400 words.

**Step 4: Commit**

```bash
git add paper.md
git commit -m "feat(paper): strengthen SECI theoretical grounding

Expand SECI model explanation with all four quadrants,
Socialization Failure mapping to workforce data, and
active vs. passive Externalization argument.

Addresses #506 task 2.1"
```

---

### Task 4: Expand the Validator Paradox discussion (+200-400 words)

**Files:**
- Modify: `paper.md` (Validator Paradox section)
- Reference: `ARCHIVED/20260115_JMIR-Submission/paper.md` (search for "Validator Paradox", "Standard Work", "ratchet")

**Step 1: Read the archived version's Validator Paradox treatment**

The current paper has only one paragraph on this. The archived version and issue #505 identify this as "the most intellectually honest contribution." Find the richer treatment.

**Step 2: Expand the Validator Paradox section**

Add ~200-400 words covering:
1. State the paradox explicitly as a counterargument: "A critical objection to HiL-SG is circular: if the framework requires domain experts to validate AI-generated queries, and the core problem is that domain experts are leaving, then the framework fails precisely when it is most needed."
2. Resolve via Lean "Standard Work" ([@alukal2006]): Validation is not "eternal truth" but "current known standard." Each validation establishes a floor, not a ceiling. When the next expert arrives, they inherit a baseline and can improve it.
3. The "Knowledge Ratchet" metaphor: Each validated triple prevents regression. Even if the next validator is less experienced, the organization cannot slide below the last validated state.
4. Real-world precedent: UC Davis Health's AMAM Stage 0→6 journey used standardized "S.M.A.R.T." definitions ([@himss2025ucdavis]), demonstrating that codified standards survive turnover.
5. Acknowledge the limitation: the paradox is not fully resolved. There is a minimum viable expertise threshold below which validation becomes meaningless. Future empirical work (Paper 2) should measure this threshold.

**Step 3: Verify word count**

Run: `cat paper.md | sed '1,/^---$/d' | sed '/^# Acknowledgments/,$d' | wc -w`

Expected: ~2,500-2,800 words.

**Step 4: Commit**

```bash
git add paper.md
git commit -m "feat(paper): expand Validator Paradox and Standard Work argument

Develop the paradox as counterargument, resolve via Lean Standard Work
and Knowledge Ratchet metaphor, cite UC Davis precedent, acknowledge
minimum expertise threshold limitation.

Addresses #506 task 2.2"
```

---

### Task 5: Restore key evidence for the Three Pillars (+300-500 words)

**Files:**
- Modify: `paper.md` (Evidence Base section)
- Reference: `ARCHIVED/20260115_JMIR-Submission/paper.md` (Pillars 1-3 content)

**Step 1: Read the archived version's pillar evidence**

The current paper has thin evidence for each pillar. The archived version has extensive statistics and citations. Identify the **strongest** evidence points without reproducing full subsections.

**Step 2: Selectively strengthen each pillar**

Add ~100-150 words per pillar:

**Pillar 1 (Analytics Maturity):** Add the clinical safety correlation: "EMRAM levels 6-7 correlate with 3.25 times higher odds of better Leapfrog Safety Grades" ([@snowdon2024]). Add the data quality trap: "39-71% missing data rates in cancer databases" ([@yang2021]) remain uncorrected because the experts who understand the context are leaving.

**Pillar 2 (Workforce Agility):** Add the cost dimension: "Knowledge loss can cost up to three times annual salary" ([@massingham2018; @oracle2024]). Add the productivity lag: "specialized roles require 18-24 months to reach fluency" ([@ledikwe2013; @konrad2022]). Add the concept of "Collective Knowledge Structures" required for complex task performance ([@rao2006]).

**Pillar 3 (Technical Enablement):** Add the NL2SQL tipping point data: "63% increase in self-service adoption and 37% reduction in retrieval time" ([@dadi2025]). Add precision medicine accuracy: "92.5% accuracy in parsing complex queries" ([@yang2025]). Add the qualifier: "not yet sufficiently accurate for unsupervised use" ([@ziletti2024]).

**Step 3: Verify word count**

Expected: ~3,000-3,300 words.

**Step 4: Commit**

```bash
git add paper.md
git commit -m "feat(paper): restore key evidence for Three Pillars

Add clinical safety correlation (EMRAM/Leapfrog), turnover costs,
productivity lag, NL2SQL adoption and accuracy data.

Addresses #506 task 2.3"
```

---

### Task 6: Expand Analytics Resilience Index context (+200-300 words)

**Files:**
- Modify: `paper.md` (ARI section)
- Reference: `ARCHIVED/20260115_JMIR-Submission/paper.md` (search for "Resilience Index", "maturity")

**Step 1: Expand ARI section**

Currently the ARI is a table with minimal explanation. Add ~200-300 words covering:

1. **Why resilience, not maturity:** Static maturity models (like HIMSS AMAM) assume linear progression and a stable workforce. Resilience measures the ability to *sustain* capability through disruption. In a high-turnover environment, an organization at AMAM Stage 5 that falls to Stage 3 after a key departure has low resilience regardless of its peak maturity.
2. **How ARI could be operationalized:** Sketch a measurement approach. Each dimension could be scored on a Likert-type scale (1-5). Example: "Knowledge Locus" scored by surveying whether key queries are documented in a shared repository vs. known only to named individuals. Aggregate score indicates organizational resilience posture.
3. **Relationship to existing frameworks:** ARI complements (not replaces) AMAM by adding a temporal/dynamic dimension. AMAM measures "where you are"; ARI measures "how far you fall when someone leaves."

**Step 2: Verify word count**

Expected: ~3,200-3,600 words.

**Step 3: Commit**

```bash
git add paper.md
git commit -m "feat(paper): expand ARI with resilience rationale and operationalization

Explain why resilience > maturity for turnover context, sketch
measurement approach, position relative to AMAM.

Addresses #506 task 2.4"
```

---

### Task 7: Expand Cognitive Forcing Functions (+100-200 words)

**Files:**
- Modify: `paper.md` (Safety section)

**Step 1: Expand the safety argument**

Currently 2 sentences. Add ~100-200 words:

1. Frame HiL-SG as a **safety mechanism**, not a productivity tool. The risk of unsupervised AI in clinical analytics is "laundering hallucinations": a plausible-sounding but incorrect query result that drives clinical decisions.
2. Cognitive Forcing Functions ([@ziletti2024]) require the AI to explain its logic *before* showing results, forcing the user to engage System 2 (analytical) thinking rather than System 1 (fast, heuristic) acceptance.
3. Evidence: user studies show this pattern reduces error recovery time by 30-40 seconds ([@ipeirotis2025]).
4. Connection to aviation safety literature: checklists and mandatory call-outs are analogous forcing functions that transformed aviation safety. HiL-SG applies the same principle to analytics.

**Step 2: Verify word count**

Expected: ~3,400-3,800 words.

**Step 3: Commit**

```bash
git add paper.md
git commit -m "feat(paper): expand Cognitive Forcing Functions safety argument

Frame HiL-SG as safety mechanism, cite error recovery evidence,
draw aviation safety analogy.

Addresses #506 task 2.5"
```

---

### Task 8: Update stale `ang2004` turnover citation

**Files:**
- Modify: `paper.md` (references to "2.9 years" tenure)
- Modify: `references.bib` (add new entry if needed)
- Reference: `../library` knowledge graph (search for workforce/turnover data)

**Step 1: Search the library knowledge graph for updated turnover data**

Run: `cd ../library && uv run python utils/tool_search.py "healthcare IT workforce turnover tenure 2024 2025"`

If the library graph has relevant results, extract the most current statistic on healthcare IT tenure or turnover rates. Prefer 2024-2025 sources: HIMSS Workforce Survey, KLAS Research, LinkedIn Workforce Reports, or NSI Nursing Solutions Report.

**Step 2: Check existing references.bib for usable modern data**

The following entries already exist and contain modern workforce data:
- `wittkieffer2024`: 53% of CIOs <3 years tenure (already cited)
- `himssworkforce2024`: 79% reporting persistent shortages (already cited)
- `rajamani2025`: 55% intend to leave (already cited)
- `nsi2025`: 30% of new employees leaving within first year (already cited)

**Step 3: Replace the stale citation in paper.md**

Find the passage referencing `[@ang2004]` and the "2.9 years" statistic. Replace it with one of two approaches:

**Option A (preferred):** If a 2024-2025 source with a direct tenure figure is found, cite it directly. Remove `[@ang2004]` from the passage.

**Option B (fallback):** Reframe the passage to acknowledge the data gap explicitly: "A foundational 2004 study established healthcare IT tenure at 2.9 years [@ang2004]; no direct replication exists, but contemporary signals are worse: 30% of new healthcare employees leave within their first year [@nsi2025], and 55% of informatics specialists intend to leave their positions [@rajamani2025]." This turns the stale citation into evidence of the "data desert" itself.

**Step 4: Verify the citation is updated**

Run: `grep -n "ang2004\|2\.9.year" paper.md`

Expected: Either `ang2004` is removed or reframed with modern context.

**Step 5: Commit**

```bash
git add paper.md references.bib
git commit -m "fix(paper): update stale Ang & Slaughter 2004 turnover citation

Replace or reframe the 22-year-old '2.9 years' statistic with
2024-2025 workforce data from existing references.

Addresses #506 task 3.1"
```

---

## Phase 3: Quality & Compliance

### Task 9: Ensure product neutrality and add competing interests

**Files:**
- Modify: `paper.md` (scan for vendor language, check Conflicts of Interest section)

**Step 1: Scan for vendor brochure tone**

Search `paper.md` for:
- Any language that sounds like a product pitch (e.g., "our platform", "the solution enables")
- Verify conversational AI is framed as "Governance Forcing Function" (enabler), not standalone solution
- Verify the framework is descriptive (reveals interconnections), not prescriptive (recommends specific solutions)

Run: `grep -in "platform\|product\|solution\|our tool\|our system\|enables\|seamless" paper.md`

Fix any vendor-sounding language.

**Step 2: Verify Conflicts of Interest section**

The current paper already has a Conflicts of Interest section (lines 161-163). Verify it adequately discloses:
- Author's role at Yuimedi, Inc.
- Author's employment at Indiana University Health
- That the paper does not evaluate or recommend specific products

This addresses #371.

**Step 3: Commit (if changes needed)**

```bash
git add paper.md
git commit -m "fix(paper): ensure product neutrality and verify competing interests

Scan for vendor language, verify Governance Forcing Function framing,
confirm Conflicts of Interest disclosure.

Addresses #506 task 3.2, Closes #371"
```

---

### Task 10: Final validation and word count check

**Files:**
- Read: `paper.md` (final state)
- Run: `scripts/validate_jmir_compliance.py`, `scripts/validate_references.py`

**Step 1: Run JMIR Viewpoint compliance validator**

Run: `uv run python scripts/validate_jmir_compliance.py --article-type viewpoint`

Expected: ALL PASS. Specifically:
- Abstract: Unstructured, ≤450 words
- Structure: No IMRD headers
- Word count: ≤5,000 body words
- Required end sections: All present
- AI disclosure: Present
- Citations: Present and formatted correctly

**Step 2: Validate references**

Run: `uv run python scripts/validate_references.py --all`

Expected: All citations in paper.md have matching entries in references.bib. No broken URLs (or known broken ones are flagged).

**Step 3: Run quality checks**

Run: `uv run ruff format . && uv run ruff check --fix . && uv run mypy scripts/`

Expected: Clean.

**Step 4: Final word count**

Run: `cat paper.md | sed '1,/^---$/d' | sed '/^# Acknowledgments/,$d' | wc -w`

Expected: 4,000-5,000 words. If over 5,000, trim the weakest evidence in the Three Pillars section. If under 4,000, further expand the Validator Paradox or ARI sections.

**Step 5: Commit**

```bash
git add -A
git commit -m "chore(paper): pass all JMIR Viewpoint compliance checks

Word count within 4,000-5,000 range, all validators pass,
references validated, code quality clean.

Addresses #506 Phase 3"
```

---

## Phase 4: Build & Prepare for Submission

### Task 11: Build all paper formats and visual review

**Files:**
- Run: `scripts/build_paper.sh`
- Review: Generated PDF, HTML, DOCX

**Step 1: Build all formats**

Run: `./scripts/build_paper.sh --format all`

Expected: PDF, HTML, DOCX, LaTeX all generate without errors.

**Step 2: Visual review checklist**

Manually verify in the PDF:
- [ ] Title page renders correctly
- [ ] Abstract is a single flowing paragraph (no section headers)
- [ ] Table of Contents reflects descriptive (non-IMRD) headers
- [ ] Figures 1 and 2 render correctly with captions
- [ ] ARI table renders correctly
- [ ] All citations resolve to numbered references
- [ ] References section is complete
- [ ] No orphan/widow typographic issues

**Step 3: Commit build artifacts**

```bash
git add paper.pdf paper.html paper.docx paper.tex 2>/dev/null
git commit -m "build: regenerate paper artifacts for Viewpoint submission

Addresses #506 Phase 4"
```

---

### Task 12: Write resubmission cover letter

**Files:**
- Create: `cover-letter.md`

**Step 1: Draft cover letter**

Create `cover-letter.md` with:
- Reference manuscript ID ms#91493
- Acknowledge the editor's feedback on length
- State the revision addresses length (from ~12,730 to ≤5,000 words)
- Specify article type: Viewpoint
- Briefly describe the restructuring: IMRD → descriptive headers, content focused on framework + key evidence
- Note the paper retains its core contribution (HiL-SG framework, Validated Query Triples, ARI) while removing exhaustive methodology/literature review sections appropriate for a full research paper

**Step 2: Commit**

```bash
git add cover-letter.md
git commit -m "docs: add resubmission cover letter for JMIR ms#91493

Reference original submission, describe revision scope,
specify Viewpoint article type.

Addresses #506 task 3.7"
```

---

## Dependency graph

```
Task 1 (validator) ─┐
                     ├─→ Task 2 (restructure) ─→ Tasks 3-8 (content, parallel) ─→ Task 9 (neutrality)
                     │                                                               ↓
                     │                                                          Task 10 (validation)
                     │                                                               ↓
                     │                                                          Task 11 (build)
                     │                                                               ↓
                     └──────────────────────────────────────────────────────────→ Task 12 (cover letter)
```

Tasks 3-8 can be done in any order and are independent of each other. All depend on Task 2. Tasks 9-12 are sequential.

---

## Using `../library` knowledge graph

Task 8 uses the `../library` repo's semantic search to find updated workforce statistics. The relevant command:

```bash
cd ../library
uv run python utils/tool_search.py "healthcare IT workforce turnover tenure 2024 2025"
```

The library contains 23+ ingested papers on healthcare, workforce, and data standardization. The search may surface documents like:
- `2024_WittKieffer_CIO-Insights-Healthcare-IT-Leadership.pdf`
- `2024_NSI_National-Health-Care-Retention-Report.pdf`
- `h25eu-future-workforce.pdf` (HIMSS)

If the library graph returns relevant results with more current tenure data than Ang & Slaughter 2004, add a new BibTeX entry to `references.bib` and cite it in `paper.md`.
