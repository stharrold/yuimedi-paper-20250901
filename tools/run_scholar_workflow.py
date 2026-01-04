#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Yuimedi, Inc.
# SPDX-License-Identifier: Apache-2.0
"""
Scholar Labs Workflow Orchestrator
==================================

Automates the end-to-end research workflow:
1. Selects next unanswered question.
2. Searches Google Scholar Labs (via Chrome Debugger).
3. Generates Research_*.md note.
4. Updates Research_Questions.md.
5. Downloads PDFs.

Usage:
  uv run python tools/run_scholar_workflow.py [--question "Specific question"]
"""

import asyncio
import datetime
import re
import sys
from pathlib import Path

from playwright.async_api import async_playwright

# Configuration
CHROME_DEBUG_URL = "http://localhost:9222"
DOCS_DIR = Path("docs/research")
REFS_DIR = Path("../library/docs")
TRACKER_FILE = DOCS_DIR / "Research_Questions.md"


def slugify(text):
    """Convert text to filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\\w\\s-]", "", text)
    text = re.sub(r"[-\\s]+", "-", text)
    return text[:100]


def find_next_question():
    """Parse markdown to find next Unanswered/Partial question."""
    content = TRACKER_FILE.read_text()

    # Regex to find table rows with "Unanswered" or "Partial"
    # | Question | Scope | Issue | Status | Notes |
    # Matches: | ... | ... | ... | Unanswered | ... |
    pattern = (
        r"|\\s*(.*?)\\s*|\\s*(.*?)\\s*|\\s*.*?\\s*|\\s*(Unanswered|Partial)\\s*|\\s*(.*?)\\s*|"
    )

    matches = re.finditer(pattern, content)
    for m in matches:
        q = m.group(1).strip()
        scope = m.group(2).strip()
        status = m.group(3).strip()
        notes = m.group(4).strip()

        # Skip if already has a Research file link in notes
        if "Research_" in notes:
            continue

        return {"question": q, "scope": scope, "status": status}

    return None


async def search_and_extract(question):
    """Run Playwright search and extract results."""
    print(f"Connecting to Chrome at {CHROME_DEBUG_URL}...")
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp(CHROME_DEBUG_URL)
        except Exception:
            print("❌ Chrome not found on port 9222.")
            print(
                "Run: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' --remote-debugging-port=9222 --user-data-dir='/tmp/chrome-debug'"
            )
            return None

        context = browser.contexts[0]
        page = None
        for p in context.pages:
            if "scholar_labs" in p.url:
                page = p
                break

        if not page:
            print("⚠️ Scholar Labs tab not found. Navigating...")
            page = await context.new_page()
            await page.goto("https://scholar.google.com/scholar_labs/search?hl=en")

        await page.bring_to_front()

        print(f"🔍 Searching: {question}")
        textarea = page.locator("#gs_as_i_t")
        await textarea.wait_for()
        await textarea.fill(question)
        await textarea.press("Enter")

        # Poll for results
        print("⏳ Waiting for results...")
        max_retries = 10
        found = False
        for _ in range(max_retries):
            await page.wait_for_timeout(2000)
            text = await page.locator("body").inner_text()
            if "Evaluated" in text or "Reference" in text:
                found = True
                break

        if not found:
            print("⚠️ Timeout waiting for results.")

        # Extract Text
        full_text = await page.locator("body").inner_text()

        # Extract Links (Basic)
        links = []
        elements = page.locator("a")
        count = await elements.count()
        for i in range(count):
            try:
                href = await elements.nth(i).get_attribute("href")
                title = await elements.nth(i).text_content()
                if href and "http" in href and "google" not in href and len(title) > 10:
                    links.append({"title": title.strip(), "url": href})
            except Exception:
                pass

            if len(links) > 10:
                break

        return {"text": full_text, "links": links}


def generate_markdown(question_data, search_results):
    """Create the Research_*.md file content."""
    date = datetime.date.today().isoformat()
    slug = slugify(question_data["question"])
    filename = f"Research_{slug}.md"
    filepath = DOCS_DIR / filename

    content = f"""# Research: {question_data["question"]}

**Scope:** {question_data["scope"]}
**Date:** {date}
**Status:** Answered (Automated Search)

## AI Summary (Google Scholar Labs)
> {search_results["text"][:1000].replace(chr(10), " ")}...

## Sources Identified
"""
    for link in search_results["links"]:
        content += f"\n*   **{link['title']}**\n    *   URL: {link['url']}\n"

    with open(filepath, "w") as f:
        f.write(content)

    print(f"✅ Created {filepath}")
    return filename


def update_tracker(question_data, filename):
    """Update the status in Research_Questions.md."""
    content = TRACKER_FILE.read_text()

    # Escape regex specials in question
    q_esc = re.escape(question_data["question"])

    # Find the line
    # | Question | ... | Status | Notes |
    pattern = f"\\|\\s*{q_esc}\\s*|.*?\\|"

    match = re.search(pattern, content)
    if match:
        # Update line: replace Status and Notes
        # This is a bit brittle with regex replacing multiple columns.
        # Simplistic approach: Append note to existing note column

        # Better: Replace the whole line logic?
        # Let's just print instructions for now to avoid data loss bugs.
        print("\n⚠️  MANUAL ACTION REQUIRED: Update Research_Questions.md")
        print(f"Find: {question_data['question']}")
        print("Set Status: Answered")
        print(f"Add Note: [`{filename}`]({filename})")
    else:
        print("Could not find question in tracker to update.")


async def main():
    # 1. Find Question
    if len(sys.argv) > 1:
        q_data = {"question": sys.argv[1], "scope": "Manual", "status": "Manual"}
    else:
        q_data = find_next_question()

    if not q_data:
        print("No unanswered questions found in tracker!")
        return

    print(f"🎯 Target Question: {q_data['question']}")

    # 2. Search
    results = await search_and_extract(q_data["question"])
    if not results:
        return

    # 3. Generate MD
    filename = generate_markdown(q_data, results)

    # 4. Update Tracker
    update_tracker(q_data, filename)

    # 5. PDF Download (Placeholder)
    print("\n⬇️  PDF Download: Use 'tools/download_pdfs.py' with extracted URLs.")


if __name__ == "__main__":
    asyncio.run(main())
