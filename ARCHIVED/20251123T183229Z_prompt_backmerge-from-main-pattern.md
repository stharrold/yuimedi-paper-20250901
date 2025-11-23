# Prompt: Implement Backmerge-from-Main Pattern

```yaml
created: 2025-11-23T18:32:29Z
author: stharrold
type: implementation-prompt
scope: workflow-scripts
priority: P1
estimated_effort: medium
related_issues: []
related_prs: [230, 231]
```

## Context

### Problem Statement

The current backmerge workflow in `/workflow:7_backmerge` has an implicit dependency on the release branch (`release/*`) still existing after the release PR is merged. This coupling creates fragility:

1. **Dependency risk**: If `release/*` branch is deleted before backmerge, the workflow fails
2. **Missing merge commit**: The release branch doesn't contain the merge commit created when merging to main
3. **Workflow coupling**: `/workflow:7_backmerge` cannot run independently of `/workflow:6_release`

### Solution Pattern

Create `backmerge/*` branch **from main** (not from release branch) to ensure:

1. **Independence**: Backmerge can run anytime after main is updated
2. **Completeness**: Includes the merge commit on main
3. **Decoupling**: No dependency on release branch existing

### Current vs Proposed Flow

**Current (Coupled):**
```
release/v1.6.0 ──PR──> main
       │
       └──PR──> develop  (FAILS if release branch deleted)
```

**Proposed (Decoupled):**
```
release/v1.6.0 ──PR──> main ──(tag v1.6.0)──> (delete release/*)
                         │
                         └──> backmerge/v1.6.0 ──PR──> develop
```

## Repository Context

### Relevant Files to Modify

```
.claude/skills/git-workflow-manager/scripts/
├── backmerge_workflow.py      # PRIMARY: Update to create branch from main
├── release_workflow.py        # SECONDARY: May need coordination updates
└── backmerge_release.py       # REVIEW: Check if still needed or deprecated

.agents/git-workflow-manager/scripts/
├── backmerge_workflow.py      # MIRROR: Keep in sync with .claude/
├── release_workflow.py        # MIRROR: Keep in sync with .claude/
└── backmerge_release.py       # MIRROR: Keep in sync with .claude/

.claude/commands/workflow/
└── 7_backmerge.md             # UPDATE: Documentation for new pattern
```

### Current backmerge_workflow.py Behavior

The current `step_pr_develop()` function:
1. Finds release branch via `find_release_branch()`
2. Creates PR from `release/*` → `develop`
3. Depends on release branch existing

### Desired backmerge_workflow.py Behavior

The new `step_pr_develop()` function should:
1. Create `backmerge/<version>` branch from `origin/main`
2. Push backmerge branch to origin
3. Create PR from `backmerge/*` → `develop`
4. NOT depend on release branch existing

## Implementation Requirements

### 1. Update `backmerge_workflow.py`

#### 1.1 Add new function: `create_backmerge_branch()`

```python
def create_backmerge_branch(version: str) -> Optional[str]:
    """Create backmerge branch from main.

    Args:
        version: Version string (e.g., 'v1.6.0')

    Returns:
        Branch name if successful, None otherwise
    """
    backmerge_branch = f"backmerge/{version}"

    # Fetch latest
    run_cmd(["git", "fetch", "origin"], check=False)

    # Create branch from main
    result = run_cmd(
        ["git", "checkout", "-b", backmerge_branch, "origin/main"],
        check=False
    )
    if result.returncode != 0:
        print(f"✗ Failed to create {backmerge_branch}: {result.stderr}")
        return None

    # Push branch
    result = run_cmd(
        ["git", "push", "-u", "origin", backmerge_branch],
        check=False
    )
    if result.returncode != 0:
        print(f"✗ Failed to push {backmerge_branch}: {result.stderr}")
        return None

    return backmerge_branch
```

#### 1.2 Update `step_pr_develop()` to use backmerge branch

```python
def step_pr_develop(version: Optional[str] = None) -> bool:
    """Create PR from backmerge branch to develop.

    Creates backmerge/<version> from main, then PRs to develop.
    This ensures the merge commit from main is included.
    """
    print("\n" + "=" * 60)
    print("STEP 1: PR Backmerge → Develop")
    print("=" * 60)

    # Determine version from latest tag if not provided
    if not version:
        result = run_cmd(
            ["git", "describe", "--tags", "--abbrev=0", "origin/main"],
            check=False
        )
        version = result.stdout.strip() if result.returncode == 0 else None

    if not version:
        print("✗ Could not determine version. Specify --version.")
        return False

    print(f"  Backmerging version: {version}")

    # Create backmerge branch from main
    backmerge_branch = create_backmerge_branch(version)
    if not backmerge_branch:
        return False

    # Check if develop is behind main
    result = run_cmd(
        ["git", "rev-list", "--count", "origin/develop..origin/main"],
        check=False
    )
    commits_behind = result.stdout.strip()

    if commits_behind == "0":
        print("⚠️  develop is already up to date with main")
        # Cleanup the branch we just created
        run_cmd(["git", "checkout", get_contrib_branch()], check=False)
        run_cmd(["git", "branch", "-D", backmerge_branch], check=False)
        run_cmd(["git", "push", "origin", "--delete", backmerge_branch], check=False)
        return True

    # Create PR
    print(f"\n[PR] Creating PR: {backmerge_branch} → develop...")
    result = run_cmd(
        [
            "gh", "pr", "create",
            "--base", "develop",
            "--head", backmerge_branch,
            "--title", f"Backmerge {version} to develop",
            "--body", f"Backmerge main ({version}) to develop.\n\nKeeps develop in sync with production.\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)",
        ],
        check=False,
    )

    if result.returncode != 0:
        if "already exists" in result.stderr:
            print("⚠️  PR already exists")
        else:
            print(f"✗ PR creation failed: {result.stderr}")
            return False

    print(f"✓ Step 1 complete: PR created {backmerge_branch} → develop")
    print("\nNext: Merge PR in GitHub, then run: backmerge_workflow.py rebase-contrib")
    return True
```

#### 1.3 Update `step_cleanup_release()` to also clean backmerge branch

```python
def step_cleanup_release(version: Optional[str] = None) -> bool:
    """Delete release and backmerge branches locally and remotely."""
    # ... existing release cleanup code ...

    # Also cleanup backmerge branch
    backmerge_branch = f"backmerge/{version}"

    print(f"\n[Delete] Cleaning up {backmerge_branch}...")
    run_cmd(["git", "branch", "-D", backmerge_branch], check=False)
    result = run_cmd(
        ["git", "push", "origin", "--delete", backmerge_branch],
        check=False
    )
    if result.returncode != 0:
        if "remote ref does not exist" in result.stderr:
            print("  Backmerge branch already deleted or never existed")
        else:
            print(f"⚠️  Backmerge branch delete warning: {result.stderr}")
```

### 2. Update `release_workflow.py` (if needed)

Review `release_workflow.py` to ensure it doesn't assume backmerge will use release branch. The release workflow should:
1. Create release branch from develop
2. PR to main
3. Tag on main
4. **NOT** handle backmerge (that's separate)

### 3. Review `backmerge_release.py`

Check if this older script is still used or should be deprecated in favor of the consolidated `backmerge_workflow.py`.

### 4. Update Slash Command Documentation

Update `.claude/commands/workflow/7_backmerge.md` to document:
- New backmerge-from-main pattern
- Independence from release workflow
- Version auto-detection from tags

### 5. Sync `.agents/` Mirror

After all changes:
```bash
rsync -av --delete --exclude=".DS_Store" --exclude="__pycache__" \
  .claude/skills/ .agents/
rsync -av --delete --exclude=".DS_Store" --exclude="__pycache__" \
  .claude/commands/ .agents/commands/
```

## Testing Requirements

### Manual Testing Steps

1. **Test with release branch existing:**
   ```bash
   # After release PR merged, before cleanup
   podman-compose run --rm dev python \
     .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py \
     pr-develop --version v1.6.0
   ```

2. **Test with release branch already deleted:**
   ```bash
   # Delete release branch first
   git push origin --delete release/v1.6.0

   # Should still work
   podman-compose run --rm dev python \
     .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py \
     pr-develop --version v1.6.0
   ```

3. **Test version auto-detection:**
   ```bash
   # Should detect v1.6.0 from tags
   podman-compose run --rm dev python \
     .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py \
     pr-develop
   ```

4. **Test idempotency:**
   ```bash
   # Running twice should not fail
   podman-compose run --rm dev python \
     .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py \
     pr-develop --version v1.6.0
   # Second run should report "already exists" or "up to date"
   ```

### Validation Checklist

- [ ] `backmerge_workflow.py` creates branch from `origin/main`
- [ ] Backmerge branch naming: `backmerge/<version>`
- [ ] PR created from backmerge branch to develop
- [ ] Version auto-detected from latest tag if not provided
- [ ] Works even if release branch deleted
- [ ] Cleanup deletes both release and backmerge branches
- [ ] `.agents/` mirror updated
- [ ] Slash command documentation updated
- [ ] Quality gates pass

## Code Quality Requirements

### Style
- Follow existing code patterns in the scripts
- Use type hints (Python 3.9+ style: `list[str]` not `List[str]`)
- Include docstrings with Args/Returns sections
- Log stderr on command failures (per PR #226 pattern)

### Error Handling
- Use `check=False` for git commands that may fail
- Provide clear error messages with suggested fixes
- Return to editable branch (contrib/*) on failure

### Git Safety
- Use `--force-with-lease` for any force pushes
- Never force push to main or develop
- Always fetch before comparing branches

## Commit Message Format

```
feat(git-workflow): Implement backmerge-from-main pattern

- Create backmerge/* branch from main instead of reusing release/*
- Decouple /workflow:7_backmerge from /workflow:6_release
- Auto-detect version from latest tag on main
- Include merge commit in backmerge (fixes sync gap)
- Update cleanup to handle backmerge branches

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Related Documentation

- **Current Scripts:**
  - `.claude/skills/git-workflow-manager/scripts/backmerge_workflow.py`
  - `.claude/skills/git-workflow-manager/scripts/release_workflow.py`
  - `.claude/skills/git-workflow-manager/CLAUDE.md`

- **Workflow Commands:**
  - `.claude/commands/workflow/6_release.md`
  - `.claude/commands/workflow/7_backmerge.md`

- **Reference PRs:**
  - PR #230 - Release v1.6.0 (release → main)
  - PR #231 - Backmerge v1.6.0 (backmerge → develop) - used new pattern

## Success Criteria

1. **Independence**: `/workflow:7_backmerge` runs successfully even if release branch doesn't exist
2. **Completeness**: Backmerge includes the merge commit from main
3. **Idempotency**: Running backmerge twice doesn't cause errors
4. **Auto-detection**: Version detected from tags when not specified
5. **Cleanup**: Both release and backmerge branches cleaned up properly
6. **Documentation**: Slash command docs updated to reflect new pattern
7. **Mirror sync**: `.agents/` directory matches `.claude/skills/`
