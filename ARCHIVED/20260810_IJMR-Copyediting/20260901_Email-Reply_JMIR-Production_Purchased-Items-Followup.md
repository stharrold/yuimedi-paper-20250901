# Reply to JMIR Production Editor: Follow-Up on Purchased Items

**Manuscript:** i-JMR ms#96541, Interact J Med Res 2026;15:e96541, doi:10.2196/96541
**Published:** 2026-08-31, https://www.i-jmr.org/2026/1/e96541/
**Drafted:** 2026-09-01
**To:** laura.mcreynolds@jmir.org (Laura McReynolds, Production Editor)
**Cc:** production@jmir.org
**Subject:** Re: JMIR Interactive Journal of Medical Research Manuscript #96541 - Pre-Production Queries

> **Address note.** Laura's thread runs to the **yuimedi** address (cc gmail). Natalia's
> visual abstract thread runs to **gmail**. This is the production thread.

---

## The complete purchase list

Taken from the receipts, not from memory. The project notes had recorded only 2 of these.

| Item | Amount | Receipt | Status |
|---|---|---|---|
| Article Processing Fee (less Viewpoints discount) | $1,588.00 | 24 Jul, `IJMR-96541-RCPT-001056433` | Delivered, published |
| TrendMD Promotion | $250.00 | 24 Jul | **Unknown**, largest add-on |
| Sponsored Tweet Campaign | $99.00 | 24 Jul | **Unknown**, timing was the whole reason for the hold |
| Lifelong Author Ad in Article | $99.00 | 24 Jul | **Unknown**, banner to us.yuimedi.com |
| PubMed Now! Ahead of Print | $50.00 | 24 Jul | Delivered, but **record is stale** |
| Visual Abstract | $545.00 | 4 Aug, `IJMR-RCPT-001056626` | Delivered, live as ToC |

Total: **$2,631.00**, of which **$1,043.00** is optional promotion and services.

## What was verified before drafting

**PubMed Now! did deliver.** PMID **42497119**, deposited with pubdate 2026-07-13 (the
acceptance date), status "PubMed - as supplied by publisher", which is the ahead-of-print
state. PMC ID **PMC13528883** assigned.

**But both records carry the pre-copyedit title and the acceptance date:**

| | PubMed / PMC | Published article |
|---|---|---|
| Title | "**Healthcare** Analytics Challenges: A **Three-Pillar** Framework..." | "**Health Care** Analytics Challenges: A **3-Pillar** Framework..." |
| Date | 2026 Jul 13 | 2026 Aug 31 |
| Issue | (blank) | 1 |

This matters more than a cosmetic mismatch. PubMed is the primary discovery route in
biomedicine and the source reference managers pull from, so the stale title propagates into
other people's bibliographies. It also splits discoverability: a search on the real title
will not match the indexed one. There is history here too, since the 2026-08-13 proof round
already caught JMIR typesetting corrupting the title in the metadata field the author cannot
see or edit, which is the same field that feeds Crossref and PubMed.

**Not verifiable from here:** the article page returns HTTP 202 with an empty body to
scripted requests (publisher bot wall), so TrendMD placement, the Lifelong Author Ad banner,
and the ToC image need a look in a browser. Worth doing before sending, so the questions
below can be narrowed to what is genuinely missing.

---

## Message to send

```text
Hi Laura,

Thank you for seeing this through, and for suggesting the hold in the first place. The
article went live with the visual abstract in place, which is exactly the outcome I was
hoping for.

Now that it has published, could I ask about follow-up on the promotional items I
purchased with the article? There were five, and I want to make sure each is on track:

1. PubMed Now! (Ahead of Print). This did deposit, and the record is up as PMID
   42497119 with PMC13528883. However, both PubMed and PMC still carry the
   pre-copyediting title, "Healthcare Analytics Challenges: A Three-Pillar Framework...",
   and the 13 July acceptance date rather than the final "Health Care Analytics
   Challenges: A 3-Pillar Framework..." and the publication date. Could the deposit be
   refreshed to the final version? I ask because reference managers pull from PubMed, so
   the earlier title would end up in other people's citations.

2. TrendMD Promotion. When does this campaign begin, and is there any reporting on it I
   can expect?

3. Sponsored Tweet Campaign. When is the tweet scheduled? I would like to be able to
   amplify it from our own accounts when it goes out.

4. Lifelong Author Ad in Article. Could you confirm this is live, and let me know
   whether the destination URL can be updated later if our site structure changes?

5. Visual Abstract. Complete, and it looks great. I have asked Natalia separately for a
   copy of the final file for my records.

No urgency on any of this beyond the PubMed metadata, which I would like to get right
before it propagates further.

Thank you again for everything on this one.

Best,
Samuel
```

---

## Notes on the drafting (not sent)

**Opens by crediting her.** The hold was Laura's own recommendation and it worked. Saying
so is both true and the right footing for reopening a thread she closed with "it has been a
pleasure working with you."

**PubMed is placed first and given a reason.** It is the only item with a demonstrated
problem rather than an open question, and it is the only one that degrades with time as the
stale metadata spreads. Explaining *why* (reference managers pull from PubMed) turns it from
a pedantic correction into an obvious fix.

**Each remaining item is one specific question.** A list of five vague "any update?" items
invites one vague reply. Asking when the tweet is scheduled, whether the ad is live, and
whether TrendMD reports, each gets a discrete answer.

**The tweet question is framed as wanting to amplify**, not as checking up. That is honest
and gives her a reason to tell you the date.

**The Lifelong Author Ad question about updating the URL later** is the genuinely
forward-looking one: "lifelong" implies a long horizon, and us.yuimedi.com may not be stable
across that span. Better asked now than discovered later.

### Deliberately not raised

- **Laura's unanswered 2026-08-11 commitment** to confirm "by Thursday" whether an
  unpromoted tweet fires automatically at publication. Moot now: the article published with
  the visual abstract already in place, so the failure mode that question guarded against
  cannot occur. Item 3 asks the forward-looking version instead.
- **That the project notes tracked only 2 of the 5 purchases.** Our own record-keeping gap,
  not hers.

---

## Repo follow-up, separate from the email

`CLAUDE.md` records only the Sponsored Tweet Campaign and Lifelong Author Ad under
purchased promotion. It should list all five, with amounts and receipt numbers, so a future
session does not have to re-derive them from redacted receipt images. TrendMD at $250 is the
single largest add-on and was absent entirely.
