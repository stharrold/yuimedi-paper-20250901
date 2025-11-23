---
description: "workflow/5_integrate → workflow/6_release → workflow/7_backmerge | Release to production"
order: 6
prev: /5_integrate
next: /7_backmerge
---

# /6_release - Step 6 of 7

**Workflow**: `/1_specify` → `/2_plan` → `/3_tasks` → `/4_implement` → `/5_integrate` → `/6_release` → `/7_backmerge`

**Purpose**: Create release from develop, run quality gates, and create PR to main for production deployment.

**Prerequisites**: Features integrated to develop (from `/5_integrate`), develop has commits since last release

**Outputs**: Release branch created, PR to main, tag on main after merge

**Next**: Run `/7_backmerge` after release PR is merged to main

---

# Release Workflow Command

Create a release and deploy to production.

## Workflow Steps (in order)

1. **create-release** - Create release branch from develop
2. **run-gates** - Run quality gates on release branch
3. **pr-main** - Create PR from release to main
4. **tag-release** - Tag release on main after PR merge

## Usage

Run workflow step:
```bash
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/release_workflow.py <step>
```

## Available Steps

- `create-release` - Create release/<version> branch from develop
- `run-gates` - Run quality gates on release branch
- `pr-main` - Create PR from release to main
- `tag-release` - Tag the release on main after merge
- `full` - Run all steps in sequence
- `status` - Show current release status

## Example Session

```bash
# 1. Create release branch (auto-calculates version)
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/release_workflow.py create-release

# 2. Run quality gates on release branch
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/release_workflow.py run-gates

# 3. Create PR to main
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/release_workflow.py pr-main

# 4. After PR merged, tag the release
podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/release_workflow.py tag-release
```

## Semantic Versioning

Version is auto-calculated if not provided:
- **MAJOR**: Breaking changes detected
- **MINOR**: New features added
- **PATCH**: Bug fixes only

## Quality Gates

The `run-gates` step runs quality gates:
- Test coverage (≥80%)
- All tests passing
- Build successful
- Linting clean

## Notes

- Release branch is ephemeral (deleted after backmerge)
- Tag is created on main after PR merge
- CHANGELOG.md is updated automatically if present
