---
name: notepad-plus-plus
description: Notepad++ text editor for Windows. Use for quick editing.
---

# Notepad++

Notepad++ is a lightweight, free source code editor for Windows. It is famous for its low footprint and being written in C++.

## When to Use

- **Quick Edits**: Editing config files, XML, or JSON on a Windows server.
- **Log Analysis**: Search and highlight in massive log files.
- **Regex**: Great "Find in Files" with regex substitution.

## Core Concepts

### Scintilla

The editing component engine behind N++.

### Plugins

Managed via "Plugins Admin". XML Tools, Compare, NppExec.

### Macros

Record and playback keystrokes. Very useful for repetitive text transformations.

## Best Practices (2025)

**Do**:

- **Use "Compare"**: The Diff plugin is simple and effective.
- **Use Dark Mode**: Yes, even Notepad++ has dark mode now.
- **Portable Version**: Carry it on a USB stick (or cloud drive) with your toolkit.

**Don't**:

- **Don't code full apps**: It lacks LSP and modern IDE features. Use VS Code for dev, N++ for text munging.

## References

- [Notepad++ Website](https://notepad-plus-plus.org/)
