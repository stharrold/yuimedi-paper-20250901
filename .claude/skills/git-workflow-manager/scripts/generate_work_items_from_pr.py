#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 stharrold
# SPDX-License-Identifier: Apache-2.0
"""Generate work-items from unresolved PR conversations.

This script fetches unresolved PR review conversations and automatically creates
GitHub issues for each conversation.

The workflow pattern is:
1. Claude fetches unresolved PR conversations
2. Claude creates one GitHub issue per conversation
3. User approves PR in web portal (conversations remain as issues)
4. Claude creates feature worktrees to fix each issue
5. Repeat until no unresolved conversations

Constants:
- GITHUB_GRAPHQL_TEMPLATE: GraphQL query for fetching GitHub review threads
  Rationale: GitHub requires GraphQL for isResolved status (not available in REST API)
- WORK_ITEM_SLUG_PATTERN: pr-<pr-number>-issue-<sequence>
  Rationale: Sequential numbering, PR-scoped, sortable, compatible with worktree naming
"""

import sys
from pathlib import Path

# Add VCS module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"))
from vcs import create_issue, detect_provider, query_pr_review_threads

WORK_ITEM_SLUG_PATTERN = "pr-{pr_number}-issue-{sequence}"  # e.g., pr-94-issue-1


class PRFeedbackWorkItemGenerator:
    """Generate work-items from unresolved PR conversations."""

    def __init__(self):
        """Initialize generator.  Provider is auto-detected from git remote."""
        provider = detect_provider()
        self.provider_name = provider.value.replace("_", " ").title()

    def fetch_unresolved_conversations(self, pr_number: int) -> list[dict]:
        """Fetch unresolved PR conversations via vcs.query_pr_review_threads."""
        return query_pr_review_threads(pr_number)

    def create_work_item_from_conversation(
        self, pr_number: int, conversation: dict, sequence: int
    ) -> tuple[str, str]:
        """Create work-item from conversation.

        Args:
            pr_number: Pull request number
            conversation: Conversation dictionary from fetch_unresolved_conversations
            sequence: Work-item sequence number (1, 2, 3, ...)

        Returns:
            Tuple of (work_item_url, work_item_slug)

        Raises:
            RuntimeError: If work-item creation fails
        """
        slug = WORK_ITEM_SLUG_PATTERN.format(pr_number=pr_number, sequence=sequence)

        # Generate title (first 50 chars of comment body)
        comment_preview = conversation["body"][:50]
        if len(conversation["body"]) > 50:
            comment_preview += "..."
        title = f"PR #{pr_number} feedback: {comment_preview}"

        # Generate body with conversation context
        body_parts = [
            f"**From PR:** #{pr_number}",
            f"**Conversation:** {conversation['url']}",
        ]

        if conversation.get("file"):
            location = conversation["file"]
            if conversation.get("line"):
                location += f":{conversation['line']}"
            body_parts.append(f"**Location:** {location}")

        body_parts.append(f"**Author:** {conversation['author']}")
        body_parts.append("")  # Blank line
        body_parts.append(conversation["body"])
        body_parts.append("")  # Blank line
        body_parts.append("---")
        body_parts.append(f"Related to PR #{pr_number}")

        body = "\n".join(body_parts)

        # Create issue (try with labels first, fall back to no labels if they don't exist)
        pr_label = f"pr-{pr_number}"
        try:
            issue_url = create_issue(
                title=title,
                body=body,
                labels=["pr-feedback", pr_label],
                assignee_self=True,
            )
            return (issue_url, slug)
        except RuntimeError as e:
            error_msg = str(e)
            if "not found" in error_msg.lower() and "label" in error_msg.lower():
                print("    [WARN]  Labels not found, creating issue without labels...")
                issue_url = create_issue(title=title, body=body, assignee_self=True)
                return (issue_url, slug)
            raise

    def display_conversations(self, conversations: list[dict]) -> None:
        """Display unresolved conversations grouped by file.

        Args:
            conversations: List of conversation dictionaries
        """
        if not conversations:
            print("\n[OK] No unresolved conversations found!")
            return

        print("\n" + "=" * 80)
        print(f"UNRESOLVED PR CONVERSATIONS ({len(conversations)} total)")
        print("=" * 80)

        # Group by file
        file_groups = {}
        general_conversations = []

        for conv in conversations:
            if conv.get("file"):
                file_path = conv["file"]
                if file_path not in file_groups:
                    file_groups[file_path] = []
                file_groups[file_path].append(conv)
            else:
                general_conversations.append(conv)

        # Display general conversations
        if general_conversations:
            print("\n[PIN] GENERAL COMMENTS")
            print("-" * 80)
            for i, conv in enumerate(general_conversations, 1):
                print(f"\n[{i}] {conv['author']} wrote:")
                print(f"    {conv['body'][:100]}{'...' if len(conv['body']) > 100 else ''}")
                print(f"    [LINK] {conv['url']}")

        # Display file-specific conversations
        if file_groups:
            print("\n[FILE] FILE-SPECIFIC COMMENTS")
            print("-" * 80)
            for file_path, file_convs in sorted(file_groups.items()):
                print(f"\n  {file_path}")
                for conv in file_convs:
                    line_info = f" (line {conv['line']})" if conv.get("line") else ""
                    print(f"    * {conv['author']}{line_info}:")
                    print(f"      {conv['body'][:100]}{'...' if len(conv['body']) > 100 else ''}")
                    print(f"      [LINK] {conv['url']}")

        print("\n" + "=" * 80 + "\n")


def generate_work_items_from_pr(pr_number: int, dry_run: bool = False) -> int:
    """Generate work-items from unresolved PR conversations.

    Args:
        pr_number: Pull request number
        dry_run: If True, only display conversations without creating work-items

    Returns:
        0 on success, 1 on failure

    Raises:
        ValueError: If pr_number is invalid
    """
    # Input validation
    if not isinstance(pr_number, int) or pr_number <= 0:
        raise ValueError(f"Invalid PR number: {pr_number}. Must be a positive integer.")

    # Detect VCS provider
    try:
        generator = PRFeedbackWorkItemGenerator()
    except Exception as e:
        print(f"ERROR: Failed to detect VCS provider: {e}", file=sys.stderr)
        print("Make sure you're in a git repository with a configured remote.")
        return 1

    print(f"\n[FIX] Using {generator.provider_name}\n")

    # Fetch unresolved conversations
    print(f"[FIND] Fetching unresolved conversations from PR #{pr_number}...")
    try:
        conversations = generator.fetch_unresolved_conversations(pr_number)
    except RuntimeError as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        return 1

    # Display conversations
    generator.display_conversations(conversations)

    if not conversations:
        return 0  # Success - no work-items to create

    if dry_run:
        print("[INFO]  Dry run mode - no work-items created")
        print(f"Would create {len(conversations)} work-items with slugs:")
        for i in range(len(conversations)):
            slug = WORK_ITEM_SLUG_PATTERN.format(pr_number=pr_number, sequence=i + 1)
            print(f"  - {slug}")
        return 0

    # Create work-items
    print("[BUILD] Creating work-items...")
    created_work_items = []

    for i, conversation in enumerate(conversations, 1):
        try:
            work_item_url, work_item_slug = generator.create_work_item_from_conversation(
                pr_number, conversation, i
            )
            created_work_items.append((work_item_url, work_item_slug))
            print(f"  [OK] Created {work_item_slug}: {work_item_url}")

        except RuntimeError as e:
            print(f"\n  [FAIL] Failed to create work-item {i}: {e}", file=sys.stderr)
            print(f"    Stopping after {len(created_work_items)} successful work-items.")
            break

    # Summary
    print("\n" + "=" * 80)
    print("[OK] WORK-ITEM GENERATION COMPLETE")
    print("=" * 80)
    print(
        f"\nCreated {len(created_work_items)} work-items from {len(conversations)} conversations:"
    )
    for url, slug in created_work_items:
        print(f"  * {slug}")
        print(f"    {url}")

    print("\n[LIST] Next steps:")
    print(f"  1. Review and approve PR #{pr_number} in web portal")
    print("  2. For each work-item, create feature worktree:")
    for _, slug in created_work_items:
        print(
            f"     python .claude/skills/git-workflow-manager/scripts/create_worktree.py feature {slug} contrib/<user>"
        )
    print("  3. Implement fixes and create PRs for each work-item")
    print("  4. Repeat until no unresolved conversations\n")

    return 0


def main():
    """Main entry point for script."""
    if len(sys.argv) < 2:
        print(
            "Usage: python generate_work_items_from_pr.py <pr-number> [--dry-run]", file=sys.stderr
        )
        print("\nExamples:")
        print("  python generate_work_items_from_pr.py 94")
        print("  python generate_work_items_from_pr.py 94 --dry-run")
        sys.exit(1)

    try:
        pr_number = int(sys.argv[1])
    except ValueError:
        print(f"ERROR: Invalid PR number '{sys.argv[1]}'. Must be an integer.", file=sys.stderr)
        sys.exit(1)

    dry_run = "--dry-run" in sys.argv

    try:
        exit_code = generate_work_items_from_pr(pr_number, dry_run)
        sys.exit(exit_code)
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
