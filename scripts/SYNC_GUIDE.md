# GitHub <-> TODO Sync Guide

This guide covers the complete usage of the GitHub issues to TODO files synchronization system for the YuiQuery Healthcare Analytics Research project.

## 🎯 Overview

The sync system provides bidirectional synchronization between GitHub issues and local TODO files, enabling seamless project management for academic research workflows.

### System Components
- `sync_todos.sh` - Main automation script (bash)
- `sync_github_todos.py` - Core synchronization engine (Python)
- `TODO_FOR_AI.json` - Structured task data for AI assistants
- `TODO_FOR_HUMAN.md` - Human-readable task summary

## 🚀 Quick Start

### Prerequisites Check
```bash
# Verify GitHub CLI is installed
gh --version

# Check authentication status
gh auth status

# Confirm Python 3 availability
python3 --version
```

### First-Time Setup
```bash
# Navigate to repository root
cd /Users/stharrold/Documents/GitHub/yuimedi-paper-20250901

# Install UV if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create UV environment and install dependencies
uv venv
uv pip install -e ".[dev]"

# Make script executable
chmod +x scripts/sync_todos.sh

# Install GitHub CLI if needed
brew install gh

# Authenticate with GitHub
gh auth login
```

### Basic Usage
```bash
# Run complete synchronization
./scripts/sync_todos.sh

# Or from scripts directory
cd scripts && ./sync_todos.sh
```

## 📋 Detailed Usage

### Command Line Execution
```bash
# Standard sync with user prompts
./scripts/sync_todos.sh

# Automated sync (answers 'yes' to all prompts)
echo -e "y\ny" | ./scripts/sync_todos.sh

# Verbose output for debugging
bash -x ./scripts/sync_todos.sh
```

### Understanding the Output
```
YuiQuery Healthcare Research TODO Sync Automation
==================================================
✅ Prerequisites verified
📁 Creating backup of existing TODO files...
   Backed up: TODO_FOR_AI.json -> .todo_backups/TODO_FOR_AI_20250821_143052.json
   Backed up: TODO_FOR_HUMAN.md -> .todo_backups/TODO_FOR_HUMAN_20250821_143052.md

🔄 Running GitHub <-> TODO synchronization...
Phase 1: GitHub -> TODO sync
Found 15 GitHub issues
Converting GitHub issues to TODO format...
Updated TODO_FOR_AI.json with 18 tasks
Generated TODO_FOR_HUMAN.md with 18 tasks
Validating sync consistency...
All GitHub issues synchronized with TODO files

✅ Synchronization completed successfully

📋 Current task summary:
   Total tasks: 18
   GitHub issues: 15
   Critical (P0): 2
   High priority (P1): 5
   In progress: 3
   Blocked: 1
```

## 🔧 GitHub Issue Configuration

### Priority Levels
Add these HTML comments to GitHub issue descriptions:

```markdown
<!-- priority: P0 -->  🔴 Critical - Blocks research progress
<!-- priority: P1 -->  🟠 High - Important for research completion  
<!-- priority: P2 -->  🟡 Medium - Standard research tasks (default)
<!-- priority: P3 -->  🟢 Low - Optional enhancements
```

### Status Tracking
```markdown
<!-- status: todo -->         📝 Not started
<!-- status: in_progress -->   🔄 Currently working
<!-- status: blocked -->       🚫 Waiting on dependencies
<!-- status: done -->          ✅ Completed
```

### Dependencies
```markdown
<!-- depends-on: #123, #456 -->  🔗 Task dependencies
```

### Complete Example
```markdown
# Research Task: Validate Healthcare NLP Claims

<!-- priority: P1 -->
<!-- status: in_progress -->
<!-- depends-on: #145, #167 -->

Comprehensive validation of natural language processing claims in the healthcare 
analytics research paper, focusing on:

- [ ] Verify cited accuracy percentages (45-78% range)
- [ ] Validate case study implementations  
- [ ] Cross-check empirical results with source papers
- [ ] Ensure medical terminology usage is accurate

**Estimated effort**: 4-6 hours
**Deadline**: Before paper submission
```

## 📁 File Structure and Outputs

### Generated Files
```
├── TODO_FOR_AI.json          # Structured task data
├── TODO_FOR_HUMAN.md         # Human-readable summary
└── .todo_backups/            # Automatic backups
    ├── TODO_FOR_AI_20250821_143052.json
    └── TODO_FOR_HUMAN_20250821_143052.md
```

### TODO_FOR_AI.json Structure
```json
{
  "project": "YuiQuery Healthcare Analytics Research",
  "version": "1.0.0",
  "type": "Academic research documentation", 
  "updated": "2025-08-21T14:30:52Z",
  "last_sync": "2025-08-21T14:30:52Z",
  "sync_metadata": {
    "total_github_issues": 15,
    "total_tasks": 18,
    "sync_conflicts": [],
    "validation_status": "synced"
  },
  "tasks": [
    {
      "id": "gh-123",
      "github_issue_number": 123,
      "title": "Validate Healthcare NLP Claims",
      "description": "Comprehensive validation of natural language processing claims...",
      "priority": "P1",
      "status": "in_progress",
      "dependencies": ["gh-145", "gh-167"],
      "labels": ["research", "validation"],
      "assignee": "username",
      "created_at": "2025-08-20T10:00:00Z",
      "updated_at": "2025-08-21T14:00:00Z"
    }
  ],
  "priority_distribution": {"P0": 2, "P1": 5, "P2": 8, "P3": 3},
  "status_distribution": {"todo": 8, "in_progress": 3, "blocked": 1, "done": 6}
}
```

### TODO_FOR_HUMAN.md Format
```markdown
# File: TODO_FOR_HUMAN.md
# Project: YuiQuery Healthcare Analytics Research
# Updated: 2025-08-21

## Priority 0 - Critical
> **CRITICAL**: Essential research tasks blocking publication progress

- [ ] **[#145]** Complete systematic literature review validation
  - Status: `in_progress` 
  - Details: Verify methodology compliance with PRISMA guidelines...

## Priority 1 - High  
> **HIGH**: Important research components for whitepaper completion

- [ ] **[#123]** Validate Healthcare NLP Claims
  - Dependencies: #145, #167
  - Status: `in_progress`
  - Details: Comprehensive validation of natural language processing claims...

## Blocked Tasks
> **BLOCKED**: Tasks waiting on dependencies or external factors

- [ ] **[#167]** Statistical Analysis Review
  - Blocked by: #145
  - Reason: Waiting on literature review completion...

## Recently Completed
> **DONE**: Recently finished tasks for reference

- [x] **[#156]** Merge research documents into paper.md (2025-08-21)
- [x] **[#134]** Update bibliography formatting (2025-08-20)
```

## 🔄 Workflow Integration

### Daily Research Workflow
```bash
# 1. Start of day - sync latest changes
./scripts/sync_todos.sh

# 2. Review priorities
open TODO_FOR_HUMAN.md

# 3. Work on tasks...

# 4. Update GitHub issues with progress

# 5. End of day - sync and commit
./scripts/sync_todos.sh
```

### Team Collaboration
```bash
# Before team meetings
./scripts/sync_todos.sh

# Create new research tasks
gh issue create --title "Literature Review Section X" --body "<!-- priority: P1 -->"

# Assign tasks to team members  
gh issue edit 123 --add-assignee username

# After task completion
gh issue close 123 --comment "Research validated, integrated into paper.md"
```

### Academic Milestones
```bash
# Pre-submission checklist
./scripts/sync_todos.sh
grep -c "P0\|P1" TODO_FOR_AI.json  # Check critical tasks

# Conference preparation
gh issue list --label "presentation" --state open

# Post-publication cleanup
gh issue close --label "completed-research"
```

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### GitHub Authentication Problems
```bash
# Check current authentication
gh auth status

# Re-authenticate if needed
gh auth login --web

# Verify repository access
gh repo view
```

#### Repository Name Mismatch
```
Warning: Repository name 'actual-name' doesn't match expected 'yuimedi-paper-20250901'
Continue anyway? (y/N):
```

**Solutions:**
1. Type `y` to continue (recommended for forks/renamed repos)
2. Edit line 56 in `sync_todos.sh` to update expected name:
   ```bash
   if [[ "$REPO_NAME" != "your-actual-repo-name" ]]; then
   ```

#### Python Script Errors
```bash
# Check Python path and permissions
which python3
python3 scripts/sync_github_todos.py

# Verify script permissions
ls -la scripts/
chmod +x scripts/sync_todos.sh
```

#### Sync Failures and Recovery
If sync fails, automatic recovery:
```bash
# Script automatically restores backups on failure
# Manual recovery if needed:
cp .todo_backups/TODO_FOR_AI_LATEST.json TODO_FOR_AI.json
cp .todo_backups/TODO_FOR_HUMAN_LATEST.md TODO_FOR_HUMAN.md
```

#### Git Commit Issues
```bash
# If commit fails due to conflicts
git status
git add TODO_FOR_AI.json TODO_FOR_HUMAN.md
git commit -m "chore: manual sync of TODO files"

# If push fails
git pull --rebase
git push
```

### Validation and Debugging

#### Check Sync Consistency
```bash
# Run validation manually
python3 scripts/sync_github_todos.py
# Look for "All GitHub issues synchronized" message

# Compare GitHub vs local
gh issue list --json number,title,state
jq '.tasks[].github_issue_number' TODO_FOR_AI.json
```

#### Verbose Output
```bash
# Debug script execution
bash -x scripts/sync_todos.sh

# Python debugging
python3 -u scripts/sync_github_todos.py
```

#### Backup Management
```bash
# List backups
ls -la .todo_backups/

# Clean old backups manually
find .todo_backups/ -name "TODO_FOR_*" -type f -mtime +7 -delete

# Restore specific backup
cp .todo_backups/TODO_FOR_AI_20250821_143052.json TODO_FOR_AI.json
```

## ⚙️ Advanced Configuration

### Custom Priority Mapping
Edit `sync_github_todos.py` line 66 to customize priority parsing:
```python
priority_match = re.search(r'<!-- priority:\s*(P\d|Critical|High|Medium|Low) -->', body, re.IGNORECASE)
```

### Custom Repository Settings
Update script configuration in `sync_todos.sh`:
```bash
# Line 56 - Repository name validation
if [[ "$REPO_NAME" != "your-custom-repo" ]]; then

# Line 149-160 - Commit message template
COMMIT_MESSAGE=$(cat <<'COMMIT_MSG'
Your custom commit message format
COMMIT_MSG
)
```

### Integration with Other Tools

#### CI/CD Integration
```yaml
# GitHub Actions example
name: Sync TODOs
on:
  issues:
    types: [opened, edited, closed]
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Sync TODOs
        run: |
          chmod +x scripts/sync_todos.sh
          echo -e "y\ny" | ./scripts/sync_todos.sh
```

#### IDE Integration
```json
// VS Code tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Sync TODOs",
      "type": "shell", 
      "command": "./scripts/sync_todos.sh",
      "group": "build",
      "presentation": {"echo": true, "reveal": "always"}
    }
  ]
}
```

## 📊 Monitoring and Analytics

### Task Metrics
```bash
# Extract metrics from TODO_FOR_AI.json
jq '.priority_distribution' TODO_FOR_AI.json
jq '.status_distribution' TODO_FOR_AI.json

# Count by assignee
jq '[.tasks[] | select(.assignee != null) | .assignee] | group_by(.) | map({assignee: .[0], count: length})' TODO_FOR_AI.json

# Time tracking
jq '.tasks[] | select(.status == "done") | {title, completed: .updated_at}' TODO_FOR_AI.json
```

### Research Progress Tracking
```bash
# Critical path analysis
jq '.tasks[] | select(.priority == "P0" or .priority == "P1") | {title, status, dependencies}' TODO_FOR_AI.json

# Blocked task analysis
jq '.tasks[] | select(.status == "blocked") | {title, dependencies}' TODO_FOR_AI.json

# Completion velocity
jq '[.tasks[] | select(.status == "done")] | length' TODO_FOR_AI.json
```

## 📚 Best Practices

### GitHub Issue Management
1. **Use descriptive titles**: "Validate NLP Claims in Section 3.2" vs "Fix validation"
2. **Include metadata comments**: Always add priority and status
3. **Link related issues**: Use `depends-on` for task dependencies
4. **Regular updates**: Update status as work progresses
5. **Close completed issues**: Don't leave finished tasks open

### Research Workflow
1. **Start each session with sync**: Ensure you have latest task status
2. **Review TODO_FOR_HUMAN.md**: Check priorities before starting work
3. **Update progress frequently**: Change status as you work
4. **Document blockers**: Use status comments to explain delays
5. **End session with sync**: Commit progress for team visibility

### File Management
1. **Don't edit TODO files manually**: Always use GitHub issues as source of truth
2. **Preserve backups**: Keep `.todo_backups/` directory
3. **Commit sync results**: Don't leave TODO changes uncommitted
4. **Review sync output**: Check for validation errors or conflicts

### Team Coordination
1. **Assign issues clearly**: Use `@username` for accountability
2. **Use labels consistently**: Tag issues by research area or type
3. **Comment on progress**: Add GitHub comments for status updates
4. **Schedule regular syncs**: Ensure team has consistent view

## 🔗 Related Documentation

- **CLAUDE.md**: AI assistant instructions and project patterns
- **DECISION_LOG.json**: Project decision history and rationale
- **TODO_FOR_HUMAN.md**: Current human-readable task summary
- **TODO_FOR_AI.json**: Technical task data structure
- **GitHub Issues**: Source of truth for all project tasks

## 📞 Support

### Quick Reference Commands
```bash
# Basic sync
./scripts/sync_todos.sh

# Check status
gh auth status && git status

# Emergency restore
cp .todo_backups/TODO_FOR_AI_LATEST.json TODO_FOR_AI.json

# Validate setup
gh repo view && python3 --version
```

### Getting Help
1. Check this guide for common issues
2. Review script output for specific error messages
3. Validate GitHub CLI authentication and repository access
4. Check file permissions and Python availability
5. Review backup files for recovery options

---

*Last updated: 2025-08-21*  
*Project: YuiQuery Healthcare Analytics Research*  
*Script version: 1.0.0*