# Reference Materials

This directory contains reference documents and resources used in the YuiQuery Healthcare Analytics Research project.

## Encryption

PDF files in this directory are encrypted at rest using [git-crypt](https://github.com/AGWA/git-crypt). This protects copyrighted materials while allowing version control.

### Access Requirements

To access encrypted PDFs:
1. Obtain the symmetric key file (`yuimedi-paper-20250901.git-crypt-key`)
2. Run: `git-crypt unlock /path/to/yuimedi-paper-20250901.git-crypt-key`

### Key Backup

The key is stored outside this repository. Back it up to a secure location (e.g., OS keyring, password manager).

### For New Contributors

Request the git-crypt key from the repository owner. Without it, PDF files appear as binary blobs.

## 📁 Contents

### 20250905_Anthropic_Code-Modernization-Playbook.pdf
**Source**: Anthropic
**Date**: September 5, 2025
**Pages**: 8
**Size**: 281KB

**Description**: Anthropic's guide to code modernization best practices, including Claude Code usage patterns and AI-assisted development workflows.

**Relevance to Project**:
- Best practices for AI-assisted research and documentation
- Claude Code integration patterns used in this repository
- Modern development workflows referenced in CLAUDE.md

**Citation**:
```bibtex
@techreport{anthropic2025modernization,
  title = {Code Modernization Playbook},
  author = {Anthropic},
  institution = {Anthropic PBC},
  year = {2025},
  month = {9},
  type = {Technical Guide},
  url = {https://anthropic.com/}
}
```

**Referenced In**:
- [`CLAUDE.md`](../../CLAUDE.md) - Development workflow guidance
- [`README.md`](../../README.md) - Project setup instructions
- GitHub Issues #126, #137, #151 - Integration tasks

## 📚 Adding New References

When adding reference materials to this directory:

1. **Use descriptive filenames**: `YYYYMMDD_Source_Title.pdf`
2. **Update this README**: Add entry with metadata
3. **Provide citation**: Include proper academic/technical citation
4. **Note relevance**: Explain why this reference is important
5. **Track usage**: List where the reference is cited

### Reference Naming Convention
```
YYYYMMDD_Source_Title-Description.extension

Examples:
20250905_Anthropic_Code-Modernization-Playbook.pdf
20250810_HIMSS_Analytics-Maturity-Model.pdf
20250715_NIH_Research-Ethics-Guidelines.pdf
```

## 🔗 Reference Types

### Industry Reports
- Vendor documentation
- Technical whitepapers
- Implementation guides
- Best practice playbooks

### Academic Resources
- Research methodology guides
- Statistical analysis references
- Systematic review protocols
- Citation style guides

### Standards & Regulations
- Healthcare IT standards (HL7, FHIR)
- Compliance guidelines (HIPAA, IRB)
- Data governance frameworks
- Quality assurance standards

### Technical Documentation
- API documentation
- Tool usage guides
- Configuration references
- Architecture patterns

## 📖 Usage Guidelines

### Copyright & Fair Use
- **Respect copyright**: Only include materials with appropriate permissions
- **Fair use**: Academic research use under educational exemption
- **Attribution**: Always cite sources properly
- **Distribution**: Do not redistribute proprietary materials publicly

### Version Control
- **Track versions**: Use dated filenames for version clarity
- **Archive old versions**: Move superseded documents to `ARCHIVED/`
- **Update references**: When new versions available, update citations
- **Note changes**: Document significant updates in this README

### File Management
- **Keep organized**: Use subdirectories if collection grows large
- **Reasonable size**: Large files (>10MB) should be hosted externally
- **Format preference**: PDF for documents, Markdown for text
- **Searchable**: Use OCR for scanned documents when possible

## 🔍 Finding References

### Search in This Directory
```bash
# List all references
ls -lh docs/references/

# Search by source
ls docs/references/ | grep -i "anthropic"

# Search by date
ls docs/references/ | grep "202509"

# Full-text search (if PDFs are OCR'd)
grep -r "machine learning" docs/references/
```

### Citation Lookup
All references cited in the main paper can be found in:
- [`paper.md`](../../paper.md) - Full citations in References section
- Format: `[A#]` for academic sources, `[I#]` for industry sources

## 📊 Current References

### By Category
- **Industry**: 1 (Anthropic Code Modernization Playbook)
- **Academic**: 0
- **Standards**: 0
- **Technical**: 0

### By Year
- **2025**: 1 document
- Total: 1 document

## 🔄 Maintenance

### Regular Reviews
- **Quarterly**: Check for updated versions of reference materials
- **Before publication**: Verify all citations are current
- **Annual**: Archive outdated references, update citations

### Adding to Bibliography
When citing references from this directory in `paper.md`:
1. Add full citation to References section
2. Use appropriate citation format `[A#]` or `[I#]`
3. Include URL or DOI when available
4. Note access date for web resources

## 🔗 Related Documentation

- [Main Research Paper](../../paper.md) - Citations and references
- [Documentation Directory](../README.md) - Paper organization
- [Archive](../../ARCHIVED/README.md) - Historical references

---

*Reference materials for YuiQuery Healthcare Analytics Research project*
*Last Updated: 2025-11-20*
