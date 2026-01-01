---
title: "YuiQuery Research Repository - Task Management"
version: "2.0.0"
last_updated: "2025-11-21"
migration_date: "2025-11-21"
migration_reason: "Consolidated duplicate TODO items and migrated to GitHub Issues for better tracking"
archived_files:
  - path: "ARCHIVED/TODO/20251121T095620Z_TODO_FOR_AI.json"
    original_name: "TODO_FOR_AI.json"
    items: 169
    todo_items: 69
    done_items: 100
    description: "Structured task tracking with priority and technical context"
  - path: "ARCHIVED/TODO/20251121T095620Z_TODO_FOR_HUMAN.md"
    original_name: "TODO_FOR_HUMAN.md"
    description: "Human-readable task list generated from TODO_FOR_AI.json"
migration_summary:
  original_todo_items: 69
  duplicate_items: 33
  unique_items_created: 36
  github_issues_created: 36
  deduplication_rate: "47.8%"
task_tracking:
  primary_source: "GitHub Issues"
  repository: "stharrold/yuimedi-paper-20250901"
  issue_tracker_url: "https://github.com/stharrold/yuimedi-paper-20250901/issues"
  documentation: "All tasks now tracked as GitHub Issues with comprehensive context for Claude Code"
---

# TODO Management - GitHub Issues

**Status:** Active task tracking has been migrated to GitHub Issues
**Date:** November 21, 2025

## Overview

This repository has migrated from local TODO files (TODO_FOR_AI.json, TODO_FOR_HUMAN.md) to GitHub Issues for better project management, collaboration, and transparency.

## Why This Change?

1. **Eliminated Duplicates**: Reduced 69 todo items to 36 unique consolidated tasks (47.8% reduction)
2. **Better Tracking**: GitHub Issues provide better visibility, comments, and progress tracking
3. **Claude Code Integration**: Each issue includes comprehensive instructions for Claude Code
4. **Collaboration**: Team members can comment, update, and track work in one place
5. **Transparency**: Public issue tracker for research project transparency

## Migration Statistics

- **Original TODO items**: 69 active tasks
- **Duplicate items found**: 33 (many tasks appeared 3-4 times)
- **Consolidated unique items**: 36
- **GitHub Issues created**: 36 (issues #183-#218)
- **Completed tasks archived**: 100 tasks marked as done

## Accessing Current Tasks

### View All Tasks
```bash
# List all open issues
gh issue list

# List by priority (check labels)
gh issue list --label "P0"  # Critical
gh issue list --label "P1"  # High
gh issue list --label "P2"  # Medium

# View specific issue
gh issue view <number>
```

### Task Categories

**Critical Tasks (P0)**:
- Create Backup Developer Documentation
- Update Publication Strategy with Portals
- Document Risk Assessment Methodology
- Create Risk Scoring Matrix
- Document Probability Calculations

**High Priority (P1)**:
- Add Anthropic Teams Claude Code best practices
- Cite Anthropic Code Modernization Playbook
- Create Methodology Validation Checklist
- Setup Complete Directory Structure
- Setup Synthetic Data with Synthea
- Update Risk Register with Numerical Scores

**Medium Priority (P2)**:
- Documentation improvements
- Code quality fixes
- Paper generation tasks
- Citation consistency reviews

## For Claude Code

When working on tasks:

1. **Find tasks**: `gh issue list --state open`
2. **View task details**: `gh issue view <number>`
3. **Update progress**: Comment on the issue with updates
4. **Close when done**: `gh issue close <number> --comment "Completed: <summary>"`

Each GitHub Issue includes:
- Comprehensive task description
- Context for Claude Code (project patterns, validation requirements)
- Expected deliverables
- Repository-specific instructions

## Archived Files

Previous TODO files have been archived with timestamps:

- `ARCHIVED/TODO/20251121T095620Z_TODO_FOR_AI.json` (169 tasks total, 100 completed)
- `ARCHIVED/TODO/20251121T095620Z_TODO_FOR_HUMAN.md` (human-readable version)

These files are preserved for historical reference but are no longer actively maintained.

## Task Management Workflow

### For Humans
1. Browse issues: https://github.com/stharrold/yuimedi-paper-20250901/issues
2. Create new tasks as GitHub Issues (use issue templates if available)
3. Comment on issues to discuss or provide updates
4. Close issues when work is complete

### For Claude Code
1. Query open issues: `gh issue list --state open --json number,title,labels`
2. Read issue details: `gh issue view <number>`
3. Update with progress: `gh issue comment <number> --body "Progress update: ..."`
4. Close when done: `gh issue close <number> --comment "Completed successfully"`

## Sync with GitHub Issues

This repository no longer uses bidirectional sync between local TODO files and GitHub Issues. GitHub Issues are now the single source of truth for task management.

**Historical Note**: The previous `scripts/sync_github_todos.py` script synchronized local TODO_FOR_AI.json with GitHub Issues. This workflow has been deprecated in favor of direct GitHub Issues management.

## Migration Benefits

1. **No More Duplicates**: Single source of truth eliminates confusion
2. **Better Context**: Each issue has comprehensive instructions for Claude Code
3. **Improved Collaboration**: Comments and discussions on issues
4. **Progress Tracking**: Issue states (open/closed) show clear progress
5. **Integration**: Works seamlessly with GitHub Projects, milestones, labels
6. **Transparency**: Public visibility into research project status

## Next Steps

- Review open issues: https://github.com/stharrold/yuimedi-paper-20250901/issues
- Prioritize critical (P0) and high priority (P1) tasks
- Use GitHub Projects for sprint planning (optional)
- Close issues as work is completed

---

**For questions about this migration, see git commit history or GitHub Issues.**
