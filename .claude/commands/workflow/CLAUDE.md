---
type: claude-context
directory: .claude/commands/workflow
purpose: 4-phase v6 workflow commands using Claude's feature-dev plugin.
parent: ../CLAUDE.md
sibling_readme: null
children:
  []
---

# Claude Code Context: workflow

## Purpose

4-phase v6 workflow commands using Claude's feature-dev plugin for streamlined development.

## v6 Workflow Flow

```
/workflow:v6_1_worktree "feature description"
    | creates worktree, user runs /feature-dev in worktree
    v
/workflow:v6_2_integrate "feature/YYYYMMDDTHHMMSSZ_slug"
    | PR feature->contrib->develop
    v
/workflow:v6_3_release
    | create release, PR to main, tag
    v
/workflow:v6_4_backmerge
    | PR release->develop, rebase contrib, cleanup
```

## Contents

- `v6_1_worktree.md` - Create worktree for feature-dev
- `v6_2_integrate.md` - Integrate feature to develop
- `v6_3_release.md` - Release to production
- `v6_4_backmerge.md` - Sync release to develop

## Related

- **Parent**: [commands](../CLAUDE.md)
