---
type: claude-context
directory: specs/apply-workflow-templates
purpose: Specifications for the apply-workflow-templates feature (GitHub Issue #239)
parent: ../CLAUDE.md
children:
  - ARCHIVED/CLAUDE.md
---

# Claude Code Context: apply-workflow-templates

## Purpose

Specifications for the apply-workflow-templates feature (GitHub Issue #239).

## Contents

- `spec.md` - Technical specification
- `plan.md` - Implementation plan with tasks
- `ARCHIVED/` - Deprecated specification files

## Feature Summary

This feature syncs updated workflow skills and commands from stharrold-templates to this repository:
- 9 skills in `.claude/skills/`
- 8 workflow commands in `.claude/commands/workflow/`
- Mirror in `.agents/` for cross-tool compatibility

## Key Tasks

1. Backup current skills (E1_001)
2. Sync skills directory (E2_001)
3. Sync commands directory (E3_001)
4. Sync .agents directory (E4_001)
5. Run pre-commit hooks (E5_001)
6. Run quality gates (E5_002)

## Related

- **Parent**: [specs](../CLAUDE.md)
- **Planning**: `planning/apply-workflow-templates/`
- **GitHub Issue**: #239
