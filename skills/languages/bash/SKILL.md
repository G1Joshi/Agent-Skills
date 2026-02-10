---
name: bash
description: Bash shell scripting for automation, pipelines, and system administration. Use for .sh files and Linux scripting.
---

# Bash

Bourne Again SHell, the standard shell for Linux and macOS.

## When to Use

- Automating system tasks
- CI/CD pipelines
- File manipulation
- Glue code between CLIs

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

### Variables

No data types. Everything is a string.

```bash
count=10
echo $count
```

### Pipes and Redirection

- `|`: Pipe output of one command to input of next.
- `>`: Redirect output to file (overwrite).
- `>>`: Redirect output to file (append).

```bash
cat file.txt | grep "error" > errors.log
```

### Exit Codes

Commands return `0` for success and non-zero for failure. Check with `$?`.

## Best Practices

**Do**:

- Use `set -e` (e)xit on error
- Use `set -u` (u)nset variable usage is error
- Use `set -o pipefail` to catch errors in pipes
- Quote variables `"$VAR"` to handle spaces

**Don't**:

- Parse `ls` output (use globs `*`)
- Use simple `[` vs `[[` (double brackets are safer)

## References

- [ShellCheck](https://www.shellcheck.net/)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
