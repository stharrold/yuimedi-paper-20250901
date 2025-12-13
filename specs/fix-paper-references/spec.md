# Specification: Fix Paper References

**Type:** documentation
**Slug:** fix-paper-references
**Date:** 2025-12-11
**Author:** stharrold
**GitHub Issue:** #261

## Overview

This specification defines the methodology for fixing unsupported claims and hallucinated references in `paper.md`. The goal is to ensure every citation is verifiable against peer-reviewed sources, removing fabricated references and replacing them with legitimate academic evidence.

## Implementation Context

**BMAD Planning:** See `planning/fix-paper-references/` for complete requirements and architecture.

**Scope:**
- Remove hallucinated/fabricated references
- Verify all remaining citations against DOIs and authoritative sources
- Replace unverifiable claims with evidence-based assertions
- Document verification methodology for reproducibility

## Verification Methodology

### Citation Verification Process

1. **DOI Validation**: Check all DOI links resolve to actual publications
2. **Source Verification**: Confirm cited content supports the claim made
3. **Author Verification**: Validate author names and affiliations exist
4. **Publication Verification**: Confirm journal/venue is legitimate
5. **Date Verification**: Ensure publication dates are accurate

### Verification Categories

| Category | Criteria | Action |
|----------|----------|--------|
| VERIFIED | DOI resolves, content matches claim | Keep |
| PARTIALLY VERIFIED | Source exists, paywall prevents full access | Keep with DOI fallback |
| NEEDS REPLACEMENT | Cannot verify, likely fabricated | Find alternative source |
| UNUSED | Defined but never cited | Remove |

### Hallucination Detection Signals

References flagged for deeper review if they exhibit:
- Suspiciously specific statistics without meta-analysis source
- RCT claims without registration number
- Author combinations that don't appear in academic databases
- Journal names that don't exist or have been discontinued
- DOIs that resolve to different papers than cited

## Citation Standards

### Academic References [A*]

**Required fields:**
- Author(s) with verifiable names
- Title matching actual publication
- Journal/venue that exists
- Year matching actual publication
- DOI or stable URL

**Format:**
```
[A1] Author(s). "Title." Journal, Year. DOI/URL
```

### Industry References [I*]

**Required fields:**
- Organization name
- Document/page title
- Stable URL or archive link
- Access date for web content

**Format:**
```
[I1] Organization. "Title." URL (accessed YYYY-MM-DD)
```

## Three-Pillar Claim Mapping

All claims must connect to the three-pillar framework with verified evidence:

### Pillar 1: Analytics Maturity

| Claim | Required Evidence | Status |
|-------|-------------------|--------|
| Low AMAM adoption | HIMSS official data or peer-reviewed survey | VERIFIED [I1] |
| Stage 0-1 prevalence | Published analytics maturity assessment | VERIFIED [I2] |

### Pillar 2: Workforce Turnover

| Claim | Required Evidence | Status |
|-------|-------------------|--------|
| Healthcare turnover rates | Meta-analysis or large-scale survey | VERIFIED [A1], [A2] |
| Knowledge loss impact | Peer-reviewed study on institutional memory | VERIFIED [A4] |
| Training costs | Industry report with methodology | VERIFIED [I3], [I4] |

### Pillar 3: Technical Barriers

| Claim | Required Evidence | Status |
|-------|-------------------|--------|
| NL2SQL accuracy benchmarks | Published benchmark results | VERIFIED [A3], [A5] |
| Schema complexity challenges | Peer-reviewed NL2SQL research | VERIFIED [A6], [A7] |
| Clinical readiness limitations | Expert assessment or validation study | VERIFIED [A9], [A10] |

## Quality Gates

### Pre-Merge Validation

- [x] All citations have valid reference entries
- [x] All references are cited at least once (no orphans)
- [x] DOI links validated (or documented as paywalled)
- [x] No hallucination signals detected
- [x] Claims match verified source content

### Documentation Validation

```bash
# Run before merge
./validate_documentation.sh
python scripts/validate_references.py --all
```

## URL Status Classification

### Paywalled (HTTP 403)

URLs returning 403 are often legitimate sources behind publisher paywalls:

| Status | Meaning | Action |
|--------|---------|--------|
| PMC 403 | NIH archive, may require institutional access | Provide DOI fallback |
| ScienceDirect 403 | Elsevier paywall | Provide DOI fallback |
| HIMSS 403 | Membership content | Note access requirement |

### Truly Broken (HTTP 404/500)

URLs that no longer exist:
- Find archived version (Wayback Machine)
- Replace with alternative source
- Remove if no alternative exists

## Metrics

### Before (Baseline)

| Metric | Value |
|--------|-------|
| Total References | 54 |
| Unused References | 29 |
| Broken URLs | 23 |
| Potentially Hallucinated | Unknown |

### After (Target)

| Metric | Value |
|--------|-------|
| Total References | 18 |
| Unused References | 0 |
| Verified Sources | 18 |
| Paywalled (with DOI) | 8 |

## Testing Requirements

### Automated Validation

The existing validation scripts verify:
1. All `[A*]` and `[I*]` markers have matching reference entries
2. All reference entries are cited in the paper body
3. URL accessibility (with timeout and retry)
4. File size limits and cross-reference integrity

### Manual Review Checklist

- [x] Each verified claim matches source content
- [x] Author names are spelled correctly
- [x] Publication years are accurate
- [x] DOIs resolve to correct papers
- [x] Removed references had valid justification
- [x] No unverified percentage claims (91% removed)

## Implementation Notes

### Key Decisions

1. **Conservative approach**: Prefer removing questionable references over keeping them
2. **Paywall handling**: Keep paywalled sources with DOI if the citation is otherwise verifiable
3. **Benchmark preference**: Use published benchmarks (EHRSQL, TREQS) over proprietary claims
4. **Temporal relevance**: Prefer recent sources (2020+) for rapidly evolving fields

### Lessons Learned

- Original 111 citations likely included AI-generated fabrications
- Meta-analyses are more reliable than single studies for turnover data
- Healthcare NL2SQL benchmarks are limited but growing
- Many industry reports require registration/membership access

## References

- `planning/fix-paper-references/requirements.md` - Business requirements
- `planning/fix-paper-references/architecture.md` - Technical approach
- `specs/fix-paper-references/claims_analysis.md` - Detailed claim mapping
- `specs/fix-paper-references/reference_verification.md` - Verification results
