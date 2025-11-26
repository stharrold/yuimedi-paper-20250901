# YuiQuery Healthcare Research: Workflow v5.3 Architecture Analysis

## Executive Summary

This is a **skill-based progressive disclosure workflow** for documentation and research development. The system uses 9 specialized skills to manage a git-flow + GitHub-flow hybrid with worktree isolation. Key innovation: callable tools (BMAD, SpecKit) reduce token usage by 75-92% compared to manual reproduction.

**Current version:** 5.3.0 | **Repository:** YuiQuery Healthcare Analytics Research

---

## 1. HIGH-LEVEL ARCHITECTURE

### Execution Flow: User Request → Workflow Completion

```
User: "next step?"
  ↓
workflow-orchestrator (loaded always)
  ↓
  1. Detect context (main repo vs worktree, current branch, TODO file)
  2. Load tech-stack-adapter (once per session) → detect Python/uv/Podman
  3. Determine phase from context + TODO file YAML frontmatter
  4. Load phase-appropriate skills (1-3 per phase)
  5. Prompt user for explicit "Y" confirmation
  6. Wait for confirmation before proceeding
  ↓
Skill execution (phase-specific)
  ↓
  Example Phase 1: bmad-planner
    - Run create_planning.py (callable tool)
    - Interactive Q&A with three personas (Analyst, Architect, PM)
    - Generate planning/<slug>/ with requirements.md, architecture.md, epics.md
    - Commit changes to contrib branch
  ↓
Update TODO file via workflow-utilities
  ↓
Check context usage
  - At 80K tokens: warn user
  - At 100K tokens: save state to TODO, prompt /init + /compact
  ↓
Next iteration (user says "next step?" again)
```

### Phase Map

```
Phase 0: Session start           (tech-stack-adapter)
Phase 1: Planning (main repo)    (bmad-planner) → plan/
Phase 2: Implementation (worktree) (speckit-author, git-workflow-manager) → specs/
Phase 3: Quality (worktree)      (quality-enforcer)
Phase 4: Integration (main repo) (git-workflow-manager, speckit-author optional)
Phase 5: Release (main repo)     (git-workflow-manager, quality-enforcer)
Phase 6: Hotfix (hotfix worktree) (git-workflow-manager, quality-enforcer, speckit-author optional)
```

---

## 2. KEY ARCHITECTURAL PATTERNS

### A. Progressive Skill Loading (Token Efficiency)

**Problem:** All 9 skills at once = 60K tokens wasted

**Solution:** Load only skills needed for current phase

```
Initial: orchestrator + tech-stack (~10K tokens)
Phase 1: + bmad-planner (~5K tokens)
Phase 2: + speckit-author + git-workflow-manager (~8K tokens)
Phase 3: + quality-enforcer (~5K tokens)
Total per feature: ~30-35K tokens

vs old monolith: 60K tokens
Savings: ~50% reduction
```

**Implementation:** workflow-orchestrator SKILL.md contains decision tree (algorithms, not executable)

---

### B. BMAD → SpecKit Context Reuse

**Problem:** Planning and specs are separate, questions repeat

**Solution:** Callable tools with persistent context

**Phase 1 (BMAD):**
- Runs: `python create_planning.py my-feature stharrold`
- Creates: `planning/my-feature/requirements.md`, `architecture.md`, `epics.md`
- Stores in main repo (persists across sessions)

**Phase 2 (SpecKit):**
- Runs: `python create_specifications.py feature my-feature stharrold`
- Auto-detects: `../planning/my-feature/` from feature worktree
- Reads: requirements, architecture, epics from Phase 1
- Adaptive Q&A:
  - Without BMAD: 10-15 questions
  - With BMAD: 5-8 questions (context already gathered)

**Token savings:** ~1,700-2,700 tokens per feature (context reuse)

---

### C. VCS Abstraction Layer

**Problem:** GitHub and Azure DevOps have different APIs

**Solution:** Unified adapter pattern in workflow-utilities

```
workflow-utilities/scripts/vcs/
├── provider.py          # Auto-detect from git remote
├── base_adapter.py      # Interface definition
├── github_adapter.py    # gh CLI wrapper
└── azure_adapter.py     # az CLI wrapper
```

**Usage pattern:**
```python
from vcs import get_vcs_adapter

adapter = get_vcs_adapter()  # Auto-detects GitHub vs Azure DevOps
pr_url = adapter.create_pr(title, body, source_branch, target_branch)
```

**Benefits:**
- Works with GitHub or Azure DevOps without code changes
- Uses CLI tools (gh/az) instead of direct API
- Extensible for other VCS providers

---

### D. AgentDB Dual-Write Architecture

**Problem:** Complex queries on workflow state require parsing TODO files (expensive)

**Solution:** DuckDB analytics cache (read-only, synced from TODO files)

**Pattern:**
```
TODO_*.md (source of truth - human-editable, git-tracked)
    ↓ (sync)
AgentDB (read-only cache - 24-hour session)
    ↓ (queries)
Workflow analytics (89% token reduction for complex queries)
```

**When to use:**
- Complex queries (dependencies, task chains, blocked tasks): Use AgentDB
- Simple reads (single TODO file): Parse file directly
- Cross-workflow queries: AgentDB shines

**Token savings:** ~2,500 tokens reduction (89%) for complex queries

---

## 3. CRITICAL DESIGN DECISIONS

### A. Why TODO Files in Main Repo, Not Worktrees?

**Problem:** Worktrees are isolated from main repo, but workflow state must persist across sessions

**Solution:** TODO_*.md files stored in main repo, worktrees reference via `../TODO_*.md`

**Benefits:**
- Persistent across worktree deletion
- Single source of truth for workflow state
- Can archive after worktree cleanup
- Git-tracked with commit history
- Accessible from main repo for manifest updates

**Example structure:**
```
main-repo/
  TODO_feature_20251108T143000Z_auth-system.md
  planning/auth-system/
  specs/auth-system/
  ARCHIVED/TODO_feature_*.md (after completion)

worktree-feature/
  (references ../TODO_feature_20251108T143000Z_auth-system.md)
```

---

### B. Why Worktrees Instead of Branch Switching?

**Problem:** Branch switching loses uncommitted work, testing multiple features requires stashing

**Solution:** Git worktrees = isolated working directories

```
git worktree add ../standard_feature_<slug> feature/<timestamp>_<slug>
```

**Benefits:**
- No stash/pop needed
- Multiple branches active simultaneously
- Each feature gets isolated environment
- Clean separation (main repo untouched during feature work)
- Faster context switching (no need to rebuild dependencies)

**Cost:** Extra directory overhead (minimal)

---

### C. How Skill Versioning System Works

**Pattern:** MAJOR.MINOR.PATCH in YAML frontmatter of SKILL.md

```
.claude/skills/bmad-planner/SKILL.md
---
name: bmad-planner
version: 5.1.0          # ← Updated here
description: |
  ...
---
```

**Cross-file validation:**
- `validate_versions.py` checks all SKILL.md files
- Validates WORKFLOW.md references correct versions
- Validates TODO.md version consistency
- Fails if inconsistencies found

**Update process:**
- Modify SKILL.md, CLAUDE.md, CHANGELOG.md
- Run `validate_versions.py` to check consistency
- Run `sync_skill_docs.py` to update WORKFLOW.md sections
- Commit with standardized message

---

## 4. COMMON PITFALLS (Not Obvious from Individual Files)

### A. Branch Protection Violations

**Protected branches:** `main` and `develop` (NEVER delete, NEVER commit or push directly from local; only merge via PR in GitHub/Azure DevOps web UI)

**Key distinction:** Protection prevents direct *local* commits/pushes. PR merges via web UI are the approved method and do not violate protection.

**Common mistakes:**
```
❌ git commit -m "..." && git push origin develop
   → Violates protection policy (direct local commit/push to protected branch)

✅ Create PR: feature → contrib → develop (merge via PR in web UI)
   → Follows protection policy (merge via PR in web UI is the approved method)

❌ git branch -D main
   → Irreversible disaster

✅ All operations use PRs (even back-merge from release)
```

**Enforcement:** All scripts validate branch before committing

---

### B. Context Management at 100K Tokens

**Thresholds:**
- 80K tokens: Warning (complete current task)
- 100K tokens: Checkpoint (save + reset)

**Required actions at 100K:**
```
1. System auto-saves to TODO_*.md
2. System commits checkpoint
3. User must run: /init (updates memory files)
4. User must run: /compact (compresses buffer)
5. Context preserved in TODO_*.md for resume
```

**Common mistakes:**
```
❌ Ignore checkpoint warning, continue past 100K
   → Hard limit hit, session ends mid-task

✅ Complete current task, then checkpoint at 100K
   → Clean state save, resume preserved
```

---

### C. TODO File Lifecycle (Register → Update → Archive)

**Phase 1/2: Registration**
```bash
# After creating TODO_feature_*.md
python workflow_registrar.py TODO_feature_*.md feature <slug>
# Adds to TODO.md workflows.active[] array
```

**During workflow: Updates**
```bash
# After each task completion
python todo_updater.py TODO_feature_*.md <task_id> complete
# Updates task status, last_update timestamp
```

**Phase 4.4: Archival**
```bash
# After PR merged to contrib branch
python workflow_archiver.py TODO_feature_*.md --summary "..." --version "1.6.0"
# Moves: TODO_*.md → ARCHIVED/TODO_*.md
# Updates: TODO.md (active[] → archived[])
```

**Common mistakes:**
```
❌ Delete TODO file after workflow
   → Lost history, can't recover, breaks TODO.md

✅ Use workflow_archiver.py
   → Preserves history, updates manifest consistently
```

---

### D. When to Use Which Skill

**Phase 1 (Main repo, contrib branch):**
- BMAD exists? → Skip, move to Phase 2
- BMAD doesn't exist? → Run bmad-planner (create_planning.py)

**Phase 2 (Worktree):**
- Specs don't exist? → Run speckit-author (create_specifications.py)
- Specs exist? → Implement code

**Phase 3 (Worktree):**
- Implementation complete? → Run quality-enforcer (run_quality_gates.py)
- Tests passing + coverage ≥80%? → Calculate semantic_version.py, create PR

**Phase 4 (Main repo, contrib branch):**
- PR to develop needs creation? → Run git-workflow-manager (create PR)
- PR feedback conversations? → Run generate_work_items_from_pr.py (optional)
- As-built feedback needed? → Run speckit-author (update_asbuilt.py, optional)

---

## 5. CRITICAL ARCHITECTURAL INSIGHTS

### A. Worktree + Timestamp Pattern

```
feature/20251108T143000Z_auth-system
                    ↑↑↑↑↑↑↑↑↑
                    Compact ISO8601
                    No colons/hyphens (shell escaping safe)
                    Sortable by date
```

**Why NOT use traditional branch names?**
```
❌ feature/auth-system → Ambiguous, collision risk (multiple auth features)
❌ feature/auth-system-2 → Manual tracking, error-prone
✅ feature/20251108T143000Z_auth-system → Unique, sortable, timestamped
```

---

### B. Skill Loading Decision Tree (From Orchestrator)

**Note:** This is algorithmic pseudo-code showing the orchestrator's decision logic, not executable Python. The orchestrator SKILL.md contains algorithms for skill selection, not executable code.

```
# Algorithmic pseudo-code (not executable Python)

if not SESSION_CONFIG:
    load('tech-stack-adapter')      # Detect uv/Podman/Python version

context = detect_context()

if context['is_worktree']:
    # In feature/release/hotfix worktree
    if not specs_exist():
        load('speckit-author')       # Phase 2.3
    elif not quality_gates_pass():
        load('quality-enforcer')     # Phase 3
    else:
        load('git-workflow-manager') # Phase 4
        create_pr()

elif 'contrib' in context['branch']:
    # In main repo on contrib branch
    if not planning_exists():
        load('bmad-planner')         # Phase 1
    else:
        load('git-workflow-manager') # Phase 2 or 4
        create_worktree() or create_pr()

elif context['branch'] == 'develop':
    # In main repo on develop
    load('git-workflow-manager')     # Phase 5
    create_release()
```

---

### C. The Callable Tool Revolution (Phase 1-2)

**Before v5.2:**
- Claude reproduces planning Q&A each time (~2,500 tokens)
- Claude reproduces spec generation each time (~2,000 tokens)
- **Total per feature: ~4,500 tokens lost to reproduction**

**After v5.2 (Callable Tools):**
- `create_planning.py` handles BMAD Q&A + generation (~200 tokens to invoke)
- `create_specifications.py` handles spec generation (~200 tokens to invoke)
- Auto-detects BMAD context in Phase 2
- **Token savings: 92% reduction per feature**

**Implementation key:** Scripts run interactively in main context, Claude doesn't reproduce logic

---

### D. Why TODO.md YAML Frontmatter Structure?

```yaml
---
type: workflow-master-manifest
version: 5.0.0

workflows:
  active:
    - slug: auth-system
      timestamp: 20251108T143000Z
      title: "User Authentication"
      status: in_progress
      file: "TODO_feature_20251108T143000Z_auth.md"

  archived:
    - slug: workflow
      timestamp: 20251023T123254Z
      status: completed
      completed_at: "2025-10-23T19:30:00Z"
      semantic_version: "1.2.0"
      file: "ARCHIVED/TODO_feature_20251023T123254Z_workflow.md"
      summary: "What was accomplished"

context_stats:
  total_workflows_completed: 1
  current_token_usage: 55000
  last_checkpoint: "2025-11-03T17:07:21Z"
---
```

**Why?**
- Machine-readable (enables AgentDB queries)
- Single source of truth (all workflows in one file)
- Git-trackable (no database files)
- Human-readable (YAML is clear)
- Extensible (add new fields without breaking parsing)

---

## 6. INTEGRATION PATTERNS

### A. Shared Utilities Dependency Web

```
workflow-utilities (bottom layer)
  ├── deprecate_files.py (archive old files)
  ├── directory_structure.py (create standard dirs)
  ├── todo_updater.py (update task status)
  ├── workflow_registrar.py (register in TODO.md)
  ├── workflow_archiver.py (archive completed workflow)
  ├── sync_manifest.py (sync filesystem to TODO.md)
  ├── vcs/ (GitHub/Azure abstraction)
  └── validate_versions.py (cross-file consistency)
       ↑ Used by all other skills

workflow-orchestrator (coordinator)
  └── Uses workflow-utilities for state management
       ↑ Calls other skills as needed

[bmad-planner, speckit-author, git-workflow-manager, quality-enforcer]
  └── All depend on workflow-utilities
       ↑ Called by orchestrator
```

---

### B. Context Flow Across Phases

```
Phase 1 Output → Phase 2 Input
planning/auth-system/
  ├── requirements.md ──┐
  ├── architecture.md   ├─→ SpecKit reads (auto-detected)
  └── epics.md ─────────┘

Phase 2 Output → Phase 3 Input
specs/auth-system/
  ├── spec.md ──┐
  └── plan.md   └─→ Quality gates verify test coverage

Phase 2 Output → Phase 4 Input
specs/auth-system/
  ├── spec.md ──┐
  └── plan.md   └─→ update_asbuilt.py compares vs planning/
                   Creates feedback loop
```

---

## 7. PRODUCTION SAFETY & ROLLBACK

**Tag-based deployment (not branch-based):**
```
✅ Deploy git tag: v1.5.1 (immutable, tested)
❌ Deploy branch head: main (mutable, could change)

Emergency rollback (2 minutes):
git checkout v1.5.0  # Last known good
```

**Main branch protection:**
- Hotfix work isolated in separate worktree (main untouched)
- All changes merge via PR (traceable)
- Tags are immutable (instant rollback possible)

---

## 8. SESSION INITIALIZATION

**Every session starts:**
```bash
python .claude/skills/tech-stack-adapter/scripts/detect_stack.py
```

**Outputs:**
```
TEST_CMD="uv run pytest"
BUILD_CMD="uv sync"
COVERAGE_CMD="uv run pytest --cov=src"
```

**Stored in:** SESSION_CONFIG (memory, not persisted)

**Used by:** quality-enforcer, git-workflow-manager, orchestrator

---

## 9. FILE ORGANIZATION STANDARDS

**Every directory must have:**
```
directory/
├── CLAUDE.md          # Context for Claude (with YAML frontmatter)
├── README.md          # Human docs (with YAML frontmatter)
└── ARCHIVED/
    ├── CLAUDE.md
    ├── README.md
    └── *.zip files    # Deprecated files
```

**YAML frontmatter:**
```yaml
# CLAUDE.md
---
type: claude-context
directory: path/to/dir
purpose: What this directory is for
parent: ../CLAUDE.md
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
  - subdir/CLAUDE.md
related_skills:
  - skill-1
  - skill-2
---
```

**Enforced by:** `directory_structure.py` (all new dirs)

---

## 10. KEY CONSTANTS & RATIONALE

| Constant | Value | Rationale |
|----------|-------|-----------|
| CHECKPOINT_THRESHOLD | 100K tokens | 73% of 136K effective capacity |
| WARNING_THRESHOLD | 80K tokens | Gives time to finish current task |
| TIMESTAMP_FORMAT | YYYYMMDDTHHMMSSZ | Removes colons/hyphens from standard ISO8601 for shell safety and sortability |
| MIN_TEST_COVERAGE | 80% | Prevents technical debt |
| WORK_ITEM_SLUG | pr-N-issue-M | Sequential, PR-scoped, sortable |
| FORCE_PUSH_SAFETY | --force-with-lease | Only if remote unchanged since fetch |

---

## SUMMARY FOR FUTURE CLAUDE INSTANCES

**Load orchestrator first.** It detects context and loads skills dynamically based on phase.

**Understand TODO.md lifecycle:** Register → Update → Archive. Never delete TODO files.

**Know the phases:** BMAD (main) → Worktree + SpecKit (isolated) → Quality (gates) → PR (integrate) → Release (production) → Hotfix (emergency).

**Use callable tools:** Don't reproduce BMAD/SpecKit logic. Run scripts and let them handle interaction.

**Watch token usage:** 100K threshold is real. Save state and checkpoint cleanly.

**Respect branch protection:** main and develop are protected. All changes via PR.

**VCS abstraction exists:** Use it for GitHub/Azure DevOps portability.
