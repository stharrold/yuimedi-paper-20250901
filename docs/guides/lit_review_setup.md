# Academic Literature Review Tool - Setup Guide

Complete setup instructions for the Academic Literature Review Tool, covering both local and containerized installations.

## Prerequisites

### Required

- **Python**: 3.11, 3.12, or 3.13
- **uv**: Fast Python package manager
- **Git**: Version control

### Optional

- **Docker or Podman**: For containerized deployment
- **Anthropic API Key**: For AI-powered features
- **PubMed Email**: For enhanced PubMed API access

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/stharrold/yuimedi-paper-20250901.git
cd yuimedi-paper-20250901
```

### 2. Install uv (if not already installed)

#### macOS/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:

```bash
uv --version
```

### 3. Install Dependencies

```bash
# Install all dependencies (including dev dependencies)
uv sync

# Install only runtime dependencies
uv sync --no-dev

# Install with optional features
uv sync --extra ai      # AI-powered features
uv sync --extra export  # Document export (DOCX)
uv sync --all-extras    # All optional features
```

### 4. Verify Installation

```bash
# Check that CLI is available
uv run academic-review --version

# Run a quick test
uv run academic-review --help
```

### 5. Configure Environment (Optional)

Create a `.env` file in the project root:

```bash
# Data storage location (default: ~/.lit_review)
LIT_REVIEW_DATA_DIR=/path/to/your/reviews

# API Keys (optional)
ANTHROPIC_API_KEY=sk-ant-...
PUBMED_EMAIL=your.email@example.com

# Logging (optional)
LOG_LEVEL=INFO
```

Or set environment variables directly:

```bash
export LIT_REVIEW_DATA_DIR=/path/to/reviews
export ANTHROPIC_API_KEY=sk-ant-...
export PUBMED_EMAIL=your.email@example.com
```

### 6. Run Tests (Optional)

```bash
# Run all tests
uv run pytest tests/lit_review/ -v

# Run with coverage
uv run pytest tests/lit_review/ --cov=lit_review --cov-report=term-missing

# Exclude integration tests (no API calls)
uv run pytest tests/lit_review/ -m "not integration"
```

## Container Setup (Docker/Podman)

### Using Pre-built Image (Recommended)

```bash
# Pull the latest image
docker pull ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest

# Or with Podman
podman pull ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest

# Run with volume for data persistence
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest \
  --help
```

### Building from Source

```bash
# Build the container
docker build -f Containerfile.lit_review -t lit-review-tool:local .

# Or with Podman
podman build -f Containerfile.lit_review -t lit-review-tool:local .

# Test the build
docker run --rm lit-review-tool:local --version
```

### Container Usage Examples

```bash
# Initialize a review
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  lit-review-tool:local \
  init "My Review" --question "What is the impact?"

# Search for papers
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  lit-review-tool:local \
  search "My Review" --database crossref --keywords "machine learning"

# Export review
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  lit-review-tool:local \
  export "My Review" --format bibtex --output /home/reviewer/data/refs.bib
```

### Container with Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  lit-review:
    image: ghcr.io/stharrold/yuimedi-paper-20250901/lit-review-tool:latest
    volumes:
      - ./review_data:/home/reviewer/data
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - PUBMED_EMAIL=${PUBMED_EMAIL}
      - LIT_REVIEW_DATA_DIR=/home/reviewer/data
    command: ["--help"]
```

Usage:

```bash
# Show help
docker-compose run --rm lit-review --help

# Initialize review
docker-compose run --rm lit-review init "My Review" -q "Question"

# Search
docker-compose run --rm lit-review search "My Review" -d crossref -k "terms"
```

## API Key Setup

### Anthropic API (Optional - for AI features)

1. Create an account at https://console.anthropic.com
2. Generate an API key
3. Set the environment variable:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Or add to `.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
```

**Note**: AI features are optional. The tool will fall back to keyword-based analysis if no key is provided.

### PubMed API (Optional - for enhanced rate limits)

PubMed allows 3 requests/second without an API key, and 10 requests/second with an email address.

Set your email:

```bash
export PUBMED_EMAIL=your.email@example.com
```

Or add to `.env`:

```
PUBMED_EMAIL=your.email@example.com
```

**No API key required** - just an email address for the polite pool.

## Data Storage

### Default Location

By default, reviews are stored in:

- **macOS/Linux**: `~/.lit_review/`
- **Windows**: `%USERPROFILE%\.lit_review\`

### Custom Location

Set `LIT_REVIEW_DATA_DIR` to use a custom location:

```bash
export LIT_REVIEW_DATA_DIR=/path/to/reviews
```

### Data Structure

```
review_data/
├── review_1_title/
│   ├── metadata.json    # Review configuration
│   ├── papers.json      # Paper records
│   └── backups/         # Automatic backups
├── review_2_title/
│   └── ...
└── ...
```

### Backup Strategy

The tool automatically creates backups before overwriting data:

- Backups stored in `review_name/backups/`
- Timestamped filenames: `papers_YYYYMMDD_HHMMSS.json.bak`
- Manually backup: `cp -r ~/.lit_review /path/to/backup`

## Troubleshooting

### uv sync fails

```bash
# Clear cache and retry
uv cache clean
uv sync --frozen

# Check Python version
python --version  # Should be 3.11+
```

### CLI command not found

```bash
# Use uv run prefix
uv run academic-review --help

# Or activate virtual environment
source .venv/bin/activate
academic-review --help
```

### Import errors

```bash
# Ensure dependencies are installed
uv sync

# Check virtual environment
uv run python -c "import lit_review; print(lit_review.__file__)"
```

### Permission errors (Container)

```bash
# Ensure volume has correct permissions
chmod -R 755 review_data/

# Or run with proper user mapping
docker run --rm \
  -v $(pwd)/review_data:/home/reviewer/data \
  --user $(id -u):$(id -g) \
  lit-review-tool:local --help
```

### API rate limiting

```bash
# Set PubMed email for higher rate limit
export PUBMED_EMAIL=your.email@example.com

# Use delays between searches
# (automatically handled by adapters)

# Check adapter logs
uv run academic-review search "Review" -d pubmed -k "terms" --verbose
```

## Development Setup

For contributing to the tool:

### 1. Install Development Dependencies

```bash
uv sync --all-extras
```

### 2. Install Pre-commit Hooks

```bash
uv run pre-commit install
```

### 3. Run Quality Checks

```bash
# Format code
uv run ruff format lit_review/ tests/lit_review/

# Lint
uv run ruff check lit_review/ tests/lit_review/

# Type check
uv run mypy lit_review/

# Security scan
uv run bandit -r lit_review/

# Run all quality gates
python .gemini/skills/quality-enforcer/scripts/run_quality_gates.py
```

### 4. Run Tests with Coverage

```bash
# All tests with coverage
uv run pytest tests/lit_review/ \
  --cov=lit_review \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-fail-under=80

# View HTML coverage report
open htmlcov/index.html
```

## Next Steps

After setup is complete:

1. Read [lit_review_workflow.md](lit_review_workflow.md) for usage examples
2. Try the quick start in [lit_review/README.md](../lit_review/README.md)
3. Check [GEMINI.md](../GEMINI.md) for development guidelines

## Support

- **Issues**: https://github.com/stharrold/yuimedi-paper-20250901/issues
- **Documentation**: See `docs/` directory
- **Main README**: [README.md](../README.md)
