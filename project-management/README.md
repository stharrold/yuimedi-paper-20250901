# Project Management Directory

This directory contains detailed project management documentation for the YuiQuery Healthcare Analytics Research project.

## Overview

**Main Overview Document**: See [`project-management.md`](../project-management.md) at repository root for:
- Executive summary and business case
- Strategic positioning and ROI analysis
- Implementation status and milestones
- Quality gates and decision authority

This directory contains the **detailed supporting files** referenced in the overview.

## Directory Structure

```
project-management/
├── README.md                         # This file
├── ARCHIVED/                         # Deprecated project management files
├── budget/                           # Financial planning and tracking
│   └── budget-final.json             # Detailed budget breakdown ($33,495 total)
├── risks/                            # Risk assessment and mitigation
│   ├── risk-register-v2.csv          # Risk tracking matrix
│   └── risk-register.csv             # Original risk register
├── roles/                            # Team structure and responsibilities
│   ├── raci-matrix.csv               # Responsibility assignment matrix
│   └── backup-developer.md           # Contingency planning
├── github-milestones.md              # GitHub milestone configuration
├── methodology-validation-checklist.md  # Research methodology validation
├── probability-calculation.md        # Statistical methodology for risk assessment
├── quality-gates.md                  # Quality thresholds and acceptance criteria
├── risk-assessment-methodology.md    # Risk evaluation framework
├── risk-methodology-validation.md    # Validation of risk approach
└── risk-scoring-matrix.csv           # Quantitative risk scoring system
```

## Purpose

This directory provides:
- **Financial Governance**: Budget planning and expense tracking
- **Risk Management**: Comprehensive risk assessment and mitigation strategies
- **Team Coordination**: Role definitions and responsibility matrices
- **Quality Assurance**: Milestone gates and acceptance criteria

## Key Documents

### Budget & Financial
- **budget-final.json**: Complete financial breakdown
  - Total investment: $33,495
  - ROI timeline: 6-12 months
  - Cost categories: Personnel, SME review, infrastructure

### Risk Management
- **risk-register-v2.csv**: Active risk tracking
  - Identified risks across technical, business, and operational categories
  - Probability and impact scoring
  - Mitigation strategies and ownership

- **risk-assessment-methodology.md**: Framework for risk evaluation
  - Quantitative scoring methodology
  - Risk matrix calculations
  - Validation against industry standards

### Team & Roles
- **raci-matrix.csv**: Responsibility Assignment Matrix
  - Responsible, Accountable, Consulted, Informed for each task
  - Role definitions and escalation paths
  - Decision authority matrix

- **backup-developer.md**: Contingency planning
  - Backup developer assignment (completed Sept 3, 2025)
  - Knowledge transfer procedures
  - Single-point-of-failure mitigation

### Quality Assurance
- **quality-gates.md**: Milestone acceptance criteria
  - Phase gates with clear success metrics
  - Go/no-go decision thresholds
  - Quality validation procedures

## Relationship to Main Overview

```
project-management.md (root)
├── Executive Summary
├── Business Case
├── Strategic Decisions
└── References to detailed files in project-management/
    ↓
project-management/ (this directory)
├── budget/ - Financial details
├── risks/ - Risk management details
├── roles/ - Team structure details
└── *.md - Methodology and process details
```

**When to use which:**
- **Read project-management.md first**: For overview, executive summary, and strategic context
- **Use this directory**: For detailed planning, tracking, and operational management

## Project Health Metrics

### Current Status (Updated: 2025-12-18)
- **Paper 1**: Ready for submission (Dec 31, 2025 deadline)
- **Paper 2**: Planned (Jan 31, 2026 deadline)
- **Paper 3**: Planned (Mar 15, 2026 deadline)
- **Success Probability**: 75%
- **Budget Status**: On track ($33,495 approved)
- **Task Tracking**: [GitHub Issues](https://github.com/stharrold/yuimedi-paper-20250901/issues)

## Related Documentation

- [Main Project Management Overview](../project-management.md) - Strategic overview and executive summary
- [GitHub Issues](https://github.com/stharrold/yuimedi-paper-20250901/issues) - Active task tracking
- [TODO.md](../TODO.md) - Master workflow manifest
- [CLAUDE.md](../CLAUDE.md) - Project development standards

## Governance & Escalation

### Decision Authority
- **Budget Changes**: Requires executive approval over $5,000
- **Scope Changes**: Quality gate review and YLT approval
- **Risk Mitigation**: Project manager authority up to $2,500
- **Timeline Changes**: Stakeholder consultation required

---

*Project management documentation supporting YuiQuery Healthcare Analytics Research*
*See [project-management.md](../project-management.md) for strategic overview*
*Last Updated: 2025-12-18*
