---
type: gemini-context
directory: .gemini/skills/agentdb-state-manager
purpose: Persistent state management using AgentDB (DuckDB) for workflow state tracking and analytics.

Tracks workflow transitions via slash command invocations.

**Primary purpose:** Workflow state tracking and analytics
parent: ../GEMINI.md
sibling_readme: README.md
children:
  - ARCHIVED/GEMINI.md
  - schemas/GEMINI.md
  - scripts/GEMINI.md
  - templates/GEMINI.md
related_skills:
  - workflow-orchestrator
  - workflow-utilities
  - git-workflow-manager
---

# Gemini Code Context: agentdb-state-manager

## Purpose

Persistent state management using AgentDB (DuckDB) for workflow state tracking and analytics.

Tracks workflow phase transitions via slash command invocations. Each slash command (/workflow:v7x1_1-worktree through /workflow:v7x1_4-backmerge) records its completion in AgentDB.

**Primary purpose:** Workflow state tracking and analytics

## Directory Structure

```
.gemini/skills/agentdb-state-manager/
├── scripts/
│   ├── __init__.py
│   ├── init_database.py           # Initialize AgentDB schema
│   ├── record_sync.py             # Record workflow transitions (NEW)
│   ├── query_workflow_state.py    # Query current workflow phase (NEW)
│   ├── query_state.py             # Query current state (legacy)
│   ├── analyze_metrics.py         # Historical analytics
│   └── checkpoint_manager.py      # Context checkpoints
├── templates/
│   └── workflow-states.json       # Canonical state definitions
├── SKILL.md                       # Complete skill documentation
├── GEMINI.md                      # This file
├── README.md                      # Human-readable overview
├── CHANGELOG.md                   # Version history
└── ARCHIVED/                      # Deprecated files
    ├── GEMINI.md
    └── README.md
```

## Usage by Gemini Code

### When to Call This Skill

**Context:** Use when workflow analytics or complex state queries are needed

**User says:**
- "Analyze workflow metrics"
- "What tasks are blocking progress?"
- "Show task dependencies"
- "Store checkpoint at 100K tokens"
- "Query workflow state"

**Gemini Code should:**
1. Recognize this is AgentDB state management work
2. Check if AgentDB initialized (agent_synchronizations table exists)
3. If not initialized, run init_database.py first
4. Use query_workflow_state.py to get current phase
5. Use record_sync.py to record phase transitions

### Key Scripts

**record_sync.py** - Record workflow phase transitions:
```bash
uv run python .gemini/skills/agentdb-state-manager/scripts/record_sync.py \
  --sync-type workflow_transition \
  --pattern phase_1_specify \
  --source "planning/{slug}" \
  --target "worktree"
```

**query_workflow_state.py** - Query current workflow phase:
```bash
uv run python .gemini/skills/agentdb-state-manager/scripts/query_workflow_state.py \
  --format json
```

Returns:
```json
{
  "phase": 2,
  "phase_name": "plan",
  "next_command": "/3_tasks",
  "pattern": "phase_2_plan"
}
```

### Workflow Integration

**Phase 0 (Setup):**
```bash
# Initialize AgentDB on first use
uv run python .gemini/skills/agentdb-state-manager/scripts/init_database.py
```

**All Phases (After Phase Completion):**
```bash
# Record phase transition (called by each slash command)
uv run python .gemini/skills/agentdb-state-manager/scripts/record_sync.py \
  --sync-type workflow_transition \
  --pattern phase_{N}_{name}
```

**Complex Queries:**
```bash
# Query task dependencies
python .gemini/skills/agentdb-state-manager/scripts/query_state.py --dependencies

# Analyze workflow metrics
python .gemini/skills/agentdb-state-manager/scripts/analyze_metrics.py --trends
```

**At 100K Tokens:**
```bash
# Store checkpoint
python .gemini/skills/agentdb-state-manager/scripts/checkpoint_manager.py store
```

### Token Efficiency

**Before (Manual File Parsing - deprecated):**
- Parse specs/*/tasks.md: ~1,500 tokens
- Resolve dependencies: ~800 tokens
- Total: ~2,300 tokens per query

**After (AgentDB Query):**
- Run query script: ~200 tokens
- Parse results: ~100 tokens
- Total: ~300 tokens per query

**Savings: ~2,000 tokens (87% reduction) for complex queries**

## Integration with Other Skills

**workflow-orchestrator:**
- Calls query_workflow_state.py for next-step determination
- Uses checkpoint_manager.py at 100K tokens
- Falls back to specs/*/tasks.md if AgentDB unavailable

**workflow-utilities:**
- Uses worktree_context.py for state isolation
- workflow_progress.py reads from AgentDB

**git-workflow-manager:**
- Records transitions during worktree creation and PR workflow

## Best Practices

1. **Initialize once per session:** Run init_database.py at session start
2. **Record transitions:** Use record_sync.py after each phase completion
3. **Query before acting:** Use query_workflow_state.py to determine next step
4. **Session awareness:** AgentDB lasts 24 hours, re-initialize if expired
5. **specs/*/tasks.md is truth:** AgentDB caches specs data for efficiency






## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
- **[../GEMINI.md](../GEMINI.md)** - Parent directory: skills

**Child Directories:**
- **[ARCHIVED/GEMINI.md](ARCHIVED/GEMINI.md)** - Archived
- **[schemas/GEMINI.md](schemas/GEMINI.md)** - Schemas
- **[scripts/GEMINI.md](scripts/GEMINI.md)** - Scripts
- **[templates/GEMINI.md](templates/GEMINI.md)** - Templates

## Related Skills

- workflow-orchestrator
- workflow-utilities
- git-workflow-manager
