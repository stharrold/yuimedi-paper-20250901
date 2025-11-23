# Archive Directory

This directory contains historical project files and backups maintained for reference and audit purposes.

## 📂 Directory Structure

```
archive/
├── backups/          # Archived backup files (manual and automated)
├── implementation/   # Historical implementation logs and summaries
├── temp/             # Temporary files moved from active areas
└── todo-history/     # Historical TODO snapshots for progress tracking
```

## 🎯 Purpose

The archive serves as a historical record of:
- **TODO Evolution**: Snapshots of task lists showing project progression
- **Implementation History**: Detailed logs of development decisions and implementations
- **Backup Recovery**: Safety net for important files before major changes
- **Audit Trail**: Documentation for understanding project timeline and decisions

## 📅 Retention Policy

- **TODO History**: Kept for minimum 6 months for progress analysis
- **Implementation Logs**: Kept indefinitely for audit and learning purposes
- **Backups**: Kept for 3 months, then reviewed for relevance
- **Temp Files**: Reviewed monthly for permanent archival or deletion

## 🔍 Finding Files

### By Date
Files use timestamp format: `YYYYMMDDTHHMMSSZ` (ISO 8601)

```bash
# Find files from specific date
ls archive/**/TODO_FOR_AI_20250820*.json

# Find recent archives (last 30 days)
find archive/ -type f -mtime -30
```

### By Type
```bash
# TODO history
ls archive/todo-history/

# Implementation logs
ls archive/implementation/

# Backups
ls archive/backups/
```

## 🗃️ Archive Process

Files are archived when:
1. **TODO Sync**: Old TODO versions saved before sync operations
2. **Major Updates**: Important files backed up before significant changes
3. **Completed Phases**: Project phase documentation moved after completion
4. **Manual Archive**: Use `tools/workflow-utilities/archive_manager.py`

## ⚠️ Important Notes

- **Do NOT delete** archive files without team review
- **Keep directory structure** intact for navigation
- **Update this README** when adding new archive categories
- **Reference DECISION_LOG.json** for context on archived decisions

## 🐛 Known Issues in Archived Files

### `implementation/yuiquery-implementation-json_20250903T065157Z.json`

**Issue**: Contains shell variable expansion syntax `${references.salary_data}`, `${references.single_irb}`, etc. that doesn't work in JSON context.

**Context**: This file was an early implementation template that referenced external URLs via a `references` object. The shell syntax was never intended to be executed directly - it served as documentation placeholders.

**Status**: Preserved as historical artifact. Not fixed because:
1. File is archived and not actively used
2. Modifying archives would compromise audit trail integrity
3. The `references` object at the top of the file contains the actual URLs

**Reference URLs** (from the archived file's `references` object):
- salary_data: `https://www.glassdoor.com/Salaries/healthcare-data-analyst-salary-SRCH_KO0,23.htm`
- single_irb: `https://grants.nih.gov/policy/humansubjects/single-irb-policy-multi-site-research.htm`
- hipaa_deidentification: `https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html`

## 📊 Statistics

Last updated: 2025-09-03

- TODO snapshots: 14+ versions tracked
- Implementation logs: Complete August-September 2025 period
- Oldest archive: 2025-08-20
- Most recent: 2025-09-03

## 🔗 Related Documentation

- [Archive Manager Tool](../tools/workflow-utilities/archive_manager.py) - Automated archival
- [DECISION_LOG.json](../DECISION_LOG.json) - Decision history
- [TODO_FOR_AI.json](../TODO_FOR_AI.json) - Current task list

---

*This directory is version controlled to preserve project history.*
