# Epic Breakdown: Academic Literature Review Tool for Rigorous Claim Verification

**Date:** 2025-12-09
**Author:** stharrold
**Status:** Draft

## Overview

This document breaks down the Academic Literature Review Tool feature into 7 implementable epics following the TDD approach with clear scope, dependencies, and priorities.

**References:**
- [Requirements](requirements.md) - Business requirements and acceptance criteria
- [Architecture](architecture.md) - Technical design and technology stack
- [GitHub Issue #258](https://github.com/stharrold/yuimedi-paper-20250901/issues/258) - Feature tracking

## Epic Summary

| Epic ID | Name | Complexity | Priority | Dependencies | Estimated Effort |
|---------|------|------------|----------|--------------|------------------|
| E-001 | Project Setup & Configuration | Low | P0 | None | 1-2 days |
| E-002 | Domain Layer (TDD) | Medium | P0 | E-001 | 3-4 days |
| E-003 | Application Layer | High | P0 | E-002 | 4-5 days |
| E-004 | Infrastructure Layer | High | P0 | E-002 | 4-5 days |
| E-005 | CLI Interface | Medium | P0 | E-003, E-004 | 2-3 days |
| E-006 | Testing & Quality Gates | Medium | P0 | E-005 | 2-3 days |
| E-007 | CI/CD & Deployment | Low | P1 | E-006 | 1-2 days |

**Total Estimated Effort:** 17-24 days (3-5 weeks)

## Epic Definitions

### E-001: Project Setup & Configuration

**Description:**
Establish project structure, dependencies, development environment with Docker/Podman, and configuration files following repository standards.

**Scope:**
- Component/module: Project foundation and development environment
- Deliverables:
  - [ ] Directory structure (domain/, application/, infrastructure/, interfaces/, tests/)
  - [ ] pyproject.toml with all dependencies (click, pydantic, scikit-learn, biopython, python-docx)
  - [ ] Containerfile and podman-compose.yml
  - [ ] Git hooks for pre-push testing
  - [ ] Configuration files (.env.example, pytest.ini, .flake8, .mypy.ini)
  - [ ] README and setup documentation

**Complexity:** Low

**Complexity Reasoning:**
Straightforward setup tasks following established patterns in the repository. No business logic or complex algorithms. Main challenges are ensuring all dependencies are compatible and configuration is correct.

**Priority:** P0

**Priority Reasoning:**
Must have - blocks all other work. No development can proceed without proper project structure and dependencies.

**Dependencies:**
- **Requires:** None (starting point)
- **Blocks:** All other epics (E-002 through E-007)

**Acceptance Criteria:**
- [ ] All directories created with __init__.py files
- [ ] pyproject.toml passes `uv sync`
- [ ] Docker builds successfully with `podman build`
- [ ] Container runs with `podman-compose run --rm dev`
- [ ] pytest discovers test structure
- [ ] Pre-push hook executes tests

**Related Requirements:**
- NFR-18: Test coverage ≥80% infrastructure
- NFR-22: All dependencies managed via uv
- Technology Constraints: Python 3.8+, uv, Podman

**Technical Components:**
- Files to create:
  - `pyproject.toml`, `Containerfile`, `podman-compose.yml`
  - `pytest.ini`, `.env.example`
  - `.git/hooks/pre-push`
  - Directory tree: domain/, application/, infrastructure/, interfaces/, tests/
- Tests required: Integration test for Docker build

**Estimated Effort:** 1-2 days

**Risks:**
| Risk | Mitigation |
|------|------------|
| Dependency conflicts | Pin versions in pyproject.toml, test in fresh container |
| Docker build issues | Use proven base image, test locally before CI |

---

### E-002: Domain Layer (TDD)

**Description:**
Implement core business entities (Paper, Review, Citation) and value objects (DOI, Author, Keywords) using Test-Driven Development with comprehensive validation.

**Scope:**
- Component/module: Domain layer (pure business logic, no external dependencies)
- Deliverables:
  - [ ] Value objects: DOI, Author, Keywords with validation
  - [ ] Entity: Paper with metadata, quality scoring, citation keys
  - [ ] Entity: Review with workflow stages, paper management, assessments
  - [ ] Domain services: BibtexParser, CitationFormatter
  - [ ] Domain exceptions: ValidationError, WorkflowError
  - [ ] Unit tests for all domain components (>90% coverage)

**Complexity:** Medium

**Complexity Reasoning:**
Requires careful design of immutable value objects, entity validation rules, and workflow state management. TDD approach adds discipline but reduces bugs. No external dependencies simplifies testing but business rules must be thorough.

**Priority:** P0

**Priority Reasoning:**
Must have - core foundation for all features. Application and infrastructure layers depend on stable domain entities. TDD ensures quality from the start.

**Dependencies:**
- **Requires:** E-001 (Project Setup)
- **Blocks:** E-003 (Application Layer), E-004 (Infrastructure Layer)

**Acceptance Criteria:**
- [ ] All value objects are immutable dataclasses
- [ ] DOI validates format: `^10\\.\\d{4,}/[-._;()/:\\w]+$`
- [ ] Paper equality based on DOI only
- [ ] Review enforces stage transitions (planning → screening → analysis → synthesis)
- [ ] Quality scores validate 0-10 range
- [ ] Citation keys generated: AuthorYear or AuthorEtAlYear format
- [ ] Test coverage >90% for domain layer
- [ ] All tests pass with pytest

**Related Requirements:**
- FR-002: Deduplication (DOI-based equality)
- FR-003: Quality assessment (0-10 scoring)
- NFR-18: Test coverage ≥80%
- NFR-19: SOLID principles
- NFR-21: Docstrings for all public methods

**Technical Components:**
- Files to create:
  - `domain/exceptions.py`
  - `domain/values/doi.py`, `domain/values/author.py`, `domain/values/keywords.py`
  - `domain/entities/paper.py`, `domain/entities/review.py`, `domain/entities/citation.py`
  - `domain/services/bibtex_parser.py`, `domain/services/citation_formatter.py`
  - Full test suite in `tests/domain/`
- Database changes: None (pure domain logic)
- Tests required: Unit tests for all classes and methods

**Estimated Effort:** 3-4 days

**Risks:**
| Risk | Mitigation |
|------|------------|
| Validation logic too complex | Keep rules simple, document edge cases |
| TDD slows initial progress | Trust the process, better quality long-term |
| Immutability constraints | Use dataclasses with frozen=True |

---

### E-003: Application Layer

**Description:**
Implement use cases (SearchPapers, AnalyzeThemes, GenerateSynthesis, ExportReview) and define ports (interfaces) for external dependencies.

**Scope:**
- Component/module: Application layer (use cases and ports)
- Deliverables:
  - [ ] Ports (interfaces): SearchService, PaperRepository, AIAnalyzer
  - [ ] Use case: SearchPapers with parallel execution and deduplication
  - [ ] Use case: AnalyzeThemes with TF-IDF and clustering
  - [ ] Use case: GenerateSynthesis with narrative generation
  - [ ] Use case: ExportReview with multiple format support
  - [ ] Unit tests with mocked dependencies (>80% coverage)

**Complexity:** High

**Complexity Reasoning:**
Complex orchestration logic for parallel searches, deduplication algorithms, TF-IDF implementation, hierarchical clustering. Requires careful dependency injection design and comprehensive mocking for tests.

**Priority:** P0

**Priority Reasoning:**
Must have - implements core feature logic. Required for CLI to function. Blocks interface layer.

**Dependencies:**
- **Requires:** E-002 (Domain Layer for entities)
- **Blocks:** E-005 (CLI Interface needs use cases)

**Acceptance Criteria:**
- [ ] SearchPapers executes 4+ databases in parallel using ThreadPoolExecutor
- [ ] Deduplication achieves >99% accuracy on test dataset
- [ ] AnalyzeThemes completes in <30s for 500 papers
- [ ] Ports defined as Abstract Base Classes (abc.ABC)
- [ ] All use cases accept dependencies via constructor injection
- [ ] Error handling with exponential backoff for network errors
- [ ] Test coverage >80% with mocked ports

**Related Requirements:**
- FR-001: Multi-database search with parallel execution
- FR-002: Automatic deduplication
- FR-004: Thematic analysis using TF-IDF
- FR-005: AI-powered synthesis
- FR-006: Multiple export formats
- NFR-1: 1000 papers/minute search throughput
- NFR-2: <30s theme analysis for 500 papers
- NFR-6: Exponential backoff for network errors

**Technical Components:**
- Files to create:
  - `application/ports/search_service.py`, `application/ports/paper_repository.py`, `application/ports/ai_analyzer.py`
  - `application/usecases/search_papers.py` (parallel execution, deduplication)
  - `application/usecases/analyze_themes.py` (TF-IDF, clustering)
  - `application/usecases/generate_synthesis.py` (narrative generation)
  - `application/usecases/export_review.py` (BibTeX, DOCX, LaTeX, HTML, JSON)
  - Full test suite in `tests/application/`
- Tests required: Unit tests with mocked ports, integration tests

**Estimated Effort:** 4-5 days

**Risks:**
| Risk | Mitigation |
|------|------------|
| Parallel execution complexity | Use proven ThreadPoolExecutor pattern |
| TF-IDF performance issues | Profile and optimize, use numpy efficiently |
| Mocking all dependencies | Create reusable mock fixtures in conftest.py |

---

### E-004: Infrastructure Layer

**Description:**
Implement database adapters (Crossref, PubMed, ArXiv, Semantic Scholar), persistence (JSONRepository), and AI integration (ClaudeAnalyzer).

**Scope:**
- Component/module: Infrastructure layer (external implementations)
- Deliverables:
  - [ ] CrossrefAdapter implementing SearchService
  - [ ] PubMedAdapter using Biopython
  - [ ] ArxivAdapter (optional)
  - [ ] SemanticScholarAdapter (optional)
  - [ ] JSONRepository with atomic writes and backups
  - [ ] ClaudeAnalyzer with AI-powered theme extraction
  - [ ] Integration tests with live APIs (skippable if keys missing)

**Complexity:** High

**Complexity Reasoning:**
Multiple API integrations with different authentication schemes, rate limits, and response formats. Atomic file operations with backups require careful implementation. AI integration with fallback logic.

**Priority:** P0

**Priority Reasoning:**
Must have - implements actual database searches and persistence. Required for CLI to function with real data.

**Dependencies:**
- **Requires:** E-002 (Domain entities to populate)
- **Blocks:** E-005 (CLI needs working adapters)

**Acceptance Criteria:**
- [ ] CrossrefAdapter searches without API key
- [ ] PubMedAdapter handles API rate limits (3/sec)
- [ ] JSONRepository performs atomic writes with temp file + rename
- [ ] Automatic backups created before overwrites
- [ ] File locking for concurrent access
- [ ] ClaudeAnalyzer has fallback to keyword-based analysis
- [ ] All adapters handle network errors gracefully
- [ ] Integration tests pass with live APIs (or skip gracefully)

**Related Requirements:**
- FR-001: Multi-database search
- FR-005: AI-powered synthesis
- NFR-4: Exponential backoff for network errors
- NFR-5: Atomic file writes with backups
- NFR-6: API keys from environment only
- NFR-10: API keys never logged

**Technical Components:**
- Files to create:
  - `infrastructure/adapters/crossref_adapter.py`
  - `infrastructure/adapters/pubmed_adapter.py`
  - `infrastructure/adapters/arxiv_adapter.py` (optional)
  - `infrastructure/adapters/semantic_scholar_adapter.py` (optional)
  - `infrastructure/persistence/json_repository.py` (atomic writes, backups, file locking)
  - `infrastructure/ai/claude_analyzer.py` (AI with fallback)
  - Integration tests in `tests/integration/`
- Database changes: JSON file structure in review_data/
- Tests required: Integration tests (skippable without keys), unit tests for logic

**Estimated Effort:** 4-5 days

**Risks:**
| Risk | Mitigation |
|------|------------|
| API rate limits break searches | Implement rate limiting, exponential backoff |
| API response format changes | Comprehensive integration tests, version clients |
| Atomic write failures | Test extensively, use proven temp+rename pattern |
| AI API costs | Cache responses, make AI optional with fallback |

---

### E-005: CLI Interface

**Description:**
Implement Click-based CLI commands (init, search, assess, analyze, synthesize, status, export) with progress indicators and error handling.

**Scope:**
- Component/module: Interface layer (CLI entry point)
- Deliverables:
  - [ ] CLI commands: init, search, assess, analyze, synthesize, status, export
  - [ ] Progress indicators for long operations
  - [ ] Clear error messages without stack traces
  - [ ] Help text for all commands
  - [ ] Dependency injection wiring
  - [ ] Entry point in pyproject.toml: `academic-review` command
  - [ ] End-to-end CLI tests

**Complexity:** Medium

**Complexity Reasoning:**
Straightforward Click framework usage but requires careful dependency injection, error handling, and user experience design. Must integrate all use cases and adapters properly.

**Priority:** P0

**Priority Reasoning:**
Must have - user-facing interface for all features. Required to complete full workflow.

**Dependencies:**
- **Requires:** E-003 (Use cases), E-004 (Adapters)
- **Blocks:** E-006 (Testing needs working CLI)

**Acceptance Criteria:**
- [ ] `academic-review init` creates new review with prompts
- [ ] `academic-review search` executes multi-database search with progress
- [ ] `academic-review assess <doi>` displays paper and prompts for scoring
- [ ] `academic-review analyze` runs theme extraction and displays results
- [ ] `academic-review synthesize` generates narrative synthesis
- [ ] `academic-review status` shows review statistics
- [ ] `academic-review export --format <fmt>` generates specified format
- [ ] All commands show clear error messages
- [ ] Help text available for all commands

**Related Requirements:**
- All FR requirements (FR-001 through FR-008)
- NFR-14: Clear error messages without stack traces
- NFR-15: Progress indicators for long operations
- NFR-17: Command-line help text

**Technical Components:**
- Files to create:
  - `interfaces/cli/review_cli.py` (all Click commands)
  - Dependency injection setup in CLI
  - Entry point configuration in pyproject.toml
  - End-to-end tests in `tests/integration/`
- Tests required: Integration tests for full CLI workflow

**Estimated Effort:** 2-3 days

**Risks:**
| Risk | Mitigation |
|------|------------|
| Dependency injection complexity | Use simple constructor injection |
| Poor user experience | Test with real users, iterate on feedback |
| Error handling gaps | Comprehensive exception handling at CLI boundary |

---

### E-006: Testing & Quality Gates

**Description:**
Achieve >80% test coverage, implement comprehensive test suites (unit, integration, performance), and establish quality checks (linting, type checking, security).

**Scope:**
- Component/module: Testing infrastructure and quality assurance
- Deliverables:
  - [ ] Test coverage >80% overall
  - [ ] Unit tests for all business logic
  - [ ] Integration tests for API calls and file I/O
  - [ ] Performance tests (<100ms operations, <30s analysis)
  - [ ] Quality checks: ruff (linting), mypy (type checking)
  - [ ] Security scan with bandit
  - [ ] Pytest configuration and fixtures
  - [ ] Coverage reports (HTML)

**Complexity:** Medium

**Complexity Reasoning:**
Requires comprehensive test coverage across all layers. Performance testing needs benchmarking infrastructure. Quality tools need configuration and integration.

**Priority:** P0

**Priority Reasoning:**
Must have - ensures feature quality and reliability. Academic tool must be trustworthy.

**Dependencies:**
- **Requires:** E-005 (Complete implementation to test)
- **Blocks:** E-007 (CI/CD needs passing tests)

**Acceptance Criteria:**
- [ ] Overall test coverage ≥80% (pytest --cov)
- [ ] All unit tests pass (pytest tests/domain/ tests/application/)
- [ ] All integration tests pass (pytest tests/integration/)
- [ ] Performance tests meet targets (<100ms ops, <30s analysis)
- [ ] Ruff linting passes with no errors
- [ ] Mypy type checking passes with no errors
- [ ] Bandit security scan shows no high-severity issues
- [ ] Test fixtures reusable across test suites

**Related Requirements:**
- NFR-1: 1000 papers/minute throughput
- NFR-2: <30s theme analysis
- NFR-4: <100ms UI operations
- NFR-18: ≥80% test coverage
- NFR-19: SOLID principles
- NFR-20: Cyclomatic complexity <10
- NFR-21: All public methods documented

**Technical Components:**
- Files to create:
  - `tests/conftest.py` (shared fixtures)
  - `pytest.ini` (pytest configuration)
  - Performance test suite in `tests/performance/`
  - Coverage configuration in pyproject.toml
- Tests required: Complete test suite with >80% coverage

**Estimated Effort:** 2-3 days

**Risks:**
| Risk | Mitigation |
|------|------------|
| Coverage gaps in complex logic | Identify gaps early, write tests incrementally |
| Performance test flakiness | Use consistent test data, run multiple iterations |
| Type checking errors | Start with mypy early, fix incrementally |

---

### E-007: CI/CD & Deployment

**Description:**
Setup GitHub Actions for automated testing, Docker Hub publishing, Zenodo integration for DOI assignment, and documentation.

**Scope:**
- Component/module: CI/CD pipeline and deployment automation
- Deliverables:
  - [ ] GitHub Actions workflow for PR testing
  - [ ] GitHub Actions workflow for main releases
  - [ ] Docker Hub integration with automated builds
  - [ ] Zenodo DOI assignment for releases
  - [ ] Complete documentation (README, setup guide, workflow guide)
  - [ ] CITATION.cff for GitHub
  - [ ] .zenodo.json for DOI metadata

**Complexity:** Low

**Complexity Reasoning:**
Standard CI/CD patterns with GitHub Actions. Docker Hub and Zenodo integrations are well-documented. Main work is configuration and documentation.

**Priority:** P1

**Priority Reasoning:**
Should have - important for maintainability and distribution but not blocking core functionality. Can be added after initial implementation.

**Dependencies:**
- **Requires:** E-006 (Passing tests to run in CI)
- **Blocks:** None (final epic)

**Acceptance Criteria:**
- [ ] GitHub Actions runs on all PRs (lint, type check, test)
- [ ] GitHub Actions builds Docker image on main push
- [ ] Docker image pushed to Docker Hub with version tags
- [ ] Zenodo creates DOI for tagged releases
- [ ] README includes quick start, installation, usage guide
- [ ] Setup documentation covers local and Docker workflows
- [ ] CITATION.cff configured with authors and metadata
- [ ] .zenodo.json configured for DOI assignment

**Related Requirements:**
- NFR-18: Automated testing in CI
- Technology Constraints: GitHub Actions, Docker Hub, Zenodo
- Deployment Strategy: Docker image distribution

**Technical Components:**
- Files to create:
  - `.github/workflows/ci.yml` (PR testing)
  - `.github/workflows/release.yml` (Docker build and push)
  - `CITATION.cff` (citation metadata)
  - `.zenodo.json` (Zenodo configuration)
  - `README.md` (comprehensive documentation)
  - `docs/setup.md`, `docs/workflow.md`
- Tests required: CI workflow validation

**Estimated Effort:** 1-2 days

**Risks:**
| Risk | Mitigation |
|------|------------|
| CI pipeline failures | Test workflows locally with act or similar |
| Docker Hub credentials | Use GitHub secrets, test integration |
| Zenodo integration issues | Follow official documentation, test with sandbox |

---

## Implementation Plan

### Phase 1: Foundation (Week 1)

**Epics:** E-001 (Project Setup)

**Goal:** Establish project structure, dependencies, and development environment

**Deliverables:**
- Complete directory structure
- Working Docker environment
- All dependencies installed and verified

**Success Criteria:**
- [ ] Docker builds successfully
- [ ] pytest discovers test structure
- [ ] Pre-push hook executes

---

### Phase 2: Core Business Logic (Week 1-2)

**Epics:** E-002 (Domain Layer)

**Goal:** Implement core domain entities and value objects using TDD

**Deliverables:**
- Paper, Review, Citation entities
- DOI, Author, Keywords value objects
- Domain services for BibTeX and citations
- >90% test coverage for domain

**Success Criteria:**
- [ ] All domain tests pass
- [ ] Entities enforce business rules
- [ ] Value objects are immutable

---

### Phase 3: Application & Infrastructure (Week 2-3)

**Epics:** E-003 (Application Layer), E-004 (Infrastructure Layer)

**Goal:** Implement use cases and external integrations

**Deliverables:**
- Search, analyze, synthesize, export use cases
- Database adapters for Crossref, PubMed
- JSON persistence with atomic writes
- AI integration with Claude

**Success Criteria:**
- [ ] Multi-database search works in parallel
- [ ] Theme analysis completes in <30s for 500 papers
- [ ] All export formats generate correctly
- [ ] Integration tests pass

---

### Phase 4: User Interface (Week 3-4)

**Epics:** E-005 (CLI Interface)

**Goal:** Create user-facing CLI with all commands

**Deliverables:**
- Complete CLI with 7 commands
- Progress indicators and error handling
- Help text and documentation

**Success Criteria:**
- [ ] Full review workflow completes successfully
- [ ] Error messages are clear and helpful
- [ ] Performance targets met

---

### Phase 5: Quality Assurance (Week 4)

**Epics:** E-006 (Testing & Quality Gates)

**Goal:** Achieve comprehensive test coverage and quality standards

**Deliverables:**
- >80% test coverage
- All quality checks passing
- Performance benchmarks verified

**Success Criteria:**
- [ ] All tests pass
- [ ] Coverage ≥80%
- [ ] No quality tool errors

---

### Phase 6: Deployment (Week 5)

**Epics:** E-007 (CI/CD & Deployment)

**Goal:** Automate testing, building, and deployment

**Deliverables:**
- GitHub Actions workflows
- Docker Hub integration
- Zenodo DOI assignment
- Complete documentation

**Success Criteria:**
- [ ] CI passes on all PRs
- [ ] Docker image builds and publishes
- [ ] Documentation complete

---

## Dependency Graph

```
E-001 (Project Setup)
  ↓
  ├─→ E-002 (Domain Layer)
  │     ↓
  │     ├─→ E-003 (Application Layer) ─┐
  │     │                              │
  │     └─→ E-004 (Infrastructure) ────┤
  │                                     │
  │                                     ↓
  └─────────────────────────────→ E-005 (CLI Interface)
                                        ↓
                                   E-006 (Testing & Quality)
                                        ↓
                                   E-007 (CI/CD & Deployment)
```

**Critical Path:** E-001 → E-002 → E-003 → E-005 → E-006 → E-007

**Parallel Work:** E-003 and E-004 can be developed in parallel after E-002

---

## Timeline

| Week | Epics | Focus |
|------|-------|-------|
| Week 1 | E-001, E-002 | Foundation and domain logic |
| Week 2 | E-002, E-003, E-004 | Complete domain, start use cases and adapters |
| Week 3 | E-003, E-004, E-005 | Complete use cases/adapters, build CLI |
| Week 4 | E-005, E-006 | Complete CLI, comprehensive testing |
| Week 5 | E-006, E-007 | Quality gates, CI/CD setup |

**Milestone Dates:**
- **M1:** Week 1 - Foundation and domain complete
- **M2:** Week 3 - All use cases and adapters working
- **M3:** Week 4 - CLI functional with full workflow
- **M4:** Week 5 - Production-ready with CI/CD

---

## Resource Requirements

### Development
- Python developer: 3-5 weeks full-time
- TDD expertise required
- Clean Architecture experience preferred
- Academic research domain knowledge helpful

### Testing
- Unit testing: Included in development (TDD)
- Integration testing: 2-3 days
- Performance testing: 1 day
- Security review: 1 day

### Infrastructure
- Development: Local Podman containers
- API keys: Crossref (email), PubMed (optional), Anthropic (optional)
- Storage: Minimal (<100MB for typical use)

---

## Open Questions

- [ ] Should we support SQLite in addition to JSON for larger reviews? (Decision: Start with JSON, add SQLite if needed)
- [ ] What is the maximum number of papers to support? (Decision: Target 10,000 papers)
- [ ] Which databases should be prioritized? (Decision: Crossref and PubMed first, ArXiv/Semantic Scholar later)
- [ ] How to handle papers behind paywalls? (Decision: Metadata only, no full-text retrieval)
- [ ] Should AI features be mandatory or optional? (Decision: Optional with fallback to keyword-based analysis)

---

## Success Metrics

**Epic Completion:**
- [ ] All epic acceptance criteria met
- [ ] Test coverage ≥ 80% for each epic
- [ ] No P0 or P1 bugs in epic scope
- [ ] Code review approved

**Feature Completion:**
- [ ] All 7 epics delivered
- [ ] End-to-end literature review workflow completes successfully
- [ ] Performance benchmarks met (1000 papers/min search, <30s analysis)
- [ ] Documentation complete and reviewed
- [ ] Tool validated with actual research paper claims

---

## Notes

- **TDD Approach:** Write tests first for all business logic. This is non-negotiable for academic tool quality.
- **Clean Architecture:** Maintain strict layer boundaries. Domain has no external dependencies.
- **PRISMA Compliance:** Validate all workflow stages against PRISMA 2020 guidelines.
- **Repository Integration:** This extends the existing lit_review/ package, doesn't replace it.
- **Real-World Validation:** Test with actual claims from the YuiQuery paper to ensure usefulness.
