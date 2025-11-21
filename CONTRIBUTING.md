# Contributing to YuiQuery Healthcare Analytics Research

Thank you for considering contributing to this research project! This document provides guidelines for contributing to the YuiQuery healthcare analytics research documentation.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Documentation Requirements](#documentation-requirements)
- [Pull Request Process](#pull-request-process)
- [Quality Standards](#quality-standards)

## Code of Conduct

This project follows a professional and respectful code of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Prioritize technical accuracy and truthfulness
- Welcome contributions from all skill levels

## Getting Started

### Prerequisites

Ensure you have the required tools installed:

```bash
# Required
python3 --version     # Python 3.8+ (for workflow utilities)
git --version         # Version control
gh --version          # GitHub CLI (for PR management)

# Optional but recommended
uv --version          # Python package manager (for dev tools)
pandoc --version      # Document generation
```

### Initial Setup

1. **Fork and clone the repository:**
   ```bash
   gh repo fork stharrold/yuimedi-paper-20250901 --clone
   cd yuimedi-paper-20250901
   ```

2. **Install development dependencies (optional):**
   ```bash
   uv sync  # Installs black, flake8, mypy, pre-commit
   ```

3. **Run validation scripts:**
   ```bash
   ./validate_documentation.sh
   ```

## Development Workflow

This repository uses a contrib branch workflow:

### Branch Structure

```
main (production)
  ↑
develop (integration)
  ↑
contrib/stharrold (active development)
  ↑
feature/* (individual features)
```

### Creating a Feature Branch

```bash
# Create feature branch from contrib/stharrold
git checkout contrib/stharrold
git pull origin contrib/stharrold
git checkout -b feat/my-feature
```

### Daily Maintenance

```bash
# Rebase contrib branch onto develop
git checkout contrib/stharrold
git fetch origin
git rebase origin/develop
git push origin contrib/stharrold --force-with-lease
```

### Pull Request Flow

1. **Feature → contrib/stharrold**: After feature implementation
2. **contrib/stharrold → develop**: When ready for integration
3. **develop → main**: For production releases

## Documentation Requirements

### Academic Research Standards

**Citation Management:**
- Use `[A#]` format for academic sources (peer-reviewed journals, systematic reviews)
- Use `[I#]` format for industry sources (case studies, white papers)
- Maintain complete bibliography with DOI links where available
- Ensure all claims are supported by citations

**Healthcare Domain Accuracy:**
- Accurately use medical terminology (ICD-10, CPT, SNOMED, RxNorm)
- Reference healthcare IT standards appropriately (HIMSS AMAM, HL7, FHIR)
- Account for regulatory context (HIPAA, data governance)
- Frame findings within healthcare-specific challenges

**Statistical Reporting:**
- Include confidence intervals, p-values, and effect sizes where appropriate
- Report quantitative results with statistical significance
- Follow systematic literature review methodology

### Document Structure

**Academic Paper Format:**
- Abstract, Introduction, Literature Review, Methods, Results, Discussion, Conclusion
- Appendices for glossaries and practical examples
- Consistent section numbering and cross-references

**File Organization:**
- Primary research document: `paper.md`
- Supporting materials: `images/`, `docs/`, `scripts/`
- Project management: `TODO_FOR_AI.json`, `TODO_FOR_HUMAN.md`, `DECISION_LOG.json`

### Validation

Before committing documentation changes:

```bash
./validate_documentation.sh  # Runs all 5 validation tests:
# - test_file_size.sh (30KB limit for modular files)
# - test_cross_references.sh (internal links)
# - test_content_duplication.sh (detect duplicates)
# - test_command_syntax.sh (validate bash commands)
# - test_yaml_structure.sh (check frontmatter)
```

## Pull Request Process

### 1. Create Pull Request

```bash
# Push feature branch
git push origin feat/my-feature

# Create PR to contrib/stharrold
gh pr create \
  --title "feat: descriptive title" \
  --body "Detailed description" \
  --base contrib/stharrold
```

### 2. PR Requirements

- [ ] All validation scripts pass
- [ ] Documentation follows academic standards
- [ ] Citations properly formatted
- [ ] Commit messages follow convention
- [ ] No sensitive information exposed

### 3. Commit Message Format

```
<type>(<scope>): <subject>

<body>

Closes #issue-number

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:** feat, fix, docs, style, refactor, test, chore

### 4. Review Process

- Self-merge enabled for personal contrib branches
- Request review for significant changes
- Address feedback before merge

### 5. After Merge

```bash
# Cleanup branches
git checkout contrib/stharrold
git pull origin contrib/stharrold
git branch -D feat/my-feature
git push origin --delete feat/my-feature
```

## Quality Standards

### Documentation Standards

**Academic Quality:**
- Systematic methodology for literature reviews
- Evidence-based claims with proper citations
- Empirical validation with quantitative results
- Healthcare context maintained throughout

**Technical Accuracy:**
- Correctly represent NL2SQL technology state
- Accurately describe healthcare analytics maturity models
- Realistically portray implementation challenges
- Base ROI calculations on documented case studies

**Writing Quality:**
- Clear, concise academic writing
- Consistent terminology throughout
- Proper grammar and spelling
- Logical flow and narrative coherence

### Python Script Standards

**Core Principles:**
- **Stdlib only**: No external dependencies for core tools
- **Cross-platform**: Works on macOS, Linux, Windows
- **System Python**: Use `/usr/bin/python3` in scripts
- **Error handling**: Comprehensive try/except with clear messages

**Development Tools (optional):**
```bash
# Linting
uv run black .

# Type checking
uv run mypy scripts/

# Code quality
uv run flake8 scripts/
```

### Workflow Utilities

**Archive Management:**
```bash
# List archives
python3 tools/workflow-utilities/archive_manager.py list

# Create archive
python3 tools/workflow-utilities/archive_manager.py create path/to/file
```

**Directory Structure:**
```bash
# Validate directory structure
python3 tools/workflow-utilities/directory_structure.py docs/

# Every directory should have:
# - CLAUDE.md (AI context)
# - README.md (human documentation)
# - ARCHIVED/ (deprecated files)
```

**Version Validation:**
```bash
# Check version consistency
python3 tools/workflow-utilities/validate_versions.py
```

## Document Generation

### Pandoc PDF Generation

**Basic PDF:**
```bash
pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.pdf
```

**Professional Academic PDF:**
```bash
pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.pdf \
  --template=eisvogel \
  --pdf-engine=xelatex \
  --listings \
  --toc \
  --number-sections
```

**HTML for Web:**
```bash
pandoc paper.md -o YuiQuery-Healthcare-Analytics-Research.html \
  --standalone \
  --toc \
  --self-contained
```

## Questions or Issues?

- Open an issue on GitHub
- Check CLAUDE.md for detailed guidance
- Review existing PRs for examples

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).
