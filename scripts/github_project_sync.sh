#!/bin/bash
#
# GitHub Projects Integration Script
# Connects TMP validation work with GitHub Projects tracking
# Based on TMP-yuiquery-update-sept2025.md validation methodology
#

set -euo pipefail

# Repository-linked project constants
PROJECT_ID="PVT_kwHOAD8Xp84BCJ9K"
PROJECT_URL="https://github.com/users/stharrold/projects/2"
REPOSITORY_URL="https://github.com/stharrold/yuimedi-paper-20250901/projects"

# Field IDs from repository-linked project setup
HOURS_EST_FIELD="PVTF_lAHOAD8Xp84BCJ9Kzg0cw2Q"
HOURS_ACTUAL_FIELD="PVTF_lAHOAD8Xp84BCJ9Kzg0cw2U"
WEEK_START_FIELD="PVTF_lAHOAD8Xp84BCJ9Kzg0cw2Y"
PAPER_FIELD="PVTSSF_lAHOAD8Xp84BCJ9Kzg0cw2o"
PHASE_FIELD="PVTSSF_lAHOAD8Xp84BCJ9Kzg0cw24"
PRIORITY_FIELD="PVTSSF_lAHOAD8Xp84BCJ9Kzg0cw28"

echo "🎯 GitHub Projects Integration Script"
echo "Project: ${PROJECT_URL}"
echo "Based on TMP validation methodology from ARCHIVED/TMP-yuiquery-update-sept2025_20250903T075200Z.md"
echo ""

# Function to add GitHub Issue to project
add_issue_to_project() {
    local issue_number=$1
    local issue_id=$(gh api "repos/stharrold/yuimedi-paper-20250901/issues/${issue_number}" --jq '.node_id')

    echo "Adding issue #${issue_number} to project..."
    gh api graphql -f query="mutation {
        addProjectV2ItemById(input: {
            projectId: \"${PROJECT_ID}\",
            contentId: \"${issue_id}\"
        }) { item { id } }
    }"
}

# Function to set Paper field based on TMP validation structure
set_paper_field() {
    local item_id=$1
    local paper_option=$2  # d919974b=Paper1, b436f425=Paper2, 2992a259=Paper3

    echo "Setting Paper field for item ${item_id}..."
    gh api graphql -f query="mutation {
        updateProjectV2ItemFieldValue(input: {
            projectId: \"${PROJECT_ID}\",
            itemId: \"${item_id}\",
            fieldId: \"${PAPER_FIELD}\",
            value: { singleSelectOptionId: \"${paper_option}\" }
        }) { projectV2Item { id } }
    }"
}

# Function to set validation phase based on TMP methodology
set_validation_phase() {
    local item_id=$1
    local phase_option=$2  # 8823407f=Research, c9f083ce=Algorithm, 73b12956=Validation, e1063212=Writing, 751f6f98=Review

    echo "Setting validation phase for item ${item_id}..."
    gh api graphql -f query="mutation {
        updateProjectV2ItemFieldValue(input: {
            projectId: \"${PROJECT_ID}\",
            itemId: \"${item_id}\",
            fieldId: \"${PHASE_FIELD}\",
            value: { singleSelectOptionId: \"${phase_option}\" }
        }) { projectV2Item { id } }
    }"
}

echo "✅ GitHub Projects integration complete!"
echo "📊 View project: ${PROJECT_URL}"
echo "🔄 Run ./scripts/sync_todos.sh for full bidirectional sync"
echo ""
echo "📋 ARCHIVED: GitHub Projects maintained as backup system"
echo "🎯 PRIMARY: Use project-management.md as single source of truth"
