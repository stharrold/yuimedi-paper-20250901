# Skill Update Checklist

## Purpose

This checklist ensures that when a skill implementation changes, all related documentation files are updated consistently to prevent documentation drift and version mismatches.

## When to Use This Checklist

Use this checklist when:
- Modifying a skill's Python script (e.g., `create_planning.py`)
- Adding/removing features from a skill
- Changing a skill's interactive Q&A flow
- Updating templates used by a skill
- Modifying skill integration with other skills
- Updating token efficiency or performance metrics

## Version Numbering (Semantic Versioning)

Skills and WORKFLOW.md use semantic versioning: `MAJOR.MINOR.PATCH`

**MAJOR (X.0.0):**
- Breaking changes to skill API or interface
- Removed features or functionality
- Changes requiring updates to calling code
- Major workflow restructuring

**MINOR (x.Y.0):**
- New features or capabilities added
- New parameters or options added (backward compatible)
- Enhanced interactive Q&A
- New template sections
- Improved integration with other skills

**PATCH (x.y.Z):**
- Bug fixes
- Documentation updates
- Template formatting improvements
- Error message improvements
- Performance optimizations (no behavior change)

## Complete Update Checklist

### Step 1: Determine Version Bump

- [ ] Identify the type of change (breaking, feature, fix)
- [ ] Determine new version number based on semantic versioning
- [ ] Current version: `________`
- [ ] New version: `________`
- [ ] Change type: `☐ MAJOR  ☐ MINOR  ☐ PATCH`

### Step 2: Update the Skill's SKILL.md File

**File:** `.claude/skills/<skill-name>/SKILL.md`

- [ ] Update version in YAML frontmatter:
  ```yaml
  ---
  name: <skill-name>
  version: X.Y.Z  ← Update this
  description: |
    ...
  ---
  ```

- [ ] Update "## Purpose" section if purpose changed
- [ ] Update "## When to Use" section if triggers changed
- [ ] Update "## Interactive Callable Tool" section:
  - [ ] Command syntax (if arguments changed)
  - [ ] Example usage (if parameters changed)
  - [ ] Interactive session flow (if Q&A changed)
  - [ ] Token efficiency metrics (if changed)

- [ ] Update "## Integration with Workflow" section if phase changes
- [ ] Update "## Integration with [Other Skill]" sections if affected
- [ ] Update "## Output Files" section if file structure changed
- [ ] Update "## Template Placeholders" section if templates changed
- [ ] Update "## Best Practices" section if recommendations changed

### Step 3: Update the Skill's CLAUDE.md File

**File:** `.claude/skills/<skill-name>/CLAUDE.md`

- [ ] Update usage instructions
- [ ] Update command examples (match SKILL.md examples)
- [ ] Update integration notes with other skills
- [ ] Update token efficiency metrics
- [ ] Update workflow phase references
- [ ] Update "## Key Scripts" section

### Step 4: Update WORKFLOW.md (Root)

**File:** `WORKFLOW.md`

Find and update relevant sections:

- [ ] **Version number** (if WORKFLOW.md structure changed):
  - Line 3: `**Version:** X.Y.Z`

- [ ] **Phase section** where this skill is used:
  - Example: Phase 1 (BMAD), Phase 2 (SpecKit), Phase 3 (Quality), etc.

- [ ] **Skill Structure** section (lines 38-69):
  - [ ] Update skill description
  - [ ] Update token estimates

- [ ] **Phase-specific subsections**:
  - [ ] Command syntax and examples
  - [ ] Interactive session flow descriptions
  - [ ] Output file structure
  - [ ] Token savings metrics

- [ ] **Common Commands Reference** section (lines 1457-1538):
  - [ ] Update command syntax
  - [ ] Update examples

- [ ] **Related Skills** section at end of affected phases
  - [ ] Update hyperlinks if skill renamed

### Step 5: Update Root CLAUDE.md

**File:** `CLAUDE.md` (root directory)

- [ ] Update "## Workflow v5.0 Architecture" section:
  - [ ] Skill list and descriptions
  - [ ] Token savings metrics

- [ ] Update "## Common Development Commands" section:
  - [ ] Command syntax
  - [ ] Examples

- [ ] Update "## Key Workflow Behaviors" if applicable
- [ ] Update "## Context Monitoring" if token metrics changed
- [ ] Update version history in semantic versioning section

### Step 6: Update Templates (If Applicable)

**Files:** `.claude/skills/<skill-name>/templates/*.template`

- [ ] Update template structure if changed
- [ ] Update placeholders if added/removed
- [ ] Update sections if reorganized
- [ ] Test template processing with updated script

### Step 7: Update Integration Points

For each skill that integrates with the updated skill:

- [ ] **workflow-orchestrator/SKILL.md**:
  - [ ] Update phase instructions
  - [ ] Update script invocation examples

- [ ] **Other dependent skills**:
  - [ ] List dependent skills: `_________________`
  - [ ] Update their SKILL.md integration sections
  - [ ] Update their CLAUDE.md references

### Step 8: Create CHANGELOG Entry

**File:** `.claude/skills/<skill-name>/CHANGELOG.md` (create if doesn't exist)

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature or capability

### Changed
- Modified behavior or interface

### Fixed
- Bug fix or correction

### Token Efficiency
- Previous: X tokens
- New: Y tokens
- Savings: Z tokens (N%)
```

Example:
```markdown
## [5.1.0] - 2025-10-24

### Added
- Interactive Q&A for database migration strategy
- Auto-detection of BMAD planning context

### Changed
- Epic breakdown now includes complexity reasoning
- Template processing uses regex for better placeholder matching

### Token Efficiency
- Previous: 2,500 tokens (manual approach)
- New: 200 tokens (callable tool)
- Savings: 2,300 tokens (92%)
```

### Step 9: Validate Consistency

Run validation script (once created):

```bash
python .claude/skills/workflow-utilities/scripts/validate_versions.py
```

Manual validation (until script exists):

- [ ] All skill versions in YAML frontmatter match expectations
- [ ] WORKFLOW.md references match updated skill versions
- [ ] Command examples are identical across SKILL.md, CLAUDE.md, WORKFLOW.md
- [ ] Token metrics are consistent across all files
- [ ] Integration descriptions match in all affected skills

### Step 9.5: Verify Alignment with Official Documentation

**NEW:** Check if changes align with official Claude Code best practices:

```bash
# Review official docs for your skill type
# https://docs.claude.com/en/docs/agents-and-tools/agent-skills
# https://docs.claude.com/en/docs/agents-and-tools/building-agents
```

**Verification checklist:**

- [ ] **Review official patterns:** Check if official docs have new recommendations
- [ ] **Compare changes:** Does your update diverge from official patterns?
- [ ] **Document discrepancies:** If diverging, document rationale in SKILL.md:
  ```markdown
  ## Official Documentation Alignment

  **Discrepancy:** [Describe what differs]
  **Official pattern:** [What official docs recommend]
  **Local pattern:** [What this skill uses]
  **Citation:** https://docs.claude.com/en/docs/agents-and-tools/agent-skills
  **Rationale:** [Why local pattern is used for this workflow]
  ```
- [ ] **Update SKILL.md:** Add or update "Official Documentation Alignment" section
- [ ] **Alert users:** If significant divergence, mention in CHANGELOG.md

**When to document divergence:**
- File structure differs from official spec
- YAML frontmatter has additional fields
- Integration patterns unique to this workflow
- Any workflow-specific customizations

**Example discrepancy documentation:**
```markdown
## Official Documentation Alignment

**File Structure:**
- Official: `skill.md`, `README.md`
- Local: `SKILL.md`, `CLAUDE.md`, `README.md`, `CHANGELOG.md`, `ARCHIVED/`
- Citation: https://docs.claude.com/en/docs/agents-and-tools/agent-skills
- Rationale: Extended structure supports multi-phase workflow with version
  tracking (CHANGELOG.md), Claude Code context (CLAUDE.md), and archival
  system (ARCHIVED/).
```

### Step 10: Commit Changes

Use semantic commit message format:

```bash
git add .claude/skills/<skill-name>/ WORKFLOW.md CLAUDE.md
git commit -m "feat(<skill-name>): <brief description>

Updated <skill-name> from vX.Y.Z to vA.B.C:
- <summary of changes>

Updated documentation:
- .claude/skills/<skill-name>/SKILL.md (version, commands, integration)
- .claude/skills/<skill-name>/CLAUDE.md (usage, examples)
- WORKFLOW.md (Phase N section, commands, metrics)
- CLAUDE.md (version history, commands)

Token efficiency:
- Previous: X tokens
- New: Y tokens
- Savings: Z tokens (N%)

Refs: .claude/skills/<skill-name>/CHANGELOG.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
"
```

### Step 11: Test the Update

- [ ] Run the updated skill script manually:
  ```bash
  python .claude/skills/<skill-name>/scripts/<script-name>.py --help
  ```

- [ ] Verify interactive Q&A flow (if applicable)
- [ ] Verify output files match updated templates
- [ ] Verify git commit message format
- [ ] Check for any errors or warnings

### Step 12: Archive Previous Version (Optional)

If making major changes:

```bash
# Archive previous SKILL.md version
cp .claude/skills/<skill-name>/SKILL.md \
   .claude/skills/<skill-name>/ARCHIVED/SKILL_vX.Y.Z.md

# Archive previous WORKFLOW.md version (if WORKFLOW.md version changed)
cp WORKFLOW.md ARCHIVED/Workflow-vX-Y-Z.md
```

## Quick Reference: Files to Check

When updating any skill, always check these files:

### Skill-Specific Files
```
.claude/skills/<skill-name>/
├── SKILL.md          ← Update: version, commands, integration
├── CLAUDE.md         ← Update: usage, examples
├── CHANGELOG.md      ← Update: add new version entry
├── templates/        ← Update: if templates changed
└── scripts/          ← Primary change location
```

### Repository-Wide Files
```
WORKFLOW.md           ← Update: phase sections, commands, metrics
CLAUDE.md             ← Update: commands, version history
```

### Integration Files (Check if Applicable)
```
.claude/skills/workflow-orchestrator/SKILL.md    ← If orchestrator calls updated
.claude/skills/bmad-planner/SKILL.md             ← If BMAD integrates
.claude/skills/speckit-author/SKILL.md           ← If SpecKit integrates
.claude/skills/git-workflow-manager/SKILL.md     ← If git operations changed
.claude/skills/quality-enforcer/SKILL.md         ← If quality gates changed
.claude/skills/workflow-utilities/SKILL.md       ← If utilities changed
```

## Common Mistakes to Avoid

❌ **Updating script without updating SKILL.md version**
- All script changes require version bump in SKILL.md frontmatter

❌ **Inconsistent command examples**
- Command syntax must match exactly in SKILL.md, CLAUDE.md, WORKFLOW.md

❌ **Forgetting to update WORKFLOW.md**
- WORKFLOW.md phase sections must reflect current skill behavior

❌ **Not updating token efficiency metrics**
- If script changes affect token usage, update metrics in all files

❌ **Missing integration updates**
- If skill changes affect other skills, update their integration sections

❌ **No CHANGELOG entry**
- Every version bump requires a CHANGELOG entry

❌ **Incorrect semantic versioning**
- Follow MAJOR.MINOR.PATCH rules strictly

## Example: Updating bmad-planner from 5.0.0 to 5.1.0

### Change Made
Added interactive Q&A for database migration strategy in `create_planning.py`

### Version Bump Decision
- **Type:** MINOR (new feature, backward compatible)
- **Old version:** 5.0.0
- **New version:** 5.1.0

### Files Updated

1. ✓ `.claude/skills/bmad-planner/SKILL.md`
   - Version: 5.0.0 → 5.1.0
   - Added migration Q&A to interactive flow section
   - Updated token metrics (if changed)

2. ✓ `.claude/skills/bmad-planner/CLAUDE.md`
   - Updated Q&A example to include migration question

3. ✓ `WORKFLOW.md`
   - Phase 1 section: Updated interactive session example
   - Added migration question to example flow

4. ✓ `CLAUDE.md` (root)
   - Updated Phase 1 description to mention migration

5. ✓ `.claude/skills/bmad-planner/CHANGELOG.md`
   - Added [5.1.0] entry with new feature

6. ✓ `.claude/skills/speckit-author/SKILL.md`
   - Updated integration section (SpecKit detects migration from BMAD)

### Commit Message
```
feat(bmad): add database migration strategy Q&A

Updated bmad-planner from v5.0.0 to v5.1.0:
- Added interactive Q&A for database migration strategy (Alembic/Manual/None)
- Enhanced architecture document generation with migration details

Updated documentation:
- .claude/skills/bmad-planner/SKILL.md (version 5.1.0, Q&A flow)
- .claude/skills/bmad-planner/CLAUDE.md (example updated)
- WORKFLOW.md (Phase 1 interactive session)
- CLAUDE.md (Phase 1 description)
- .claude/skills/speckit-author/SKILL.md (integration note)

Refs: .claude/skills/bmad-planner/CHANGELOG.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Related Documentation

- **[CONTRIBUTING.md](../../CONTRIBUTING.md)** - Contributor guidelines (to be created)
- **[validate_versions.py](../workflow-utilities/scripts/validate_versions.py)** - Version consistency validator (to be created)
- **[sync_skill_docs.py](../workflow-utilities/scripts/sync_skill_docs.py)** - Documentation sync tool (to be created)
- **[WORKFLOW.md](../../WORKFLOW.md)** - Complete workflow guide
- **[CLAUDE.md](../../CLAUDE.md)** - Claude Code interaction guide

## Feedback and Improvements

If you encounter issues with this checklist or have suggestions for improvement:

1. Create an issue in the repository
2. Update this checklist directly
3. Add notes in ARCHIVED/ with timestamp

Last updated: 2025-10-24
Version: 1.0.0
