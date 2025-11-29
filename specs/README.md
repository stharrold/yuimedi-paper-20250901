# Specifications

This directory contains feature specifications generated during workflow Phase 2 (SpecKit).

## Contents

| Feature | Issue | Status |
|---------|-------|--------|
| [apply-workflow-templates](apply-workflow-templates/) | #239 | In Progress |

## Structure

Each feature specification includes:
- **spec.md** - Technical specification
- **plan.md** - Implementation plan with task breakdown
- **CLAUDE.md** - AI context
- **README.md** - Human overview
- **ARCHIVED/** - Deprecated specification files

## Workflow

1. **Phase 1 (BMAD)**: Create planning documents in `planning/{slug}/`
2. **Phase 2 (SpecKit)**: Generate specifications in `specs/{slug}/`
3. **Phase 3 (Tasks)**: Extract tasks from `plan.md`
4. **Phase 4 (Implement)**: Execute tasks

## Related

- [Planning Documents](../planning/)
- [Workflow Commands](../.claude/commands/workflow/)
