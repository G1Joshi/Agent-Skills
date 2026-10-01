---
name: notepad-plus-plus
description: Expert Notepad++ assistance covering text editing, regex search/replace, macro automation, plugin management via Plugins Admin, and session handling. Use when scripting text transformations, configuring Notepad++ plugins, editing large log files, or automating batch file replacements.
---

# Notepad++

Notepad++ is a lightweight, free source code editor for Windows. It is famous for its low footprint and being written in C++.

## When to Use

- **Rapid Windows Log & File Inspection**: Opening multi-gigabyte log dumps and configuration files without memory thrashing.
- **Advanced Regular Expression Replacements**: Executing multi-file regex find-and-replace across nested directories.
- **Batch Text Manipulation**: Column/block editing, character set transcoding, and newline normalization (CRLF/LF).
- **Lightweight Script Automation**: Running command-line compilers or linters via the NppExec plugin.

## Quick Start

### 1. Regex Find and Replace (Multiline & Capture Groups)

- Open Find & Replace: `Ctrl + H`
- Search Mode: Select **Regular expression** (check `. matches newline` if spanning lines)
- Find What: `(\w+)\s*=\s*"(.*?)"`
- Replace With: `{"key": "$1", "val": "$2"}`

### 2. Run from Command Line

```cmd
notepad++.exe -multiInst -nosession "C:\path\to\large_logfile.log"
```

## Core Concepts

### Multi-Line Regular Expression Find & Replace

Matching, parsing, and cleaning enterprise log files using PCRE regex engine:

```regex
# Find ISO timestamp followed by ERROR level and message:
^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)\s+\[ERROR\]\s+(.*)$

# Replace with structured TSV for Excel/database import:
$1\tERROR\t$2

# Find and eliminate empty or blank whitespace lines:
^[ \t]*$\r?\n
# Replace with: (leave empty)
```

### Column Mode (Block Selection) Editing

- Hold **Alt + Shift + Arrow Keys** (or **Alt + Left Click Drag**) to select a rectangular block across multiple lines.
- Type text or press **Edit -> Column Editor...** (`Alt+C`):
  - Insert running numbers: Initial value `1`, Increase by `1`, Format `Dec` / `Hex`.
  - Prepend leading prefixes (e.g. `export const VAR_`) simultaneously to 100+ lines.

### Automated Script Execution with NppExec

Automating Python linting or compilation directly from Notepad++:

```text
// NppExec Script: Run Python Lint & Test
npp_save
cd $(CURRENT_DIRECTORY)
cmd /c "ruff check $(FILE_NAME) && pytest -q $(FILE_NAME)"
```

## Common Patterns

### Regex Data Extraction and Transformation

**Problem**: Parse unstructured server log entries into structured CSV or JSON.  
**Solution**: Apply capture groups in Notepad++ Regex Find & Replace (`Ctrl + H`).

```regex
# Find Expression:
^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+\[(\w+)\]\s+(.*)$

# Replace Expression:
{"date": "$1", "time": "$2", "level": "$3", "message": "$4"}
```

## Best Practices

**Do**:

- Set Default Directory to "Remember last used directory" and encoding to **UTF-8 without BOM**.
- Use `Alt + Mouse Drag` for precise rectangular column editing across structured tabular files.
- Leverage the **Document Map** (`View -> Document Map`) for rapid visual navigation of large source files.
- Configure **Auto-Completion** for XML/HTML tags and word completion under **Settings -> Preferences -> Auto-Completion**.

**Don't**:

- Use standard Notepad++ for multi-gigabyte files without enabling Large File Mode or adjusting buffer sizes.
- Save Windows CRLF line endings when collaborating on Linux/Docker container repositories; enforce LF via Status Bar.
- Leave unsaved session snapshots enabled on shared or untrusted workstations.

## Troubleshooting

| Error                                                      | Cause                                                          | Solution                                                                                                     |
| ---------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Notepad++ crashes when opening multi-gigabyte log file     | 32-bit architecture memory limits or Scintilla buffer overflow | Use 64-bit Notepad++ build, or install `LargeFiles` plugin; disable syntax styling for `.log` files.         |
| Regex search matches unexpectedly across unintended blocks | Greedy quantifier `.*` used instead of lazy `.*?`              | Change quantifier from `.*` to non-greedy `.*?` or restrict character classes `[^"]*`.                       |
| Plugins Admin menu missing                                 | Enterprise deployment or outdated portable installation        | Download latest 64-bit release from notepad-plus-plus.org; ensure `plugins` directory has write permissions. |

## References

- [Notepad++ Website](https://notepad-plus-plus.org/)
