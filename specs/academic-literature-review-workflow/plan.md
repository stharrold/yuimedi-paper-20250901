# Implementation Plan: Academic Literature Review Workflow

**Type:** feature
**Slug:** academic-literature-review-workflow
**Date:** 2025-12-02
**GitHub Issue:** #253

## Task Breakdown

Based on BMAD Epics from `planning/academic-literature-review-workflow/epics.md`.

---

### Phase 1: Project Setup (Epic E1)

#### Task E1_001: Create Package Structure

**Priority:** P0

**Files:**
- `lit_review/__init__.py`
- `lit_review/domain/__init__.py`
- `lit_review/domain/entities/__init__.py`
- `lit_review/domain/values/__init__.py`
- `lit_review/domain/services/__init__.py`
- `lit_review/application/__init__.py`
- `lit_review/application/usecases/__init__.py`
- `lit_review/application/ports/__init__.py`
- `lit_review/infrastructure/__init__.py`
- `lit_review/infrastructure/adapters/__init__.py`
- `lit_review/infrastructure/persistence/__init__.py`
- `lit_review/interfaces/__init__.py`
- `lit_review/interfaces/cli/__init__.py`

**Description:**
Create the `lit_review/` package with Clean Architecture directory structure.

**Steps:**
1. Create `lit_review/` directory with all subdirectories
2. Add `__init__.py` files to each package
3. Verify package can be imported

**Acceptance Criteria:**
- [ ] Package structure matches architecture.md
- [ ] `python -c "import lit_review"` succeeds

**Verification:**
```bash
python -c "import lit_review; print('OK')"
```

**Dependencies:** None

---

#### Task E1_002: Update pyproject.toml

**Priority:** P0

**Files:**
- `pyproject.toml`

**Description:**
Add new dependencies for lit_review package.

**Steps:**
1. Add click, requests, pydantic, python-dotenv to dependencies
2. Add optional dependencies (ai, export, dev)
3. Add entry point for `academic-review` CLI

**Acceptance Criteria:**
- [ ] `uv sync` installs all dependencies
- [ ] Optional groups install correctly

**Verification:**
```bash
uv sync && uv run python -c "import click, requests, pydantic; print('OK')"
```

**Dependencies:** E1_001

---

#### Task E1_003: Create Test Directory Structure

**Priority:** P0

**Files:**
- `tests/lit_review/__init__.py`
- `tests/lit_review/domain/__init__.py`
- `tests/lit_review/domain/entities/__init__.py`
- `tests/lit_review/domain/values/__init__.py`
- `tests/lit_review/application/__init__.py`
- `tests/lit_review/integration/__init__.py`
- `tests/lit_review/conftest.py`
- `tests/lit_review/fixtures/sample_papers.json`

**Description:**
Create test directory structure mirroring source structure.

**Steps:**
1. Create test directories
2. Add conftest.py with shared fixtures
3. Add sample data fixtures

**Acceptance Criteria:**
- [ ] `uv run pytest tests/lit_review/ --collect-only` succeeds
- [ ] Fixtures load correctly

**Verification:**
```bash
uv run pytest tests/lit_review/ --collect-only
```

**Dependencies:** E1_001

---

### Phase 2: Domain Layer (Epic E2)

#### Task E2_001: Implement Domain Exceptions

**Priority:** P0

**Files:**
- `lit_review/domain/exceptions.py`
- `tests/lit_review/domain/test_exceptions.py`

**Description:**
Implement ValidationError and WorkflowError domain exceptions.

**Steps:**
1. Create exceptions.py with ValidationError, WorkflowError
2. Add docstrings and error message handling
3. Write basic tests

**Acceptance Criteria:**
- [ ] ValidationError accepts message parameter
- [ ] WorkflowError accepts message parameter
- [ ] Tests pass

**Verification:**
```bash
uv run pytest tests/lit_review/domain/test_exceptions.py -v
```

**Dependencies:** E1_001

---

#### Task E2_002: Implement DOI Value Object

**Priority:** P0

**Files:**
- `lit_review/domain/values/doi.py`
- `tests/lit_review/domain/values/test_doi.py`

**Description:**
Implement immutable DOI value object with regex validation.

**Steps:**
1. Create frozen dataclass with validation in __post_init__
2. Use regex `^10\.\d{4,}/[-._;()/:\w]+$`
3. Write TDD tests first

**Acceptance Criteria:**
- [ ] DOI is immutable (frozen=True)
- [ ] Valid DOIs pass validation
- [ ] Invalid DOIs raise ValidationError
- [ ] 100% test coverage

**Verification:**
```bash
uv run pytest tests/lit_review/domain/values/test_doi.py -v --cov=lit_review.domain.values.doi
```

**Dependencies:** E2_001

---

#### Task E2_003: Implement Author Value Object

**Priority:** P0

**Files:**
- `lit_review/domain/values/author.py`
- `tests/lit_review/domain/values/test_author.py`

**Description:**
Implement immutable Author value object.

**Steps:**
1. Create frozen dataclass with last_name, first_name, initials, orcid
2. Add validation for required fields
3. Write TDD tests first

**Acceptance Criteria:**
- [ ] Author is immutable
- [ ] Required fields validated
- [ ] ORCID optional
- [ ] 100% test coverage

**Verification:**
```bash
uv run pytest tests/lit_review/domain/values/test_author.py -v
```

**Dependencies:** E2_001

---

#### Task E2_004: Implement Paper Entity

**Priority:** P0

**Files:**
- `lit_review/domain/entities/paper.py`
- `tests/lit_review/domain/entities/test_paper.py`

**Description:**
Implement Paper entity with business logic methods.

**Steps:**
1. Create dataclass with DOI, title, authors, year, journal, abstract, keywords, quality_score
2. Implement get_citation_key() method
3. Implement set_quality_score() with validation (0-10)
4. Paper equality based on DOI only
5. Write TDD tests first

**Acceptance Criteria:**
- [ ] Paper stores all required fields
- [ ] Citation key format: AuthorYear or AuthorEtAlYear
- [ ] Quality score validates 0-10 range
- [ ] Equality based on DOI
- [ ] 100% test coverage

**Verification:**
```bash
uv run pytest tests/lit_review/domain/entities/test_paper.py -v
```

**Dependencies:** E2_002, E2_003

---

#### Task E2_005: Implement Review Entity

**Priority:** P0

**Files:**
- `lit_review/domain/entities/review.py`
- `tests/lit_review/domain/entities/test_review.py`

**Description:**
Implement Review entity with workflow stage enforcement.

**Steps:**
1. Create ReviewStage enum (PLANNING, SEARCH, SCREENING, ANALYSIS, SYNTHESIS, COMPLETE)
2. Create Review dataclass with title, research_question, criteria, papers, stage
3. Implement advance_stage() with transition validation
4. Implement add_paper() with stage rules (cannot add during PLANNING)
5. Implement generate_statistics()
6. Write TDD tests first

**Acceptance Criteria:**
- [ ] Workflow stages enforced
- [ ] Cannot skip stages
- [ ] Cannot add papers during PLANNING
- [ ] Statistics calculated correctly
- [ ] 100% test coverage

**Verification:**
```bash
uv run pytest tests/lit_review/domain/entities/test_review.py -v
```

**Dependencies:** E2_004

---

#### Task E2_006: Implement Citation Formatter Service

**Priority:** P1

**Files:**
- `lit_review/domain/services/citation_formatter.py`
- `tests/lit_review/domain/services/test_citation_formatter.py`

**Description:**
Implement citation formatting service.

**Steps:**
1. Create CitationFormatter class
2. Implement format_bibtex() method
3. Implement format_apa() method
4. Write TDD tests first

**Acceptance Criteria:**
- [ ] BibTeX format correct
- [ ] APA format correct
- [ ] 100% test coverage

**Verification:**
```bash
uv run pytest tests/lit_review/domain/services/test_citation_formatter.py -v
```

**Dependencies:** E2_004

---

### Phase 3: Application Layer (Epic E3)

#### Task E3_001: Define Search Service Port

**Priority:** P0

**Files:**
- `lit_review/application/ports/search_service.py`

**Description:**
Define abstract SearchService port interface.

**Steps:**
1. Create ABC with search() abstract method
2. Define method signature: search(query: str, limit: int) -> list[Paper]

**Acceptance Criteria:**
- [ ] ABC properly defined
- [ ] Type hints complete

**Verification:**
```bash
uv run python -c "from lit_review.application.ports.search_service import SearchService; print('OK')"
```

**Dependencies:** E2_004

---

#### Task E3_002: Define Paper Repository Port

**Priority:** P0

**Files:**
- `lit_review/application/ports/paper_repository.py`

**Description:**
Define abstract PaperRepository port interface.

**Steps:**
1. Create ABC with save(), load(), delete() abstract methods
2. Define method signatures with proper types

**Acceptance Criteria:**
- [ ] ABC properly defined
- [ ] Type hints complete

**Verification:**
```bash
uv run python -c "from lit_review.application.ports.paper_repository import PaperRepository; print('OK')"
```

**Dependencies:** E2_005

---

#### Task E3_003: Implement SearchPapers Use Case

**Priority:** P0

**Files:**
- `lit_review/application/usecases/search_papers.py`
- `tests/lit_review/application/usecases/test_search_papers.py`

**Description:**
Implement search papers use case with deduplication.

**Steps:**
1. Create SearchPapersUseCase dataclass
2. Accept SearchService ports for each database
3. Implement execute() with parallel search capability
4. Deduplicate results by DOI
5. Write tests with mocked ports

**Acceptance Criteria:**
- [ ] Depends only on ports (not implementations)
- [ ] Deduplication by DOI works
- [ ] Handles missing adapters gracefully
- [ ] > 80% test coverage

**Verification:**
```bash
uv run pytest tests/lit_review/application/usecases/test_search_papers.py -v
```

**Dependencies:** E3_001

---

#### Task E3_004: Implement ExportReview Use Case

**Priority:** P0

**Files:**
- `lit_review/application/usecases/export_review.py`
- `tests/lit_review/application/usecases/test_export_review.py`

**Description:**
Implement export review use case for multiple formats.

**Steps:**
1. Create ExportReviewUseCase dataclass
2. Implement execute() with format parameter
3. Support BibTeX, JSON formats
4. Write tests with mocked repository

**Acceptance Criteria:**
- [ ] BibTeX export correct
- [ ] JSON export correct
- [ ] > 80% test coverage

**Verification:**
```bash
uv run pytest tests/lit_review/application/usecases/test_export_review.py -v
```

**Dependencies:** E3_002, E2_006

---

### Phase 4: Infrastructure Layer (Epic E4)

#### Task E4_001: Implement Crossref Adapter

**Priority:** P0

**Files:**
- `lit_review/infrastructure/adapters/crossref_adapter.py`
- `tests/lit_review/infrastructure/adapters/test_crossref_adapter.py`
- `tests/lit_review/integration/test_crossref_integration.py`

**Description:**
Implement Crossref API adapter with rate limiting.

**Steps:**
1. Create CrossrefAdapter implementing SearchService
2. Implement search() with requests library
3. Parse Crossref response to Paper entities
4. Add exponential backoff for rate limiting
5. Write unit tests with mocked responses
6. Write integration test (marked slow)

**Acceptance Criteria:**
- [ ] Implements SearchService port
- [ ] Exponential backoff works
- [ ] Response parsing correct
- [ ] Timeout handling (30s)
- [ ] Unit tests with mocks
- [ ] Integration test marked slow

**Verification:**
```bash
uv run pytest tests/lit_review/infrastructure/adapters/test_crossref_adapter.py -v
uv run pytest tests/lit_review/integration/test_crossref_integration.py -v -m slow
```

**Dependencies:** E3_001

---

#### Task E4_002: Implement JSON Repository

**Priority:** P0

**Files:**
- `lit_review/infrastructure/persistence/json_repository.py`
- `tests/lit_review/infrastructure/persistence/test_json_repository.py`

**Description:**
Implement JSON file-based persistence with atomic writes.

**Steps:**
1. Create JSONReviewRepository implementing PaperRepository
2. Implement save() with atomic write (temp + rename)
3. Implement automatic backup before overwrite
4. Implement load() with deserialization
5. Write comprehensive tests

**Acceptance Criteria:**
- [ ] Implements PaperRepository port
- [ ] Atomic writes (temp + rename)
- [ ] Automatic backup
- [ ] Serialization/deserialization correct
- [ ] > 80% test coverage

**Verification:**
```bash
uv run pytest tests/lit_review/infrastructure/persistence/test_json_repository.py -v
```

**Dependencies:** E3_002

---

#### Task E4_003: Implement PubMed Adapter

**Priority:** P1

**Files:**
- `lit_review/infrastructure/adapters/pubmed_adapter.py`
- `tests/lit_review/infrastructure/adapters/test_pubmed_adapter.py`

**Description:**
Implement PubMed API adapter.

**Steps:**
1. Create PubMedAdapter implementing SearchService
2. Implement search() using E-utilities API
3. Parse PubMed response to Paper entities
4. Add rate limiting
5. Write tests

**Acceptance Criteria:**
- [ ] Implements SearchService port
- [ ] Rate limiting works
- [ ] Response parsing correct

**Verification:**
```bash
uv run pytest tests/lit_review/infrastructure/adapters/test_pubmed_adapter.py -v
```

**Dependencies:** E3_001

---

### Phase 5: CLI Interface (Epic E5)

#### Task E5_001: Create CLI Group

**Priority:** P0

**Files:**
- `lit_review/interfaces/cli/review_cli.py`

**Description:**
Create Click CLI group for review commands.

**Steps:**
1. Create review_cli.py with @click.group()
2. Add --help documentation
3. Configure entry point in pyproject.toml

**Acceptance Criteria:**
- [ ] `academic-review --help` shows commands
- [ ] Click group properly configured

**Verification:**
```bash
uv run academic-review --help
```

**Dependencies:** E1_002

---

#### Task E5_002: Implement Init Command

**Priority:** P0

**Files:**
- `lit_review/interfaces/cli/review_cli.py`
- `tests/lit_review/interfaces/cli/test_review_cli.py`

**Description:**
Implement `review init` command.

**Steps:**
1. Add init command with title argument
2. Add --question option for research question
3. Create Review and persist
4. Write CLI tests

**Acceptance Criteria:**
- [ ] Creates new review
- [ ] Persists to JSON
- [ ] Clear output messages

**Verification:**
```bash
uv run academic-review init "Test Review" -q "What is the impact?"
```

**Dependencies:** E5_001, E4_002

---

#### Task E5_003: Implement Search Command

**Priority:** P0

**Files:**
- `lit_review/interfaces/cli/review_cli.py`

**Description:**
Implement `review search` command.

**Steps:**
1. Add search command with --database, --keywords, --limit options
2. Call SearchPapersUseCase
3. Display results summary
4. Add progress indicator

**Acceptance Criteria:**
- [ ] Search works with Crossref
- [ ] Results displayed correctly
- [ ] Progress indicator shown

**Verification:**
```bash
uv run academic-review search -d crossref -k "machine learning healthcare" -l 10
```

**Dependencies:** E5_002, E4_001

---

#### Task E5_004: Implement Status Command

**Priority:** P0

**Files:**
- `lit_review/interfaces/cli/review_cli.py`

**Description:**
Implement `review status` command.

**Steps:**
1. Add status command
2. Display current stage, paper counts, statistics
3. Handle missing review gracefully

**Acceptance Criteria:**
- [ ] Shows current workflow stage
- [ ] Shows paper statistics
- [ ] Handles missing review

**Verification:**
```bash
uv run academic-review status
```

**Dependencies:** E5_002

---

#### Task E5_005: Implement Export Command

**Priority:** P0

**Files:**
- `lit_review/interfaces/cli/review_cli.py`

**Description:**
Implement `review export` command.

**Steps:**
1. Add export command with --format, --output options
2. Call ExportReviewUseCase
3. Write to file
4. Display success message

**Acceptance Criteria:**
- [ ] BibTeX export works
- [ ] JSON export works
- [ ] Output file created

**Verification:**
```bash
uv run academic-review export -f bibtex -o references.bib
```

**Dependencies:** E5_002, E3_004

---

### Phase 6: Testing & QA (Epic E6)

#### Task E6_001: Create Test Fixtures

**Priority:** P0

**Files:**
- `tests/lit_review/fixtures/sample_papers.json`
- `tests/lit_review/fixtures/mock_crossref_response.json`
- `tests/lit_review/conftest.py`

**Description:**
Create comprehensive test fixtures.

**Steps:**
1. Create sample papers JSON with 10 papers
2. Create mock Crossref API response
3. Add pytest fixtures in conftest.py

**Acceptance Criteria:**
- [ ] Fixtures load correctly
- [ ] Cover various edge cases

**Verification:**
```bash
uv run pytest tests/lit_review/ --collect-only
```

**Dependencies:** E2_004

---

#### Task E6_002: Coverage Analysis

**Priority:** P0

**Files:**
- `pytest.ini` or `pyproject.toml`

**Description:**
Run coverage analysis and fix gaps.

**Steps:**
1. Run pytest with coverage
2. Identify gaps < 80%
3. Add missing tests
4. Verify coverage targets met

**Acceptance Criteria:**
- [ ] Overall coverage ≥ 80%
- [ ] Domain layer 100%
- [ ] No critical paths uncovered

**Verification:**
```bash
uv run pytest tests/lit_review/ --cov=lit_review --cov-report=term --cov-fail-under=80
```

**Dependencies:** All implementation tasks

---

#### Task E6_003: Security Audit

**Priority:** P0

**Files:**
- N/A (audit only)

**Description:**
Run security audit with bandit.

**Steps:**
1. Install bandit
2. Run bandit on lit_review/
3. Fix any findings

**Acceptance Criteria:**
- [ ] No high severity issues
- [ ] No medium severity issues

**Verification:**
```bash
uv run bandit -r lit_review/ -ll
```

**Dependencies:** All implementation tasks

---

### Phase 7: Integration & Docs (Epic E7)

#### Task E7_001: Integration with validate_references.py

**Priority:** P1

**Files:**
- `lit_review/interfaces/import_export.py`
- `tests/lit_review/interfaces/test_import_export.py`

**Description:**
Create integration with existing validate_references.py.

**Steps:**
1. Create import function for paper.md references
2. Create export function to paper.md format
3. Write integration tests

**Acceptance Criteria:**
- [ ] Can import existing [A1], [I1] citations
- [ ] Can export to paper.md format

**Verification:**
```bash
uv run pytest tests/lit_review/interfaces/test_import_export.py -v
```

**Dependencies:** E5_005

---

#### Task E7_002: Update CLAUDE.md

**Priority:** P1

**Files:**
- `CLAUDE.md`
- `lit_review/CLAUDE.md`

**Description:**
Update documentation with new package info.

**Steps:**
1. Add lit_review to CLAUDE.md
2. Create lit_review/CLAUDE.md
3. Document CLI commands

**Acceptance Criteria:**
- [ ] CLAUDE.md updated
- [ ] CLI documented

**Verification:**
Manual review

**Dependencies:** E5_005

---

## Task Dependencies Graph

```
E1_001 ─┬─> E1_002 ─> E5_001 ─┬─> E5_002 ─┬─> E5_003
        │                      │           ├─> E5_004
        └─> E1_003             │           └─> E5_005
                               │
E2_001 ─┬─> E2_002 ─┐         │
        │           ├─> E2_004 ─> E2_005 ─┐
        └─> E2_003 ─┘                      │
                                           ├─> E3_001 ─> E3_003 ─> E4_001
E2_006 <─ E2_004                           │
                                           └─> E3_002 ─> E3_004 ─> E4_002
```

## Critical Path

1. E1_001 → E1_002 → E2_001 → E2_002 → E2_004 → E2_005 → E3_002 → E4_002 → E5_002 → E5_003

## Quality Checklist

Before considering this feature complete:

- [ ] All tasks marked as complete
- [ ] Test coverage ≥ 80%
- [ ] All tests passing (unit + integration)
- [ ] Linting clean (`uv run ruff check lit_review/ tests/`)
- [ ] Type checking clean (`uv run mypy lit_review/`)
- [ ] Security audit clean (`uv run bandit -r lit_review/`)
- [ ] CLI commands documented
- [ ] Code reviewed

## Risk Assessment

### High Risk Tasks

- **E4_001 (Crossref Adapter)**: External API may change or rate limit
  - Mitigation: Cache responses, mock for tests, exponential backoff

- **E2_005 (Review Entity)**: Complex workflow state machine
  - Mitigation: TDD, comprehensive state transition tests

### Medium Risk Tasks

- **E3_003 (SearchPapers)**: Deduplication logic complexity
  - Mitigation: Clear DOI-based equality, comprehensive tests

## Notes

### Implementation Tips

- Follow TDD: write tests first for domain layer
- Use frozen dataclasses for value objects
- Keep domain layer pure (no external dependencies)
- Use dependency injection for adapters

### Common Pitfalls

- Don't add external dependencies to domain layer
- Don't skip workflow stages
- Remember to handle API rate limiting

### Resources

- [Crossref API Docs](https://api.crossref.org)
- [Click Documentation](https://click.palletsprojects.com/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
