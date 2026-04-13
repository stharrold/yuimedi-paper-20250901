#!/bin/bash
# Documentation validation orchestrator for yuimedi-paper repository

# Get script directory for relative path resolution (handle symlinks)
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, resolve it
done
SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
REPO_ROOT="$( cd -P "$SCRIPT_DIR/../.." && pwd )"

echo "=== YuiQuery Research Documentation Validation ==="
echo ""

# Run all validation tests
total_errors=0

# Test 1: File size validation
echo "Test 1: File size validation"
"$SCRIPT_DIR/test_file_size.sh"
if [ $? -ne 0 ]; then
    ((total_errors++))
fi
echo ""

# Test 2: Cross-reference validation
echo "Test 2: Cross-reference validation"
"$SCRIPT_DIR/test_cross_references.sh"
if [ $? -ne 0 ]; then
    ((total_errors++))
fi
echo ""

# Test 3: Content duplication detection
echo "Test 3: Content duplication detection"
"$SCRIPT_DIR/test_content_duplication.sh"
if [ $? -ne 0 ]; then
    ((total_errors++))
fi
echo ""

# Test 4: Command syntax validation
echo "Test 4: Command syntax validation"
"$SCRIPT_DIR/test_command_syntax.sh"
if [ $? -ne 0 ]; then
    ((total_errors++))
fi
echo ""

# Test 5: YAML structure validation
echo "Test 5: YAML structure validation"
"$SCRIPT_DIR/test_yaml_structure.sh"
if [ $? -ne 0 ]; then
    ((total_errors++))
fi
echo ""

# Detect Python 3.11+ runner. Prefer uv (respects pyproject.toml's
# requires-python = ">=3.11"), then python3, then bare python if it is
# Python 3.11+ (common on venvs where only `python` is on PATH). Never fall
# back to Python 2 or older Python 3 versions. The 3.11 floor is required
# because scripts/validate_references.py imports `datetime.UTC`, added in 3.11.
PYTHON_CMD=()
if command -v uv &> /dev/null; then
    PYTHON_CMD=("uv" "run" "python")
elif command -v python3 &> /dev/null && \
     python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
    PYTHON_CMD=("python3")
elif command -v python &> /dev/null && \
     python -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
    PYTHON_CMD=("python")
fi

# Reference validation (tests 6-7) requires Python 3.11+. If no interpreter is
# available, fail fast with a clear error rather than silently skipping these
# checks and giving a misleading validation result in local runs or CI.
if [ ${#PYTHON_CMD[@]} -eq 0 ]; then
    echo "❌ ERROR: No Python 3.11+ interpreter found (tried uv, python3, python)."
    echo "   Tests 6-7 (reference validation) require Python 3.11+ (scripts/validate_references.py uses datetime.UTC)."
    echo ""
    echo "=== Validation Summary ==="
    echo "❌ FAIL: Python 3.11+ interpreter is required for reference validation"
    exit 1
fi

# Test 6: Reference validation (citations and URLs)
echo "Test 6: Reference validation"
"${PYTHON_CMD[@]}" "$REPO_ROOT/scripts/validate_references.py" --check-citations
if [ $? -ne 0 ]; then
    ((total_errors++))
    echo "  ❌ Reference validation failed"
else
    echo "  ✅ Reference validation passed"
fi
echo ""

# Test 7: LaTeX-in-URL validation
echo "Test 7: LaTeX-in-URL validation"
"${PYTHON_CMD[@]}" "$REPO_ROOT/scripts/validate_references.py" --check-latex
if [ $? -ne 0 ]; then
    ((total_errors++))
    echo "  ❌ LaTeX-in-URL validation failed"
else
    echo "  ✅ LaTeX-in-URL validation passed"
fi
echo ""

# Summary
echo "=== Validation Summary ==="
if [ $total_errors -eq 0 ]; then
    echo "✅ PASS: All validation tests passed"
    exit 0
else
    echo "❌ FAIL: $total_errors test(s) failed"
    exit 1
fi
