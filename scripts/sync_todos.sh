#!/bin/bash
# File: sync_todos.sh
# Project: YuiQuery Healthcare Analytics Research
# Type: Academic research documentation project
# Focus: Natural language to SQL in healthcare
# Updated: 2025-08-21

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m' 
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory and repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${BLUE}YuiQuery Healthcare Research TODO Sync Automation${NC}"
echo "=================================================="

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

# Check GitHub CLI
if ! command -v gh &> /dev/null; then
    echo -e "${RED}GitHub CLI (gh) not found. Please install it first:${NC}"
    echo "   brew install gh"
    echo "   # or visit: https://cli.github.com/"
    exit 1
fi

# Check if authenticated with GitHub
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Not authenticated with GitHub. Please run:${NC}"
    echo "   gh auth login"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 not found. Please install Python 3.${NC}"
    exit 1
fi

# Verify we're in a git repository
if ! git rev-parse --git-dir &> /dev/null; then
    echo -e "${RED}Not in a git repository.${NC}"
    exit 1
fi

# Verify we're in the correct repository (optional safety check)
REPO_NAME=$(gh repo view --json name --jq .name 2>/dev/null || echo "unknown")
if [[ "$REPO_NAME" != "yuimedi-20250901" ]]; then
if [[ "$REPO_NAME" != "$EXPECTED_REPO_NAME" ]]; then
    echo -e "${YELLOW}Warning: Repository name '$REPO_NAME' doesn't match expected '$EXPECTED_REPO_NAME'${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Sync cancelled by user${NC}"
        exit 0
    fi
fi

echo -e "${GREEN}Prerequisites verified${NC}"

# Change to repository root
cd "$REPO_ROOT"

# Backup existing TODO files (if they exist)
BACKUP_DIR="$REPO_ROOT/.todo_backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if [[ -f "TODO_FOR_AI.json" || -f "TODO_FOR_HUMAN.md" ]]; then
    echo -e "${BLUE}Creating backup of existing TODO files...${NC}"
    mkdir -p "$BACKUP_DIR"
    
    if [[ -f "TODO_FOR_AI.json" ]]; then
        cp "TODO_FOR_AI.json" "$BACKUP_DIR/TODO_FOR_AI_${TIMESTAMP}.json"
        echo "   Backed up: TODO_FOR_AI.json -> $BACKUP_DIR/TODO_FOR_AI_${TIMESTAMP}.json"
    fi
    
    if [[ -f "TODO_FOR_HUMAN.md" ]]; then
        cp "TODO_FOR_HUMAN.md" "$BACKUP_DIR/TODO_FOR_HUMAN_${TIMESTAMP}.md"
        echo "   Backed up: TODO_FOR_HUMAN.md -> $BACKUP_DIR/TODO_FOR_HUMAN_${TIMESTAMP}.md"
    fi
fi

# Activate UV environment and run the Python sync script
echo -e "${BLUE}Running GitHub <-> TODO synchronization...${NC}"

# Check if UV environment exists
if [[ ! -d "$REPO_ROOT/.venv" ]]; then
    echo -e "${YELLOW}UV environment not found.${NC}"
    echo "   To set up the environment, run:"
    echo "      uv venv"
    echo "      source .venv/bin/activate"
    echo "      uv pip install -e ."
    exit 1
fi

# Activate UV environment and run sync
if (source "$REPO_ROOT/.venv/bin/activate" && python "$SCRIPT_DIR/sync_github_todos.py"); then
    echo -e "${GREEN}Synchronization completed successfully${NC}"
else
    echo -e "${RED}Synchronization failed${NC}"
    
    # Restore backups if sync failed
    if [[ -d "$BACKUP_DIR" ]]; then
        echo -e "${YELLOW}Restoring backup files...${NC}"
        if [[ -f "$BACKUP_DIR/TODO_FOR_AI_${TIMESTAMP}.json" ]]; then
            cp "$BACKUP_DIR/TODO_FOR_AI_${TIMESTAMP}.json" "TODO_FOR_AI.json"
            echo "   Restored: TODO_FOR_AI.json"
        fi
        if [[ -f "$BACKUP_DIR/TODO_FOR_HUMAN_${TIMESTAMP}.md" ]]; then
            cp "$BACKUP_DIR/TODO_FOR_HUMAN_${TIMESTAMP}.md" "TODO_FOR_HUMAN.md"
            echo "   Restored: TODO_FOR_HUMAN.md"
        fi
    fi
    
    exit 1
fi

# Check for changes in TODO files
echo -e "${BLUE}Checking for changes to commit...${NC}"

CHANGES_DETECTED=false
FILES_TO_COMMIT=()

# Check TODO_FOR_AI.json
if git diff --quiet HEAD -- "TODO_FOR_AI.json" 2>/dev/null; then
    echo "   No changes in TODO_FOR_AI.json"
else
    echo "   Changes detected in TODO_FOR_AI.json"
    FILES_TO_COMMIT+=("TODO_FOR_AI.json")
    CHANGES_DETECTED=true
fi

# Check TODO_FOR_HUMAN.md
if git diff --quiet HEAD -- "TODO_FOR_HUMAN.md" 2>/dev/null; then
    echo "   No changes in TODO_FOR_HUMAN.md"
else
    echo "   Changes detected in TODO_FOR_HUMAN.md"
    FILES_TO_COMMIT+=("TODO_FOR_HUMAN.md")
    CHANGES_DETECTED=true
fi

# If changes detected, commit them
if [[ "$CHANGES_DETECTED" == true ]]; then
    echo -e "${BLUE}Committing TODO file changes...${NC}"
    
    # Add changed files
    for file in "${FILES_TO_COMMIT[@]}"; do
        git add "$file"
        echo "   Added: $file"
    done
    
    # Create commit with proper message format (using HEREDOC as specified in CLAUDE.md)
    COMMIT_MESSAGE=$(cat <<'COMMIT_MSG'
chore: sync TODO files with GitHub issues

Bidirectional synchronization between GitHub issues and local TODO files:
- Updated TODO_FOR_AI.json with research task metadata and priorities  
- Regenerated TODO_FOR_HUMAN.md with current research status
    COMMIT_MESSAGE=$(cat <<COMMIT_MSG
chore: sync TODO files with GitHub issues

Bidirectional synchronization between GitHub issues and local TODO files:
- Updated TODO_FOR_AI.json with research task metadata and priorities  
- Regenerated TODO_FOR_HUMAN.md with current research status
- Aligned with ${PROJECT_NAME} ${WORKFLOW_NAME}

Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
COMMIT_MSG
    )
    
    if git commit -m "$COMMIT_MESSAGE"; then
        echo -e "${GREEN}Changes committed successfully${NC}"
        
        # Show commit details
        echo -e "${BLUE}Commit details:${NC}"
        git show --stat HEAD
        
        # Ask about pushing changes
        echo -e "${YELLOW}Push changes to remote repository?${NC}"
        read -p "Push to remote? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if git push; then
                echo -e "${GREEN}Changes pushed to remote repository${NC}"
            else
                echo -e "${RED}Failed to push changes. You may need to pull first.${NC}"
                echo "   Run: git pull --rebase && git push"
            fi
        else
            echo -e "${YELLOW}Changes committed locally but not pushed${NC}"
            echo "   To push later: git push"
        fi
        
    else
        echo -e "${RED}Failed to commit changes${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}No changes to commit - TODO files are up to date${NC}"
fi

# Clean up old backups (keep last 5)
if [[ -d "$BACKUP_DIR" ]]; then
    echo -e "${BLUE}Cleaning up old backups...${NC}"
    
    # Count backup files
    BACKUP_COUNT=$(find "$BACKUP_DIR" -name "TODO_FOR_*_*.json" -o -name "TODO_FOR_*_*.md" | wc -l)
    
    if [[ $BACKUP_COUNT -gt 10 ]]; then
        echo "   Removing old backups (keeping last 10)..."
        # Remove backups older than 7 days
        find "$BACKUP_DIR" -name "TODO_FOR_*_*" -type f -mtime +7 -delete
    fi
fi

# Final summary
echo
echo -e "${GREEN}YuiQuery Healthcare Research TODO sync completed successfully!${NC}"
echo "=================================================="

# Show current task summary
if [[ -f "TODO_FOR_AI.json" ]]; then
    echo -e "${BLUE}Current task summary:${NC}"
    
    # Extract summary using Python one-liner
    python3 -c "
import json
try:
    with open('TODO_FOR_AI.json', 'r') as f:
        data = json.load(f)
    
    total = data.get('sync_metadata', {}).get('total_tasks', 0)
    github_issues = data.get('sync_metadata', {}).get('total_github_issues', 0)
    priority_dist = data.get('priority_distribution', {})
    status_dist = data.get('status_distribution', {})
    
    print(f'   Total tasks: {total}')
    print(f'   GitHub issues: {github_issues}')
    print(f'   Critical (P0): {priority_dist.get(\"P0\", 0)}')
    print(f'   High priority (P1): {priority_dist.get(\"P1\", 0)}')
    print(f'   In progress: {status_dist.get(\"in_progress\", 0)}')
    print(f'   Blocked: {status_dist.get(\"blocked\", 0)}')
    
except Exception as e:
    print(f'   Error reading summary: {e}')
"
fi

echo
echo -e "${BLUE}Next steps:${NC}"
echo "   • Review TODO_FOR_HUMAN.md for priority tasks"
echo "   • Check TODO_FOR_AI.json for technical implementation details" 
echo "   • Run this script regularly to keep GitHub and local TODOs in sync"
echo "   • Use 'gh issue create' to add new tasks that will sync automatically"

echo
echo -e "${GREEN}All done! Happy researching!${NC}"