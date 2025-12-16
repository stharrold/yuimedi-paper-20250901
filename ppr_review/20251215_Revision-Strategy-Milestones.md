# NL2SQL Healthcare Paper Series: Revision Strategy & Milestones

## Executive Summary

Three-paper series submitted to JMIR Medical Informatics using open-source GCP implementation with Synthea synthetic data. This approach eliminates commercial COI concerns while maintaining scientific rigor.

| Paper | Focus | Target | Timeline |
|-------|-------|--------|----------|
| Paper 1 | Three-Pillar Analytical Framework | JMIR Medical Informatics | Dec 31, 2025 |
| Paper 2 | Reference Implementation (GCP/Synthea) | JMIR Medical Informatics | Jan 31, 2026 |
| Paper 3 | FHIR/OMOP Schema Mapping | JMIR Medical Informatics | Mar 15, 2026 |

---

## Revised Milestones

### Milestone 1: Paper 1 - Three-Pillar Analytical Framework

**Title**: Natural Language Analytics in Healthcare: A Three-Pillar Framework Connecting Analytics Maturity, Workforce Turnover, and Technical Barriers

**Due Date**: December 31, 2025

**Target Venue**: JMIR Medical Informatics (primary), arXiv cs.CL (preprint)

**Description**:
```
Narrative review presenting novel analytical framework synthesizing three
interdependent healthcare analytics challenges. Pure evidence synthesis
with no solution advocacy.

Deliverables:
- Three-pillar framework (analytics maturity, turnover, NL2SQL barriers)
- Updated literature (replace 2004 turnover data with 2020+ sources)
- PRISMA-ScR methodology documentation
- Verified citations (academic + industry)
- Publication-ready manuscript

Scope (from original paper):
- Sections 1-4 (Executive Summary through Literature Review)
- Section 4.6 (Gaps in Current Literature)
- Section 4.7 (Why Problem Persists) - revised, speculative claims removed
- Appendices A-B (Glossary, HIMSS AMAM)

Excluded (moves to Paper 2):
- Section 5 (Proposed Solution)
- Section 6 (Evaluation)
- Appendix C (SQL examples)
```

**State**: In Progress (revision phase)

**Priority**: High

**Key Revisions Required**:
```
[x] Split solution content to Paper 2
[ ] Update turnover statistics (replace [A10] 2004 data)
[ ] Add PRISMA-ScR flow diagram
[ ] Add search strategy table
[ ] Revise Section 4.7 (remove speculative market claims)
[ ] Expert review (2-3 colleagues)
[ ] Revise COI statement (no product recommendations)
```

**Success Criteria**:
- Three-pillar framework clearly articulated as novel contribution
- All statistics from sources dated 2020+
- No product recommendations or vendor mentions
- Methodology section includes search documentation
- Ready for JMIR submission

**COI Statement (Paper 1)**:
```
S.T.H. is employed by Indiana University Health and serves as product
advisor to YuiMedi, a healthcare analytics company. This framework
analysis contains no product recommendations and was conducted
independently. The author takes full responsibility for the content.
```

---

### Milestone 2: Paper 2 - Reference Implementation

**Title**: Healthcare Knowledge Portal Reference Implementation: Query Memoization Architecture for Institutional Memory Preservation Using Cloud-Native Services and Synthetic EHR Data

**Due Date**: January 31, 2026 (revised from Jan 10)

**Target Venue**: JMIR Medical Informatics

**Description**:
```
Empirical validation of Healthcare Knowledge Portal architecture using
open-source GCP implementation with Synthea synthetic data. Demonstrates
query memoization as institutional knowledge preservation mechanism.

Implementation Stack:
- Google Cloud Platform (Vertex AI, BigQuery, Cloud Functions)
- Synthea SyntheticMass dataset (https://synthea.mitre.org/downloads)
- Open-source codebase (GitHub, Apache 2.0 license)

Deliverables:
- Knowledge portal paradigm literature review [A25-A28]
- Query memoization architecture (resolution hierarchy)
- Security/governance framework (HIPAA-aligned)
- GCP reference implementation
- Performance benchmarking on Synthea data
- Accuracy metrics with confidence scoring
- Cache hit rate progression analysis
- Risk mitigation for 30% LLM failure rate
- Open-source code repository
- Publication-ready manuscript

Key Architectural Components:
1. Query Resolution Hierarchy
   - Exact match: cached SQL (confidence 1.0)
   - Semantic similarity: cached + parameter substitution
   - Novel query: LLM generation (human validation flag)

2. Institutional Learning Loop
   - Validated queries enter cache
   - Cache grows as organizational corpus
   - Staff turnover does not lose query patterns

3. Security Architecture
   - Query allowlist/blocklist
   - PHI exposure prevention
   - Role-based restrictions
   - Audit trail
   - Prompt injection mitigation
```

**State**: Open

**Priority**: High

**Key Development Tasks**:
```
[ ] Literature review: Knowledge portal paradigm [A25-A28]
[ ] Download/configure Synthea SyntheticMass dataset
[ ] Design GCP architecture (Vertex AI, BigQuery, Cloud Functions)
[ ] Implement query memoization system
[ ] Implement security framework
[ ] Develop testing framework
[ ] Execute benchmarking experiments
[ ] Statistical analysis
[ ] Document cache hit rate progression
[ ] Open-source code repository setup
[ ] Draft manuscript
[ ] Expert review
[ ] Final revisions
```

**Success Criteria**:
- Query accuracy >85% on Synthea dataset
- Cache hit rate metrics documented (baseline -> 6-month projection)
- Security framework HIPAA-aligned
- Statistical significance demonstrated (p<0.05)
- Reproducible methodology (open-source code)
- 30% failure rate explicitly addressed with mitigations
- Knowledge preservation mechanism empirically validated

**COI Statement (Paper 2)**:
```
S.T.H. is employed by Indiana University Health and serves as product
advisor to YuiMedi, a healthcare analytics company. This research uses
an independent open-source implementation on public synthetic data and
does not evaluate any commercial products. Code is available at [GitHub
URL] under Apache 2.0 license. The author takes full responsibility for
the content.
```

---

### Milestone 3: Paper 3 - Schema Mapping & Interoperability

**Title**: Meta-Level Schema Mapping for Healthcare Knowledge Portals: FHIR R4 and OMOP CDM v5.4 Interoperability Framework

**Due Date**: March 15, 2026

**Target Venue**: JMIR Medical Informatics

**Description**:
```
Extension of Paper 2 reference implementation to multi-schema
interoperability using FHIR R4 and OMOP CDM v5.4.

Deliverables:
- FHIR R4 and OMOP CDM v5.4 mapping architecture
- Healthcare terminology integration (ICD-10, CPT, SNOMED, RxNorm)
- Query translation framework (NL -> schema-appropriate SQL)
- Interoperability testing on multiple schema representations
- Extension to Paper 2 open-source implementation
- Publication-ready manuscript

Technical Scope:
- Synthea data in native format
- Synthea data converted to OMOP CDM
- FHIR R4 resource mapping
- Cross-schema query translation
- Terminology service integration
```

**State**: Open

**Priority**: Medium

**Key Development Tasks**:
```
[ ] FHIR R4 / OMOP CDM v5.4 documentation review
[ ] Design mapping architecture
[ ] Implement schema detection/routing
[ ] Develop query translation layer
[ ] Terminology service integration
[ ] Cross-schema testing
[ ] Interoperability validation
[ ] Documentation
[ ] Draft manuscript
[ ] Technical review
[ ] Final revisions
```

**Success Criteria**:
- Successful mapping to minimum 3 schema representations
- FHIR R4 compliance validated
- OMOP CDM v5.4 adherence confirmed
- Query translation accuracy >90%
- Interoperability demonstrated across schemas
- Healthcare terminology standards integrated

**COI Statement (Paper 3)**:
```
[Same as Paper 2]
```

---

## JMIR Submission Strategy

### Why JMIR Medical Informatics

1. **COI Policy**: Granular disclosure forms; transparent process
2. **Scope Fit**: Health informatics systems, implementation research
3. **Series Support**: Supports article linking, cross-referencing
4. **Open Access**: Results accessible to practitioners
5. **Review Timeline**: ~8-12 weeks (reasonable for series pacing)

### Submission Sequence

```
Paper 1: Submit Dec 31, 2025
         Expected decision: Feb 2026

Paper 2: Submit Jan 31, 2026 (reference Paper 1 as "under review")
         If Paper 1 accepted, update reference
         Expected decision: Mar-Apr 2026

Paper 3: Submit Mar 15, 2026 (reference Papers 1-2)
         Expected decision: May-Jun 2026
```

### Cover Letter Strategy

**Paper 1**:
```
"This narrative review presents a novel three-pillar framework..."
[Standard submission]
```

**Paper 2**:
```
"This implementation study builds on our analytical framework
(Harrold, [status] in JMIR Medical Informatics). We demonstrate
a reference implementation using open-source tools and public
synthetic data, enabling independent replication..."
```

**Paper 3**:
```
"This paper extends our Healthcare Knowledge Portal reference
implementation (Papers 1-2) to address healthcare data
interoperability challenges..."
```

---

## Paper 1: Detailed Revision Checklist

### Critical (Must Complete)

#### 1. Update Turnover Statistics
**Current Problem**: [A10] Ang & Slaughter 2004 data is 20 years old.

**Action Items**:
```
[ ] Search: "healthcare IT workforce turnover 2020-2024"
[ ] Target sources:
    - HIMSS Workforce Survey (annual)
    - AHIMA/NORC 2023 survey [I11] - expand usage
    - CHIME CIO surveys
    - Becker's Healthcare IT reports
[ ] Replace 34% calculation with current validated figure
[ ] If unavailable, qualify: "Historical data suggests..."
```

#### 2. Strengthen Methodology Section
**Action Items**:
```
[ ] Add search strategy table:
    | Database | Search Terms | Date Range | Results |
    |----------|--------------|------------|---------|
    | PubMed   | ...          | 2019-2024  | N       |

[ ] Add PRISMA-ScR flow diagram
[ ] Document single-coder limitation explicitly
[ ] Consider OSF post-hoc registration
```

#### 3. Revise Section 4.7 Market Analysis
**Action Items**:
```
[ ] Remove: "Major technology providers may face inherent tensions..."
[ ] Keep: Watson Health/Haven case studies [I9, I10] as observed patterns
[ ] Reframe as "observed patterns" not "structural disincentives"
[ ] Add: "Further research needed to establish causal mechanisms"
```

### High Priority

#### 4. Remove Solution Advocacy
```
[ ] Delete or move Section 5 entirely
[ ] Delete or move Section 6 entirely
[ ] Remove promotional language ("strategic imperative", "call to action")
[ ] Ensure conclusion focuses on framework contribution, not solution
```

#### 5. Framework Validation
```
[ ] Add section: "Framework Development and Validation"
[ ] Document iterative emergence from literature
[ ] Solicit 2-3 expert reviews before submission
[ ] Map to existing frameworks (HIMSS, DIKW hierarchy)
```

---

## Paper 2: Detailed Development Checklist

### Critical

#### 1. Reframe Using Knowledge Portal Paradigm
**Action Items**:
```
[ ] Replace terminology:
    "Conversational AI platform" -> "Healthcare Knowledge Portal"
    "Democratize analytics" -> "Enable self-service analytics"

[ ] Add theoretical grounding:
    - Knowledge portal paradigm [A25, A26]
    - SECI model (tacit/explicit conversion) [A27]
    - Organizational memory systems [A28]
```

#### 2. Implement Query Memoization Architecture
**Action Items**:
```
[ ] Design query resolution hierarchy:
    1. Exact match -> cached SQL (confidence 1.0)
    2. Semantic similarity -> cached + parameter substitution
    3. Novel query -> LLM generation (human validation)

[ ] Implement institutional learning loop:
    - Validated queries enter cache
    - Cache grows as organizational corpus
    - Persistence mechanism (BigQuery table or similar)

[ ] Define metrics:
    | Stage      | Cache Hit Rate | Risk Profile |
    |------------|----------------|--------------|
    | Month 1-3  | 10-20%         | High         |
    | Month 6-12 | 50-70%         | Medium       |
    | Year 2+    | 80-90%         | Low          |
```

#### 3. Address 30% Failure Rate
**Action Items**:
```
[ ] Add section: "Clinical Safety Considerations"
    - Query failure modes:
      * Syntactically invalid (detectable)
      * Semantically incorrect (silent failures)
      * Correct SQL, wrong interpretation

    - Risk matrix:
      | Failure Type | Probability | Impact   | Mitigation          |
      |--------------|-------------|----------|---------------------|
      | Syntax error | 5%          | Low      | Auto-detect         |
      | Wrong table  | 15%         | High     | Schema validation   |
      | Wrong filter | 10%         | Critical | Result bounds check |

    - Mitigations:
      * Human-in-the-loop for clinical decisions
      * Confidence scoring with thresholds
      * Query result validation rules
      * Cached queries bypass LLM risk entirely
```

#### 4. Security/Governance Framework
**Action Items**:
```
[ ] Add section: "Security Architecture"
    - Query allowlist/blocklist patterns
    - PHI exposure prevention (no SELECT * on patient tables)
    - Role-based query restrictions
    - Audit trail (who, what, when)
    - Prompt injection mitigation

[ ] Reference standards:
    - NIST Cybersecurity Framework [A31]
    - HITRUST CSF [A32]
    - HIPAA Security Rule technical safeguards
```

### High Priority

#### 5. GCP Implementation Design
**Action Items**:
```
[ ] Architecture components:
    - Vertex AI: LLM inference (Gemini or PaLM)
    - BigQuery: Synthea data warehouse + query cache
    - Cloud Functions: API layer
    - Cloud Run: Web interface (optional)
    - Secret Manager: API keys, credentials

[ ] Synthea data setup:
    - Download SyntheticMass (1M patients)
    - Load to BigQuery
    - Document schema mapping

[ ] Open-source repository:
    - GitHub public repo
    - Apache 2.0 license
    - README with setup instructions
    - Terraform/deployment scripts
```

#### 6. Empirical Validation Framework
**Action Items**:
```
[ ] Study design: Mixed-methods evaluation

[ ] Primary outcomes:
    - Query accuracy (% matching expert-validated)
    - Time-to-insight (minutes to answer standard queries)
    - Cache hit rate progression

[ ] Secondary outcomes:
    - User satisfaction (SUS score, if applicable)
    - Error rate by query complexity
    - Novel vs cached query distribution

[ ] Test query set:
    - 50+ healthcare analytics queries
    - Stratified by complexity
    - Expert-validated ground truth SQL

[ ] Statistical analysis:
    - Accuracy confidence intervals
    - Cache hit rate trends
    - Comparison to baseline (manual SQL)
```

#### 7. Quantify Success Metrics
**Action Items**:
```
[ ] Replace vague language:
    "significant reduction" -> "target: 50% reduction"
    "substantial improvement" -> "target: 30% improvement"

[ ] Define baselines:
    - Expert SQL development time for standard queries
    - Current error/revision rate
    - Manual query complexity ceiling
```

---

## Paper 3: Development Notes

### Scope
- Extends Paper 2 implementation to multi-schema support
- FHIR R4 resource mapping
- OMOP CDM v5.4 tables
- Cross-schema query translation

### Key Technical Challenges
```
1. Schema detection: Identify source schema from NL query context
2. Terminology mapping: ICD-10 <-> SNOMED <-> OMOP concepts
3. Query translation: Same NL query -> different SQL by schema
4. Result normalization: Consistent output format across schemas
```

### Deferred to Paper 3
- Multi-institution federation (future work)
- Real-time FHIR API integration (future work)
- Clinical validation studies (requires IRB, real data)

---

## Citation Additions

### Paper 1 (replace/add)
```
[A10-NEW] Current healthcare IT turnover study (2022-2024) - TBD
[A29] PRISMA-ScR: Tricco et al. (2018). PRISMA Extension for Scoping Reviews
[A30] OSF pre-registration guidance
```

### Paper 2 (add)
```
[A25] Firestone, J.M., & McElroy, M.W. (2003). Key Issues in the New
      Knowledge Management. Butterworth-Heinemann.

[A26] Maier, R. (2007). Knowledge Management Systems: Information and
      Communication Technologies for Knowledge Management (3rd ed.). Springer.

[A27] Nonaka, I., & Takeuchi, H. (1995). The Knowledge-Creating Company.
      Oxford University Press.

[A28] Alavi, M., & Leidner, D.E. (2001). Review: Knowledge Management and
      Knowledge Management Systems. MIS Quarterly, 25(1), 107-136.

[A31] NIST. (2018). Framework for Improving Critical Infrastructure
      Cybersecurity, Version 1.1.

[A32] HITRUST Alliance. (2024). HITRUST CSF v11.

[A33] Greshake Tzovaras, B., et al. (2023). Not what you've signed up for:
      Compromising Real-World LLM-Integrated Applications with Indirect
      Prompt Injection. AISec '23.

[A34] Aamodt, A., & Plaza, E. (1994). Case-Based Reasoning: Foundational
      Issues, Methodological Variations, and System Approaches. AI
      Communications, 7(1), 39-59.

[A35] Walonoski, J., et al. (2018). Synthea: An approach, method, and
      software mechanism for generating synthetic patients and the
      synthetic electronic health care record. JAMIA, 25(3), 230-238.
      [Synthea citation]
```

---

## Pre-Submission Quality Gates

### Paper 1 (Framework)
```
[ ] No product recommendations or vendor mentions
[ ] All statistics from sources dated 2020+
[ ] Methodology section includes search strategy table
[ ] PRISMA-ScR flow diagram included
[ ] Three-pillar framework explicitly presented as novel contribution
[ ] Limitations section addresses single-author bias
[ ] Section 4.7 contains no speculative causal claims
[ ] COI statement accurate (advisor role disclosed, no product evaluation)
[ ] Expert review completed (2-3 reviewers)
```

### Paper 2 (Implementation)
```
[ ] Knowledge portal paradigm properly cited [A25-A28]
[ ] Query memoization architecture documented
[ ] Cache hit rate included as maturity metric
[ ] 30% failure rate explicitly addressed with mitigations
[ ] Security/governance framework complete
[ ] GCP implementation reproducible (open-source code)
[ ] Synthea dataset properly cited [A35]
[ ] Validation metrics quantified with baselines
[ ] All success metrics have specific targets (not "significant")
[ ] COI statement emphasizes independent implementation
[ ] Code repository public and documented
```

### Paper 3 (Interoperability)
```
[ ] References Papers 1-2 appropriately
[ ] FHIR R4 compliance documented
[ ] OMOP CDM v5.4 adherence confirmed
[ ] Cross-schema query translation accuracy >90%
[ ] Terminology mapping documented
[ ] Extension to Paper 2 codebase
[ ] COI statement consistent with series
```

---

## Timeline Summary

```
2025-12-15  Paper 1 revision begins
2025-12-31  Paper 1 submitted to JMIR + arXiv
2026-01-01  Paper 2 development begins
2026-01-15  GCP implementation complete
2026-01-25  Paper 2 benchmarking complete
2026-01-31  Paper 2 submitted to JMIR
2026-02-01  Paper 3 development begins
2026-02-28  Paper 1 decision expected
2026-03-15  Paper 3 submitted to JMIR
2026-04-30  Paper 2 decision expected
2026-06-15  Paper 3 decision expected
```

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Paper 1 rejected | Medium | High | Address reviewer feedback, resubmit |
| Updated turnover data unavailable | Low | Medium | Use multiple sources, qualify claims |
| GCP implementation delays | Medium | Medium | Start early, use familiar tools |
| Synthea schema complexity | Low | Low | Well-documented, community support |
| JMIR series not recognized | Low | Low | Cross-reference in each paper |
| Expert reviewers unavailable | Low | Low | Expand network, allow lead time |

---

## Appendix: Synthea Dataset Notes

**Source**: https://synthea.mitre.org/downloads

**SyntheticMass Dataset**:
- ~1 million synthetic patients
- Massachusetts geographic distribution
- Full EHR data (conditions, medications, procedures, observations)
- CSV and FHIR formats available

**BigQuery Loading**:
```sql
-- Example schema for conditions table
CREATE TABLE synthea.conditions (
  START DATE,
  STOP DATE,
  PATIENT STRING,
  ENCOUNTER STRING,
  CODE STRING,
  DESCRIPTION STRING
);
```

**Advantages for Research**:
- No PHI concerns
- Reproducible results
- Established benchmark in literature [A35]
- Free and publicly available
