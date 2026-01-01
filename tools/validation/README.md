# Documentation Validation Tools

This directory contains validation scripts for ensuring quality and consistency of documentation in the YuiQuery research repository.

## 🎯 Purpose

These validation tools automatically check for:
- **File Size**: Ensure modular documentation stays under 30KB limit
- **Cross-References**: Validate internal markdown links aren't broken
- **Content Duplication**: Detect accidentally duplicated sections
- **Command Syntax**: Verify bash code blocks have valid syntax
- **Structure Validation**: Check JSON/YAML files are well-formed
- **Reference Validation**: Verify citations in paper.md exist in references.bib
- **LaTeX-in-URL Detection**: Catch LaTeX escape sequences in URLs

## 🚀 Quick Start

### Run All Validations
```bash
# From repository root
./tools/validation/validate_documentation.sh

# Or from this directory
./validate_documentation.sh
```

### Run Individual Tests
```bash
# File size validation
./tools/validation/test_file_size.sh

# Cross-reference checking
./tools/validation/test_cross_references.sh

# Content duplication detection
./tools/validation/test_content_duplication.sh

# Command syntax validation
./tools/validation/test_command_syntax.sh

# YAML/JSON structure validation
./tools/validation/test_yaml_structure.sh
```

## 📋 Validation Tests

### 1. File Size Validation (`test_file_size.sh`)
**Purpose**: Ensure documentation files remain maintainable and focused

**Checks**:
- Modular documentation files should be < 30KB
- Main paper.md can be larger (it's the comprehensive document)
- Warns on files approaching the limit

**Why**: Large files are harder to review, edit, and maintain. Modular documentation promotes better organization.

**Exit Codes**:
- `0` - All files within limits
- `1` - One or more files exceed limits

### 2. Cross-Reference Validation (`test_cross_references.sh`)
**Purpose**: Ensure internal markdown links are valid

**Checks**:
- `[text](file.md)` links point to existing files
- `[text](#section)` anchors reference valid sections
- Relative paths resolve correctly

**Why**: Broken links frustrate users and reduce documentation quality.

**Exit Codes**:
- `0` - All cross-references valid
- `1` - Broken links detected

### 3. Content Duplication Detection (`test_content_duplication.sh`)
**Purpose**: Identify accidentally duplicated content across files

**Checks**:
- Similar paragraphs/sections across multiple files
- Copy-paste errors during refactoring
- Inconsistent updates to duplicated content

**Why**: Duplication leads to maintenance burden and inconsistency when only one copy is updated.

**Exit Codes**:
- `0` - No significant duplication
- `1` - Duplicated content detected

### 4. Command Syntax Validation (`test_command_syntax.sh`)
**Purpose**: Verify bash commands in code blocks are syntactically valid

**Checks**:
- Bash code blocks have valid syntax
- No unclosed quotes or parentheses
- Basic shell script validation

**Why**: Invalid examples in documentation confuse users and damage credibility.

**Exit Codes**:
- `0` - All commands have valid syntax
- `1` - Syntax errors detected

### 5. Structure Validation (`test_yaml_structure.sh`)
**Purpose**: Validate JSON and YAML files are well-formed

**Checks**:
- JSON files parse correctly
- YAML files have valid syntax
- Configuration files are structurally sound

**Why**: Malformed structured data breaks automated tools and workflows.

**Exit Codes**:
- `0` - All files well-formed
- `1` - Parsing errors detected

### 6. Reference Validation (`validate_references.py --check-citations`)
**Purpose**: Ensure all citations in paper.md exist in references.bib

**Checks**:
- Every `[@key]` citation has a matching BibTeX entry
- Detects undefined references before PDF build fails
- Validates pandoc-citeproc format citations

**Why**: Missing citations cause build failures and broken references in published papers.

**Exit Codes**:
- `0` - All citations have matching references
- `1` - Undefined citations detected

### 7. LaTeX-in-URL Validation (`validate_references.py --check-latex`)
**Purpose**: Detect LaTeX escape sequences accidentally left in URLs

**Checks**:
- URLs in references.bib don't contain `\_` or other LaTeX escapes
- Catches common copy-paste errors from LaTeX documents

**Why**: LaTeX escapes in URLs cause broken links when rendered.

**Exit Codes**:
- `0` - No LaTeX commands in URLs
- `1` - LaTeX escapes detected in URLs

## 🔧 Validation Orchestrator

### validate_documentation.sh
**Main Script**: Runs all validation tests in sequence

**Features**:
- Executes all 7 validation tests (5 bash + 2 Python)
- Aggregates results
- Provides summary pass/fail status
- Colorized output for readability

**Usage**:
```bash
./tools/validation/validate_documentation.sh
```

**Exit Codes**:
- `0` - All tests passed
- `1+` - Number of failed tests

**Output Example**:
```
=== YuiQuery Research Documentation Validation ===

Test 1: File size validation
✅ All files within size limits

Test 2: Cross-reference validation
✅ All cross-references valid

Test 3: Content duplication detection
⚠️  Minor duplication detected in 2 files

Test 4: Command syntax validation
✅ All command syntax valid

Test 5: YAML structure validation
✅ All structured files well-formed

Test 6: Reference validation
Found 110 references (99 academic, 11 industry)
  ✅ Reference validation passed

Test 7: LaTeX-in-URL validation
OK: No LaTeX commands found in URLs
  ✅ LaTeX-in-URL validation passed

=== Validation Summary ===
✅ PASS: All validation tests passed
```

## 🛠️ Integration

### Pre-Commit Hooks
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
./tools/validation/validate_documentation.sh
if [ $? -ne 0 ]; then
    echo "Documentation validation failed. Commit aborted."
    exit 1
fi
```

### GitHub Actions
Add to `.github/workflows/validate.yml`:
```yaml
name: Documentation Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Validation
        run: ./tools/validation/validate_documentation.sh
```

### CI/CD Pipeline
```bash
# In your CI/CD script
./tools/validation/validate_documentation.sh || exit 1
```

## 📊 Validation Metrics

### Current Repository Status
Run validation to see current metrics:
```bash
./tools/validation/validate_documentation.sh
```

### Tracking Quality Over Time
```bash
# Add to monthly review script
echo "$(date): Validation Results" >> validation_history.log
./tools/validation/validate_documentation.sh >> validation_history.log 2>&1
```

## 🔍 Customization

### Adjusting Thresholds

**File Size Limits** - Edit `test_file_size.sh`:
```bash
MAX_SIZE=30720  # 30KB in bytes
```

**Duplication Sensitivity** - Edit `test_content_duplication.sh`:
```bash
SIMILARITY_THRESHOLD=0.8  # 80% similarity triggers warning
```

### Adding New Validations

1. Create new test script: `test_your_check.sh`
2. Make executable: `chmod +x test_your_check.sh`
3. Add to `validate_documentation.sh`:
```bash
echo "Test N: Your check description"
"$SCRIPT_DIR/test_your_check.sh"
if [ $? -ne 0 ]; then
    ((total_errors++))
fi
echo ""
```

## 🐛 Troubleshooting

### Script Not Executable
```bash
chmod +x tools/validation/*.sh
```

### Wrong Working Directory
Scripts use `$SCRIPT_DIR` for path resolution, so they work from any directory:
```bash
# These all work
./tools/validation/validate_documentation.sh
cd tools/validation && ./validate_documentation.sh
bash tools/validation/validate_documentation.sh
```

### Test Failures
```bash
# Run individual tests for detailed output
./tools/validation/test_file_size.sh -v  # Verbose mode

# Debug specific test
bash -x ./tools/validation/test_command_syntax.sh
```

## 🔗 Related Documentation

- [CLAUDE.md](../../CLAUDE.md) - Project documentation standards
- [README.md](../../README.md) - Repository overview
- [scripts/validate_references.py](../../scripts/validate_references.py) - Reference validation script

## 📈 Best Practices

### When to Run Validations

**Always**:
- Before committing changes
- Before creating pull requests
- After major refactoring
- Monthly as part of documentation review

**Optional**:
- During active editing (for quick feedback)
- In CI/CD pipeline (automated quality gate)
- Before publication or release

### Interpreting Results

- **All Pass**: Documentation meets quality standards ✅
- **Warnings**: Non-critical issues, fix when convenient ⚠️
- **Failures**: Must fix before merging ❌

### Maintaining Validations

- Review validation rules quarterly
- Update thresholds based on repository needs
- Add new checks as documentation grows
- Archive obsolete validations

## 🎓 Validation Philosophy

These tools embody documentation quality principles:
- **Automated**: Catch issues early without manual review
- **Fast**: Complete validation in seconds
- **Actionable**: Clear error messages with fix guidance
- **Non-Intrusive**: Pass/fail, not style enforcement
- **Maintainable**: Simple scripts, easy to understand and modify

---

*Part of YuiQuery Healthcare Analytics Research project documentation infrastructure*
