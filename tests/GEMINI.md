---
type: claude-context
directory: tests
purpose: Pytest test suite for skill validation
parent: ../GEMINI.md
sibling_readme: null
children:
  - skills/GEMINI.md
  - unit/GEMINI.md
---

# Gemini Context Context: tests

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
uv run pytest --cov=.gemini/skills --cov-report=term

# Run specific test category
uv run pytest tests/skills/ -v
uv run pytest tests/unit/ -v
```

## Test Organization

- `tests/skills/` - Tests for .gemini/skills/ functionality
- `tests/unit/` - Unit tests for individual components

## Related

- **Parent**: [Root GEMINI.md](../GEMINI.md)

## Related Documentation

- **[../GEMINI.md](../GEMINI.md)** - Parent directory: Root

**Child Directories:**
- **[ARCHIVED/GEMINI.md](ARCHIVED/GEMINI.md)** - Archived
- **[lit_review/GEMINI.md](lit_review/GEMINI.md)** - Lit Review
- **[skills/GEMINI.md](skills/GEMINI.md)** - Skills
- **[unit/GEMINI.md](unit/GEMINI.md)** - Unit
