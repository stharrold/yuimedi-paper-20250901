# Claude Code Implementation Prompt: YuiQuery Whitepapers Remediation

## Context
You are implementing critical fixes to the YuiQuery Whitepapers project. The original project plan has major flaws that will cause failure. You have a JSON file with validated remediation steps that must be executed systematically.

## Files
- **Implementation instructions**: `/Users/stharrold/Documents/GitHub/yuimedi-paper-20250901/yuiquery-implementation-json.json`
- **Target document**: `/Users/stharrold/Documents/GitHub/yuimedi-paper-20250901/github-project-guide-v2.md`

## Phase 1: Setup and Backup (IMMEDIATE)

1. **Create backup**:
```bash
cd /Users/stharrold/Documents/GitHub/yuimedi-paper-20250901
cp github-project-guide-v2.md github-project-guide-v2-backup-$(date +%Y%m%d).md
```

2. **Read and parse JSON**:
```bash
cat yuiquery-implementation-json.json | python3 -m json.tool
```

3. **Create implementation tracking**:
```bash
echo "# Implementation Progress $(date)" > implementation-log.md
echo "Original guide backed up to: github-project-guide-v2-backup-$(date +%Y%m%d).md" >> implementation-log.md
```

## Phase 2: Repository Creation

Execute from JSON `phase_1_critical_fixes.tasks[1].commands`:
```bash
# Create GitHub repository
gh repo create yuimedi/yuiquery-whitepapers --public --clone
cd yuiquery-whitepapers

# Create project
gh project create --owner yuimedi --title 'YuiQuery Research Papers'

# Setup directory structure
mkdir -p docs/{paper1,paper2,paper3}/{research,data,figures}
mkdir -p src/{algorithms,analysis,mapping}
mkdir -p project-management/{budget,compliance,risks}
```

## Phase 3: Update Original Guide

Edit `github-project-guide-v2.md` with these critical changes:

### Section: Timeline Overview
REPLACE:
```
**Start Date:** 2025-08-01  
**End Date:** 2026-02-26
```
WITH:
```
**Start Date:** 2025-09-02  
**End Date:** 2026-03-15
**CRITICAL CHANGES:**
- Paper 1 deadline: 2025-09-30 (for HIMSS abstract Oct 15)
- Paper 2 deadline: 2025-12-20 (holiday buffer added)
- Paper 3 deadline: 2026-03-15 (for AMIA abstract Mar 1)
```

### Section: Executive Decisions
ADD after existing content:
```
## Implementation Status (Updated: $(date))
- [IN PROGRESS] Backup developer assignment (Deadline: Sept 6)
- [PENDING] Budget approval for $28,700 total
- [COMPLETE] Repository created at yuimedi/yuiquery-whitepapers
- [PENDING] IRB determination filing
```

### Section: Adjusted Time Estimates
REPLACE entire section with:
```
## Revised Scope (30% Reduction)
- **Paper 1:** 70 hours (was 100)
- **Paper 2:** 70 hours (was 100)  
- **Paper 3:** 70 hours (was 100)
- **Total:** 210 hours (was 330)

Deliverables reduced to:
- MUST: Academic paper only
- SHOULD: Conference abstract
- REMOVED: Blog posts, webinar materials
```

## Phase 4: Compliance Setup

Execute from JSON `phase_2_compliance.tasks`:
```bash
# Create compliance documentation
mkdir -p compliance/irb
echo "# IRB Determination

Project uses de-identified data per HIPAA standards.
No human subjects research per 45 CFR 46.

Reference: https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html
Submitted: $(date)" > compliance/irb/determination.md

# Setup synthetic data
git clone https://github.com/synthetichealth/synthea.git ./data/synthea
cd ./data/synthea && ./run_synthea -p 100
```

## Phase 5: Create Risk Register

Create `project-management/risks/risk-register.csv`:
```csv
risk,probability,impact,mitigation,owner,review_date
DSH_unavailable,high,critical,backup_assigned,YLT,weekly
data_access_fails,medium,high,synthetic_data_ready,DSH,2025-10-15
budget_overrun,medium,medium,phased_approval,YLT,monthly
conference_deadline,low,medium,abstracts_ready_early,DSH,2025-09-15
```

## Phase 6: GitHub Milestones

Execute:
```bash
gh api repos/yuimedi/yuiquery-whitepapers/milestones \
  --method POST \
  --field title="Paper 1: Literature Review" \
  --field due_on="2025-09-30T23:59:59Z"

gh api repos/yuimedi/yuiquery-whitepapers/milestones \
  --method POST \
  --field title="Paper 2: Proof of Concept" \
  --field due_on="2025-12-20T23:59:59Z"

gh api repos/yuimedi/yuiquery-whitepapers/milestones \
  --method POST \
  --field title="Paper 3: FHIR Mapping" \
  --field due_on="2026-03-15T23:59:59Z"
```

## Phase 7: Quality Gates Documentation

Create `project-management/quality-gates.md`:
```markdown
# Quality Gates

## Gate 1: Literature Validation (Paper 1)
- Criteria: Minimum 10 validated sources
- TRL Level: 3 (NASA standard)
- Decision: YLT designated member
- Deadline: 2025-09-25

## Gate 2: Algorithm Accuracy (Paper 2)
- Criteria: 85% accuracy minimum
- Reference: https://arxiv.org/abs/1811.12808
- Testing: Against synthetic dataset
- Deadline: 2025-12-10

## Gate 3: Interoperability (Paper 3)
- Criteria: 3+ system mappings
- Standard: FHIR R4
- Systems: Epic, CMS, OMOP
- Deadline: 2026-03-01
```

## Phase 8: Budget Documentation

Create `project-management/budget/budget-final.json`:
```json
{
  "primary_work": {
    "hours": 210,
    "rate": 75,
    "total": 15750
  },
  "backup_coverage": {
    "hours": 100,
    "rate": 75,
    "total": 7500
  },
  "sme_reviews": {
    "hours": 18,
    "rate": 150,
    "total": 2700
  },
  "publication_fees": 3500,
  "tools_and_setup": 1000,
  "total": 30450,
  "contingency_10_percent": 3045,
  "grand_total": 33495
}
```

## Phase 9: GitHub Actions

Create `.github/workflows/project-tracking.yml`:
```yaml
name: Project Tracking
on:
  schedule:
    - cron: '0 10 * * 2'  # Weekly Tuesday 10am
  issues:
    types: [opened, closed]
    
jobs:
  track-progress:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Update metrics
        run: |
          echo "Week $(date +%V): Progress update" >> progress.log
          gh project item-list 1 --owner yuimedi --format json > metrics.json
      - name: Check gates
        run: |
          python3 scripts/check-quality-gates.py
```

## Phase 10: Validation and Reporting

1. **Verify all changes**:
```bash
# Check repository exists
gh repo view yuimedi/yuiquery-whitepapers

# Verify milestones
gh api repos/yuimedi/yuiquery-whitepapers/milestones

# Test synthetic data
ls -la ./data/synthea/output/fhir/*.json | head -5
```

2. **Generate implementation report**:
```bash
echo "# Implementation Report - $(date)

## Completed Actions
- [x] Repository created
- [x] Project structure setup
- [x] Budget documented ($33,495 total)
- [x] Timeline adjusted for conferences
- [x] Scope reduced by 30%
- [x] Risk register created
- [x] Quality gates defined

## Pending Actions
- [ ] Backup developer hired (Deadline: Sept 6)
- [ ] IRB determination filed (Deadline: Sept 9)
- [ ] Executive budget approval (Deadline: Sept 6)

## Risk Status
- **HIGH**: Single point of failure (DSH) - MITIGATION IN PROGRESS
- **MEDIUM**: Data access - SYNTHETIC BACKUP READY
- **LOW**: Conference deadlines - TIMELINE ADJUSTED

## Success Probability
- Original plan: 20%
- With fixes: 60%
- Current status: 45% (pending backup developer)
" > implementation-report.md
```

## Critical Success Factors

Execute ALL phases in order. Do NOT skip:
- Backup creation (Phase 1)
- Budget documentation showing $33,495 total
- Scope reduction removing blog/webinar deliverables
- Risk register with DSH backup as critical
- Conference deadline alignments

## Verification Commands

After completion, run:
```bash
# Verify all files created
find . -type f -name "*.md" -o -name "*.json" -o -name "*.csv" | grep -E "(budget|risk|gate|implementation)" 

# Check git status
git status

# Create summary
echo "Implementation complete. Key changes:
- Budget increased to $33,495 (was unspecified)
- Timeline extended to March 2026 (was February)
- Scope reduced by 30% (removed marketing deliverables)
- Backup developer role defined (addressing critical risk)
- Conference deadlines properly aligned
" > IMPLEMENTATION_SUMMARY.txt
```

## Final Step

Update the original guide's header:
```markdown
# GitHub Project Setup Guide - YuiQuery Whitepapers
**VERSION: 3.0 - REMEDIATED**
**Last Updated: $(date)**
**Implementation Status: COMPLETE**
**Success Probability: 60% (was 20%)**
```