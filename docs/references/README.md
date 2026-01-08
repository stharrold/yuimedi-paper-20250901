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

### 2019_Yuan_JAMIA_Criteria2Query.pdf
**Source**: Journal of the American Medical Informatics Association (JAMIA)
**Date**: April 2019
**Pages**: 294--305
**Size**: [Check PDF]

**Description**: Criteria2Query: a natural language interface to clinical databases for cohort definition.

**Relevance to Project**:
- Demonstrates NL interface for cohort definition.
- Provides metrics on productivity gains (speedup in query specification).

**Citation**:
```bibtex
@article{yuan2019,
  author = {Yuan, C., Ryan, P. B., Ta, C., Guo, Y., Li, Z., et al},
  title = {{Criteria2Query: a natural language interface to clinical databases for cohort definition}},
  year = {2019},
  journal = {Journal of the American Medical Informatics Association},
  doi = {10.1093/jamia/ocy178},
  url = {https://academic.oup.com/jamia/article-abstract/26/4/294/5308980},
  file = {../library/docs/2019_Yuan_JAMIA_Criteria2Query.pdf},
  note = {Original citation: [A35]},
}
```

### 2006_Rao_European-Management-Review_Organizational-Learning-Forgetting.pdf
**Source**: European Management Review
**Date**: 2006
**Pages**: 77--85
**Size**: [Check PDF]

**Description**: Organizational learning and forgetting: The effects of turnover and structure.

**Relevance to Project**:
- Provides theoretical basis for the "Organizational Knowledge Ratchet".
- Discusses how structure buffers against knowledge loss from turnover.

**Citation**:
```bibtex
@article{rao2006,
  author = {Rao, R. D. and Argote, L.},
  title = {Organizational learning and forgetting: The effects of turnover and structure},
  journal = {European Management Review},
  year = {2006},
  volume = {3},
  number = {2},
  pages = {77--85},
  url = {https://onlinelibrary.wiley.com/doi/abs/10.1057/palgrave.emr.1500057},
  file = {../library/docs/2006_Rao_European-Management-Review_Organizational-Learning-Forgetting.pdf},
  note = {Original citation: [New]}
}
```

### 2007_Richesson_JAMIA_Data-Standards-Clinical-Research.pdf
**Source**: Journal of the American Medical Informatics Association (JAMIA)
**Date**: 2007
**Pages**: 687--695
**Size**: [Check PDF]

**Description**: Data standards in clinical research: Gaps, overlaps, challenges and future directions.

**Relevance to Project**:
- Analyzes persistent tensions between local solutions and global interoperability.
- Foundational for understanding technical barriers to standardization.

**Citation**:
```bibtex
@article{richesson2007,
  author = {Richesson, R. L., \& Krischer, J. P},
  title = {{Data standards in clinical research: Gaps, overlaps, challenges and future directions}},
  year = {2007},
  journal = {Journal of the American Medical Informatics Association},
  doi = {10.1197/jamia.M2470},
  url = {https://academic.oup.com/jamia/article/14/6/687/750453},
  file = {../library/docs/2007_Richesson_JAMIA_Data-Standards-Clinical-Research.pdf},
  note = {Original citation: [A26]},
}
```

### 2010_Mantas_Methods-Informatics-Medicine_IMIA-Health-Informatics-Education.pdf
**Source**: Methods of Information in Medicine
**Date**: 2010
**Pages**: [Check PDF]
**Size**: [Check PDF]

**Description**: Recommendations of the International Medical Informatics Association (IMIA) on education in biomedical and health informatics.

**Relevance to Project**:
- Standard for health informatics education.
- Context for the "Workforce Turnover" pillar.

**Citation**:
```bibtex
@article{mantas2010,
  author = {Mantas, J., Ammenwerth, E., Demiris, G., Hasman, A., Haux, R., Hersh, W., Hovenga, E., Lun, K. C., Marin, H., Martin-Sanchez, F., \& Wright, G},
  title = {{Recommendations of the International Medical Informatics Association (IMIA) on education in biomedical and health informatics: First revision}},
  year = {2010},
  journal = {Methods of Information in Medicine},
  doi = {10.3414/ME5119},
  url = {https://pubmed.ncbi.nlm.nih.gov/20054502/},
  file = {../library/docs/2010_Mantas_Methods-Informatics-Medicine_IMIA-Health-Informatics-Education.pdf},
  note = {Original citation: [A12]},
}
```

### 2013_Ledikwe_HR-For-Health_Health-Information-Workforce.pdf
**Source**: Human Resources for Health
**Date**: 2013
**Pages**: [Check PDF]
**Size**: [Check PDF]

**Description**: Establishing a health information workforce: Innovation for low- and middle-income countries.

**Relevance to Project**:
- Workforce development and training duration analysis.
- Supports the "Workforce Turnover" pillar.

**Citation**:
```bibtex
@article{ledikwe2013,
  author = {Ledikwe, J. H., Reason, L. L., Burnett, S. M., Busang, L., Bodika, S., Lebelonyane, R., Ludick, S., Matshediso, E., Mawandia, S., Mmelesi, M., Sento, B., \& Semo, B.-W},
  title = {{Establishing a health information workforce: Innovation for low- and middle-income countries}},
  year = {2013},
  journal = {Human Resources for Health},
  doi = {10.1186/1478-4491-11-35},
  url = {https://human-resources-health.biomedcentral.com/articles/10.1186/1478-4491-11-35},
  file = {../library/docs/2013_Ledikwe_HR-For-Health_Health-Information-Workforce.pdf},
  note = {Original citation: [A11]},
}
```

### 2016_Bardsley_Health-Foundation_Understanding-Analytical-Capability.pdf
**Source**: The Health Foundation
**Date**: 2016
**Pages**: [Check PDF]
**Size**: [Check PDF]

**Description**: Understanding analytical capability in health care: Do we have more data than insight?

**Relevance to Project**:
- Foundational report on the gap between data availability and analytical capability.
- Supports the "Analytics Maturity" pillar.

**Citation**:
```bibtex
@misc{bardsley2016,
  author = {Bardsley, M},
  title = {{Understanding analytical capability in health care: Do we have more data than insight? The Health Foundation}},
  year = {2016},
  url = {https://www.health.org.uk/publications/understanding-analytical-capability-in-health-care},
  file = {../library/docs/2016_Bardsley_Health-Foundation_Understanding-Analytical-Capability.pdf},
  note = {Original citation: [A15]},
}
```

### 2019_Gal_NYULawRev_Data-Standardization.pdf
**Source**: NYU Law Review
**Date**: October 2019
**Pages**: 34 (737--770)
**Size**: [Not specified]

**Description**: Emphasizes the importance of data standardization for improving data portability and interoperability in the global economy.

**Relevance to Project**:
- Theoretical grounding for data standardization benefits.
- Analysis of market-led vs government-led standardization.

**Citation**:
```bibtex
@article{gal2019,
  author = {Gal, Michal S. and Rubinfeld, Daniel L.},
  title = {{Data Standardization}},
  year = {2019},
  journal = {NYU Law Review},
  volume = {94},
  number = {4},
  pages = {737--770},
  url = {https://www.nyulawreview.org/issues/volume-94-number-4/data-standardization/},
  file = {../library/docs/2019_Gal_NYULawRev_Data-Standardization.pdf},
  note = {Original citation: [A109]},
}
```

### 2020_Wang_WebConf_Text-to-SQL-EMR.pdf
**Source**: The Web Conference (WWW)
**Date**: April 2020
**Pages**: 2216--2226
**Size**: [Check PDF]

**Description**: Text-to-SQL generation for question answering on electronic medical records.

**Relevance to Project**:
- Benchmark for NL2SQL on EMR data (MIMIC-III).
- Highlights the need for semantic mapping beyond string matching.

**Citation**:
```bibtex
@inproceedings{wang2020,
  author = {Wang, P., Shi, T., \& Reddy, C. K},
  title = {{Text-to-SQL generation for question answering on electronic medical records}},
  year = {2020},
  booktitle = {Proceedings of The Web Conference 2020},
  doi = {10.1145/3366423.3380120},
  url = {https://arxiv.org/abs/1908.01839},
  file = {../library/docs/2020_Wang_WebConf_Text-to-SQL-EMR.pdf},
  note = {Original citation: [A5]},
}
```

### 2020_Health-Catalyst_Healthcare-Analytics-Adoption.pdf
**Source**: Health Catalyst
**Date**: 2020
**Pages**: [Check PDF]
**Size**: [Check PDF]

**Description**: The healthcare analytics adoption model: A roadmap to analytic maturity.

**Relevance to Project**:
- Alternative maturity model (8 levels) complementary to HIMSS AMAM.
- Provides strategic roadmap for data-driven healthcare.

**Citation**:
```bibtex
@misc{health2020,
  author = {Health Catalyst},
  title = {{The healthcare analytics adoption model: A roadmap to analytic maturity}},
  year = {2020},
  url = {https://www.healthcatalyst.com/learn/insights/healthcare-analytics-adoption-model-roadmap-analytic-maturity},
  file = {../library/docs/2020_Health-Catalyst_Healthcare-Analytics-Adoption.pdf},
  note = {Original citation: [I3]},
}
```

### 2020_Pesqueira_J-Med-Syst_Big-Data-Skills-Healthcare.pdf
**Source**: Journal of Medical Systems
**Date**: 2020
**Pages**: [Check PDF]
**Size**: [Check PDF]

**Description**: Big data skills sustainable development in healthcare and pharmaceuticals.

**Relevance to Project**:
- Addresses the skills gap in healthcare analytics.
- Supports the "Workforce Turnover" and "Analytics Maturity" pillars.

**Citation**:
```bibtex
@article{pesqueira2020,
  author = {Pesqueira, A., Sousa, M. J., \& Rocha, Á},
  title = {{Big data skills sustainable development in healthcare and pharmaceuticals}},
  year = {2020},
  journal = {Journal of Medical Systems},
  doi = {10.1007/s10916-020-01665-9},
  url = {https://link.springer.com/article/10.1007/s10916-020-01665-9},
  file = {../library/docs/2020_Pesqueira_J-Med-Syst_Big-Data-Skills-Healthcare.pdf},
  note = {Original citation: [A16]},
}
```

### 2022_Sezgin_JMIR-Med-Inform_Operationalizing-AI-in-US-Healthcare.pdf
**Source**: JMIR Medical Informatics
**Date**: 2022
**Pages**: [Check PDF]
**Size**: [Check PDF]

**Description**: Operationalizing and implementing pretrained, large artificial intelligence linguistic models in the US health care system: Outlook of generative pretrained transformer 3 (GPT-3) as a service model.

**Relevance to Project**:
- Discusses the implementation of LLMs (GPT-3) in healthcare.
- Relevant to the "Technical Barriers" pillar and NL2SQL context.

**Citation**:
```bibtex
@article{sezgin2022,
  author = {Sezgin, E., Sirrianni, J., \& Linwood, S. L},
  title = {{Operationalizing and implementing pretrained, large artificial intelligence linguistic models in the {US} health care system: Outlook of generative pretrained transformer 3 (GPT-3) as a service model}},
  year = {2022},
  journal = {{JMIR} Medical Informatics},
  doi = {10.2196/32875},
  url = {https://medinform.jmir.org/2022/2/e32875},
  file = {../library/docs/2022_Sezgin_JMIR-Med-Inform_Operationalizing-AI-in-US-Healthcare.pdf},
  note = {Original citation: [A19]},
}
```

### 2023_Jiao_IEEE-Access_Economic-Value-AI-Healthcare.pdf
**Source**: IEEE Access
**Date**: 2023
**Pages**: [Check PDF]
**Size**: [Check PDF]

**Description**: The economic value and clinical impact of artificial intelligence in healthcare: A scoping literature review.

**Relevance to Project**:
- Reviews the economic value of AI in healthcare.
- Supports the "Workforce Turnover" and "Technical Barriers" pillars (ROI of AI).

**Citation**:
```bibtex
@article{jiao2023,
  author = {Jiao, W., Zhang, X., \& D'Souza, F},
  title = {{The economic value and clinical impact of artificial intelligence in healthcare: A scoping literature review}},
  year = {2023},
  journal = {{IEEE} Access},
  doi = {10.1109/ACCESS.2023.3327905},
  url = {https://ieeexplore.ieee.org/document/10297311},
  file = {../library/docs/2023_Jiao_IEEE-Access_Economic-Value-AI-Healthcare.pdf},
  note = {Original citation: [A20]},
}
```

### 2024_WittKieffer_CIO-Insights-Healthcare-IT-Leadership.pdf
**Source**: WittKieffer
**Date**: October 2024
**Pages**: [Check PDF]
**Size**: [Check PDF]

**Description**: Insights into the state of healthcare IT leadership, discussing trends, challenges, and the evolving role of the CIO.

**Relevance to Project**:
- Context on healthcare IT leadership challenges (turnover, strategic alignment).
- Supports the "Workforce Turnover" pillar of the framework.

**Citation**:
```bibtex
@techreport{wittkieffer2024,
  title = {{CIO Insights: The State of Healthcare IT Leadership}},
  author = {{WittKieffer}},
  year = {2024},
  month = {10},
  institution = {WittKieffer},
  url = {https://api.wittkieffer.com/wp-content/uploads/2012/10/cio-insights-the-state-of-healthcare-it-leadership-wittkieffer-october-2024.pdf},
  file = {../library/docs/2024_WittKieffer_CIO-Insights-Healthcare-IT-Leadership.pdf},
  note = {Original citation: [I2]},
}
```

### 2024_Forrester_ROI-Microsoft-Power-Apps.pdf
**Source**: Forrester Research
**Date**: 2024
**Pages**: [Check PDF]
**Size**: [Check PDF]

**Description**: The total economic impact of Microsoft Power Apps. Forrester Consulting.

**Relevance to Project**:
- Quantitative ROI metrics for low-code platforms.
- Supports the "Technical Barriers" pillar (alternative to traditional development).

**Citation**:
```bibtex
@misc{forrester2024,
  author = {Forrester Research},
  title = {{The total economic impact of Microsoft Power Apps. Forrester Consulting}},
  year = {2024},
  url = {https://tei.forrester.com/go/microsoft/powerappstei/?lang=en-us},
  file = {../library/docs/2024_Forrester_ROI-Microsoft-Power-Apps.pdf},
  note = {Original citation: [I5]},
}
```

### 2024_NSI_National-Health-Care-Retention-Report.pdf
**Source**: NSI Nursing Solutions
**Date**: 2024
**Pages**: [Check PDF]
**Size**: [Check PDF]

**Description**: 2025 National Health Care Retention & RN Staffing Report. Provides baseline data on retention and staffing.

**Relevance to Project**:
- Essential data for the "Workforce Turnover" pillar.
- Provides quantitative baselines for turnover rates.

**Citation**:
```bibtex
@techreport{nsi2025,
  author = {{NSI Nursing Solutions}},
  title = {{2025 National Health Care Retention \& RN Staffing Report}},
  year = {2024},
  institution = {NSI Nursing Solutions},
  url = {https://www.nsinursingsolutions.com/documents/library/nsi_national_health_care_retention_report.pdf},
  file = {../library/docs/2024_NSI_National-Health-Care-Retention-Report.pdf},
  note = {Retention baseline data}
}
```

### 2025_Dadi_JCSTS_Natural-Language-Interfaces-Database-Management.pdf
**Source**: Journal of Computer Science and Technology Studies (JCSTS)
**Date**: May 2025
**Pages**: 7 (927--933)
**Size**: [Not specified]

**Description**: Explores the transformative role of Natural Language Interfaces (NLIs) in database management, tracing their evolution and organizational impact.

**Relevance to Project**:
- Quantitative evidence for productivity gains from NL2SQL.
- Demonstrates organizational impact of conversational AI interfaces.

**Citation**:
```bibtex
@article{dadi2025,
  author = {Dadi, Chaitanya Bharat and Hoque, Md Refadul and Ali, Md Musa and Ferdausi, Shaharia and Fatema, Kanis and Hasan, Md Rakibul},
  title = {{Natural Language Interfaces for Database Management: Bridging the Gap Between Users and Data through Conversational {AI}}},
  year = {2025},
  journal = {Journal of Computer Science and Technology Studies},
  volume = {7},
  number = {3},
  pages = {927--933},
  doi = {10.32996/jcsts.2025.7.3.103},
  url = {https://al-kindipublisher.com/index.php/jcsts/article/view/9694},
  file = {../library/docs/2025_Dadi_JCSTS_Natural-Language-Interfaces-Database-Management.pdf},
  note = {Original citation: [A36]},
}
```

### 2025_Hong_JPART_Employee-Turnover-Organizational-Memory.pdf
**Source**: Journal of Public Administration Research and Theory
**Date**: 2025
**Pages**: 18 (434--451)
**Size**: [Not specified]

**Description**: Investigates how organizational memory (task standardization and centralization) buffers the disruptive effects of turnover.

**Relevance to Project**:
- Connects task standardization to knowledge retention.
- Supports the "Workforce Turnover" pillar.

**Citation**:
```bibtex
@article{hong2025,
  author = {Hong, J. H.},
  title = {When Does Employee Turnover Matter? Organizational Memory in Federal IT},
  journal = {Journal of Public Administration Research and Theory},
  year = {2025},
  url = {https://academic.oup.com/jpart/advance-article-abstract/doi/10.1093/jopart/muaf019/8162522},
  file = {../library/docs/2025_Hong_JPART_Employee-Turnover-Organizational-Memory.pdf},
  note = {Original citation: [New]}
}
```

### 20250905_Anthropic_Code-Modernization-Playbook.pdf
**Source**: Anthropic
**Date**: September 5, 2025
**Pages**: 8
**Size**: 281KB

**Description**: Anthropic's guide to code modernization best practices, including Claude Code usage patterns and AI-assisted development workflows.

**Relevance to Project**:
- Best practices for AI-assisted research and documentation
- Claude Code integration patterns used in this repository
- Modern development workflows referenced in GEMINI.md

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
- [`GEMINI.md`](../../GEMINI.md) - Development workflow guidance
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
ls -lh ../library/docs/

# Search by source
ls ../library/docs/ | grep -i "anthropic"

# Search by date
ls ../library/docs/ | grep "202509"

# Full-text search (if PDFs are OCR'd)
grep -r "machine learning" ../library/docs/
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
