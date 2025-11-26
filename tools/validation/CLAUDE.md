---
type: claude-context
directory: tools/validation
purpose: Documentation validation test scripts
parent: ../CLAUDE.md
sibling_readme: null
children: []
---

# Claude Code Context: tools/validation

## Purpose

Bash validation scripts for documentation quality enforcement.

## Contents

5 validation test scripts:

| Script | Purpose |
|--------|---------|
| `test_file_size.sh` | Enforces 30KB limit on modular docs |
| `test_cross_references.sh` | Validates internal markdown links |
| `test_content_duplication.sh` | Detects duplicate sections |
| `test_command_syntax.sh` | Validates bash code blocks |
| `test_yaml_structure.sh` | Checks JSON/YAML structure |

**Orchestrator:** `validate_documentation.sh` (runs all 5 tests)

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

- **Parent**: [tools/CLAUDE.md](../CLAUDE.md)
