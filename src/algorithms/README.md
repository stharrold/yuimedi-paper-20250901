# Natural Language to SQL Algorithms

## Purpose
Core algorithms for YuiQuery's natural language to SQL translation capabilities

## Key Components

### Schema Inference
- Automatic discovery of table relationships
- Primary/foreign key detection
- Data type inference from values
- Column purpose classification

### NL2SQL Translation
- Query intent classification
- Entity recognition in healthcare context
- SQL query generation
- Query optimization

### Healthcare-Specific Adaptations
- Medical terminology handling
- Clinical workflow understanding
- HIPAA-compliant query filtering
- Patient cohort identification

## Algorithm Categories

1. **Parsing & Understanding**
   - Natural language parsing
   - Medical entity extraction
   - Intent classification

2. **Schema Analysis**
   - Table relationship discovery
   - Statistical profiling
   - Metadata inference

3. **Query Generation**
   - SQL construction
   - Join path optimization
   - Aggregation handling

4. **Validation & Safety**
   - Query validation
   - Performance estimation
   - Privacy preservation

## Implementation Notes
- Python-based implementation
- Leverages healthcare NLP libraries
- Integrates with database via config/database
- Test cases use synthetic data only