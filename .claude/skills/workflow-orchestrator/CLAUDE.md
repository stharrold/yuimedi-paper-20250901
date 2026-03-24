---
type: claude-context
directory: .claude/skills/workflow-orchestrator
purpose: Workflow Orchestrator is **the main coordinator skill** for the 4-phase v7x1 workflow system. Unlike other skills, it contains no executable scripts - instead, it provides algorithmic guidance for Claude Code to detect workflow context, determine current phase, load appropriate skills dynamically, and manage context usage. This is a **conceptual skill** that directs Gemini's behavior rather than providing callable tools.
parent: ../CLAUDE.md
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
  - scripts/CLAUDE.md
  - templates/CLAUDE.md
related_skills:
  - tech-stack-adapter
  - git-workflow-manager
  - workflow-utilities
  - agentdb-state-manager
---

# Claude Code Context: workflow-orchestrator

## Purpose

Workflow Orchestrator is **the main coordinator skill** for the 7-phase workflow system. Unlike other skills, it contains no executable scripts - instead, it provides algorithmic guidance for Claude Code to detect workflow context, determine current phase, load appropriate skills dynamically, and manage context usage. This is a **conceptual skill** that directs Gemini's behavior rather than providing callable tools.

> **Note**: As of v7x1.0, workflow state tracking has migrated from TODO_*.md files to AgentDB (DuckDB). Use `query_workflow_state.py` from `agentdb-state-manager` to determine current phase instead of parsing TODO files.

## Directory Structure

```
.claude/skills/workflow-orchestrator/
├── scripts/                      # (Only __init__.py - no executable scripts)
│   └── __init__.py               # Package initialization
├── templates/                    # (none - no template files)
├── SKILL.md                      # Complete orchestration logic and algorithms
├── CLAUDE.md                     # This file
├── README.md                     # Human-readable overview
├── CHANGELOG.md                  # Version history
└── ARCHIVED/                     # Deprecated files
    ├── CLAUDE.md
    └── README.md
```

## Key Concepts

### No Executable Scripts

**Why no scripts?**
- Orchestration logic is too dynamic for static scripts
- Needs to adapt to conversation context and user intent
- Requires Gemini's natural language understanding
- Context detection is built into Claude Code's capabilities

**What SKILL.md provides:**
- Algorithms (Python pseudocode) for Gemini to implement mentally
- Decision trees for phase determination
- Skill loading patterns
- Context management guidance

---

### Context Detection Algorithm

**Purpose:** Determine where user is in workflow (main repo vs worktree, which phase)

**Algorithm (updated for AgentDB):**
```python
def detect_context():
    """Determine current workflow phase and required skills."""

    # Detect location
    repo_root = git_rev_parse_show_toplevel()
    current_dir = pwd()
    current_branch = git_branch_show_current()

    is_worktree = (current_dir != repo_root)

    # Query AgentDB for workflow state (preferred method)
    # Use: python .claude/skills/agentdb-state-manager/scripts/query_workflow_state.py
    workflow_state = query_agentdb_workflow_state()

    if workflow_state:
        phase = workflow_state['phase']
        phase_name = workflow_state['phase_name']
        next_command = workflow_state['next_command']
    else:
        # Fallback: detect from specs/*/tasks.md
        specs = glob('specs/*/tasks.md')
        workflow_type = detect_from_branch(current_branch)  # feature|release|hotfix

    return {
        'repo_root': repo_root,
        'current_dir': current_dir,
        'current_branch': current_branch,
        'is_worktree': is_worktree,
        'workflow_type': workflow_type,
        'todo_file': todo_file
    }
```

**Claude Code implements this by:**
```python
import subprocess
from pathlib import Path
import glob

# Get repo root
repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip()

# Get current directory
current_dir = str(Path.cwd())

# Check if worktree
is_worktree = (current_dir != repo_root)

# Find TODO files
if is_worktree:
    todos = glob.glob('../TODO_*.md')
else:
    todos = glob.glob('TODO_*.md')

# Determine workflow type
if todos:
    workflow_type = Path(todos[0]).name.split('_')[1]  # feature|release|hotfix
```

---

### Skill Loading Logic

**Purpose:** Load only skills needed for current phase (token efficiency)

**Decision tree (from SKILL.md):**

```python
context = detect_context()

# Phase 0: Always load tech-stack-adapter first (once per session)
if not SESSION_CONFIG_LOADED:
    load_skill('tech-stack-adapter')
    config = run_detect_stack()
    SESSION_CONFIG = config

# Phase determination
if context['is_worktree']:
    # In feature/release/hotfix worktree (Phase 2-3)

    if not spec_exists():
        # Phase 2.3: Need SpecKit
        load_skill('speckit-author')
        run_create_specifications()
    elif not quality_gates_passed():
        # Phase 3: Need Quality
        load_skill('quality-enforcer')
        load_skill('git-workflow-manager')  # for semantic_version.py
        run_quality_gates()
        calculate_version()
    else:
        # Phase 4: Ready for PR
        load_skill('git-workflow-manager')
        create_pr()

elif 'contrib' in context['current_branch']:
    # In main repo on contrib branch (Phase 1 or 4)

    if not planning_exists():
        # Phase 1: Need BMAD
        load_skill('bmad-planner')
        run_create_planning()
    else:
        # Phase 2: Need worktree
        load_skill('git-workflow-manager')
        create_worktree()

elif context['current_branch'] == 'develop':
    # In main repo on develop (Phase 5)
    load_skill('git-workflow-manager')
    create_release()

else:
    # Unknown context
    display_workflow_help()
```

**Claude Code should:**
1. Always check context before loading skills
2. Only load skills needed for current phase
3. Use progressive skill loading (not all at once)
4. Follow the decision tree above

---

### Context Management

**Purpose:** Prevent Claude Code from exceeding context limits

**Thresholds (from SKILL.md):**
- **80K tokens:** Warning - complete current task before checkpoint
- **100K tokens:** Checkpoint - save state to TODO file, prompt user to run `/init` then `/compact`

**Algorithm:**
```python
def check_context_usage():
    """Monitor context and prompt user at thresholds."""

    current_tokens = get_token_count()

    if current_tokens >= 100000:
        # CRITICAL: Checkpoint required
        save_state_to_todo()
        commit_changes()
        display_message("""
        ✓ State saved to TODO file

        Context usage: 100K tokens (checkpoint threshold)

        Please run:
        1. /init (updates memory files)
        2. /compact (compresses memory buffer)
        3. Continue working (context preserved in TODO file)
        """)
        return 'checkpoint'

    elif current_tokens >= 80000:
        # WARNING: Approaching checkpoint
        display_message("""
        ⚠️  Context usage: 80K tokens (approaching 100K checkpoint)

        Recommendation: Complete current task before checkpoint
        """)
        return 'warning'

    return 'normal'
```

**Claude Code should:**
1. Monitor token usage after each response
2. Warn user at 80K tokens
3. Checkpoint at 100K tokens automatically
4. Save complete state before checkpointing

---

## Usage by Claude Code

### When User Says "Next Step?"

**Context:** User wants to continue workflow

**Claude Code should:**

1. **Load tech-stack-adapter (if not loaded):**
   ```python
   if not SESSION_CONFIG:
       config = detect_stack()
       SESSION_CONFIG = config
   ```

2. **Detect current context:**
   ```python
   context = detect_context()
   # Returns: {repo_root, current_dir, is_worktree, workflow_type, todo_file}
   ```

3. **Load appropriate skills based on context:**
   ```python
   if context['is_worktree']:
       # Phase 2-3: Implementation/Quality
       if no_spec():
           load_and_run('speckit-author', 'create_specifications.py')
       elif no_quality():
           load_and_run('quality-enforcer', 'run_quality_gates.py')
       else:
           load_and_run('git-workflow-manager', 'create_pr')
   elif 'contrib' in context['branch']:
       # Phase 1: Planning
       load_and_run('bmad-planner', 'create_planning.py')
   ```

4. **Execute phase-appropriate action**

5. **Check context usage:**
   ```python
   check_context_usage()
   ```

---

### Progressive Skill Loading

**Goal:** Minimize context usage by loading only what's needed

**Pattern:**
```python
# ❌ Bad: Load everything upfront
load_all_skills()  # Wastes ~50K tokens on unused skills

# ✅ Good: Load as needed
if user_needs_planning():
    load_skill('bmad-planner')  # ~5K tokens
elif user_needs_specs():
    load_skill('speckit-author')  # ~5K tokens
# etc.
```

**Token savings:**
- Loading all 9 skills upfront: ~60K tokens
- Progressive loading (2-3 skills per phase): ~10-15K tokens
- **Savings: ~45-50K tokens (75% reduction)**

---

### Phase Transitions

**Phase 1 → Phase 2:**
```python
# User completed BMAD planning in main repo
# Next step: Create feature worktree

context = detect_context()
if planning_exists() and not context['is_worktree']:
    load_skill('git-workflow-manager')
    create_worktree(slug, base_branch='contrib/stharrold')
    # Guide user to: cd ../german_feature_<slug>
```

**Phase 2 → Phase 3:**
```python
# User completed implementation in worktree
# Next step: Run quality gates

if implementation_complete() and not quality_gates_passed():
    load_skill('quality-enforcer')
    run_quality_gates()
    if passed:
        calculate_semantic_version()
```

**Phase 3 → Phase 4:**
```python
# User passed quality gates
# Next step: Create PR

if quality_gates_passed() and not pr_created():
    load_skill('git-workflow-manager')
    create_pr(title, body, base='contrib/stharrold')
```

---

## Integration with Other Skills

**All skills are coordinated by workflow-orchestrator:**

**tech-stack-adapter:**
- Loaded first (Phase 0)
- Provides SESSION_CONFIG for all other skills

**bmad-planner:**
- Loaded in Phase 1 (main repo, contrib branch, no planning/)
- Creates planning/ documents

**git-workflow-manager:**
- Loaded in Phase 2 (create worktree)
- Loaded in Phase 3 (semantic version)
- Loaded in Phase 4 (create PR, daily rebase)
- Loaded in Phase 5 (release workflow)

**speckit-author:**
- Loaded in Phase 2.3 (worktree, no specs/)
- Creates specs/ documents

**quality-enforcer:**
- Loaded in Phase 3 (worktree, implementation complete)
- Validates quality gates

**workflow-utilities:**
- Loaded as needed by other skills
- Provides shared utilities

**agentdb-state-manager:**
- Loaded for complex queries (optional)
- Provides analytics cache

---

## Workflow Phase Map (v7x1)

```
Phase 0: Session Start
├── Load: tech-stack-adapter
└── Action: Detect project configuration

Phase 1: Worktree (/workflow:v7x1_1-worktree)
├── Load: git-workflow-manager
├── Action: Create feature worktree
└── Action: Record state in AgentDB

Phase 2: Integration (/workflow:v7x1_2-integrate)
├── Load: git-workflow-manager
├── Action: Push feature → Create PR (feature -> contrib)
├── Action: Cleanup worktree
├── Action: Push contrib → Create PR (contrib -> develop)
└── Action: Record state in AgentDB

Phase 3: Release (/workflow:v7x1_3-release)
├── Load: git-workflow-manager
├── Action: Create release branch
├── Action: Create PR (release -> main)
├── Action: Tag release
└── Action: Record state in AgentDB

Phase 4: Backmerge (/workflow:v7x1_4-backmerge)
├── Load: git-workflow-manager
├── Action: Create PR (release -> develop)
├── Action: Rebase contrib on develop
├── Action: Cleanup release branch
└── Action: Record state in AgentDB
```

---

## Decision Criteria

**How orchestrator decides what to do:**

1. **Where am I?**
   - Main repo or worktree?
   - What branch?

2. **What exists?**
   - planning/ directory?
   - specs/ directory?
   - TODO file?
   - Quality gates passed?

3. **What's next?**
   - Follow phase map based on answers above

4. **What skills do I need?**
   - Load only skills for current phase

5. **Am I approaching context limit?**
   - Warn at 80K, checkpoint at 100K

---

## Constants and Rationale

**Context thresholds:**
- **80K tokens:** Warning threshold
  - **Rationale:** Gives user time to complete current task before checkpoint
- **100K tokens:** Checkpoint threshold
  - **Rationale:** 73% of 136K effective capacity, ensures clean checkpoint

**Progressive skill loading:**
- **Rationale:** Minimize context usage, load only what's needed for current phase

**Phase-based coordination:**
- **Rationale:** Clear structure, predictable behavior, easy to follow

---








## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
- **[../CLAUDE.md](../CLAUDE.md)** - Parent directory: skills

**Child Directories:**
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived
- **[scripts/CLAUDE.md](scripts/CLAUDE.md)** - Scripts
- **[templates/CLAUDE.md](templates/CLAUDE.md)** - Templates

## Related Skills

- **tech-stack-adapter** - Always loaded first
- **git-workflow-manager** - Loaded in Phases 1, 2, 3, 4
- **workflow-utilities** - Loaded as needed
- **agentdb-state-manager** - Tracks workflow state
