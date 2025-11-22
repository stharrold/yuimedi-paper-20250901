---
type: workflow-manifest
workflow_type: {{WORKFLOW_TYPE}}
slug: {{SLUG}}
timestamp: {{TIMESTAMP}}
github_user: {{GH_USER}}

metadata:
  title: "{{TITLE}}"
  description: "{{DESCRIPTION}}"
  created: "{{CREATED}}"
  stack: python
  package_manager: uv
  test_framework: pytest
  containers: []

workflow_progress:
  phase: 1
  current_step: "1.1"
  last_task: null
  last_update: "{{CREATED}}"
  status: "planning"

quality_gates:
  test_coverage: 80
  tests_passing: false
  build_successful: false
  semantic_version: "1.0.0"

tasks:
  planning:
    - id: plan_001
      description: "Create requirements.md"
      status: pending
      completed_at: null

    - id: plan_002
      description: "Create architecture.md"
      status: pending
      completed_at: null

  specification:
    - id: spec_001
      description: "Write spec.md with API contracts"
      status: pending
      completed_at: null

    - id: spec_002
      description: "Write plan.md with task breakdown"
      status: pending
      completed_at: null

  implementation:
    - id: impl_001
      description: "TBD - Add implementation tasks"
      status: pending
      completed_at: null

  testing:
    - id: test_001
      description: "TBD - Add testing tasks"
      status: pending
      completed_at: null

  containerization:
    - id: container_001
      description: "TBD - Add containerization tasks"
      status: pending
      completed_at: null

context_checkpoints: []
# Populated when context usage exceeds 100K tokens
# Format:
#   - timestamp: "2025-10-23T15:30:00Z"
#     token_usage: 100234
#     phase: 2
#     step: "2.4"
#     last_task: "impl_003"
#     notes: "Brief status summary"
---

# TODO: {{TITLE}}

**Type:** {{WORKFLOW_TYPE}}
**Slug:** {{SLUG}}
**Created:** {{CREATED}}
**GitHub User:** {{GH_USER}}

## Overview

{{DESCRIPTION}}

## Current Status

**Phase:** Planning (1)
**Current Step:** 1.1
**Last Updated:** {{CREATED}}

## Active Tasks

### Phase 1: Planning

- [ ] **plan_001**: Create requirements.md
  - Define business requirements and success criteria
  - Location: `planning/{{SLUG}}/requirements.md`

- [ ] **plan_002**: Create architecture.md
  - Design system architecture and components
  - Location: `planning/{{SLUG}}/architecture.md`

## Next Steps

1. Complete planning documents in main repository
2. Create feature worktree for implementation
3. Write detailed specifications
4. Implement functionality
5. Write tests and validate quality gates
6. Create pull request

## Quality Gates

- [ ] Test coverage ≥ 80%
- [ ] All tests passing
- [ ] Build successful
- [ ] Linting clean (ruff)
- [ ] Type checking clean (mypy)
- [ ] Containers healthy (if applicable)

## Workflow Commands

```bash
# Check workflow status
cat TODO_{{WORKFLOW_TYPE}}_{{TIMESTAMP}}_{{SLUG}}.md

# Create feature worktree
python .claude/skills/git-workflow-manager/scripts/create_worktree.py {{WORKFLOW_TYPE}} {{SLUG}} contrib/{{GH_USER}}

# Update task status
python .claude/skills/workflow-utilities/scripts/todo_updater.py TODO_{{WORKFLOW_TYPE}}_{{TIMESTAMP}}_{{SLUG}}.md <task_id> <status>

# Run quality gates
python .claude/skills/quality-enforcer/scripts/run_quality_gates.py
```

## Status History

- {{CREATED}}: Workflow initialized
