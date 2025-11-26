#!/bin/bash
# Command syntax validation - check bash code blocks in markdown files

echo "Testing bash command syntax in documentation..."

# Files to check
FILES_TO_CHECK=(
    "CLAUDE.md"
    "README.md"
    "CONTRIBUTING.md"
)

total_errors=0
total_commands=0

for target_file in "${FILES_TO_CHECK[@]}"; do
    if [ ! -f "$target_file" ]; then
        echo "  ⚠ $target_file: not found (skipping)"
        continue
    fi

    echo "  Checking: $target_file"
    file_errors=0
    commands_tested=0

    # Extract bash commands from code blocks
    in_bash_block=false
    while IFS= read -r line; do
        if [[ $line == '```bash' ]]; then
            in_bash_block=true
            continue
        elif [[ $line == '```' ]] && [ "$in_bash_block" = true ]; then
            in_bash_block=false
            continue
        elif [ "$in_bash_block" = true ]; then
            # Remove leading $ if present
            command=$(echo "$line" | sed 's/^\$ *//')

            # Skip empty lines, comments, and continuation lines
            [[ -z "$command" || "$command" =~ ^# || "$command" =~ ^[[:space:]]*$ ]] && continue
            [[ "$command" =~ \\$ ]] && continue  # Skip lines ending with \

            ((commands_tested++))
            ((total_commands++))

            # Basic syntax check (this is conservative - only checks obvious errors)
            # Skip commands with placeholders like <argument>
            if [[ ! "$command" =~ \< ]] && [[ ! "$command" =~ \.\.\. ]]; then
                if ! bash -n <<< "$command" 2>/dev/null; then
                    echo "    ✗ Syntax error: $command"
                    ((file_errors++))
                    ((total_errors++))
                fi
            fi
        fi
    done < "$target_file"

    if [ $file_errors -eq 0 ]; then
        echo "    ✓ $commands_tested commands checked, all valid"
    fi
done

echo ""
if [ $total_errors -eq 0 ]; then
    echo "✅ PASS: All $total_commands bash commands have valid syntax"
    exit 0
else
    echo "❌ FAIL: Found $total_errors syntax errors in $total_commands commands"
    exit 1
fi
