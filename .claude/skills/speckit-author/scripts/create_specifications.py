#!/usr/bin/env python3
"""Interactive SpecKit tool - creates spec.md and plan.md in worktree.

This script runs interactively in a feature/release/hotfix worktree and:
1. Detects BMAD planning context from ../planning/<slug>/
2. Conducts interactive Q&A session (with or without BMAD context)
3. Generates spec.md and plan.md from templates
4. Creates compliant specs/<slug>/ directory structure
5. Updates TODO_*.md with tasks parsed from plan.md
6. Commits changes to the feature branch

Usage:
    python .claude/skills/speckit-author/scripts/create_specifications.py \\
        <workflow_type> <slug> <gh_user> [--todo-file <path>]

Example:
    python .claude/skills/speckit-author/scripts/create_specifications.py \\
        feature my-feature stharrold --todo-file ../TODO_feature_20251024_my-feature.md

Constants:
- TIMESTAMP_FORMAT: YYYY-MM-DD (for spec headers)
  Rationale: Human-readable date format for documentation
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

# Constants with documented rationale
TIMESTAMP_FORMAT = '%Y-%m-%d'  # Human-readable date for documentation
VALID_WORKFLOW_TYPES = ['feature', 'release', 'hotfix']  # Supported workflow types
TASK_PATTERN = re.compile(r'^####\s+Task\s+(\w+_\d+):\s+(.+)$', re.MULTILINE)  # Parse tasks from plan.md


def error_exit(message: str, code: int = 1) -> None:
    """Print error message and exit with code."""
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(code)


def run_command(cmd: List[str], capture=True, check=True) -> Optional[str]:
    """Run command and return output or None on error."""
    try:
        if capture:
            result = subprocess.run(
                cmd, check=check, capture_output=True, text=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check)
            return None
    except subprocess.CalledProcessError as e:
        if check:
            error_exit(f"Command failed: {' '.join(cmd)}\n{e.stderr}")
        return None
    except FileNotFoundError:
        error_exit(f"Command not found: {cmd[0]}")


def detect_context() -> Dict[str, any]:
    """Detect current worktree context and BMAD planning availability."""

    # Get repository root
    repo_root = Path(run_command(['git', 'rev-parse', '--show-toplevel']))
    current_dir = Path.cwd()
    current_branch = run_command(['git', 'branch', '--show-current'])

    # Determine if in worktree (different from repo root)
    is_worktree = current_dir != repo_root

    if not is_worktree:
        error_exit(
            "Not in a worktree. This script must be run from a feature/release/hotfix worktree.\n"
            f"Current directory: {current_dir}\n"
            f"Repository root: {repo_root}\n"
            "Create a worktree first using create_worktree.py"
        )

    return {
        'repo_root': repo_root,
        'current_dir': current_dir,
        'current_branch': current_branch,
        'is_worktree': is_worktree,
    }


def find_bmad_planning(slug: str) -> Optional[Dict[str, Path]]:
    """Check for BMAD planning documents in ../planning/<slug>/."""

    planning_dir = Path('..') / 'planning' / slug

    if not planning_dir.exists():
        return None

    bmad_docs = {
        'planning_dir': planning_dir,
        'requirements': planning_dir / 'requirements.md',
        'architecture': planning_dir / 'architecture.md',
        'epics': planning_dir / 'epics.md',
    }

    # Check which documents exist
    available = {
        key: path for key, path in bmad_docs.items()
        if key == 'planning_dir' or path.exists()
    }

    if len(available) <= 1:  # Only planning_dir exists, no actual docs
        return None

    return available


def ask_question(prompt: str, options: Optional[List[str]] = None, default: Optional[str] = None) -> str:
    """Ask user a question and return response."""

    if options:
        print(f"\n{prompt}")
        for i, option in enumerate(options, 1):
            print(f"  {i}) {option}")

        if default:
            print(f"  [default: {default}]")

        while True:
            response = input("> ").strip()

            if not response and default:
                return default

            # Allow numeric selection
            if response.isdigit():
                idx = int(response) - 1
                if 0 <= idx < len(options):
                    return options[idx]

            # Allow direct text match
            if response in options:
                return response

            print("Invalid selection. Please try again.")
    else:
        if default:
            print(f"\n{prompt} [{default}]")
        else:
            print(f"\n{prompt}")

        response = input("> ").strip()
        return response if response else (default or "")


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    """Ask yes/no question."""
    default_str = "Y/n" if default else "y/N"
    response = input(f"\n{prompt} ({default_str}) > ").strip().lower()

    if not response:
        return default

    return response in ['y', 'yes']


def interactive_qa_with_bmad(bmad_docs: Dict[str, Path], slug: str) -> Dict[str, any]:
    """Conduct interactive Q&A when BMAD planning exists."""

    print("\n" + "=" * 70)
    print("SpecKit Interactive Specification Tool")
    print("=" * 70)
    print(f"\n✓ Detected BMAD planning context: ../planning/{slug}/")

    # Display BMAD summary
    print("\nBMAD Summary:")

    if 'requirements' in bmad_docs:
        req_text = bmad_docs['requirements'].read_text()
        fr_count = len(re.findall(r'FR-\d+', req_text))
        us_count = len(re.findall(r'US-\d+', req_text))
        print(f"  - Requirements: {fr_count} functional requirements, {us_count} user stories")

    if 'architecture' in bmad_docs:
        arch_text = bmad_docs['architecture'].read_text()
        # Extract technology stack mentions
        stack_lines = [line for line in arch_text.split('\n') if any(
            tech in line.lower() for tech in ['python', 'fastapi', 'flask', 'django', 'postgresql', 'sqlite']
        )]
        if stack_lines:
            print("  - Architecture: Technology stack defined")

    if 'epics' in bmad_docs:
        epic_text = bmad_docs['epics'].read_text()
        epic_count = len(re.findall(r'E-\d+', epic_text))
        print(f"  - Epics: {epic_count} epics defined")

    print("\nImplementation Questions:")
    print("-" * 70)

    responses = {}

    # Database migrations (if database mentioned in architecture)
    if 'architecture' in bmad_docs:
        arch_text = bmad_docs['architecture'].read_text().lower()
        if 'database' in arch_text or 'postgresql' in arch_text or 'mysql' in arch_text:
            responses['migration_strategy'] = ask_question(
                "Database migrations strategy?",
                options=["Alembic (recommended)", "Manual SQL migrations", "None needed"],
                default="Alembic (recommended)"
            )

    # Testing approach
    responses['include_e2e_tests'] = ask_yes_no(
        "Include end-to-end (E2E) tests?", default=False
    )

    responses['include_performance_tests'] = ask_yes_no(
        "Include performance/load tests?", default=False
    )

    responses['include_security_tests'] = ask_yes_no(
        "Include security tests (OWASP checks)?", default=False
    )

    # Task granularity
    responses['task_granularity'] = ask_question(
        "Task granularity preference?",
        options=["Small tasks (1-2 hours each)", "Medium tasks (half-day each)", "Large tasks (full-day each)"],
        default="Small tasks (1-2 hours each)"
    )

    # Epic implementation order
    if 'epics' in bmad_docs:
        responses['follow_epic_order'] = ask_yes_no(
            "Follow epic priority order from epics.md?", default=True
        )

    # Additional implementation notes
    responses['additional_notes'] = ask_question(
        "Any additional implementation notes or constraints? (optional)"
    )

    return responses


def interactive_qa_without_bmad(slug: str) -> Dict[str, any]:
    """Conduct interactive Q&A when no BMAD planning exists."""

    print("\n" + "=" * 70)
    print("SpecKit Interactive Specification Tool")
    print("=" * 70)
    print(f"\n⚠ No BMAD planning found for '{slug}'")
    print("I'll gather requirements through comprehensive Q&A.")
    print("\nRecommendation: Use BMAD planning for future features")
    print("=" * 70)

    responses = {}

    # Core requirements
    responses['purpose'] = ask_question(
        "What is the main purpose of this feature?"
    )

    responses['users'] = ask_question(
        "Who are the primary users of this feature?"
    )

    responses['success_criteria'] = ask_question(
        "How will success be measured? (metrics, goals)"
    )

    # Technology stack
    print("\nTechnology Stack:")

    responses['web_framework'] = ask_question(
        "Web framework (if applicable)?",
        options=["FastAPI", "Flask", "Django", "None"],
        default="None"
    )

    responses['database'] = ask_question(
        "Database?",
        options=["SQLite (dev)", "PostgreSQL", "MySQL", "None"],
        default="None"
    )

    if responses['database'] != "None":
        responses['migration_strategy'] = ask_question(
            "Database migration strategy?",
            options=["Alembic", "Manual SQL", "None"],
            default="Alembic"
        )

    responses['testing_framework'] = ask_question(
        "Testing framework?",
        options=["pytest (recommended)", "unittest", "other"],
        default="pytest (recommended)"
    )

    # Performance & security
    responses['performance_target'] = ask_question(
        "Performance target? (e.g., '<200ms response time', 'not critical')"
    )

    responses['security_requirements'] = ask_question(
        "Security requirements? (e.g., 'authentication', 'encryption', 'none')"
    )

    # Testing preferences
    responses['target_coverage'] = ask_question(
        "Test coverage target?",
        default="80%"
    )

    responses['include_e2e_tests'] = ask_yes_no(
        "Include E2E tests?", default=False
    )

    responses['include_performance_tests'] = ask_yes_no(
        "Include performance tests?", default=False
    )

    # Task breakdown
    responses['task_granularity'] = ask_question(
        "Task size preference?",
        options=["Small (1-2 hours)", "Medium (half-day)", "Large (full-day)"],
        default="Small (1-2 hours)"
    )

    return responses


def load_template(template_name: str) -> str:
    """Load template file from ../templates/."""

    # Get script directory and navigate to templates
    script_dir = Path(__file__).parent
    template_path = script_dir.parent / 'templates' / template_name

    if not template_path.exists():
        error_exit(f"Template not found: {template_path}")

    return template_path.read_text()


def generate_spec_md(
    slug: str,
    workflow_type: str,
    gh_user: str,
    date: str,
    qa_responses: Dict[str, any],
    bmad_docs: Optional[Dict[str, Path]]
) -> str:
    """Generate spec.md from template."""

    spec_template = load_template('spec.md.template')

    # Replace placeholders
    title = slug.replace('-', ' ').replace('_', ' ').title()
    spec = spec_template.replace('{{TITLE}}', title)
    spec = spec.replace('{{WORKFLOW_TYPE}}', workflow_type)
    spec = spec.replace('{{SLUG}}', slug)
    spec = spec.replace('{{DATE}}', date)
    spec = spec.replace('{{GH_USER}}', gh_user)

    # Add Q&A context as comments in spec
    # (This helps Claude Code understand implementation preferences)
    context_section = "\n## Implementation Context\n\n"
    context_section += "<!-- Generated from SpecKit interactive Q&A -->\n\n"

    if bmad_docs:
        context_section += f"**BMAD Planning:** See `../planning/{slug}/` for complete requirements and architecture.\n\n"

    context_section += "**Implementation Preferences:**\n\n"
    for key, value in qa_responses.items():
        if value and value != "":
            formatted_key = key.replace('_', ' ').title()
            context_section += f"- **{formatted_key}:** {value}\n"

    # Insert context section after ## Overview
    spec = spec.replace(
        '## Requirements Reference',
        context_section + '\n## Requirements Reference'
    )

    return spec


def generate_plan_md(
    slug: str,
    workflow_type: str,
    date: str,
    qa_responses: Dict[str, any],
    bmad_docs: Optional[Dict[str, Path]]
) -> str:
    """Generate plan.md from template with example tasks."""

    plan_template = load_template('plan.md.template')

    # Replace placeholders
    title = slug.replace('-', ' ').replace('_', ' ').title()
    plan = plan_template.replace('{{TITLE}}', title)
    plan = plan.replace('{{WORKFLOW_TYPE}}', workflow_type)
    plan = plan.replace('{{SLUG}}', slug)
    plan = plan.replace('{{DATE}}', date)

    # Add implementation note
    note = "\n<!-- Note: Customize task breakdown based on specific feature requirements -->\n"
    note += "<!-- This template provides the structure. Claude Code will populate with actual tasks. -->\n\n"

    plan = plan.replace('## Task Breakdown', note + '## Task Breakdown')

    return plan


def parse_tasks_from_plan(plan_md: str) -> List[Dict[str, str]]:
    """Parse task IDs and descriptions from plan.md."""

    tasks = []

    # Find all task headers matching pattern: #### Task impl_001: Description
    matches = TASK_PATTERN.findall(plan_md)

    for task_id, description in matches:
        # Determine category from task ID prefix
        category = task_id.split('_')[0]  # impl, test, doc, etc.

        tasks.append({
            'id': task_id,
            'description': description.strip(),
            'category': category,
            'status': 'pending'
        })

    return tasks


def update_todo_file(todo_path: Path, tasks: List[Dict[str, str]]) -> None:
    """Update TODO_*.md frontmatter with tasks from plan.md."""

    try:
        import yaml
    except ImportError:
        error_exit(
            "PyYAML required for TODO updates. Install: pip install pyyaml or uv add pyyaml"
        )

    if not todo_path.exists():
        print(f"⚠ TODO file not found: {todo_path}")
        print("  Skipping TODO update. Please update manually.")
        return

    content = todo_path.read_text()

    # Split frontmatter and body
    if not content.startswith('---'):
        print("⚠ TODO file missing YAML frontmatter")
        print("  Skipping TODO update. Please update manually.")
        return

    parts = content.split('---', 2)
    if len(parts) < 3:
        print("⚠ Invalid TODO file format")
        print("  Skipping TODO update. Please update manually.")
        return

    frontmatter = yaml.safe_load(parts[1])
    body = parts[2]

    # Initialize tasks section if not exists
    if 'tasks' not in frontmatter:
        frontmatter['tasks'] = {}

    # Group tasks by category
    tasks_by_category = {}
    for task in tasks:
        category = task['category']
        if category not in tasks_by_category:
            tasks_by_category[category] = []

        tasks_by_category[category].append({
            'id': task['id'],
            'description': task['description'],
            'status': task['status']
        })

    # Update frontmatter with tasks
    for category, category_tasks in tasks_by_category.items():
        frontmatter['tasks'][category] = category_tasks

    # Update workflow progress
    if 'workflow_progress' not in frontmatter:
        frontmatter['workflow_progress'] = {}

    frontmatter['workflow_progress']['phase'] = 2
    frontmatter['workflow_progress']['current_step'] = "2.4"
    frontmatter['workflow_progress']['last_update'] = datetime.now(timezone.utc).isoformat()

    # Write back
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    new_content = f"---\n{yaml_str}---{body}"
    todo_path.write_text(new_content)

    print(f"✓ Updated TODO file: {todo_path}")
    print(f"  Added {len(tasks)} tasks across {len(tasks_by_category)} categories")


def create_specs_directory(slug: str, workflow_type: str) -> Path:
    """Create specs/<slug>/ directory with required structure."""

    specs_dir = Path('specs') / slug
    specs_dir.mkdir(parents=True, exist_ok=True)

    # Create CLAUDE.md
    claude_md = f"""# Claude Code Context: specs/{slug}

## Purpose

SpecKit specifications for {workflow_type} '{slug}'

## Directory Structure

```
specs/{slug}/
├── spec.md        # Detailed technical specification
├── plan.md        # Implementation task breakdown
├── CLAUDE.md      # This file
├── README.md      # Human-readable overview
└── ARCHIVED/      # Deprecated specs
```

## Files in This Directory

- **spec.md** - Complete technical specification with implementation details
- **plan.md** - Task breakdown (impl_*, test_*, doc_*) with acceptance criteria

## Usage

When implementing this feature:
1. Read spec.md for technical details
2. Follow plan.md task order
3. Update TODO_*.md task status as you complete each task
4. Refer to ../planning/{slug}/ for BMAD context (if available)

## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
- **[../../planning/{slug}/CLAUDE.md](../../planning/{slug}/CLAUDE.md)** - BMAD Planning (if available)
"""

    (specs_dir / 'CLAUDE.md').write_text(claude_md)

    # Create README.md
    readme = f"""# Specifications: {slug.replace('-', ' ').title()}

## Overview

SpecKit specifications for {workflow_type} development.

## Files

- **spec.md** - Detailed technical specification
- **plan.md** - Implementation task breakdown

## Generated By

SpecKit Interactive Tool - `.claude/skills/speckit-author/scripts/create_specifications.py`

## Related

- BMAD Planning: `../../planning/{slug}/` (if available)
- Implementation: `../../src/`
- Tests: `../../tests/`
"""

    (specs_dir / 'README.md').write_text(readme)

    # Create ARCHIVED/ subdirectory
    archived_dir = specs_dir / 'ARCHIVED'
    archived_dir.mkdir(exist_ok=True)

    (archived_dir / 'CLAUDE.md').write_text(
        f"# Claude Code Context: specs/{slug}/ARCHIVED\n\n"
        "Archived specifications and deprecated files.\n"
    )

    (archived_dir / 'README.md').write_text(
        f"# Archived: specs/{slug}\n\n"
        "Deprecated specification files are stored here.\n"
    )

    return specs_dir


def commit_changes(slug: str, specs_dir: Path, todo_file: Optional[Path]) -> None:
    """Commit spec.md, plan.md, and TODO updates."""

    # Git add files
    run_command(['git', 'add', str(specs_dir)])

    if todo_file and todo_file.exists():
        run_command(['git', 'add', str(todo_file)])

    # Create commit message
    commit_msg = f"""docs(spec): add SpecKit specifications for {slug}

Generated by SpecKit Interactive Tool:
- spec.md: Detailed technical specification
- plan.md: Implementation task breakdown
- Updated TODO with tasks from plan.md

Refs: {todo_file.name if todo_file else 'TODO_*.md'}
"""

    run_command(['git', 'commit', '-m', commit_msg])

    print("\n✓ Committed changes to branch")


def main():
    """Main entry point for SpecKit interactive tool."""

    parser = argparse.ArgumentParser(
        description='Interactive SpecKit tool - creates spec.md and plan.md in worktree'
    )
    parser.add_argument('workflow_type', choices=VALID_WORKFLOW_TYPES,
                        help='Workflow type: feature, release, or hotfix')
    parser.add_argument('slug', help='Feature slug (e.g., my-feature)')
    parser.add_argument('gh_user', help='GitHub username')
    parser.add_argument('--todo-file', type=Path,
                        help='Path to TODO file (default: auto-detect ../TODO_*.md)')
    parser.add_argument('--no-commit', action='store_true',
                        help='Skip git commit (for testing)')

    args = parser.parse_args()

    # 1. Detect context
    context = detect_context()
    print(f"Working in worktree: {context['current_dir']}")
    print(f"Branch: {context['current_branch']}")

    # 2. Find TODO file
    todo_file = args.todo_file
    if not todo_file:
        # Auto-detect TODO file
        todo_pattern = Path('..') / f'TODO_{args.workflow_type}_*_{args.slug}.md'
        import glob
        matches = glob.glob(str(todo_pattern))
        if matches:
            todo_file = Path(matches[0])
            print(f"✓ Auto-detected TODO file: {todo_file}")
        else:
            print(f"⚠ No TODO file found matching: {todo_pattern}")
            print("  Continuing without TODO update...")

    # 3. Check for BMAD planning
    bmad_docs = find_bmad_planning(args.slug)

    # 4. Interactive Q&A
    if bmad_docs:
        qa_responses = interactive_qa_with_bmad(bmad_docs, args.slug)
    else:
        qa_responses = interactive_qa_without_bmad(args.slug)

    # 5. Generate specifications
    print("\n" + "=" * 70)
    print("Generating specifications...")
    print("=" * 70)

    date = datetime.now(timezone.utc).strftime(TIMESTAMP_FORMAT)

    spec_md = generate_spec_md(
        args.slug, args.workflow_type, args.gh_user, date,
        qa_responses, bmad_docs
    )

    plan_md = generate_plan_md(
        args.slug, args.workflow_type, date,
        qa_responses, bmad_docs
    )

    # 6. Create specs directory
    specs_dir = create_specs_directory(args.slug, args.workflow_type)

    # Write spec.md and plan.md
    spec_path = specs_dir / 'spec.md'
    plan_path = specs_dir / 'plan.md'

    spec_path.write_text(spec_md)
    plan_path.write_text(plan_md)

    print(f"✓ Created {spec_path} ({len(spec_md)} chars)")
    print(f"✓ Created {plan_path} ({len(plan_md)} chars)")

    # 7. Parse tasks and update TODO
    tasks = parse_tasks_from_plan(plan_md)

    if tasks and todo_file:
        update_todo_file(todo_file, tasks)
    elif not tasks:
        print("⚠ No tasks found in plan.md (template uses placeholders)")
        print("  Claude Code will populate plan.md with actual tasks")

    # 8. Commit changes
    if not args.no_commit:
        commit_changes(args.slug, specs_dir, todo_file)
    else:
        print("\n⚠ Skipping commit (--no-commit flag)")

    # Trigger sync engine (Phase 3 integration)
    try:
        import asyncio
        integration_path = Path(__file__).parent.parent.parent / "agentdb-state-manager" / "scripts"
        if str(integration_path) not in sys.path:
            sys.path.insert(0, str(integration_path))
        from worktree_agent_integration import trigger_sync_completion

        asyncio.run(trigger_sync_completion(
            agent_id="research",
            action="documentation_complete",
            state_snapshot={
                "slug": args.slug,
                "workflow_type": args.workflow_type,
                "spec_file": str(specs_dir / "spec.md"),
                "plan_file": str(specs_dir / "plan.md"),
                "tasks_generated": len(tasks) if tasks else 0,
                "bmad_context_available": bmad_docs is not None
            },
            context={"user": args.gh_user}
        ))
    except Exception:
        # Graceful degradation: don't fail if sync unavailable
        pass

    # 9. Summary
    print("\n" + "=" * 70)
    print("SpecKit Specifications Created Successfully!")
    print("=" * 70)
    print("\nFiles created:")
    print(f"  - {spec_path}")
    print(f"  - {plan_path}")
    print(f"  - {specs_dir}/CLAUDE.md")
    print(f"  - {specs_dir}/README.md")

    if tasks and todo_file:
        print("\nTODO updated:")
        print(f"  - {todo_file}")
        print(f"  - {len(tasks)} tasks added")

    print("\nNext steps:")
    print("  1. Review spec.md and plan.md")
    print("  2. Implement tasks from plan.md")
    print("  3. Update TODO task status as you complete each task")

    if bmad_docs:
        print(f"  4. Refer to ../planning/{args.slug}/ for BMAD context")

    print("")


if __name__ == '__main__':
    main()
