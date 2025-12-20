# Academic Research Literature Search and Synthesis Workflow (v4.0)

> **Revision Notes (v4.0):** Renamed from search-scholar.md. Added Research_Questions.md integration for automatic question selection, local filesystem saving, status updates, and GitHub issue management. Preserved all v3.1 Google Scholar Labs functionality.

You are assisting with an academic research workflow to search for scholarly literature using Google Scholar Labs, synthesize findings, and update project tracking.

## Inputs

- **mode**: How to select the research question
  - `"next"`: Auto-select highest priority unanswered question from Research_Questions.md
  - `"question"`: Use the provided research_question text directly
  - `"questions"`: Process a range (e.g., "1-5") or list (e.g., "3, 7, 12") from Research_Questions.md
- **research_question**: (Required if mode != "next") The specific question text or range
- **sort_by**: (Optional) How to order results: "relevance" | "citations". Default: "relevance"
- **early_completion**: (Optional) If true and 8+ results found after 90 seconds, proceed with partial results. Default: false

## Workflow Steps

### Step 0: Select Research Question (NEW in v4.0)

**If mode="next":**
1. Read `docs/references/Research_Questions.md`
2. Parse the "Unanswered Questions" section
3. Select highest priority question using these criteria (in order):
   - **Scope priority**: Paper1 > Paper2 > Paper3 (earlier deadlines first)
   - **Status priority**: "Unanswered" > "Partial" (skip "→ Gap" - already confirmed missing)
   - **Has GitHub issue**: Prefer questions with linked issues for tracking
4. Extract from the selected question:
   - Question text
   - Scope (Paper1/Paper2/Paper3)
   - GitHub issue number (if any)
   - Category section name

**If mode="question":**
- Use the provided research_question text directly
- Check Research_Questions.md to find matching entry for scope/issue info

**If mode="questions":**
- Parse the range (e.g., "1-5") or list (e.g., "3, 7, 12")
- Map to questions in Research_Questions.md by their order in the Unanswered section
- Process each sequentially

### Step 1: Navigate to Google Scholar Labs

- Go to https://scholar.google.com/scholar_labs/search
- If an existing session is open, click "+ New session" in the left sidebar to start fresh

### Step 1b: Verify Account Availability

- **Before submitting your query**, check if the current account has available searches
- If "Daily limit reached" message appears at the bottom of the page:
  1. Click the profile icon (top-right corner)
  2. Select an alternate Google account from the dropdown
  3. Wait for the page to reload with the new account
- Multiple Google accounts can extend daily search capacity

### Step 2: Parse Research Questions

- If a range is specified (e.g., "questions 1-5"), identify all individual questions from the source file
- If multiple questions specified (e.g., "questions 3, 7, 12"), parse the list
- Process each question sequentially, creating a separate output file for each

### Step 3: Submit the Research Question

- Locate the "Ask Scholar" input field at the bottom of the page
- Enter the research question exactly as provided
- Click the send arrow button to submit

**Query Formulation Tips:**
- Remove question words ("What", "How", "Why") if needed
- Add domain qualifiers: "healthcare", "clinical", "medical informatics"
- Try both specific and broader terms
- Include methodological terms: "systematic review", "benchmark", "evaluation"

### Step 4: Wait for Search Completion (typically 1-2 minutes, maximum 5 minutes)

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

### Step 5: Extract Paper URLs (SIMPLIFIED)

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

### Step 6: Extract and Format Results

- Use `get_page_text` to capture all result content from Scholar Labs
- Extract full paper URLs from Step 5
- If `sort_by` is "citations", reorder papers by citation count (highest first)
- Calculate citation age ratio: citations ÷ max(1, current_year - publication_year) for relative impact assessment
- **Note:** For papers published in the current year, use 1 as the divisor to avoid division by zero
- Note any citation relationships between papers in the results
- Note any "Cached" labels (indicates Google has a cached version if original source unavailable)
- Format results using the template below

### Step 7: Save Results Locally (CHANGED in v4.0)

**File Storage:**
- Save directly to `docs/references/Research_<slug>.md` using the Write tool
- No longer uses vscode.dev - files are written to the local filesystem

**Filename Convention:**
- Use the full research question text
- Convert to lowercase
- Replace whitespaces with hyphens
- Remove all non-alphanumeric characters (except hyphens)
- Prefix with `Research_`
- Add `.md` extension

**Examples:**
- "What is NL2SQL?" → `Research_what-is-nl2sql.md`
- "Has schema discovery been applied to healthcare databases specifically?" → `Research_has-schema-discovery-been-applied-to-healthcare-databases-specifically.md`

**Determine Status:**
- **Answered**: 5+ peer-reviewed sources directly addressing the question
- **Partial**: 1-4 sources OR sources only partially address the question
- **Gap**: No relevant sources found after multiple query variations

### Step 8: Update Research_Questions.md (NEW in v4.0)

Based on the determined status:

**If Answered:**
1. Move the question from "Unanswered Questions" to the appropriate "Answered Questions" subsection
2. Add the link to the new Research_*.md file
3. Remove from Unanswered section

**If Partial:**
1. Keep in "Unanswered Questions" section
2. Update Status column to "Partial"
3. Add Notes with brief summary and link to Research_*.md file

**If Gap:**
1. Keep in "Unanswered Questions" section
2. Update Status column to "→ Gap"
3. Add Notes: "Added to paper.md 'Gaps in Current Literature'"

**Always update the "Research File Index" table at the bottom of Research_Questions.md.**

### Step 9: Update GitHub Issue (NEW in v4.0)

If the question has a linked GitHub issue:

```bash
gh issue comment <NUMBER> --body "## Research Update

**Question:** <question text>
**Status:** Answered/Partial/Gap
**Research File:** docs/references/Research_<slug>.md

### Summary
<2-3 sentence summary of findings>

### Key Sources Found
- Author (Year): <title> - <one-line relevance>
- ...

### Next Steps
<If partial/gap, what additional research is needed>"
```

If status is "Answered" AND all questions in that issue are now resolved:
```bash
gh issue close <NUMBER> --comment "All research questions resolved. See Research_*.md files for details."
```

### Step 10: Repeat for Multiple Questions

- If multiple questions were specified, click "+ New session" and repeat steps 3-9 for each question
- Track progress and report: "Completed question X of Y"
- Aggregate GitHub issue updates when multiple questions share the same issue

---

## Timing Expectations

**Per Question:**
- Question selection (if mode="next"): 30 seconds
- Account verification/switching (if needed): 30-60 seconds
- Search: 1-2 minutes
- URL extraction (using read_page): 30 seconds - 1 minute
- Formatting and saving: 1-2 minutes
- Research_Questions.md update: 30 seconds
- GitHub issue update: 30 seconds
- **Total: 5-7 minutes per question**

**For Multiple Questions:**
- Add ~1 minute overhead per additional question for session management
- Example: 5 questions ≈ 30-40 minutes total

---

## Output Template

All sections are required. Do not skip or abbreviate any section.

```markdown
# Research Question: [Full question text]

**Status:** Answered | Partial | Gap
**Scope:** Paper1, Paper2, Paper3
**GitHub Issue:** #XXX (or "None")
**Source:** Google Scholar Labs
**Date:** [Current date]
**Results Found:** [X] relevant papers
**Sorted By:** [Relevance/Citations]
**Search Duration:** [X minutes/seconds]
**Search Queries Used:**
- "query 1"
- "query 2"

---

## Summary of Findings

[Brief 2-3 sentence overview of what the search found, including the date range of papers and dominant research themes. Clearly state whether literature answers the question, partially answers it, or reveals a gap.]

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

## Relevance to Three-Pillar Framework

1. **Analytics maturity:** [How findings relate to healthcare analytics maturity challenges]
2. **Workforce turnover:** [How findings relate to institutional knowledge loss]
3. **Technical barriers:** [How findings relate to NL2SQL and technical implementation challenges]

---

## Gaps Identified

[List any sub-questions or aspects NOT answered by the literature found]

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
- **Files are saved directly to the local filesystem** at `docs/references/Research_*.md`
- **Research_Questions.md is updated automatically** after each question is researched
- **GitHub issues are commented on** with research summaries

---

## Example Usage

**Auto-select next priority question:**
```
/scholar:research-question next
```

**Single specific question:**
```
/scholar:research-question "What algorithms exist for automatic primary key/foreign key discovery from database metadata?"
```

**Multiple questions by range:**
```
/scholar:research-question questions 1-5
```

**Specific questions:**
```
/scholar:research-question questions 3, 7, 12
```

**With options:**
```
/scholar:research-question next sort_by:citations early_completion:true
```

---

## Completion Report (for multiple questions)

When processing multiple questions, provide a summary at the end:

```
## Search Session Complete

**Questions Processed:** X of Y
**Total Papers Found:** [sum]
**Total Time:** [X minutes]

**Results by Status:**
- Answered: X questions
- Partial: X questions
- Gap: X questions

**Files Created:**
1. Research_[question-one-slug].md (10 papers) - Answered
2. Research_[question-two-slug].md (3 papers) - Partial
3. Research_[question-three-slug].md (0 papers) - Gap

**GitHub Issues Updated:**
- #XXX: Commented with findings for 2 questions
- #YYY: Closed (all questions resolved)

**Failed Searches:** [list any questions that returned no results with suggested reformulations]
```

---

## Changelog

**v4.0 (December 2025):**
- Renamed from search-scholar.md to research-question.md
- Added Step 0: Research_Questions.md integration for automatic question selection
- Added priority selection: Paper1 > Paper2 > Paper3 (by deadline)
- Changed Step 7: Local filesystem saving (replaces vscode.dev workflow)
- Added Step 8: Research_Questions.md status updates after research
- Added Step 9: GitHub issue commenting and closing
- Added status determination logic (Answered: 5+ sources, Partial: 1-4 sources, Gap: 0 sources)
- Added "Relevance to Three-Pillar Framework" section to output template
- Added "Gaps Identified" section to output template
- Added mode parameter: "next" | "question" | "questions"
- Preserved all v3.1 Google Scholar Labs search functionality

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
- Removed quick mode option—comprehensive output only
