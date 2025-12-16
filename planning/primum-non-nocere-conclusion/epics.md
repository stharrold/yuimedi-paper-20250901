# Epics: Primum Non Nocere Conclusion Framework

**Feature Slug:** primum-non-nocere-conclusion
**GitHub Issue:** #293
**Created:** 2025-12-15

---

## Epic Overview

| Epic | Description | Priority | Estimated Effort |
|------|-------------|----------|------------------|
| E1 | Conclusion Structure Revision | High | Medium |
| E2 | Primum Non Nocere Integration | High | Medium |
| E3 | Tone Alignment & Review | Medium | Low |
| E4 | Quality Assurance | High | Low |

---

## Epic 1: Conclusion Structure Revision

### Goal
Transform conclusion from technology advocacy to evidence-based decision framework.

### Tasks

| ID | Task | Status | Notes |
|----|------|--------|-------|
| E1.1 | Read current conclusion (lines 702-740) | Pending | Understand exact wording |
| E1.2 | Draft revised opening paragraph | Pending | Remove "compelling evidence" advocacy |
| E1.3 | Revise "Summary of Contributions" item 3 | Pending | Remove "strategic imperative" language |
| E1.4 | Replace "Strategic Implications" section | Pending | New "Implications for Organizational Assessment" |
| E1.5 | Replace "Call to Action" section | Pending | New "Future Research Directions" + "Closing Reflection" |
| E1.6 | Review section flow and transitions | Pending | Ensure coherent narrative |

### Acceptance Criteria
- [ ] No advocacy language ("compelling evidence for implementing", "strategic imperative")
- [ ] No urgency language ("immediate action", "how quickly")
- [ ] Conclusion presents framework as decision-support tool
- [ ] Maintains academic tone throughout

---

## Epic 2: Primum Non Nocere Integration

### Goal
Integrate "First, do no harm" rhetorical framework addressing both adoption risks and inaction harms.

### Tasks

| ID | Task | Status | Notes |
|----|------|--------|-------|
| E2.1 | Draft "Dual Dimensions of Harm" section | Pending | ~200 words |
| E2.2 | Connect to three-pillar framework evidence | Pending | Analytics maturity, turnover, technical barriers |
| E2.3 | Add primum non nocere reference to opening | Pending | Latin term with translation |
| E2.4 | Integrate framework reference in closing | Pending | Evidence-based evaluation framing |
| E2.5 | Verify citation references [A10], [A24], [A6] | Pending | Ensure in-text citations valid |

### Content Draft: "Dual Dimensions of Harm"

```markdown
## The Dual Dimensions of Harm

Healthcare's traditional interpretation of *primum non nocere* counsels caution:
new technologies should be thoroughly validated before clinical deployment, and
governance frameworks should default to rejection until safety is established.
This principle has served healthcare well, protecting patients from unproven
interventions and maintaining professional standards.

However, the evidence reviewed in this paper suggests that *primum non nocere*
must be applied bidirectionally. The three-pillar analysis reveals substantial
harms from **inaction**:

- **Analytics maturity gaps** leave clinical decisions unsupported by available
  data, potentially compromising patient care optimization
- **Workforce turnover** (34% annually for healthcare IT staff [A10]) causes
  institutional memory loss costing organizations up to three times annual
  salary budgets [A24]
- **Technical barriers** disconnect clinical experts from data insights,
  delaying evidence-based practice improvements

These findings do not argue that healthcare organizations should abandon caution.
Rather, they suggest that a complete application of *primum non nocere* requires
evaluating **both** the risks of premature technology adoption **and** the ongoing
harms of maintaining current approaches. The three-pillar framework presented in
this review provides a structured approach for this dual evaluation.
```

### Acceptance Criteria
- [ ] Primum non nocere explicitly defined (Latin + English)
- [ ] Traditional interpretation acknowledged
- [ ] Evidence-based harm-of-inaction presented
- [ ] Three-pillar framework positioned as assessment tool
- [ ] Balanced tone (not advocacy)

---

## Epic 3: Tone Alignment & Review

### Goal
Ensure revised conclusion aligns with Paper 1 revision strategy and maintains academic objectivity.

### Tasks

| ID | Task | Status | Notes |
|----|------|--------|-------|
| E3.1 | Cross-reference revision strategy milestones | Pending | Check alignment with `20251215_Revision-Strategy-Milestones.md` |
| E3.2 | Remove/revise promotional language | Pending | "strategic imperative", "competitive advantage", etc. |
| E3.3 | Verify no product recommendations | Pending | Paper 1 scope |
| E3.4 | Self-review for advocacy tone | Pending | Objective assessment |
| E3.5 | Optional: Request peer review | Pending | Second opinion on tone |

### Revision Strategy Alignment Checklist

From `ppr_review/20251215_Revision-Strategy-Milestones.md`:

- [ ] No product recommendations or vendor mentions
- [ ] Three-pillar framework clearly articulated as novel contribution
- [ ] Methodology section includes search documentation (N/A - conclusion)
- [ ] Ready for JMIR submission

Paper 1 Pre-Submission Quality Gates (from milestones):
- [ ] No promotional language ("strategic imperative", "call to action")
- [ ] Section contains no speculative causal claims
- [ ] COI statement accurate (N/A - conclusion section)

### Acceptance Criteria
- [ ] Aligns with Paper 1 revision strategy
- [ ] Maintains academic objectivity
- [ ] No promotional/marketing language

---

## Epic 4: Quality Assurance

### Goal
Validate changes pass all quality gates and maintain paper integrity.

### Tasks

| ID | Task | Status | Notes |
|----|------|--------|-------|
| E4.1 | Run `./validate_documentation.sh` | Pending | 7 tests |
| E4.2 | Run `python scripts/validate_references.py --all` | Pending | Citation validation |
| E4.3 | Check cross-references to conclusion | Pending | Document Structure section references |
| E4.4 | Verify word count within limits | Pending | JMIR: 5,000-8,000 words |
| E4.5 | Update abstract if needed | Pending | May need minor adjustment |
| E4.6 | Rebuild paper artifacts | Pending | PDF, HTML, DOCX |

### Quality Gate Commands

```bash
# Documentation validation
./validate_documentation.sh

# Reference validation
python scripts/validate_references.py --all

# Format and lint
uv run ruff format . && uv run ruff check --fix .

# Build artifacts
./scripts/build_paper.sh --format all
```

### Acceptance Criteria
- [ ] All validation tests pass
- [ ] All citations verified
- [ ] Paper builds successfully in all formats
- [ ] No regressions in other sections

---

## Implementation Order

### Phase 1: Preparation
1. E1.1: Read current conclusion
2. E3.1: Cross-reference revision strategy

### Phase 2: Drafting
3. E2.1: Draft "Dual Dimensions of Harm"
4. E1.2: Draft revised opening
5. E1.3: Revise contributions item 3
6. E1.4: Replace strategic implications
7. E1.5: Replace call to action

### Phase 3: Integration
8. E2.2-E2.5: Connect framework, verify citations
9. E1.6: Review flow and transitions
10. E3.2-E3.5: Tone alignment

### Phase 4: Validation
11. E4.1-E4.6: Quality assurance

---

## Dependencies

```
E1.1 ─────────────────────────┐
                              ├─> E1.2, E1.3, E1.4, E1.5
E3.1 ─────────────────────────┘
                              │
E2.1 ─────────────────────────┤
                              ▼
                        E1.6, E2.2-E2.5
                              │
                              ▼
                        E3.2-E3.5
                              │
                              ▼
                        E4.1-E4.6
```

---

## Estimated Timeline

| Phase | Tasks | Duration |
|-------|-------|----------|
| Phase 1: Preparation | E1.1, E3.1 | 15 min |
| Phase 2: Drafting | E2.1, E1.2-E1.5 | 45 min |
| Phase 3: Integration | E2.2-E2.5, E1.6, E3.2-E3.5 | 30 min |
| Phase 4: Validation | E4.1-E4.6 | 15 min |
| **Total** | | **~2 hours** |

---

## Success Metrics

1. **Rhetorical effectiveness**: Conclusion presents balanced harm assessment
2. **Academic alignment**: No advocacy language detected
3. **Framework utility**: Three-pillar model positioned as decision tool
4. **Quality compliance**: All validation gates pass
5. **Stakeholder approval**: (Optional) Peer review confirms balanced tone
