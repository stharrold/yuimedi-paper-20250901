# Specifications: Apply Workflow Templates

**Feature Slug:** apply-workflow-templates
**GitHub Issue:** #239
**Date:** 2025-11-28

## Overview

This directory contains specifications for syncing updated workflow skills and commands from the stharrold-templates repository.

## Contents

- **spec.md** - Technical specification defining what will be synced and how
- **plan.md** - Implementation plan with task breakdown
- **CLAUDE.md** - AI context for Claude Code
- **ARCHIVED/** - Deprecated specification files

## Quick Links

- [Technical Specification](spec.md)
- [Implementation Plan](plan.md)
- [Planning Documents](../../planning/apply-workflow-templates/) (in main repo)
- [GitHub Issue #239](https://github.com/stharrold/yuimedi-paper-20250901/issues/239)

## Summary

### What's Being Synced

| Component | Count | Source | Target |
|-----------|-------|--------|--------|
| Skills | 9 | `.tmp/stharrold-templates/.claude/skills/` | `.claude/skills/` |
| Commands | 8 | `.tmp/stharrold-templates/.claude/commands/` | `.claude/commands/` |
| Agents Mirror | 9 | `.tmp/stharrold-templates/.agents/` | `.agents/` |

### Skills Being Updated

1. agentdb-state-manager
2. bmad-planner
3. git-workflow-manager
4. initialize-repository
5. quality-enforcer
6. speckit-author
7. tech-stack-adapter
8. workflow-orchestrator
9. workflow-utilities

## Validation

After implementation, verify:
```bash
# Run quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py

# Run documentation validation
./validate_documentation.sh
```
