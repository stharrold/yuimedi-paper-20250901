#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.47"]
# ///
"""Capture reader-facing evidence of the TrendMD listing for i-JMR ms#96541.

Loads real non-JMIR article pages that carry the TrendMD widget, each in a fresh
browser context, and watches the widget's own recommendations response. When
campaign 6nFy9EFs (or our title, in either form) is served, it saves:

  widget.png     element screenshot of the rendered #trendmd-suggestions widget
  item.png       element screenshot of our listing inside the widget
  viewport.png   viewport with the listing scrolled into view
  fullpage.png   the whole host page, so the publisher site is visible
  widget.html    outerHTML of the rendered widget
  response.json  the recommendations response the widget rendered from
  request.json   that request's URL, method, headers, and body
  meta.json      host URL, final URL, page title, UTC time, item position/record

Every load is logged to attempts.jsonl, hit or miss. The script never clicks and
never requests a clickUrl/url, since each registers a billed $1 click.

Run from the repo root (not from inside ARCHIVED/, which would create a .venv):

  uv run --script ARCHIVED/20260810_IJMR-Copyediting/20260923_trendmd_evidence_capture.py --hours 48
"""

from __future__ import annotations

import argparse
import asyncio
import json
import random
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path

from playwright.async_api import async_playwright

CAMPAIGN_ID = "6nFy9EFs"
TITLE_RE = re.compile(
    r"Health ?care Analytics Challenges|Health Care Analytics Challenges|(3|Three)-Pillar Framework",
    re.I,
)
RECS_RE = re.compile(r"rev\.trendmd\.com/ad-slots/[^/]+/recommendations")

# Non-JMIR article pages that carry the TrendMD widget (verified 2026-09-23; BMJ Health &
# Care Informatics, J Med Ethics, BMJ Open Quality, and BMC do NOT carry it). Topical mix:
# the listing was served most beside digital-health and research-ethics/data-governance hosts.
HOSTS = [
    "https://innovations.bmj.com/content/8/2/129",  # digital front door
    "https://innovations.bmj.com/content/7/2/414",  # ML hospital discharge predictions
    "https://innovations.bmj.com/content/12/2/126",  # anthropomorphic generative AI
    "https://innovations.bmj.com/content/11/4/207",  # why digital innovation fails
    "https://doi.org/10.1136/bmjopen-2020-044289",  # patient involvement in health data governance
    "https://doi.org/10.1136/bmjopen-2022-065803",  # locum doctors, routinely collected workforce data
    "https://doi.org/10.1136/bmjopen-2026-117423",  # hospital workforce shortages
    "https://academic.oup.com/jamiaopen/article/doi/10.1093/jamiaopen/ooaf167/8415655",  # LLM clinical analytics
]

# Headless Chrome announces "HeadlessChrome" and is stopped at the host's Cloudflare check
# ("Just a moment..."); an ordinary desktop Chrome user agent passes (verified 2026-09-23).
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"

OUT = Path(__file__).resolve().parent / "20260923_TrendMD-Evidence"


def now() -> datetime:
    return datetime.now(UTC)


TEST_CAMPAIGN: str | None = None  # --test-campaign: exercise the capture path on another campaign


def is_ours(item: dict) -> bool:
    if TEST_CAMPAIGN:
        if TEST_CAMPAIGN == "*":  # any other publisher's paid item
            return item.get("linkingType") == 1
        return item.get("campaignId") == TEST_CAMPAIGN
    return item.get("campaignId") == CAMPAIGN_ID or bool(TITLE_RE.search(item.get("title") or ""))


def log_attempt(record: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "attempts.jsonl").open("a") as fh:
        fh.write(json.dumps(record) + "\n")


async def load_once(browser, host: str) -> dict:
    """Load one host page in a fresh context; capture evidence if our listing is served."""
    ts = now()
    rec: dict = {"utc": ts.isoformat(timespec="seconds"), "host": host}
    context = await browser.new_context(
        viewport={"width": 1280, "height": 900}, locale="en-US", user_agent=USER_AGENT
    )
    page = await context.new_page()
    try:
        async with page.expect_response(
            lambda r: bool(RECS_RE.search(r.url)) and r.request.method == "POST", timeout=45000
        ) as resp_info:
            await page.goto(host, wait_until="domcontentloaded", timeout=60000)
        resp = await resp_info.value
        rec["final_url"] = page.url
        rec["page_title"] = await page.title()
        rec["api_status"] = resp.status
        items = await resp.json()
        rec["n_items"] = len(items)
        rec["external_campaigns"] = [
            i.get("campaignId") for i in items if i.get("linkingType") == 1
        ]
        ours = [i for i in items if is_ours(i)]
        rec["ours"] = bool(ours)
        if not ours:
            return rec

        item = ours[0]
        await page.wait_for_selector("#trendmd-suggestions a", timeout=20000)
        await page.wait_for_timeout(2500)
        slug = re.sub(r"[^a-z0-9]+", "-", re.sub(r"^https?://", "", page.url).lower()).strip("-")[
            :60
        ]
        hit_dir = OUT / f"hit_{ts.strftime('%Y%m%dT%H%M%SZ')}_{slug}"
        hit_dir.mkdir(parents=True, exist_ok=True)

        widget = page.locator("#trendmd-suggestions")
        await widget.scroll_into_view_if_needed()
        await page.wait_for_timeout(800)
        await widget.screenshot(path=str(hit_dir / "widget.png"))
        (hit_dir / "widget.html").write_text(await widget.evaluate("el => el.outerHTML"))

        # Our listing's anchor, matched by its rendered title text.
        anchor = widget.locator(
            "a",
            has_text=item["title"][:60] if TEST_CAMPAIGN else re.compile(TITLE_RE.pattern, re.I),
        ).first
        if await anchor.count():
            await anchor.scroll_into_view_if_needed()
            await page.wait_for_timeout(500)
            card = anchor.locator("xpath=ancestor::*[self::li or self::div][1]")
            target = card if await card.count() else anchor
            await target.screenshot(path=str(hit_dir / "item.png"))
            await page.screenshot(path=str(hit_dir / "viewport.png"))
            rec["item_rendered"] = True
        else:
            rec["item_rendered"] = False
        await page.screenshot(path=str(hit_dir / "fullpage.png"), full_page=True)

        req = resp.request
        (hit_dir / "response.json").write_text(json.dumps(items, indent=2))
        (hit_dir / "request.json").write_text(
            json.dumps(
                {
                    "url": req.url,
                    "method": req.method,
                    "headers": await req.all_headers(),
                    "post_data": req.post_data,
                },
                indent=2,
            )
        )
        meta = {
            "captured_utc": ts.isoformat(timespec="seconds"),
            "host_url": host,
            "final_url": page.url,
            "page_title": rec["page_title"],
            "item_position": items.index(item) + 1,
            "items_in_response": len(items),
            "item": {
                k: v for k, v in item.items() if k not in ("clickUrl", "url", "impressionUrl")
            },
            "note": "Unmodified page. No clicks were made; tracking URLs omitted because requesting them bills a click.",
        }
        (hit_dir / "meta.json").write_text(json.dumps(meta, indent=2))
        rec["hit_dir"] = hit_dir.name
        return rec
    except Exception as exc:  # noqa: BLE001 - log every failure mode and keep sampling
        rec["error"] = f"{type(exc).__name__}: {str(exc)[:200]}"
        try:
            rec["page_title"] = await page.title()
        except Exception:  # noqa: BLE001
            pass
        return rec
    finally:
        await context.close()


async def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--hours", type=float, default=48.0, help="stop after this many hours")
    ap.add_argument("--target-hits", type=int, default=3, help="stop after this many captures")
    ap.add_argument(
        "--min-hosts",
        type=int,
        default=2,
        help="...spanning at least this many distinct host pages",
    )
    ap.add_argument(
        "--min-gap", type=float, default=90.0, help="minimum seconds between page loads"
    )
    ap.add_argument(
        "--max-gap", type=float, default=210.0, help="maximum seconds between page loads"
    )
    ap.add_argument(
        "--max-loads", type=int, default=0, help="stop after this many loads (0 = no limit)"
    )
    ap.add_argument("--headed", action="store_true", help="show the browser window")
    ap.add_argument(
        "--test-campaign",
        help="treat this campaignId as ours, to test the capture path (use with --out)",
    )
    ap.add_argument(
        "--out", help="output directory (default: 20260923_TrendMD-Evidence next to this script)"
    )
    args = ap.parse_args()
    global OUT, TEST_CAMPAIGN
    TEST_CAMPAIGN = args.test_campaign
    if args.out:
        OUT = Path(args.out).resolve()

    deadline = now() + timedelta(hours=args.hours)
    hits: list[dict] = []
    loads = 0
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(channel="chrome", headless=not args.headed)
        try:
            while now() < deadline:
                for host in random.sample(HOSTS, len(HOSTS)):
                    rec = await load_once(browser, host)
                    loads += 1
                    log_attempt(rec)
                    print(
                        json.dumps(
                            {
                                k: rec.get(k)
                                for k in ("utc", "host", "ours", "n_items", "error", "hit_dir")
                            }
                        ),
                        flush=True,
                    )
                    if rec.get("hit_dir"):
                        hits.append(rec)
                    distinct = {h["host"] for h in hits}
                    if (
                        (len(hits) >= args.target_hits and len(distinct) >= args.min_hosts)
                        or (args.max_loads and loads >= args.max_loads)
                        or now() >= deadline
                    ):
                        print(
                            json.dumps(
                                {
                                    "done": True,
                                    "loads": loads,
                                    "hits": len(hits),
                                    "hosts_with_hits": sorted(distinct),
                                }
                            ),
                            flush=True,
                        )
                        return
                    await asyncio.sleep(random.uniform(args.min_gap, args.max_gap))
        finally:
            await browser.close()
    print(json.dumps({"done": True, "loads": loads, "hits": len(hits)}), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
