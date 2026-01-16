# YuiQuery Healthcare Analytics Research

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Research whitepaper on natural language to SQL in healthcare - a comprehensive analysis of conversational AI platforms for healthcare analytics addressing low analytics maturity, workforce turnover, and technical barriers in natural language query processing.

## 📄 Research Documents

**[Main Research Paper](paper.md)** - Academic research paper on YuiQuery healthcare analytics with 108 verified citations

## 🚀 Quick Access

```bash
# Clone repository
git clone https://github.com/yourusername/yuimedi-paper-20250901.git
cd yuimedi-paper-20250901

# View main research document
open paper.md

# Setup development environment
uv sync
./validate_documentation.sh
```

## 📋 Project Overview

This repository contains research documentation for YuiQuery, a conversational AI platform for healthcare analytics that addresses three key challenges:

1. **Low Healthcare Analytics Maturity**: Enabling non-technical healthcare professionals to perform complex data analysis
2. **Healthcare Workforce Turnover**: Preserving institutional memory and analytical capabilities
3. **Technical Barriers**: Bridging the gap between natural language queries and SQL database operations

## 🏗️ Repository Structure

```
.
├── paper.md                    # Main research document (comprehensive whitepaper)
├── README.md                   # Project overview and quick start guide
├── GEMINI.md                   # AI assistant instructions and project context
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # Apache 2.0 (code) / CC BY 4.0 (research content)
│
├── project-management/         # Project management documentation
│   ├── risks/                  # Risk assessment and mitigation
│   ├── roles/                  # Team roles and responsibilities
│   ├── budget/                 # Budget tracking
│   └── compliance/             # Compliance requirements
├── project-management.md       # Project management overview
│
├── .gemini-state/             # Workflow state tracking (AgentDB)
│
├── scripts/                    # Validation and build scripts
│   ├── validate_references.py # Reference validation + URL checks
│   ├── build_paper.sh         # PDF/HTML/DOCX generation
│   └── README.md              # Scripts documentation
│
├── images/                     # Research diagrams and YuiQuery feature screenshots
├── docs/                       # Additional documentation (paper versions)
├── lit_review/                 # Literature review workflow package (Python)
├── src/                        # Source code for analysis and algorithms
├── config/                     # Configuration files
├── compliance/                 # IRB and compliance documentation
├── tools/                      # Workflow utilities
└── ARCHIVED/                   # Historical files and backups
```

## 📖 Research Focus Areas

### Core Research Topics
- **Natural Language Processing** in healthcare contexts
- **SQL Generation** from conversational queries
- **Healthcare Analytics** platform design
- **Institutional Memory** preservation systems
- **Workforce Development** in healthcare analytics

### Key Contributions
- Systematic review of natural language analytics in healthcare
- Comprehensive bibliography of academic and industry sources
- Analysis of technical barriers in healthcare data access
- Framework for conversational AI in clinical settings

## 🛠️ Development Setup

### Prerequisites

- **UV Package Manager** (recommended): Fast Python package management
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Git**: Version control
- **GitHub CLI** (optional): For PR management
  ```bash
  brew install gh  # macOS
  ```

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/yuimedi-paper-20250901.git
cd yuimedi-paper-20250901

# Setup UV environment (automatic .venv creation)
uv sync

# Run validation tests
./validate_documentation.sh

# Verify setup
uv run python --version
```

### Development Workflow

```bash
# Format code (Ruff - Black-compatible, 10-100x faster)
uv run ruff format .

# Lint code (replaces flake8, isort, and more)
uv run ruff check .

# Type checking
uv run mypy scripts/

# Run validation
./validate_documentation.sh
```

### Containerized Build (Recommended)

To avoid local environment issues and ensure consistency, use the "Smart Reset" Podman sequence:

```bash
# 1. Clear old containers (fixes port/name conflicts)
podman rm -f -a

# 2. Ensure venv volume exists (preserves dependencies)
podman volume create yuimedi_venv_cache

# 3. Build image
podman build -t yuimedi-paper:latest -f Containerfile .

# 4. Generate Paper (PDF/HTML/DOCX)
podman run --rm \
  -v "$PWD:/app:Z" \
  -v yuimedi_venv_cache:/app/.venv \
  -w /app \
  yuimedi-paper:latest \
  ./scripts/build_paper.sh --format all
```

### Workflow Utilities

```bash
# Archive management
uv run python tools/workflow-utilities/archive_manager.py list

# Directory structure validation
uv run python tools/workflow-utilities/directory_structure.py docs/

# Version consistency checking
uv run python tools/workflow-utilities/validate_versions.py
```

## 🤝 Contributing

### Academic Collaboration

```bash
# Fork and clone
git clone https://github.com/yourusername/yuimedi-paper-20250901.git
cd yuimedi-paper-20250901

# Setup development environment
uv sync

# Create research branch
git checkout -b research/your-contribution

# Review existing literature
open 20250810T235500Z_YuiQuery-Bibliography.md
```

### Contribution Guidelines

1. **Research Standards**
   - Follow academic citation formats
   - Use evidence-based analysis
   - Maintain scholarly tone
   - Reference peer-reviewed sources

2. **Documentation Standards**
   - Use Markdown for all documents
   - Include proper citations and references
   - Maintain consistent formatting
   - Update bibliography for new sources
   - Run `./validate_documentation.sh` before committing

3. **Review Process**
   - Submit pull requests with detailed descriptions
   - Include rationale for research additions
   - Ensure consistency with existing analysis
   - Request review from research team

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📊 Research Methodology

This research employs:

| Method | Application | Sources |
|--------|-------------|---------|
| Narrative Review | Literature analysis | Academic databases |
| Industry Analysis | Technology assessment | Vendor documentation |
| Case Studies | Implementation examples | Healthcare organizations |
| Technical Analysis | Architecture evaluation | Platform specifications |

## 📝 License

**Dual Licensed:**
- **Research Content** (`*.md` documents): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Code & Scripts** (`scripts/`, `lit_review/`): [Apache 2.0](https://opensource.org/licenses/Apache-2.0)

This licensing approach promotes open access to healthcare research while ensuring proper attribution for academic contributions.

## 🙏 Acknowledgments

- Healthcare analytics professionals who provided domain expertise
- Academic institutions supporting natural language processing research
- Open source community for tools and frameworks
- Healthcare organizations sharing implementation insights

## 📮 Contact

**Research Team**: YuiQuery Healthcare Analytics Project
**Repository**: [https://github.com/yourusername/yuimedi-paper-20250901](https://github.com/yourusername/yuimedi-paper-20250901)
**Discussions**: [GitHub Discussions](https://github.com/yourusername/yuimedi-paper-20250901/discussions)

## 📈 Citation

```bibtex
@techreport{harrold2026,
  title = {Healthcare Analytics Challenges: A Three-Pillar Framework Connecting Analytics Maturity, Workforce Dynamics, and Technical Barriers},
  author = {Harrold, Samuel T.},
  year = {2026},
  month = {1},
  institution = {Yuimedi, Inc.},
  type = {Technical Whitepaper},
  url = {https://github.com/stharrold/yuimedi-paper-20250901},
  note = {Research on conversational AI platforms addressing healthcare analytics challenges}
}
```

## 🎯 Research Impact

This research aims to:
- **Advance** natural language processing applications in healthcare
- **Reduce** technical barriers to healthcare data analysis
- **Improve** institutional knowledge preservation
- **Enable** broader access to healthcare analytics capabilities
- **Support** evidence-based decision making in clinical settings

---

<p align="center">
  <a href="#top">⬆️ Back to Top</a>
</p>
