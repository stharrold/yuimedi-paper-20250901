# Implementation Plan: Reference Validation

**Type:** feature
**Slug:** reference-validation
**Date:** 2025-12-02

## Overview

Implement Python scripts to validate that all citations in `paper.md` are properly supported by accessible references. This is a documentation-only repository, so scripts must use **Python stdlib only** (no external packages).

## Task Breakdown

### Phase 1: Reference Parsing (FR-002)

#### Task T001: Parse references from paper.md

**Priority:** High
**Category:** implementation

**Files:**
- `scripts/validate_references.py` (new)
- `paper.md` (read-only)

**Description:**
Create a Python script using stdlib only to parse the References section of paper.md and extract all citation entries with their markers ([A1], [I1], etc.) and URLs.

**Steps:**
1. Create `scripts/validate_references.py` with stdlib imports only
2. Implement regex patterns to match [A*] and [I*] citation markers
3. Extract URLs from each reference entry
4. Build a dictionary mapping citation markers to metadata (title, URL, type)

**Acceptance Criteria:**
- [ ] Script parses all 111 citations from paper.md
- [ ] Correctly identifies [A*] academic and [I*] industry citations
- [ ] Extracts URL for each reference that has one
- [ ] Uses only Python stdlib (no external packages)

**Verification:**
```bash
python scripts/validate_references.py --parse-only
# Should output: "Found N references (X academic, Y industry)"
```

**Dependencies:** None

---

#### Task T002: Extract claims requiring citations

**Priority:** High
**Category:** implementation

**Files:**
- `scripts/validate_references.py`
- `paper.md` (read-only)

**Description:**
Extend the validation script to identify statements in paper.md that contain citation markers, mapping claims to their supporting references.

**Steps:**
1. Add function to scan paper.md body (excluding References section)
2. Extract text surrounding each citation marker
3. Build claim-to-citation mapping
4. Identify any orphaned citations (referenced but not defined)

**Acceptance Criteria:**
- [ ] Identifies all paragraphs/sentences with citations
- [ ] Maps each claim to its citation markers
- [ ] Detects orphaned citation markers (no matching reference)
- [ ] Detects unused references (defined but never cited)

**Verification:**
```bash
python scripts/validate_references.py --check-citations
# Should output: "N claims found, M orphaned markers, K unused references"
```

**Dependencies:** T001

---

### Phase 2: URL Validation (FR-003)

#### Task T003: Validate reference URLs

**Priority:** High
**Category:** implementation

**Files:**
- `scripts/validate_references.py`

**Description:**
Add URL validation to check that each reference URL is accessible (returns HTTP 200 or valid redirect).

**Steps:**
1. Use `urllib.request` for HTTP requests (stdlib)
2. Implement timeout and retry logic
3. Handle redirects gracefully
4. Record HTTP status for each URL
5. Generate report of broken/inaccessible URLs

**Acceptance Criteria:**
- [ ] Checks each reference URL for accessibility
- [ ] Handles HTTP redirects (301, 302, 307, 308)
- [ ] Timeout after 10 seconds per URL
- [ ] Reports broken URLs with status codes
- [ ] Uses only Python stdlib (urllib.request)

**Verification:**
```bash
python scripts/validate_references.py --check-urls
# Should output: "Checked N URLs: M accessible, K broken"
```

**Dependencies:** T001

---

### Phase 3: Report Generation (FR-005)

#### Task T004: Generate validation report

**Priority:** Medium
**Category:** implementation

**Files:**
- `scripts/validate_references.py`
- `docs/validation_report.md` (new, generated)

**Description:**
Generate a comprehensive markdown report summarizing validation results.

**Steps:**
1. Add report generation function
2. Include summary statistics
3. List issues by severity (broken URLs, orphaned citations, unused refs)
4. Output to `docs/validation_report.md`

**Acceptance Criteria:**
- [ ] Generates markdown report with summary stats
- [ ] Lists all broken URLs with reference markers
- [ ] Lists orphaned citation markers
- [ ] Lists unused references
- [ ] Report is human-readable and actionable

**Verification:**
```bash
python scripts/validate_references.py --report
# Should create docs/validation_report.md
```

**Dependencies:** T001, T002, T003

---

### Phase 4: Testing & Quality

#### Task T005: Add unit tests

**Priority:** High
**Category:** testing

**Files:**
- `tests/test_validate_references.py` (new)

**Description:**
Create unit tests for the reference validation script.

**Steps:**
1. Create test file with pytest
2. Test reference parsing with sample data
3. Test citation extraction
4. Test URL validation (with mocked responses)
5. Test report generation

**Acceptance Criteria:**
- [ ] Tests cover reference parsing
- [ ] Tests cover citation extraction
- [ ] Tests cover edge cases (malformed refs, missing URLs)
- [ ] Tests pass with `uv run pytest`

**Verification:**
```bash
uv run pytest tests/test_validate_references.py -v
```

**Dependencies:** T001, T002, T003, T004

---

#### Task T006: Integrate with existing validation

**Priority:** Medium
**Category:** integration

**Files:**
- `validate_documentation.sh`
- `scripts/validate_references.py`

**Description:**
Integrate the new reference validation into the existing `validate_documentation.sh` script.

**Steps:**
1. Add reference validation as test 6 in validate_documentation.sh
2. Ensure script exits with appropriate codes
3. Update documentation about validation tests

**Acceptance Criteria:**
- [ ] `./validate_documentation.sh` includes reference validation
- [ ] Reference validation failures cause script to fail
- [ ] Documentation updated to describe new test

**Verification:**
```bash
./validate_documentation.sh
# Should include "Test 6: Reference validation"
```

**Dependencies:** T004, T005

---

### Phase 5: Documentation

#### Task T007: Update project documentation

**Priority:** Low
**Category:** documentation

**Files:**
- `CLAUDE.md`
- `scripts/CLAUDE.md`

**Description:**
Update project documentation to describe the new reference validation capability.

**Steps:**
1. Add reference validation to Essential Commands in root CLAUDE.md
2. Document the script in scripts/CLAUDE.md
3. Ensure commands are accurate and tested

**Acceptance Criteria:**
- [ ] Root CLAUDE.md mentions reference validation
- [ ] scripts/CLAUDE.md documents validate_references.py
- [ ] All documented commands work correctly

**Verification:**
```bash
# Run documented command
python scripts/validate_references.py --help
```

**Dependencies:** T006

---

## Task Summary

| Task ID | Name | Priority | Category | Dependencies |
|---------|------|----------|----------|--------------|
| T001 | Parse references from paper.md | High | implementation | None |
| T002 | Extract claims requiring citations | High | implementation | T001 |
| T003 | Validate reference URLs | High | implementation | T001 |
| T004 | Generate validation report | Medium | implementation | T001, T002, T003 |
| T005 | Add unit tests | High | testing | T001-T004 |
| T006 | Integrate with existing validation | Medium | integration | T004, T005 |
| T007 | Update project documentation | Low | documentation | T006 |

## Parallel Execution Opportunities

- **T002 and T003** can run in parallel after T001 completes
- **T007** can be started early and refined as implementation progresses

## Task Dependencies Graph

```
T001 (Parse references)
  │
  ├─→ T002 (Extract claims) ─┐
  │                           ├─→ T004 (Generate report) ─→ T005 (Tests) ─→ T006 (Integration) ─→ T007 (Docs)
  └─→ T003 (Validate URLs) ──┘
```

## Quality Checklist

Before considering this feature complete:

- [ ] All tasks marked as complete
- [ ] Script uses stdlib only (per project constraint)
- [ ] Tests pass with `uv run pytest`
- [ ] Linting clean (`uv run ruff check scripts/`)
- [ ] Type checking clean (`uv run mypy scripts/`)
- [ ] `./validate_documentation.sh` passes (all 6 tests)
- [ ] Reference validation report generated
- [ ] Documentation updated

## Notes

### Key Constraints

- **Stdlib only**: Per CLAUDE.md, scripts must use Python stdlib only (sys, os, subprocess, json, pathlib, datetime, re, typing, urllib)
- **No external packages**: Cannot use requests, beautifulsoup, etc.
- **Documentation-only repo**: Focus is on validating paper.md citations, not building a web service

### Implementation Tips

- Use `urllib.request.urlopen()` for HTTP requests
- Use `re` module for parsing citation patterns
- Use `json` for structured output
- Use `pathlib.Path` for file operations
