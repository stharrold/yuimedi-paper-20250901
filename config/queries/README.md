# SQL Query Library

## Purpose
Centralized repository of SQL queries used across all three research papers. Queries are version-controlled for reproducibility and sharing.

## Organization

### Paper 1: Literature Review Queries
Location: `paper1/`

- **Statistical Analysis**
  - Healthcare analytics maturity distribution
  - Turnover rate calculations
  - Knowledge gap quantification

- **Evidence Gathering**
  - Literature database searches
  - Citation network queries
  - Theme extraction support

### Paper 2: Proof of Concept Queries
Location: `paper2/`

- **Schema Discovery**
  - Table relationship detection
  - Primary/foreign key inference
  - Data profiling queries

- **Validation Queries**
  - Accuracy testing queries
  - Performance benchmarks
  - Error analysis queries

- **Algorithm Testing**
  - NL2SQL translation tests
  - Edge case validations
  - Degraded data scenarios

### Paper 3: FHIR Mapping Queries
Location: `paper3/`

- **Mapping Validation**
  - FHIR resource extraction
  - Cross-system comparisons
  - Semantic preservation tests

- **Interoperability Tests**
  - Epic integration queries
  - OMOP CDM transformations
  - CMS quality measure queries

## Query Standards

### Naming Convention
`[paper_number]_[category]_[description].sql`

Examples:
- `p1_stats_turnover_rates.sql`
- `p2_validate_schema_inference.sql`
- `p3_fhir_patient_mapping.sql`

### Documentation Requirements
Each query file must include:
```sql
-- Query: [Name]
-- Purpose: [What this query does]
-- Paper: [1, 2, or 3]
-- Author: [Developer initials]
-- Date: [Creation date]
-- Dependencies: [Required tables/views]
-- Expected Runtime: [Estimated execution time]
```

### Performance Guidelines
- Use EXPLAIN ANALYZE for optimization
- Document index requirements
- Include execution plans for complex queries
- Note any performance considerations

## Reusable Components

### Common Table Expressions (CTEs)
Store frequently used CTEs in `common/`

### Utility Functions
Database functions in `functions/`

### Views
Materialized views in `views/`

## Version Control
- All queries must be tested before committing
- Include sample results in comments
- Document any schema assumptions
- Tag queries used in published papers
