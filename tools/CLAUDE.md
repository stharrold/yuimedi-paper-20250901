---
type: claude-context
directory: tools
purpose: Documentation validation scripts
parent: ../CLAUDE.md
sibling_readme: null
children:
  - validation/CLAUDE.md
---

# Claude Code Context: tools

## Purpose

Documentation validation scripts (bash-based tests for doc quality).

## Contents

- `validation/` - Documentation validation test scripts

## Subdirectory: validation/

Contains 5 validation test scripts:
- `test_file_size.sh` - Enforces 30KB limit on modular docs
- `test_cross_references.sh` - Validates internal markdown links
- `test_content_duplication.sh` - Detects duplicate sections
- `test_command_syntax.sh` - Validates bash code blocks
- `test_yaml_structure.sh` - Checks JSON/YAML structure

Orchestrator: `validate_documentation.sh` (symlinked from root)

## Usage

```bash
# Run all validation tests
./validate_documentation.sh

# Run individual tests
tools/validation/test_file_size.sh
tools/validation/test_cross_references.sh
```

## Archived

- `workflow-utilities/` - Archived 2026-01-01; redundant with `.claude/skills/workflow-utilities/`

## Related

- **Parent**: [Root CLAUDE.md](../CLAUDE.md)
- **Workflow utilities**: [.claude/skills/workflow-utilities/](../.claude/skills/workflow-utilities/CLAUDE.md)
