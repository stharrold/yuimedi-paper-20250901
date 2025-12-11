# Academic Literature Review Tool - Planning Documents

## Overview

This directory contains comprehensive planning documents for the Academic Literature Review Tool feature - a test-driven systematic literature review workflow system for rigorous claim verification in healthcare research.

**Status:** Planning Complete, Ready for Implementation
**GitHub Issue:** [#258](https://github.com/stharrold/yuimedi-paper-20250901/issues/258)
**Created:** 2025-12-09
**Author:** stharrold

## Purpose

Enable systematic, reproducible literature reviews following PRISMA guidelines to support evidence-based claims in the YuiQuery research paper. The tool will provide multi-database search, automated deduplication, quality assessment, thematic analysis, and multiple export formats.

## Planning Documents

### [requirements.md](requirements.md)
Business requirements, functional and non-functional requirements, user stories, and acceptance criteria.

**Key Requirements:**
- FR-001: Multi-database search with parallel execution (Crossref, PubMed, ArXiv, Semantic Scholar)
- FR-002: Automatic deduplication (>99% accuracy)
- FR-003: Paper quality assessment and screening workflow
- FR-004: Thematic analysis using TF-IDF and clustering
- FR-005: AI-powered synthesis generation
- FR-006: Multiple export formats (BibTeX, DOCX, LaTeX, HTML, JSON)
- FR-007: PRISMA flow diagram generation
- FR-008: Citation network analysis

**Performance Targets:**
- 1000 papers/minute search throughput
- <30 seconds theme analysis for 500 papers
- <500MB memory for 10,000 papers

### [architecture.md](architecture.md)
Technical architecture, technology stack, design decisions, and implementation approach.

**Architecture:** Clean Architecture (4 layers)
1. **Domain Layer:** Entities (Paper, Review, Citation), Value Objects (DOI, Author, Keywords)
2. **Application Layer:** Use Cases (Search, Analyze, Synthesize, Export), Ports (interfaces)
3. **Infrastructure Layer:** Adapters (Crossref, PubMed), Persistence (JSON), AI (Claude)
4. **Interface Layer:** CLI (Click-based commands)

**Technology Stack:**
- Python 3.8+, Click, Pydantic, scikit-learn, biopython, python-docx
- Testing: pytest (>80% coverage), ruff (linting), mypy (type checking)
- Containers: Podman + podman-compose
- CI/CD: GitHub Actions, Docker Hub, Zenodo

### [epics.md](epics.md)
Implementation plan broken into 7 epics with dependencies, timelines, and acceptance criteria.

**Epics:**
1. **E-001:** Project Setup & Configuration (1-2 days)
2. **E-002:** Domain Layer (TDD) (3-4 days)
3. **E-003:** Application Layer (4-5 days)
4. **E-004:** Infrastructure Layer (4-5 days)
5. **E-005:** CLI Interface (2-3 days)
6. **E-006:** Testing & Quality Gates (2-3 days)
7. **E-007:** CI/CD & Deployment (1-2 days)

**Timeline:** 3-5 weeks (17-24 days estimated effort)

## Key Features

- **Multi-Database Search:** Parallel searches across 4+ academic databases
- **Smart Deduplication:** DOI-based + title similarity matching (>99% accuracy)
- **Systematic Assessment:** Quality scoring (0-10), inclusion/exclusion tracking
- **Thematic Analysis:** TF-IDF keyword extraction + hierarchical clustering
- **AI-Powered Synthesis:** Claude API integration with fallback to keyword-based
- **PRISMA Compliance:** Flow diagrams, checklists, methodology documentation
- **Multiple Exports:** BibTeX, DOCX (APA7), LaTeX (Nature/IEEE/generic), HTML, JSON
- **Citation Networks:** Forward/backward citation analysis

## Design Principles

1. **Test-Driven Development (TDD):** Write tests before implementation
2. **Clean Architecture:** Strict layer separation, no cross-layer dependencies
3. **SOLID Principles:** Applied throughout codebase
4. **High Test Coverage:** >80% requirement for academic tool trustworthiness
5. **Academic Rigor:** PRISMA guidelines, reproducible workflows
6. **Performance:** 1000 papers/min searches, <30s analysis for 500 papers

## Success Criteria

- [ ] Complete full literature review workflow functional
- [ ] Search 4+ databases with >99% deduplication accuracy
- [ ] Generate PRISMA-compliant reports
- [ ] Export to 5+ formats successfully
- [ ] Achieve >80% test coverage
- [ ] Performance targets met
- [ ] Tool validates actual claims from YuiQuery paper

## Integration with Repository

**Extends:** `lit_review/` package with new systematic review capabilities
**Respects existing standards:**
- Dependency strategy (stdlib for scripts, external for lit_review/)
- Validation system (`./validate_documentation.sh`)
- Branch strategy (feature/* → contrib/* → develop → main)
- Testing requirements (>80% coverage)
- SOLID principles and Clean Architecture

## Next Steps

1. **Create feature worktree:**
   ```bash
   python .claude/skills/git-workflow-manager/scripts/create_worktree.py feature academic-literature-review-tool contrib/stharrold --no-todo
   ```

2. **Run /2_plan** in worktree to design implementation approach

3. **Run /3_tasks** to generate detailed task list

4. **Begin implementation** with E-001 (Project Setup)

## Related Documents

- **Implementation Guide:** [.tmp/20251209_Implementation-Academic-Literature-Review-Tool.md](../../.tmp/20251209_Implementation-Academic-Literature-Review-Tool.md)
- **Workflow Specifications:** [.tmp/academic-literature-review-workflow/](../../.tmp/academic-literature-review-workflow/)
- **GitHub Issue:** [#258](https://github.com/stharrold/yuimedi-paper-20250901/issues/258)

## Workflow Context

**Workflow Steps:**
1. ✅ /1_specify - Create planning documents (COMPLETE)
2. ⏭️ /2_plan - Design implementation approach in worktree
3. ⏭️ /3_tasks - Generate task list
4. ⏭️ /4_implement - Execute implementation
5. ⏭️ /5_integrate - Integrate to develop
6. ⏭️ /6_release - Release to main
7. ⏭️ /7_backmerge - Sync back to develop and contrib

## Questions?

See [CLAUDE.md](CLAUDE.md) for technical context and integration details.

---

**Note:** This is a production tool for research, not just documentation. Focus on rigorous academic standards, comprehensive testing, and Clean Architecture principles.
