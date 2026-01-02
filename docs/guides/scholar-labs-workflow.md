# Google Scholar Labs Research Workflow

This algorithm captures the semi-automated workflow for answering research questions using Google Scholar Labs (AI Overviews) by **leveraging User-Attended Automation**. The user manually supervises the session and handles authentication, while scripts automate the repetitive data entry and extraction tasks.

## Prerequisites
*   **Google Chrome** installed.
*   **Playwright** installed (`uv pip install playwright`).
*   **Google Account** with access to Scholar Labs (or standard Scholar as fallback).

## Algorithm Steps

### 1. Initialization (User Action)
*   Close all Chrome instances.
*   Run Chrome with remote debugging:
    ```bash
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"
    ```
*   **Authenticate:** Log in to Google in the opened window.
*   **Navigate:** Go to [https://scholar.google.com/scholar_labs/search](https://scholar.google.com/scholar_labs/search).

### 2. Question Selection (Automated)
*   Read `docs/research/Research_Questions.md`.
*   Identify the next question marked `Unanswered` or `Partial`.
*   Extract the **Scope** (Paper1/Paper2/Paper3).

### 3. Execution (Automated Script)
*   **Connect:** Script connects to `localhost:9222` via Playwright.
*   **Search:** Submits the natural language question to the Labs interface.
*   **Wait:** Polls for "Evaluated X results" completion.
*   **Extract:** Scrapes the AI overview text and the list of source citations (Title, URL, Snippet).

### 4. Documentation (Automated Script)
*   **Create Note:** Generates `docs/research/Research_<question-slug>.md`.
    *   Populates "Key Findings" from the AI summary.
    *   Populates "Sources" table with links.
*   **Update Tracker:** Updates `Research_Questions.md`:
    *   Change Status to `Answered` or `Partial`.
    *   Add Link to the new research note.
    *   Add Date/Note about findings.

### 5. Artifact Retrieval (Automated Script)
*   **Download:** Iterates through source URLs.
*   **Save:** Downloads accessible PDFs to `docs/references/YYYY_Author_Journal_Title.pdf`.
*   **Log:** Records success/failure for each download.

## Scripts
*   `tools/scholar_labs_search.py`: Core search logic.
*   `tools/run_scholar_workflow.py`: Master orchestrator (To Be Implemented).
