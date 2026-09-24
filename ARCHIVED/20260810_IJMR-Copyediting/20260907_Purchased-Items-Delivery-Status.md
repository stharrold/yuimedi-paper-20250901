# Purchased Items: Delivery Status as of 2026-09-07

**Manuscript:** i-JMR ms#96541, Interact J Med Res 2026;15:e96541, doi:10.2196/96541
**Published:** 2026-08-31
**Checked:** 2026-09-07, via Playwright (the article page and PubMed both bot-wall `curl`)
**Prompted by:** `20260907_Email-Reply_JMIR-Production_Purchased-Items-Followup.pdf`

> **SUPERSEDED 2026-09-15: all 6 items delivered.** See the RESOLUTION section at the end.
> The body below is kept as a dated record of what was observable on 2026-09-07, and 2 of
> its conclusions (the tweet and TrendMD rows) turned out to be wrong.

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


---

## RESOLUTION, 2026-09-15: every purchased item delivered

Source: Laura McReynolds' 3 replies to the 2026-09-08 follow-up, archived in
`20260909_Email_JMIR-Production_Delivery.pdf` (18 messages; Gmail renders times in CEST),
plus the author's X capture `20260901_X-Twitter-JmirPublications.pdf`.

| Item | Amount | Final status | Evidence |
|---|---|---|---|
| Article Processing Fee | $1,588.00 | Delivered | Published 2026-08-31 |
| Visual Abstract | $545.00 | Delivered | Unchanged from above |
| Lifelong Author Ad | $99.00 | Delivered | Unchanged from above |
| PubMed Now! Ahead of Print | $50.00 | **Delivered, fixed 2026-09-09** | Duplicate entry merged; 42497119 redirects to **42684405** |
| Sponsored Tweet Campaign | $99.00 | **Delivered 2026-09-01** | https://x.com/jmirpub/status/2094846699487609125, 5 promoted ads |
| TrendMD Promotion | $250.00 | **Running** (to ~2026-12-02) | Marketing confirmation via Laura; campaign data requested from the rep |

### Timeline

- **Sep 8, 10:45 EDT:** follow-up sent.
- **Sep 8, 11:39 EDT:** Laura forwards items 2 and 3 to marketing and escalates PubMed to her
  manager, who takes it to the platform managers and PubMed.
- **Sep 8, 16:35 EDT:** tweet link plus marketing's ads dashboard: "there are 5 ads running
  now", 152 total link clicks. TrendMD "has started and is estimated to run until December 2";
  marketing is asking the rep for data.
- **Sep 9, 15:52 EDT:** PubMed resolved. "It looks like there was a duplicate entry which was
  causing it not to refresh."

### PubMed: independently verified 2026-09-15

- https://pubmed.ncbi.nlm.nih.gov/42497119/ redirects to https://pubmed.ncbi.nlm.nih.gov/42684405/.
- PMID 42684405 reads "Health Care Analytics Challenges: A 3-Pillar Framework...", cited as
  "2026 Aug 31:15:e96541", no longer "Online ahead of print".
- A PubMed search on the DOI returns only 42684405; `esummary` for 42497119 now errors
  ("cannot get document summary").
- PMC13528883's `citation_pmid` meta tag is 42684405.

So the "cache or slight delay" explanation of 2026-09-01 was not the cause. The acceptance-time
deposit and the published-version deposit had created 2 records, and the stale one was the
one PubMed kept serving. Only a person at JMIR could have found that; no amount of waiting
would have fixed it.

**Residual (cosmetic):** the i-JMR article page and its `/citations` tab still display
"PMID: 42497119" and link `ncbi.nlm.nih.gov/pubmed/42497119` (the page's embedded data also
carries `pmid:42497119`). The link works through the redirect. The EndNote, BibTeX and RIS
exports carry no PMID at all, so the retired ID does not reach reference managers.

### Sponsored tweet: my 2026-09-07 "No evidence" was wrong

The tweet posted 2026-09-01 (19:55 CEST, 13:55 EDT), the day marketing said it would. The
author's capture shows 23.4K views on the organic post. The dashboard shows 5 promoted
variants, all Active, all carrying the visual abstract as the card image:

1. "Healthcare analytics has a knowledge problem."
2. "What if your healthcare organization could preserve the expertise of every analytics..."
3. "What if every validated query could become institutional knowledge?..."
4. "Who validates the AI when the experts leave?..."
5. "What happens when your healthcare analytics experts leave?..."

**Why 3 channels showed nothing:** the Tweetations tab still reports "no tweets available"
on 2026-09-15, and promoted posts did not surface on the @jmirpub profile timeline either.
Tweetations evidently does not capture JMIR's own promoted posts.

**Independently verified 2026-09-15** (Playwright, logged out): the status URL is publicly
viewable, shows "7:55 PM · Sep 1, 2026" and 23.4K views, and its card ("Read the full
article!", "From i-jmr.org") links to https://www.i-jmr.org/2026/1/e96541/. The card image
(`pbs.twimg.com/media/HRJhxZeXEAEh70J`, 1561x877) is the corrected visual abstract
center-cropped to 16:9, with "This viewpoint calls for the ... (HITL-KG) framework" legible.
**Not independently verifiable:** the 5 promoted variants, their Active status, and the 152
link clicks, which rest on marketing's dashboard image alone. The caveat stated above
("a *promoted* tweet may not be captured") was the true explanation, and the later claim
that a zero there "does mean something" was wrong.

### TrendMD: the 2026-09-08 correction held

The campaign had started. The absence from 3 widgets was sampling, exactly as the
correction said. The only open thread is the campaign report marketing requested.

### Lessons for papers 2 and 3

1. **Every "missing" paid promotion here was in fact running.** Author-side observation
   produced 2 false negatives out of 2. For any paid placement (tweet, TrendMD), ask for
   the vendor dashboard or report; do not infer non-delivery from any public page.
2. **A PubMed record that will not refresh may be a duplicate, not a lag.** If the
   Ahead-of-Print record still shows acceptance metadata a week after publication, ask
   production to check for a duplicate entry rather than waiting.
3. **After a PMID merge, the publisher's page keeps the old ID.** Check the article page
   and exports for the retired PMID.


---

## UPDATE, 2026-09-23: TrendMD campaign observed directly, and misconfigured

Source: Laura's 2026-09-15 3:53 PM reply (`20260916_Email_JMIR-Production_Metrics.pdf`),
plus direct sampling of the TrendMD recommendation API.

### Laura's reply

- **PMID fixed.** Verified 2026-09-23 on the article page: it shows PMID 42684405, links
  `ncbi.nlm.nih.gov/pubmed/42684405`, and the retired 42497119 appears nowhere in the HTML.
- **TrendMD data (from marketing, 2026-09-10)** is a table headed **"The Continuity Trap in
  Data Science Health Research"**: 56,661 inbound sponsored impressions, 25 clicks (0.04% CTR),
  $1.00 CPC, $25.00 spent. That title is a different Viewpoint: Adebamowo C et al.,
  J Med Internet Res 2026;e98699, doi 10.2196/98699 (PMID 42616578), published 2026-08-19.
  No author in common with ours.

### Direct observation: the campaign is running

TrendMD's widget fetches its list with
`POST https://rev.trendmd.com/ad-slots/<slot-id>/recommendations`, body
`{"npis":[],"doctorSpecialties":[],"sourceMetadata":{"title":...,"doi":...},"startTime":<ms>}`
and headers `x-revops-version`, `x-revops-source-type: 2`, `x-revops-session-id` (any UUID),
`x-revops-source-url`. It returns 10 items; `linkingType: 0` is the host publisher's own
(organic) content, `linkingType: 1` is another publisher's paid campaign, each with a
`campaignId`. Replaying that request from a BMJ Innovations page (slot
`d4a1ec99-9e42-40c8-b978-0900a2367aae`) with varied topical host titles, 89 calls, no clicks:

| Host titles | Our item served |
|---|---|
| Digital health, analytics maturity, informatics (2 runs) | 11/48, 4/21 |
| Research ethics, secondary data use | 14/20 |

**Our article is promoted as campaign `6nFy9EFs`.** Delivery is now positively observed,
which author-side widget checks could never establish.

### The creative is wrong

The served item (id `3406cbc2-fcac-4d2f-9020-a724e9c8d115`, publicationId
`62573720-f78a-42f8-8292-b255f2d682ca`):

- `title`: "Healthcare Analytics Challenges: A Three-Pillar Framework..." (the **pre-copyedit**
  title, the same stale acceptance-time metadata PubMed carried)
- `subtitle` (byline): **"Clement Adebamowo"**, the first author of the Continuity Trap paper
- `publicationName` / `publicationAbbreviatedName`: the article title, not the journal;
  `authors` empty; `publicationDate` null
- Served far more often beside research-ethics hosts than beside our own topic, which
  suggests targeting keyed to the Continuity Trap paper (small sample; suggestive only)

Reading: one campaign mixing the two articles. The Sep 10 report may be this campaign under
the other article's label, or a different campaign entirely; only marketing can say.

**Not verified:** the click destination. The `clickUrl` is a session-bound
`rev.trendmd.com/open/...` token and following it registers a real $1 click against the
campaign, so it was deliberately not followed. Ask marketing instead.

**Serving stopped later the same morning.** At 2026-09-23 13:10 UTC the same API replay returned our item 0 of 10 times (it had been 14 of 20 about 20 minutes earlier with the same host titles), and 21 reloads of the real BMJ Innovations page (https://innovations.bmj.com/content/8/2/129) never served it; that page renders exactly the items the API returns, so the item was not served rather than hidden. Cause unknown: daily budget pacing, a frequency cap on this browser after sampling, or a campaign change. The hit responses above were not saved, and they came from replayed requests with synthetic host titles, so they are not reader-facing evidence.

**Evidence standard before emailing marketing:** a screenshot of a real publisher page rendering the listing, with the page URL, UTC time, and the matching recommendations response. Captured by `20260923_trendmd_evidence_capture.py` (this folder) into `20260923_TrendMD-Evidence/`. Hold the reply to Laura until it exists.

**Capture run started 2026-09-23 13:37 UTC** (detached, `caffeinate -i`, PID in `20260923_TrendMD-Evidence/run.pid`): up to 48 h, stops after 3 captures across 2 or more host pages. Hosts are 8 real article pages verified to carry the widget (4 BMJ Innovations, 3 BMJ Open, 1 JAMIA Open); every load is logged to `attempts.jsonl`, so the log also records how often the listing is served. The capture path was tested on another publisher's item before launch (all 8 artifacts written; the test output was discarded).

### Next

Reply drafted: `20260923_Email-Reply_JMIR-Production_TrendMD-Campaign.md`. Asks marketing
to confirm the article campaign `6nFy9EFs` links to, correct the title, byline, and journal
fields, and confirm whether the Sep 10 report is this campaign.


---

## EVIDENCE CAPTURED, 2026-09-24: the two campaigns' bylines are swapped

**Capture:** 2026-09-24 03:10:53 UTC, on a real, unmodified BMJ Open article page,
https://bmjopen.bmj.com/content/11/3/e044289 ("Public and patient involvement in health data
governance (DATAGov)..."). No clicks. Artifacts:
`20260923_TrendMD-Evidence/hit_20260924T031053Z_bmjopen-bmj-com-content-11-3-e044289/`
(widget, item, viewport, and full-page PNGs; the rendered response; request; meta).
Attachment copies (byte-identical): `20260924_TrendMD-Listing_BMJ-Open_widget.png` and
`20260924_TrendMD-Listing_BMJ-Open_item.png`.

The same rendered widget shows both campaigns, side by side, with each other's byline:

| Campaign | Position | Title shown | Byline shown |
|---|---|---|---|
| `6nFy9EFs` (ours) | 6 of 10 | Healthcare Analytics Challenges: A Three-Pillar Framework Connecting Analytics Maturity, Workforce Agility, and Technical Enablement (pre-copyedit title) | Clement Adebamowo |
| `MJ6iVWT7` | 8 of 10 | The Continuity Trap in Data Science Health Research | Samuel Harrold |

Both records also carry the article title in `publicationName` (no journal) and no date.
So the fault is a swap between the two JMIR campaigns set up around the same time, plus the
stale acceptance-time title on ours. The Sep 10 report, labeled "The Continuity Trap", is
plausibly `MJ6iVWT7`, not ours.

**Run summary** (`20260923_TrendMD-Evidence/attempts.jsonl`, stopped once this capture
existed): 519 loads, 2026-09-23 13:37 UTC to 2026-09-24 12:32 UTC; 490 succeeded (29
timeouts); 342 carried other publishers' paid items, 176 distinct campaigns. Hosts: BMJ
Innovations 256, BMJ Open 189, JAMIA Open 45.

| Campaign | Served in successful loads | When |
|---|---|---|
| `6nFy9EFs` (ours) | 1 of 490 | 2026-09-24 03:10 UTC |
| `MJ6iVWT7` (Continuity Trap) | 8 of 490 | 2026-09-24 00:02 to 03:42 UTC, on 2 BMJ Open pages and BMJ Innovations |

Both served only in a window just after 00:00 UTC, consistent with daily budget pacing
(nothing in the 10.5 h before). Only ours triggered screenshots; the other campaign's 7
further sightings are logged by campaign ID only.

**Still not verified:** where each listing's click goes. Asked of marketing in the reply.

**Next:** reply to Laura updated with the URL, time, and attached screenshots:
`20260923_Email-Reply_JMIR-Production_TrendMD-Campaign.md`.
