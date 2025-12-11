# Implementation Plan: PDF Generation Pipeline

**Type:** infrastructure
**Slug:** pdf-generation-pipeline
**Date:** 2025-12-11
**GitHub Issue:** #264

## Overview

Implement an automated MD-to-LaTeX-to-PDF pipeline for generating publication-ready documents from `paper.md`. The pipeline uses Pandoc with XeLaTeX and the Eisvogel template.

**Key tools:** pandoc, xelatex, Eisvogel template, GitHub Actions

## Task Breakdown

### Phase 1: Build Script

#### Task T001: Create build_paper.sh script

**Priority:** High

**Files:**
- `scripts/build_paper.sh` (new)

**Description:**
Create the main build script that wraps pandoc for PDF generation with dependency checking and error handling.

**Steps:**
1. Create `scripts/build_paper.sh` with shebang and strict mode
2. Implement dependency checks (pandoc, xelatex)
3. Implement Eisvogel template auto-installation
4. Implement pandoc conversion with XeLaTeX engine
5. Add --format flag support (pdf, html, docx, all)
6. Add --help flag with usage documentation
7. Set appropriate exit codes

**Acceptance Criteria:**
- [ ] `./scripts/build_paper.sh` generates paper.pdf
- [ ] `./scripts/build_paper.sh --format html` generates paper.html
- [ ] `./scripts/build_paper.sh --format docx` generates paper.docx
- [ ] `./scripts/build_paper.sh --format all` generates all formats
- [ ] Script exits with code 1 if pandoc missing
- [ ] Script exits with code 1 if xelatex missing
- [ ] Script auto-installs Eisvogel if missing

**Verification:**
```bash
./scripts/build_paper.sh --help
./scripts/build_paper.sh
ls -la paper.pdf
```

**Dependencies:** None

---

#### Task T002: Create metadata.yaml for pandoc

**Priority:** High

**Files:**
- `metadata.yaml` (new)

**Description:**
Create YAML metadata file for pandoc with document properties (title, author, formatting options).

**Steps:**
1. Create `metadata.yaml` with document title and author
2. Add formatting options (fontsize, margins, line spacing)
3. Add table of contents configuration
4. Add color link settings
5. Test with build script

**Acceptance Criteria:**
- [ ] `metadata.yaml` exists with all required fields
- [ ] PDF output includes title and author
- [ ] PDF has table of contents
- [ ] PDF has numbered sections

**Verification:**
```bash
cat metadata.yaml
./scripts/build_paper.sh
# Visually verify PDF formatting
```

**Dependencies:** T001

---

### Phase 2: Container Updates

#### Task T003: Update Containerfile with PDF dependencies

**Priority:** High

**Files:**
- `Containerfile`

**Description:**
Add pandoc and texlive packages to the development container for PDF generation support.

**Steps:**
1. Add apt-get install commands for pandoc, texlive-xetex, texlive-latex-extra
2. Add texlive-fonts-recommended and texlive-fonts-extra
3. Add Eisvogel template installation
4. Clean up apt cache to minimize image size
5. Test container build

**Acceptance Criteria:**
- [ ] `podman-compose build` succeeds
- [ ] `podman-compose run --rm dev pandoc --version` works
- [ ] `podman-compose run --rm dev xelatex --version` works
- [ ] Container size increase < 500MB

**Verification:**
```bash
podman-compose build
podman-compose run --rm dev pandoc --version
podman-compose run --rm dev xelatex --version
podman images | grep yuimedi
```

**Dependencies:** T001

---

#### Task T004: Test PDF generation in container

**Priority:** High

**Files:**
- None (testing only)

**Description:**
Verify that PDF generation works correctly inside the container environment.

**Steps:**
1. Build container with new dependencies
2. Run build script inside container
3. Verify PDF output
4. Test all output formats (pdf, html, docx)
5. Verify output files can be accessed from host

**Acceptance Criteria:**
- [ ] `podman-compose run --rm dev ./scripts/build_paper.sh` succeeds
- [ ] PDF file accessible on host after container run
- [ ] All formats work in container

**Verification:**
```bash
podman-compose run --rm dev ./scripts/build_paper.sh --format all
ls -la paper.pdf paper.html paper.docx
```

**Dependencies:** T003

---

### Phase 3: CI/CD Workflow

#### Task T005: Create GitHub Actions workflow

**Priority:** High

**Files:**
- `.github/workflows/pdf-generation.yml` (new)

**Description:**
Create CI workflow that automatically generates PDFs when paper.md changes.

**Steps:**
1. Create workflow file with appropriate triggers (paper.md changes)
2. Add job to build container and generate PDF
3. Configure artifact upload for PDF
4. Add release attachment for tagged releases
5. Set workflow timeout to 15 minutes

**Acceptance Criteria:**
- [ ] Workflow triggers on paper.md push to main/develop
- [ ] Workflow triggers on PR with paper.md changes
- [ ] PDF artifact uploaded successfully
- [ ] Workflow completes in < 10 minutes

**Verification:**
```bash
# Push change to paper.md
# Verify workflow runs in GitHub Actions
# Download artifact and verify PDF
```

**Dependencies:** T004

---

#### Task T006: Add release attachment logic

**Priority:** Medium

**Files:**
- `.github/workflows/pdf-generation.yml`

**Description:**
Extend the workflow to attach PDFs to GitHub releases.

**Steps:**
1. Add release trigger to workflow
2. Add job to upload PDF as release asset
3. Use gh CLI or GitHub API for upload
4. Test with a test release

**Acceptance Criteria:**
- [ ] PDF attached to release automatically
- [ ] Release asset named appropriately (paper-v{version}.pdf)

**Verification:**
```bash
# Create a test tag/release
# Verify PDF appears in release assets
```

**Dependencies:** T005

---

### Phase 4: Documentation

#### Task T007: Create PDF generation documentation

**Priority:** Medium

**Files:**
- `docs/pdf-generation.md` (new)

**Description:**
Create documentation for setting up and using the PDF generation pipeline.

**Steps:**
1. Document local setup for macOS (Homebrew)
2. Document local setup for Ubuntu
3. Document container-based usage
4. Add troubleshooting section for common errors
5. Add examples for each output format

**Acceptance Criteria:**
- [ ] macOS setup instructions verified
- [ ] Ubuntu setup instructions verified
- [ ] Container usage documented
- [ ] Troubleshooting covers: missing pandoc, missing xelatex, LaTeX errors

**Verification:**
```bash
# Follow documentation steps on fresh system
# Verify all commands work
```

**Dependencies:** T004

---

#### Task T008: Update CLAUDE.md with PDF commands

**Priority:** Medium

**Files:**
- `CLAUDE.md`

**Description:**
Add PDF generation commands to the Essential Commands section of CLAUDE.md.

**Steps:**
1. Add PDF generation commands to Essential Commands
2. Document container-based PDF generation
3. Reference docs/pdf-generation.md for details

**Acceptance Criteria:**
- [ ] PDF commands documented in CLAUDE.md
- [ ] Commands are accurate and tested

**Verification:**
```bash
# Review CLAUDE.md
# Verify commands work as documented
```

**Dependencies:** T007

---

### Phase 5: Quality Assurance

#### Task T009: Run full validation suite

**Priority:** High

**Files:**
- All project files

**Description:**
Run all validation and quality checks to ensure the feature doesn't break existing functionality.

**Steps:**
1. Run documentation validation
2. Run reference validation
3. Run linting (ruff)
4. Run type checking (mypy)
5. Run all tests
6. Run quality gates

**Acceptance Criteria:**
- [ ] `./validate_documentation.sh` passes
- [ ] `python scripts/validate_references.py --all` passes
- [ ] `uv run ruff format . && uv run ruff check --fix .` clean
- [ ] `uv run mypy scripts/` clean
- [ ] `uv run pytest` passes

**Verification:**
```bash
./validate_documentation.sh
python scripts/validate_references.py --all
uv run ruff format . && uv run ruff check --fix .
uv run mypy scripts/
uv run pytest
```

**Dependencies:** T008

---

#### Task T010: Test end-to-end PDF generation

**Priority:** High

**Files:**
- None (testing only)

**Description:**
Perform end-to-end testing of the complete PDF generation pipeline.

**Steps:**
1. Test local PDF generation
2. Test container PDF generation
3. Simulate CI workflow locally
4. Verify PDF quality (formatting, fonts, images)
5. Verify PDF file size is reasonable

**Acceptance Criteria:**
- [ ] PDF renders correctly with all sections
- [ ] References section properly formatted
- [ ] Tables and figures display correctly
- [ ] File size < 5MB

**Verification:**
```bash
./scripts/build_paper.sh
open paper.pdf  # macOS
# or: xdg-open paper.pdf  # Linux
```

**Dependencies:** T009

---

## Task Summary

| Task | Description | Priority | Dependencies |
|------|-------------|----------|--------------|
| T001 | Create build_paper.sh script | High | None |
| T002 | Create metadata.yaml | High | T001 |
| T003 | Update Containerfile | High | T001 |
| T004 | Test PDF in container | High | T003 |
| T005 | Create CI workflow | High | T004 |
| T006 | Add release attachment | Medium | T005 |
| T007 | Create documentation | Medium | T004 |
| T008 | Update CLAUDE.md | Medium | T007 |
| T009 | Run validation suite | High | T008 |
| T010 | End-to-end testing | High | T009 |

## Task Dependencies Graph

```
T001 ─┬─> T002 ─────────────────────────────────────┐
      │                                              │
      └─> T003 ─> T004 ─┬─> T005 ─> T006 ─────────┐ │
                        │                          │ │
                        └─> T007 ─> T008 ─> T009 ─┴─┴─> T010
```

## Parallel Work Opportunities

- **[P] T002, T003** can run in parallel after T001
- **[P] T005, T007** can run in parallel after T004

## Quality Checklist

Before considering this feature complete:

- [ ] All 10 tasks marked as complete
- [ ] `./scripts/build_paper.sh` generates valid PDF
- [ ] Container PDF generation works
- [ ] CI workflow triggers and succeeds
- [ ] Documentation accurate and tested
- [ ] All validation passes
- [ ] PDF quality verified

## Risk Assessment

### High Risk Tasks

- **T003**: Container size increase may exceed budget
  - Mitigation: Use `--no-install-recommends`, consider texlive-base instead of texlive-full

- **T005**: CI workflow may timeout on large documents
  - Mitigation: Cache container layers, set appropriate timeout

### Medium Risk Tasks

- **T001**: Eisvogel template installation may fail on different platforms
  - Mitigation: Document manual installation fallback

## Notes

### Pandoc Options Rationale

- `--pdf-engine=xelatex`: Required for Unicode support and modern fonts
- `--template=eisvogel`: Academic formatting with clean design
- `--listings`: Code block formatting with syntax highlighting
- `--number-sections`: Automatic section numbering
- `--toc`: Auto-generated table of contents

### Local Installation Commands

**macOS:**
```bash
brew install pandoc
brew install --cask mactex-no-gui
# or: brew install basictex
```

**Ubuntu:**
```bash
sudo apt-get install pandoc texlive-xetex texlive-latex-extra
```

### Container Command

```bash
podman-compose run --rm dev ./scripts/build_paper.sh
```
