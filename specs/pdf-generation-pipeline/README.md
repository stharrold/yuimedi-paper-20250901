# PDF Generation Pipeline

**Feature:** Automated MD-to-LaTeX-to-PDF pipeline
**GitHub Issue:** #264
**Status:** Specification Complete

## Overview

This feature implements an automated pipeline for converting `paper.md` to publication-ready PDF using Pandoc with XeLaTeX and the Eisvogel academic template.

## Components

| Component | Description | Status |
|-----------|-------------|--------|
| `scripts/build_paper.sh` | Build script with dependency management | Planned |
| `metadata.yaml` | Document metadata for pandoc | Planned |
| `Containerfile` | Container with texlive packages | Planned |
| `.github/workflows/pdf-generation.yml` | CI workflow | Planned |
| `docs/pdf-generation.md` | User documentation | Planned |

## Quick Start

### Local (after implementation)

```bash
# Generate PDF
./scripts/build_paper.sh

# Generate all formats
./scripts/build_paper.sh --format all
```

### Container

```bash
podman-compose run --rm dev ./scripts/build_paper.sh
```

## Documentation

- **[spec.md](spec.md)** - Technical specification
- **[plan.md](plan.md)** - Implementation tasks
- **[planning/pdf-generation-pipeline/](../../planning/pdf-generation-pipeline/README.md)** - BMAD planning

## Task Summary

10 tasks across 5 phases:

1. **Build Script** (T001-T002): Core build script and metadata
2. **Container** (T003-T004): Containerfile updates and testing
3. **CI/CD** (T005-T006): GitHub Actions workflow
4. **Documentation** (T007-T008): User docs and CLAUDE.md updates
5. **Quality** (T009-T010): Validation and end-to-end testing

## Dependencies

- pandoc >= 2.19
- texlive-xetex
- Eisvogel template >= 2.0
