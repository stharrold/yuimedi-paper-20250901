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

# Detect Python 3 runner (prefer uv, then python3; skip bare python to avoid Python 2)
PYTHON_CMD=()
if command -v uv &> /dev/null; then
    PYTHON_CMD=("uv" "run" "python")
elif command -v python3 &> /dev/null; then
    PYTHON_CMD=("python3")
fi

# Test 6: Reference validation (citations and URLs)
echo "Test 6: Reference validation"
if [ ${#PYTHON_CMD[@]} -eq 0 ]; then
    echo "  ⚠ Skipped: No Python 3 interpreter found (tried uv, python3)"
    ((total_errors++))
else
    "${PYTHON_CMD[@]}" "$REPO_ROOT/scripts/validate_references.py" --check-citations
    if [ $? -ne 0 ]; then
        ((total_errors++))
        echo "  ❌ Reference validation failed"
    else
        echo "  ✅ Reference validation passed"
    fi
fi
echo ""

# Test 7: LaTeX-in-URL validation
echo "Test 7: LaTeX-in-URL validation"
if [ ${#PYTHON_CMD[@]} -eq 0 ]; then
    echo "  ⚠ Skipped: No Python 3 interpreter found"
    ((total_errors++))
else
    "${PYTHON_CMD[@]}" "$REPO_ROOT/scripts/validate_references.py" --check-latex
    if [ $? -ne 0 ]; then
        ((total_errors++))
        echo "  ❌ LaTeX-in-URL validation failed"
    else
        echo "  ✅ LaTeX-in-URL validation passed"
    fi
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
