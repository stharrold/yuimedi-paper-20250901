---
description: Academic Literature Review Workflow Package
children:
- ARCHIVED/GEMINI.md
- application/GEMINI.md
- domain/GEMINI.md
- infrastructure/GEMINI.md
- interfaces/GEMINI.md
parent: ../GEMINI.md
---

# Gemini Context Context: lit_review

## Purpose

Academic literature review workflow system following Clean Architecture principles. Provides CLI commands for managing systematic literature reviews with search, assessment, and export capabilities.

## Architecture

```
lit_review/
├── domain/           # Core business logic (no external dependencies)
│   ├── entities/     # Paper, Review entities
│   ├── values/       # DOI, Author value objects
│   ├── services/     # CitationFormatter
│   └── exceptions.py # Domain exceptions
├── application/      # Use cases and ports
│   ├── ports/        # SearchService, PaperRepository interfaces
│   └── usecases/     # SearchPapersUseCase, ExportReviewUseCase
├── infrastructure/   # External service implementations
│   ├── adapters/     # CrossrefAdapter
│   └── persistence/  # JSONReviewRepository
└── interfaces/       # User interfaces
    └── cli/          # Click-based review_cli.py
```

## Key Commands

```bash
# Initialize a new review
academic-review init "ML Healthcare" -q "What is the impact?" -i "Peer-reviewed"

# Search academic databases
academic-review search "ML Healthcare" -d crossref -k "machine learning diagnosis"

# Check review status
academic-review status "ML Healthcare"

# Advance workflow stage
academic-review advance "ML Healthcare"

# Export to BibTeX
academic-review export "ML Healthcare" -f bibtex -o refs.bib

# List all reviews
academic-review list

# Delete a review
academic-review delete "ML Healthcare" --yes
```

## Workflow Stages

PLANNING → SEARCH → SCREENING → ANALYSIS → SYNTHESIS → COMPLETE

- PLANNING: Define research question and criteria
- SEARCH: Search databases and add papers
- SCREENING: Assess papers against criteria
- ANALYSIS: Deep analysis of included papers
- SYNTHESIS: Write up findings
- COMPLETE: Review finished

## Configuration

Set `LIT_REVIEW_DATA_DIR` environment variable to customize data storage location:

```bash
export LIT_REVIEW_DATA_DIR=/path/to/data
```

Default: `~/.lit_review/`

## Testing

```bash
# Run all tests
uv run pytest tests/lit_review/ -v

# Run with coverage
uv run pytest tests/lit_review/ --cov=lit_review --cov-report=term-missing
```

## Related

- **Parent**: [Root GEMINI.md](../GEMINI.md)
- **Spec**: [specs/academic-literature-review-workflow/spec.md](../specs/academic-literature-review-workflow/spec.md)

## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
- **[../GEMINI.md](../GEMINI.md)** - Parent directory: Root

**Child Directories:**
- **[ARCHIVED/GEMINI.md](ARCHIVED/GEMINI.md)** - Archived
- **[application/GEMINI.md](application/GEMINI.md)** - Application
- **[domain/GEMINI.md](domain/GEMINI.md)** - Domain
- **[infrastructure/GEMINI.md](infrastructure/GEMINI.md)** - Infrastructure
- **[interfaces/GEMINI.md](interfaces/GEMINI.md)** - Interfaces
