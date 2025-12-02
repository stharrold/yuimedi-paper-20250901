# Specification: Academic Literature Review Workflow

**Type:** feature
**Slug:** academic-literature-review-workflow
**Date:** 2025-12-02
**Author:** stharrold
**GitHub Issue:** #253

## Overview

This feature adds a comprehensive academic literature review workflow system (`lit_review/` package) to the repository, enabling systematic literature review capabilities. The system follows Clean Architecture principles with domain-driven design, supporting paper entity management, multi-database search (Crossref, PubMed, ArXiv), workflow stage enforcement (PLANNING → SEARCH → SCREENING → ANALYSIS → SYNTHESIS → COMPLETE), thematic analysis, and export to multiple formats (BibTeX, JSON, DOCX). It complements the existing `validate_references.py` functionality.

## Implementation Context

**BMAD Planning:** See `planning/academic-literature-review-workflow/` for complete requirements and architecture.

**Implementation Preferences:**

- **Migration Strategy:** None needed (JSON file-based persistence)
- **Include Performance Tests:** True
- **Include Security Tests:** True
- **Task Granularity:** Small tasks
- **Follow Epic Order:** True
- **Additional Notes:** External packages allowed (click, requests, pydantic). Follow TDD approach with >80% test coverage.

## Detailed Specification

### Architecture Overview

```
lit_review/                    # New package
├── domain/                    # Core business logic (no dependencies)
│   ├── entities/              # Paper, Review, Citation
│   ├── values/                # DOI, Author, Keywords (immutable)
│   ├── services/              # BibTeX parsing, Citation formatting
│   └── exceptions.py
├── application/               # Use cases & ports
│   ├── usecases/              # SearchPapers, AnalyzeThemes, ExportReview
│   └── ports/                 # ABCs: SearchService, PaperRepository
├── infrastructure/            # External implementations
│   ├── adapters/              # Crossref, PubMed, ArXiv, SemanticScholar
│   ├── persistence/           # JSONRepository
│   └── ai/                    # ClaudeAnalyzer (optional)
└── interfaces/                # Entry points
    └── cli/                   # Click CLI: review_cli.py
```

### Component 1: Domain Layer - Value Objects

**Files:** `lit_review/domain/values/doi.py`, `author.py`

```python
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class DOI:
    """Immutable DOI value object with validation."""
    value: str

    def __post_init__(self):
        if not re.match(r'^10\.\d{4,}/[-._;()/:\w]+$', self.value):
            raise ValidationError(f"Invalid DOI: {self.value}")

@dataclass(frozen=True)
class Author:
    """Immutable author value object."""
    last_name: str
    first_name: str
    initials: str
    orcid: str | None = None
```

### Component 2: Domain Layer - Entities

**Files:** `lit_review/domain/entities/paper.py`, `review.py`

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class ReviewStage(Enum):
    PLANNING = "planning"
    SEARCH = "search"
    SCREENING = "screening"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    COMPLETE = "complete"

@dataclass
class Paper:
    """Paper entity with business logic."""
    doi: DOI
    title: str
    authors: list[Author]
    publication_year: int
    journal: str
    abstract: str = ""
    keywords: list[str] = field(default_factory=list)
    quality_score: float | None = None

    def get_citation_key(self) -> str:
        """Generate citation key: AuthorYear or AuthorEtAlYear."""
        first_author = self.authors[0].last_name if self.authors else "Unknown"
        suffix = "EtAl" if len(self.authors) > 2 else ""
        return f"{first_author}{suffix}{self.publication_year}"

@dataclass
class Review:
    """Review entity with workflow stage enforcement."""
    title: str
    research_question: str
    inclusion_criteria: list[str]
    exclusion_criteria: list[str]
    papers: set[Paper] = field(default_factory=set)
    stage: ReviewStage = ReviewStage.PLANNING

    def advance_stage(self) -> None:
        """Advance to next workflow stage."""
        stages = list(ReviewStage)
        current_idx = stages.index(self.stage)
        if current_idx < len(stages) - 1:
            self.stage = stages[current_idx + 1]
        else:
            raise WorkflowError("Already at final stage")

    def add_paper(self, paper: Paper) -> None:
        """Add paper (enforces stage rules)."""
        if self.stage == ReviewStage.PLANNING:
            raise WorkflowError("Cannot add papers during PLANNING stage")
        self.papers.add(paper)
```

### Component 3: Application Layer - Ports

**Files:** `lit_review/application/ports/search_service.py`, `paper_repository.py`

```python
from abc import ABC, abstractmethod

class SearchService(ABC):
    """Abstract search service port."""
    @abstractmethod
    def search(self, query: str, limit: int = 100) -> list[Paper]:
        pass

class PaperRepository(ABC):
    """Abstract repository port."""
    @abstractmethod
    def save(self, review: Review) -> None:
        pass

    @abstractmethod
    def load(self, review_id: str) -> Review:
        pass
```

### Component 4: Application Layer - Use Cases

**Files:** `lit_review/application/usecases/search_papers.py`, `export_review.py`

```python
@dataclass
class SearchPapersUseCase:
    """Search papers across multiple databases."""
    crossref: SearchService | None = None
    pubmed: SearchService | None = None

    def execute(self, query: str, databases: list[str] = None, limit: int = 100) -> list[Paper]:
        """Execute search with deduplication by DOI."""
        results = {}
        # Search each database, deduplicate by DOI
        for paper in self._search_databases(query, databases, limit):
            if paper.doi.value not in results:
                results[paper.doi.value] = paper
        return list(results.values())
```

### Component 5: Infrastructure Layer - Crossref Adapter

**File:** `lit_review/infrastructure/adapters/crossref_adapter.py`

```python
import requests
from time import sleep

class CrossrefAdapter(SearchService):
    """Crossref API adapter with rate limiting."""
    BASE_URL = "https://api.crossref.org/works"

    def search(self, query: str, limit: int = 100) -> list[Paper]:
        """Search Crossref with exponential backoff."""
        params = {"query": query, "rows": limit}
        for attempt in range(3):
            try:
                response = requests.get(self.BASE_URL, params=params, timeout=30)
                response.raise_for_status()
                return self._parse_response(response.json())
            except requests.RequestException:
                sleep(2 ** attempt)
        return []
```

### Component 6: Infrastructure Layer - JSON Repository

**File:** `lit_review/infrastructure/persistence/json_repository.py`

```python
import json
from pathlib import Path
import tempfile
import shutil

class JSONReviewRepository(PaperRepository):
    """JSON file-based persistence with atomic writes."""

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)

    def save(self, review: Review) -> None:
        """Atomic write: temp file + rename."""
        path = self.data_dir / f"{review.title}.json"
        # Backup existing
        if path.exists():
            shutil.copy(path, path.with_suffix(".json.bak"))
        # Atomic write
        with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=self.data_dir) as f:
            json.dump(self._serialize(review), f)
            temp_path = f.name
        Path(temp_path).rename(path)
```

### Component 7: CLI Interface

**File:** `lit_review/interfaces/cli/review_cli.py`

```python
import click

@click.group()
def review():
    """Academic literature review workflow."""
    pass

@review.command()
@click.argument("title")
@click.option("--question", "-q", required=True, help="Research question")
def init(title: str, question: str):
    """Initialize a new literature review."""
    pass

@review.command()
@click.option("--database", "-d", type=click.Choice(["crossref", "pubmed", "arxiv"]))
@click.option("--keywords", "-k", required=True, help="Search keywords")
@click.option("--limit", "-l", default=100, help="Max results")
def search(database: str, keywords: str, limit: int):
    """Search academic databases."""
    pass

@review.command()
@click.option("--format", "-f", type=click.Choice(["bibtex", "json", "docx"]))
@click.option("--output", "-o", required=True, help="Output file")
def export(format: str, output: str):
    """Export review to specified format."""
    pass
```

## Testing Requirements

### Unit Tests

**File:** `tests/lit_review/domain/values/test_doi.py`

```python
import pytest
from lit_review.domain.values.doi import DOI
from lit_review.domain.exceptions import ValidationError

def test_doi_valid_format_accepts():
    """Valid DOI format is accepted."""
    doi = DOI("10.1234/test-article")
    assert doi.value == "10.1234/test-article"

def test_doi_invalid_format_raises_validation_error():
    """Invalid DOI format raises ValidationError."""
    with pytest.raises(ValidationError):
        DOI("invalid-doi")

def test_doi_immutable():
    """DOI is immutable (frozen dataclass)."""
    doi = DOI("10.1234/test")
    with pytest.raises(AttributeError):
        doi.value = "new"
```

### Integration Tests

**File:** `tests/lit_review/integration/test_crossref_integration.py`

```python
import pytest

@pytest.mark.slow
def test_crossref_search_returns_papers():
    """Crossref search returns valid papers."""
    adapter = CrossrefAdapter()
    results = adapter.search("machine learning healthcare", limit=5)
    assert len(results) > 0
    assert all(isinstance(p, Paper) for p in results)
```

## Quality Gates

- [ ] Test coverage ≥ 80%
- [ ] All tests passing
- [ ] Linting clean (`uv run ruff check lit_review/ tests/`)
- [ ] Type checking clean (`uv run mypy lit_review/`)
- [ ] Security audit clean (`uv run bandit -r lit_review/`)
- [ ] Performance benchmarks passing

## Dependencies

**pyproject.toml additions:**

```toml
[project.dependencies]
click = ">=8.0.0"
requests = ">=2.28.0"
pydantic = ">=2.0.0"
python-dotenv = ">=0.19.0"

[project.optional-dependencies]
ai = ["anthropic>=0.18.0"]
export = ["python-docx>=0.8.11", "bibtexparser>=1.4.0"]
dev = ["pytest>=7.0.0", "pytest-cov>=4.0.0", "mypy>=1.0.0", "bandit>=1.7.0"]

[project.scripts]
academic-review = "lit_review.interfaces.cli.review_cli:review"
```

## Security Considerations

- API keys read from environment variables only (`CROSSREF_EMAIL`, `ANTHROPIC_API_KEY`)
- Never log API keys or sensitive data
- Input validation on all user inputs (DOI regex, author fields)
- File permissions 600 for configuration files

## References

- [BMAD Requirements](../../planning/academic-literature-review-workflow/requirements.md)
- [BMAD Architecture](../../planning/academic-literature-review-workflow/architecture.md)
- [BMAD Epics](../../planning/academic-literature-review-workflow/epics.md)
- [Crossref API](https://api.crossref.org)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
