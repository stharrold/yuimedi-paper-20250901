---
type: claude-context
directory: specs/research-session
purpose: Research session specifications for literature review
parent: /CLAUDE.md
---

# Research Session Specs

## Quick Reference

**Issue:** #368 (Schema Discovery and Validation)
**Branch:** feature/20251220T190333Z_research-session
**Scope:** Paper2

## Current Task

Iterative literature search using Google Scholar Labs to answer:
- Q7: Semantic table/column matching for NL2SQL

## Key Files

- `spec.md` - Technical specification
- `plan.md` - Task breakdown and workflow
- `../../docs/references/Research_Questions.md` - Question tracking
- `../../planning/research-session/` - BMAD planning documents

## Session Context

This is an interactive research session. The workflow:
1. User provides research question
2. Claude searches Google Scholar Labs via browser automation
3. Results are extracted and formatted
4. Findings saved to docs/references/
5. Repeat for additional questions
