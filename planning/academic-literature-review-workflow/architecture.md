# Architecture: Academic Literature Review Workflow

**Issue:** #253
**Created:** 2025-12-01
**Status:** Draft

## Overview

This document describes the technical architecture for the Academic Literature Review Workflow system, following Clean Architecture principles with domain-driven design.

## Architecture Principles

### Clean Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                      Interfaces (CLI)                       │
│                 Entry points for user interaction           │
├─────────────────────────────────────────────────────────────┤
│                    Infrastructure                            │
│         External adapters: APIs, Persistence, AI            │
├─────────────────────────────────────────────────────────────┤
│                      Application                             │
│             Use cases and port definitions                   │
├─────────────────────────────────────────────────────────────┤
│                        Domain                                │
│           Entities, Value Objects, Domain Services          │
└─────────────────────────────────────────────────────────────┘
```

### Dependency Rule

Dependencies point inward only:
- Domain has no external dependencies
- Application depends only on Domain
- Infrastructure depends on Application and Domain
- Interfaces depends on all layers

## Directory Structure

```
lit_review/                    # New package for literature review
├── __init__.py
├── domain/                    # Core business logic (no dependencies)
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── paper.py          # Paper entity
│   │   ├── review.py         # Review entity (workflow stages)
│   │   └── citation.py       # Citation entity
│   ├── values/
│   │   ├── __init__.py
│   │   ├── doi.py            # DOI value object
│   │   ├── author.py         # Author value object
│   │   └── keywords.py       # Keywords value object
│   ├── services/
│   │   ├── __init__.py
│   │   ├── bibtex_parser.py  # BibTeX parsing
│   │   └── citation_formatter.py
│   └── exceptions.py          # Domain exceptions
│
├── application/               # Use cases & ports
│   ├── __init__.py
│   ├── usecases/
│   │   ├── __init__.py
│   │   ├── search_papers.py   # Search across databases
│   │   ├── analyze_themes.py  # Thematic analysis
│   │   ├── generate_synthesis.py
│   │   └── export_review.py   # Export to various formats
│   └── ports/
│       ├── __init__.py
│       ├── paper_repository.py  # ABC for persistence
│       ├── search_service.py    # ABC for search adapters
│       └── ai_analyzer.py       # ABC for AI analysis
│
├── infrastructure/            # External implementations
│   ├── __init__.py
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── crossref_adapter.py
│   │   ├── pubmed_adapter.py
│   │   ├── arxiv_adapter.py
│   │   └── semantic_scholar_adapter.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── json_repository.py  # JSON file persistence
│   └── ai/
│       ├── __init__.py
│       └── claude_analyzer.py  # Claude API integration
│
└── interfaces/                # Entry points
    ├── __init__.py
    └── cli/
        ├── __init__.py
        └── review_cli.py      # Click CLI commands

tests/
├── lit_review/                # Tests mirror source structure
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── test_paper.py
│   │   │   └── test_review.py
│   │   └── values/
│   │       ├── test_doi.py
│   │       └── test_author.py
│   ├── application/
│   │   └── usecases/
│   │       ├── test_search_papers.py
│   │       └── test_export_review.py
│   └── integration/
│       └── test_crossref_integration.py
└── fixtures/
    ├── sample_papers.json
    └── mock_responses/
```

## Domain Layer

### Entities

#### Paper Entity

```python
@dataclass
class Paper:
    doi: DOI                    # Value object
    title: str
    authors: List[Author]       # Value objects
    publication_year: int
    journal: str
    abstract: str = ""
    keywords: List[str] = field(default_factory=list)
    quality_score: Optional[float] = None

    # Business logic methods
    def set_quality_score(score: float) -> None
    def get_citation_key() -> str
    def is_relevant_to(search_terms: List[str]) -> bool
```

#### Review Entity

```python
@dataclass
class Review:
    title: str
    research_question: str
    inclusion_criteria: List[str]
    exclusion_criteria: List[str]
    papers: Set[Paper]
    stage: ReviewStage  # Enum: PLANNING, SEARCH, SCREENING, ANALYSIS, SYNTHESIS, COMPLETE

    # Workflow enforcement
    def advance_stage() -> None
    def add_paper(paper: Paper) -> None  # Enforces stage rules
    def assess_paper(doi: DOI, score: float, include: bool) -> None
    def get_included_papers() -> List[Paper]
    def generate_statistics() -> Dict[str, Any]
```

### Value Objects

Value objects are immutable and validate on creation:

```python
@dataclass(frozen=True)
class DOI:
    value: str

    def __post_init__(self):
        if not re.match(r'^10\.\d{4,}/[-._;()/:\w]+$', self.value):
            raise ValidationError(f"Invalid DOI: {self.value}")

@dataclass(frozen=True)
class Author:
    last_name: str
    first_name: str
    initials: str
    orcid: Optional[str] = None
```

## Application Layer

### Use Cases

Use cases orchestrate domain entities and call ports:

```python
@dataclass
class SearchPapersUseCase:
    crossref: Optional[SearchService]
    pubmed: Optional[SearchService]

    def execute(query: str, database: str = None, limit: int = 100) -> List[Paper]:
        # Search databases
        # Deduplicate by DOI
        # Return papers
```

### Ports (Interfaces)

Ports define contracts for external dependencies:

```python
class SearchService(ABC):
    @abstractmethod
    def search(query: str, limit: int = 100) -> List[Paper]:
        pass

class PaperRepository(ABC):
    @abstractmethod
    def save(review: Review) -> None:
        pass

    @abstractmethod
    def load(review_id: str) -> Review:
        pass
```

## Infrastructure Layer

### Adapters

Adapters implement ports with external services:

```python
class CrossrefAdapter(SearchService):
    BASE_URL = "https://api.crossref.org/works"

    def search(query: str, limit: int = 100) -> List[Paper]:
        # Call Crossref API
        # Parse response
        # Return Paper entities
```

### Persistence

JSON file-based persistence:

```python
class JSONReviewRepository(PaperRepository):
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)

    def save(review: Review) -> None:
        # Atomic write: temp file + rename
        # Automatic backup before overwrite

    def load(review_id: str) -> Review:
        # Load and deserialize
```

## Data Flow

### Search Flow

```
User Request → CLI → SearchPapersUseCase → SearchService (port)
                                                ↓
                                        CrossrefAdapter (implementation)
                                                ↓
                                        Crossref API (external)
                                                ↓
                                        Parse to Paper entities
                                                ↓
                                        Deduplicate by DOI
                                                ↓
                                        Add to Review
                                                ↓
                                        Persist via JSONRepository
```

### Export Flow

```
User Request → CLI → ExportReviewUseCase → Review Entity
                                                ↓
                                        Get included papers
                                                ↓
                                        Format to BibTeX/JSON/etc
                                                ↓
                                        Write to file
```

## Integration with Existing System

### Relationship to validate_references.py

The new system complements existing functionality:

| validate_references.py | lit_review package |
|------------------------|-------------------|
| Validates existing paper.md | Creates new reviews |
| Parses [A1], [I1] citations | Uses DOI-based entities |
| Checks URL accessibility | Searches academic databases |
| Generates validation reports | Generates synthesis documents |

### Integration Points

1. **Import from paper.md**: Parse existing references into Review
2. **Export to paper.md format**: Generate [A*], [I*] citations
3. **Shared DOI validation**: Use same regex patterns

## Technology Stack

### Core Dependencies

```toml
[project.dependencies]
click = ">=8.0.0"        # CLI framework
requests = ">=2.28.0"    # HTTP client
pydantic = ">=2.0.0"     # Data validation
python-dotenv = ">=0.19.0"  # Environment management

[project.optional-dependencies]
ai = [
    "anthropic>=0.18.0",  # Claude API
]
export = [
    "python-docx>=0.8.11",  # Word export
    "bibtexparser>=1.4.0",  # BibTeX parsing
]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.0.0",
]
```

## Error Handling

### Domain Exceptions

```python
class ValidationError(Exception):
    """Invalid domain data"""

class WorkflowError(Exception):
    """Invalid workflow transition"""
```

### Error Handling Strategy

| Layer | Strategy |
|-------|----------|
| Domain | Raise domain exceptions immediately |
| Application | Catch, log, wrap in application exceptions |
| Infrastructure | Retry with backoff, partial results on failure |
| Interface | User-friendly messages, exit codes |

## Security Considerations

1. **API Keys**: Read from environment variables only
2. **Logging**: Never log API keys or sensitive data
3. **Input Validation**: Sanitize all user inputs
4. **File Permissions**: 600 for configuration files
