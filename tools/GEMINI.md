---
type: claude-context
directory: tools
purpose: Documentation validation scripts
parent: ../GEMINI.md
sibling_readme: null
children:
  - validation/GEMINI.md
---

# Gemini Context Context: tools

## Purpose

Documentation validation scripts (bash-based tests for doc quality).

## Contents

- `validation/` - Documentation validation test scripts

## Subdirectory: validation/

Contains 7 validation tests (5 bash + 2 Python):
- `test_file_size.sh` - Enforces 30KB limit on modular docs
- `test_cross_references.sh` - Validates internal markdown links
- `test_content_duplication.sh` - Detects duplicate sections
- `test_command_syntax.sh` - Validates bash code blocks
- `test_yaml_structure.sh` - Checks JSON/YAML structure
- `validate_references.py --check-citations` - Validates citations in paper.md
- `validate_references.py --check-latex` - Detects LaTeX commands in URLs

Orchestrator: `validate_documentation.sh` (symlinked from root, runs all 7 tests)

## Usage

```bash
# Run all validation tests
./validate_documentation.sh

# Run individual tests
tools/validation/test_file_size.sh
tools/validation/test_cross_references.sh
```

## Archived

- `workflow-utilities/` - Archived 2026-01-01; redundant with `.gemini/skills/workflow-utilities/`

## Related

- **Parent**: [Root GEMINI.md](../GEMINI.md)
- **Workflow utilities**: [.gemini/skills/workflow-utilities/](../.gemini/skills/workflow-utilities/GEMINI.md)

## Related Documentation

- **[../GEMINI.md](../GEMINI.md)** - Parent directory: Root

**Child Directories:**
- **[ARCHIVED/GEMINI.md](ARCHIVED/GEMINI.md)** - Archived
- **[validation/GEMINI.md](validation/GEMINI.md)** - Validation
