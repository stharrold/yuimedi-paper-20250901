---
type: claude-context
directory: tests
purpose: Pytest test suite for skill validation
parent: ../CLAUDE.md
sibling_readme: null
children:
- ARCHIVED/CLAUDE.md
- lit_review/CLAUDE.md
- skills/CLAUDE.md
- unit/CLAUDE.md
---

# Claude Code Context: tests

## Purpose

Pytest test suite for validating workflow skills and utilities.

## Contents

- `conftest.py` - Shared fixtures
- `skills/` - Skill-specific tests
- `unit/` - Unit tests

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=.claude/skills --cov-report=term

# Run specific test category
uv run pytest tests/skills/ -v
uv run pytest tests/unit/ -v
```

## Test Organization

- `tests/skills/` - Tests for .claude/skills/ functionality
- `tests/unit/` - Unit tests for individual components

## Related

- **Parent**: [Root CLAUDE.md](../CLAUDE.md)

## Related Documentation

- **[../CLAUDE.md](../CLAUDE.md)** - Parent directory: Root

**Child Directories:**
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived
- **[lit_review/CLAUDE.md](lit_review/CLAUDE.md)** - Lit Review
- **[skills/CLAUDE.md](skills/CLAUDE.md)** - Skills
- **[unit/CLAUDE.md](unit/CLAUDE.md)** - Unit
