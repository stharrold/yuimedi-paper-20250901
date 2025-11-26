---
type: claude-context
directory: scripts
purpose: GitHub sync automation scripts using Python stdlib only
parent: ../CLAUDE.md
sibling_readme: README.md
children: []
---

# Claude Code Context: scripts

## Purpose

Automation scripts for GitHub Issues synchronization. **All scripts use Python stdlib only** - no external dependencies.

## Contents

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
# Run sync script
python scripts/sync_github_todos.py

# Or use bash wrapper
./scripts/sync_todos.sh
```

## Related

- **Parent**: [Root CLAUDE.md](../CLAUDE.md)
- **Sibling**: [README.md](README.md)
