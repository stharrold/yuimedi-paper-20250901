---
description: Configuration for AI behavior when using local Codacy CLI
applyTo: '**'
---

# Codacy Local CLI Rules

Configuration for AI behavior when using the local Codacy CLI for code quality analysis.

## CRITICAL: After ANY successful file edit
- YOU MUST IMMEDIATELY run the local Codacy CLI for each file that was edited:
  ```bash
  ./.codacy/cli.sh analyze --tool pylint path/to/edited/file.py
  ```
- For non-Python files, use appropriate tools or run all tools:
  ```bash
  ./.codacy/cli.sh analyze path/to/edited/file
  ```
- If any issues are found in the new edits, propose and apply fixes for them.
- > NOTE: Failure to follow this rule is considered a critical error.

## After every response
- If you made any file edits in this conversation, verify you ran the local Codacy CLI analysis

## CRITICAL: Dependencies and Security Checks
- IMMEDIATELY after ANY of these actions:
  - Running npm/yarn/pnpm install
  - Adding dependencies to package.json
  - Adding dependencies to requirements.txt
  - Adding dependencies to pom.xml
  - Adding dependencies to build.gradle
  - Adding dependencies to uv.lock or pyproject.toml
  - Any other package manager operations
- You MUST run security scanning with Trivy:
  ```bash
  ./.codacy/cli.sh analyze --tool trivy .
  ```
- If any vulnerabilities are found because of the newly added packages:
  - Stop all other operations
  - Propose and apply fixes for the security issues
  - Only continue with the original task after security issues are resolved

## Available Analysis Tools

The local Codacy CLI provides the following tools:

### Code Quality Tools
- **pylint** - Python code analysis
- **eslint** - JavaScript/TypeScript analysis
- **pmd** - Java code analysis
- **revive** - Go code analysis
- **dartanalyzer** - Dart code analysis

### Security Tools
- **trivy** - Vulnerability and secret scanning
- **semgrep** - Security-focused static analysis

### Complexity Tools
- **lizard** - Cyclomatic complexity analysis

## Common Usage Patterns

### Single File Analysis
```bash
# Python file
./.codacy/cli.sh analyze --tool pylint mcp-manager.py

# JavaScript file
./.codacy/cli.sh analyze --tool eslint script.js

# Any supported file
./.codacy/cli.sh analyze specific-file.ext
```

### Security Scanning
```bash
# Full security scan
./.codacy/cli.sh analyze --tool trivy .

# Specific vulnerability types
./.codacy/cli.sh analyze --tool semgrep
```

### Output Formats
```bash
# Standard JSON output (default)
./.codacy/cli.sh analyze --tool pylint file.py

# SARIF format for CI/CD integration
./.codacy/cli.sh analyze --format sarif -o results.sarif

# Output to file
./.codacy/cli.sh analyze --tool pylint -o analysis-results.json
```

### Full Project Analysis
```bash
# Run all configured tools on entire project
./.codacy/cli.sh analyze

# Run specific tool on all supported files
./.codacy/cli.sh analyze --tool pylint
```

## Error Handling

### If CLI is not available
- Verify the CLI is installed: `./.codacy/cli.sh version`
- Check that the wrapper script has execute permissions: `chmod +x ./.codacy/cli.sh`
- Ensure the binary cache exists in `~/Library/Caches/Codacy/` (macOS)

### If analysis fails
- Check file exists and is readable
- Verify tool supports the file type
- Review tool-specific configuration in `.codacy/tools-configs/`
- Check `.codacy/codacy.yaml` for tool definitions

## General Guidelines

- Repeat the analysis for each modified file individually
- "Propose fixes" means to both suggest and, if possible, automatically apply the fixes
- You MUST NOT wait for the user to ask for analysis or remind you to run the tool
- Do not run analysis looking for changes in code coverage metrics
- Focus on actionable code quality and security issues
- When multiple files are edited, analyze each one separately for targeted feedback

## Tool Configuration

Tool-specific configurations are maintained in:
- `.codacy/codacy.yaml` - Main configuration with tool versions
- `.codacy/tools-configs/` - Individual tool configuration files
- `.codacy/cli-config.yaml` - CLI operation mode (local)

The local CLI operates in **local mode** and does not require cloud connectivity or API tokens.
