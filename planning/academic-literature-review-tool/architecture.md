# Architecture: Academic Literature Review Tool

**Date:** 2025-12-09
**Author:** stharrold
**Status:** Draft

## System Overview

### High-Level Architecture

The Academic Literature Review Tool follows Clean Architecture principles with four distinct layers, ensuring separation of concerns and testability.

```
┌──────────────────────────────────────────────────────────────┐
│                    Interface Layer (CLI)                     │
│  • Click commands (init, search, assess, analyze, export)   │
│  • User input/output formatting                             │
│  • Dependency injection configuration                        │
└────────────────────┬─────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────────┐
│                   Application Layer                          │
│  • Use Cases: SearchPapers, AnalyzeThemes, ExportReview     │
│  • Ports (Interfaces): SearchService, PaperRepository       │
│  • Workflow orchestration and coordination                   │
└────────────────────┬─────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────────┐
│                 Infrastructure Layer                         │
│  • Adapters: CrossrefAdapter, PubMedAdapter, etc.           │
│  • Persistence: JSONRepository with atomic writes            │
│  • AI: ClaudeAnalyzer for synthesis generation              │
└────────────────────┬─────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────────┐
│                     Domain Layer                             │
│  • Entities: Paper, Review, Citation                        │
│  • Value Objects: DOI, Author, WorkflowStage                │
│  • Domain Services: BibtexParser, CitationFormatter         │
│  • Business rules and invariants (no external dependencies)  │
└──────────────────────────────────────────────────────────────┘
```

### Architecture Layers

**1. Domain Layer (Innermost - No Dependencies)**
- Pure business logic with domain entities, value objects, and services
- No dependencies on external frameworks, databases, or APIs
- Enforces all business rules and invariants
- 100% unit testable with no mocks required

**2. Application Layer (Use Cases & Ports)**
- Implements application-specific business rules (use cases)
- Defines ports (interfaces) for external dependencies
- Orchestrates domain entities to fulfill use cases
- Technology-agnostic coordination logic

**3. Infrastructure Layer (External Implementations)**
- Implements adapters for external systems (APIs, databases)
- Provides concrete implementations of application ports
- Handles all external communication and I/O
- Contains framework-specific code

**4. Interface Layer (Entry Points)**
- Provides user-facing interfaces (CLI commands)
- Configures dependency injection
- Handles input validation and output formatting
- Entry point for the application

### Components

**1. CLI Interface**
- **Purpose:** Command-line interface for all user interactions
- **Technology:** Click framework with rich progress indicators
- **Commands:** init, search, assess, analyze, synthesize, status, export
- **Interfaces:** Communicates with application layer use cases

**2. Search Orchestrator**
- **Purpose:** Coordinates parallel searches across multiple databases
- **Technology:** Python threading with ThreadPoolExecutor
- **Interfaces:** Uses SearchService port, returns List[Paper]
- **Error Handling:** Graceful degradation with partial results

**3. Database Adapters**
- **Purpose:** Integrate with external academic databases
- **Technology:** httpx for async HTTP, biopython for PubMed
- **Adapters:** CrossrefAdapter, PubMedAdapter, ArxivAdapter, SemanticScholarAdapter
- **Interfaces:** Implement SearchService port

**4. Deduplication Service**
- **Purpose:** Remove duplicate papers by DOI and title similarity
- **Technology:** Levenshtein distance for title matching
- **Interfaces:** Pure domain service, no external dependencies
- **Algorithm:** O(n log n) using DOI hash map + title comparison

**5. Quality Assessment Manager**
- **Purpose:** Track paper quality scores and inclusion decisions
- **Technology:** Pydantic models with validation
- **Interfaces:** PaperRepository port for persistence
- **Features:** Batch CSV import, validation, statistics

**6. Thematic Analysis Engine**
- **Purpose:** Extract themes using TF-IDF and clustering
- **Technology:** scikit-learn (TfidfVectorizer, AgglomerativeClustering)
- **Interfaces:** Operates on domain Paper entities
- **Output:** ThemeHierarchy with main themes and subthemes

**7. AI Synthesis Generator**
- **Purpose:** Generate narrative synthesis using AI
- **Technology:** Claude API for text generation
- **Interfaces:** Implements AIAnalyzer port
- **Fallback:** Keyword-based synthesis if AI unavailable

**8. Export Manager**
- **Purpose:** Export reviews in multiple formats
- **Technology:** python-docx (DOCX), jinja2 (LaTeX), built-in (JSON, BibTeX, HTML)
- **Formats:** BibTeX, DOCX (APA7), LaTeX (Nature/IEEE/generic), HTML, JSON
- **Interfaces:** Operates on Review entity, outputs files

**9. Persistence Layer**
- **Purpose:** Save and load review data with data integrity
- **Technology:** JSON files with atomic writes (temp + rename)
- **Features:** Automatic backups, file locking, soft deletes
- **Interfaces:** Implements PaperRepository port

## Technology Stack

### Core Technologies

- **Language:** Python 3.8+
- **Package Manager:** uv (fast, deterministic dependency resolution)
- **CLI Framework:** Click 8.1+ (with rich progress bars)
- **Data Validation:** Pydantic 2.0+ (automatic validation, serialization)
- **HTTP Client:** httpx 0.24+ (async/await support, HTTP/2)
- **Testing Framework:** pytest 7.4+ with pytest-cov for coverage
- **Type Checking:** mypy 1.5+ (strict mode enabled)
- **Linting:** ruff 0.1+ (fast Python linter and formatter)
- **Containers:** Docker with multi-stage builds

### Domain-Specific Libraries

- **Academic APIs:**
  - biopython 1.80+ (PubMed E-utilities parsing)
  - crossrefapi 1.5+ (Crossref REST API wrapper)

- **Text Analysis:**
  - scikit-learn 1.3+ (TF-IDF, clustering)
  - numpy 1.24+ (numerical operations)

- **Export Generation:**
  - python-docx 0.8+ (Word document generation)
  - jinja2 3.1+ (LaTeX template rendering)
  - bibtexparser 1.4+ (BibTeX parsing and generation)

### Development Tools

- **Version Control:** Git with pre-commit hooks
- **CI/CD:** GitHub Actions
- **Code Quality:**
  - ruff format (code formatting)
  - ruff check (linting)
  - mypy (type checking)
  - pytest --cov (test coverage >80%)
- **Documentation:** Markdown with GitHub Pages

### Technology Justification

**Why Python?**
- Dominant language in academic/scientific computing
- Excellent libraries for text analysis (scikit-learn) and API integration (httpx, biopython)
- Strong typing support with mypy
- Rapid development with clear, readable syntax

**Why Click for CLI?**
- Industry-standard Python CLI framework
- Rich progress indicators and formatting
- Excellent documentation and community support
- Easy testing of CLI commands

**Why Pydantic for validation?**
- Automatic validation with clear error messages
- Native JSON serialization/deserialization
- Type hints integration with mypy
- Performance: Rust-based core in v2

**Why JSON for persistence?**
- Human-readable for debugging and manual edits
- Version-control friendly (Git diff works well)
- No database server required (simplifies deployment)
- Sufficient performance for typical review sizes (<10k papers)
- Easy backup and portability

**Why Clean Architecture?**
- Separates business logic from external dependencies
- Highly testable (domain layer has no external dependencies)
- Flexible: easy to swap implementations (e.g., JSON → SQLite)
- Maintainable: clear separation of concerns

## Data Model

### Domain Entities

**Paper (Core Entity)**
```python
@dataclass(frozen=True)
class Paper:
    doi: Optional[DOI]              # Validated DOI value object
    title: str                      # Required
    authors: List[Author]           # At least one required
    year: int                       # 1900-current year
    journal: Optional[str]
    abstract: Optional[str]
    keywords: List[str]
    quality_score: Optional[int]    # 0-10 scale
    include: Optional[bool]         # Inclusion decision
    assessment_notes: Optional[str]

    def __hash__(self) -> int:
        return hash(self.doi) if self.doi else hash(self.title)

    def __eq__(self, other) -> bool:
        if self.doi and other.doi:
            return self.doi == other.doi
        return self.title.lower() == other.title.lower()
```

**Review (Aggregate Root)**
```python
@dataclass
class Review:
    review_id: str                  # Unique identifier
    title: str                      # Review title
    research_question: str          # Main research question
    papers: Set[Paper]              # Unique papers
    stage: WorkflowStage            # Current workflow stage
    search_queries: Dict[str, str]  # Database → query mapping
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]        # Extensible metadata

    def add_paper(self, paper: Paper, stage: WorkflowStage) -> None:
        """Add paper at specific workflow stage"""
        if self.stage != stage:
            raise WorkflowError(f"Cannot add paper at stage {stage}, review is at {self.stage}")
        self.papers.add(paper)

    def assess_paper(self, doi: DOI, score: int, include: bool, notes: str) -> None:
        """Assess paper quality and inclusion"""
        if not 0 <= score <= 10:
            raise ValidationError("Score must be 0-10")
        # Update paper in set with assessment

    def get_statistics(self) -> Dict[str, int]:
        """Get review statistics"""
        return {
            "total": len(self.papers),
            "assessed": len([p for p in self.papers if p.quality_score is not None]),
            "included": len([p for p in self.papers if p.include is True]),
            "excluded": len([p for p in self.papers if p.include is False]),
        }
```

**Author (Value Object)**
```python
@dataclass(frozen=True)
class Author:
    last_name: str
    first_name: str
    initials: str
    orcid: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.last_name}, {self.initials}"
```

**DOI (Value Object)**
```python
@dataclass(frozen=True)
class DOI:
    value: str

    def __post_init__(self):
        pattern = r'^10\.\d{4,}/[-._;()/:\w]+$'
        if not re.match(pattern, self.value):
            raise ValidationError(f"Invalid DOI format: {self.value}")

    def to_url(self) -> str:
        return f"https://doi.org/{self.value}"
```

**WorkflowStage (Enum)**
```python
class WorkflowStage(str, Enum):
    INITIALIZED = "initialized"    # Review created
    SEARCH = "search"              # Papers found
    SCREENING = "screening"        # Title/abstract screening
    ELIGIBILITY = "eligibility"    # Full-text assessment
    INCLUDED = "included"          # Final included papers
    ANALYSIS = "analysis"          # Thematic analysis
    SYNTHESIS = "synthesis"        # Narrative synthesis
    EXPORTED = "exported"          # Review exported
```

### Entity Relationships

```
Review (1) ────── (0..*) Paper
                        │
                        └─ (1..*) Author

Paper (1) ────── (0..1) Assessment
Paper (0..*) ──── (0..*) Citation ──── (0..*) Paper
                                              (cited paper)

Review (1) ────── (0..1) ThemeHierarchy
                        │
                        └─ (1..*) Theme
                                │
                                └─ (0..*) Theme (subthemes)
```

### Data Flow

**1. Search Workflow**
```
User: academic-review search <query>
  ↓
CLI: parse arguments, create SearchPapersUseCase
  ↓
Use Case: coordinate parallel database searches
  ↓
Adapters: call Crossref, PubMed, ArXiv, Semantic Scholar APIs
  ↓
Domain: create Paper entities, deduplicate by DOI
  ↓
Repository: save Review with papers to JSON
  ↓
CLI: display results summary and statistics
```

**2. Assessment Workflow**
```
User: academic-review assess <doi> --score 8 --include
  ↓
CLI: parse arguments, load Review
  ↓
Domain: validate score (0-10), update Paper assessment
  ↓
Repository: atomic write Review to JSON (with backup)
  ↓
CLI: display updated assessment statistics
```

**3. Analysis Workflow**
```
User: academic-review analyze
  ↓
CLI: load Review, create AnalyzeThemesUseCase
  ↓
Use Case: filter included papers only
  ↓
Domain Service: TF-IDF keyword extraction
  ↓
Domain Service: build co-occurrence matrix
  ↓
Domain Service: hierarchical clustering
  ↓
Domain: create ThemeHierarchy entity
  ↓
Repository: save Review with themes
  ↓
CLI: display theme summary with top keywords
```

**4. Export Workflow**
```
User: academic-review export --format docx
  ↓
CLI: load Review, create ExportReviewUseCase
  ↓
Use Case: format Review for DOCX export
  ↓
Infrastructure: generate DOCX with python-docx (APA7 style)
  ↓
File System: write DOCX to output directory
  ↓
CLI: display export path and success message
```

## API Design

### CLI Commands

#### `academic-review init`

Initialize a new literature review.

**Usage:**
```bash
academic-review init <review-id> --title "Review Title" --question "Research question?"
```

**Arguments:**
- `review-id`: Unique identifier for the review (alphanumeric + hyphens)
- `--title`: Review title (required)
- `--question`: Research question (required)

**Output:**
```
✓ Review initialized: my-review-2025
  Title: Healthcare Analytics Maturity
  Question: What factors influence healthcare analytics maturity?
  Location: ./review_data/reviews/my-review-2025.json
```

#### `academic-review search`

Search academic databases for papers.

**Usage:**
```bash
academic-review search <query> --databases crossref,pubmed --limit 500
```

**Arguments:**
- `query`: Search query string
- `--databases`: Comma-separated list (crossref, pubmed, arxiv, semantic_scholar)
- `--limit`: Max papers per database (default: 100)

**Output:**
```
Searching databases...
  ✓ Crossref: 342 papers found
  ✓ PubMed: 156 papers found
  ✗ ArXiv: Timeout (30s)
  ✓ Semantic Scholar: 98 papers found

Results:
  Total found: 596 papers
  After deduplication: 523 papers (73 duplicates removed)
  Added to review: my-review-2025
```

#### `academic-review assess`

Assess paper quality and make inclusion decisions.

**Usage:**
```bash
# Single assessment
academic-review assess <doi> --score 8 --include --notes "Relevant to research question"

# Batch assessment from CSV
academic-review assess --batch assessments.csv
```

**Arguments:**
- `doi`: Paper DOI to assess
- `--score`: Quality score 0-10
- `--include / --exclude`: Inclusion decision
- `--notes`: Assessment notes
- `--batch`: CSV file with columns: doi, score, include, notes

**Output:**
```
✓ Assessed: 10.1234/example.doi
  Score: 8/10
  Decision: INCLUDE
  Notes: Relevant to research question

Review statistics:
  Total papers: 523
  Assessed: 124 (23.7%)
  Included: 89 (71.8%)
  Excluded: 35 (28.2%)
```

#### `academic-review analyze`

Perform thematic analysis on included papers.

**Usage:**
```bash
academic-review analyze --method tfidf --clusters 5
```

**Arguments:**
- `--method`: Analysis method (tfidf, ai, hybrid) [default: tfidf]
- `--clusters`: Number of main themes (3-10) [default: 5]

**Output:**
```
Analyzing 89 included papers...
  ✓ Keyword extraction (TF-IDF)
  ✓ Co-occurrence analysis
  ✓ Hierarchical clustering

Themes identified: 5 main themes, 12 subthemes

Theme 1: Healthcare Data Analytics (23 papers)
  • Keywords: analytics, data, healthcare, maturity, insights
  • Subthemes: Predictive analytics, Descriptive analytics

Theme 2: Workforce Challenges (18 papers)
  • Keywords: workforce, turnover, retention, training, skills
  • Subthemes: Staff retention, Training programs

[...]
```

#### `academic-review synthesize`

Generate narrative synthesis of review findings.

**Usage:**
```bash
academic-review synthesize --output synthesis.md
```

**Arguments:**
- `--output`: Output file path (default: synthesis.md)

**Output:**
```
Generating synthesis...
  ✓ Introduction and research question
  ✓ Theme summaries (5 themes)
  ✓ Evidence synthesis
  ✓ Research gaps identified
  ✓ Conclusions and future directions

Synthesis written to: synthesis.md (2,847 words)
```

#### `academic-review status`

Show review progress and statistics.

**Usage:**
```bash
academic-review status
```

**Output:**
```
Review: my-review-2025
Stage: ELIGIBILITY
Created: 2025-12-01
Updated: 2025-12-09

Progress:
  Papers found: 523
  Screening: 124/523 (23.7%)
  Included: 89 (71.8% of assessed)
  Excluded: 35 (28.2% of assessed)

Themes: 5 main themes identified
Export: Not yet exported

Next steps:
  1. Complete screening (399 papers remaining)
  2. Verify included papers
  3. Generate synthesis
  4. Export review
```

#### `academic-review export`

Export review in multiple formats.

**Usage:**
```bash
# Single format
academic-review export --format docx --output review.docx

# Multiple formats
academic-review export --format bibtex,docx,latex,html,json --outdir exports/
```

**Arguments:**
- `--format`: Export format(s): bibtex, docx, latex, html, json (comma-separated)
- `--output`: Output file path (single format only)
- `--outdir`: Output directory (multiple formats)
- `--template`: LaTeX template (nature, ieee, generic) [default: generic]
- `--style`: DOCX style (apa7, apa6, mla) [default: apa7]

**Output:**
```
Exporting review...
  ✓ BibTeX: exports/review.bib (89 entries)
  ✓ DOCX: exports/review.docx (APA7 style, 34 pages)
  ✓ LaTeX: exports/review.tex (generic template)
  ✓ HTML: exports/review.html (interactive, 2.1 MB)
  ✓ JSON: exports/review.json (complete data, 1.8 MB)

All exports complete. Total size: 4.2 MB
```

## Container Architecture

### Multi-Stage Containerfile

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY lit_review/ lit_review/
COPY scripts/ scripts/

# Set PATH to use virtual environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Create data directories
RUN mkdir -p /app/review_data/reviews /app/review_data/.backups /app/review_data/.deleted

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD academic-review status || exit 1

# Set entrypoint
ENTRYPOINT ["academic-review"]
CMD ["--help"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  academic-review:
    build:
      context: .
      dockerfile: Containerfile
    volumes:
      - ./review_data:/app/review_data
      - ./exports:/app/exports
    environment:
      - CROSSREF_API_EMAIL=${CROSSREF_API_EMAIL}
      - SEMANTIC_SCHOLAR_API_KEY=${SEMANTIC_SCHOLAR_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}  # For AI synthesis
      - LOG_LEVEL=INFO
    command: ["status"]

  # Development service with source code mounted
  academic-review-dev:
    build:
      context: .
      dockerfile: Containerfile
      target: builder
    volumes:
      - ./lit_review:/app/lit_review
      - ./scripts:/app/scripts
      - ./tests:/app/tests
      - ./review_data:/app/review_data
      - ./exports:/app/exports
    environment:
      - CROSSREF_API_EMAIL=${CROSSREF_API_EMAIL}
      - SEMANTIC_SCHOLAR_API_KEY=${SEMANTIC_SCHOLAR_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - LOG_LEVEL=DEBUG
    command: ["bash"]
    stdin_open: true
    tty: true
```

### Container Usage

```bash
# Build container
docker build -t academic-review:latest .

# Run command
docker run --rm \
  -v $(pwd)/review_data:/app/review_data \
  -e CROSSREF_API_EMAIL=user@example.com \
  academic-review:latest search "healthcare analytics"

# Development mode
docker-compose run --rm academic-review-dev bash

# Inside container
academic-review init my-review --title "Test" --question "Test?"
pytest tests/ -v
```

## Security Considerations

### Authentication & Authorization

**API Keys:**
- Stored in environment variables only
- Never logged or printed
- Validated at startup with clear error messages
- Per-database configuration (CROSSREF_API_EMAIL, SEMANTIC_SCHOLAR_API_KEY, etc.)

**File Permissions:**
- Review data files: 600 (owner read/write only)
- Backup files: 600 (owner read/write only)
- Exported files: 644 (owner read/write, others read)

### Input Validation

**User Input:**
- All CLI arguments validated by Click parameter types
- DOIs validated with regex before API calls
- File paths validated to prevent directory traversal
- Query strings sanitized to prevent injection

**API Responses:**
- All responses validated with Pydantic models
- Missing fields handled gracefully with defaults
- Unexpected fields logged but ignored
- Malformed responses trigger retry with exponential backoff

### SQL Injection Prevention

Not applicable (no SQL database). JSON-based persistence with Pydantic validation.

### Secrets Management

**Environment Variables:**
```bash
# .env file (never committed to Git)
CROSSREF_API_EMAIL=user@example.com
SEMANTIC_SCHOLAR_API_KEY=abc123...
ANTHROPIC_API_KEY=sk-...
```

**Loading:**
```python
from dotenv import load_dotenv
import os

load_dotenv()

CROSSREF_EMAIL = os.getenv("CROSSREF_API_EMAIL")
if not CROSSREF_EMAIL:
    raise EnvironmentError("CROSSREF_API_EMAIL not set")
```

**Logging:**
```python
# Never log secrets
logger.info(f"Using Crossref API with email: {CROSSREF_EMAIL[:5]}...")  # First 5 chars only
```

### Rate Limiting

**Per-Database Limits:**
- Crossref: 50 requests/second with email
- PubMed: 3 requests/second (10 with API key)
- ArXiv: 1 request/3 seconds
- Semantic Scholar: 100 requests/5 minutes

**Implementation:**
```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=50, period=1)  # 50 calls per second
def call_crossref_api(query: str) -> List[Dict]:
    # API call implementation
    pass
```

### CORS Policy

Not applicable (CLI tool, no web server).

## Error Handling Strategy

### Error Categories

**1. Network Errors (Transient)**
- Connection timeout
- DNS resolution failure
- HTTP 5xx errors
- **Strategy:** Retry with exponential backoff (max 3 attempts)

**2. API Errors (Permanent)**
- HTTP 400 Bad Request (invalid query)
- HTTP 401 Unauthorized (missing/invalid API key)
- HTTP 404 Not Found (resource doesn't exist)
- **Strategy:** Log error, return empty results or raise with clear message

**3. Validation Errors (User Input)**
- Invalid DOI format
- Score out of range (not 0-10)
- Missing required fields
- **Strategy:** Raise ValidationError with helpful message and suggestions

**4. File System Errors**
- Permission denied
- Disk full
- File not found
- **Strategy:** Check permissions first, provide fix instructions, use atomic writes

**5. Data Integrity Errors**
- Corrupted JSON
- Missing backup
- Concurrent modification
- **Strategy:** Restore from backup, log error, notify user

### Logging

**Log Levels:**
- DEBUG: Detailed diagnostics (API requests, data transformations)
- INFO: Normal operations (searches, assessments, exports)
- WARNING: Recoverable issues (API timeout, partial results)
- ERROR: Serious problems (file write failure, validation error)
- CRITICAL: System-level failures (missing API keys, corrupted data)

**Log Format (Structured JSON):**
```json
{
  "timestamp": "2025-12-09T10:30:45.123Z",
  "level": "INFO",
  "logger": "lit_review.application.search",
  "message": "Searching Crossref",
  "review_id": "my-review-2025",
  "query": "healthcare analytics",
  "limit": 100,
  "duration_ms": 1234
}
```

**Log Configuration:**
```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Add extra fields from record
        if hasattr(record, "review_id"):
            log_data["review_id"] = record.review_id
        return json.dumps(log_data)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("academic-review.log"),
        logging.StreamHandler()  # Also log to console
    ]
)
```

### Monitoring

**Health Check:**
```python
@click.command()
def health():
    """Check system health"""
    checks = {
        "review_data_writable": check_directory_writable("./review_data"),
        "api_keys_present": check_api_keys(),
        "disk_space": check_disk_space(min_mb=100),
    }

    if all(checks.values()):
        click.echo("✓ All systems operational")
        sys.exit(0)
    else:
        click.echo("✗ Health check failed")
        for check, status in checks.items():
            click.echo(f"  {check}: {'✓' if status else '✗'}")
        sys.exit(1)
```

**Metrics (Optional):**
- Request count by database
- Request duration percentiles (p50, p95, p99)
- Error rate by error type
- Papers processed per second
- Memory usage

## Testing Strategy

### Unit Tests (80%+ of tests)

**Domain Layer:**
- Test all entities with valid/invalid data
- Test all value objects (DOI, Author validation)
- Test domain services (BibTeX parsing, citation formatting)
- No mocks required (pure business logic)

**Example:**
```python
def test_paper_equality_by_doi():
    """Papers with same DOI are equal"""
    paper1 = Paper(doi=DOI("10.1234/example"), title="Paper 1", ...)
    paper2 = Paper(doi=DOI("10.1234/example"), title="Paper 2", ...)
    assert paper1 == paper2

def test_review_stage_transition():
    """Review enforces valid stage transitions"""
    review = Review(stage=WorkflowStage.INITIALIZED)
    review.add_paper(paper, stage=WorkflowStage.SEARCH)  # OK

    with pytest.raises(WorkflowError):
        review.add_paper(paper, stage=WorkflowStage.ANALYSIS)  # Wrong stage
```

**Application Layer:**
```python
def test_search_use_case_with_mock_adapters():
    """SearchPapersUseCase coordinates database searches"""
    # Mock adapters
    crossref = Mock(spec=SearchService)
    crossref.search.return_value = [paper1, paper2]

    pubmed = Mock(spec=SearchService)
    pubmed.search.return_value = [paper2, paper3]  # paper2 is duplicate

    # Execute use case
    use_case = SearchPapersUseCase(adapters={"crossref": crossref, "pubmed": pubmed})
    results = use_case.execute(query="test", databases=["crossref", "pubmed"])

    # Assertions
    assert len(results) == 3  # paper1, paper2, paper3 (paper2 deduplicated)
    crossref.search.assert_called_once()
    pubmed.search.assert_called_once()
```

### Integration Tests (15-20% of tests)

**API Integration:**
```python
@pytest.mark.integration
def test_crossref_adapter_real_api():
    """CrossrefAdapter retrieves real data from API"""
    adapter = CrossrefAdapter(email="test@example.com")
    results = adapter.search(query="healthcare analytics", limit=10)

    assert len(results) > 0
    assert all(isinstance(p, Paper) for p in results)
    assert all(p.doi is not None for p in results)  # Crossref always has DOIs
```

**File I/O:**
```python
@pytest.mark.integration
def test_json_repository_atomic_writes(tmp_path):
    """JSONRepository uses atomic writes"""
    repo = JSONRepository(base_path=tmp_path)
    review = create_sample_review()

    # Save review
    repo.save(review)

    # Verify file exists
    assert (tmp_path / "reviews" / f"{review.review_id}.json").exists()

    # Verify backup created
    backups = list((tmp_path / ".backups").glob(f"{review.review_id}_*.json"))
    assert len(backups) == 1
```

### Performance Tests

**Benchmarks:**
```python
@pytest.mark.benchmark
def test_search_performance(benchmark):
    """Search completes in <2 minutes for 1000 papers"""
    use_case = SearchPapersUseCase(adapters=create_real_adapters())

    result = benchmark(
        use_case.execute,
        query="healthcare",
        databases=["crossref", "pubmed", "arxiv", "semantic_scholar"],
        limit=250  # 250 per database = 1000 total
    )

    assert benchmark.stats.mean < 120  # <2 minutes
    assert len(result) >= 900  # Allow for some duplicates

@pytest.mark.benchmark
def test_theme_analysis_performance(benchmark):
    """Theme analysis completes in <30s for 500 papers"""
    papers = [create_sample_paper() for _ in range(500)]
    use_case = AnalyzeThemesUseCase()

    result = benchmark(use_case.execute, papers=papers)

    assert benchmark.stats.mean < 30  # <30 seconds
    assert 3 <= len(result.themes) <= 10  # Reasonable theme count
```

### Container Tests

**Build Validation:**
```bash
# Test container builds successfully
docker build -t academic-review:test .

# Test health check
docker run --rm academic-review:test health

# Test CLI command
docker run --rm academic-review:test --version
```

## Deployment Strategy

### Environments

**1. Local Development**
- Use `uv sync` for dependency management
- Run tests with `pytest`
- Use `.env` file for API keys
- SQLite for development database (if needed)

**2. Docker Development**
- Use `docker-compose` for consistent environment
- Mount source code for live reloading
- Shared review_data volume for persistence

**3. Production (CLI Distribution)**
- PyPI package: `pip install academic-review-tool`
- Docker image: `docker pull academic-review:latest`
- Binary distribution: PyInstaller for standalone executable

### CI/CD Pipeline

**GitHub Actions Workflow:**

```yaml
name: CI/CD

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        run: uv sync --frozen

      - name: Lint with ruff
        run: |
          uv run ruff format --check .
          uv run ruff check .

      - name: Type check with mypy
        run: uv run mypy lit_review/ scripts/

      - name: Test with pytest
        run: |
          uv run pytest tests/ -v --cov=lit_review --cov-report=xml

      - name: Check coverage
        run: |
          coverage=$(uv run coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//')
          if (( $(echo "$coverage < 80" | bc -l) )); then
            echo "Coverage $coverage% is below 80%"
            exit 1
          fi

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3

  build-container:
    needs: test
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: docker build -t academic-review:${{ github.sha }} .

      - name: Test Docker image
        run: |
          docker run --rm academic-review:${{ github.sha }} --version
          docker run --rm academic-review:${{ github.sha }} health

      - name: Push to Docker Hub (main only)
        if: github.ref == 'refs/heads/main'
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker tag academic-review:${{ github.sha }} academic-review:latest
          docker push academic-review:latest

  release:
    needs: build-container
    if: github.ref == 'refs/heads/main' && startsWith(github.event.head_commit.message, 'release:')
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Build PyPI package
        run: |
          uv sync
          uv run python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

### Database Migrations

Not applicable (JSON-based persistence, no schema migrations).

If migrating to SQLite/PostgreSQL in future:
- Use Alembic for schema versioning
- Test migrations in staging first
- Only backward-compatible changes
- Provide rollback scripts for each migration

## Observability

### Logging

**Application Logs:**
- Format: Structured JSON to `academic-review.log`
- Fields: timestamp, level, logger, message, review_id, duration_ms
- Rotation: Daily rotation, keep 30 days
- Location: `./logs/academic-review.log`

**Access Logs:**
Not applicable (CLI tool, no HTTP server).

**Error Logs:**
- All ERROR and CRITICAL level messages
- Include full stack trace and context
- Deduplicate similar errors (max 1 per minute)

### Metrics

**Search Metrics:**
- Papers found per database
- Search duration per database
- Deduplication rate (duplicates / total)
- API errors by database and error type

**Assessment Metrics:**
- Papers assessed per day
- Inclusion rate (included / assessed)
- Average quality score
- Time per assessment

**Export Metrics:**
- Export format usage
- Export file sizes
- Export duration by format

**Performance Metrics:**
- Memory usage (peak and average)
- CPU usage during analysis
- Disk I/O for file operations

### Tracing

Not applicable (CLI tool, no distributed system).

If adding web API in future, use OpenTelemetry for distributed tracing.

## Scalability Plan

### Current Scale (JSON-based)

**Supported:**
- Up to 10,000 papers per review
- Up to 100 reviews
- Total data: <1GB

**Performance:**
- Search: 1000 papers/minute
- Analysis: <30 seconds for 500 papers
- Export: <60 seconds for 1000 papers
- Memory: <500MB peak usage

### Scaling Strategy

**Vertical Scaling (if needed for larger reviews):**
- Increase memory allocation (current: 500MB → 2GB)
- Use faster CPU for clustering (current: 2 cores → 8 cores)
- Optimize TF-IDF with sparse matrices

**Horizontal Scaling (future):**
- Not applicable (CLI tool, single-user)
- If multi-user needed, migrate to web API with PostgreSQL backend

**Database Scaling (if >10k papers):**
- Migrate from JSON to SQLite for better query performance
- Use indexes on DOI, title, year fields
- Implement pagination for large result sets

**Caching (if API costs become issue):**
- Cache API responses by query hash (TTL: 7 days)
- Use Redis for distributed cache (if web API added)
- Invalidate cache on manual refresh

## Disaster Recovery

### Backup Strategy

**Automatic Backups:**
- Before every write: create backup in `.backups/`
- Keep last 5 backups per review
- Compression: gzip for backups >1MB

**Manual Backups:**
- `academic-review backup --review-id <id> --output backup.tar.gz`
- Include review data, exports, and logs
- Store backups in version control or cloud storage

### Recovery Procedures

**1. Corrupted Review File**
```bash
# Automatic: Load from latest backup
academic-review load --review-id my-review --from-backup latest

# Manual: Restore specific backup
cp review_data/.backups/my-review_20251209_103045.json.gz review_data/reviews/my-review.json.gz
gunzip review_data/reviews/my-review.json.gz
```

**2. Accidental Deletion**
```bash
# Restore from soft delete
academic-review restore --review-id my-review

# If soft delete expired, restore from Git history
git checkout HEAD~5 -- review_data/reviews/my-review.json
```

**3. Data Integrity Check**
```bash
# Verify all reviews
academic-review verify --all

# Fix issues automatically
academic-review verify --fix
```

**4. Complete Data Loss**
```bash
# Restore from Git
git checkout main -- review_data/

# Restore from external backup
tar -xzf backup-20251201.tar.gz -C ./
```

**5. Post-Recovery Validation**
```bash
# Load each review and check statistics
academic-review status --review-id my-review

# Re-run critical operations
academic-review analyze
academic-review export --format json
```

## Open Technical Questions

- [ ] **Question 1:** Should we support custom database sources beyond the initial four (Crossref, PubMed, ArXiv, Semantic Scholar)?
  - **Impact:** Extensibility vs. complexity
  - **Decision needed:** Before Phase 3 (Infrastructure)

- [ ] **Question 2:** Do we need SQLite backend option for very large reviews (>10k papers)?
  - **Impact:** Performance vs. simplicity
  - **Decision needed:** After Phase 5 (based on performance tests)

- [ ] **Question 3:** Should thematic analysis support languages other than English?
  - **Impact:** Scope increase, additional dependencies (language models)
  - **Decision needed:** Before Phase 2 (Application)

- [ ] **Question 4:** Is offline mode necessary for scenarios without internet access?
  - **Impact:** Caching strategy, storage requirements
  - **Decision needed:** Before Phase 3 (Infrastructure)

- [ ] **Question 5:** Should we integrate with Zenodo for automatic DOI assignment to completed reviews?
  - **Impact:** Additional API integration, authentication
  - **Decision needed:** After Phase 4 (nice-to-have)

- [ ] **Question 6:** Do we need role-based access control for collaborative reviews?
  - **Impact:** Major architecture change (multi-user support)
  - **Decision needed:** Out of scope for v1, reconsider for v2

## Design Trade-offs

### Decision 1: Clean Architecture vs. Simpler Layered Architecture

**Chosen:** Clean Architecture (4 layers with dependency inversion)

**Reasoning:**
- **Pro:** Separates business logic from external dependencies
- **Pro:** Highly testable (domain layer has no external dependencies)
- **Pro:** Flexible: easy to swap implementations (JSON → SQLite, TF-IDF → AI)
- **Pro:** Maintainable: clear separation of concerns
- **Con:** More initial complexity and boilerplate
- **Con:** Steeper learning curve for contributors

**Alternative Considered:** Layered architecture (presentation → business → data)
- **Why not chosen:** Tight coupling between layers, harder to test, less flexible

---

### Decision 2: JSON Files vs. SQLite Database

**Chosen:** JSON files with atomic writes

**Reasoning:**
- **Pro:** Human-readable for debugging and manual edits
- **Pro:** Version-control friendly (Git diff works well)
- **Pro:** No database server required (simpler deployment)
- **Pro:** Sufficient performance for typical review sizes (<10k papers)
- **Pro:** Easy backup and portability
- **Con:** Limited query capabilities (can't filter/sort without loading entire file)
- **Con:** Performance degrades for very large reviews (>10k papers)

**Alternative Considered:** SQLite database
- **Why not chosen:** Overkill for typical use case, binary format not version-control friendly
- **Future option:** Provide SQLite backend for large reviews (>10k papers)

---

### Decision 3: TF-IDF vs. AI-Only for Thematic Analysis

**Chosen:** TF-IDF with optional AI enhancement

**Reasoning:**
- **Pro:** TF-IDF is deterministic and reproducible
- **Pro:** No API costs or rate limits
- **Pro:** Fast (<30s for 500 papers)
- **Pro:** Transparent: users can inspect keywords and clusters
- **Con:** May miss semantic relationships that AI would catch
- **Solution:** Provide AI-powered enhancement as optional feature

**Alternative Considered:** AI-only thematic analysis
- **Why not chosen:** Non-deterministic, API costs, requires internet, slower

---

### Decision 4: CLI vs. Web Interface

**Chosen:** CLI-first with Click framework

**Reasoning:**
- **Pro:** Academic workflows are script-driven and automation-friendly
- **Pro:** Easy to integrate with existing tools (Make, shell scripts)
- **Pro:** No server deployment required
- **Pro:** Faster to develop and test
- **Con:** Less visual, steeper learning curve for non-technical users
- **Future option:** Add web interface in v2 if demand exists

**Alternative Considered:** Web interface (Flask/FastAPI)
- **Why not chosen:** Overkill for single-user academic tool, adds deployment complexity

---

### Decision 5: Parallel vs. Sequential Database Searches

**Chosen:** Parallel searches with ThreadPoolExecutor

**Reasoning:**
- **Pro:** 3-4x faster than sequential searches
- **Pro:** Better user experience (results in 30-60s vs 2-4 minutes)
- **Pro:** Handles timeouts gracefully (partial results)
- **Con:** More complex error handling
- **Con:** Higher memory usage (concurrent connections)
- **Mitigation:** Limit to 4 workers (one per database)

**Alternative Considered:** Sequential searches
- **Why not chosen:** Too slow for practical use (2-4 minutes per search)

## References

### Academic Standards

- **PRISMA 2020:** [PRISMA Statement](http://www.prisma-statement.org/)
  - Guidelines for systematic review reporting
  - Flow diagram specification
  - Checklist of 27 items

### API Documentation

- **Crossref REST API:** https://api.crossref.org
- **PubMed E-utilities:** https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **ArXiv API:** https://arxiv.org/help/api/user-manual
- **Semantic Scholar API:** https://api.semanticscholar.org/

### Architecture Patterns

- **Clean Architecture:** Robert C. Martin, 2012
  - [Blog post](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
  - Dependency inversion, separation of concerns

- **Hexagonal Architecture:** Alistair Cockburn, 2005
  - Ports and adapters pattern
  - Alternative name for similar concepts

### Python Best Practices

- **Pydantic Documentation:** https://docs.pydantic.dev/
- **Click Documentation:** https://click.palletsprojects.com/
- **pytest Best Practices:** https://docs.pytest.org/en/stable/goodpractices.html
- **Python Type Hints (PEP 484):** https://peps.python.org/pep-0484/
