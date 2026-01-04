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
"""

import asyncio
import sys

from playwright.async_api import async_playwright

CHROME_DEBUG_URL = "http://localhost:9222"
LABS_URL = "https://scholar.google.com/scholar_labs/search?hl=en"


async def search_scholar_labs(query):
    async with async_playwright() as p:
        try:
            # Connect to existing browser
            browser = await p.chromium.connect_over_cdp(CHROME_DEBUG_URL)
        except Exception:
            print(f"Error: Could not connect to Chrome at {CHROME_DEBUG_URL}")
            print("Ensure Chrome is running with --remote-debugging-port=9222")
            return

        context = browser.contexts[0]

        # Find or open Labs tab
        page = None
        for p in context.pages:
            if "scholar_labs" in p.url:
                page = p
                break

        if not page:
            print("Opening new Scholar Labs tab...")
            page = await context.new_page()
            await page.goto(LABS_URL)
        else:
            print("Using existing Scholar Labs tab.")
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
            # The interface shows "Looking for results..." then updates.
            # We wait for the result container or a stable state.
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

            # Standard Scholar results usually have class 'gs_r' or 'gs_ri'
            # Title link is 'h3.gs_rt a'
            results = page.locator(".gs_r")
            count = await results.count()

            if count == 0:
                print(
                    "No standard result elements (.gs_r) found. Checking for Labs-specific list..."
                )
                # Fallback or specific labs selectors could go here

            for i in range(count):
                result = results.nth(i)
                try:
                    # Title link
                    title_link = result.locator("h3.gs_rt a")
                    if await title_link.count() > 0:
                        title = await title_link.inner_text()
                        url = await title_link.get_attribute("href")
                        print(f"[{i + 1}] {title}")
                        print(f"    URL: {url}")

                        # Author/Snippet
                        authors_div = result.locator(".gs_a")
                        if await authors_div.count() > 0:
                            authors = await authors_div.inner_text()
                            print(f"    Info: {authors}")
                        print("-" * 40)
                except Exception as e:
                    print(f"Error parsing result {i}: {e}")

            print("=" * 60)

        except Exception as e:
            print(f"Interaction Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scholar_labs_search.py <query>")
        sys.exit(1)

    query = sys.argv[1]
    asyncio.run(search_scholar_labs(query))
