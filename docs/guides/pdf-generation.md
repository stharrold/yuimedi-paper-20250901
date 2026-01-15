# PDF Generation and Build Pipeline

This document describes how to generate publication-ready PDFs from `paper.md`.

**Current Recommendation (Jan 2026):** Use **Local Build** with `tectonic` on macOS due to persistent Podman `applehv` socket instability.

## Quick Start

### Option 1: Local Build (Recommended for macOS)

Fastest and most reliable method.

```bash
# 1. Install dependencies
brew install pandoc tectonic

# 2. Build Paper (PDF, HTML, DOCX)
./scripts/build_paper.sh --format all
```

### Option 2: Container Build (Linux / CI)

Standard method for CI/CD parity. Use if local build fails.

```bash
# Smart Reset Build (Fixes port/name conflicts)
podman rm -f -a
podman volume create yuimedi_venv_cache
podman build -t yuimedi-paper:latest -f Containerfile .

# Run with explicit volume mapping
podman run --rm \
  -v "$PWD:/app:Z" \
  -v yuimedi_venv_cache:/app/.venv \
  -w /app \
  yuimedi-paper:latest \
  ./scripts/build_paper.sh --format all
```

## Troubleshooting Podman on macOS

### Error: "dial tcp 127.0.0.1:xxxxx: connect: connection refused"

**Symptoms:**
- `podman machine start` reports success ("Machine started successfully").
- Immediately running `podman info` or `podman run` fails with "connection refused".
- SSH access (`podman machine ssh`) fails with "vm is not running".

**Root Cause:**
A known instability with the `applehv` virtualization provider on macOS (Apple Silicon). The QEMU process starts but crashes immediately or fails to bind the API forwarding socket to the expected port, causing the client to lose connection.

**Fix Attempts (that often fail):**
- `podman machine rm -f` / `init` (Issue persists on fresh machines)
- Deep cleaning `~/.local/share/containers`
- Reinstalling via Brew

**Official Solution:**
Use the **Local Build** strategy (Option 1 above). We have patched `scripts/build_paper.sh` to support `tectonic` as a fallback PDF engine specifically to bypass this virtualization layer failure.

## Installation Details

### macOS Requirements

```bash
# Core tool
brew install pandoc

# PDF Engine (Choose one)
brew install tectonic             # Modern, self-contained (Recommended)
# OR
brew install --cask mactex-no-gui # Traditional, large download
```

### Script Architecture

The build script (`scripts/build_paper.sh`) intelligently selects the PDF engine:
1.  Checks for `xelatex` (container standard).
2.  If missing, checks for `tectonic` (local fallback).
3.  Configures `pandoc` arguments accordingly.

### Metadata Configuration

The `metadata.yaml` file has been optimized for compatibility:
- Specific font requirements ("DejaVu Serif") are commented out to allow `tectonic` to use its default Latin Modern fonts.
- This prevents `Package fontspec Error` during local builds.

## Output Files

| Format | Output File | Engine |
|--------|-------------|--------|
| PDF | `paper.pdf` | `tectonic` or `xelatex` |
| HTML | `paper.html` | `pandoc` native |
| DOCX | `paper.docx` | `pandoc` native |
| LaTeX | `paper.tex` | Intermediate source |
