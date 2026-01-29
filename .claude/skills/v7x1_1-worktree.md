---
name: v7x1_1-worktree
description: Create worktree for feature development (Step 1 of 4)
---

# /v7x1_1-worktree - Step 1 of 4

**v7x1 Workflow**: `/v7x1_1-worktree` → Implementation → `/v7x1_2-integrate` → `/v7x1_3-release` → `/v7x1_4-backmerge`

**Task**: Create a git worktree for isolated feature development.

**Input**: Feature description (e.g., "add user authentication")

## Step 1: Extract Feature Slug

Parse the feature description to create a kebab-case slug:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters
- Limit to 50 characters

Example: "Add User Authentication" → `add-user-authentication`

## Step 2: Create Feature Worktree

```bash
uv run python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature <slug> contrib/stharrold
```

**Output:**
- Branch: `feature/<timestamp>_<slug>`
- Worktree: `../<repo-name>_feature_<timestamp>_<slug>/`

**Placeholders:** `<slug>` = kebab-case feature name, `<repo-name>` = repository directory name

## Step 3: Display Next Steps

After creating worktree, instruct user:

```
✓ Worktree created

Worktree path: {path}
Branch: {branch}

=== NEXT STEPS ===

1. Navigate to worktree:
   cd {worktree_path}

2. Implement the feature

3. Return to main repo and run:
   /v7x1_2-integrate "{branch}"
```

## Reference

Full documentation: `.claude/skills/v7x1-workflow.md`
