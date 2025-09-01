# Scripts Directory

This directory contains automation scripts for the YuiQuery Healthcare Analytics Research project, focusing on GitHub integration and TODO management for academic research workflows.

## 📁 Directory Contents

```
scripts/
├── README.md                 # This file - overview and documentation
├── SYNC_GUIDE.md            # Comprehensive usage guide for sync system
├── sync_todos.sh            # Main automation script (bash)
└── sync_github_todos.py     # Core synchronization engine (Python)
```

## 🎯 Purpose

These scripts enable seamless integration between GitHub Issues and local TODO files, providing:

- **True bidirectional synchronization** - Creates GitHub Issues from TODO tasks AND syncs back
- **Academic workflow optimization** for research documentation projects
- **Automated project management** with priority tracking and status updates
- **Team collaboration support** through consistent task visibility
- **Zero-setup compatibility** - Works with empty repositories or existing GitHub Issues

## 🚀 Quick Start

### Essential Commands
```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create UV environment and install dependencies
uv venv
uv pip install -e ".[dev]"

# Make scripts executable
chmod +x scripts/sync_todos.sh

# Run complete synchronization
./scripts/sync_todos.sh

# View comprehensive guide
open scripts/SYNC_GUIDE.md
```

### Prerequisites
- UV (Python package manager) installed
- GitHub CLI (`gh`) installed and authenticated  
- Git repository with GitHub remote
- Python 3.8+ (automatically managed by UV)

## 📋 Script Descriptions

### sync_todos.sh
**Main automation wrapper script**

- **Language**: Bash shell script
- **Purpose**: Complete workflow automation for GitHub ↔ TODO synchronization
- **Features**:
  - **True bidirectional sync**: Creates GitHub Issues from TODO tasks AND syncs back
  - **Empty repository support**: Works with repositories that have no GitHub Issues
  - Prerequisites verification (GitHub CLI, Python, authentication)
  - Automatic backup creation before sync
  - Error handling and recovery
  - Git integration with proper commit messages
  - User-friendly output with colored status indicators
  - Cleanup of old backup files

**Usage:**
```bash
./scripts/sync_todos.sh                    # Interactive mode
echo -e "y\ny" | ./scripts/sync_todos.sh   # Automated mode
bash -x ./scripts/sync_todos.sh            # Debug mode
```

### sync_github_todos.py
**Core synchronization engine**

- **Language**: Python 3
- **Purpose**: Bidirectional data transformation between GitHub Issues and TODO formats
- **Features**:
  - **Bidirectional sync**: TODO → GitHub (creates missing issues) AND GitHub → TODO (updates data)
  - **Empty repository handling**: Gracefully handles repositories with no GitHub Issues
  - GitHub Issues API integration via `gh` CLI
  - Metadata parsing from issue descriptions (priority, status, dependencies)
  - GitHub Issue creation with proper metadata formatting
  - JSON structure generation for AI workflow integration
  - Human-readable Markdown generation
  - Validation and consistency checking
  - Healthcare research project optimizations

**Key Functions:**
- `fetch_github_issues()` - Retrieves all repository issues
- `load_existing_todo()` - Loads current TODO_FOR_AI.json file
- `create_github_issue()` - Creates individual GitHub Issues with metadata
- `sync_to_github()` - Creates GitHub Issues from TODO tasks (TODO → GitHub)
- `parse_issue_metadata()` - Extracts structured data from issue descriptions
- `github_to_todo()` - Converts GitHub format to TODO structure
- `sync_from_github()` - Updates TODO files from GitHub Issues (GitHub → TODO)
- `update_todo_ai_file()` - Generates structured JSON for AI assistants
- `generate_human_markdown()` - Creates human-readable task summary

### SYNC_GUIDE.md
**Comprehensive usage documentation**

- **Type**: User documentation
- **Purpose**: Complete reference guide for sync system usage
- **Covers**:
  - Detailed usage instructions
  - GitHub issue configuration
  - Troubleshooting and recovery
  - Advanced configuration options
  - Best practices and workflows
  - Integration examples

## 🔧 Configuration

### GitHub Issue Metadata Format
The sync system recognizes these HTML comments in GitHub issue descriptions:

```markdown
<!-- priority: P0 -->  # Critical (blocks research progress)
<!-- priority: P1 -->  # High (important for completion)
<!-- priority: P2 -->  # Medium (standard tasks, default)
<!-- priority: P3 -->  # Low (optional enhancements)

<!-- status: todo -->         # Not started
<!-- status: in_progress -->   # Currently working
<!-- status: blocked -->       # Waiting on dependencies
<!-- status: done -->          # Completed

<!-- depends-on: #123, #456 --> # Task dependencies
```

### Repository Settings
Default configuration expects repository name `yuimedi-paper-20250901`. To customize:

1. Edit `sync_todos.sh` line 56:
   ```bash
   if [[ "$REPO_NAME" != "your-repo-name" ]]; then
   ```

2. Update project information in `sync_github_todos.py` lines 27-32:
   ```python
   self.project_info = {
       "type": "your_project_type",
       "focus": "your_research_focus",
       "documentation_only": True,
       "research_phase": "your_phase"
   }
   ```

## 📊 Generated Files

### TODO_FOR_AI.json
Structured task data optimized for AI workflow integration:

```json
{
  "project": "YuiQuery Healthcare Analytics Research",
  "version": "1.0.0",
  "type": "Academic research documentation",
  "updated": "2025-08-21T14:30:52Z",
  "sync_metadata": {
    "total_github_issues": 15,
    "total_tasks": 18,
    "validation_status": "synced"
  },
  "tasks": [...],
  "priority_distribution": {"P0": 2, "P1": 5, "P2": 8, "P3": 3},
  "status_distribution": {"todo": 8, "in_progress": 3, "blocked": 1, "done": 6}
}
```

### TODO_FOR_HUMAN.md
Human-readable task summary organized by priority:

```markdown
# TODO for Human Review

## Priority 0 - Critical
> **CRITICAL**: Essential research tasks blocking publication progress

- [ ] **[#145]** Complete systematic literature review validation
  - Status: `in_progress`
  - Dependencies: #134, #156

## Priority 1 - High
> **HIGH**: Important research components for whitepaper completion

[Additional priority sections...]

## Blocked Tasks
[Tasks waiting on dependencies...]

## Recently Completed
[Recent accomplishments for reference...]
```

### Backup Files
Automatic backups stored in `.todo_backups/`:

```
.todo_backups/
├── TODO_FOR_AI_20250821_143052.json
├── TODO_FOR_HUMAN_20250821_143052.md
├── TODO_FOR_AI_20250820_091234.json
└── TODO_FOR_HUMAN_20250820_091234.md
```

## 🔄 Workflow Integration

### Academic Research Workflow
```bash
# Daily research routine
./scripts/sync_todos.sh          # Sync latest changes
open TODO_FOR_HUMAN.md           # Review priorities
# ... work on research tasks ...
# ... update GitHub issue status ...
./scripts/sync_todos.sh          # Sync progress at end of day
```

### Team Collaboration
```bash
# Create new research task
gh issue create --title "Validate Section 3.2 Claims" \
  --body "<!-- priority: P1 -->$(cat task_description.md)"

# Assign to team member
gh issue edit 123 --add-assignee researcher-username

# Track progress
./scripts/sync_todos.sh
grep "in_progress" TODO_FOR_HUMAN.md
```

### Publication Preparation
```bash
# Check critical tasks before submission
./scripts/sync_todos.sh
jq '.tasks[] | select(.priority == "P0") | {title, status}' TODO_FOR_AI.json

# Generate final task report
jq '.status_distribution' TODO_FOR_AI.json
```

## 🛠️ Troubleshooting

### Quick Diagnostics
```bash
# Check UV environment
uv --version && source .venv/bin/activate && python --version

# Check prerequisites
gh auth status && git status

# Verify repository access
gh repo view

# Test sync components (with UV environment)
source .venv/bin/activate && python scripts/sync_github_todos.py
```

### Common Issues

**GitHub Authentication:**
```bash
gh auth login --web
gh auth status
```

**Repository Access:**
```bash
gh repo view  # Should show repository details
```

**UV Environment Setup:**
```bash
# Install UV if not available
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Install project with dev dependencies
uv pip install -e ".[dev]"

# Verify environment
source .venv/bin/activate && python --version  # Should be 3.8+
```

**File Permissions:**
```bash
chmod +x scripts/sync_todos.sh
ls -la scripts/
```

### Recovery Procedures

**Restore from Backup:**
```bash
# List available backups
ls -la .todo_backups/

# Restore specific backup
cp .todo_backups/TODO_FOR_AI_20250821_143052.json TODO_FOR_AI.json
cp .todo_backups/TODO_FOR_HUMAN_20250821_143052.md TODO_FOR_HUMAN.md
```

**Manual Sync Recovery:**
```bash
# If sync fails, run components individually
python3 scripts/sync_github_todos.py

# Check output for errors
echo $?  # Should be 0 for success

# Manually commit if needed
git add TODO_FOR_AI.json TODO_FOR_HUMAN.md
git commit -m "chore: manual TODO sync"
```

## 📈 Advanced Usage

### Custom Priority Mapping
Modify `sync_github_todos.py` to support custom priority formats:

```python
# Line 66 - Add custom priority patterns
priority_match = re.search(r'<!-- priority:\s*(P\d|Critical|High|Medium|Low|Urgent) -->', body, re.IGNORECASE)
```

### Automated Integration
```yaml
# GitHub Actions workflow
name: Sync TODOs
on:
  issues:
    types: [opened, edited, closed, reopened]
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup GitHub CLI
        run: gh auth login --with-token <<< "${{ secrets.GITHUB_TOKEN }}"
      - name: Run TODO Sync
        run: |
          chmod +x scripts/sync_todos.sh
          echo -e "y\ny" | ./scripts/sync_todos.sh
```

### IDE Integration
```json
// VS Code tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Sync Research TODOs",
      "type": "shell",
      "command": "./scripts/sync_todos.sh",
      "group": "build",
      "presentation": {"echo": true, "reveal": "always"},
      "problemMatcher": []
    }
  ]
}
```

## 📊 Analytics and Monitoring

### Task Metrics
```bash
# Priority distribution
jq '.priority_distribution' TODO_FOR_AI.json

# Status breakdown
jq '.status_distribution' TODO_FOR_AI.json

# Assignee workload
jq '[.tasks[] | select(.assignee != null) | .assignee] | group_by(.) | map({assignee: .[0], count: length})' TODO_FOR_AI.json

# Blocked tasks analysis
jq '.tasks[] | select(.status == "blocked") | {title, dependencies}' TODO_FOR_AI.json
```

### Progress Tracking
```bash
# Critical path items
jq '.tasks[] | select(.priority == "P0" or .priority == "P1") | {title, status, dependencies}' TODO_FOR_AI.json

# Recent completions
jq '.tasks[] | select(.status == "done") | {title, completed: .updated_at}' TODO_FOR_AI.json | tail -10

# Velocity calculation
jq '[.tasks[] | select(.status == "done")] | length' TODO_FOR_AI.json
```

## 🔗 Integration with Project Systems

### Related Files
- `../TODO_FOR_AI.json` - Generated structured task data
- `../TODO_FOR_HUMAN.md` - Generated human-readable summary
- `../DECISION_LOG.json` - Project decision history
- `../CLAUDE.md` - AI assistant instructions

### Dependency Chain
```
GitHub Issues (source of truth)
       ↓
sync_github_todos.py (data transformation)
       ↓
TODO_FOR_AI.json (structured data)
       ↓
TODO_FOR_HUMAN.md (human summary)
       ↓
Git commits (version control)
```

## 📚 Best Practices

### Script Usage
1. **Run sync regularly** - Keep GitHub and local files consistent
2. **Review output** - Check for errors or validation warnings
3. **Backup awareness** - Know where backups are stored
4. **Test before automation** - Verify manual sync works before automating

### GitHub Issue Management
1. **Use metadata comments** - Always include priority and status
2. **Descriptive titles** - Make issues easy to understand
3. **Link dependencies** - Use `depends-on` for task relationships
4. **Update progress** - Change status as work progresses
5. **Close completed tasks** - Don't leave finished work open

### File Management
1. **Don't edit TODO files manually** - Always use GitHub as source
2. **Commit sync results** - Include TODO updates in version control
3. **Preserve backups** - Keep `.todo_backups/` directory
4. **Monitor disk usage** - Clean old backups periodically

## 🔄 Maintenance

### Regular Tasks
```bash
# Weekly backup cleanup
find .todo_backups/ -name "TODO_FOR_*" -type f -mtime +7 -delete

# Monthly validation
./scripts/sync_todos.sh
python3 scripts/sync_github_todos.py

# Check for script updates
git log --oneline scripts/
```

### Version Updates
1. Update version numbers in script headers
2. Update documentation dates
3. Test with new GitHub CLI versions
4. Validate Python compatibility

## 📞 Support

### Quick Reference
```bash
# Essential commands
./scripts/sync_todos.sh                    # Main sync
gh auth status                             # Check GitHub auth
python3 scripts/sync_github_todos.py      # Test core sync
cp .todo_backups/TODO_FOR_AI_LATEST.json TODO_FOR_AI.json  # Emergency restore
```

### Getting Help
1. Check `SYNC_GUIDE.md` for detailed usage instructions
2. Review script output for specific error messages
3. Validate GitHub CLI authentication and repository access
4. Verify Python availability and script permissions
5. Check backup files for recovery options

---

*Directory: `/scripts/`*  
*Project: YuiQuery Healthcare Analytics Research*  
*Updated: 2025-08-21*  
*Type: Academic research automation*