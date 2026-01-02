---
type: claude-context
directory: scripts
purpose: GitHub sync automation scripts using Python stdlib only
parent: ../GEMINI.md
sibling_readme: README.md
children: []
---

# Gemini Context Context: scripts

## Purpose

Automation scripts for GitHub Issues synchronization. **All scripts use Python stdlib only** - no external dependencies.

## Contents

- `validate_references.py` - Reference validation for paper.md citations
- `sync_github_todos.py` - Main GitHub Issues sync script
- `sync_todos.sh` - Bash wrapper for sync script
- `github_project_sync.sh` - GitHub project board sync
- `SYNC_GUIDE.md` - Detailed sync documentation

## Zero Dependencies Architecture

**CRITICAL:** Scripts in this directory must use only Python stdlib:

```python
# Allowed imports
import sys, os, subprocess, json, pathlib, datetime, re, typing

# NOT allowed
import requests  # Use subprocess + curl instead
import click     # Use argparse instead
```

## Usage

```bash
# Validate paper.md references
python scripts/validate_references.py --all
python scripts/validate_references.py --check-citations
python scripts/validate_references.py --check-urls --verbose
python scripts/validate_references.py --report

# Run sync script
python scripts/sync_github_todos.py

# Or use bash wrapper
./scripts/sync_todos.sh
```

## Related

- **Parent**: [Root GEMINI.md](../GEMINI.md)
- **Sibling**: [README.md](README.md)
