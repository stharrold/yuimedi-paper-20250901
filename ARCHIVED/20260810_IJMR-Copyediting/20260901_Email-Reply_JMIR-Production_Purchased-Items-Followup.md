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
| TrendMD Promotion | $250.00 | 24 Jul | **LIVE** on the article page |
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

**TrendMD: live.** Three scripts load from `js.trendmd.com` (`trendmd-ns.min.js`,
`polyfills.js`, `widget.js`) and the page contains `div#trendmd-suggestions` plus a
rendered `trendmd-links-...` container.

**Lifelong Author Ad: live.** The page carries an anchor to `https://us.yuimedi.com/`.

**PubMed Now!: deposited, but frozen at acceptance.** PMID **42497119**, PMC **PMC13528883**,
status "PubMed - as supplied by publisher".

| | PubMed / PMC | Article page metadata |
|---|---|---|
| Title | "**Healthcare** Analytics Challenges: A **Three-Pillar** Framework..." | "**Health Care** ... **3-Pillar** ..." |
| Date | 2026 Jul 13 | `citation_date` 2026-08-31 |
| Issue | (blank) | `citation_issue` 1 |

The article page's own `citation_*` tags are all correct, so this is purely a matter of the
PubMed deposit not having been refreshed after publication. That makes it an easy ask: the
correct metadata already exists on JMIR's side.

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

3. TrendMD. I can see the widget is live on the article. Is there any reporting on the
   campaign I can expect, and does it run for a set period?

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

**Revised after verification.** The first draft asked whether TrendMD and the author ad
were live, and when they would begin. Both are demonstrably live, so those questions would
have wasted her time and made the note read as inattentive. They became confirmations with a
narrower follow-up each: reporting for TrendMD, URL updatability for the ad.

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
