# Requirements: Academic Literature Review Tool

**Date:** 2025-12-09
**Author:** stharrold
**Status:** Draft

## Business Context

### Problem Statement

The YuiQuery research paper makes claims about healthcare analytics maturity, workforce turnover, and technical barriers that must be supported by rigorous literature review following academic standards. Currently, the repository has a basic lit_review package but lacks comprehensive systematic review capabilities for:
- Multi-database search across academic sources (Crossref, PubMed, ArXiv, Semantic Scholar)
- Systematic deduplication and quality assessment following PRISMA guidelines
- Automated thematic analysis and synthesis generation
- Multiple export formats for academic publication

This tool will enable systematic, reproducible literature reviews that meet publication standards for healthcare research.

### Success Criteria

- [ ] Successfully search 1000+ papers per minute across all four databases (Crossref, PubMed, ArXiv, Semantic Scholar)
- [ ] Complete full literature review workflow (search → assess → analyze → synthesize → export) in <30 minutes for typical review (500 papers)
- [ ] Generate PRISMA-compliant documentation automatically (flow diagram, checklist, search documentation)
- [ ] Achieve >80% test coverage across all modules
- [ ] Export reviews in all required formats (BibTeX, DOCX, LaTeX, HTML, JSON)

### Stakeholders

- **Primary:** Research team conducting systematic literature reviews for healthcare papers
- **Secondary:** Academic reviewers evaluating systematic review methodology; Journal editors assessing PRISMA compliance; Future researchers replicating or extending reviews

## User Stories

### US-1: Multi-Database Search

**As a** researcher
**I want** to search multiple academic databases simultaneously
**So that** I can find comprehensive literature on a topic without manually querying each database

**Acceptance Criteria:**
- [ ] Search Crossref, PubMed, ArXiv, and Semantic Scholar in parallel
- [ ] Automatically deduplicate results by DOI (when available)
- [ ] Handle API rate limits gracefully with exponential backoff
- [ ] Return results in <2 minutes for typical queries (up to 1000 papers)
- [ ] Continue with partial results if one database fails or times out

### US-2: Systematic Quality Assessment

**As a** researcher
**I want** to assess paper quality systematically
**So that** I can maintain rigorous inclusion/exclusion criteria for my review

**Acceptance Criteria:**
- [ ] Score papers on 0-10 quality scale with justification
- [ ] Record binary inclusion/exclusion decisions
- [ ] Track assessment notes and rationale for decisions
- [ ] Support batch assessment from CSV for high-volume screening
- [ ] Generate quality assessment summary statistics

### US-3: Thematic Analysis

**As a** researcher
**I want** to extract themes from included papers automatically
**So that** I can identify research patterns and knowledge gaps

**Acceptance Criteria:**
- [ ] Use TF-IDF for keyword extraction from titles and abstracts
- [ ] Build co-occurrence matrices to identify related concepts
- [ ] Perform hierarchical clustering to group themes
- [ ] Generate theme hierarchy with main themes and subthemes
- [ ] Complete analysis in <30 seconds for 500 papers

### US-4: Multi-Format Export

**As a** researcher
**I want** to export my review in multiple formats
**So that** I can submit to different journals with varying requirements

**Acceptance Criteria:**
- [ ] Export to BibTeX for reference managers (Zotero, Mendeley)
- [ ] Generate DOCX with APA7 formatting for Word-based journals
- [ ] Create LaTeX for Nature/IEEE/generic journal templates
- [ ] Produce HTML for web publication and interactive exploration
- [ ] Export complete JSON for data archival and replication

### US-5: PRISMA Compliance

**As a** researcher
**I want** PRISMA-compliant reporting automatically generated
**So that** my review meets systematic review publication standards

**Acceptance Criteria:**
- [ ] Generate PRISMA flow diagram showing paper flow (identification, screening, eligibility, inclusion)
- [ ] Complete PRISMA checklist automatically with evidence references
- [ ] Track all inclusion/exclusion decisions with justifications
- [ ] Document search strategies for each database with timestamps
- [ ] Export PRISMA documentation in multiple formats

## Functional Requirements

### FR-001: Multi-Database Search Coordination
**Priority:** P0
**Description:** Coordinate parallel searches across Crossref, PubMed, ArXiv, and Semantic Scholar with thread pool execution, handling rate limits, timeouts, and partial failures gracefully.

**Acceptance Criteria:**
- [ ] Execute searches in parallel using thread pool (max 4 workers)
- [ ] Apply exponential backoff on rate limit errors (max 3 retries)
- [ ] Timeout individual database searches at 30 seconds
- [ ] Return partial results if some databases fail
- [ ] Log all API errors with database source and error details

### FR-002: Automatic Deduplication
**Priority:** P0
**Description:** Automatically deduplicate papers by DOI (primary) and title similarity (secondary) to prevent duplicate entries in review dataset.

**Acceptance Criteria:**
- [ ] Deduplicate by exact DOI match (case-insensitive)
- [ ] Use Levenshtein distance for title similarity (threshold: 85%)
- [ ] Preserve metadata from first encountered instance
- [ ] Log all deduplications with source database information
- [ ] Generate deduplication statistics report

### FR-003: Paper Quality Assessment Workflow
**Priority:** P0
**Description:** Provide systematic workflow for assessing paper quality with scoring, inclusion/exclusion decisions, and batch processing capabilities.

**Acceptance Criteria:**
- [ ] Score papers on 0-10 scale with required justification
- [ ] Record binary include/exclude decision
- [ ] Support freeform assessment notes (optional)
- [ ] Batch assess from CSV with columns: DOI, score, include, notes
- [ ] Validate all assessments before saving

### FR-004: Thematic Analysis Engine
**Priority:** P1
**Description:** Extract themes using TF-IDF keyword extraction, co-occurrence analysis, and hierarchical clustering to identify research patterns.

**Acceptance Criteria:**
- [ ] Extract top 50 keywords using TF-IDF from titles and abstracts
- [ ] Build keyword co-occurrence matrix (threshold: 3+ co-occurrences)
- [ ] Perform hierarchical clustering (Ward linkage) to group related keywords
- [ ] Generate 3-5 main themes with subthemes
- [ ] Complete analysis in <30 seconds for 500 papers

### FR-005: AI-Powered Synthesis Generation
**Priority:** P1
**Description:** Generate narrative synthesis using AI to summarize findings, identify patterns, and suggest research gaps.

**Acceptance Criteria:**
- [ ] Generate 500-1000 word synthesis organized by themes
- [ ] Include introduction with research question
- [ ] Provide evidence summary for each theme
- [ ] Identify research gaps and future directions
- [ ] Include properly formatted citations

### FR-006: Multi-Format Export
**Priority:** P0
**Description:** Export reviews in BibTeX, DOCX (APA7), LaTeX (Nature/IEEE/generic), HTML, and JSON formats.

**Acceptance Criteria:**
- [ ] BibTeX: Standard format compatible with all reference managers
- [ ] DOCX: APA7 formatting with sections, citations, references
- [ ] LaTeX: Three templates (Nature, IEEE, generic) with proper bibliography
- [ ] HTML: Interactive web version with search and filtering
- [ ] JSON: Complete review data for archival and replication

### FR-007: PRISMA Flow Diagram Generation
**Priority:** P1
**Description:** Generate PRISMA flow diagram showing paper flow through identification, screening, eligibility, and inclusion stages.

**Acceptance Criteria:**
- [ ] Track papers at each PRISMA stage (identification, screening, eligibility, included)
- [ ] Record reasons for exclusion at each stage
- [ ] Generate flow diagram as PNG with standard PRISMA layout
- [ ] Include counts for each stage and exclusion reasons
- [ ] Export flow diagram data as JSON for custom visualization

### FR-008: Citation Network Analysis
**Priority:** P2
**Description:** Analyze citation relationships between papers to identify influential works and citation clusters.

**Acceptance Criteria:**
- [ ] Build citation graph from paper references
- [ ] Calculate citation counts and centrality metrics
- [ ] Identify highly-cited papers and citation clusters
- [ ] Visualize citation network as interactive graph
- [ ] Export network data for further analysis

## Non-Functional Requirements

### Performance

**NFR-001: Search Performance**
- Target: 1000 papers per minute across all databases
- Measurement: Time from search invocation to results returned
- Monitoring: Log search duration and paper count for each query

**NFR-002: Analysis Performance**
- Target: Theme analysis completes in <30 seconds for 500 papers
- Measurement: Time from analysis invocation to theme hierarchy generated
- Monitoring: Log analysis duration and paper count

**NFR-003: Memory Efficiency**
- Target: Memory usage <500MB for 10,000 papers
- Measurement: Peak memory usage during operations
- Monitoring: Memory profiling in integration tests

### Reliability

**NFR-004: Network Error Handling**
- Strategy: Automatic retry with exponential backoff (initial: 1s, max: 60s)
- Max retries: 3 attempts per request
- Fallback: Return partial results on timeout
- Logging: All network errors with context

**NFR-005: Data Integrity**
- Strategy: Atomic file writes with temporary file + rename
- Backups: Automatic backup before each write
- Validation: Pydantic validation on all data models
- Recovery: Load from backup on corruption detection

### Security

**NFR-006: API Key Management**
- Storage: Environment variables only (CROSSREF_API_KEY, PUBMED_API_KEY, etc.)
- Logging: Never log API keys or sensitive credentials
- Validation: Check for API key presence at startup
- Documentation: Clear setup instructions for required keys

**NFR-007: Input Validation**
- Strategy: Validate all user inputs using Pydantic models
- Sanitization: Escape special characters in search queries
- Error messages: Clear validation errors without exposing internals
- Rate limiting: Respect API rate limits for all databases

### Usability

**NFR-008: Error Messages**
- Format: Clear, actionable error messages without stack traces in production
- Context: Include relevant context (e.g., which database failed)
- Suggestions: Provide fix suggestions where applicable
- Logging: Full stack traces in logs for debugging

**NFR-009: Progress Indicators**
- Search: Show progress for each database search
- Analysis: Display progress for long-running analyses
- Export: Show export progress for large datasets
- Format: Use Click progress bars for CLI operations

### Maintainability

**NFR-010: Test Coverage**
- Target: >80% code coverage across all modules
- Unit tests: All business logic in domain and application layers
- Integration tests: All external API calls and file I/O
- Performance tests: All critical operations with timing assertions

**NFR-011: SOLID Principles**
- Single Responsibility: Each class has one reason to change
- Open/Closed: Extensible without modifying existing code
- Liskov Substitution: Subtypes must be substitutable for base types
- Interface Segregation: No client forced to depend on unused methods
- Dependency Inversion: Depend on abstractions, not concretions

## Constraints

### Technology

- **Language:** Python 3.8+ (for broad compatibility)
- **Package Manager:** uv (for fast, reproducible dependency management)
- **Framework:** Click (for CLI interface with progress indicators)
- **Validation:** Pydantic (for data validation and serialization)
- **Testing:** pytest with pytest-cov for coverage
- **Database:** JSON files with atomic writes (simple, version-control friendly)
- **Container:** Docker (for reproducible development environment)

### Budget

- **API Costs:** Free tiers for all databases (Crossref, PubMed, ArXiv, Semantic Scholar)
- **Compute:** Local development sufficient, no cloud infrastructure required
- **Storage:** Minimal (typical review <100MB)

### Timeline

- **Phase 1 (Domain):** 1 week - Core entities and value objects with TDD
- **Phase 2 (Application):** 2 weeks - Use cases and ports
- **Phase 3 (Infrastructure):** 2 weeks - Database adapters and persistence
- **Phase 4 (Interface):** 1 week - CLI commands
- **Phase 5 (Testing):** 1 week - Integration tests and performance tests
- **Total:** 7 weeks

### Dependencies

**External APIs:**
- Crossref REST API (https://api.crossref.org)
- PubMed E-utilities API (https://eutils.ncbi.nlm.nih.gov/entrez/eutils/)
- ArXiv API (http://export.arxiv.org/api/query)
- Semantic Scholar API (https://api.semanticscholar.org)

**Third-Party Libraries:**
- click - CLI framework
- pydantic - Data validation
- httpx - Async HTTP client
- scikit-learn - TF-IDF and clustering
- biopython - PubMed parsing
- python-docx - Word document generation
- jinja2 - LaTeX template rendering

## Out of Scope

**Explicitly NOT included in this feature:**

- Real-time collaborative editing of reviews
- Web-based user interface (CLI only for this version)
- Automated full-text PDF download and extraction
- Machine learning for paper screening automation
- Integration with reference managers (beyond BibTeX export)
- Publishing/hosting of completed reviews
- Version control for review iterations (use Git for this)
- Custom database source additions (fixed to 4 databases)
- Forward citation tracking (only backward citations)
- Automated email alerts for new papers

## Risks and Mitigation

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| API rate limits cause slow searches | High | Medium | Implement exponential backoff, cache results, parallelize across databases |
| PubMed API downtime | Medium | High | Return partial results, log errors clearly, provide retry mechanism |
| Missing DOIs prevent deduplication | High | Medium | Implement title similarity fallback using Levenshtein distance |
| Large reviews (10k+ papers) cause memory issues | Low | High | Implement streaming for exports, use generators where possible |
| Theme analysis produces poor quality themes | Medium | Medium | Provide manual theme override, tune TF-IDF parameters, use AI fallback |
| Export formats don't match journal requirements | Medium | High | Provide configurable templates, document customization process |
| Test coverage slips below 80% | Medium | High | Pre-commit hooks for coverage checks, block PRs below threshold |
| Clean Architecture increases initial complexity | Low | Low | Comprehensive documentation, clear examples, gradual team onboarding |

## Data Requirements

### Data Entities

**Primary Entities:**
1. **Paper:** Core publication metadata (DOI, title, authors, abstract, year, journal, keywords)
2. **Review:** Container for systematic review (review_id, title, research_question, papers, stage, metadata)
3. **Author:** Person metadata (last_name, first_name, initials, orcid)
4. **Assessment:** Quality assessment record (paper_doi, score, include, notes, timestamp)
5. **Theme:** Thematic analysis result (theme_name, keywords, subthemes, paper_count)
6. **Citation:** Citation relationship (citing_doi, cited_doi, citation_context)

**Value Objects:**
1. **DOI:** Validated DOI string with regex pattern
2. **WorkflowStage:** Enum (INITIALIZED, SEARCH, SCREENING, ELIGIBILITY, INCLUDED, ANALYSIS, SYNTHESIS, EXPORTED)

### Data Volume

- **Typical review:** 100-1000 papers, 5-50 MB JSON
- **Large review:** 1000-10000 papers, 50-500 MB JSON
- **Growth rate:** Linear with paper count
- **Peak memory:** 2x file size during operations

### Data Retention

- **Active reviews:** Keep indefinitely in `review_data/reviews/`
- **Deleted reviews:** Soft delete to `review_data/.deleted/` for 30 days
- **Backups:** Keep last 5 backups in `review_data/.backups/`
- **Exports:** User manages exported files (not tracked by tool)

## Assumptions

1. **Network Connectivity:** Users have reliable internet access for API calls
2. **API Availability:** All four databases (Crossref, PubMed, ArXiv, Semantic Scholar) are accessible and operational
3. **Search Queries:** Users provide well-formed search queries appropriate for academic databases
4. **Input Data:** Paper metadata from APIs is generally complete and accurate
5. **Local Storage:** Users have sufficient disk space for review data (typically <1GB)
6. **Python Environment:** Users can set up Python 3.8+ environment with uv
7. **API Keys:** Users can obtain free API keys where required (Crossref, Semantic Scholar)
8. **Text Encoding:** All paper metadata is UTF-8 encoded
9. **DOI Availability:** Most academic papers have DOIs for deduplication
10. **English Language:** Papers are primarily in English for thematic analysis

## Questions and Open Issues

- [ ] Should we support custom database sources beyond the initial four?
- [ ] Do we need support for importing existing review data from other tools (e.g., Zotero, Mendeley)?
- [ ] Should theme analysis support languages other than English?
- [ ] Is offline mode necessary for scenarios without internet access?
- [ ] Should we implement audit logging for compliance requirements?
- [ ] Do we need role-based access control for collaborative reviews?
- [ ] Should we integrate with Zenodo for automatic DOI assignment to reviews?
- [ ] Is there value in exporting to specific journal templates beyond Nature/IEEE?

## Approval

- [ ] Product Owner review (Research team lead)
- [ ] Technical Lead review (Python architecture expert)
- [ ] Security review (API key management, input validation)
- [ ] Ready for architecture phase
