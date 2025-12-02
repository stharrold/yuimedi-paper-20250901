# Epics: Academic Literature Review Workflow

**Issue:** #253
**Created:** 2025-12-01
**Status:** Draft

## Epic Overview

| Epic | Description | Priority | Dependencies |
|------|-------------|----------|--------------|
| E1 | Project Setup & Configuration | P0 | None |
| E2 | Domain Layer Implementation | P0 | E1 |
| E3 | Application Layer Implementation | P0 | E2 |
| E4 | Infrastructure Layer Implementation | P0 | E3 |
| E5 | CLI Interface Implementation | P0 | E4 |
| E6 | Testing & Quality Assurance | P0 | E2-E5 |
| E7 | Integration & Documentation | P1 | E6 |

---

## E1: Project Setup & Configuration

**Goal:** Establish project structure, dependencies, and development environment.

### Tasks

| ID | Task | Estimate |
|----|------|----------|
| E1.1 | Create `lit_review/` package structure | Small |
| E1.2 | Update `pyproject.toml` with new dependencies | Small |
| E1.3 | Create `.env.example` with API key templates | Small |
| E1.4 | Set up test directory structure | Small |
| E1.5 | Create pytest configuration | Small |
| E1.6 | Add mypy configuration for new package | Small |

### Acceptance Criteria

- [ ] Package structure matches architecture.md
- [ ] `uv sync` installs all dependencies
- [ ] `pytest lit_review/` runs (even with 0 tests)
- [ ] `mypy lit_review/` passes

---

## E2: Domain Layer Implementation

**Goal:** Implement core business entities and value objects with full test coverage.

### Tasks

| ID | Task | Test First | Estimate |
|----|------|------------|----------|
| E2.1 | Implement `domain/exceptions.py` | No | Small |
| E2.2 | Implement `domain/values/doi.py` with validation | Yes | Small |
| E2.3 | Implement `domain/values/author.py` | Yes | Small |
| E2.4 | Implement `domain/entities/paper.py` | Yes | Medium |
| E2.5 | Implement `domain/entities/review.py` with workflow | Yes | Medium |
| E2.6 | Implement `domain/services/citation_formatter.py` | Yes | Small |

### Acceptance Criteria

- [ ] All value objects are immutable (frozen=True)
- [ ] DOI validation uses regex pattern
- [ ] Paper equality based on DOI only
- [ ] Review enforces workflow stage transitions
- [ ] 100% test coverage for domain layer
- [ ] All tests follow `test_<unit>_<scenario>_<expected>` naming

---

## E3: Application Layer Implementation

**Goal:** Implement use cases and port definitions.

### Tasks

| ID | Task | Dependencies | Estimate |
|----|------|--------------|----------|
| E3.1 | Define `ports/search_service.py` ABC | E2 | Small |
| E3.2 | Define `ports/paper_repository.py` ABC | E2 | Small |
| E3.3 | Implement `usecases/search_papers.py` | E3.1 | Medium |
| E3.4 | Implement `usecases/export_review.py` | E3.2 | Medium |
| E3.5 | Implement `usecases/analyze_themes.py` | E3.2 | Medium |
| E3.6 | Implement `usecases/generate_synthesis.py` | E3.5 | Medium |

### Acceptance Criteria

- [ ] All ports are abstract base classes
- [ ] Use cases depend only on ports (not implementations)
- [ ] SearchPapersUseCase supports parallel database search
- [ ] Deduplication by DOI works correctly
- [ ] > 80% test coverage with mocked ports

---

## E4: Infrastructure Layer Implementation

**Goal:** Implement external service adapters and persistence.

### Tasks

| ID | Task | Dependencies | Estimate |
|----|------|--------------|----------|
| E4.1 | Implement `adapters/crossref_adapter.py` | E3.1 | Medium |
| E4.2 | Implement `persistence/json_repository.py` | E3.2 | Medium |
| E4.3 | Implement `adapters/pubmed_adapter.py` | E3.1 | Medium |
| E4.4 | Implement `ai/claude_analyzer.py` (optional) | E3 | Large |

### Acceptance Criteria

- [ ] CrossrefAdapter implements SearchService port
- [ ] JSONRepository uses atomic writes (temp + rename)
- [ ] Automatic backup before overwrites
- [ ] Exponential backoff for rate limiting
- [ ] Integration tests against real APIs (marked slow)

---

## E5: CLI Interface Implementation

**Goal:** Implement command-line interface using Click.

### Tasks

| ID | Task | Dependencies | Estimate |
|----|------|--------------|----------|
| E5.1 | Create `cli/review_cli.py` with Click group | E4 | Small |
| E5.2 | Implement `review init` command | E4.2 | Small |
| E5.3 | Implement `review search` command | E4.1 | Medium |
| E5.4 | Implement `review assess` command | E4.2 | Small |
| E5.5 | Implement `review status` command | E4.2 | Small |
| E5.6 | Implement `review analyze` command | E3.5 | Small |
| E5.7 | Implement `review synthesize` command | E3.6 | Small |
| E5.8 | Implement `review export` command | E3.4 | Small |
| E5.9 | Add entry point to pyproject.toml | E5.1-E5.8 | Small |

### Acceptance Criteria

- [ ] All commands handle missing review gracefully
- [ ] Progress indicators for long operations
- [ ] Clear error messages for users
- [ ] `academic-review --help` shows all commands
- [ ] Commands can be invoked from project root

---

## E6: Testing & Quality Assurance

**Goal:** Ensure comprehensive test coverage and code quality.

### Tasks

| ID | Task | Dependencies | Estimate |
|----|------|--------------|----------|
| E6.1 | Create test fixtures (sample_papers.json) | E2 | Small |
| E6.2 | Create mock API responses | E4 | Small |
| E6.3 | Write integration tests for workflow | E5 | Medium |
| E6.4 | Run coverage and fix gaps | E6.1-E6.3 | Medium |
| E6.5 | Add performance benchmarks | E4 | Small |
| E6.6 | Security audit (bandit) | E5 | Small |

### Acceptance Criteria

- [ ] Overall coverage > 80%
- [ ] All critical paths at 100%
- [ ] No security issues from bandit
- [ ] Performance tests pass benchmarks
- [ ] CI pipeline passes

---

## E7: Integration & Documentation

**Goal:** Integrate with existing system and document.

### Tasks

| ID | Task | Dependencies | Estimate |
|----|------|--------------|----------|
| E7.1 | Create integration with validate_references.py | E5 | Medium |
| E7.2 | Write user documentation (README section) | E5 | Small |
| E7.3 | Create example workflow in docs/ | E5 | Small |
| E7.4 | Update CLAUDE.md with new package info | E5 | Small |
| E7.5 | Add Makefile targets for review commands | E5 | Small |

### Acceptance Criteria

- [ ] Can import existing paper.md references
- [ ] Can export to paper.md format
- [ ] README documents all commands
- [ ] Example shows complete workflow
- [ ] `make review-init`, `make review-search` etc. work

---

## Implementation Order

```
Phase 1: Foundation
├── E1: Project Setup
└── E2: Domain Layer

Phase 2: Core Logic
├── E3: Application Layer
└── E4: Infrastructure Layer

Phase 3: User Interface
└── E5: CLI Interface

Phase 4: Quality & Integration
├── E6: Testing & QA
└── E7: Integration & Docs
```

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Crossref API changes | Low | High | Pin API version, add fallbacks |
| Rate limiting issues | Medium | Medium | Implement backoff, cache results |
| Complex workflow logic | Medium | High | TDD approach, comprehensive tests |
| Dependency conflicts | Low | Medium | Use virtual environment, pin versions |

## Definition of Done

Epic is complete when:
1. All tasks completed
2. All acceptance criteria met
3. Tests passing with > 80% coverage
4. Code reviewed (if applicable)
5. Documentation updated
6. No blocking issues
