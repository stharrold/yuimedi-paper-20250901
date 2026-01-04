#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
"""
Scholar Labs Search Tool
========================

Automates searching Google Scholar Labs (AI Overviews) using an existing
authenticated Chrome session via User-Attended Automation.

Requirements:
1. Google Chrome running with remote debugging:
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"
2. User must be logged in to Google Scholar in that Chrome instance.
3. playwright installed: `uv pip install playwright`

Usage:
  uv run python tools/scholar_labs_search.py "Your research question here"
  uv run python tools/scholar_labs_search.py --follow-up "Your follow-up question here"
"""

import argparse
import asyncio

from playwright.async_api import async_playwright

CHROME_DEBUG_URL = "http://localhost:9222"
LABS_URL = "https://scholar.google.com/scholar_labs/search?hl=en"


async def search_scholar_labs(query, follow_up=False):
    async with async_playwright() as p:
        try:
            # Connect to existing browser
            browser = await p.chromium.connect_over_cdp(CHROME_DEBUG_URL)
        except Exception:
            print(f"Error: Could not connect to Chrome at {CHROME_DEBUG_URL}")
            print("Ensure Chrome is running with --remote-debugging-port=9222")
            return

        context = browser.contexts[0]

        # Find existing Labs tab
        page = None
        for p_obj in context.pages:
            if "scholar_labs" in p_obj.url:
                page = p_obj
                break

        if not page:
            print("Opening new Scholar Labs tab...")
            page = await context.new_page()
            await page.goto(LABS_URL)
        else:
            if not follow_up:
                print("New question: Resetting session...")
                await page.goto(LABS_URL)
            else:
                print("Follow-up question: Using existing session context.")
            await page.bring_to_front()

        # Input Query
        print(f"Searching for: {query}")
        try:
            # Labs uses a textarea with id="gs_as_i_t"
            textarea = page.locator("#gs_as_i_t")
            await textarea.wait_for(state="visible", timeout=5000)

            await textarea.fill(query)
            await textarea.press("Enter")

            print("Query submitted. Waiting for AI analysis...")

            # Wait for results
            await page.wait_for_timeout(5000)  # Initial wait

            # Polling for completion (simple version)
            max_retries = 5
            for i in range(max_retries):
                text = await page.locator("body").inner_text()
                if "Looking for results..." not in text and "Evaluated" in text:
                    break
                print(f"  ... processing ({i + 1}/{max_retries})")
                await page.wait_for_timeout(3000)

            # Dump AI Overview Text
            content = await page.locator("body").inner_text()

            print("\n" + "=" * 60)
            print("SCHOLAR LABS RESULTS (AI Overview)")
            print("=" * 60)
            print(content[:5000])
            print("\n" + "=" * 60)

            # Extract Sources with URLs
            print("EXTRACTED SOURCES")
            print("=" * 60)

            results = page.locator(".gs_r")
            count = await results.count()

            for i in range(count):
                result = results.nth(i)
                try:
                    # Title link
                    title_link = result.locator("h3.gs_rt a").first
                    if await title_link.count() > 0:
                        title = await title_link.inner_text()
                        url = await title_link.get_attribute("href")
                        print(f"[{i + 1}] {title}")
                        print(f"    URL: {url}")

                        # Author/Snippet
                        authors_div = result.locator(".gs_a").first
                        if await authors_div.count() > 0:
                            authors = await authors_div.inner_text()
                            print(f"    Info: {authors}")

                        # PDF URL
                        pdf_link = result.locator(".gs_or_ggsm a").first
                        if await pdf_link.count() > 0:
                            pdf_url = await pdf_link.get_attribute("href")
                            print(f"    PDF: {pdf_url}")

                        print("-" * 40)
                except Exception as e:
                    print(f"Error parsing result {i}: {e}")

            print("=" * 60)

        except Exception as e:
            print(f"Interaction Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scholar Labs Search Tool")
    parser.add_argument("query", help="The research question to search for")
    parser.add_argument(
        "--follow-up",
        action="store_true",
        help="Treat as a follow-up to the existing session",
    )
    args = parser.parse_args()

    asyncio.run(search_scholar_labs(args.query, args.follow_up))
