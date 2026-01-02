# Academic Literature Review Tool

A Python-based systematic literature review tool implementing Clean Architecture for rigorous academic claim verification in healthcare research.

## When to Use

| Approach | Use Case | DOI Quality |
|----------|----------|-------------|
| `lit_review/` | Systematic reviews (PRISMA-compliant) | API-verified from authoritative sources |
| Manual curation | Narrative reviews | Requires manual verification |

**This paper** (`paper.md`) used manual curation for its narrative review. The 108 references in `references.bib` were gathered through traditional literature searching, not through this tool.

**Use `lit_review/` when:**
- Conducting a systematic review with PRISMA methodology
- Need reproducible, automated multi-database searches
- Want API-verified DOIs (eliminates manual entry errors)
- Require structured workflow stages (PLANNING → SEARCH → SCREENING → ANALYSIS → SYNTHESIS)

**Use manual curation when:**
- Writing narrative reviews or opinion pieces
- Sources are primarily grey literature or non-indexed
- Need flexibility outside systematic review methodology

## Features

- **Multi-Database Search**: Parallel searches across Crossref, PubMed, ArXiv, and Semantic Scholar
- **Automatic Deduplication**: DOI-based deduplication with >99% accuracy
- **Quality Assessment**: Structured paper assessment with 0-10 scoring
- **Thematic Analysis**: TF-IDF and hierarchical clustering for theme extraction
- **AI-Powered Synthesis**: Optional Claude AI integration for narrative generation
- **Multiple Export Formats**: BibTeX, DOCX, LaTeX, HTML, JSON
- **PRISMA Compliance**: Follows PRISMA 2020 guidelines for systematic reviews
- **Test-Driven**: >80% code coverage with comprehensive test suite
- **Clean Architecture**: Strict layer separation for maintainability

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/stharrold/yuimedi-paper-20250901.git
cd yuimedi-paper-20250901

# Install dependencies with uv
uv sync

# Verify installation
uv run academic-review --help
```

### Basic Usage

```bash
# Initialize a new review
uv run academic-review init "ML in Radiology" \
  --question "What is the effectiveness of ML for radiology diagnosis?" \
  --include "Peer-reviewed" \
  --include "English language" \
  --exclude "Preprints"

# Search for papers
uv run academic-review search "ML in Radiology" \
  --database crossref \
  --keywords "machine learning radiology diagnosis"

# Check review status
uv run academic-review status "ML in Radiology"

# Export to BibTeX
uv run academic-review export "ML in Radiology" \
  --format bibtex \
  --output my_review.bib
```

## Architecture

The tool follows Clean Architecture principles with four layers:

```
┌─────────────────────────────────────────┐
│         Interfaces (CLI)                │  ← User interaction
├─────────────────────────────────────────┤
│    Infrastructure (Adapters, AI)       │  ← External services
├─────────────────────────────────────────┤
│   Application (Use Cases, Ports)       │  ← Business workflows
├─────────────────────────────────────────┤
│  Domain (Entities, Value Objects)      │  ← Core business logic
└─────────────────────────────────────────┘
```

### Layer Responsibilities

- **Domain**: Core entities (Paper, Review), value objects (DOI, Author), business rules
- **Application**: Use cases (SearchPapers, AnalyzeThemes), port interfaces
- **Infrastructure**: Database adapters, AI integration, file persistence
- **Interfaces**: CLI commands and user interaction

## Workflow Stages

Reviews follow a structured workflow based on PRISMA guidelines:

1. **PLANNING**: Define research question and inclusion/exclusion criteria
2. **SEARCH**: Execute multi-database searches, collect papers
3. **SCREENING**: Assess papers against criteria, track decisions
4. **ANALYSIS**: Deep analysis of included papers, thematic coding
5. **SYNTHESIS**: Generate narrative synthesis and conclusions
6. **COMPLETE**: Export final review in desired format

```bash
# Advance to next stage
uv run academic-review advance "My Review"
```

## CLI Commands

### `init` - Initialize a new review

```bash
uv run academic-review init TITLE \
  --question "Your research question" \
  --include "Inclusion criterion 1" \
  --include "Inclusion criterion 2" \
  --exclude "Exclusion criterion"
```

### `search` - Search academic databases

```bash
uv run academic-review search TITLE \
  --database crossref \
  --keywords "search terms"
```

Supported databases:
- `crossref` - Crossref API (no key required)
- `pubmed` - PubMed/MEDLINE (optional API key)
- `arxiv` - arXiv preprints
- `semantic-scholar` - Semantic Scholar

### `status` - Show review statistics

```bash
uv run academic-review status TITLE
```

Displays:
- Current stage
- Paper counts by status
- Inclusion/exclusion criteria
- Progress indicators

### `assess` - Assess a paper

```bash
uv run academic-review assess TITLE DOI \
  --status included \
  --score 8 \
  --notes "High quality RCT"
```

### `analyze` - Run thematic analysis

```bash
uv run academic-review analyze TITLE
```

Extracts themes using:
- TF-IDF for keyword importance
- Hierarchical clustering for theme grouping
- Optional AI-powered theme naming

### `synthesize` - Generate narrative synthesis

```bash
uv run academic-review synthesize TITLE
```

Creates:
- Summary of included papers
- Theme descriptions
- Evidence synthesis
- Recommendations for future research

### `export` - Export review

```bash
uv run academic-review export TITLE \
  --format bibtex \
  --output output.bib
```

Formats:
- `bibtex` - BibTeX references
- `docx` - Word document with full report
- `latex` - LaTeX document
- `html` - HTML report
- `json` - Machine-readable JSON

### `list` - List all reviews

```bash
uv run academic-review list
```

### `delete` - Delete a review

```bash
uv run academic-review delete TITLE --yes
```

## Configuration

### Environment Variables

- `LIT_REVIEW_DATA_DIR` - Data storage location (default: `~/.lit_review`)
- `ANTHROPIC_API_KEY` - Claude API key for AI features (optional)
- `PUBMED_EMAIL` - Email for PubMed API access (optional but recommended)

### Setup Example

```bash
# Set data directory
export LIT_REVIEW_DATA_DIR=/path/to/reviews

# Set API keys (optional)
export ANTHROPIC_API_KEY=sk-ant-...
export PUBMED_EMAIL=your.email@example.com

# Run commands
uv run academic-review init "My Review" -q "Research question"
```

## Development

### Running Tests

```bash
# All tests
uv run pytest tests/lit_review/ -v

# With coverage
uv run pytest tests/lit_review/ --cov=lit_review --cov-report=term-missing

# Exclude integration tests (no API calls)
uv run pytest tests/lit_review/ -m "not integration"

# Run specific test file
uv run pytest tests/lit_review/domain/test_paper.py -v
```

### Code Quality

```bash
# Format code
uv run ruff format lit_review/ tests/lit_review/

# Lint
uv run ruff check lit_review/ tests/lit_review/

# Type check
uv run mypy lit_review/

# Security scan
uv run bandit -r lit_review/
```

### Project Structure

```
lit_review/
├── domain/
│   ├── entities/
│   │   ├── paper.py          # Paper entity
│   │   ├── review.py         # Review entity
│   │   └── citation.py       # Citation entity
│   ├── values/
│   │   ├── doi.py            # DOI value object
│   │   ├── author.py         # Author value object
│   │   └── keywords.py       # Keywords value object
│   ├── services/
│   │   └── citation_formatter.py
│   └── exceptions.py
├── application/
│   ├── ports/
│   │   ├── search_service.py
│   │   ├── paper_repository.py
│   │   └── ai_analyzer.py
│   └── usecases/
│       ├── search_papers.py
│       ├── analyze_themes.py
│       ├── generate_synthesis.py
│       └── export_review.py
├── infrastructure/
│   ├── adapters/
│   │   ├── crossref_adapter.py
│   │   ├── pubmed_adapter.py
│   │   ├── arxiv_adapter.py
│   │   └── semantic_scholar_adapter.py
│   ├── persistence/
│   │   └── json_repository.py
│   └── ai/
│       └── claude_analyzer.py
└── interfaces/
    └── cli/
        └── review_cli.py
```

## Troubleshooting

### Common Issues

#### Error: Review not found
```bash
# List all reviews to check name
uv run academic-review list

# Names are case-sensitive
uv run academic-review status "Exact Title"
```

#### Error: DOI validation failed
```bash
# DOI must start with "10."
# Example: 10.1001/jama.2024.12345
uv run academic-review assess "My Review" "10.1001/jama.2024.12345"
```

#### API rate limiting
```bash
# PubMed limits: 3 requests/second without key
# Solution: Set PUBMED_EMAIL for 10 requests/second
export PUBMED_EMAIL=your.email@example.com

# Crossref: No rate limit with polite pool
# Automatic when you set email in requests
```

#### Low test coverage
```bash
# Run with coverage report
uv run pytest --cov=lit_review --cov-report=html

# Open htmlcov/index.html to see gaps
open htmlcov/index.html
```

### Performance Tips

- Use `--database crossref` first (fastest, no key required)
- Enable AI features only when needed (API costs)
- Export to JSON for fastest processing
- Use parallel searches (automatic with ThreadPoolExecutor)

## Citation

If you use this tool in your research, please cite:

```bibtex
@software{harrold2025litreview,
  title = {Academic Literature Review Tool for Rigorous Claim Verification},
  author = {Harrold, Samuel T. and {YuiQuery Research Team}},
  year = {2025},
  url = {https://github.com/stharrold/yuimedi-paper-20250901},
  version = {1.0.0},
  doi = {10.5281/zenodo.XXXXXXX}
}
```

See [CITATION.cff](../CITATION.cff) for more details.

## License

MIT License - see [LICENSE](../LICENSE) for details.

## Contributing

This is a research repository. For contributions, please:

1. Fork the repository
2. Create a feature branch
3. Follow the existing code style
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

## Support

- Issues: https://github.com/stharrold/yuimedi-paper-20250901/issues
- Documentation: See `docs/` directory
- Examples: See `examples/` directory (if available)

## Acknowledgments

Developed to support rigorous claim verification in the YuiQuery healthcare analytics research paper. Built with Clean Architecture principles and test-driven development.
