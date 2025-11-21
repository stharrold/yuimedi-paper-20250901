#!/bin/bash
# Documentation validation orchestrator for yuimedi-paper repository

echo "=== YuiQuery Research Documentation Validation ==="
echo ""

# Run all validation tests
total_errors=0

# Test 1: File size validation
echo "Test 1: File size validation"
./test_file_size.sh
if [ $? -ne 0 ]; then
    ((total_errors++))
fi
echo ""

# Test 2: Cross-reference validation
echo "Test 2: Cross-reference validation"
./test_cross_references.sh
if [ $? -ne 0 ]; then
    ((total_errors++))
fi
echo ""

# Test 3: Content duplication detection
echo "Test 3: Content duplication detection"
./test_content_duplication.sh
if [ $? -ne 0 ]; then
    ((total_errors++))
fi
echo ""

# Test 4: Command syntax validation
echo "Test 4: Command syntax validation"
./test_command_syntax.sh
if [ $? -ne 0 ]; then
    ((total_errors++))
fi
echo ""

# Test 5: YAML structure validation
echo "Test 5: YAML structure validation"
./test_yaml_structure.sh
if [ $? -ne 0 ]; then
    ((total_errors++))
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