# Proof review, i-JMR ms#96541 (final proof round)

Proof notification received 2026-08-13 16:51 EDT from donotreply@exeterpremedia.com
(reply-to laura.mcreynolds@jmir.org, cc production@jmir.org). Archived as
`20260813_Email_JMIR-Production-Editor.pdf`.

- Proof PDF of record: `96541_modified2.pdf` (14 pages, downloaded 2026-08-13 18:12 EDT).
- Baseline for comparison: `96541_modified.pdf`, the version approved at the close
  of copyediting on 2026-08-10.
- Sign-off window: 3 days from receipt, so approximately 2026-08-16.
- Review is in Kriyadocs, Chrome only, submitting author only. Approve then Submit
  closes author access.
- Standing instruction from the email: only errors and important corrections are
  accepted at this stage. Discretionary style and content changes will be refused.

## Verification performed

Text layers of both proofs extracted with `pdftotext -layout`, then compared two ways:

1. Sentence level word diff, to see every change in context.
2. Position independent word multiset diff, so that the two column reflow between
   the two versions could not hide an insertion or a deletion.

Every change in word counts reconciles to a known cause. Nothing was silently
dropped in typesetting. Page count is unchanged at 14.

All substantive changes agreed during copyediting were confirmed still present in
the new proof: the sentence naming the 3 pillars at first use, "26 organizations
worldwide", "a total cost of up to US $8.97 million", the conversational AI system
named at first mention, reference 28 ("design workspaces", author Ge X), and
reference 61 (full title with year 2025).

## Corrections to enter (2 items)

### 1. Title reads "InHealth Care Analytics Challenges"

The article title is corrupted in the new proof. It was correct in both earlier
versions and is correct in the manuscript source, so this was introduced during
typesetting.

- Correct: `Health Care Analytics Challenges: A 3-Pillar Framework Connecting
  Analytics Maturity, Workforce Agility, and Technical Enablement`
- In the proof: `InHealth Care Analytics Challenges: ...`

It appears in at least two places in the rendered proof: the page 1 title block and
the "Please cite as" block in the end matter. The same corrupted string is in the
subject line and body of the proof notification email, which suggests the error is
in the title metadata field rather than in the typeset display text alone.

Ask explicitly for the correction in all of: the title metadata field, the typeset
title on page 1, any running or short title, and the "Please cite as" block. The
title field is what gets deposited to Crossref and PubMed, so a display only fix
would leave the wrong title in the permanent record.

### 2. Reference 85 cites a version specific Zenodo record instead of the concept DOI

During copyediting I asked whether the Zenodo deposit should become a numbered
reference rather than an inline DOI. Converting it to reference 85 answers that
question and is welcome. The identifier used is wrong, however.

As set:

> 85. Harrold ST. Health care analytics challenges: a 3-pillar framework connecting
> analytics maturity, workforce agility, and technical enablement. Zenodo.
> URL: https://zenodo.org/records/21880033 [Accessed 2026-08-11]

`https://zenodo.org/records/21880033` is the version specific record for v5.0.0
(its own DOI is 10.5281/zenodo.21880033). It is frozen at that release and will
never resolve to later versions of the deposit. The correct identifier is the
concept DOI, which always resolves to the most recent version:

    10.5281/zenodo.18264359

Requested change: replace `URL: https://zenodo.org/records/21880033 [Accessed
2026-08-11]` with `[doi: 10.5281/zenodo.18264359]`, matching the DOI formatting used
by the other references in the list. The reference otherwise stands as set.

Verified against the Zenodo API on 2026-08-13: record 21880033 reports
`conceptdoi: 10.5281/zenodo.18264359` and `version: v5.0.0`.

## Query to add for the Publisher

The proof email states that once the proof is approved and no queries are pending,
the article is scheduled for publication. The agreed production hold lives on a
separate email thread with the Production Editor, so it should be restated here in
writing where the production team will see it.

Suggested text:

> Please note a production hold agreed with Laura McReynolds on 2026-08-11: this
> article is to be held at the final production stage until the in house visual
> abstract is complete, then published with the visual abstract in place, with the
> sponsored tweet sent alongside it. Approving this proof is not a request to
> schedule publication. The visual abstract questionnaire was submitted 2026-08-06.

Approving the proof inside the 3 day window and holding publication are not in
conflict. Approve on time so the proof stage does not become the bottleneck, and let
the hold be governed by the query and by Laura's thread.

## Not raised (copyeditor changes, correctly left alone)

These are all changes made since the approved version that are legitimate and should
not consume credibility at a stage that accepts only error corrections:

- `colocated` to `co-located`.
- `2 decade-old` to `2-decade-old`, adding the missing numeral. The en dash between
  "decade" and "old" is the correct compound modifier convention and is not an error.
- Reference 19 journal name expanded to "ACM SIGMIS DATABASE: the DATABASE for
  Advances in Information Systems".
- Table footnote "cNL: Natural Language" set to "cNL: natural language." for sentence
  case and terminal punctuation.
- "Yuimedi, Inc," set to "Yuimedi, Inc.," in the conflicts of interest statement.
- The Data Availability statement rewritten to cite reference 85 in place of the
  inline DOI URL. Only the identifier inside reference 85 is at issue, not the
  restructuring.

## Figures: checked, unchanged, one judgment call

Both embedded images were extracted from each proof and hashed. They are byte
identical between `96541_modified.pdf` and `96541_modified2.pdf`, so typesetting did
not touch them. Both were then inspected visually, since figure label text is
rasterized and no text diff can see it.

Figure 1 is correct: "NLP engine and SQL generation" carries the requested "and" in
place of the plus sign, "Health care database" is set correctly, and all labels are
sentence case. Figure 2 carries the requested "3 pillars" in place of "THREE
PILLARS", and all labels are sentence case.

One pre-existing defect, not introduced by typesetting: in Figure 2 the "Stabilizes"
edge label and its arrowhead overlap the "3 pillars" subgraph title, clipping the end
of the word. The overlap comes from the PNG supplied at copyediting, so it was
present in the approved version and in every earlier proof.

This is a judgment call rather than a clear correction. Arguments for leaving it:
fixing it means editing `figures/knowledge-cycle.mmd`, re-rendering, regenerating the
1200px upload copy, and re-uploading at a stage that asks for errors only, and the
figure was already approved through copyediting with the collision in place. Argument
for raising it: it is a legibility defect that will be permanent in the published
article, and the label is one of the three pillar outcomes the figure exists to show.

If raised, it should go in as a query to the Publisher with a replacement PNG, not as
an in-system text edit.

## Second pass, after the author's in-system edits (96541_modified3.pdf)

Exported 2026-08-13 18:44 EDT, after correcting the title and reference 85 in
Kriyadocs. Compared against `96541_modified2.pdf` by the same two methods.

Exactly 6 token changes, all intended and nothing else: "InHealth" to "Health" twice,
the version-specific Zenodo URL replaced by the concept DOI URL, and the access date
advanced to 2026-08-13. Total word count unchanged at 8018, so the edits introduced no
collateral damage. Page 1 and the page 14 cite-as block were both confirmed visually.

Reference apparatus audited independently on this version: 85 references listed, no
gaps, no duplicates, all 85 cited in the body, and first citations appear in strict
numerical order 1 through 85. Note that citation-order checks must use reading-order
extraction (`pdftotext` with no `-layout`), because `-layout` interleaves the two
columns and reports about 16 phantom ordering violations.

Reference 85 could not be rendered in the bracketed `[doi: ...]` form the other entries
use. That form appears to come from a DOI metadata field rather than typed text. The
entry as it stands is accurate and matches how the other URL-only references in the
list are set, so it is raised as a formatting request only, explicitly non-blocking.

### Further findings, none of them typesetting regressions

Four were proposed. Two were wrong and are withdrawn; two held.

WITHDRAWN. Table 2's caption "Three-pillar assessment rubric indicators" and the
Multimedia Appendix 2 caption "Three-pillar organizational assessment rubric" are
correct as set. I read them as leftovers from the numeral sweep because the body uses
"3-pillar" throughout, but i-JMR and AMA style never open a sentence or title with a
numeral, and a caption is a sentence, so a sentence-initial number is spelled out.
Figure 2's caption is the control that proves the rule was applied consistently
rather than abandoned: "The 6-step validated query cycle and its mapping to the 3
pillars" begins with "The", so both numerals fall mid-sentence and correctly stay
numerals. The lesson for any future pass: before calling a spelled-out number an
inconsistency, check its position in the sentence.

HELD. "a continuous cycle of four conversion modes" introduces the numbered SECI list,
while the sentence just after the list reads "these 4 modes form a self-reinforcing
spiral". Both are mid-sentence, so the numeral is the correct form in both. Corrected
in-system by the author.

HELD, and stronger than first described. The Funding statement reads "Yuimedi, Inc,
provided financial support", missing the period after "Inc". The version approved on
2026-08-10 contained two identical "Yuimedi, Inc," constructions, in Funding (line 485)
and in Conflicts of Interest (line 506). This typesetting round corrected the Conflicts
of Interest instance to "Yuimedi, Inc.," and left the Funding one. It is a
half-completed fix from this round rather than an authorial inconsistency, which is
what makes it worth raising at a stage that accepts only error corrections.

On the comma itself, which is a separate question from the missing period: "Yuimedi,
Inc." with the comma is the author's own supplied form, carried through from
`metadata.yaml`, `paper.md`, `CITATION.cff`, and `.zenodo.json`, and it matches the page
1 affiliation. The journal did not impose it. Chicago and AMA both prefer dropping the
comma before Inc, but style guides defer to an organization's legal registration for
proper names, and the form is already consistent across the article and across the
ORCID, Zenodo, and citation records. Changing it at proof stage would be exactly the
discretionary style change the notification refuses. Not raised.

## Third pass: 96541_modified4.pdf plus the two appendices

`96541_modified4.pdf` (19:42 EDT) applied the "4 conversion modes" numeral and the
Funding period. Four token changes, nothing else, word count still 8018.

The author then supplied `96541_appendix1.docx` and `96541_appendix2.docx`, the
multimedia appendices as production holds them. These had never been reviewed in this
process, and they are the source of most of what follows.

### Two errors in the article text

Neither is a typesetting regression from this round; both were in the version approved
on 2026-08-10.

- Reference 38 reads "Ziletti A, DAmbrosi L." The apostrophe in "D'Ambrosi" has been
  dropped. Confirmed visually on page 11, where reference 20's "Nonaka's" on the same
  page proves apostrophes render. `references.bib` line 53 has it correctly. A sweep
  established this is isolated: it is the only author name in the bibliography with an
  apostrophe, and both apostrophe-bearing titles (reference 81 "IBM's", reference 10
  "'information age'") render correctly, so this is single-character loss rather than
  an encoding pass.
- Page 7, under "The 3-Pillar Rubric": "reviewed in the The Evidence Base: 3 Pillars
  section" doubles the article. WITHDRAWN 2026-08-19, and wrong on my part. House
  style requires the form "the <Section Title>" with the title reproduced verbatim,
  so a section whose own title begins with "The" necessarily yields "the The". It is
  correct as set, and production was right to leave it. The parallel on page 6, "as
  detailed in the Theoretical Grounding: Socialization Failure section", is the
  control: same rule, no doubling, only because that title does not begin with "The".
  This is the same trap as the sentence-initial numeral: a construction that reads as
  an error in isolation is required by a rule operating one level up.

### The appendices in production are the R2 uploads

Root cause for most of the appendix findings: JMIR holds the files uploaded with the R2
revision in July. The copyeditor's corrections were applied to the article only, and
the appendices are separately uploaded files that an in-system text edit cannot reach.

Appendix 2's reference list now contradicts the article's on two entries:

| Entry | Article (correct) | Appendix 2 (stale) |
|---|---|---|
| Healthcare IT News | "At HIMSS24 APAC, the Adoption Model for Analytics Maturity gets facelift" | "HIMSS launches modernised Analytics Maturity Assessment Model" |
| NSI staffing report | 2026 edition, published 2026 | 2025 edition, published 2024 |

The Healthcare IT News direction was the one item where the correct value was not
obvious, since three earlier submission packages and
`docs/research/2024_HealthcareITNews_HIMSS-Launches-Modernised-AMAM.md` all carry
"modernised". It was settled from `bibliography-audit/himss2024news/5-landing-page.html`,
saved 2026-07-09, whose `<title>` and `og:title` both read "At HIMSS24 APAC, the
Adoption Model for Analytics Maturity gets facelift". The article is right; the
appendix carries the defect that the 2026-08-10 sweep caught and fixed in the bib.

Two further Appendix 2 errors were introduced by JMIR's typesetting, since both are
correct in the R2 file that was uploaded and correct in the article:

- Reference 4: "Shahbaz G M." for "Shahbaz M, Gao C, Zhai L, Shahzad F, Hu Y."
- Reference 5: "Ziletti &D A." for "Ziletti A, D'Ambrosi L."

These match the author-separator mangling documented in the root `CLAUDE.md`: a
comma-or-ampersand blob parses as a single name and renders as garbage.

Appendix 1 has two problems of the same family:

- Its heading reads "Validated Query Triple Examples for Healthcare Analytics",
  predating the health care copyedit and contradicting the article's own title.
- It quotes a section title that no longer exists: "The Solution: Externalization via
  Socio-Technical Artifacts". The article's heading is now "Sociotechnical",
  unhyphenated.

### Replacement files

Built and verified 2026-08-13 19:57 EDT, archived here as
`20260813_multimedia_appendix_1_replacement.docx` and
`20260813_multimedia_appendix_2_replacement.docx`.

The 2026-08-10 snapshot appendices carried five of the six corrections (Health Care
heading, both author lists, the corrected Healthcare IT News title, the 2026 NSI
edition) but not the sixth, since `multimedia_appendix_1.md` line 5 still quoted
"Socio-Technical Artifacts". That line was changed to "Sociotechnical Artifacts" and
the appendices rebuilt with `./scripts/build_paper.sh --format all`. `references.bib`
is unchanged since the snapshot, so the rebuild reproduces the copyeditor's
bibliography corrections exactly rather than reintroducing anything.

All six verified in the built DOCX files afterward. The rebuilt appendix 1 differs from
the snapshot by that one sentence and nothing else; the rebuilt appendix 2 is textually
identical to the snapshot.

`paper.docx`, `paper.pdf`, and the appendix 2 outputs were reverted after the build. No
source feeding them changed, so their diffs were nondeterministic build noise, and the
archived appendix 2 replacement was re-taken from the restored tracked artifact so its
provenance matches byte for byte.

Deliberately not raised: Appendix 1 spells out "three components", "five-step", and
"six-step" where the article uses numerals. JMIR appears to treat appendices as
author-supplied rather than copyediting them to house style, and these are internal to
the appendix rather than contradicting the article, so they are discretionary. They
could be changed at no extra cost during the rebuild.

## Remaining before sign-off

- The publication date appears twice: "published 21.Aug.2026" in the end matter, and
  again in the copyright line on the final page as "Originally published in the
  Interactive Journal of Medical Research (https://www.i-jmr.org/), 21.Aug.2026." Both
  need updating when the hold lifts. The copyright line is the one likely to be missed,
  since it sits apart from the publication date field.
- Confirm the corrected title in the final version. The notification offers the option
  to request a view of the final version before scheduling. Worth taking, given that
  the title error appeared after a round that had it right.
- Confirm the title metadata field specifically. The author can correct the typeset
  title but cannot see or edit metadata, and the corrupted title appeared in the
  notification email, which is generated from metadata.
