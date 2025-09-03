# Database Configuration

## Connection Details
- **Database Type**: PostgreSQL (or as configured)
- **Host**: Configured via environment variables
- **Database Name**: yuiquery_research
- **Credentials**: Store in .env file (NEVER commit to repository)

## Environment Variables
```bash
# .env file (create locally, do not commit)
DB_HOST=your_host
DB_PORT=5432
DB_NAME=yuiquery_research
DB_USER=your_username
DB_PASSWORD=your_password
DB_SSL_MODE=require
```

## Data Sources

### Primary: Institutional Pre-anonymized Healthcare Data
- De-identified per HIPAA standards
- Access via secure VPN only
- Refresh schedule: Monthly

### Backup: Synthea Synthetic Patient Data
- 100+ synthetic patients
- FHIR-compliant format
- For testing when primary unavailable

## Database Schema

### Core Tables
- `patient_demographics` - Basic patient information
- `clinical_encounters` - Visit and encounter data
- `diagnoses` - ICD-10 coded conditions
- `procedures` - CPT coded procedures
- `medications` - Prescription and administration data
- `lab_results` - Laboratory test results
- `vital_signs` - Blood pressure, weight, etc.

### Metadata Tables
- `data_dictionary` - Column descriptions
- `table_relationships` - Foreign key mappings
- `audit_log` - Data access tracking

## Security Requirements
1. All connections must use SSL/TLS
2. Credentials stored in environment variables only
3. No production data in development/test
4. Access logging required for compliance
5. PHI handling per HIPAA guidelines

## Query Performance
- Index strategy documented in migrations/
- Query optimization guidelines in queries/
- Connection pooling configured for efficiency

## Backup and Recovery
- Daily automated backups
- Point-in-time recovery enabled
- Test restore procedures monthly