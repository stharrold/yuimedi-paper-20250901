# Data Directory

This directory contains data files used in the YuiQuery Healthcare Analytics research project.

## Purpose

Store research data files, synthetic datasets, and analysis outputs. Large files are gitignored to keep the repository lightweight.

## Contents

- **synthetic/** - Synthea-generated synthetic patient data (if generated)
- **analysis/** - Output files from analysis scripts
- **exports/** - Exported datasets and results

## Data Sources

### Primary Data
Research data is available through the YuiQuery platform at:
- `yuiquery.yuimedi.com/chats/v3/`

### Synthetic Data (Status: Not Required)

**Decision Date**: 2025-11-23
**Status**: `not_needed`

Synthea synthetic patient data generation was originally planned as a backup data source. This task was marked as `not_needed` because:

1. **Primary data available**: Research data is accessible through `yuiquery.yuimedi.com/chats/v3/`
2. **No backup required**: The YuiQuery platform provides reliable data access
3. **Scope reduction**: Per project-management/scope documents, backup data generation was deprioritized

**If synthetic data becomes needed in future**:
- Repository: https://github.com/synthetichealth/synthea
- Generate 100 patients: `./run_synthea -p 100`
- See `compliance/README.md` for data handling guidelines

## Important Notes

1. **No PHI**: This directory should NEVER contain Protected Health Information (PHI)
2. **Gitignored**: Large data files are excluded from version control
3. **De-identified Only**: All data must be de-identified per HIPAA standards

## Related Documentation

- `compliance/README.md` - HIPAA compliance and data handling
- `docs/references/README.md` - Data source references
- `src/analysis/README.md` - Analysis code documentation
