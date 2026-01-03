---
type: claude-context
directory: tools/validation
purpose: Documentation validation test scripts
parent: ../GEMINI.md
sibling_readme: null
children:
- ARCHIVED/GEMINI.md
---

# Gemini Context Context: tools/validation

## Purpose

Bash validation scripts for documentation quality enforcement.

## Contents

7 validation tests (5 bash scripts + 2 Python checks):

| Test | Script | Purpose |
|------|--------|---------|
| 1 | `test_file_size.sh` | Enforces 30KB limit on modular docs |
| 2 | `test_cross_references.sh` | Validates internal markdown links |
| 3 | `test_content_duplication.sh` | Detects duplicate sections |
| 4 | `test_command_syntax.sh` | Validates bash code blocks |
| 5 | `test_yaml_structure.sh` | Checks JSON/YAML structure |
| 6 | `validate_references.py --check-citations` | Validates paper.md citations against references.bib |
| 7 | `validate_references.py --check-latex` | Detects LaTeX commands in URLs |

**Orchestrator:** `validate_documentation.sh` (runs all 7 tests)

## Usage

```bash
# Run all validation tests (from repo root)
./validate_documentation.sh

# Run individual tests
tools/validation/test_file_size.sh
tools/validation/test_cross_references.sh
tools/validation/test_content_duplication.sh
tools/validation/test_command_syntax.sh
tools/validation/test_yaml_structure.sh
```

## Exit Codes

- `0` - All tests pass
- `1` - One or more tests failed

## Related

- **Parent**: [tools/GEMINI.md](../GEMINI.md)

## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
- **[../GEMINI.md](../GEMINI.md)** - Parent directory: tools

**Child Directories:**
- **[ARCHIVED/GEMINI.md](ARCHIVED/GEMINI.md)** - Archived
