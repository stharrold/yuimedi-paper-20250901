# Source Code Directory

This directory contains algorithms and analysis code supporting the YuiQuery healthcare analytics research project.

## 📁 Directory Structure

```
src/
├── algorithms/     # NL2SQL core algorithms and healthcare adaptations
├── analysis/       # Data analysis scripts and statistical methods
└── mapping/        # Schema mapping and healthcare terminology processing
```

## 🎯 Purpose

Source code in this directory supports:
- **Research Implementation**: Algorithms described in paper.md
- **Data Analysis**: Processing healthcare datasets for research validation
- **Proof of Concept**: Demonstrating YuiQuery capabilities
- **Reproducibility**: Enabling validation of research findings

## 🔬 Key Components

### Algorithms (`algorithms/`)
Core natural language to SQL translation algorithms with healthcare-specific adaptations:
- Schema inference and relationship discovery
- NL2SQL translation with medical terminology handling
- Query optimization and validation
- HIPAA-compliant filtering

See [algorithms/README.md](algorithms/README.md) for details.

### Analysis (`analysis/`)
Statistical analysis and data processing scripts for research validation:
- Healthcare analytics maturity assessment
- Query complexity analysis
- Performance benchmarking
- Case study data processing

See [analysis/README.md](analysis/README.md) for details.

### Mapping (`mapping/`)
Healthcare-specific schema mapping and terminology processing:
- Medical vocabulary mapping (ICD-10, CPT, SNOMED)
- Table relationship inference
- Clinical workflow modeling
- Data dictionary generation

See [mapping/README.md](mapping/README.md) for details.

## 🛠️ Development Environment

### Prerequisites
```bash
# UV package manager (required)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup environment
uv sync

# Verify installation
uv run python --version  # Should be 3.8+
```

### Running Code
```bash
# Format code
uv run ruff format src/

# Lint code
uv run ruff check src/

# Type checking
uv run mypy src/

# Run specific script
uv run python src/algorithms/your_script.py
```

## 📊 Data Access

All source code uses:
- **De-identified data** from `config/database/` configuration
- **Synthetic data** as backup (Synthea-generated)
- **No PHI** in code or version control
- **IRB exempt** status (see `compliance/irb/determination.md`)

## 🔒 Security & Compliance

- **No credentials** in code (use environment variables)
- **HIPAA compliance** maintained throughout
- **Audit logging** for data access
- **Privacy preservation** in all algorithms

## 🔗 Related Documentation

- [Main Research Paper](../paper.md) - Academic documentation of methods
- [Database Configuration](../config/database/README.md) - Data source setup
- [IRB Determination](../compliance/irb/determination.md) - Research ethics status
- [GEMINI.md](../GEMINI.md) - Development guidelines

## 📝 Code Standards

- **Python 3.8+** required
- **Type hints** for public functions
- **Docstrings** for all modules and classes
- **Ruff formatting** (Black-compatible)
- **No hardcoded paths** or credentials

## 🧪 Testing

```bash
# Run tests (when available)
uv run pytest src/tests/

# Test with synthetic data
uv run python src/algorithms/test_with_synthea.py
```

## 📈 Contributing

When adding new source code:
1. Follow existing directory structure
2. Add appropriate README in subdirectories
3. Ensure HIPAA compliance
4. Document healthcare-specific adaptations
5. Use UV environment for dependencies
6. Run linting and type checking before commit

---

*This directory contains implementation supporting the research documented in [paper.md](../paper.md)*
