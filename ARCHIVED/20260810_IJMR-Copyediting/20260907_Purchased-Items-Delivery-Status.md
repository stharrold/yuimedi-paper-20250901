# Purchased Items: Delivery Status as of 2026-09-07

**Manuscript:** i-JMR ms#96541, Interact J Med Res 2026;15:e96541, doi:10.2196/96541
**Published:** 2026-08-31
**Checked:** 2026-09-07, via Playwright (the article page and PubMed both bot-wall `curl`)
**Prompted by:** `20260907_Email-Reply_JMIR-Production_Purchased-Items-Followup.pdf`

## Laura's commitments, made 2026-09-01

Two messages, 12:05 PM and 2:00 PM:

| Item | Her answer | Date given |
|---|---|---|
| PubMed record | "a cache or slight delay at Pubmed's end. Our team will monitor this and check in/reach out to PubMed if the record is not updated in the next couple of days" | ~3 Sep |
| Sponsored Tweet | Marketing says it "will go out today" | 1 Sep |
| TrendMD | Marketing says it "will likely start tomorrow or Thursday" | 2 to 3 Sep |
| Lifelong Author Ad | Email support@jmir.org to change the destination URL | answered, no action pending |

She closed with an explicit invitation: "feel free to reach out to me later this week if
anything is delayed beyond the given Thursday date, and I can check in on it with the
relevant parties." Today is Monday 2026-09-07, so that invitation is live for every dated
item below.

## Status

| Item | Amount | Status | Evidence |
|---|---|---|---|
| Article Processing Fee | $1,588.00 | **Delivered** | Published 2026-08-31, correct copyedited title and citation |
| Visual Abstract | $545.00 | **Delivered** | Live as ToC image; PDF + 5000x3750 PNG received 2026-09-01; both corrections verified; CC-BY reuse terms in writing |
| Lifelong Author Ad | $99.00 | **Delivered** | Anchor to https://us.yuimedi.com/ present on the article page, re-verified 2026-09-07 |
| PubMed Now! Ahead of Print | $50.00 | **Partial** | Deposit fired (PMID 42497119, PMC13528883), but the record is still the acceptance-time one |
| Sponsored Tweet Campaign | $99.00 | **No evidence** | JMIR's own Tweetations tab reports zero tweets, All Time |
| TrendMD Promotion | $250.00 | **No evidence** | Article still absent from the closest topical match's widget |

**3 of 6 fully delivered. $349 of promotion unverified, plus the $50 PubMed item incomplete.**

## Detail on the 3 unresolved items

### PubMed Now!: deposit fired, record never refreshed

The PubMed *page* (not just the `esummary` API, which lags) still reads, on 2026-09-07:

- Title: "**Healthcare** Analytics Challenges: A **Three-Pillar** Framework..." (pre-copyedit)
- Citation: "2026 Jul 13."
- Still flagged "Online ahead of print"
- No volume or issue

PMC (PMC13528883) has had the correct title and the 31 Aug date since at least 2026-09-01.
So the 2 databases have been out of step for a week, which weakens the "cache or slight
delay" reading: a cache would not hold one record and not the other for 6 days. It is now
4 days past Laura's "couple of days," which is exactly the trigger she asked to be told
about.

### Sponsored Tweet: no trace

The article page has a **Tweetations** tab (JMIR's own tweet tracking, at
https://www.i-jmr.org/2026/1/e96541/tweetations). Set to **All Time**, it reports:

> "There are currently no tweets available for this article within the specified range."

Six days after "will go out today."

**Caveat, stated plainly:** Tweetations depends on JMIR's own harvesting pipeline, and a
*promoted* tweet may not be captured the same way an organic mention is. So this is strong
evidence, not proof. It is nonetheless JMIR's own instrument reporting nothing.

**What only the author can check:** https://x.com/jmirpub directly. X gates unauthenticated
access, so it cannot be verified from here.

### TrendMD: still not placed

Re-ran the 2026-09-01 baseline test on J Med Internet Res 2024;26:e56316 (Snowdon, digital
maturity), the closest topical match and a paper ours cites. Our article is still absent
from its widget.

**This check is stronger than it was on 1 Sep**, because the widget's second tier has
*changed* between the 2 dates (it now carries BMJ items that were not there before). The
widget is therefore refreshing rather than serving a stale cache, and ours still does not
appear in it. Due date was 2 to 3 Sep.

Caveat: recommendation sets rotate and personalize, and this is 1 sample. Absence is not
proof. But 2 negative observations 6 days apart, across a demonstrated refresh, is a
reasonable basis for asking.

## Recommended next step

Laura asked to be told if anything slipped past Thursday. All 3 items did. A single short
follow-up on her thread covering PubMed, the tweet, and TrendMD is exactly what she
invited, and she is the stated escalation point for cross-team issues.

Before sending, check https://x.com/jmirpub for the tweet, since that is the one item that
can only be confirmed from a logged-in account and a positive result would remove it from
the list.


---

## CORRECTION, 2026-09-08: the TrendMD evidence is weaker than stated above

A Chrome print-to-PDF of the Snowdon page taken by the author
(`~/Downloads/202609/2024_Snowden.pdf`, 26 pp) contains a widget item that **none of the
Playwright captures did**:

> "Mortality and transitions-of-care after COVID-19 hospitalization among US Medicare
> patients: a retrospective claims analysis. **Brought to you by Pfizer Medical Affairs,
> EM-USA-CVD-0102**"

That is a *sponsored* placement, carrying the "Brought to you by" sponsor label, which is
what a paid TrendMD promotion looks like from the reader's side.

**Consequence:** sponsored slots vary by impression, session or viewer. The same page,
loaded by 2 parties on the same day, served a sponsored item to one and not the other.
Therefore the observation "our article is absent from these 3 widgets" **cannot distinguish
between the campaign not running and the campaign running but not served in our samples.**
The earlier framing in this file overstated it.

What survives the correction:

- The claim in the email, "I'm having trouble finding the article in TrendMD widgets on
  related pages", remains accurate. It reports the author's experience, not a conclusion.
- The organic (unsponsored) recommendation lists are stable enough to compare across dates,
  and ours has never appeared in one. That is still suggestive, but organic placement is
  not what the $250 buys.
- Asking marketing to confirm the campaign is running remains the right move. It is now the
  *only* way to settle it, since author-side observation provably cannot.

**Do not attach the widget screenshots to the email as proof.** They no longer support a
"not delivered" claim, and presenting them as such would be wrong on the facts. Keep them
as a dated record of what the organic lists contained.

### Method note for papers 2 and 3

A negative observation in an ad or recommendation network is nearly worthless as evidence,
because delivery is probabilistic per impression. Positive observation works (seeing your
item placed proves delivery); absence does not disprove it. The reliable check is the
campaign report from the vendor, not the rendered page.

Also: the word "TrendMD" appears nowhere as text on a page carrying the widget. The
branding is a logo image, so `grep -i trendmd` on extracted page text returns 0 on a page
where the widget is fully rendered. Detect it by `div#trendmd-suggestions` in the DOM or by
the "We also recommend" / "Powered by" strings instead.
