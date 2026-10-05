#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.47", "pillow>=10"]
# ///
"""Capture reader-facing evidence of the TrendMD listings for i-JMR ms#96541.

Loads real non-JMIR article pages that carry the TrendMD widget, each in a fresh
browser context, and reads the widget's own recommendations response. When a
watched campaign is served (ours, 6nFy9EFs, or the Continuity Trap campaign,
MJ6iVWT7, whose bylines were swapped with ours on 2026-09-24), it saves:

  browser_widget.png  one-screen (1440x900 @2x) view with the widget centred, under a
                      capture header showing the full URL and UTC time
  browser_top.png     the same for the top of the page (article title, journal)
  widget.png          element screenshot of the rendered #trendmd-suggestions widget
  item_<cid>.png      element screenshot of each watched listing
  page.mhtml          full-page archive (Chrome MHTML snapshot)
  widget.html         outerHTML of the rendered widget
  response.json       the recommendations response the widget rendered from
  request.json        that request's URL, method, headers, and body
  meta.json           URL, title, UTC time, each watched item and its status
  MANIFEST.sha256     SHA-256 of every file above

The capture header is drawn onto the image after capture and labelled as such; the
page itself is not modified apart from declining the cookie banner ("Reject All"),
which the header and meta.json both state. Every load, hit or miss, is appended to
attempts.jsonl with the external campaigns served and the response's SHA-256.
run_meta.json records the script hash, git commit, browser and library versions,
and arguments; summary.json is written on exit, including on SIGTERM/SIGINT.

The script never clicks a listing and never requests a clickUrl/url: each
registers a billed $1 click.

Run from the repo root (not from inside ARCHIVED/, which would create a .venv):

  caffeinate -i uv run --script ARCHIVED/20260810_IJMR-Copyediting/20260923_trendmd_evidence_capture.py \\
      --window 23:30-05:00 --hours 14
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.metadata
import json
import os
import platform
import random
import re
import signal
import subprocess
import sys
import uuid
from datetime import UTC, datetime, time, timedelta
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.async_api import async_playwright

OUR_CAMPAIGN = "6nFy9EFs"
WATCH = {
    OUR_CAMPAIGN: "Health Care Analytics Challenges (Harrold, i-JMR 2026;15:e96541)",
    "MJ6iVWT7": "The Continuity Trap in Data Science Health Research (Adebamowo et al., JMIR 2026;e98699)",
}
TITLE_RE = re.compile(r"Health ?care Analytics Challenges|(3|Three)-Pillar Framework", re.I)
RECS_RE = re.compile(r"rev\.trendmd\.com/ad-slots/[^/]+/recommendations")

# Non-JMIR article pages that carry the TrendMD widget (verified 2026-09-23; BMJ Health &
# Care Informatics, J Med Ethics, BMJ Open Quality, and BMC do NOT carry it). Topical mix:
# both watched listings were served beside digital-health and data-governance hosts.
HOSTS = [
    "https://innovations.bmj.com/content/8/2/129",  # digital front door
    "https://innovations.bmj.com/content/7/2/414",  # ML hospital discharge predictions
    "https://innovations.bmj.com/content/12/2/126",  # anthropomorphic generative AI
    "https://innovations.bmj.com/content/11/4/207",  # why digital innovation fails
    "https://bmjopen.bmj.com/content/11/3/e044289",  # health data governance (DATAGov)
    "https://doi.org/10.1136/bmjopen-2022-065803",  # locum doctors, workforce data
    "https://bmjopen.bmj.com/content/16/7/e117423",  # hospital workforce shortages
    "https://academic.oup.com/jamiaopen/article/doi/10.1093/jamiaopen/ooaf167/8415655",
]

# Headless Chrome announces "HeadlessChrome" and is stopped at the host's Cloudflare
# check ("Just a moment..."); an ordinary desktop Chrome user agent passes.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
)
VIEWPORT = {"width": 1440, "height": 900}
SCALE = 2
COOKIE_REJECT = re.compile(r"^\s*(Reject All|Reject all|Reject All Cookies|Decline All)\s*$")
FONT_PATHS = [
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

HERE = Path(__file__).resolve().parent
OUT: Path = HERE / f"{datetime.now(UTC):%Y%m%d}_TrendMD-Evidence"
TEST_CAMPAIGN: str | None = None
STOP = asyncio.Event()


def now() -> datetime:
    return datetime.now(UTC)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def watched(item: dict) -> str | None:
    """Return the watch key for an item, or None."""
    if TEST_CAMPAIGN:
        if TEST_CAMPAIGN == "*" and item.get("linkingType") == 1:
            return item.get("campaignId")
        return item.get("campaignId") if item.get("campaignId") == TEST_CAMPAIGN else None
    cid = item.get("campaignId")
    if cid in WATCH:
        return cid
    if TITLE_RE.search(item.get("title") or ""):
        return cid or OUR_CAMPAIGN
    return None


def byline(item: dict) -> str:
    sub = item.get("subtitle") or {}
    return (sub.get("content") if isinstance(sub, dict) else "") or item.get("authors") or ""


def listing_status(cid: str, item: dict) -> str:
    """Classify a watched listing as 'correct' or a description of what is wrong."""
    title, by = item.get("title") or "", byline(item)
    problems = []
    if cid == OUR_CAMPAIGN:
        if not re.search(r"Health Care Analytics Challenges: A 3-Pillar", title):
            problems.append("pre-copyedit title")
        if "Harrold" not in by:
            problems.append(f"byline '{by}'")
    elif cid == "MJ6iVWT7":
        if "Adebamowo" not in by:
            problems.append(f"byline '{by}'")
    if (item.get("publicationName") or "") == title:
        problems.append("journal field holds the title")
    return "correct" if not problems else "; ".join(problems)


def log_attempt(record: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "attempts.jsonl").open("a") as fh:
        fh.write(json.dumps(record) + "\n")


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for p in FONT_PATHS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default(size=size)


def add_capture_header(png: Path, url: str, captured: datetime, note: str) -> None:
    """Draw a browser-toolbar-style capture header (URL + UTC time) above a screenshot."""
    img = Image.open(png).convert("RGB")
    w = img.width
    bar_h = 52 * SCALE
    canvas = Image.new("RGB", (w, img.height + bar_h), (222, 225, 230))
    canvas.paste(img, (0, bar_h))
    d = ImageDraw.Draw(canvas)
    pad = 12 * SCALE
    right = f"Captured {captured:%Y-%m-%d %H:%M:%S} UTC  |  {note}"
    f_url, f_right = font(15 * SCALE), font(12 * SCALE)
    right_w = d.textlength(right, font=f_right)
    field = (pad, 9 * SCALE, w - pad * 2 - int(right_w), bar_h - 9 * SCALE)
    d.rounded_rectangle(
        field, radius=17 * SCALE, fill=(255, 255, 255), outline=(200, 203, 208), width=SCALE
    )
    text = url
    max_w = field[2] - field[0] - 2 * pad
    while d.textlength(text, font=f_url) > max_w and len(text) > 20:
        text = text[:-2]
    if text != url:
        text = text[:-1] + "…"
    d.text((field[0] + pad, bar_h // 2), text, font=f_url, fill=(32, 33, 36), anchor="lm")
    d.text((w - pad, bar_h // 2), right, font=f_right, fill=(80, 84, 90), anchor="rm")
    d.line([(0, bar_h - 1), (w, bar_h - 1)], fill=(180, 184, 190), width=SCALE)
    canvas.save(png, optimize=True)


async def dismiss_cookie_banner(page) -> str:
    for sel in ("#onetrust-reject-all-handler", "button#truste-consent-required"):
        btn = page.locator(sel)
        if await btn.count() and await btn.first.is_visible():
            await btn.first.click(timeout=5000)
            await page.wait_for_timeout(800)
            return f"rejected ({sel})"
    btn = page.get_by_role("button", name=COOKIE_REJECT)
    if await btn.count() and await btn.first.is_visible():
        await btn.first.click(timeout=5000)
        await page.wait_for_timeout(800)
        return "rejected (button text)"
    return "none found"


async def capture(page, context, resp, items: list, hits: dict[str, dict], ts: datetime) -> Path:
    slug = re.sub(r"[^a-z0-9]+", "-", re.sub(r"^https?://", "", page.url).lower()).strip("-")[:60]
    hit_dir = OUT / f"hit_{ts:%Y%m%dT%H%M%SZ}_{slug}"
    hit_dir.mkdir(parents=True, exist_ok=True)
    await page.wait_for_selector("#trendmd-suggestions a", timeout=20000)
    await page.wait_for_timeout(2500)
    cookie = await dismiss_cookie_banner(page)
    note = (
        "headless Chrome; cookie banner declined, page otherwise unmodified"
        if cookie.startswith("rejected")
        else "headless Chrome, page unmodified"
    )

    widget = page.locator("#trendmd-suggestions")
    await widget.evaluate("el => el.scrollIntoView({block: 'center'})")
    await page.wait_for_timeout(1000)
    await page.screenshot(path=str(hit_dir / "browser_widget.png"))
    add_capture_header(hit_dir / "browser_widget.png", page.url, ts, note)
    await widget.screenshot(path=str(hit_dir / "widget.png"))
    (hit_dir / "widget.html").write_text(await widget.evaluate("el => el.outerHTML"))

    for cid, item in hits.items():
        anchor = widget.locator("a", has_text=(item.get("title") or "")[:50]).first
        if await anchor.count():
            card = anchor.locator("xpath=ancestor::*[self::li or self::div][1]")
            target = card if await card.count() else anchor
            await target.screenshot(path=str(hit_dir / f"item_{cid}.png"))

    await page.evaluate("window.scrollTo(0, 0)")
    await page.wait_for_timeout(800)
    await page.screenshot(path=str(hit_dir / "browser_top.png"))
    add_capture_header(hit_dir / "browser_top.png", page.url, ts, note)

    try:
        cdp = await context.new_cdp_session(page)
        snap = await cdp.send("Page.captureSnapshot", {"format": "mhtml"})
        (hit_dir / "page.mhtml").write_text(snap["data"])
    except Exception as exc:  # noqa: BLE001 - archive is best-effort
        (hit_dir / "page.mhtml.error.txt").write_text(f"{type(exc).__name__}: {exc}\n")

    req = resp.request
    (hit_dir / "response.json").write_text(json.dumps(items, indent=2) + "\n")
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
        + "\n"
    )
    meta = {
        "captured_utc": ts.isoformat(timespec="seconds"),
        "page_url": page.url,
        "page_title": await page.title(),
        "items_in_response": len(items),
        "cookie_banner": cookie,
        "watched": {
            cid: {
                "label": WATCH.get(cid, "test campaign"),
                "position": items.index(item) + 1,
                "title": item.get("title"),
                "byline": byline(item),
                "publicationName": item.get("publicationName"),
                "status": listing_status(cid, item),
                "record": {
                    k: v for k, v in item.items() if k not in ("clickUrl", "url", "impressionUrl")
                },
            }
            for cid, item in hits.items()
        },
        "note": "No clicks were made; tracking URLs omitted because requesting them bills a click. "
        "The capture header on browser_*.png is drawn after capture.",
    }
    (hit_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    lines = [
        f"{sha256_file(p)}  ./{p.name}"
        for p in sorted(hit_dir.iterdir())
        if p.name != "MANIFEST.sha256"
    ]
    (hit_dir / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
    return hit_dir


async def load_once(browser, host: str, run_id: str, n: int) -> dict:
    ts = now()
    rec: dict = {"run_id": run_id, "n": n, "utc": ts.isoformat(timespec="seconds"), "host": host}
    context = await browser.new_context(
        viewport=VIEWPORT, device_scale_factor=SCALE, locale="en-US", user_agent=USER_AGENT
    )
    page = await context.new_page()
    try:
        async with page.expect_response(
            lambda r: bool(RECS_RE.search(r.url)) and r.request.method == "POST", timeout=45000
        ) as resp_info:
            await page.goto(host, wait_until="domcontentloaded", timeout=60000)
        resp = await resp_info.value
        body = await resp.body()
        items = json.loads(body)
        rec.update(
            status="ok",
            final_url=page.url,
            page_title=await page.title(),
            api_status=resp.status,
            response_sha256=sha256_bytes(body),
            n_items=len(items),
            external=[
                [i.get("campaignId"), (i.get("title") or "")[:80], byline(i)]
                for i in items
                if i.get("linkingType") == 1
            ],
        )
        hits = {}
        for i in items:
            key = watched(i)
            if key and key not in hits:
                hits[key] = i
        rec["watched"] = {cid: listing_status(cid, i) for cid, i in hits.items()}
        if hits:
            rec["hit_dir"] = (await capture(page, context, resp, items, hits, ts)).name
        return rec
    except Exception as exc:  # noqa: BLE001 - log every failure mode and keep sampling
        title = ""
        try:
            title = await page.title()
        except Exception:  # noqa: BLE001
            pass
        rec.update(
            status="challenge" if "just a moment" in title.lower() else "error",
            page_title=title,
            error=f"{type(exc).__name__}: {str(exc)[:200]}",
        )
        return rec
    finally:
        await context.close()


def in_window(window: tuple[time, time] | None, t: datetime) -> bool:
    if not window:
        return True
    start, end = window
    cur = t.time()
    return start <= cur < end if start < end else (cur >= start or cur < end)


def parse_window(s: str | None) -> tuple[time, time] | None:
    if not s:
        return None
    a, b = s.split("-")
    return time.fromisoformat(a), time.fromisoformat(b)


def git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(HERE), "rev-parse", "HEAD"], text=True
        ).strip()
    except Exception:  # noqa: BLE001
        return "unknown"


async def main() -> None:
    global OUT, TEST_CAMPAIGN
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--hours", type=float, default=48.0, help="stop after this many hours")
    ap.add_argument("--window", help="only load pages within this UTC window, e.g. 23:30-05:00")
    ap.add_argument(
        "--target-hits", type=int, default=3, help="stop after this many captures of our listing"
    )
    ap.add_argument(
        "--min-gap", type=float, default=60.0, help="minimum seconds between page loads"
    )
    ap.add_argument(
        "--max-gap", type=float, default=150.0, help="maximum seconds between page loads"
    )
    ap.add_argument(
        "--max-loads", type=int, default=0, help="stop after this many loads (0 = no limit)"
    )
    ap.add_argument(
        "--restart-every", type=int, default=40, help="restart the browser every N loads"
    )
    ap.add_argument("--headed", action="store_true", help="show the browser window")
    ap.add_argument("--test-campaign", help="treat this campaignId ('*' = any external) as watched")
    ap.add_argument(
        "--out", help="output directory (default: YYYYMMDD_TrendMD-Evidence next to this script)"
    )
    args = ap.parse_args()
    TEST_CAMPAIGN = args.test_campaign
    if args.out:
        OUT = Path(args.out).resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    window = parse_window(args.window)

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, STOP.set)

    run_id = uuid.uuid4().hex[:12]
    started = now()
    deadline = started + timedelta(hours=args.hours)
    (OUT / "run.pid").write_text(f"{os.getpid()}\n")
    stats = {"loads": 0, "ok": 0, "challenge": 0, "error": 0, "our_hits": 0, "captures": 0}
    host_fail: dict[str, int] = {}
    host_cooldown: dict[str, datetime] = {}

    async with async_playwright() as pw:
        launch = {"channel": "chrome", "headless": not args.headed}
        browser = await pw.chromium.launch(**launch)
        meta = {
            "run_id": run_id,
            "started_utc": started.isoformat(timespec="seconds"),
            "args": vars(args),
            "hosts": HOSTS,
            "watch": WATCH,
            "script": str(Path(__file__).resolve().relative_to(HERE.parent.parent)),
            "script_sha256": sha256_file(Path(__file__).resolve()),
            "git_head": git_head(),
            "browser_version": browser.version,
            "playwright_version": importlib.metadata.version("playwright"),
            "pillow_version": importlib.metadata.version("pillow"),
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "user_agent": USER_AGENT,
            "viewport": VIEWPORT,
            "device_scale_factor": SCALE,
        }
        (OUT / f"run_meta_{run_id}.json").write_text(json.dumps(meta, indent=2) + "\n")
        print(json.dumps({"run_id": run_id, "out": str(OUT)}), flush=True)
        try:
            while not STOP.is_set() and now() < deadline:
                if not in_window(window, now()):
                    try:
                        await asyncio.wait_for(STOP.wait(), timeout=60)
                    except TimeoutError:
                        pass
                    continue
                ready = [h for h in HOSTS if host_cooldown.get(h, started) <= now()]
                if not ready:
                    await asyncio.sleep(60)
                    continue
                for host in random.sample(ready, len(ready)):
                    if STOP.is_set() or now() >= deadline or not in_window(window, now()):
                        break
                    if not browser.is_connected() or (
                        stats["loads"] and stats["loads"] % args.restart_every == 0
                    ):
                        try:
                            await browser.close()
                        except Exception:  # noqa: BLE001
                            pass
                        browser = await pw.chromium.launch(**launch)
                    stats["loads"] += 1
                    rec = await load_once(browser, host, run_id, stats["loads"])
                    log_attempt(rec)
                    stats[rec["status"]] += 1
                    if rec["status"] == "ok":
                        host_fail[host] = 0
                    else:
                        host_fail[host] = host_fail.get(host, 0) + 1
                        if host_fail[host] >= 3:
                            host_cooldown[host] = now() + timedelta(minutes=30)
                            host_fail[host] = 0
                    if rec.get("hit_dir"):
                        stats["captures"] += 1
                        stats["our_hits"] += int(
                            OUR_CAMPAIGN in rec.get("watched", {}) or bool(TEST_CAMPAIGN)
                        )
                    print(
                        json.dumps(
                            {
                                k: rec.get(k)
                                for k in ("n", "utc", "host", "status", "watched", "hit_dir")
                            }
                        ),
                        flush=True,
                    )
                    if stats["our_hits"] >= args.target_hits or (
                        args.max_loads and stats["loads"] >= args.max_loads
                    ):
                        STOP.set()
                        break
                    try:
                        await asyncio.wait_for(
                            STOP.wait(), timeout=random.uniform(args.min_gap, args.max_gap)
                        )
                    except TimeoutError:
                        pass
        finally:
            summary = {
                "run_id": run_id,
                "started_utc": meta["started_utc"],
                "ended_utc": now().isoformat(timespec="seconds"),
                **stats,
            }
            (OUT / f"summary_{run_id}.json").write_text(json.dumps(summary, indent=2) + "\n")
            (OUT / "run.pid").unlink(missing_ok=True)
            print(json.dumps({"done": True, **summary}), flush=True)
            try:
                await browser.close()
            except Exception:  # noqa: BLE001
                pass


if __name__ == "__main__":
    asyncio.run(main())
