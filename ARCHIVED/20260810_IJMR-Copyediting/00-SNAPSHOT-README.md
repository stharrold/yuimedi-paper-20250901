# i-JMR Copyediting Round, ms#96541 (2026-08-10)

Persistent snapshot of the repository state used to produce the artifacts for the
i-JMR copyediting round of manuscript 96541, "Health Care Analytics Challenges."

This directory is self-contained: it holds the correspondence that triggered the
round, every source file the artifacts were built from, the tooling that built
them, the artifacts themselves, and a checksum manifest. Nothing here needs the
surrounding repository to be audited or rebuilt.

Note on convention: `ARCHIVED/CLAUDE.md` asks for zipped archives, but submission
packages are kept as loose directories (see `ARCHIVED/20260712_IJMR-Submission/`)
so that individual files can be uploaded to the journal without unpacking. This
package follows that precedent.

## Correspondence

| File | Contents |
|:---|:---|
| `20260810_Email_IJMR-96541_Copyediting.pdf` | Request to review the copyedited manuscript, 2026-08-10 05:47, from donotreply@exeterpremedia.com (Editage for JMIR). Reply-to copyedit@editage.com, copyediting@jmir.org. |
| `96541.pdf` | **The copyedited proof.** 14 pages, typeset in i-JMR house style by Antenna House. This is the document the copyeditor's queries refer to. Scanned clean of active content and injection phrases 2026-08-10. |
| `96541_modified.pdf` | The proof after the author's Kriyadocs edits, reviewed before Approve and Submit. |
| `20260810_Email-Reply_IJMR-96541_Copyediting.txt` | Reply to the copyeditor confirming approval and how each query was handled. |
| `20260728_Email_JMIR-Production-Editor.pdf` | Production thread with Laura McReynolds (Production Editor): pre-production queries, the AJE-as-ToC policy, the Lifelong Author Ad URL, and the purchase of the in-house visual abstract service. |
| `20260805_Email_IJMR_Visual_Abstract*.pdf` | Natalia March's visual abstract questionnaire request, the service overview, and the form. States the 3-week turnaround, the single author review round, and the standard-ToC-then-swap fallback. |
| `20260806_visual-abstract-questionnaire-plaintext.txt` | The questionnaire answers as submitted 2026-08-06. |
| `20260810_Email_JMIR-Production-Editor.pdf` | The same production thread after the author's 2026-08-10 reply raising the publication-vs-visual-abstract timing conflict (6 messages). |
| `20260810_Email-Reply_JMIR-Production_Visual-Abstract-Timing.txt` | That reply as sent, with the timing arithmetic and the reasoning for declining the AJE graphic as a Multimedia Appendix. |
| `20260810_JMIR_Data-Sharing-Policy.pdf` | The KB page whose template 4 the data availability statement now uses. |

The proof carries the assigned publication details:

| Field | Value |
|:---|:---|
| DOI | 10.2196/96541 |
| Citation | Interact J Med Res 2026;15:e96541 |
| URL | https://www.i-jmr.org/2026/1/e96541 |
| Publication date | **21.Aug.2026** |
| Edited by | Matthew Balcarras |
| Peer reviewed by | Moez Hamedani, Xiaoni Zhang |

Deadline: **2 to 3 business days** from 2026-08-10, so approximately
**2026-08-12 to 2026-08-13**. An extension can be requested from the copyeditor
if the publication schedule allows.

## How this round is actually submitted

The email specifies that copyediting is completed **in JMIR's Kriyadocs web
system** via the emailed link, in Google Chrome, and that only the submitting
user (Samuel Thomas Harrold) can edit the manuscript. The workflow is:

1. Open the edited file through the link in the email.
2. Address every copyeditor comment in the system.
3. For anything that cannot be done in the system, add a query addressed to the
   copyeditor.
4. Click "Approve," complete the steps on the page, then "Submit."

After submission, author access to the article is closed until the final proofs.

This means the round is **not** completed by uploading a rebuilt DOCX to a
submission form, as the R1 and R2 rounds were. The artifacts in this directory
serve two purposes: as the authoritative local record of the manuscript state,
and as attachments or reference copies if the copyeditor asks for a file rather
than in-system edits.

## Package contents

**Build inputs** (what the artifacts are generated from)

`paper.md`, `metadata.yaml`, `references.bib`, `citation-style-ama.csl`,
`reference.docx`, `multimedia_appendix_1.md`, `multimedia_appendix_2.md`,
`multimedia_appendix_*.caption.txt`, `figures/`

`figures/` holds the Mermaid sources (`*.mmd`), the rendered build images
(`*.mmd.png`, `*.mmd.svg`), the 1200px journal upload copies (`*.figure.png`),
the caption text, and the styling and Puppeteer config used to render them.

**Build tooling** (what turns inputs into artifacts)

`build_paper.sh` (also in `scripts/`), `scripts/`, `Containerfile`,
`pyproject.toml`, `uv.lock`, `.pre-commit-config.yaml`

**Project metadata**

`CLAUDE.md`, `README.md`, `CITATION.cff`, `.zenodo.json`, `LICENSE`, `NOTICE`

**Generated artifacts**

`paper.docx`, `paper.pdf`, `paper.tex`, `paper.html`,
`multimedia_appendix_1.{docx,pdf,html}`, `multimedia_appendix_2.{docx,pdf,html}`

**Audit records**

| File | Contents |
|:---|:---|
| `BUILD-PROVENANCE.md` | Tool versions, git state, and exact steps to reproduce the artifacts |
| `MANIFEST.sha256` | SHA-256 of every file in this package |
| `20260810_copyedit-changes.md` | What changed this round and why, plus open queries |
| `20260810_copyedit-source-changes.diff` | The literal source diff applied this round |

## Which files are uploadable

If the copyeditor requests files rather than in-system edits:

| Artifact | Use |
|:---|:---|
| `paper.docx` | The manuscript. JMIR reads the title from `docProps/core.xml`, which is set correctly. |
| `paper.pdf` | Read-only reference copy, 24 pages. |
| `multimedia_appendix_1.docx` | Worked Validated Query Triple examples. |
| `multimedia_appendix_2.docx` | Full Three-Pillar rubric with scoring anchors. |
| `figures/architecture.figure.png` | Figure 1, sized to the 1200px maximum. |
| `figures/knowledge-cycle.figure.png` | Figure 2, sized to the 1200px maximum. |

Do not upload `paper.tex` or `paper.html`; they are build byproducts retained
here for reproducibility only.
