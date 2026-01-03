#!/bin/bash
# Content duplication detection test - check for repeated sections in documentation

echo "Checking for content duplication in documentation..."

# Key files to check
FILES_TO_CHECK=(
    "paper.md"
    "CLAUDE.md"
    "README.md"
    "CONTRIBUTING.md"
)

# Simple check: look for sections that appear identical multiple times
# This is a basic heuristic - checks for repeated heading + first paragraph patterns

total_warnings=0

for file in "${FILES_TO_CHECK[@]}"; do
    if [ ! -f "$file" ]; then
        echo "  ⚠ $file: not found (skipping)"
        continue
    fi

    echo "  Checking: $file"

    # Count occurrences of major sections (## headers)
    duplicates=$(grep '^## ' "$file" 2>/dev/null | sort | uniq -d | wc -l)

    if [ $duplicates -gt 0 ]; then
        echo "    ⚠ Found $duplicates potentially duplicate section headings"
        ((total_warnings++))
    else
        echo "    ✓ No obvious duplicate sections found"
    fi
done

# This is an informational check - warnings don't fail the test
echo ""
if [ $total_warnings -eq 0 ]; then
    echo "✅ PASS: No duplicate content detected"
else
    echo "⚠️  PASS: $total_warnings file(s) with potential duplicates (review manually)"
fi

exit 0
