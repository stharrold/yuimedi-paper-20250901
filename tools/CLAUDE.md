---
type: claude-context
directory: tools
purpose: Documentation validation scripts and workflow utilities
parent: ../CLAUDE.md
sibling_readme: null
children:
  - validation/CLAUDE.md
  - workflow-utilities/CLAUDE.md
---

# Claude Code Context: tools

## Purpose

Utility scripts for documentation validation and workflow management.

## Contents

- `validation/` - Documentation validation test scripts
- `workflow-utilities/` - Archive management and version checking

## Subdirectories

### validation/

Contains 5 validation test scripts:
- `test_file_size.sh` - Enforces 30KB limit on modular docs
- `test_cross_references.sh` - Validates internal markdown links
- `test_content_duplication.sh` - Detects duplicate sections
- `test_command_syntax.sh` - Validates bash code blocks
- `test_yaml_structure.sh` - Checks JSON/YAML structure

Orchestrator: `validate_documentation.sh` (symlinked from root)

### workflow-utilities/

Archive management and version checking utilities.

## Usage

```bash
# Run all validation tests
./validate_documentation.sh

# Run individual tests
tools/validation/test_file_size.sh
tools/validation/test_cross_references.sh
```

## Related

- **Parent**: [Root CLAUDE.md](../CLAUDE.md)
