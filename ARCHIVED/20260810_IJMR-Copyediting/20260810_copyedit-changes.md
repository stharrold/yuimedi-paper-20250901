# Copyediting Round Log, ms#96541 (2026-08-10)

What the copyeditor asked for, what was changed in response, and what remains
open. The literal source diff is `20260810_copyedit-source-changes.diff`.

## Query 1: undefined "three-pillar structure"

**Copyeditor:** on "The three-pillar structure aligns with established models
across healthcare informatics and knowledge management (Table 1):" asked to
"clarify which 3-pillar structure this refers to as it has not been mentioned
previously in the main text."

**Assessment:** correct, and worth more than a pointer to the title. "Three-Pillar"
appears in the title and abstract, but this sentence was its first appearance in
the body, used with a definite article as though already introduced. Compounding
it, the body's opening enumerates a different trio, the "Triple Threat" (low
analytics maturity, semantic gap, workforce instability). Two of those three
names differ from the pillar names, so a reader would likely attach "three-pillar
structure" to the wrong antecedent.

Probable cause: the pillars were introduced in the original ~12,730-word Original
Paper submission. When that was compressed to a ~4,500-word Viewpoint, the
introducing passage was cut while every downstream reference survived. Title and
abstract kept the term alive, which is why it stayed invisible to the author and
to both reviewers, all of whom read the abstract first.

**Change:** defined the pillars at first use.

Before:

> The three-pillar structure aligns with established models across healthcare
> informatics and knowledge management (Table 1):

After:

> The framework's three pillars name the organizational capabilities at stake in
> the Triple Threat: analytics maturity, workforce agility, and technical
> enablement. This structure aligns with established models across health care
> informatics and knowledge management (Table 1):

"At stake in" was chosen deliberately over "undermined by." The latter is
circular for the first pillar, since threat 1 already is low analytics maturity,
and it implies a positional mapping that does not hold: the threats run maturity,
semantic gap, workforce, while the pillars run maturity, workforce, technical.

## Query 2: "healthcare" to "health care"

**Copyeditor:** replace "healthcare" with "health care" (AMA house style).

**Change:** 28 replacements across three source files.

| File | Replaced | Preserved |
|:---|---:|---:|
| `paper.md` | 25 | 2 |
| `metadata.yaml` | 2 | 0 |
| `multimedia_appendix_1.md` | 1 | 0 |

Capitalization was resolved by context rather than mechanically. The article
title and the H1 heading took title case ("Health Care Analytics"), while
sentence-initial instances took sentence case ("Health care organizations").

**Deliberately preserved:** both instances of "Healthcare Information and
Management Systems Society," the HIMSS legal name, at `paper.md` line 32 and in
the abbreviations list. House style governs the author's prose, not an
organization's registered name.

**`references.bib` deliberately untouched.** It holds 28 instances across
published article titles, journal names (*International Journal of Healthcare
Management*, *Management in Healthcare*), a corporate author (*Healthcare IT
News*), and **7 URLs**. AMA style requires titles reproduced as published, and a
global replace would silently break live links, turning `healthcareitnews.com`
into `health careitnews.com`. This exemption should be stated to the copyeditor
so that no find-and-replace is run across the bibliography.

## Query 3: Figure 1 (architecture) text

**Copyeditor**, three requests on the architecture figure:

1. Revise "Healthcare" to "Health care."
2. Set all text within the figure to sentence case, for example "Clinical User"
   to "Clinical user."
3. Remove all spaces before and after the plus sign.

**Change:** all three addressed by editing `figures/architecture.mmd` and
re-rendering. Node labels now read:

| Before | After |
|:---|:---|
| Clinical User | Clinical user |
| Conversational AI / NLP Engine + SQL Generation | Conversational AI / NLP engine and SQL generation |
| Data Warehouse / Healthcare Database | Data warehouse / Health care database |
| Expert Validation | Expert validation |
| Insight Delivery / Results and Visualizations | Insight delivery / Results and visualizations |
| Organizational Memory / Validated Query Triples | Organizational memory / Validated query triples |
| Knowledge Base / Ontologies + Best Practices | Knowledge base / Ontologies and best practices |

Acronyms (AI, NLP, SQL) keep their capitalization. Edge labels were already
sentence case and are unchanged.

**On request 3, the plus sign:** rather than closing up the spaces, the plus sign
was replaced with the word "and" in both labels. Closing the spaces would have
produced "NLP engine+SQL generation," which invites a misreading as "NLP
(engine+SQL) generation," because a plus sign conventionally binds tightly to the
tokens on either side. Substituting "and" satisfies the request completely, since
no plus sign remains to be spaced, while removing the ambiguity. It also reads
better: a plus sign used as a prose conjunction is informal for a journal figure.
If the copyeditor prefers the literal closed-up form, it is a one-line change to
each label.

**Files regenerated:** `figures/architecture.mmd.svg`,
`figures/architecture.mmd.png` (1094x1247), `figures/architecture.figure.png`
(1052x1200, the journal upload copy at the 1200px maximum), and
`figures/architecture.mmd.caption.txt`, which had carried the old title-case node
names. The rendered output was compared against the previous version: layout,
node positions, arrow routing, shading, and font are unchanged, and only the
label text differs.

Figure 2 was flagged at this point as likely to need the same treatment. The
copyeditor confirmed that shortly afterward; see Query 4.

## Query 4: Figure 2 (validated query cycle) text

**Copyeditor**, two requests on the knowledge cycle figure:

1. Set all text within the figure to sentence case, for example "VALIDATED QUERY
   CYCLE" to "Validated query cycle," "AI explains logic; Analyst confirms" to
   "AI explains logic; analyst confirms," and "Analytics Maturity" to "Analytics
   maturity."
2. Revise "Three pillars" to "3 pillars."

**Change:** both addressed by editing `figures/knowledge-cycle.mmd` and
re-rendering.

| Before | After |
|:---|:---|
| VALIDATED QUERY CYCLE (subgraph title) | Validated query cycle |
| THREE PILLARS (subgraph title) | 3 pillars |
| AI explains logic; Analyst confirms | AI explains logic; analyst confirms |
| Analytics Maturity | Analytics maturity |
| Workforce Agility | Workforce agility |
| Technical Enablement | Technical enablement |

The numbered step headings ("1. Query," "2. Generation," "3. Validation,"
"4. Storage," "5. Retrieval," "6. Persistence") are each a single word after the
numeral and are already sentence case, so they are unchanged. Step subtitles
("Analyst asks question," "System generates SQL," "Triple stored," "Future
queries match," "Knowledge survives turnover") and all edge labels ("Correct,"
"Incorrect," "Advances," "Stabilizes," "Increases," "New analyst uses validated
queries") were already sentence case. Acronyms (AI, SQL) keep their
capitalization.

**Files regenerated:** `figures/knowledge-cycle.mmd.svg`,
`figures/knowledge-cycle.mmd.png` (795x1434, unchanged from before),
`figures/knowledge-cycle.figure.png` (665x1200, the journal upload copy), and
`figures/knowledge-cycle.mmd.caption.txt`, which had carried the old title-case
terms and the spelled-out "Six-step" and "three outcome pillars." The caption now
uses numerals and sentence case to match the proof, whose Figure 2 caption reads
"The 6-step validated query cycle and its mapping to the 3 pillars."

**Pre-existing cosmetic note, not introduced by this change:** the dashed
"Stabilizes" connector crosses the pillars subgraph title. It did so in the
previous render with "THREE PILLARS" as well, so this is not a regression. It
could be reduced by padding the subgraph title asymmetrically, but that was left
alone as unrequested restyling.

## Word count

The copyeditor cleared the length before these changes were applied, so the
sentence at the head of the Evidence Base section ("The HITL-KG framework is
supported by three pillars of empirical evidence...") was retained rather than
cut as an offset.

| | Words |
|:---|---:|
| JMIR method count before | 4,990 |
| Query 1 (pillar definition) | +20 |
| Query 2 (each replacement turns one word into two) | +25 |
| AMAM expansion corrected (see finding A, 5 words to 4, twice) | -2 |
| Query 5 (conversational AI named at first use) | +11 |
| Query 6 ("worldwide" added to the stage 6 and 7 counts) | +1 |
| Query 7 (turnover cost sentence rewritten, "total" retained) | +7 |
| Currency consistency (`US $1.6 million` at line 130) | +1 |
| Query 8 (data availability template 4 plus code disclosure) | +12 |
| **After** | **5,065** |

65 words over the 5,000 limit, accepted by the copyeditor.

## Open items

**1. Title numeral style is inconsistent between the copyedited file and this repo.**
The copyediting email gives the manuscript title as "Health Care Analytics
Challenges: **A 3-Pillar Framework** Connecting Analytics Maturity, Workforce
Agility, and Technical Enablement." This repository uses "**A Three-Pillar**
Framework" throughout, and the term appears in many places beyond the title:
"Three-Pillar Assessment Rubric" in the abstract, body, Table 2 caption,
Limitations, Future Research, and Multimedia Appendix 2. AMA style does favor
numerals. A decision is needed on whether the numeral form applies only to the
title or to every occurrence, and the answer should be applied consistently in
one pass. Not changed here, because the copyeditor's file governs.

**2. Figure 1 text. RESOLVED, see Query 3 below.**

**3. "health care-specific" appears twice** at `paper.md` line 138. AMA would set
a compound modifier on a two-word base with an en dash ("health care–specific"),
which is awkward in a repository that bans em-dashes. The literal replacement was
applied rather than a rewording, since the copyeditor owns house style. If a
rewording is preferred, "benchmarks specific to health care" and "natural language
interfaces built for health care" read cleanly at a cost of one word each.

**4. The title change has not been propagated to publication metadata.**
`CITATION.cff`, `.zenodo.json`, and `README.md` still carry "Healthcare Analytics
Challenges." The Zenodo entry is a published record under concept DOI
10.5281/zenodo.18264359, so updating it is a deliberate act rather than
housekeeping. Recommend syncing all three at the next release, so repository
metadata matches the article as actually published.

## Findings from the copyedited proof (`96541.pdf`)

The proof is scheduled for publication on **21.Aug.2026** as
Interact J Med Res 2026;15:e96541, doi 10.2196/96541. Reviewing it surfaced the
following, listed most serious first.

### A. AMAM naming: the copyeditor is right, this repository is stale

**Resolved, no query needed.** An initial reading of this package claimed the
proof expanded AMAM two different ways and that the Abbreviations list was wrong.
That was a misreading: the "Adoption Model for Analytics Maturity" string in the
proof is **reference 2's title** (the Healthcare IT News article), correctly
retained as published. The proof is internally consistent.

Proof usage, verified:

| Location in proof | Expansion |
|:---|:---|
| Body, first use | Analytics Maturity Assessment Model |
| Table 1 footnote b | Analytics Maturity Assessment Model |
| Table 2 footnote b | Analytics Maturity Assessment Model |
| Abbreviations list | Analytics Maturity Assessment Model |
| Reference 1 title | Analytics Maturity Assessment Model (AMAM) |
| Reference 2 title | Adoption Model for Analytics Maturity (published wording, correct) |

HIMSS relaunched the model on 2024-10-02 at the HIMSS24 APAC conference, and its
current official name is **Analytics Maturity Assessment Model (AMAM)**. The
older "Adoption Model for Analytics Maturity" survives only on the legacy
himssanalytics.org site. The R1-era decision recorded in commit `64ca59f`, which
chose "Adoption Model for Analytics Maturity" as HIMSS's official expansion, was
based on that legacy source and is now out of date.

Repository-side corrections needed (the published article is already correct):

1. `paper.md` line 32, body first use, and line 230, Abbreviations list: change
   "Adoption Model for Analytics Maturity" to "Analytics Maturity Assessment
   Model."
2. `references.bib`, key `himss2024news`: the stored title is "HIMSS launches
   modernised Analytics Maturity Assessment Model." The actual article title is
   "At HIMSS24 APAC, the Adoption Model for Analytics Maturity gets facelift,"
   which is what the proof prints and what the live URL serves. The copyeditor
   caught and fixed this. Re-run `scripts/audit_references.py` after correcting.

Sources: HIMSS AMAM model page (https://www.himss.org/maturity-models/amam/),
HIMSS relaunch announcement
(https://www.himss.org/news/newly-improved-analytics-maturity-assessment-model-amam-centered-patient-outcomes-improve-ai).

### B. Sixteen abbreviations were removed from the Abbreviations list

Removed: AACODS, ACO, AI, BI, CI/CD, CIO, CMS, DIKW, DSR, EHR, EMRAM, HITL, IT,
NLP, SECI, SQL. Retained: AMAM, EMR, HIMSS, HITL-KG, LLM, NL2SQL.

Most of these are legitimate. The copyeditor spelled out terms used only once and
dropped the abbreviation entirely, so ACO, BI, CI/CD, DIKW, DSR, and EMRAM no
longer appear in the body at all. HITL only appears inside "HITL-KG," which is
listed.

But six abbreviations **still appear in the body while absent from the list**:

| Abbreviation | Uses in proof body |
|:---|---:|
| SECI | 2 |
| AACODS | 1 |
| CIO | 1 |
| CMS | 1 |
| EHR | 1 |
| NLP | 1 |

SECI is the theoretical spine of the paper and should certainly be listed. The
remaining five should either be restored to the list or spelled out at each use.
Worth one consolidated query.

### C. House style in the proof differs from this repository

The copyeditor applied two systematic conventions that the repository sources do
not follow:

1. **Numerals for numbers.** The proof has 12 numeral forms ("3-pillar",
   "3 pillars", "6-step") and zero spelled-out forms. The title is "A 3-Pillar
   Framework."
2. **Lowercase for coined terms.** "triple threat," "validated query triple,"
   "knowledge ratchet," "validator paradox," and "standard work" are lowercased
   except at sentence start, and the italic emphasis is gone.

No attempt was made to mirror these in the repository sources. Recommend syncing
`paper.md` to the published version in a single pass **after** the proof is
final, so the repository matches the article of record rather than chasing a
moving target.

### D. Text to supply for Query 1, in proof house style

The proof still carries the unclarified sentence at the head of the Table 1
discussion. The replacement drafted above should be adapted to the proof's
numeral and lowercase conventions before it is entered into the system:

> The framework's 3 pillars name the organizational capabilities at stake in the
> triple threat: analytics maturity, workforce agility, and technical enablement.
> This structure aligns with established models across health care informatics
> and knowledge management (Table 1).

### E. Reference titles correctly retain "Healthcare"

Spot-checked in the proof: "The failure of Haven Healthcare: lessons for
radiology learners" and the CNBC URL both keep the original spelling. The
bibliography exemption described above was applied correctly on the journal side.
