# FHIR/OMOP Mapping Specifications

## Purpose
Healthcare data standard mappings for YuiQuery interoperability

## Supported Standards

### FHIR R4
- Patient resources
- Observation resources
- Medication resources
- Procedure resources
- Condition resources
- Encounter resources

### OMOP CDM v5.4
- Person table mappings
- Visit occurrence
- Condition occurrence
- Drug exposure
- Measurement
- Procedure occurrence

### Epic Integration
- Epic Clarity database mappings
- Epic FHIR endpoints
- Custom Epic extensions

### CMS Quality Models
- Quality measure mappings
- eCQM specifications
- QRDA category compliance

## Mapping Components

### Core Mappings
1. **Entity Mappings**
   - Source to target field mappings
   - Value set transformations
   - Unit conversions

2. **Terminology Mappings**
   - ICD-10 to SNOMED
   - CPT to LOINC
   - RxNorm mappings
   - Custom code mappings

3. **Query Transformations**
   - SQL to FHIR queries
   - FHIR to SQL translations
   - Cross-system query routing

### JSON-LD Storage
- Reusable mapping definitions
- Version-controlled transformations
- Shareable query templates

## Implementation Strategy
1. Define source schema (from Paper 2)
2. Map to FHIR resources
3. Create bidirectional transformations
4. Validate with test queries
5. Store in JSON-LD format

## Quality Assurance
- Mapping completeness validation
- Semantic preservation testing
- Performance benchmarking
- Compliance verification
