# Documentation Directory

This directory contains supporting materials and version management for research papers related to the YuiQuery healthcare analytics project.

## 📁 Directory Structure

```
docs/
├── paper1/         # YuiQuery NL2SQL Healthcare Whitepaper (primary)
├── paper2/         # Future publications and related research
└── paper3/         # Additional research directions
```

## 🎯 Purpose

The docs directory serves as:
- **Version Management**: Tracking paper evolution and revisions
- **Supporting Materials**: Figures, supplementary research, and notes
- **Multi-Paper Organization**: Coordinating related research outputs
- **Submission Preparation**: Materials formatted for specific publication venues

## 📄 Primary Paper (paper1/)

**Main Document**: [`/paper.md`](../paper.md) (at repository root)

### Focus Areas
- Natural language to SQL in healthcare
- Low healthcare analytics maturity
- Healthcare workforce turnover and institutional memory loss
- Technical barriers in NL2SQL generation

### Status
- **Draft**: COMPLETE
- **Citations**: 111 academic and industry sources
- **Deadline**: September 30, 2025

### Submission Targets
1. **medRxiv** (primary) - Healthcare research preprint server
2. **arXiv** (secondary) - Technical audience for NL2SQL methods
3. **AHIMA Journal** - Peer review for health information management

See [paper1/README.md](paper1/README.md) for detailed information.

## 📂 Directory Contents

### paper1/
Primary whitepaper supporting materials:
- `/research/` - Literature review notes and additional sources
- `/figures/` - Diagrams and visualizations referenced in paper.md
- See [paper1/README.md](paper1/README.md)

### paper2/
Future publication materials:
- Reserved for follow-up research
- Implementation case studies
- Extended validation results

### paper3/
Additional research directions:
- Alternative approaches
- Specialized healthcare applications
- Methodological comparisons

## 🔄 Relationship to Main Paper

The primary research paper lives at the repository root as **`paper.md`** for easy access. This docs/ directory contains:
- **Supporting materials** for the main paper
- **Figures and diagrams** referenced in paper.md
- **Additional research** that didn't fit in the main document
- **Version history** and editorial notes

## 📊 Paper Versions

### Current Version (v1.0)
- Location: `/paper.md`
- Status: Complete draft
- Last updated: 2025-08-10
- Citations: 111 sources

### Version Management
Historical versions are tracked in:
- Git commit history (preferred method)
- `archive/` directory for major milestones
- Individual paper directories for submission-specific versions

## 🎨 Figures and Diagrams

Figures are stored in individual paper subdirectories:

```bash
# View available figures
ls docs/paper1/figures/

# Figures also available in main images/ directory
ls images/
```

Common figure types:
- YuiQuery feature workflows
- System architecture diagrams
- Healthcare analytics maturity models
- Query processing flowcharts

## 📝 Citation Management

Each paper directory may contain:
- `research/` - Additional literature review notes
- Citation exports for reference managers (BibTeX, RIS)
- Supplementary reading lists

Main citations are in [`paper.md`](../paper.md) using format:
- `[A#]` - Academic sources
- `[I#]` - Industry sources

## 🚀 Working with Papers

### Reading the Main Paper
```bash
# Read in terminal
less paper.md

# Or open in editor
open paper.md

# Generate PDF
pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.pdf \
  --template=eisvogel \
  --pdf-engine=xelatex \
  --listings \
  --toc \
  --number-sections
```

### Adding Supporting Materials
```bash
# Add figure to paper1
cp your_figure.png docs/paper1/figures/

# Add research notes
vim docs/paper1/research/your_notes.md

# Update paper1 README
vim docs/paper1/README.md
```

### Creating New Paper Version
```bash
# Create submission-specific version
cp paper.md docs/paper1/paper_medrxiv_submission.md

# Edit for venue requirements
vim docs/paper1/paper_medrxiv_submission.md
```

## 📚 Related Documentation

- [Main Research Paper](../paper.md) - Primary whitepaper document
- [Bibliography](../paper.md#references) - Full citation list in paper.md
- [Images Directory](../images/) - Additional research diagrams
- [CLAUDE.md](../CLAUDE.md) - Project documentation standards

## 🔗 Academic Standards

All papers in this directory follow:
- **Systematic review methodology** (PRISMA guidelines)
- **Evidence-based claims** with citations
- **Healthcare domain** terminology standards
- **Publication readiness** for peer review

## 📈 Future Papers

### Planned Publications
- **Paper 2**: Implementation case studies and ROI analysis
- **Paper 3**: Comparative analysis of NL2SQL approaches
- Additional papers as research expands

### Contribution Guidelines
When preparing new papers:
1. Create new paper directory (`paper4/`, etc.)
2. Add README with paper metadata
3. Organize figures/ and research/ subdirectories
4. Follow citation format from paper.md
5. Maintain academic quality standards

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

---

*Supporting materials for YuiQuery healthcare analytics research publications*
