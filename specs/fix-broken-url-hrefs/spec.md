# Specification: Fix Broken Url Hrefs

**Type:** feature
**Slug:** fix-broken-url-hrefs
**Date:** 2025-12-14
**Author:** stharrold

## Overview

Fix 7 references in paper.md that have `\break` LaTeX commands embedded in URLs, causing broken hyperlinks in PDF/HTML/DOCX outputs. URLs are fragmented at slashes, preventing readers from clicking through to sources. Additionally, add automated validation to prevent future regressions.

## Implementation Context

**GitHub Issue:** #276

**BMAD Planning:** See `planning/fix-broken-url-hrefs/` for complete requirements and architecture.

**Implementation Preferences:**

- **Migration Strategy:** None needed
- **Task Granularity:** Small tasks (1-2 hours each)
- **Follow Epic Order:** True
- **Additional Notes:** Documentation-only fix: Remove LaTeX \break commands from URLs in paper.md References section. No database, no deployment - just text editing and validation script updates.

## Requirements Reference

See: `planning/fix-broken-url-hrefs/requirements.md`

### Functional Requirements

| FR ID | Description | Priority |
|-------|-------------|----------|
| FR-001 | Fix broken URLs in paper.md | High |
| FR-002 | Add LaTeX-in-URL validation to validate_references.py | High |
| FR-003 | Update validate_documentation.sh to include LaTeX check | Medium |
| FR-004 | Add test coverage for LaTeX-in-URL detection | Medium |

## Detailed Specification

### Component 1: URL Fixes in paper.md

**File:** `paper.md`

**Purpose:** Remove `\break` commands from URLs in the References section

**Affected References:**
- [A2] - URL contains `\break`
- [A4] - URL contains `\break`
- [A7] - URL contains `\break`
- [I1] - URL contains `\break`
- [I6] - URL contains `\break`
- [I9] - URL contains `\break`
- [I10] - URL contains `\break`

**Before:**
```markdown
[A2]: Some Author. "Title." Available: https://example.com/\break
path/to/resource
```

**After:**
```markdown
[A2]: Some Author. "Title." Available: https://example.com/path/to/resource
```

### Component 2: LaTeX Validation Function

**File:** `scripts/validate_references.py`

**Purpose:** Add function to detect LaTeX commands (especially `\break`) in URLs

**Implementation:**

```python
import re

def check_latex_in_urls(content: str) -> list[dict]:
    """
    Check for LaTeX commands embedded in URLs.

    Args:
        content: The markdown content to check

    Returns:
        List of violations with line numbers and matched patterns
    """
    violations = []
    latex_in_url_pattern = re.compile(
        r'https?://[^\s\]>]*\\[a-zA-Z]+[^\s\]>]*',
        re.IGNORECASE
    )

    for line_num, line in enumerate(content.split('\n'), 1):
        matches = latex_in_url_pattern.findall(line)
        for match in matches:
            violations.append({
                'line': line_num,
                'url': match,
                'latex_command': re.search(r'\\[a-zA-Z]+', match).group()
            })

    return violations
```

**CLI Integration:**
- New flag: `--check-latex`
- Exit code 1 if LaTeX found in URLs
- Human-readable error messages showing line numbers and affected URLs

### Component 3: Validation Pipeline Update

**File:** `validate_documentation.sh`

**Purpose:** Include LaTeX-in-URL check in standard validation

**Change:**
```bash
# Add to validation checks
python scripts/validate_references.py --check-latex
```

## Testing Requirements

### Unit Tests

**File:** `tests/test_validate_references.py`

```python
import pytest
from scripts.validate_references import check_latex_in_urls

def test_check_latex_in_urls_detects_break():
    """Test that \\break in URLs is detected."""
    content = "Reference: https://example.com/\\break/path"
    violations = check_latex_in_urls(content)
    assert len(violations) == 1
    assert violations[0]['latex_command'] == '\\break'

def test_check_latex_in_urls_clean():
    """Test that clean URLs pass validation."""
    content = "Reference: https://example.com/path/to/resource"
    violations = check_latex_in_urls(content)
    assert len(violations) == 0

def test_check_latex_in_urls_multiple():
    """Test detection of multiple violations."""
    content = """
    [A1]: https://example1.com/\\break/path
    [A2]: https://example2.com/\\textit/path
    """
    violations = check_latex_in_urls(content)
    assert len(violations) == 2
```

### Integration Tests

**File:** `tests/test_validate_references.py`

```python
def test_paper_has_no_latex_in_urls():
    """Verify paper.md has no LaTeX commands in URLs after fix."""
    with open('paper.md', 'r') as f:
        content = f.read()
    violations = check_latex_in_urls(content)
    assert len(violations) == 0, f"Found LaTeX in URLs: {violations}"
```

## Quality Gates

- [x] All 7 URLs fixed and accessible
- [ ] validate_references.py --check-latex passes
- [ ] validate_documentation.sh passes
- [ ] Unit tests pass
- [ ] Integration test confirms paper.md is clean
- [ ] Generated outputs (PDF, HTML, DOCX) have working hyperlinks

## Verification Commands

```bash
# Run reference validation with LaTeX check
python scripts/validate_references.py --check-latex

# Full documentation validation
./validate_documentation.sh

# Run tests
uv run pytest tests/test_validate_references.py -v

# Generate and verify PDF
./scripts/build_paper.sh
# Manual: Open paper.pdf and click each reference URL
```

## References

- GitHub Issue: #276 - References: href for links broken at slash incorrect
- Related Issue: #261 - P0: Fix unsupported claims and hallucinated references
