#!/usr/bin/env python3
"""Create feature/release/hotfix worktree with TODO file.

Constants:
- TIMESTAMP_FORMAT: YYYYMMDDTHHMMSSZ (compact ISO8601)
  Rationale: Compact format that remains intact when branch names are parsed
  by underscores and hyphens. No colons/hyphens avoid shell escaping issues.
"""

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add VCS module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'workflow-utilities' / 'scripts'))
from vcs import get_vcs_adapter

# Constants with documented rationale
TIMESTAMP_FORMAT = '%Y%m%dT%H%M%SZ'  # Compact ISO8601 for filename/branch safety
VALID_WORKFLOW_TYPES = ['feature', 'release', 'hotfix']  # Supported workflow types

def create_worktree(workflow_type, slug, base_branch):
    """
    Create a worktree for feature/release/hotfix development.

    Args:
        workflow_type: 'feature' | 'release' | 'hotfix'
        slug: Short descriptive name (e.g., 'json-validator')
        base_branch: Branch to create from (e.g., 'contrib/username')

    Returns:
        dict with worktree_path, branch_name, todo_file

    Raises:
        ValueError: If inputs are invalid
        subprocess.CalledProcessError: If git/gh commands fail
        FileNotFoundError: If required tools are missing
    """
    # Input validation
    if workflow_type not in VALID_WORKFLOW_TYPES:
        raise ValueError(
            f"Invalid workflow_type '{workflow_type}'. "
            f"Must be one of: {', '.join(VALID_WORKFLOW_TYPES)}"
        )

    if not slug or not slug.replace('-', '').replace('_', '').isalnum():
        raise ValueError(
            f"Invalid slug '{slug}'. Must contain only letters, numbers, hyphens, and underscores."
        )

    # Use timezone-aware datetime (datetime.utcnow() is deprecated in Python 3.12+)
    timestamp = datetime.now(timezone.utc).strftime(TIMESTAMP_FORMAT)
    branch_name = f"{workflow_type}/{timestamp}_{slug}"

    # Get repository root
    try:
        repo_root = Path(subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'],
            text=True,
            stderr=subprocess.PIPE
        ).strip())
    except subprocess.CalledProcessError as e:
        print("ERROR: Not in a git repository", file=sys.stderr)
        print(f"Git error: {e.stderr.strip()}", file=sys.stderr)
        raise

    # Verify base branch exists
    try:
        subprocess.run(
            ['git', 'rev-parse', '--verify', base_branch],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError:
        print(f"ERROR: Base branch '{base_branch}' does not exist", file=sys.stderr)
        print("Available branches:", file=sys.stderr)
        subprocess.run(['git', 'branch', '-a'], stderr=subprocess.DEVNULL)
        raise

    worktree_path = repo_root.parent / f"{repo_root.name}_{workflow_type}_{timestamp}_{slug}"

    # Check if worktree path already exists
    if worktree_path.exists():
        raise FileExistsError(
            f"Worktree path already exists: {worktree_path}\n"
            f"Remove it first with: git worktree remove {worktree_path}"
        )

    # Create worktree
    try:
        subprocess.run([
            'git', 'worktree', 'add',
            str(worktree_path),
            '-b', branch_name,
            base_branch
        ], check=True, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        print("ERROR: Failed to create worktree", file=sys.stderr)
        print(f"Command: git worktree add {worktree_path} -b {branch_name} {base_branch}", file=sys.stderr)
        print(f"Git error: {e.stderr.strip()}", file=sys.stderr)
        raise

    # Get VCS username (GitHub/Azure DevOps)
    try:
        vcs = get_vcs_adapter()
        gh_user = vcs.get_current_user()
    except RuntimeError as e:
        print("ERROR: Failed to get VCS username", file=sys.stderr)
        print(f"Error: {e}", file=sys.stderr)
        raise

    todo_filename = f"TODO_{workflow_type}_{timestamp}_{slug}.md"
    todo_path = repo_root / todo_filename

    # Check if TODO file already exists
    if todo_path.exists():
        print(
            f"WARNING: TODO file already exists: {todo_filename}\n"
            f"This worktree may have been created before.",
            file=sys.stderr
        )

    # Copy template and customize
    template_path = repo_root / '.claude' / 'skills' / 'workflow-orchestrator' / 'templates' / 'TODO_template.md'

    # Use timezone-aware datetime for creation timestamp
    created_timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    try:
        if template_path.exists():
            try:
                with open(template_path) as f:
                    content = f.read()
            except (IOError, PermissionError) as e:
                print(f"ERROR: Cannot read template file: {template_path}", file=sys.stderr)
                print(f"Error: {e}", file=sys.stderr)
                raise

            # Replace placeholders
            content = content.replace('{{WORKFLOW_TYPE}}', workflow_type)
            content = content.replace('{{SLUG}}', slug)
            content = content.replace('{{TIMESTAMP}}', timestamp)
            content = content.replace('{{GH_USER}}', gh_user)
            content = content.replace('{{TITLE}}', slug.replace('-', ' ').title())
            content = content.replace('{{DESCRIPTION}}', f"{workflow_type.title()} for {slug}")
            content = content.replace('{{CREATED}}', created_timestamp)

            try:
                with open(todo_path, 'w') as f:
                    f.write(content)
            except (IOError, PermissionError) as e:
                print(f"ERROR: Cannot write TODO file: {todo_path}", file=sys.stderr)
                print(f"Error: {e}", file=sys.stderr)
                raise
        else:
            # Create minimal TODO if template doesn't exist
            print(f"WARNING: Template not found at {template_path}, using minimal TODO", file=sys.stderr)
            try:
                with open(todo_path, 'w') as f:
                    f.write(f"""---
type: workflow-manifest
workflow_type: {workflow_type}
slug: {slug}
timestamp: {timestamp}
github_user: {gh_user}
---

# TODO: {slug}

Workflow: {workflow_type}
Created: {created_timestamp}
""")
            except (IOError, PermissionError) as e:
                print(f"ERROR: Cannot write TODO file: {todo_path}", file=sys.stderr)
                print(f"Error: {e}", file=sys.stderr)
                raise
    except Exception:
        # Cleanup worktree if TODO creation failed
        print("ERROR: TODO file creation failed, cleaning up worktree...", file=sys.stderr)
        try:
            subprocess.run(['git', 'worktree', 'remove', str(worktree_path)],
                         stderr=subprocess.DEVNULL, check=False)
            subprocess.run(['git', 'branch', '-D', branch_name],
                         stderr=subprocess.DEVNULL, check=False)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Ignore errors during cleanup: worktree/branch may not exist or removal may fail,
            # but the original error is more important and will be re-raised.
            pass
        raise

    print(f"✓ Worktree created: {worktree_path}")
    print(f"✓ Branch: {branch_name}")
    print(f"✓ TODO file: {todo_filename}")

    return {
        'worktree_path': str(worktree_path),
        'branch_name': branch_name,
        'todo_file': todo_filename
    }

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: create_worktree.py <feature|release|hotfix> <slug> <base_branch>", file=sys.stderr)
        print(f"\nValid workflow types: {', '.join(VALID_WORKFLOW_TYPES)}", file=sys.stderr)
        print("\nExample: create_worktree.py feature my-feature contrib/username", file=sys.stderr)
        sys.exit(1)

    try:
        result = create_worktree(sys.argv[1], sys.argv[2], sys.argv[3])

        import json
        print(json.dumps(result))
    except (ValueError, FileExistsError) as e:
        print(f"\n{e}", file=sys.stderr)
        sys.exit(1)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Error already printed in function
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        sys.exit(1)
