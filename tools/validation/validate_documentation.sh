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

# Test 6: Reference validation (citations and URLs)
echo "Test 6: Reference validation"
python3 "$REPO_ROOT/scripts/validate_references.py" --check-citations 2>/dev/null
if [ $? -ne 0 ]; then
    ((total_errors++))
    echo "  ❌ Reference validation failed"
else
    echo "  ✅ Reference validation passed"
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
