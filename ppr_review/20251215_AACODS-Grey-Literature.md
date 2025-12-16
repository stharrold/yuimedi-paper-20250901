# Paper 1 Recommendation: AACODS Grey Literature Quality Assessment

## Issue
Paper 1 relies on 11 industry sources [I1-I11] without formal quality assessment. Reviewers may challenge evidence quality.

## Solution
Apply AACODS checklist (Authority, Accuracy, Coverage, Objectivity, Date, Significance) to all grey literature sources.

**Note**: GRADE and Cochrane Risk of Bias are inappropriate - designed for clinical intervention studies and RCTs, not narrative reviews with grey literature.

## Implementation

### Add to Section 3 (Methodology)

Insert subsection "3.6 Grey Literature Quality Assessment":

```
Grey literature sources were assessed using the AACODS checklist
(Tyndall, 2010), which evaluates Authority, Accuracy, Coverage,
Objectivity, Date, and Significance. Sources with vendor sponsorship
were retained when no independent alternative existed but flagged
in-text. Table X summarizes the assessment.
```

### Add Table: AACODS Assessment of Industry Sources

| Source | Authority | Accuracy | Coverage | Objectivity | Date | Significance | Include |
|--------|-----------|----------|----------|-------------|------|--------------|---------|
| [I1] HIMSS AMAM | High (industry standards body) | Verifiable (public data) | Global | High | 2024 | High | Yes |
| [I2] Snowdon/HIMSS | High (HIMSS officer) | Verifiable | N/A | High | 2024 | Medium | Yes |
| [I3] Health Catalyst | Medium (vendor) | Unverifiable | US | Low | 2020 | Medium | Yes* |
| [I4] Berkshire NHS | High (NHS trust) | Verifiable | Single site | High | 2024 | High | Yes |
| [I5] Forrester/Microsoft | Medium (analyst firm) | Unverifiable | Enterprise | Low (sponsor) | 2024 | Medium | Yes* |
| [I6] Oracle | Low (vendor) | Unverifiable | N/A | Low | 2024 | Low | Yes* |
| [I7] Precedence Research | Medium (market research) | Unverifiable | Global | Medium | 2024 | Medium | Yes |
| [I8] Anthropic | Medium (vendor) | Verifiable | N/A | Medium | 2025 | Low | Yes |
| [I9] WSJ/IBM | High (journalism) | Verifiable | N/A | High | 2022 | High | Yes |
| [I10] CNBC/Haven | High (journalism) | Verifiable | N/A | High | 2021 | High | Yes |
| [I11] AHIMA/NORC | High (professional assoc + academic) | Verifiable | US | High | 2023 | High | Yes |

*Vendor sponsorship or low objectivity noted in manuscript text.

### Add Citation

```
[A36] Tyndall, J. (2010). AACODS Checklist. Flinders University.
      https://dspace.flinders.edu.au/jspui/bitstream/2328/3326/4/AACODS_Checklist.pdf
```

### Revise In-Text References

For flagged sources, add qualifier:

**Before**:
> Forrester Research [I5] projects 206% three-year ROI...

**After**:
> Forrester Research [I5], in a Microsoft-sponsored study, projects 206% three-year ROI...

## Checklist

```
[ ] Add Section 3.6 Grey Literature Quality Assessment
[ ] Add AACODS table
[ ] Add [A36] Tyndall citation
[ ] Revise in-text references for [I3], [I5], [I6]
[ ] Verify all industry source URLs still accessible
```
