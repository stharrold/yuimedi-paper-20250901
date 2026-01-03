#!/bin/bash
# File size compliance test - documentation files should be < 30KB (except paper.md)

MAX_SIZE=30000  # 30KB limit
errors=0

# Files to check (excluding paper.md and TODO files which can be larger)
FILES_TO_CHECK=(
    "CLAUDE.md"
    "README.md"
    "CONTRIBUTING.md"
)

echo "Checking file sizes (30KB limit for modular documentation)..."

for file in "${FILES_TO_CHECK[@]}"; do
    if [ -f "$file" ]; then
        current_size=$(wc -c < "$file")
        if [ $current_size -gt $MAX_SIZE ]; then
            echo "  ✗ $file: $current_size bytes (exceeds limit by $((current_size - MAX_SIZE)) bytes)"
            ((errors++))
        else
            remaining=$((MAX_SIZE - current_size))
            echo "  ✓ $file: $current_size bytes ($remaining bytes remaining)"
        fi
    else
        echo "  ⚠ $file: not found (skipping)"
    fi
done

# Check large files exist but don't enforce size limit
if [ -f "paper.md" ]; then
    paper_size=$(wc -c < "paper.md")
    echo "  ℹ paper.md: $paper_size bytes (research document, no size limit)"
else
    echo "  ⚠ paper.md: not found"
fi

if [ -f "TODO_FOR_HUMAN.md" ]; then
    todo_size=$(wc -c < "TODO_FOR_HUMAN.md")
    echo "  ℹ TODO_FOR_HUMAN.md: $todo_size bytes (TODO file, no size limit)"
else
    echo "  ⚠ TODO_FOR_HUMAN.md: not found"
fi

if [ $errors -eq 0 ]; then
    echo "✅ PASS: All documentation files within size limits"
    exit 0
else
    echo "❌ FAIL: $errors file(s) exceed size limit"
    exit 1
fi
