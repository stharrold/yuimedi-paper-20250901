---
type: claude-context
directory: .claude/skills/agentdb-state-manager
purpose: Persistent state management using AgentDB (DuckDB) for workflow analytics and checkpoints.

Provides read-only analytics cache synchronized from TODO_*.md files.

**Primary purpose:** Data gathering and analysis for workflow state tracking
parent: null
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
related_skills:
  - workflow-orchestrator
  - workflow-utilities
  - speckit-author
  - quality-enforcer
  - bmad-planner
---

# Claude Code Context: agentdb-state-manager

## Purpose

Persistent state management using AgentDB (DuckDB) for workflow analytics and checkpoints.

Provides read-only analytics cache synchronized from TODO_*.md files.

**Primary purpose:** Data gathering and analysis for workflow state tracking

## Directory Structure

```
.claude/skills/agentdb-state-manager/
├── scripts/
│   ├── __init__.py
│   ├── init_database.py           # Initialize AgentDB schema
│   ├── sync_todo_to_db.py         # Sync TODO files → AgentDB
│   ├── query_state.py             # Query current state
│   ├── analyze_metrics.py         # Historical analytics
│   └── checkpoint_manager.py      # Context checkpoints
├── templates/
│   └── workflow-states.json       # Canonical state definitions
├── SKILL.md                       # Complete skill documentation
├── CLAUDE.md                      # This file
├── README.md                      # Human-readable overview
├── CHANGELOG.md                   # Version history
└── ARCHIVED/                      # Deprecated files
    ├── CLAUDE.md
    └── README.md
```

## Usage by Claude Code

### When to Call This Skill

**Context:** Use when workflow analytics or complex state queries are needed

**User says:**
- "Analyze workflow metrics"
- "What tasks are blocking progress?"
- "Show task dependencies"
- "Store checkpoint at 100K tokens"
- "Query workflow state"

**Claude Code should:**
1. Recognize this is AgentDB state management work
2. Check if AgentDB initialized (session_metadata table exists)
3. If not initialized, run init_database.py first
4. Sync TODO files before querying (ensure cache is current)
5. Use appropriate script for the task

### Workflow Integration

**Phase 0 (Setup):**
```bash
# Initialize AgentDB on first use
python .claude/skills/agentdb-state-manager/scripts/init_database.py
```

**All Phases (After TODO Updates):**
```bash
# Sync TODO files to AgentDB
python .claude/skills/agentdb-state-manager/scripts/sync_todo_to_db.py
```

**Complex Queries:**
```bash
# Query task dependencies
python .claude/skills/agentdb-state-manager/scripts/query_state.py --dependencies

# Analyze workflow metrics
python .claude/skills/agentdb-state-manager/scripts/analyze_metrics.py --trends
```

**At 100K Tokens:**
```bash
# Store checkpoint
python .claude/skills/agentdb-state-manager/scripts/checkpoint_manager.py store --todo TODO_*.md
```

### Token Efficiency

**Before (Manual File Parsing):**
- Read TODO_*.md file: ~1,500 tokens
- Parse YAML frontmatter: ~500 tokens
- Resolve dependencies: ~800 tokens
- Total: ~2,800 tokens per query

**After (AgentDB Query):**
- Run query script: ~200 tokens
- Parse results: ~100 tokens
- Total: ~300 tokens per query

**Savings: ~2,500 tokens (89% reduction) for complex queries**

## Integration with Other Skills

**workflow-orchestrator:**
- Calls query_state.py for next-step determination
- Uses checkpoint_manager.py at 100K tokens
- Falls back to file parsing if AgentDB unavailable

**workflow-utilities:**
- todo_updater.py triggers sync after TODO updates
- Dual write: update file + sync to database

**speckit-author:**
- Uses for as-built metrics analysis
- Historical planning accuracy queries

**quality-enforcer:**
- Stores quality gate results
- Tracks coverage trends over time

## Best Practices

1. **Initialize once per session:** Run init_database.py at session start
2. **Sync after updates:** Always sync TODO files before querying
3. **Use for complex queries only:** Simple state reads should parse TODO files directly
4. **Session awareness:** AgentDB lasts 24 hours, re-initialize if expired
5. **Files are truth:** TODO_*.md remains source of truth, AgentDB is cache

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[templates/workflow-states.json](templates/workflow-states.json)** - State definitions

## Related Skills

- workflow-orchestrator
- workflow-utilities
- speckit-author
- quality-enforcer
- bmad-planner
