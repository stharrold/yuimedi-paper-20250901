# Reply to JMIR Author Experience Manager: Final Visual Abstract Artifacts

**Manuscript:** i-JMR ms#96541, Interact J Med Res 2026;15:e96541, doi:10.2196/96541
**Drafted:** 2026-08-31
**Thread:** "Visual abstract questionnaire 96541", this would be the 6th message
**To:** natalia.march@jmir.org (Natalia March, Author Experience Manager)
**Subject:** Re: Visual abstract questionnaire 96541

| | |
|---|---|
| Thread of record | `20260826_Email_IJMR-Visual-Abstract.pdf` (5 messages) |
| Prompted by | `20260831_Email_JMIR-Production-Editor.pdf` (Laura, 2026-08-31 12:19 PM) |
| Draft 1 as received | `20260825_IJMR_Visual_Abstract.pdf` |
| Feedback as sent | `20260825_IJMR_Visual_Abstract_commented.pdf` |
| Assessment | `abstract-visual-video/20260825T200314Z_visual-abstract_critical-assessment.md` |

> **Address note.** This thread runs to the **gmail** address. Laura's production thread
> runs to the **yuimedi** address (cc gmail) and is separate. Neither sees the other by
> default.

---

## Why this matters beyond archiving

Natalia acknowledged both corrections on 2026-08-25 at 7:40 PM ("I've noted both requested
text corrections from your attached PDF") but **never sent a revised proof back**. The one
author review round was spent on draft 1.

The corrected artwork therefore reached production unseen by the author, and per Laura it
is already uploaded as the ToC image with publication proceeding on 2026-08-31. Obtaining
the final file is the only way to confirm the 2 corrections landed and that nothing else
moved.

---

## Message to send

```text
Hi Natalia,

Thank you for making both corrections, and for turning the draft around so quickly.

I heard from Laura today that the visual abstract has been uploaded as the ToC image
and that the paper is going forward for publication, so I wanted to close the loop
here.

Could you send me a copy of the final visual abstract for my records? The PDF plus a
high-resolution image version would be ideal if both are available. I would like to
have the final artwork on file, and it would be good to see the corrected version.

One related question while I have you: what use of the visual abstract is permitted
outside the article itself, for example in conference slides or on our organization's
website? I want to make sure I attribute and use it correctly.

Thank you again for putting this together. It came out well.

Best,
Samuel
```

---

## Notes on the drafting (not sent)

**Framed as a records request, not a verification demand.** Asking Natalia to confirm the
corrections were applied would read as distrust of a colleague who has already said she
made them, and there is a small risk a pointed question reopens what she considers a closed
thread. Requesting the file achieves the same end: verification happens on our side when it
arrives. The line "it would be good to see the corrected version" carries the intent
without the edge.

**The reuse question is a genuine secondary ask, not padding.** The article is open access,
but the ToC image's licensing is worth having in writing, given the Yuimedi Lifelong Author
Ad pointing at us.yuimedi.com and the likelihood of conference use. Kept to one sentence so
it cannot crowd out the primary request.

### Deliberately not raised

- **That a revised proof should have been circulated for confirmation.** True, and worth
  remembering for papers 2 and 3, but raising it now changes nothing about an artifact
  already in production, and would sour a thread that ended warmly.
- **The em dash item**, omitted from the original feedback on purpose and still moot.

---

## Verification plan

Run this when the file arrives, or as soon as the article is live, whichever comes first:
the published ToC image is itself a usable copy.

1. Confirm "This viewpoint" replaced "This study".
2. Confirm "framework" now follows "(HITL-KG)".
3. Diff the rest of the text layer against `20260825_IJMR_Visual_Abstract.pdf` to catch
   anything else that moved during the revision.
4. Hash the embedded images (`pdfimages -png` then `shasum -a256`) against the draft to
   confirm the artwork itself was not regenerated.

Archive the result as `20260831_IJMR_Visual_Abstract_final.pdf`, alongside the draft and
the annotated copy.

> **Method reminder.** Use `pdftotext -layout` for phrase diffing, but plain `pdftotext`
> for anything order-sensitive. PDF text extraction returns object creation order, not
> visual order, which produced a false "storage before validation" reading on draft 1.

---

## Lesson for papers 2 and 3

The one-round policy was written to cap *author* iterations, but as run it silently also
capped *verification*. Acknowledging a correction and demonstrating it are different
things, and the process gave no mechanism for the second.

Cheap fix next time: when sending feedback, ask in the same message for the revised proof
as confirmation only, stated explicitly as not constituting a new round.

---

## As sent: delta against the draft above

**Sent 2026-09-01 10:16 AM EDT**, cc to the yuimedi address, which usefully bridges this
thread and Laura's production thread for the first time. Sent copy of record:
`20260901_Email-Reply_IJMR_Visual-Abstract-Final-Artifacts.pdf` (6 messages).

**The article published on schedule.** The sent version replaces the draft's "Laura tells
me it is going forward for publication" with the fact: "I'm glad to see that the paper has
been published at https://www.i-jmr.org/2026/1/e96541/ with the visual abstract." The
2026-08-11 hold arrangement did its job, and the sponsored tweet fires against the intended
graphic rather than a placeholder.

Other changes, all improvements:

- **Dropped** "and it would be good to see the corrected version." Removes the last trace
  of a verification motive, leaving a clean records request. Costs nothing, because the
  published ToC image is now itself a verifiable copy.
- **Reuse question sharpened** from "what use is permitted" to "are there any terms and
  conditions I need to follow", and names Yuimedi's website explicitly rather than "our
  organization's". A direct question is likelier to get a usable written answer.
- "It came out beautifully" for "It came out well."

## Verification: now possible without the vendor

The plan below was written for whichever came first, the file or the live article. The
article won. The published ToC image can be pulled directly from
https://www.i-jmr.org/2026/1/e96541/ and checked against
`20260825_IJMR_Visual_Abstract.pdf` without waiting on Natalia's reply.
