# Configuration Directory

This directory contains configuration files and documentation for database connections, query management, and system settings for the YuiQuery research project.

## 📁 Directory Structure

```
config/
├── database/        # Database connection configuration and schema documentation
└── queries/         # Query templates and optimization guidelines
```

## 🎯 Purpose

The config directory provides:
- **Database Configuration**: Connection settings and schema documentation
- **Query Management**: SQL templates and optimization strategies
- **Environment Setup**: Development and production configuration guidance
- **Security Standards**: Credential management and access control

## 🗄️ Database Configuration (database/)

### Overview
Configuration for accessing de-identified healthcare data sources:
- **Primary**: Institutional pre-anonymized healthcare database
- **Backup**: Synthea synthetic patient data (100+ synthetic patients)
- **Database Type**: PostgreSQL (configurable)

### Key Files
See [database/README.md](database/README.md) for complete documentation.

### Database Schema
Core healthcare tables:
- `patient_demographics` - Basic patient information (de-identified)
- `clinical_encounters` - Visit and encounter data
- `diagnoses` - ICD-10 coded conditions
- `procedures` - CPT coded procedures
- `medications` - Prescription data
- `lab_results` - Laboratory test results
- `vital_signs` - Blood pressure, weight, temperature

Metadata tables:
- `data_dictionary` - Column descriptions and data types
- `table_relationships` - Foreign key mappings and join paths
- `audit_log` - Data access tracking for compliance

### Connection Configuration
```bash
# .env file (create locally, NEVER commit)
DB_HOST=your_host
DB_PORT=5432
DB_NAME=yuiquery_research
DB_USER=your_username
DB_PASSWORD=your_password
DB_SSL_MODE=require
```

**Security Requirements**:
- ✅ All credentials in environment variables only
- ✅ SSL/TLS required for all connections
- ✅ No credentials in code or version control
- ✅ Access logging for compliance audit trail

## 🔍 Query Management (queries/)

### Overview
SQL query templates and optimization guidelines for healthcare analytics.

### Key Files
See [queries/README.md](queries/README.md) for complete documentation.

### Query Categories
- **Patient Cohort Identification**: Finding patients meeting clinical criteria
- **Encounter Analysis**: Visit patterns and utilization
- **Clinical Quality Measures**: HEDIS and other quality metrics
- **Operational Analytics**: Resource utilization and efficiency
- **Financial Analysis**: Cost and revenue reporting

### Query Optimization
- Index strategy documentation
- Join path optimization for complex healthcare queries
- Aggregation performance patterns
- Connection pooling configuration

## 🔒 Security & Compliance

### Credential Management
**NEVER commit credentials to version control**

✅ **Correct**:
```python
import os
db_password = os.environ.get('DB_PASSWORD')
```

❌ **INCORRECT**:
```python
db_password = "actual_password_here"  # NEVER DO THIS
```

### Data Access
- All data is **de-identified** per HIPAA standards
- **IRB exempt** (see `compliance/irb/determination.md`)
- **Audit logging** required for all queries
- **No PHI** in logs or error messages

### Connection Security
- **SSL/TLS required** for all database connections
- **VPN required** for accessing institutional database
- **Credential rotation** quarterly (documented in DECISION_LOG.json)
- **No production data** in development/test environments

## 🛠️ Setup Instructions

### First-Time Setup

```bash
# 1. Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Setup project environment
uv sync

# 3. Create .env file (NEVER commit this file)
cat > .env << EOF
DB_HOST=your_host
DB_PORT=5432
DB_NAME=yuiquery_research
DB_USER=your_username
DB_PASSWORD=your_password
DB_SSL_MODE=require
EOF

# 4. Verify .env is in .gitignore
grep "^\.env$" .gitignore

# 5. Test connection (using python script from src/)
uv run python src/test_db_connection.py
```

### Verify .gitignore
Ensure these patterns are in `.gitignore`:
```
.env
*.env
.env.*
credentials.*
secrets.*
```

## 📊 Data Sources

### Primary: Institutional Healthcare Data
- **Type**: Pre-anonymized clinical and operational data
- **Size**: Varies by institution (typically millions of encounters)
- **Refresh**: Monthly from institutional data warehouse
- **Access**: Secure VPN with authenticated credentials
- **Compliance**: HIPAA Safe Harbor de-identification

### Backup: Synthea Synthetic Data
- **Type**: Fully synthetic patient data
- **Size**: 100+ synthetic patients with complete clinical histories
- **Purpose**: Development and testing when primary unavailable
- **Format**: FHIR-compliant JSON
- **Advantages**: No PHI, unlimited access, publicly shareable

### Switching Data Sources
```bash
# Use institutional data (default)
export DATA_SOURCE=institutional

# Use synthetic data for testing
export DATA_SOURCE=synthea

# Run analysis with selected source
uv run python src/analysis/your_analysis.py
```

## 🔍 Configuration Files

### Environment Variables (.env)
**Location**: Repository root (git-ignored)
**Purpose**: Database credentials and environment-specific settings
**Template**: Available in `config/database/` documentation

### Application Config (pyproject.toml)
**Location**: Repository root
**Purpose**: Python dependencies and tool configuration
**Tracked**: Yes (version controlled)

### Query Templates (queries/)
**Location**: `config/queries/`
**Purpose**: Reusable SQL patterns for common healthcare analytics
**Tracked**: Yes (examples only, no actual data)

## 📝 Configuration Standards

### Naming Conventions
- **Database**: snake_case for tables and columns
- **Environment Variables**: UPPER_CASE with underscores
- **Config Files**: lowercase with hyphens or underscores

### Documentation Requirements
- All config files must have inline documentation
- Security implications clearly noted
- Example values (never actual credentials)
- Related files cross-referenced

### Version Control
- ✅ **Commit**: Schema documentation, query templates, README files
- ❌ **NEVER commit**: Credentials, .env files, actual connection strings

## 🔗 Related Documentation

- [Database Configuration Details](database/README.md) - Complete database setup
- [Query Optimization Guide](queries/README.md) - SQL templates and patterns
- [Compliance Documentation](../compliance/README.md) - IRB and HIPAA compliance
- [Source Code](../src/README.md) - Code using these configurations
- [CLAUDE.md](../CLAUDE.md) - Project development standards

## 🧪 Testing Configuration

### Test Database Connection
```bash
# Test institutional database connection
uv run python -c "import os; from sqlalchemy import create_engine; \
  engine = create_engine(os.environ.get('DATABASE_URL')); \
  print('Connection successful' if engine.connect() else 'Failed')"

# Test with synthetic data
export DATA_SOURCE=synthea
uv run python src/test_synthea_connection.py
```

### Verify Security
```bash
# Ensure no credentials in tracked files
git grep -i "password" -- ':!*.md' ':!*.txt'  # Should return nothing

# Verify .env is git-ignored
git check-ignore -v .env  # Should show .gitignore rule

# Check for accidentally committed secrets
git log --all --full-history --source -- '*.env*'  # Should be empty
```

## 📈 Configuration Evolution

### Current Version (v1.0)
- PostgreSQL primary database
- Synthea backup data source
- Environment variable credential management
- SSL/TLS required connections

### Future Considerations
- Multi-database support (MySQL, SQL Server)
- Cloud database services (RDS, Cloud SQL)
- Containerized development environments
- Automated credential rotation

## ⚠️ Important Warnings

1. **NEVER commit credentials** - Always use environment variables
2. **Test in development first** - Never query production directly
3. **Verify de-identification** - Ensure no PHI exposure
4. **Use SSL/TLS** - Unencrypted connections prohibited
5. **Log access** - Maintain audit trail for compliance

## 🛟 Troubleshooting

### Connection Issues
```bash
# Check environment variables set
printenv | grep DB_

# Test network connectivity
nc -zv $DB_HOST $DB_PORT

# Verify SSL certificate
openssl s_client -connect $DB_HOST:$DB_PORT -starttls postgres
```

### Credential Issues
```bash
# Verify .env file exists and has correct permissions
ls -la .env  # Should be 600 or 400 permissions

# Reload environment variables
set -a; source .env; set +a

# Test credential access
echo $DB_PASSWORD  # Should show password (only in secure environment)
```

### Query Performance
- Check index usage in queries/README.md
- Review connection pooling settings
- Monitor query execution plans
- Consult database/ documentation for optimization

---

*Configuration for YuiQuery research project database and query management*
*All credentials must be in environment variables - NEVER commit to version control*
