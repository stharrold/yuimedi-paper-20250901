# Academic Literature Review Tool - Workflow Guide

Complete workflow examples for conducting systematic literature reviews using the Academic Literature Review Tool.

## Table of Contents

1. [Overview](#overview)
2. [Complete Workflow Example](#complete-workflow-example)
3. [Stage-by-Stage Guide](#stage-by-stage-guide)
4. [Advanced Usage](#advanced-usage)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## Overview

The tool follows PRISMA 2020 guidelines with six workflow stages:

```
PLANNING → SEARCH → SCREENING → ANALYSIS → SYNTHESIS → COMPLETE
```

Each stage has specific tasks and must be completed before advancing.

## Complete Workflow Example

This example demonstrates a complete literature review from start to finish.

### Research Question

"What is the effectiveness of machine learning models for diagnosing diabetic retinopathy compared to expert ophthalmologists?"

### Step 1: Initialize Review (PLANNING stage)

```bash
uv run academic-review init "ML Diabetic Retinopathy" \
  --question "What is the effectiveness of ML models for diagnosing diabetic retinopathy vs expert ophthalmologists?" \
  --include "Peer-reviewed articles" \
  --include "English language" \
  --include "Published 2018-2024" \
  --include "Studies with validation datasets" \
  --exclude "Conference abstracts" \
  --exclude "Studies without ground truth" \
  --exclude "Non-ophthalmic conditions"
```

**Output:**
```
Created review: ML Diabetic Retinopathy
Research question: What is the effectiveness of...
Stage: planning
```

### Step 2: Search Databases (SEARCH stage)

Advance to SEARCH stage:

```bash
uv run academic-review advance "ML Diabetic Retinopathy"
```

Search multiple databases:

```bash
# Search Crossref (fastest, no key required)
uv run academic-review search "ML Diabetic Retinopathy" \
  --database crossref \
  --keywords "machine learning diabetic retinopathy diagnosis"

# Search PubMed (medical literature)
export PUBMED_EMAIL=your.email@example.com
uv run academic-review search "ML Diabetic Retinopathy" \
  --database pubmed \
  --keywords "machine learning diabetic retinopathy"

# Search arXiv (preprints)
uv run academic-review search "ML Diabetic Retinopathy" \
  --database arxiv \
  --keywords "deep learning retinopathy"

# Search Semantic Scholar
uv run academic-review search "ML Diabetic Retinopathy" \
  --database semantic-scholar \
  --keywords "AI diabetic retinopathy diagnosis"
```

Check progress:

```bash
uv run academic-review status "ML Diabetic Retinopathy"
```

**Output:**
```
Review: ML Diabetic Retinopathy
Stage: search
Papers: 156 total
  - pending: 156
  - included: 0
  - excluded: 0
```

### Step 3: Screen Papers (SCREENING stage)

Advance to SCREENING stage:

```bash
uv run academic-review advance "ML Diabetic Retinopathy"
```

Assess papers against criteria:

```bash
# Include a high-quality paper
uv run academic-review assess "ML Diabetic Retinopathy" \
  "10.1001/jama.2016.17216" \
  --status included \
  --score 9 \
  --notes "High quality RCT, large validation set (n=11,711), expert-level performance"

# Exclude irrelevant paper
uv run academic-review assess "ML Diabetic Retinopathy" \
  "10.1234/example.2023.456" \
  --status excluded \
  --score 3 \
  --notes "No validation dataset, conference abstract only"

# Mark for later review
uv run academic-review assess "ML Diabetic Retinopathy" \
  "10.5678/unclear.2024.789" \
  --status pending \
  --notes "Need to check full text for validation details"
```

Batch screening workflow:

```bash
# List all pending papers
uv run academic-review status "ML Diabetic Retinopathy" --verbose

# For each DOI, assess:
for doi in $(cat dois_to_assess.txt); do
  echo "Assessing: $doi"
  uv run academic-review assess "ML Diabetic Retinopathy" "$doi" \
    --status included \
    --score 7 \
    --notes "Meets inclusion criteria"
done
```

### Step 4: Analyze Themes (ANALYSIS stage)

Advance to ANALYSIS stage:

```bash
uv run academic-review advance "ML Diabetic Retinopathy"
```

Run thematic analysis:

```bash
# Extract themes using TF-IDF and clustering
uv run academic-review analyze "ML Diabetic Retinopathy"
```

**Output:**
```
Analyzing themes...
Extracted 5 themes from 42 included papers:

Theme 1: Deep Learning Architectures
  Papers: 18
  Keywords: convolutional neural networks, ResNet, VGG, inception

Theme 2: Dataset Characteristics
  Papers: 15
  Keywords: validation, ground truth, fundus images, EyePACS

Theme 3: Performance Metrics
  Papers: 25
  Keywords: sensitivity, specificity, AUC, accuracy, F1-score

Theme 4: Clinical Deployment
  Papers: 8
  Keywords: real-world, clinical workflow, integration, usability

Theme 5: Interpretability
  Papers: 6
  Keywords: explainability, attention maps, grad-CAM, trust
```

With AI enhancement (optional):

```bash
export ANTHROPIC_API_KEY=sk-ant-...
uv run academic-review analyze "ML Diabetic Retinopathy" --use-ai
```

### Step 5: Generate Synthesis (SYNTHESIS stage)

Advance to SYNTHESIS stage:

```bash
uv run academic-review advance "ML Diabetic Retinopathy"
```

Generate narrative synthesis:

```bash
uv run academic-review synthesize "ML Diabetic Retinopathy"
```

**Output:**
```
Generating synthesis...

Summary:
42 papers were included examining machine learning for diabetic retinopathy diagnosis.
Studies span 2018-2024 with validation datasets ranging from 1,000 to 120,000 images.

Key Findings:
1. Deep learning models (primarily CNNs) achieve expert-level performance
2. Best models report AUC 0.96-0.99 for referable DR detection
3. External validation shows performance drop of 5-10% on average
4. Clinical deployment studies are limited (n=8)
5. Interpretability remains a key challenge for clinical acceptance

Evidence Gaps:
- Few studies in low-resource settings
- Limited diversity in validation datasets
- Insufficient long-term outcome data
- Integration with existing workflows understudied

Recommendations:
- Standardized reporting of validation datasets
- More focus on clinical deployment studies
- Development of interpretable models
- Multi-site validation studies
```

With AI enhancement:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
uv run academic-review synthesize "ML Diabetic Retinopathy" --use-ai
```

### Step 6: Export Results (COMPLETE stage)

Advance to COMPLETE stage:

```bash
uv run academic-review advance "ML Diabetic Retinopathy"
```

Export in multiple formats:

```bash
# BibTeX references
uv run academic-review export "ML Diabetic Retinopathy" \
  --format bibtex \
  --output dr_review.bib

# Word document with full report
uv run academic-review export "ML Diabetic Retinopathy" \
  --format docx \
  --output dr_review.docx

# LaTeX document
uv run academic-review export "ML Diabetic Retinopathy" \
  --format latex \
  --output dr_review.tex

# HTML report
uv run academic-review export "ML Diabetic Retinopathy" \
  --format html \
  --output dr_review.html

# Machine-readable JSON
uv run academic-review export "ML Diabetic Retinopathy" \
  --format json \
  --output dr_review.json
```

## Stage-by-Stage Guide

### PLANNING: Define Research Scope

**Goal**: Establish research question and inclusion/exclusion criteria.

**Key Activities**:
1. Formulate PICO question (Population, Intervention, Comparison, Outcome)
2. Define inclusion criteria
3. Define exclusion criteria
4. Document protocol

**Commands**:
```bash
# Initialize with comprehensive criteria
uv run academic-review init "Review Title" \
  --question "PICO-formatted question" \
  --include "Criterion 1" \
  --include "Criterion 2" \
  --exclude "Exclusion 1"

# Check initial setup
uv run academic-review status "Review Title"
```

**Tips**:
- Be specific with date ranges
- Consider language limitations
- Define study design requirements
- Plan for PRISMA flowchart

### SEARCH: Execute Database Searches

**Goal**: Systematically search academic databases.

**Key Activities**:
1. Search primary databases (Crossref, PubMed)
2. Search supplementary databases (arXiv, Semantic Scholar)
3. Document search strategies
4. Track total papers found

**Commands**:
```bash
# Advance to SEARCH stage
uv run academic-review advance "Review Title"

# Search each database
uv run academic-review search "Review Title" \
  --database crossref \
  --keywords "primary search terms"

# Check deduplication
uv run academic-review status "Review Title"
```

**Tips**:
- Start with Crossref (fastest)
- Use PubMed for medical topics
- Document exact search strings
- Note dates of searches for PRISMA

### SCREENING: Assess Papers

**Goal**: Apply inclusion/exclusion criteria to papers.

**Key Activities**:
1. Title/abstract screening
2. Full-text screening (if needed)
3. Apply inclusion/exclusion criteria
4. Document reasons for exclusion
5. Quality assessment scoring

**Commands**:
```bash
# Advance to SCREENING stage
uv run academic-review advance "Review Title"

# Include paper
uv run academic-review assess "Review Title" DOI \
  --status included \
  --score 8 \
  --notes "Reason for inclusion"

# Exclude paper
uv run academic-review assess "Review Title" DOI \
  --status excluded \
  --score 2 \
  --notes "Reason for exclusion"
```

**Tips**:
- Screen in two phases (title/abstract, then full-text)
- Document exclusion reasons
- Use quality scores consistently
- Consider dual screening for rigor

### ANALYSIS: Deep Dive into Included Papers

**Goal**: Extract themes and patterns from included papers.

**Key Activities**:
1. Data extraction
2. Thematic coding
3. Quality assessment
4. Synthesis planning

**Commands**:
```bash
# Advance to ANALYSIS stage
uv run academic-review advance "Review Title"

# Run thematic analysis
uv run academic-review analyze "Review Title"

# With AI enhancement
uv run academic-review analyze "Review Title" --use-ai
```

**Tips**:
- Use TF-IDF for objective theme extraction
- AI helps with theme naming
- Document coding framework
- Track inter-rater reliability if dual coding

### SYNTHESIS: Write Up Findings

**Goal**: Create narrative synthesis of evidence.

**Key Activities**:
1. Summarize included studies
2. Synthesize findings by theme
3. Identify evidence gaps
4. Make recommendations

**Commands**:
```bash
# Advance to SYNTHESIS stage
uv run academic-review advance "Review Title"

# Generate synthesis
uv run academic-review synthesize "Review Title"

# With AI enhancement
uv run academic-review synthesize "Review Title" --use-ai
```

**Tips**:
- AI generates draft, human refines
- Link findings to research question
- Note limitations clearly
- Follow GRADE framework for evidence quality

### COMPLETE: Export and Share

**Goal**: Disseminate review results.

**Key Activities**:
1. Export to publication format
2. Create PRISMA flowchart
3. Prepare supplementary materials
4. Archive review data

**Commands**:
```bash
# Advance to COMPLETE stage
uv run academic-review advance "Review Title"

# Export to needed formats
uv run academic-review export "Review Title" --format bibtex -o refs.bib
uv run academic-review export "Review Title" --format docx -o review.docx
uv run academic-review export "Review Title" --format json -o data.json
```

**Tips**:
- Export to multiple formats
- Include PRISMA flowchart
- Archive raw data (JSON export)
- Consider DOI for dataset via Zenodo

## Advanced Usage

### Bulk Operations

Import papers from file:

```bash
# Create DOI list
cat > dois.txt <<EOF
10.1001/jama.2016.17216
10.1038/s41591-018-0107-6
10.1016/S0140-6736(16)31679-8
EOF

# Assess all papers
while read doi; do
  uv run academic-review assess "Review Title" "$doi" \
    --status included --score 8
done < dois.txt
```

### Custom Data Directory

```bash
# Set custom location
export LIT_REVIEW_DATA_DIR=/path/to/reviews

# Or specify per-command
LIT_REVIEW_DATA_DIR=/path/to/reviews \
  uv run academic-review init "Review"
```

### Scripted Workflow

```bash
#!/bin/bash
# automated_review.sh

REVIEW="ML Healthcare Review"
QUESTION="What is the impact of ML in healthcare?"

# Initialize
uv run academic-review init "$REVIEW" --question "$QUESTION"

# Advance and search
uv run academic-review advance "$REVIEW"
uv run academic-review search "$REVIEW" -d crossref -k "machine learning healthcare"

# Check status
uv run academic-review status "$REVIEW"
```

### Integration with Reference Managers

Export to formats compatible with Zotero, Mendeley, EndNote:

```bash
# Export BibTeX (all reference managers)
uv run academic-review export "Review" -f bibtex -o refs.bib

# Import to Zotero: File → Import → refs.bib
# Import to Mendeley: File → Add Files → refs.bib
# Import to EndNote: File → Import → refs.bib
```

## Best Practices

### Protocol Registration

1. Register protocol on PROSPERO before starting
2. Document search strategy in planning stage
3. Note any protocol deviations

### Search Strategy

1. Use multiple databases (≥2 primary sources)
2. Document exact search strings
3. Note search dates for PRISMA
4. Consider grey literature sources

### Screening Process

1. Use dual screening for rigor (manual process)
2. Document inter-rater reliability
3. Resolve conflicts with third reviewer
4. Track reasons for exclusion

### Quality Assessment

1. Use validated tools (CASP, JBI, ROBINS-I)
2. Score consistently (0-10 scale)
3. Document quality criteria
4. Consider sensitivity analysis by quality

### Data Management

1. Backup regularly (automatic with tool)
2. Export to JSON for archiving
3. Consider version control for review data
4. Maintain audit trail

### Reporting

1. Follow PRISMA 2020 guidelines
2. Include PRISMA flowchart
3. Report search strategies fully
4. Share data and code (Zenodo DOI)

## Troubleshooting

### Review not advancing to next stage

Check stage requirements:

```bash
# View current status
uv run academic-review status "Review Title" --verbose

# Each stage requires:
# - PLANNING: title + question + criteria
# - SEARCH: at least 1 paper found
# - SCREENING: at least 1 paper assessed
# - ANALYSIS: at least 1 paper included
# - SYNTHESIS: themes analyzed
# - COMPLETE: synthesis generated
```

### Search returns no results

```bash
# Try broader keywords
uv run academic-review search "Review" -d crossref -k "general terms"

# Check database availability
# Crossref: always available
# PubMed: requires email
# ArXiv: may be rate-limited
# Semantic Scholar: may be rate-limited
```

### Paper already exists (duplicate)

Deduplication is automatic by DOI. If you see this message, the paper is already in your review.

```bash
# Check existing papers
uv run academic-review status "Review" --verbose

# View specific paper
uv run academic-review status "Review" --doi "10.1001/jama.2016.17216"
```

### Export fails

```bash
# Check output directory exists
mkdir -p outputs/

# Specify full path
uv run academic-review export "Review" \
  -f bibtex \
  -o /full/path/to/output.bib

# Check format is valid
# Valid formats: bibtex, docx, latex, html, json
```

## Support

- **Issues**: https://github.com/stharrold/yuimedi-paper-20250901/issues
- **Documentation**: See [lit_review_setup.md](lit_review_setup.md)
- **Examples**: See [lit_review/README.md](../lit_review/README.md)
