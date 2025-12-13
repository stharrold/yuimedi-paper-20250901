---
type: claude-context
directory: specs/pdf-generation-pipeline
purpose: SpecKit specifications for PDF generation pipeline feature
parent: ../CLAUDE.md
sibling_readme: README.md
children: []
related_skills:
  - workflow-orchestrator
  - quality-enforcer
---

# Claude Code Context: specs/pdf-generation-pipeline

## Purpose

SpecKit specifications for feature 'pdf-generation-pipeline' - automated MD-to-LaTeX-to-PDF generation.

## Directory Structure

```
specs/pdf-generation-pipeline/
├── spec.md        # Detailed technical specification
├── plan.md        # Implementation task breakdown
├── CLAUDE.md      # This file
├── README.md      # Human-readable overview
└── ARCHIVED/      # Deprecated specs
```

## Files in This Directory

- **spec.md** - Complete technical specification with pipeline architecture
- **plan.md** - Task breakdown (T001-T010) with acceptance criteria

## Usage

When implementing this feature:
1. Read spec.md for technical details (pandoc options, container setup)
2. Follow plan.md task order (build script → container → CI → docs)
3. Mark tasks complete as you finish each one
4. Refer to planning/pdf-generation-pipeline/ for BMAD context

## Key Implementation Notes

### Build Script (`scripts/build_paper.sh`)
- Uses pandoc with XeLaTeX engine
- Eisvogel template for academic formatting
- Supports --format flag: pdf (default), html, docx, all
- Auto-installs Eisvogel template on first run

### Container
- Add ~450MB for texlive packages
- Test with: `podman-compose run --rm dev ./scripts/build_paper.sh`

### CI Workflow
- Triggers on paper.md changes
- Uploads PDF as artifact
- Attaches to releases

## Related Documentation

- **[README.md](README.md)** - Human-readable documentation
- **[planning/pdf-generation-pipeline/](../../planning/pdf-generation-pipeline/CLAUDE.md)** - BMAD Planning

## Related Skills

- workflow-orchestrator
- quality-enforcer
