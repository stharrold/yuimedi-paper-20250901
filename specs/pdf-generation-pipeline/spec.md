# Specification: PDF Generation Pipeline

**Type:** infrastructure
**Slug:** pdf-generation-pipeline
**Date:** 2025-12-11
**Author:** stharrold
**GitHub Issue:** #264

## Overview

This specification defines the implementation of an automated MD-to-LaTeX-to-PDF pipeline for generating publication-ready documents from `paper.md`. The pipeline uses Pandoc with XeLaTeX and the Eisvogel template to produce academically-formatted PDFs.

## Implementation Context

**BMAD Planning:** See `planning/pdf-generation-pipeline/` for complete requirements and architecture.

**Scope:**
- Build script (`scripts/build_paper.sh`) for local PDF generation
- Container updates for pandoc/texlive packages
- CI/CD workflow for automated PDF generation on paper.md changes
- Documentation for setup and troubleshooting

## Technical Architecture

### Pipeline Flow

```
paper.md
    │
    ▼
┌──────────────────────────────────────┐
│  scripts/build_paper.sh              │
│  ┌────────────────────────────────┐  │
│  │ 1. Check dependencies          │  │
│  │    (pandoc, xelatex, eisvogel) │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │ 2. Run pandoc conversion       │  │
│  │    --pdf-engine=xelatex        │  │
│  │    --template=eisvogel         │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │ 3. Validate output             │  │
│  │    (file exists, > 0 bytes)    │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
    │
    ▼
paper.pdf
```

### Component Design

#### 1. Build Script (`scripts/build_paper.sh`)

**Purpose:** Wrapper script for pandoc conversion with dependency management.

**Interface:**
```bash
# Generate PDF (default)
./scripts/build_paper.sh

# Generate specific format
./scripts/build_paper.sh --format pdf
./scripts/build_paper.sh --format html
./scripts/build_paper.sh --format docx
./scripts/build_paper.sh --format all

# Show help
./scripts/build_paper.sh --help
```

**Features:**
- Auto-detect and validate dependencies (pandoc, xelatex)
- Auto-install Eisvogel template on first run
- Support multiple output formats (PDF, HTML, DOCX)
- Graceful error handling with informative messages
- Exit codes: 0 (success), 1 (dependency missing), 2 (conversion failed)

**Pandoc Command:**
```bash
pandoc paper.md \
  --from=markdown+smart \
  --to=pdf \
  --pdf-engine=xelatex \
  --template=eisvogel \
  --listings \
  --number-sections \
  --toc \
  --toc-depth=3 \
  --metadata-file=metadata.yaml \
  --output=paper.pdf
```

#### 2. Container Updates (`Containerfile`)

**Additions:**
```dockerfile
# PDF generation dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    texlive-xetex \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    lmodern \
    && rm -rf /var/lib/apt/lists/*

# Install Eisvogel template
RUN mkdir -p /root/.local/share/pandoc/templates && \
    curl -L https://github.com/Wandmalfarbe/pandoc-latex-template/releases/latest/download/Eisvogel.tar.gz | \
    tar xz -C /root/.local/share/pandoc/templates/
```

**Size Considerations:**
- texlive-xetex: ~200MB
- texlive-latex-extra: ~150MB
- texlive-fonts-*: ~100MB
- Total addition: ~450MB (within 500MB budget)

#### 3. CI Workflow (`.github/workflows/pdf-generation.yml`)

**Triggers:**
```yaml
on:
  push:
    paths:
      - 'paper.md'
      - 'metadata.yaml'
      - 'scripts/build_paper.sh'
    branches:
      - main
      - develop
      - 'release/*'
  pull_request:
    paths:
      - 'paper.md'
```

**Jobs:**
1. **build-pdf**: Generate PDF using container
2. **upload-artifact**: Store PDF as workflow artifact
3. **attach-to-release**: On tagged releases, attach PDF to GitHub release

**Artifact Retention:** 90 days for workflow artifacts

#### 4. Metadata File (`metadata.yaml`)

```yaml
title: "YuiQuery: A Conversational AI Platform for Healthcare Analytics"
author:
  - name: Samuel Harrold
    affiliation: Independent Researcher
date: 2025-12-11
lang: en-US
documentclass: article
papersize: letter
geometry: margin=1in
fontsize: 11pt
linestretch: 1.5
toc: true
toc-depth: 3
numbersections: true
colorlinks: true
linkcolor: blue
urlcolor: blue
citecolor: green
```

## Acceptance Criteria

### FR-001: Build Script
- [x] `./scripts/build_paper.sh` produces PDF with Eisvogel template
- [x] `./scripts/build_paper.sh --format html` produces standalone HTML
- [x] `./scripts/build_paper.sh --format all` produces PDF, HTML, DOCX
- [x] Script fails gracefully if pandoc/xelatex missing
- [x] Script auto-installs Eisvogel template on first run

### FR-002: Container Update
- [x] `podman build -t yuimedi-paper .` succeeds
- [x] `podman run --rm yuimedi-paper pandoc --version` works
- [x] `podman run --rm yuimedi-paper xelatex --version` works
- [x] Container size increase is reasonable (<500MB additional)

### FR-003: CI Workflow
- [x] Workflow triggers on paper.md changes
- [x] PDF artifact uploaded successfully
- [x] Release gets PDF attachment
- [x] Workflow completes in <10 minutes

### FR-004: Documentation
- [x] Instructions work on macOS and Ubuntu
- [x] Container usage documented
- [x] Troubleshooting covers common errors

## Non-Functional Requirements

### Performance
- PDF generation completes in <5 minutes for ~30 page paper
- Container build time <15 minutes with caching

### Compatibility
- macOS: Requires MacTeX or BasicTeX + pandoc (via Homebrew)
- Ubuntu: texlive-xetex + pandoc packages
- Container: Fully self-contained, no host dependencies

### Error Handling

| Error | Detection | User Message |
|-------|-----------|--------------|
| pandoc missing | `which pandoc` | "pandoc not found. Install via: brew install pandoc" |
| xelatex missing | `which xelatex` | "xelatex not found. Install MacTeX or texlive-xetex" |
| Eisvogel missing | template check | "Installing Eisvogel template..." |
| LaTeX error | exit code | Show pandoc stderr, suggest checking paper.md syntax |

## Testing Strategy

### Local Testing
```bash
# Test build script
./scripts/build_paper.sh
ls -la paper.pdf  # Should exist, > 0 bytes

# Test all formats
./scripts/build_paper.sh --format all
ls -la paper.pdf paper.html paper.docx
```

### Container Testing
```bash
# Build container
podman-compose build

# Test PDF generation in container
podman-compose run --rm dev ./scripts/build_paper.sh
```

### CI Testing
- PR to develop branch triggers workflow
- Verify artifact upload succeeds
- Check PDF opens correctly

## Dependencies

### External Tools
- **pandoc** >= 2.19 (for Markdown conversion)
- **xelatex** (for PDF rendering with Unicode support)
- **Eisvogel template** >= 2.0 (academic LaTeX template)

### Repository Files
- `paper.md` (source document)
- `metadata.yaml` (document metadata for pandoc)

## Migration Strategy

No database migrations required. This is a new capability that doesn't affect existing functionality.

## Security Considerations

- No secrets required for PDF generation
- CI workflow uses read-only repository access
- Container builds use pinned base images
- No network access required during PDF generation

## Rollback Plan

If PDF generation fails in CI:
1. Workflow failure doesn't block PR merge (non-blocking)
2. Manual PDF generation remains available locally
3. Previous PDF artifacts retained for 90 days

## References

- [Pandoc User's Guide](https://pandoc.org/MANUAL.html)
- [Eisvogel Template](https://github.com/Wandmalfarbe/pandoc-latex-template)
- [XeLaTeX Documentation](https://tug.org/xetex/)
- `planning/pdf-generation-pipeline/requirements.md` - Business requirements
- `planning/pdf-generation-pipeline/architecture.md` - Architecture notes
