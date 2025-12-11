---
type: claude-context
directory: tests/skills
purpose: Tests for .claude/skills/ functionality
parent: ../CLAUDE.md
sibling_readme: null
children: []
---

# Claude Code Context: tests/skills

## Purpose

Tests for validating workflow skills functionality. Contains 289 tests covering:
- VCS provider detection and adapters (GitHub, Azure DevOps)
- Semantic versioning calculation
- Release and PR workflow automation
- Quality gates enforcement

## Contents

- `conftest.py` - Shared test fixtures
- `test_vcs_provider.py` - VCS provider detection tests (31 tests)
- `test_github_adapter.py` - GitHub API adapter tests (28 tests)
- `test_azure_adapter.py` - Azure DevOps API adapter tests (36 tests)
- `test_semantic_version.py` - Semantic versioning tests (44 tests)
- `test_release_workflow.py` - Release workflow tests (46 tests)
- `test_pr_workflow.py` - PR workflow tests (40 tests)
- `test_quality_gates.py` - Quality gates tests (27 tests)
- `test_quality_enforcer.py` - Quality enforcer tests (4 tests)
- `test_release_integration.py` - Release workflow integration tests (14 tests)
- `test_pr_integration.py` - PR workflow integration tests (19 tests)

## Running Tests

```bash
# Run skill tests only
uv run pytest tests/skills/ -v

# Run with coverage (targeted modules only)
uv run pytest tests/skills/ \
  --cov=.claude/skills/git-workflow-manager/scripts \
  --cov=.claude/skills/quality-enforcer/scripts \
  --cov=.claude/skills/workflow-utilities/scripts/vcs \
  --cov-report=term

# Skip integration tests (faster)
uv run pytest tests/skills/ -m "not integration" -v
```

## Coverage Targets

Key modules with 80%+ coverage:
- `semantic_version.py`: 100%
- `provider.py`: 100%
- `release_workflow.py`: 95%
- `github_adapter.py`: 89%
- `azure_adapter.py`: 90%
- `pr_workflow.py`: 87%
- `run_quality_gates.py`: 81%

## Related

- **Parent**: [tests/CLAUDE.md](../CLAUDE.md)
