#!/usr/bin/env python3
"""
File: sync_github_todos.py
Project: YuiQuery Healthcare Analytics Research
Type: Academic research documentation project
Updated: 2025-08-21

GitHub <-> TODO Bidirectional Sync System
Synchronizes GitHub issues with TODO_FOR_AI.json and TODO_FOR_HUMAN.md
Adapted for research documentation and academic workflow management
"""

import json
import re
import subprocess
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


class YuiQueryGitHubSync:
    """Bidirectional sync between GitHub issues and YuiQuery research TODO files"""

    def __init__(self) -> None:
        self.repo_root = Path(__file__).parent.parent
        self.todo_ai_path = self.repo_root / "TODO_FOR_AI.json"
        self.todo_human_path = self.repo_root / "TODO_FOR_HUMAN.md"
        self.github_repo = "stharrold/yuimedi-paper-20250901"
        self.project_info: dict[str, Any] = {
            "type": "academic_research",
            "focus": "natural_language_sql_healthcare",
            "documentation_only": True,
            "research_phase": "whitepaper_development",
        }

    def fetch_github_issues(self) -> Optional[list[dict[str, Any]]]:
        """Fetch all issues from GitHub repository"""
        try:
            cmd = [
                "gh",
                "issue",
                "list",
                "--json",
                "number,title,body,labels,assignees,state,createdAt,updatedAt",
                "--limit",
                "1000",
                "--state",
                "all",  # Include both open and closed issues
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            issues: list[dict[str, Any]] = json.loads(result.stdout)
            return issues
        except subprocess.CalledProcessError as e:
            print(f"Error fetching GitHub issues: {e}")
            print(f"   Command: {' '.join(cmd)}")
            print(f"   Error output: {e.stderr}")
            return None  # Return None for actual errors
        except json.JSONDecodeError as e:
            print(f"Error parsing GitHub response: {e}")
            return None  # Return None for parsing errors

    def parse_issue_metadata(self, body: Optional[str]) -> dict[str, Any]:
        """Extract structured metadata from GitHub issue body"""
        if not body:
            body = ""

        metadata = {
            "priority": "P2",  # Default medium priority
            "dependencies": [],
            "status": "todo",  # Default status
        }

        # Parse priority: <!-- priority: P0 -->
        priority_match = re.search(r"<!-- priority:\s*(P\d) -->", body, re.IGNORECASE)
        if priority_match:
            metadata["priority"] = priority_match.group(1).upper()

        # Parse dependencies: <!-- depends-on: #123, #456 -->
        deps_match = re.search(r"<!-- depends-on:\s*([\d,\s#]+) -->", body, re.IGNORECASE)
        if deps_match:
            # Extract issue numbers from dependency string
            dep_numbers = re.findall(r"\d+", deps_match.group(1))
            metadata["dependencies"] = [f"gh-{num}" for num in dep_numbers]

        # Parse status: <!-- status: in_progress -->
        status_match = re.search(r"<!-- status:\s*(\w+) -->", body, re.IGNORECASE)
        if status_match:
            status = status_match.group(1).lower()
            if status in ["todo", "in_progress", "blocked", "done"]:
                metadata["status"] = status

        # Special handling for closed issues
        return metadata

    def github_to_todo(self, issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Convert GitHub issues to TODO_FOR_AI.json format"""
        print("Converting GitHub issues to TODO format...")

        ai_tasks = []
        for issue in issues:
            metadata = self.parse_issue_metadata(issue.get("body", ""))

            # Determine status from GitHub state (case-insensitive)
            if issue["state"].upper() == "CLOSED":
                metadata["status"] = "done"

            # Clean description (remove metadata comments)
            description = issue.get("body", "") or f"GitHub issue #{issue['number']}"
            # Remove only metadata HTML comments (priority, depends-on, status)
            description = re.sub(
                r"<!--\s*priority:\s*P\d\s*-->", "", description, flags=re.IGNORECASE
            )
            description = re.sub(
                r"<!--\s*depends-on:\s*[\d,\s#]+\s*-->", "", description, flags=re.IGNORECASE
            )
            description = re.sub(
                r"<!--\s*status:\s*\w+\s*-->", "", description, flags=re.IGNORECASE
            )
            description = description.strip()
            if not description:
                issue_number = issue.get("number")
                if isinstance(issue_number, int) and issue_number > 0:
                    fallback_desc = f"GitHub issue #{issue_number}"
                else:
                    fallback_desc = "GitHub issue (number unknown)"
                description = fallback_desc

            task = {
                "id": f"gh-{issue['number']}",
                "github_issue_number": issue["number"],
                "title": issue["title"],
                "description": description[:500] + "..." if len(description) > 500 else description,
                "priority": metadata["priority"],
                "status": metadata["status"],
                "dependencies": metadata["dependencies"],
                "labels": [label["name"] for label in issue.get("labels", [])],
                "assignee": issue["assignees"][0]["login"] if issue.get("assignees") else None,
                "created_at": issue["createdAt"],
                "updated_at": issue["updatedAt"],
                "implementation_notes": {
                    "github_sync": True,
                    "last_sync": datetime.now(timezone.utc).isoformat(),
                    "issue_state": issue["state"],
                },
            }
            ai_tasks.append(task)

        return ai_tasks

    def update_todo_ai_file(self, github_tasks: list[dict[str, Any]]) -> Optional[dict[str, Any]]:
        """Update TODO_FOR_AI.json with GitHub data"""
        print("Updating TODO_FOR_AI.json...")

        try:
            # Load existing TODO file if it exists
            existing_data = {}
            if self.todo_ai_path.exists():
                with open(self.todo_ai_path) as f:
                    existing_data = json.load(f)

            # Preserve internal tasks (non-GitHub tasks)
            existing_tasks = existing_data.get("tasks", [])
            internal_tasks = [
                task for task in existing_tasks if not task.get("github_issue_number")
            ]

            # Combine GitHub tasks with internal tasks
            all_tasks = github_tasks + internal_tasks

            # Sort by priority and issue number
            priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
            all_tasks.sort(
                key=lambda x: (
                    priority_order.get(x["priority"], 4),
                    x.get("github_issue_number") or 9999,
                )
            )

            # Calculate status distribution
            status_dist: dict[str, int] = {}
            priority_dist: dict[str, int] = {}
            for task in all_tasks:
                status = task["status"]
                priority = task["priority"]
                status_dist[status] = status_dist.get(status, 0) + 1
                priority_dist[priority] = priority_dist.get(priority, 0) + 1

            # Update TODO_FOR_AI.json
            todo_data = {
                "project": "YuiQuery Healthcare Analytics Research",
                "version": "1.0.0",
                "type": "Academic research documentation",
                "focus": "Natural language to SQL in healthcare",
                "updated": datetime.now(timezone.utc).isoformat(),
                "last_sync": datetime.now(timezone.utc).isoformat(),
                "sync_source": "github_bidirectional_sync",
                "sync_metadata": {
                    "github_repo": self.github_repo,
                    "sync_direction": "bidirectional",
                    "last_github_fetch": datetime.now(timezone.utc).isoformat(),
                    "total_github_issues": len(github_tasks),
                    "total_tasks": len(all_tasks),
                    "sync_conflicts": [],
                    "validation_status": "synced",
                },
                "tasks": all_tasks,
                "priority_distribution": priority_dist,
                "status_distribution": status_dist,
                "ai_workflow_integration": existing_data.get("ai_workflow_integration", {}),
                "github_sync_instructions": existing_data.get("github_sync_instructions", {}),
            }

            with open(self.todo_ai_path, "w") as f:
                json.dump(todo_data, f, indent=2)

            print(f"Updated TODO_FOR_AI.json with {len(all_tasks)} tasks")
            return todo_data

        except Exception as e:
            print(f"Error updating TODO_FOR_AI.json: {e}")
            return None

    def generate_human_markdown(self, todo_data: dict[str, Any]) -> bool:
        """Generate human-readable TODO_FOR_HUMAN.md"""
        print("Generating TODO_FOR_HUMAN.md...")

        try:
            tasks = todo_data["tasks"]

            # Organize tasks by priority and status
            priorities: dict[str, list[dict[str, Any]]] = {"P0": [], "P1": [], "P2": [], "P3": []}
            blocked = []
            completed = []

            for task in tasks:
                if task["status"] == "blocked":
                    blocked.append(task)
                elif task["status"] == "done":
                    completed.append(task)
                else:
                    priority = task["priority"]
                    if priority in priorities:
                        priorities[priority].append(task)

            # Generate markdown content
            markdown_lines = [
                "# File: TODO_FOR_HUMAN.md",
                "# Project: YuiQuery Healthcare Analytics Research",
                "# Type: Academic research documentation",
                "# Focus: Natural language to SQL in healthcare",
                f"# Updated: {datetime.now().strftime('%Y-%m-%d')}",
                "",
                "# TODO for Human Review",
                "",
                f"Last Sync: {todo_data.get('last_sync', 'Unknown')}",
                "",
            ]

            # Priority sections
            priority_names = {
                "P0": "Priority 0 - Critical",
                "P1": "Priority 1 - High",
                "P2": "Priority 2 - Medium",
                "P3": "Priority 3 - Low",
            }

            priority_descriptions = {
                "P0": "> **CRITICAL**: Essential research tasks blocking publication progress",
                "P1": "> **HIGH**: Important research components for whitepaper completion",
                "P2": "> **MEDIUM**: Supporting research and documentation improvements",
                "P3": "> **LOW**: Optional enhancements and supplementary materials",
            }

            for priority in ["P0", "P1", "P2", "P3"]:
                if priorities[priority]:
                    markdown_lines.extend(
                        [f"## {priority_names[priority]}", priority_descriptions[priority], ""]
                    )

                    for task in priorities[priority]:
                        checkbox = "- [x]" if task["status"] == "done" else "- [ ]"
                        issue_ref = (
                            f"[#{task['github_issue_number']}]"
                            if task.get("github_issue_number")
                            else "(Internal Task)"
                        )

                        markdown_lines.append(f"{checkbox} **{issue_ref}** {task['title']}")

                        if task["dependencies"]:
                            dep_refs = []
                            for dep in task["dependencies"]:
                                if dep.startswith("gh-"):
                                    dep_refs.append(f"#{dep[3:]}")
                                else:
                                    dep_refs.append(dep)
                            markdown_lines.append(f"  - Dependencies: {', '.join(dep_refs)}")

                        markdown_lines.append(f"  - Status: `{task['status']}`")

                        if task["description"]:
                            desc = (
                                task["description"][:100] + "..."
                                if len(task["description"]) > 100
                                else task["description"]
                            )
                            markdown_lines.append(f"  - Details: {desc}")

                        markdown_lines.append("")

            # Blocked tasks section
            if blocked:
                markdown_lines.extend(
                    [
                        "## Blocked Tasks",
                        "> **BLOCKED**: Tasks waiting on dependencies or external factors",
                        "",
                    ]
                )

                for task in blocked:
                    issue_ref = (
                        f"[#{task['github_issue_number']}]"
                        if task.get("github_issue_number")
                        else "(Internal Task)"
                    )
                    markdown_lines.append(f"- [ ] **{issue_ref}** {task['title']}")

                    if task["dependencies"]:
                        dep_refs = [
                            f"#{dep[3:]}" if dep.startswith("gh-") else dep
                            for dep in task["dependencies"]
                        ]
                        markdown_lines.append(f"  - Blocked by: {', '.join(dep_refs)}")

                    markdown_lines.append(
                        f"  - Reason: {task.get('description', 'Waiting on dependencies')[:100]}..."
                    )
                    markdown_lines.append("")

            # Recently completed section (last 5)
            if completed:
                recent_completed = sorted(
                    completed, key=lambda x: x.get("updated_at", ""), reverse=True
                )[:5]
                markdown_lines.extend(
                    [
                        "## Recently Completed",
                        "> **DONE**: Recently finished tasks for reference",
                        "",
                    ]
                )

                for task in recent_completed:
                    issue_ref = (
                        f"[#{task['github_issue_number']}]"
                        if task.get("github_issue_number")
                        else "(Internal Task)"
                    )
                    update_date = task.get("updated_at", "")
                    if update_date:
                        try:
                            date_obj = datetime.fromisoformat(update_date.replace("Z", "+00:00"))
                            date_str = date_obj.strftime("%Y-%m-%d")
                        except (ValueError, AttributeError):
                            date_str = ""
                    else:
                        date_str = ""

                    markdown_lines.append(f"- [x] **{issue_ref}** {task['title']} ({date_str})")
                    if task["description"]:
                        desc = (
                            task["description"][:80] + "..."
                            if len(task["description"]) > 80
                            else task["description"]
                        )
                        markdown_lines.append(f"  - {desc}")
                    markdown_lines.append("")

            # Sync metadata
            markdown_lines.extend(
                [
                    "## Sync Metadata",
                    "```json",
                    json.dumps(
                        {
                            "version": "1.0.0",
                            "last_sync_source": "github_bidirectional_sync",
                            "github_issues_total": todo_data["sync_metadata"][
                                "total_github_issues"
                            ],
                            "total_tasks": todo_data["sync_metadata"]["total_tasks"],
                            "critical_tasks": todo_data["priority_distribution"].get("P0", 0),
                            "high_priority_tasks": todo_data["priority_distribution"].get("P1", 0),
                            "blocked_tasks": todo_data["status_distribution"].get("blocked", 0),
                            "completed_tasks": todo_data["status_distribution"].get("done", 0),
                        },
                        indent=2,
                    ),
                    "```",
                    "",
                    "---",
                    "",
                    f"*Last updated: {datetime.now().strftime('%Y-%m-%d')}*",
                    "*Sync status: GitHub bidirectional sync*",
                    "*For technical details, see: TODO_FOR_AI.json*",
                ]
            )

            # Write markdown file
            with open(self.todo_human_path, "w") as f:
                f.write("\n".join(markdown_lines))

            print(f"Generated TODO_FOR_HUMAN.md with {len(tasks)} tasks")
            return True

        except Exception as e:
            print(f"Error generating TODO_FOR_HUMAN.md: {e}")
            return False

    def sync_from_github(self) -> Optional[dict[str, Any]]:
        """Phase 1: Sync GitHub issues -> TODO files"""
        print("Phase 1: GitHub -> TODO sync")

        # Fetch GitHub issues
        issues = self.fetch_github_issues()
        if issues is None:
            print("Error fetching GitHub issues")
            return None

        if not issues:
            print("No GitHub issues found - proceeding with empty issue list")
        else:
            print(f"Found {len(issues)} GitHub issues")

        # Convert to TODO format
        github_tasks = self.github_to_todo(issues)

        # Update TODO_FOR_AI.json
        todo_data = self.update_todo_ai_file(github_tasks)
        if not todo_data:
            return None

        # Generate TODO_FOR_HUMAN.md
        self.generate_human_markdown(todo_data)

        return todo_data

    def validate_sync(self) -> bool:
        """Validate consistency between GitHub and TODO files"""
        print("Validating sync consistency...")

        try:
            # Load TODO data
            with open(self.todo_ai_path) as f:
                todo_data = json.load(f)

            # Get GitHub issues
            github_issues = self.fetch_github_issues()
            if github_issues is None:
                print("Error: Could not fetch GitHub issues for validation")
                return False

            # Extract issue numbers
            todo_github_tasks = [
                task for task in todo_data["tasks"] if task.get("github_issue_number")
            ]
            todo_numbers = {task["github_issue_number"] for task in todo_github_tasks}
            github_numbers = {issue["number"] for issue in github_issues}

            # Check for mismatches
            only_in_todo = todo_numbers - github_numbers
            only_in_github = github_numbers - todo_numbers

            issues_found = []
            if only_in_todo:
                issues_found.append(f"Issues only in TODO: {sorted(only_in_todo)}")
            if only_in_github:
                issues_found.append(f"Issues only in GitHub: {sorted(only_in_github)}")

            if issues_found:
                print("Sync inconsistencies found:")
                for issue in issues_found:
                    print(f"   {issue}")
                return False
            else:
                print("All GitHub issues synchronized with TODO files")
                return True

        except Exception as e:
            print(f"Error validating sync: {e}")
            return False

    def load_existing_todo(self) -> Optional[dict[str, Any]]:
        """Load existing TODO_FOR_AI.json file if it exists"""
        try:
            if self.todo_ai_path.exists():
                with open(self.todo_ai_path) as f:
                    data: dict[str, Any] = json.load(f)
                    return data
            else:
                print("No existing TODO_FOR_AI.json found")
                return None
        except Exception as e:
            print(f"Error loading existing TODO file: {e}")
            return None

    def create_github_issue(self, task: dict[str, Any]) -> Optional[int]:
        """Create a single GitHub issue from a TODO task"""
        try:
            # Format issue body with metadata
            body_lines = []

            # Add metadata comments
            if task.get("priority"):
                body_lines.append(f"<!-- priority: {task['priority']} -->")
            if task.get("status"):
                body_lines.append(f"<!-- status: {task['status']} -->")
            if task.get("dependencies"):
                deps = ", ".join(
                    [
                        f"#{dep.replace('gh-', '')}" if dep.startswith("gh-") else dep
                        for dep in task["dependencies"]
                    ]
                )
                body_lines.append(f"<!-- depends-on: {deps} -->")

            # Add empty line after metadata
            if body_lines:
                body_lines.append("")

            # Add task description
            body_lines.append(task.get("description", ""))

            # Add additional task information
            if task.get("created_at"):
                body_lines.extend(["", f"**Created**: {task['created_at']}"])
            if task.get("labels"):
                labels_str = ", ".join(task["labels"])
                body_lines.append(f"**Labels**: {labels_str}")

            body = "\n".join(body_lines)

            # Create GitHub issue using gh CLI
            cmd = ["gh", "issue", "create", "--title", task["title"], "--body", body]

            # Add labels if present (skip if they don't exist in repo)
            # Note: Labels will be ignored if they don't exist in the repository

            # Add assignee if present and it looks like a GitHub username (not DSH)
            assignee = task.get("assignee")
            if assignee and assignee != "DSH" and not assignee.startswith("YLT"):
                cmd.extend(["--assignee", assignee])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=60,
            )

            # Extract issue number from output (format: "https://github.com/user/repo/issues/123")
            issue_url = result.stdout.strip()
            issue_number = int(issue_url.split("/")[-1])

            print(f"   Created GitHub issue #{issue_number}: {task['title']}")
            return issue_number

        except subprocess.CalledProcessError as e:
            print(f"Error creating GitHub issue: {e}")
            print(f"   Command: {' '.join(cmd)}")
            print(f"   Error output: {e.stderr}")
            return None
        except Exception as e:
            print(f"Error creating GitHub issue for task '{task.get('title', 'Unknown')}': {e}")
            return None

    def sync_to_github(self, existing_todo_data: Optional[dict[str, Any]]) -> int:
        """Phase 0: Sync TODO tasks -> GitHub issues (create missing issues)"""
        if not existing_todo_data:
            print("No existing TODO data to sync to GitHub")
            return 0

        print("Phase 0: TODO -> GitHub sync (creating missing issues)")

        # Find tasks without GitHub issue numbers (internal tasks)
        internal_tasks = []
        existing_tasks = existing_todo_data.get("tasks", [])

        # Handle both old format (remainingSteps) and new format (tasks)
        if "remainingSteps" in existing_todo_data:
            for step in existing_todo_data["remainingSteps"]:
                internal_task = {
                    "id": f"internal-{step['step']}",
                    "title": step["description"],
                    "description": step["description"],
                    "priority": step.get("priority", "P2"),
                    "status": "todo",
                    "dependencies": [],
                    "labels": [],  # No labels to avoid repository label errors
                    "assignee": None,
                    "created_at": existing_todo_data.get("metadata", {}).get("last_updated", ""),
                }
                internal_tasks.append(internal_task)

        # Also check for tasks without github_issue_number in new format
        for task in existing_tasks:
            if not task.get("github_issue_number"):
                internal_tasks.append(task)

        if not internal_tasks:
            print("No internal tasks found to create GitHub issues")
            return 0

        print(f"Found {len(internal_tasks)} internal tasks to create as GitHub issues")

        created_count = 0
        for task in internal_tasks:
            issue_number = self.create_github_issue(task)
            if issue_number:
                created_count += 1

        print(f"Successfully created {created_count} GitHub issues from TODO tasks")
        return created_count

    def main(self) -> int:
        """Main bidirectional sync function"""
        # Emit programmatic deprecation warning
        warnings.warn(
            "YuiQueryGitHubSync is deprecated since v1.3.0. "
            "Use GitHub Issues directly (gh issue list/create/view/close).",
            DeprecationWarning,
            stacklevel=2,
        )

        print("=" * 70)
        print("⚠️  DEPRECATION WARNING")
        print("=" * 70)
        print("This bidirectional sync workflow is DEPRECATED as of v1.3.0.")
        print("")
        print("GitHub Issues are now the single source of truth for task management.")
        print("Local TODO_FOR_AI.json files have been archived to ARCHIVED/TODO/.")
        print("")
        print("Please use GitHub Issues directly:")
        print("  - View tasks: gh issue list")
        print("  - Create task: gh issue create")
        print("  - View task: gh issue view <number>")
        print("  - Close task: gh issue close <number>")
        print("")
        print("See TODO.md for migration details and new workflow.")
        print("=" * 70)
        print("")
        print("YuiQuery Healthcare Research GitHub <-> TODO Sync")
        print("=" * 50)

        # Phase 0: Load existing TODO data
        existing_todo_data = self.load_existing_todo()

        # Phase 1: TODO -> GitHub sync (create missing issues)
        created_issues = self.sync_to_github(existing_todo_data)

        # Phase 2: GitHub -> TODO sync (update from all issues)
        todo_data = self.sync_from_github()
        if todo_data is None:
            print("Sync failed during GitHub -> TODO phase")
            return 1

        # Phase 3: Validation
        if not self.validate_sync():
            print("Validation found inconsistencies")
            return 1

        print("\nBidirectional sync completed successfully!")
        print("Summary:")
        print(f"   Created GitHub issues: {created_issues}")
        print(f"   Total tasks: {todo_data['sync_metadata']['total_tasks']}")
        print(f"   GitHub issues: {todo_data['sync_metadata']['total_github_issues']}")
        print(f"   Critical (P0): {todo_data['priority_distribution'].get('P0', 0)}")
        print(f"   High (P1): {todo_data['priority_distribution'].get('P1', 0)}")
        print(f"   Blocked: {todo_data['status_distribution'].get('blocked', 0)}")

        return 0


if __name__ == "__main__":
    sync = YuiQueryGitHubSync()
    exit_code = sync.main()
    sys.exit(exit_code)
