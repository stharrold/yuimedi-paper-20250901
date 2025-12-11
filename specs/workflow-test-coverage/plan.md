# Implementation Plan: Workflow Test Coverage

**Type:** feature
**Slug:** workflow-test-coverage
**Date:** 2025-12-11
**GitHub Issue:** #241

## Overview

Improve test coverage for workflow skills from ~0% to 80%. Focus on unit tests with mocks for core utilities and integration tests for critical workflows.

## Task Breakdown

### Phase 1: Test Infrastructure Setup

#### Task T001: Create test fixtures and conftest.py

**Priority:** High
**Estimated Time:** 1-2 hours

**Files:**
- `tests/skills/conftest.py`

**Description:**
Set up pytest fixtures for mocking git commands, subprocess calls, and file system operations used by workflow skills.

**Steps:**
1. Create `tests/skills/conftest.py` with fixtures
2. Add fixture for mocking `subprocess.run`
3. Add fixture for temporary git repositories
4. Add fixture for mocking DuckDB connections
5. Add fixture for temporary file system paths

**Acceptance Criteria:**
- [ ] conftest.py created with reusable fixtures
- [ ] Git mock fixture works for simulating git commands
- [ ] Subprocess mock fixture captures command calls
- [ ] Temp directory fixture cleans up after tests

**Verification:**
```bash
uv run pytest tests/skills/conftest.py --collect-only
```

**Dependencies:** None

---

### Phase 2: VCS Adapter Unit Tests (FR-001)

#### Task T002: Unit tests for VCS provider detection

**Priority:** High
**Estimated Time:** 1-2 hours

**Files:**
- `tests/skills/test_vcs_provider.py`
- `.claude/skills/workflow-utilities/scripts/vcs/provider.py`

**Description:**
Test VCS provider detection from git remote URLs.

**Steps:**
1. Create test file `tests/skills/test_vcs_provider.py`
2. Test GitHub URL detection (https, ssh, git@ formats)
3. Test Azure DevOps URL detection
4. Test unknown provider handling
5. Test edge cases (no remote, invalid URLs)

**Acceptance Criteria:**
- [ ] GitHub URL patterns tested (3+ formats)
- [ ] Azure DevOps URL patterns tested
- [ ] Unknown provider returns appropriate result
- [ ] Error cases handled gracefully

**Verification:**
```bash
uv run pytest tests/skills/test_vcs_provider.py -v
```

**Dependencies:** T001

---

#### Task T003: Unit tests for GitHub adapter

**Priority:** High
**Estimated Time:** 2-3 hours

**Files:**
- `tests/skills/test_github_adapter.py`
- `.claude/skills/workflow-utilities/scripts/vcs/github_adapter.py`

**Description:**
Test GitHub CLI adapter methods with mocked `gh` command responses.

**Steps:**
1. Create test file `tests/skills/test_github_adapter.py`
2. Mock `subprocess.run` for `gh` commands
3. Test `create_pr()` with various inputs
4. Test `get_pr_status()` method
5. Test error handling (auth failure, rate limits, network errors)

**Acceptance Criteria:**
- [ ] create_pr() tested with valid inputs
- [ ] create_pr() handles missing gh CLI gracefully
- [ ] Error responses parsed correctly
- [ ] ≥80% coverage for github_adapter.py

**Verification:**
```bash
uv run pytest tests/skills/test_github_adapter.py -v --cov=.claude/skills/workflow-utilities/scripts/vcs/github_adapter
```

**Dependencies:** T001, T002

---

#### Task T004: Unit tests for Azure DevOps adapter

**Priority:** Medium
**Estimated Time:** 2-3 hours

**Files:**
- `tests/skills/test_azure_adapter.py`
- `.claude/skills/workflow-utilities/scripts/vcs/azure_adapter.py`

**Description:**
Test Azure DevOps CLI adapter methods with mocked `az` command responses.

**Steps:**
1. Create test file `tests/skills/test_azure_adapter.py`
2. Mock `subprocess.run` for `az` commands
3. Test `create_pr()` with various inputs
4. Test error handling (auth failure, project not found)

**Acceptance Criteria:**
- [ ] create_pr() tested with valid inputs
- [ ] create_pr() handles missing az CLI gracefully
- [ ] Error responses parsed correctly
- [ ] ≥80% coverage for azure_adapter.py

**Verification:**
```bash
uv run pytest tests/skills/test_azure_adapter.py -v --cov=.claude/skills/workflow-utilities/scripts/vcs/azure_adapter
```

**Dependencies:** T001, T002

---

### Phase 3: Release Workflow Unit Tests (FR-002)

#### Task T005: Unit tests for semantic version calculation

**Priority:** High
**Estimated Time:** 1-2 hours

**Files:**
- `tests/skills/test_semantic_version.py`
- `.claude/skills/git-workflow-manager/scripts/semantic_version.py`

**Description:**
Test version calculation logic (major, minor, patch increments).

**Steps:**
1. Create test file `tests/skills/test_semantic_version.py`
2. Test `calculate_next_version()` for major bumps
3. Test `calculate_next_version()` for minor bumps
4. Test `calculate_next_version()` for patch bumps
5. Test edge cases (first release, prerelease tags)

**Acceptance Criteria:**
- [ ] Major version bump tested (1.2.3 → 2.0.0)
- [ ] Minor version bump tested (1.2.3 → 1.3.0)
- [ ] Patch version bump tested (1.2.3 → 1.2.4)
- [ ] First release (no tags) handled

**Verification:**
```bash
uv run pytest tests/skills/test_semantic_version.py -v
```

**Dependencies:** T001

---

#### Task T006: Unit tests for release workflow

**Priority:** High
**Estimated Time:** 2-3 hours

**Files:**
- `tests/skills/test_release_workflow.py`
- `.claude/skills/git-workflow-manager/scripts/release_workflow.py`

**Description:**
Test release workflow logic with mocked git operations.

**Steps:**
1. Create test file `tests/skills/test_release_workflow.py`
2. Mock git commands (branch, checkout, tag, push)
3. Test `create_release_branch()` function
4. Test `tag_release()` function
5. Test branch validation logic
6. Test error scenarios (uncommitted changes, branch exists)

**Acceptance Criteria:**
- [ ] Release branch creation tested
- [ ] Tag creation tested
- [ ] Error cases tested (dirty working tree)
- [ ] ≥80% coverage for release_workflow.py

**Verification:**
```bash
uv run pytest tests/skills/test_release_workflow.py -v --cov=.claude/skills/git-workflow-manager/scripts/release_workflow
```

**Dependencies:** T001, T005

---

### Phase 4: PR Workflow Unit Tests (FR-003)

#### Task T007: Unit tests for PR workflow

**Priority:** High
**Estimated Time:** 2-3 hours

**Files:**
- `tests/skills/test_pr_workflow.py`
- `.claude/skills/git-workflow-manager/scripts/pr_workflow.py`

**Description:**
Test PR creation and update logic with mocked VCS operations.

**Steps:**
1. Create test file `tests/skills/test_pr_workflow.py`
2. Mock VCS adapter methods
3. Test `create_pr()` function with GitHub
4. Test `create_pr()` function with Azure DevOps
5. Test PR body generation
6. Test error handling (PR already exists, permission denied)

**Acceptance Criteria:**
- [ ] PR creation tested for both VCS providers
- [ ] PR body formatting tested
- [ ] Error cases handled
- [ ] ≥80% coverage for pr_workflow.py

**Verification:**
```bash
uv run pytest tests/skills/test_pr_workflow.py -v --cov=.claude/skills/git-workflow-manager/scripts/pr_workflow
```

**Dependencies:** T001, T003, T004

---

### Phase 5: Quality Gate Unit Tests (FR-004)

#### Task T008: Unit tests for quality gates

**Priority:** High
**Estimated Time:** 2-3 hours

**Files:**
- `tests/skills/test_quality_gates.py`
- `.claude/skills/quality-enforcer/scripts/run_quality_gates.py`

**Description:**
Test quality gate execution and result aggregation.

**Steps:**
1. Expand `tests/skills/test_quality_enforcer.py` or create `test_quality_gates.py`
2. Mock subprocess calls for pytest, ruff, mypy
3. Test individual gate execution
4. Test result aggregation logic
5. Test threshold checking (pass/fail at different coverage levels)
6. Test output formatting

**Acceptance Criteria:**
- [ ] Individual gates tested (pytest, ruff, mypy)
- [ ] Result aggregation tested
- [ ] Threshold logic tested (20%, 40%, 60%, 80%)
- [ ] ≥80% coverage for run_quality_gates.py

**Verification:**
```bash
uv run pytest tests/skills/test_quality_gates.py -v --cov=.claude/skills/quality-enforcer/scripts/run_quality_gates
```

**Dependencies:** T001

---

### Phase 6: Integration Tests (FR-005)

#### Task T009: Integration test for release workflow

**Priority:** Medium
**Estimated Time:** 2-3 hours

**Files:**
- `tests/skills/integration/test_release_integration.py`

**Description:**
End-to-end test for release workflow using a temporary git repository.

**Steps:**
1. Create `tests/skills/integration/` directory
2. Create test that initializes temp git repo
3. Create commits and tags
4. Run release workflow
5. Verify branch and tag creation
6. Clean up temp repo

**Acceptance Criteria:**
- [ ] Temp git repo created with commits
- [ ] Release workflow executes successfully
- [ ] Release branch created correctly
- [ ] Tag created with correct version

**Verification:**
```bash
uv run pytest tests/skills/integration/test_release_integration.py -v -m integration
```

**Dependencies:** T005, T006

---

#### Task T010: Integration test for PR workflow

**Priority:** Medium
**Estimated Time:** 2-3 hours

**Files:**
- `tests/skills/integration/test_pr_integration.py`

**Description:**
End-to-end test for PR workflow (without actual GitHub/Azure API calls).

**Steps:**
1. Create test that uses mocked VCS adapter
2. Create temp git repo with feature branch
3. Run PR workflow
4. Verify PR metadata generated correctly
5. Verify branch handling

**Acceptance Criteria:**
- [ ] PR workflow executes with mocked VCS
- [ ] PR body generated correctly
- [ ] Branch operations work correctly
- [ ] No actual API calls made

**Verification:**
```bash
uv run pytest tests/skills/integration/test_pr_integration.py -v -m integration
```

**Dependencies:** T007

---

### Phase 7: Coverage Threshold Updates (FR-006)

#### Task T011: Update coverage threshold incrementally

**Priority:** Medium
**Estimated Time:** 1 hour

**Files:**
- `.claude/skills/quality-enforcer/scripts/run_quality_gates.py`
- `pyproject.toml` or `pytest.ini`

**Description:**
Update coverage thresholds as tests are added.

**Steps:**
1. After T001-T004: Update threshold to 20%
2. After T005-T007: Update threshold to 40%
3. After T008: Update threshold to 60%
4. After T009-T010: Update threshold to 80%
5. Verify all tests pass at each threshold

**Acceptance Criteria:**
- [ ] Coverage ≥20% after Phase 2
- [ ] Coverage ≥40% after Phase 3-4
- [ ] Coverage ≥60% after Phase 5
- [ ] Coverage ≥80% after Phase 6

**Verification:**
```bash
uv run pytest tests/skills/ --cov=.claude/skills --cov-fail-under=80
```

**Dependencies:** T001-T010

---

## Task Summary

| Task ID | Name | Priority | Dependencies | Status |
|---------|------|----------|--------------|--------|
| T001 | Test fixtures and conftest.py | High | None | Pending |
| T002 | VCS provider detection tests | High | T001 | Pending |
| T003 | GitHub adapter tests | High | T001, T002 | Pending |
| T004 | Azure DevOps adapter tests | Medium | T001, T002 | Pending |
| T005 | Semantic version tests | High | T001 | Pending |
| T006 | Release workflow tests | High | T001, T005 | Pending |
| T007 | PR workflow tests | High | T001, T003, T004 | Pending |
| T008 | Quality gates tests | High | T001 | Pending |
| T009 | Release integration test | Medium | T005, T006 | Pending |
| T010 | PR integration test | Medium | T007 | Pending |
| T011 | Coverage threshold updates | Medium | T001-T010 | Pending |

## Task Dependencies Graph

```
T001 (fixtures) ──┬──> T002 (VCS provider) ──┬──> T003 (GitHub) ──┬──> T007 (PR workflow) ──> T010 (PR integration)
                  │                          │                    │
                  │                          └──> T004 (Azure) ───┘
                  │
                  ├──> T005 (semantic version) ──> T006 (release workflow) ──> T009 (release integration)
                  │
                  └──> T008 (quality gates)

T001-T010 ──> T011 (threshold updates)
```

## Parallel Work Opportunities

- T002 and T005 can run in parallel (both depend only on T001)
- T003 and T004 can run in parallel (VCS adapters)
- T008 can run in parallel with T002-T007 (only depends on T001)

## Quality Checklist

Before considering this feature complete:

- [ ] All 11 tasks completed
- [ ] Test coverage ≥ 80% for `.claude/skills/`
- [ ] All tests pass (`uv run pytest tests/skills/ -v`)
- [ ] Tests run in < 60 seconds total
- [ ] No integration tests marked without `@pytest.mark.integration`
- [ ] Linting clean (`uv run ruff check tests/skills/`)
- [ ] Type checking clean (`uv run mypy tests/skills/`)

## Notes

### Implementation Tips

- Use `unittest.mock.patch` for subprocess mocking
- Use `pytest.fixture` with `tmp_path` for temp directories
- Use `@pytest.mark.integration` for integration tests
- Keep unit tests fast (< 1 second each)

### Common Pitfalls

- Don't mock too broadly - mock at the subprocess level, not internal functions
- Remember to test error paths, not just happy paths
- Ensure fixtures clean up properly to avoid test pollution
