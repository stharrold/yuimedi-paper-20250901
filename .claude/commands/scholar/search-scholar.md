# Academic Research Literature Search and Synthesis Workflow (v3.1)

> **Revision Notes (v3.1):** Updated based on practical execution experience. Key changes include simplified URL extraction, improved account switching guidance, clarified vscode.dev file handling, and refined timing estimates.

You are assisting with an academic research workflow to search for scholarly literature using Google Scholar Labs and synthesize findings.

## Inputs

- **research_question**: The specific research or business question to search for in academic literature. Can be a single question or a range (e.g., "question 1", "questions 1-5", "questions 3, 7, 12").
- **sort_by**: (Optional) How to order results: "relevance" | "citations". Default: "relevance"
- **early_completion**: (Optional) If true and 8+ results found after 90 seconds, proceed with partial results. Default: false

## Workflow Steps

### 1. Navigate to Google Scholar Labs

- Go to https://scholar.google.com/scholar_labs/search
- If an existing session is open, click "+ New session" in the left sidebar to start fresh

### 1b. Verify Account Availability (NEW)

- **Before submitting your query**, check if the current account has available searches
- If "Daily limit reached" message appears at the bottom of the page:
1. Click the profile icon (top-right corner)
2. Select an alternate Google account from the dropdown
3. Wait for the page to reload with the new account
- Multiple Google accounts can extend daily search capacity

### 2. Parse Research Questions

- If a range is specified (e.g., "questions 1-5"), identify all individual questions from the source file
- If multiple questions specified (e.g., "questions 3, 7, 12"), parse the list
- Process each question sequentially, creating a separate output file for each

### 3. Submit the Research Question

- Locate the "Ask Scholar" input field at the bottom of the page
- Enter the research question exactly as provided
- Click the send arrow button to submit

### 4. Wait for Search Completion (typically 1-2 minutes, maximum 5 minutes)

- Monitor the status indicator in the left sidebar
- Progress stages: "Analyzing your question" → "Looking for results..." → "Evaluated X top results" → "Found X relevant results" ✓
- Search is complete when the status shows a checkmark (✓)

**Early Completion Option:** If `early_completion` is true and 8+ results are found after 90 seconds, proceed with available results rather than waiting for the full search.

**Handling Daily Limits:**
- If "Daily limit reached" message appears, switch Google accounts (see Step 1b)
- Inform user of the limit and suggest account switching

**Edge Case Handling:**
- If Scholar Labs displays "Scholar Labs is currently not designed for queries like this" or "Search stopped," proceed with whatever results were found
- If no results, inform the user and suggest reformulating the question using these strategies:
- Rephrase as a how/what question
- Split into more specific sub-questions
- Remove jargon or acronyms
- Add domain context (e.g., "in healthcare databases")

**Interpreting Status Messages:**
- "Found X relevant results" ✓ = Complete success
- "Search stopped" + results visible = Partial success, use available results
- "Not designed for queries like this" + no results = Reformulate query
- Error messages = Retry once, then reformulate

### 5. Extract Paper URLs (SIMPLIFIED)

**Primary Method (Recommended):**
- Use `read_page` with `filter: interactive` to extract full paper URLs directly from the results page
- Google Scholar Labs provides complete URLs in the link elements (e.g., `href="https://ieeexplore.ieee.org/abstract/document/9499053/"`)
- PDF links are also directly available in the page structure

**Click-Through Method (If Needed):**
- Only click through to papers if URLs appear truncated or incomplete
- Click on the paper title link to navigate to the full paper page
- Extract the complete URL from the browser address bar
- Return to Scholar Labs results page

**Note:** The primary method saves 2-3 minutes per search compared to clicking through every paper.

### 6. Extract and Format Results

- Use `get_page_text` to capture all result content from Scholar Labs
- Extract full paper URLs from Step 5
- If `sort_by` is "citations", reorder papers by citation count (highest first)
- Calculate citation age ratio: citations ÷ max(1, current_year - publication_year) for relative impact assessment
- **Note:** For papers published in the current year, use 1 as the divisor to avoid division by zero
- Note any citation relationships between papers in the results
- Note any "Cached" labels (indicates Google has a cached version if original source unavailable)
- Format results using the template below

### 7. Save Results to vscode.dev

**File Storage:**
- All results are saved to vscode.dev (browser-based VS Code)
- Files are stored in browser local storage

**Important vscode.dev Limitations:**
- Without opening a local folder, files are saved as "Untitled-X" in browser storage
- To save with a specific filename, you have three options:
1. **Open a local folder first** via "Open Folder", then create files with proper names
2. **Use File → Save As** to download directly to your filesystem with the correct name
3. **Copy all content** (Cmd/Ctrl+A, Cmd/Ctrl+C) and paste into a local text editor

**Filename Convention (for reference):**
- Use the full research question text
- Convert to lowercase
- Replace whitespaces with hyphens
- Remove all non-alphanumeric characters (except hyphens)
- Prefix with `Research_`
- Add `.md` extension

**Examples:**
- "What is NL2SQL?" → `Research_what-is-nl2sql.md`
- "Has schema discovery been applied to healthcare databases specifically?" → `Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md`

**⚠️ IMPORTANT:** Remind user to download the file via File → Save As before closing the browser tab.

### 8. Repeat for Multiple Questions

- If multiple questions were specified, click "+ New session" and repeat steps 3-7 for each question
- Track progress and report: "Completed question X of Y"

---

## Timing Expectations

**Per Question:**
- Account verification/switching (if needed): 30-60 seconds
- Search: 1-2 minutes
- URL extraction (using read_page): 30 seconds - 1 minute
- Formatting and saving: 1-2 minutes
- **Total: 4-6 minutes per question**

**For Multiple Questions:**
- Add ~1 minute overhead per additional question for session management
- Example: 5 questions ≈ 25-35 minutes total

---

## Output Template

All sections are required. Do not skip or abbreviate any section.

```markdown
# Research Question: [Full question text]

**Source:** Google Scholar Labs
**Date:** [Current date]
**Results Found:** [X] relevant papers
**Sorted By:** [Relevance/Citations]
**Search Duration:** [X minutes/seconds]

---

## Summary of Findings

[Brief 2-3 sentence overview of what the search found, including the date range of papers and dominant research themes]

---

## 1. [Paper Title]

**Authors:** [Author names]
**Publication:** [Journal/Conference, Year]
**Citations:** [Number] ([citations/year] per year)
**Link:** [Full URL to paper]
**PDF:** [Direct PDF link if available, or "Not available"]

**Abstract/Summary:**
[Include abstract if visible in results, otherwise use Scholar Labs summary]

**Methodology/Approach:** [e.g., Machine Learning, Rule-based, Statistical, Survey/Review]

**Key Points:**
- [Main finding/contribution 1]
- [Main finding/contribution 2]
- [Main finding/contribution 3]

**Relationship to Other Papers:** [Note if this paper cites or is cited by other papers in the results]

---

[Repeat for each paper...]

---

## Key Themes and Observations

1. **[Theme 1]:** [Description]
2. **[Theme 2]:** [Description]
3. **[Theme 3]:** [Description]
4. **[Theme 4]:** [Description]
5. **[Theme 5]:** [Description]

---

## Citation Network

[Describe relationships between papers, e.g., "Paper 2 (Jiang 2020) extends the work of Paper 1 (Rostin 2009) by adding holistic detection..."]

---

## Highly Cited Papers (Relative Impact)

| Rank | Paper | Citations | Year | Citations/Year |
|------|-------|-----------|------|----------------|
| 1 | [Title] | [N] | [Year] | [N/max(1,age)] |
| 2 | [Title] | [N] | [Year] | [N/max(1,age)] |
| 3 | [Title] | [N] | [Year] | [N/max(1,age)] |
| 4 | [Title] | [N] | [Year] | [N/max(1,age)] |
| 5 | [Title] | [N] | [Year] | [N/max(1,age)] |

---

## Suggested Follow-up Questions

**From Scholar Labs:**
1. [Question suggested by Scholar Labs, if available]
2. [Question suggested by Scholar Labs, if available]
3. [Question suggested by Scholar Labs, if available]

**Based on Literature Gaps:**
1. [Question based on gaps identified in the literature]
2. [Question based on gaps identified in the literature]

---

## BibTeX Citations

```bibtex
@article{author1_year_keyword,
title={Paper Title},
    author={Author Names},
    journal={Journal Name},
        year={Year},
        volume={},
            pages={},
            doi={}
}

[Repeat for each paper...]
```
```

---

## Important Notes

- Google Scholar Labs typically completes searches in 1-2 minutes
- Results typically include up to 10 relevant papers with detailed summaries
- If the query type is not supported, Scholar Labs will indicate this—proceed with available results or suggest query reformulation
- **URLs can be extracted directly from the page** using `read_page`—click-through is usually not necessary
- The "More results" button may appear even when errors occur; rely on the checkmark status indicator
- Some papers may show "Cached" labels indicating Google's cached version is available
- **Files in vscode.dev are stored in browser local storage; remind user to download via File → Save As for a permanent local copy**

---

## Example Usage

**Single question:**
```
/search-scholar "What algorithms exist for automatic primary key/foreign key discovery from database metadata?"
```

**Multiple questions by range:**
```
/search-scholar questions 1-5
```

**Specific questions:**
```
/search-scholar questions 3, 7, 12
```

**With options:**
```
/search-scholar question 1 sort_by:citations early_completion:true
```

---

## Completion Report (for multiple questions)

When processing multiple questions, provide a summary at the end:

```
## Search Session Complete

**Questions Processed:** X of Y
**Total Papers Found:** [sum]
**Total Time:** [X minutes]
**Files Created:**
1. Research_[question-one-full-text].md (10 papers)
2. Research_[question-two-full-text].md (8 papers)
3. Research_[question-three-full-text].md (10 papers)

**Failed Searches:** [list any questions that returned no results with suggested reformulations]

**Reminder:** Files are stored in browser local storage. Use File → Save As to download each file before closing the browser.
```

---

## Changelog

**v3.1 (December 2025):**
- Added Step 1b for proactive account availability verification
- Simplified Step 5 URL extraction to use `read_page` as primary method (saves 2-3 min/search)
- Clarified vscode.dev file naming limitations and provided three workaround options
- Added note about citation/year calculation for current-year publications (use divisor of 1)
- Added guidance for "Cached" result labels
- Updated timing expectations to reflect simplified URL extraction
- Reduced estimated time per question from 5-7 minutes to 4-6 minutes

**v3.0 (December 2025):**
- Clarified vscode.dev as the only save destination with browser local storage behavior
- Added Google account switching guidance for daily limits
- Added click-through requirement for full paper URLs
- Updated filename convention to use full question text (no truncation)
- Added realistic timing expectations (5-7 minutes per question)
- Enhanced status message interpretation guide
- Made all output sections required (no optional sections)
- Removed quick mode option—comprehensive output only}
