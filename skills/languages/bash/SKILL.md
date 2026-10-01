---
name: bash
description: Expert Bash shell scripting assistance covering POSIX compliance, parameter expansion, pipelines, traps, and debugging. Use when writing robust shell scripts, automating DevOps tasks, or handling file processing.
---

# Bash

Bourne Again SHell, the standard shell for Linux and macOS.

## When to Use

- **Linux System Administration & Automation**: Scripting OS maintenance, cron jobs, file backups, and package management.
- **CI/CD Pipeline Glue Code**: Orchestrating build, test, and container push steps in GitHub Actions and GitLab CI.
- **Docker Entrypoint Scripts**: Configuring environment variables, secrets, and database wait-for loops during container startup.
- **Command-Line Wrappers**: Wrapping multi-step CLI commands into simple, repeatable internal developer utilities.

## Quick Start

```bash
#!/bin/bash

NAME="World"
echo "Hello, $NAME!"

if [ -f "file.txt" ]; then
    echo "File exists"
else
    echo "File not found"
fi
```

## Core Concepts

### Strict Error Handling (`set -euo pipefail`)

Guarantees script execution aborts on unhandled errors, unset variables, and piped command failures:

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'
	'

# -e: Exit immediately if a command exits with a non-zero status
# -u: Treat unset variables as an error and exit immediately
# -o pipefail: Pipeline exit status matches the last failing command
```

### Robust Parameter Expansion & Default Values

Safely handles optional and required script variables:

```bash
# Provide fallback default if variable unset
TARGET_ENV="${1:-staging}"

# Throw descriptive error if variable is unset or empty
DATABASE_URL="${DATABASE_URL:?Error: DATABASE_URL environment variable is required}"

# Extract filename without extension
filename="archive_2026.tar.gz"
base="${filename%%.*}" # "archive_2026"
```

### Trap Signals for Reliable Cleanup

Ensures temporary files and child processes are cleaned up upon exit or interruption:

```bash
TEMP_DIR="$(mktemp -d)"
cleanup() {
  echo "Cleaning up temporary files..."
  rm -rf "${TEMP_DIR}"
}
trap cleanup EXIT INT TERM
```

## Common Patterns

### Safe Script Header with Error and Signal Traps

**Problem**: Shell scripts fail silently halfway through, leaving orphaned temp files and corrupted state.

**Solution**:
Use unofficial bash strict mode with automatic cleanup trap:

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

TMP_DIR=$(mktemp -d)
cleanup() {
    rm -rf "$TMP_DIR"
    echo "Cleaned up temporary workspace."
}
trap cleanup EXIT ERR INT TERM

# Script business logic
echo "Working in: $TMP_DIR"
```

## Best Practices

**Do**:

- Always Quote Variables: Wrap variables in double quotes (`"${MY_VAR}"`) to prevent word splitting and glob expansion bugs.
- Lint with ShellCheck: Run `shellcheck` in CI to catch syntax pitfalls, portability bugs, and quoting errors automatically.
- Use `[[ ... ]]` for Conditions: Prefer modern Bash conditional evaluation `[[ $var == "val" ]]` over legacy `[ ... ]`.
- Use Local Variables in Functions: Always declare variables inside functions with `local var="value"`.

**Don't**:

- Parse `ls` output: Use globbing loops (`for file in *.txt; do ... done`) instead of parsing `ls`.
- Use unquoted `eval`: `eval` executes arbitrary string inputs and introduces catastrophic shell injection vulnerabilities.
- Write multi-thousand line monolithic bash scripts: Transition complex scripts to Python or Go when logic grows large.

## Troubleshooting

| Error                                  | Cause                                                             | Solution                                                      |
| :------------------------------------- | :---------------------------------------------------------------- | :------------------------------------------------------------ |
| `syntax error: unexpected end of file` | Unclosed quotes, missing `fi`, `done`, or unbalanced parentheses. | Run `bash -n script.sh` to validate syntax without executing. |
| `command not found: $'\r'`             | Windows CRLF line endings present in shell script.                | Convert line endings with `dos2unix script.sh`.               |
| `unbound variable (with set -u)`       | Referencing unset environment or script variable.                 | Provide default value: `${VAR:-default_val}`.                 |

## References

- [ShellCheck](https://www.shellcheck.net/)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
