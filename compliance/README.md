# Compliance Directory

This directory contains documentation ensuring the YuiQuery research project meets ethical, legal, and regulatory requirements for healthcare research.

## 📁 Directory Structure

```
compliance/
└── irb/                 # Institutional Review Board determinations
    └── determination.md # IRB exemption documentation
```

## 🎯 Purpose

The compliance directory provides:
- **IRB Documentation**: Human subjects research determinations
- **HIPAA Compliance**: De-identification and privacy standards
- **Regulatory Alignment**: Federal research regulations (45 CFR 46)
- **Audit Trail**: Evidence of regulatory compliance for publications

## 🔒 Key Compliance Areas

### 1. Human Subjects Research (IRB)

**Status**: **EXEMPT** - Not Human Subjects Research

The project uses:
- Pre-anonymized, de-identified data per HIPAA standards
- No direct patient identifiers (Safe Harbor method)
- Synthetic backup data (Synthea-generated)

**Determination**: This project does NOT constitute human subjects research per 45 CFR 46. No IRB review required.

See [irb/determination.md](irb/determination.md) for complete documentation.

### 2. HIPAA Privacy Standards

**Data Classification**:
- ✅ All data pre-anonymized at institutional level
- ✅ 18 HIPAA identifiers removed (Safe Harbor method)
- ✅ No Protected Health Information (PHI) in repository
- ✅ Synthetic data backup available

**Compliance Method**: Safe Harbor De-identification
- Removes 18 specific identifiers defined by HIPAA
- No actual dates of birth, zip codes, or medical record numbers
- Dates shifted by consistent random offset per patient

### 3. Data Security Requirements

**Implementation**:
- Database credentials in environment variables only (never in code)
- SSL/TLS required for all database connections
- Access logging for audit trail
- No production data in development/test environments
- Version control excludes PHI (.gitignore configured)

### 4. Research Ethics

**Ethical Principles**:
- **Beneficence**: Research aims to improve healthcare analytics access
- **Justice**: Findings benefit healthcare organizations broadly
- **Privacy**: Strong de-identification protects patient privacy
- **Transparency**: Methods and limitations clearly documented

## 📋 Regulatory References

### Federal Regulations
- **45 CFR 46**: Protection of Human Subjects
  - https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46
- **HIPAA De-identification Standards**:
  - https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html

### NIH Policies
- **Single IRB Policy** (multi-site research):
  - https://grants.nih.gov/policy/humansubjects/single-irb-policy-multi-site-research.htm

### Industry Standards
- **HIMSS Analytics Adoption Model (AMAM)**: Healthcare analytics maturity framework
- **HL7 FHIR**: Healthcare data interoperability standards

## 🔍 Data Sources & Verification

### Primary Data Source
- **Type**: Institutional pre-anonymized healthcare data
- **De-identification**: Performed by institutional data team before research access
- **Verification**: Annual compliance audit by institutional privacy officer
- **Access**: Via secure VPN with authenticated credentials

### Backup Data Source
- **Type**: Synthea synthetic patient data
- **Purpose**: Testing and development when primary data unavailable
- **Characteristics**: Fully synthetic, no real patient information
- **FHIR Compliance**: Industry-standard healthcare data format

## 📊 Compliance Checklist

Before publication or presentation:

- [x] IRB determination documented
- [x] Data de-identification verified
- [x] No PHI in repository or paper
- [x] Compliance method disclosed in methods section
- [x] Limitations acknowledged
- [ ] Institutional review (if required by organization)
- [ ] Data sharing plan (if requested by journal)

## 🛡️ Risk Mitigation

### Re-identification Risk
**Risk Level**: Minimal (Safe Harbor method)
- No quasi-identifiers that could enable re-identification
- No combination of rare demographic characteristics
- Geographic information limited to state level only

**Mitigation**:
- Expert determination available if needed (statistical disclosure control)
- Aggregate reporting for small cell sizes (n < 10)
- No release of raw data without additional review

### Data Breach Risk
**Risk Level**: Low (de-identified data)
**Mitigation**:
- Even if accessed, data cannot identify individuals
- Database access logging for audit
- Credential rotation quarterly
- Environment variables for secrets management

## 📝 Documentation Requirements

### For Academic Publications
Papers must include:
1. **Methods Section**: Data de-identification method
2. **Limitations Section**: Acknowledge de-identified data limitations
3. **Ethics Statement**: IRB determination status
4. **Data Availability**: Describe access to synthetic backup data

### For Conference Presentations
Presentations should:
1. State data is de-identified per HIPAA
2. Note IRB exemption status
3. Acknowledge institutional data source
4. Provide synthetic data option for reproducibility

## 🔗 Related Documentation

- [Database Configuration](../config/database/README.md) - Secure data access
- [Main Research Paper](../paper.md) - Methods section includes compliance discussion
- [IRB Determination](irb/determination.md) - Complete exemption documentation

## 📞 Compliance Contacts

### Internal Questions
- Review CLAUDE.md for project standards
- Check DECISION_LOG.json for compliance decisions
- Consult with institutional privacy officer if needed

### External Resources
- **HHS HIPAA Guidance**: https://www.hhs.gov/hipaa/
- **OHRP (Human Research Protections)**: https://www.hhs.gov/ohrp/
- **NIH Research Ethics**: https://www.nih.gov/health-information/nih-clinical-research-trials-you/basics

## 🔄 Compliance Review Schedule

- **Initial Review**: Completed 2025-09-01
- **Annual Review**: Required for ongoing projects
- **Pre-Publication**: Verify all compliance documentation current
- **Data Source Changes**: Requires new compliance review

## ⚠️ Important Notes

1. **Do NOT add actual PHI** to this repository
2. **Verify de-identification** before any data commit
3. **Update documentation** if data sources change
4. **Maintain audit trail** in DECISION_LOG.json
5. **Consult institutional compliance** before major changes

## 📈 Compliance Evolution

### Current Status (v1.0)
- IRB exemption documented
- HIPAA compliance via Safe Harbor de-identification
- Synthetic backup data available

### Future Considerations
- Multi-site data collaboration (would require Single IRB)
- International data sources (GDPR compliance)
- Commercial partnerships (additional legal review)

---

*Last Updated: 2025-09-01*
*Status: EXEMPT - Not Human Subjects Research*
*Compliance Method: HIPAA Safe Harbor De-identification*
