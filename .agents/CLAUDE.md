---
type: claude-context
directory: .claude
purpose: Claude Code configuration root containing commands, skills, and settings.
parent: ../CLAUDE.md
sibling_readme: null
children:
  - commands/CLAUDE.md
  - skills/CLAUDE.md
---

# Claude Code Context: .claude

## Purpose

Claude Code configuration root containing commands, skills, and settings.

## Source Status

**This directory (`.claude/`) is the PRIMARY source for AI configuration.**

Changes made here sync to:
- `.agents/` (skills only)
- `AGENTS.md` (from root CLAUDE.md)
- `.github/copilot-instructions.md` (from root CLAUDE.md)

Claude-specific content (NOT synced):
- `commands/` - Claude Code slash commands
- `settings.local.json` - Local settings

## Contents

- `commands/` - Subdirectory
- `skills/` - Subdirectory
- `settings.local.json` - Configuration

## Related

- **Parent**: [stharrold-templates](../CLAUDE.md)
- **commands**: [commands/CLAUDE.md](commands/CLAUDE.md)
- **skills**: [skills/CLAUDE.md](skills/CLAUDE.md)
