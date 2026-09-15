# Reply to JMIR Production Editor: Follow-Up on Purchased Items

**Manuscript:** i-JMR ms#96541, Interact J Med Res 2026;15:e96541, doi:10.2196/96541
**Published:** 2026-08-31, https://www.i-jmr.org/2026/1/e96541/
**Drafted:** 2026-09-01, revised same day after browser verification
**To:** laura.mcreynolds@jmir.org (Laura McReynolds, Production Editor)
**Cc:** production@jmir.org
**Subject:** Re: JMIR Interactive Journal of Medical Research Manuscript #96541 - Pre-Production Queries

> **Address note.** Laura's thread runs to the **yuimedi** address (cc gmail). Natalia's
> visual abstract thread runs to **gmail**. This is the production thread.

---

## The complete purchase list

Taken from the receipts, not from memory. The project notes had recorded only 2 of these.

| Item | Amount | Receipt | Verified status |
|---|---|---|---|
| Article Processing Fee (less Viewpoints discount) | $1,588.00 | 24 Jul, `IJMR-96541-RCPT-001056433` | Published |
| TrendMD Promotion | $250.00 | 24 Jul | Widget live; **outbound campaign not yet observed** |
| Sponsored Tweet Campaign | $99.00 | 24 Jul | **Unverifiable from here** |
| Lifelong Author Ad in Article | $99.00 | 24 Jul | **LIVE**, points to us.yuimedi.com |
| PubMed Now! Ahead of Print | $50.00 | 24 Jul | Deposited, but **record is stale** |
| Visual Abstract | $545.00 | 4 Aug, `IJMR-RCPT-001056626` | **LIVE and correct** |

Total: **$2,631.00**, of which **$1,043.00** is optional promotion and services.

## Verification performed 2026-09-01

`curl` gets HTTP 202 with an empty body from the article page (publisher bot wall), so this
was done by driving a real browser via Playwright, which clears the challenge.

**Visual abstract: delivered, and both corrections landed.** The `og:image` and
`twitter:image` both resolve to
`https://asset.jmir.pub/assets/243dedcac7689084b11e62d576effb1d.png`, a 1200x900 PNG that is
the visual abstract itself. Archived here as `20260901_IJMR_Visual_Abstract_final.png`
(sha256 `1708c9a08d57ca50...`). It now reads:

> "This **viewpoint** calls for the Human-in-the-Loop Knowledge Governance (HITL-KG)
> **framework** to shift knowledge from human memory to durable artifacts"

Both requested edits are present, the "Proof. Not for circulation." watermarks are gone, and
nothing else changed: triple threat wording, the 6-step cycle and its order, the 3 pillars,
the summary bar, and a citation block carrying the copyedited title. The verification plan
in `20260831_Email-Reply_IJMR_Visual-Abstract-Final-Artifacts.md` is satisfied without
waiting on Natalia's reply. Note this image is also the social card
(`twitter:card = summary_large_image`), so it is what the sponsored tweet will carry.

**TrendMD: widget live, outbound campaign not yet visible.** Three scripts load from
`js.trendmd.com` and the page renders `div#trendmd-suggestions` with 10 recommendations
(5 from JMIR journals, 5 from other publishers). That is the *inbound* half: other people's
articles shown to our readers.

The $250 buys the *outbound* half, our article placed into other publishers' widgets. That
is not visible on our own page, so it was tested directly by following a cross-link and
checking the destination's widget:

| Page checked | Topical fit | Our article present? |
|---|---|---|
| BMJ Innovations 8(2):129, "Healthcare's new frontier: the digital front door" (reached by clicking our own widget, landing URL carried `utm_medium=reward&utm_source=trendmd`) | adjacent | No |
| J Med Internet Res 2024;26:e56316, Snowdon, "Digital Maturity as a Predictor of Quality and Safety Outcomes" | very close, and cited by our paper | No |

The Snowdon check is the more meaningful one: its widget is populated with digital-maturity
papers including several from JMIR journals, which is exactly the slot our article would
compete for. It is absent.

**This is not evidence of a failure.** The article published 2026-08-31, one day before the
check. TrendMD needs to index new content, campaigns ramp, and recommendation sets rotate
and personalize (this was a clean browser with no history). Two negative observations cannot
prove a campaign is not running. But it is enough to ask Laura a concrete question with a
date attached rather than a vague "any reporting?"

*Note the tracking links (`rev.trendmd.com/open/...`) are session-bound and return
`{"message":"Invalid encrypted payload"}` to `curl`. They must be clicked from within the
page session.*

**Lifelong Author Ad: live.** The page carries an anchor to `https://us.yuimedi.com/`.

**PubMed Now!: deposited; PubMed stale, PMC already corrected.**
PMID **42497119**, PMC **PMC13528883**.

| Source | Title | Date | State |
|---|---|---|---|
| PubMed record page | "Healthcare ... Three-Pillar" | 2026 Jul 13, "Online ahead of print" | **Stale** |
| PMC article page | "Health Care ... 3-Pillar" | `citation_publication_date` 2026 Aug 31 | **Correct** |
| i-JMR article page | "Health Care ... 3-Pillar" | `citation_date` 2026-08-31, issue 1 | Correct |

**Correction to an earlier note in this file.** A first pass reported PubMed *and* PMC as
both stale. That was wrong about PMC. The error came from reading NCBI's `esummary` API,
which returned the original July deposit fields and lags the rendered article record.
Fetching the PMC page directly shows the corrected title and the 31 Aug date.

Method lesson: for NCBI, `esummary` is an index and can trail the live record. Verify
citation state on the rendered page, not only through the API. The sent email states the
split correctly.

**Not verifiable:** the sponsored tweet. It would appear on @jmirpub, and X gates
unauthenticated access.

---

## Message to send

```text
Hi Laura,

Thank you for seeing this through, and for suggesting the hold in the first place. The
article went live with the visual abstract in place, which is exactly the outcome I was
hoping for, and the graphic came out really well.

Now that it has published, could I ask about follow-up on a few of the items I purchased
with the article? I have checked the article page, so most of this is confirmation
rather than a question:

1. PubMed record. The Ahead of Print deposit went through and the article is up as PMID
   42497119 with PMC13528883. However, both PubMed and PMC still show the
   pre-copyediting title, "Healthcare Analytics Challenges: A Three-Pillar Framework...",
   along with the 13 July acceptance date and no issue number. The article page itself
   has all the correct metadata, so I think this just needs the deposit refreshed to the
   published version. Could that be arranged? I ask because reference managers pull from
   PubMed, so the earlier title would otherwise propagate into other people's citations.

2. Sponsored Tweet Campaign. Is this scheduled yet? I would like to amplify it from our
   own accounts when it goes out, so knowing the date would help.

3. TrendMD. I can see the widget is live on my article page. I have not yet seen my
   article appear in TrendMD widgets elsewhere, including on closely related JMIR
   articles, though I appreciate it is only a day since publication. Could you tell me
   when the promotion campaign begins, how long it runs, and whether I can expect any
   reporting on it?

4. Lifelong Author Ad. Confirmed live and pointing to us.yuimedi.com, thank you. Given
   that it is lifelong, could you let me know the process for updating the destination
   URL later if our site structure changes?

Nothing here is urgent except the PubMed metadata, which I would like to correct before
it spreads further.

Thank you again for everything on this one.

Best,
Samuel
```

---

## Notes on the drafting (not sent)

**Revised twice after verification.** The first draft asked whether TrendMD and the author
ad were live. Both are demonstrably live, so those questions would have wasted her time. The
second revision then split TrendMD in half after testing the cross-network side: the widget
being live is the inbound half, and the paid outbound placement is a separate thing that is
not yet observable. Item 3 now asks for a start date and duration, which is answerable,
rather than implying the service has failed, which the evidence does not support.

**PubMed leads, and the ask is framed as easy.** It is the only item with a demonstrated
defect, the only one that worsens with time, and, now that the page metadata is confirmed
correct, the only one where we can tell her the fix is a redeposit rather than a
re-keying. Saying "the article page itself has all the correct metadata" preempts the
possibility of the request being read as a complaint about the copyediting.

**The visual abstract is dropped as a numbered item** and folded into the opening as praise.
It is complete and verified, so listing it would pad a list whose whole value is that every
entry needs an answer.

**"I have checked the article page"** is stated up front. It signals the questions are
narrow and considered, which is what makes a five-item list land as diligence rather than
as a chore.

### Deliberately not raised

- **Laura's unanswered 2026-08-11 commitment** to confirm "by Thursday" whether an
  unpromoted tweet fires automatically at publication. Moot: the article published with the
  visual abstract already in place, so the failure mode cannot occur. Item 2 asks the
  forward-looking version instead.
- **That the project notes tracked only 2 of the 5 purchases.** Our record-keeping gap.

---

## Repo follow-up, separate from the email

`CLAUDE.md` records only the Sponsored Tweet Campaign and Lifelong Author Ad under purchased
promotion. It should list all 5 with amounts and receipt numbers, so a future session does
not have to re-derive them from redacted receipt images. TrendMD at $250 is the largest
add-on and was absent entirely.

Also worth recording: the article page bot-walls scripted requests (HTTP 202, empty body),
but Playwright clears it, and `og:image` is the reliable route to the published visual
abstract at full resolution.


---

## As sent: delta against the draft above

**Sent 2026-09-01 11:14 AM EDT**, cc to the gmail address, so both addresses now see this
thread. Sent copy of record:
`20260901_Email-Reply_JMIR-Production_Purchased-Items-Followup.pdf` (12 messages).

**Item 1 was materially improved in the sending.** Rather than asserting the record is wrong
and asking for a refresh, the sent version quotes the exact PubMed citation line and the
exact target string, links both PubMed and PMC, and asks "do you happen to know if [it] will
update". That is better on 2 counts: it is a process question rather than a defect report,
and it is precisely the framing the evidence supports, since PMC has already corrected while
PubMed has not. It also, correctly, does not claim PMC is stale.

Other changes:

- **Item 2 adds a specific question** about whether the tweet comes from
  https://x.com/jmirpub, and names LinkedIn as the amplification channel rather than the
  vaguer "our own accounts".
- **Dropped** "Nothing here is urgent except the PubMed metadata, which I would like to
  correct before it spreads further." Removes the urgency framing entirely. Defensible: the
  numbered questions carry their own weight, and PMC being already correct lowers the stakes.
- **Dropped** the "the article page itself has all the correct metadata" line, which was
  written to preempt the request being read as a complaint about copyediting. Not needed
  once the item is phrased as a question.

**Open items now awaiting Laura:** the PubMed refresh, the tweet schedule and account, the
TrendMD campaign start/duration/reporting, and the process for updating the author ad's
destination URL.
