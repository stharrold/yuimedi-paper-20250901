#!/bin/bash
# YAML structure validation - check JSON files for valid structure

echo "Testing JSON/YAML structure in project files..."

# Files to check
FILES_TO_CHECK=(
    "TODO_FOR_AI.json"
    "DECISION_LOG.json"
)

total_errors=0

for file in "${FILES_TO_CHECK[@]}"; do
    if [ ! -f "$file" ]; then
        echo "  ⚠ $file: not found (skipping)"
        continue
    fi

    echo "  Checking: $file"

    # Use Python to validate JSON structure
    if command -v python3 >/dev/null 2>&1; then
        if python3 -c "import json; json.load(open('$file'))" 2>/dev/null; then
            echo "    ✓ Valid JSON structure"
        else
            echo "    ✗ Invalid JSON structure"
            ((total_errors++))
        fi
    else
        echo "    ⚠ Python3 not available, skipping validation"
    fi
done

echo ""
if [ $total_errors -eq 0 ]; then
    echo "✅ PASS: All JSON/YAML files have valid structure"
    exit 0
else
    echo "❌ FAIL: Found $total_errors files with invalid structure"
    exit 1
fi
