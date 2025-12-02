# Specification: Reference Validation

**Type:** feature
**Slug:** reference-validation
**Date:** 2025-12-02
**Author:** stharrold

## Overview

This feature provides comprehensive validation of citations and references in paper.md, ensuring all claims have supporting references, all references have accessible URLs, and the citation format follows the established [A*]/[I*] pattern. The validation script integrates into the documentation validation suite as Test 6.

## Implementation Context

<!-- Generated from SpecKit interactive Q&A -->

**BMAD Planning:** See `planning/reference-validation/` for complete requirements and architecture.

**Implementation Preferences:**

- **Migration Strategy:** None needed
- **Task Granularity:** Small tasks (1-2 hours each)
- **Follow Epic Order:** True
- **Additional Notes:** Documentation-only repository. Focus on validating reference formatting and cross-references in paper.md.

## Requirements Reference

See: `planning/reference-validation/requirements.md` in main repository

## Components

### Reference Parser

**File:** `scripts/validate_references.py`

**Purpose:** Parse the References section of paper.md and extract all [A*] academic and [I*] industry references with their URLs.

**Key Functions:**
- `parse_references()` - Extracts reference entries from the References section
- `extract_citations()` - Finds all citation markers in the paper body
- `find_orphaned_and_unused()` - Identifies citation/reference mismatches

### URL Validator

**File:** `scripts/validate_references.py`

**Purpose:** Validate that reference URLs are accessible using Python stdlib only (urllib).

**Key Functions:**
- `check_url()` - Validates individual URL accessibility with retry logic
- `validate_urls()` - Batch validates all reference URLs

### Report Generator

**File:** `scripts/validate_references.py`

**Purpose:** Generate markdown validation reports summarizing results.

**Key Functions:**
- `generate_report()` - Creates detailed markdown report with issues and statistics

## Data Models

### Reference (dataclass)

```python
@dataclass
class Reference:
    marker: str      # e.g., "A1", "I5"
    ref_type: str    # "academic" or "industry"
    number: int
    full_text: str
    url: str | None
    url_status: int | None
    url_error: str | None
```

### Citation (dataclass)

```python
@dataclass
class Citation:
    marker: str      # e.g., "A1", "I5"
    line_number: int
    context: str     # surrounding text
```

### ValidationResult (dataclass)

```python
@dataclass
class ValidationResult:
    references: dict[str, Reference]
    citations: list[Citation]
    orphaned_citations: list[Citation]
    unused_references: list[str]
    broken_urls: list[Reference]
    accessible_urls: list[Reference]
    missing_urls: list[Reference]
```

## CLI Interface

```bash
# Parse references only
python scripts/validate_references.py --parse-only

# Check for orphaned/unused citations
python scripts/validate_references.py --check-citations

# Validate reference URLs
python scripts/validate_references.py --check-urls

# Generate validation report
python scripts/validate_references.py --report

# Run all validations
python scripts/validate_references.py --all

# JSON output
python scripts/validate_references.py --all --json
```

## Testing Requirements

**File:** `tests/test_validate_references.py`

19 tests covering:
- Reference parsing (academic and industry)
- Citation extraction
- Orphaned/unused detection
- Report generation
- Integration with real paper.md

## Quality Gates

- [x] Test coverage for all validation functions
- [x] All 19 tests passing
- [x] Linting clean (ruff check)
- [x] Type checking clean (mypy)
- [x] Python stdlib only (no external dependencies)

## Integration

Integrated into `validate_documentation.sh` as Test 6:
- Runs `--check-citations` mode during validation suite
- Exit code 1 only for orphaned citations (critical)
- Broken URLs are warnings (many academic sources have paywalls)

## References

- `planning/reference-validation/requirements.md` - Detailed requirements
- `planning/reference-validation/architecture.md` - Technical architecture
- `docs/validation_report.md` - Generated validation report
