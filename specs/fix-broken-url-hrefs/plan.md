# Implementation Plan: Fix Broken Url Hrefs

**Type:** feature
**Slug:** fix-broken-url-hrefs
**Date:** 2025-12-14

## Task Breakdown

### Phase 1: Fix URLs in paper.md

#### Task impl_001: Identify and fix broken URLs

**Priority:** High

**Files:**
- `paper.md`

**Description:**
Remove `\break` LaTeX commands from 7 URLs in the References section that are causing hyperlinks to break in generated outputs.

**Steps:**
1. Search paper.md for `\break` commands in URLs
2. For each affected reference ([A2], [A4], [A7], [I1], [I6], [I9], [I10]):
   - Remove `\break` command
   - Join URL fragments into single contiguous URL
3. Verify URLs are syntactically correct
4. Test that URLs are accessible (HTTP 200)

**Acceptance Criteria:**
- [ ] All 7 URLs are contiguous (no `\break` commands)
- [ ] URLs are valid and accessible
- [ ] No other references accidentally modified

**Verification:**
```bash
# Check no \break in URLs
grep -E 'https?://.*\\break' paper.md && echo "FAIL: Found \\break in URLs" || echo "PASS"

# Validate references
python scripts/validate_references.py --all
```

**Dependencies:**
- None

---

### Phase 2: Add Validation

#### Task impl_002: Add check_latex_in_urls function

**Priority:** High

**Files:**
- `scripts/validate_references.py`

**Description:**
Add a function to detect LaTeX commands (especially `\break`) embedded in URLs to prevent future regressions.

**Steps:**
1. Add `check_latex_in_urls(content: str) -> list[dict]` function
2. Use regex to find URLs containing LaTeX commands
3. Return list of violations with line numbers and matched commands
4. Add `--check-latex` CLI flag to argparse
5. Integrate check into main validation flow

**Acceptance Criteria:**
- [ ] Function detects `\break` and other LaTeX commands in URLs
- [ ] CLI flag `--check-latex` works
- [ ] Returns exit code 1 if violations found
- [ ] Human-readable error output

**Verification:**
```bash
# Test with clean paper.md (should pass after impl_001)
python scripts/validate_references.py --check-latex

# Test detection works (create temp file with bad URL)
echo "https://example.com/\break/path" | python -c "
import sys
sys.path.insert(0, 'scripts')
from validate_references import check_latex_in_urls
content = sys.stdin.read()
violations = check_latex_in_urls(content)
print(f'Found {len(violations)} violations')
assert len(violations) == 1
"
```

**Dependencies:**
- impl_001 (for clean paper.md to test against)

---

#### Task impl_003: Update validation pipeline

**Priority:** Medium

**Files:**
- `validate_documentation.sh`

**Description:**
Include LaTeX-in-URL check in the standard documentation validation script.

**Steps:**
1. Add call to `python scripts/validate_references.py --check-latex`
2. Update test count if needed
3. Ensure proper error handling and exit codes

**Acceptance Criteria:**
- [ ] `./validate_documentation.sh` includes LaTeX check
- [ ] Script fails if LaTeX found in URLs
- [ ] Test count updated in script header

**Verification:**
```bash
./validate_documentation.sh
```

**Dependencies:**
- impl_002

---

### Phase 3: Testing

#### Task test_001: Unit tests for LaTeX detection

**Priority:** Medium

**Files:**
- `tests/test_validate_references.py`

**Description:**
Add comprehensive unit tests for the `check_latex_in_urls` function.

**Steps:**
1. Create test file if not exists
2. Add test for detecting `\break` command
3. Add test for clean URLs (no violations)
4. Add test for multiple violations
5. Add test for edge cases (URLs at end of line, in markdown links, etc.)

**Acceptance Criteria:**
- [ ] Tests for happy path (clean URLs)
- [ ] Tests for error path (LaTeX in URLs)
- [ ] Tests for edge cases
- [ ] All tests passing

**Verification:**
```bash
uv run pytest tests/test_validate_references.py -v -k "latex"
```

**Dependencies:**
- impl_002

---

#### Task test_002: Integration test for paper.md

**Priority:** Medium

**Files:**
- `tests/test_validate_references.py`

**Description:**
Add integration test that verifies paper.md has no LaTeX commands in URLs.

**Steps:**
1. Add test that reads actual paper.md
2. Runs check_latex_in_urls against content
3. Asserts zero violations
4. Provides clear error message if violations found

**Acceptance Criteria:**
- [ ] Test reads real paper.md file
- [ ] Test fails if any LaTeX found in URLs
- [ ] Test provides actionable error message

**Verification:**
```bash
uv run pytest tests/test_validate_references.py -v -k "paper"
```

**Dependencies:**
- impl_001, impl_002

---

### Phase 4: Verification

#### Task verify_001: Generate and verify outputs

**Priority:** High

**Files:**
- `paper.pdf`
- `paper.html`
- `paper.docx`

**Description:**
Generate all output formats and verify hyperlinks work correctly.

**Steps:**
1. Run `./scripts/build_paper.sh --format all`
2. Open paper.pdf and click each reference URL
3. Open paper.html and click each reference URL
4. Open paper.docx and click each reference URL
5. Document any remaining issues

**Acceptance Criteria:**
- [ ] PDF hyperlinks work
- [ ] HTML hyperlinks work
- [ ] DOCX hyperlinks work
- [ ] All 7 previously broken URLs now functional

**Verification:**
```bash
./scripts/build_paper.sh --format all
# Manual verification of clickable links
```

**Dependencies:**
- impl_001, impl_002, impl_003

---

## Task Summary

| Task ID | Description | Priority | Dependencies |
|---------|-------------|----------|--------------|
| impl_001 | Fix broken URLs in paper.md | High | None |
| impl_002 | Add check_latex_in_urls function | High | impl_001 |
| impl_003 | Update validation pipeline | Medium | impl_002 |
| test_001 | Unit tests for LaTeX detection | Medium | impl_002 |
| test_002 | Integration test for paper.md | Medium | impl_001, impl_002 |
| verify_001 | Generate and verify outputs | High | impl_001-003 |

## Task Dependencies Graph

```
impl_001 (Fix URLs)
    ↓
impl_002 (Add validation function)
    ↓
    ├─→ impl_003 (Update pipeline)
    │       ↓
    │       └─→ verify_001 (Generate outputs)
    │
    ├─→ test_001 (Unit tests)
    │
    └─→ test_002 (Integration test)
```

## Critical Path

1. impl_001 - Fix URLs
2. impl_002 - Add validation
3. impl_003 - Update pipeline
4. verify_001 - Verify outputs

## Quality Checklist

Before considering this feature complete:

- [ ] All 7 URLs fixed in paper.md
- [ ] `python scripts/validate_references.py --check-latex` passes
- [ ] `./validate_documentation.sh` passes (all tests including new LaTeX check)
- [ ] Unit tests pass (`uv run pytest tests/test_validate_references.py -v`)
- [ ] Integration test confirms paper.md is clean
- [ ] PDF, HTML, and DOCX outputs have working hyperlinks
- [ ] Code follows scripts/ dependency rules (stdlib only)
