# PDF Generation

This document describes how to generate publication-ready PDFs from `paper.md` using the automated build pipeline.

## Quick Start

### Container (Recommended)

```bash
# Build container (first time or after Containerfile changes)
podman-compose build

# Generate PDF
podman-compose run --rm dev ./scripts/build_paper.sh

# Generate all formats (PDF, HTML, DOCX)
podman-compose run --rm dev ./scripts/build_paper.sh --format all
```

### Local

```bash
# Generate PDF (requires local pandoc + texlive installation)
./scripts/build_paper.sh

# Generate specific format
./scripts/build_paper.sh --format html
./scripts/build_paper.sh --format docx
```

## Installation

### macOS

```bash
# Install pandoc
brew install pandoc

# Install TeX Live (choose one)
brew install --cask mactex-no-gui   # Full installation (~4GB)
# or
brew install basictex               # Minimal installation (~200MB)

# If using basictex, install additional packages
sudo tlmgr update --self
sudo tlmgr install collection-fontsrecommended
sudo tlmgr install collection-latexextra
sudo tlmgr install xetex
```

### Ubuntu/Debian

```bash
# Install pandoc and TeX Live
sudo apt-get update
sudo apt-get install -y pandoc texlive-xetex texlive-latex-extra \
    texlive-fonts-recommended texlive-fonts-extra lmodern fonts-dejavu
```

### Eisvogel Template

The build script automatically installs the [Eisvogel template](https://github.com/Wandmalfarbe/pandoc-latex-template) on first run. For manual installation:

```bash
# Create templates directory
mkdir -p ~/.local/share/pandoc/templates

# Download and extract Eisvogel
curl -sL https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/Eisvogel.tar.gz | \
    tar xz -C ~/.local/share/pandoc/templates --strip-components=1
```

## Usage

### Build Script Options

```bash
./scripts/build_paper.sh [--format FORMAT] [--help]

Options:
  --format FORMAT  Output format: pdf (default), html, docx, all
  --help           Show help message

Exit codes:
  0 - Success
  1 - Missing dependency (pandoc, xelatex)
  2 - Conversion failed
```

### Output Files

| Format | Output File | Size (typical) |
|--------|-------------|----------------|
| PDF | `paper.pdf` | ~170KB |
| HTML | `paper.html` | ~100KB |
| DOCX | `paper.docx` | ~35KB |

### Metadata Configuration

Document properties are configured in `metadata.yaml`:

```yaml
# Key settings
title: "Document Title"
author:
  - name: Author Name
    affiliation: Institution
fontsize: 11pt
linestretch: 1.5
toc: true
numbersections: true
```

See `metadata.yaml` for all available options.

## CI/CD Integration

### Automatic PDF Generation

The GitHub Actions workflow (`.github/workflows/pdf-generation.yml`) automatically generates PDFs when:
- `paper.md` is pushed to `main` or `develop`
- A pull request modifies `paper.md`
- A release is published

### Release Attachments

When a release is published:
1. PDF is generated automatically
2. PDF is attached to the release as `yuiquery-paper-v{version}.pdf`
3. HTML is also attached if available

### Workflow Artifacts

PDF artifacts are available for download from the GitHub Actions workflow page for 90 days.

## Troubleshooting

### "pandoc not found"

**Cause:** Pandoc is not installed or not in PATH.

**Solution:**
```bash
# macOS
brew install pandoc

# Ubuntu
sudo apt-get install pandoc

# Verify installation
pandoc --version
```

### "xelatex not found"

**Cause:** TeX Live is not installed or xelatex is not in PATH.

**Solution:**
```bash
# macOS
brew install --cask mactex-no-gui
# Restart terminal or run: eval "$(/usr/libexec/path_helper)"

# Ubuntu
sudo apt-get install texlive-xetex

# Verify installation
xelatex --version
```

### "Template eisvogel not found"

**Cause:** Eisvogel template is not installed.

**Solution:**
```bash
# The build script auto-installs Eisvogel, but for manual installation:
mkdir -p ~/.local/share/pandoc/templates
curl -sL https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/Eisvogel.tar.gz | \
    tar xz -C ~/.local/share/pandoc/templates --strip-components=1
```

### LaTeX Errors

**Cause:** Missing LaTeX packages or syntax errors in paper.md.

**Solutions:**
1. Check pandoc output for specific missing package names
2. Install missing packages: `sudo tlmgr install <package-name>`
3. Check paper.md for invalid LaTeX in math blocks

### Container Build Failures

**Cause:** Network issues or disk space problems.

**Solutions:**
1. Retry the build: `podman-compose build --no-cache`
2. Check disk space: `df -h`
3. Clean up old images: `podman system prune`

### PDF Quality Issues

**Problem:** Fonts look wrong or characters are missing.

**Solution:** Ensure DejaVu fonts are installed:
```bash
# Ubuntu
sudo apt-get install fonts-dejavu

# macOS (usually pre-installed)
brew install --cask font-dejavu
```

## Architecture

### Pipeline Flow

```
paper.md + metadata.yaml
         │
         ▼
   ┌─────────────────────────────────────┐
   │     scripts/build_paper.sh          │
   │                                     │
   │  1. Check dependencies              │
   │  2. Install Eisvogel (if needed)    │
   │  3. Run pandoc with xelatex engine  │
   │  4. Validate output                 │
   └─────────────────────────────────────┘
         │
         ▼
    paper.pdf / paper.html / paper.docx
```

### Pandoc Options

The build script uses these pandoc options for PDF generation:

| Option | Purpose |
|--------|---------|
| `--pdf-engine=xelatex` | Unicode support, modern fonts |
| `--template=eisvogel` | Academic formatting |
| `--listings` | Code syntax highlighting |
| `--number-sections` | Automatic section numbering |
| `--toc` | Table of contents |
| `--toc-depth=3` | TOC includes up to h3 headings |

## References

- [Pandoc User's Guide](https://pandoc.org/MANUAL.html)
- [Eisvogel Template](https://github.com/Wandmalfarbe/pandoc-latex-template)
- [XeLaTeX Documentation](https://tug.org/xetex/)
- [TeX Live](https://tug.org/texlive/)
