#!/bin/bash
# Cross-reference integrity test - check internal links in markdown files

errors=0

# Files to check for cross-references
FILES_TO_CHECK=(
    "paper.md"
    "CLAUDE.md"
    "README.md"
    "CONTRIBUTING.md"
)

echo "Testing internal links in documentation files..."

for target_file in "${FILES_TO_CHECK[@]}"; do
    if [ ! -f "$target_file" ]; then
        echo "  ⚠ $target_file: not found (skipping)"
        continue
    fi

    echo "  Checking: $target_file"
    file_errors=0

    # Extract internal links and check if targets exist
    while IFS= read -r link; do
        if [[ $link =~ \[(.*)\]\((#.*)\) ]]; then
            link_text="${BASH_REMATCH[1]}"
            anchor="${BASH_REMATCH[2]#\#}"  # Remove leading #

            # Convert anchor to expected format (lowercase, spaces to dashes)
            expected_anchor=$(echo "$anchor" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

            # Check if anchor exists in file (look for matching heading)
            # Convert heading text to anchor format and check
            if ! grep -E "^#+[[:space:]].*" "$target_file" | grep -qi "$expected_anchor"; then
                # Try alternate check: look for the exact heading text
                heading_text=$(echo "$anchor" | tr '-' ' ')
                if ! grep -E "^#+[[:space:]].*" "$target_file" | grep -qi "$heading_text"; then
                    echo "    ✗ Broken link: [$link_text](#$anchor)"
                    ((file_errors++))
                    ((errors++))
                fi
            fi
        fi
    done < <(grep -o '\[.*\](#[^)]*)' "$target_file" 2>/dev/null || true)

    if [ $file_errors -eq 0 ]; then
        echo "    ✓ All internal links valid"
    fi
done

if [ $errors -eq 0 ]; then
    echo "✅ PASS: All cross-references are valid"
    exit 0
else
    echo "❌ FAIL: Found $errors broken references"
    exit 1
fi