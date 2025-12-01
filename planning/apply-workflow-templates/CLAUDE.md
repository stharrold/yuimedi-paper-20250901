---
type: claude-context
directory: planning/apply-workflow-templates
purpose: Planning documents for applying workflow templates from stharrold-templates
parent: ../CLAUDE.md
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
related_skills:
  - workflow-orchestrator
  - workflow-utilities
  - git-workflow-manager
---

# Claude Code Context: apply-workflow-templates

## Purpose

Planning documents for feature "apply-workflow-templates" (GitHub Issue #239).

## Contents

- `requirements.md` - Functional and non-functional requirements
- `architecture.md` - Sync strategy and file mapping
- `epics.md` - Task breakdown by epic

## Quick Reference

**Feature:** Apply workflow templates from `.tmp/stharrold-templates/`
**Scope:** 9 skills, 2 commands, .agents mirror
**Issue:** #248

## Next Steps

1. Create feature worktree with `/2_plan`
2. Execute sync in worktree
3. Validate with quality gates
4. Integrate via `/5_integrate`
