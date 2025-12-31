---
description: "Create worktree for feature-dev | v6 workflow step 1 of 4"
order: 1
next: /workflow:v6_2_integrate
---

# /workflow:v6_1_worktree - Step 1 of 4

**v6 Workflow**: `/workflow:v6_1_worktree` -> [feature-dev] -> `/workflow:v6_2_integrate` -> `/workflow:v6_3_release` -> `/workflow:v6_4_backmerge`

**Purpose**: Create git worktree for feature development using Claude's feature-dev plugin.

**Prerequisites**: Main repo, `contrib/*` branch

**Outputs**: Feature worktree with instructions for running feature-dev

---

## Usage

```
/workflow:v6_1_worktree "feature description"
```

Example:
```
/workflow:v6_1_worktree "add user authentication with JWT tokens"
```

---

## Step 1: Extract Feature Slug

Parse the feature description to create a kebab-case slug:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters
- Limit to 50 characters

Example: "Add User Authentication" -> "add-user-authentication"

---

## Step 2: Create Feature Worktree

Create worktree using the git-workflow-manager script:

```bash
uv run python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature {slug} contrib/stharrold
```

This creates:
- Branch: `feature/{timestamp}_{slug}`
- Worktree: `../{project}_feature_{timestamp}_{slug}/`
- State directory: `.claude-state/` in worktree

---

## Step 3: Record State in AgentDB

```bash
uv run python .claude/skills/agentdb-state-manager/scripts/record_sync.py \
  --sync-type workflow_transition \
  --pattern phase_v6_1_worktree \
  --source "main_repo" \
  --target "worktree"
```

---

## Step 4: Display Next Steps

After creating the worktree, display these instructions to the user:

```
[OK] Worktree created for v6 workflow

Worktree path: {worktree_path}
Branch: {branch_name}

=== NEXT STEPS ===

1. Exit this Claude session

2. Navigate to the worktree:
   cd {worktree_path}

3. Open a new Claude session and run feature-dev:
   /feature-dev "{original_feature_description}"

4. After implementation is complete, return to main repo:
   cd {main_repo_path}

5. Run integration:
   /workflow:v6_2_integrate "{branch_name}"
```

**Important**: Copy the feature description for use with /feature-dev.

---

## Notes

- The feature-dev plugin handles all planning, architecture, and code review
- No planning documents required (unlike v1-v7 workflow)
- Quality is ensured by feature-dev's code review phase
