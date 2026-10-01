---
name: sublime-text
description: Expert Sublime Text assistance covering Package Control, LSP integration, custom keybindings, syntax definitions, and build systems. Use when configuring Sublime Text 4, setting up LSP for language intelligence, writing custom build systems, or optimizing text editing workflows.
---

# Sublime Text 4

Sublime Text is a lightweight, ultra-responsive text editor known for its instant startup speed, multi-caret editing, and extensible Package Control ecosystem.

## When to Use

- **Instantaneous Large File Editing**: Opening massive log files, JSON dumps, and SQL exports with zero lag.
- **Multiple Selection & Column Editing**: Refactoring repeated patterns rapidly using multi-cursor manipulation.
- **Lightweight Polyglot Coding**: Editing diverse scripts (Python, Bash, Rust, Go) without the overhead of heavy IDEs.
- **Custom Build Systems & Macros**: Automating compilation, syntax checking, and text transformation pipelines.

## Quick Start

### 1. Minimal Custom Build System

```json
// ~/.config/sublime-text/Packages/User/NodeRun.sublime-build
{
  "cmd": ["node", "$file"],
  "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
  "selector": "source.js",
  "shell": true
}
```

### 2. Custom User Keybindings

```json
// Preferences > Key Bindings
[
  { "keys": ["super+shift+r"], "command": "reindent" },
  { "keys": ["super+d"], "command": "find_under_expand" }
]
```

## Core Concepts

### Production Editor Configuration (`Preferences.sublime-settings`)

Configuring modern performance, typography, and whitespace rules:

```json
{
  "font_face": "JetBrains Mono",
  "font_size": 13,
  "theme": "Default Dark.sublime-theme",
  "color_scheme": "Packages/Color Scheme - Default/Mariana.sublime-color-scheme",
  "draw_white_space": "selection",
  "ensure_newline_at_eof_on_save": true,
  "trim_trailing_white_space_on_save": true,
  "tab_size": 2,
  "translate_tabs_to_spaces": true,
  "word_wrap": false,
  "hardware_acceleration": "opengl",
  "index_files": true,
  "show_git_status": true
}
```

### Custom Polyglot Build System (`PythonTest.sublime-build`)

Automating test running and error matching directly from the editor:

```json
{
  "cmd": ["pytest", "-q", "$file"],
  "selector": "source.python",
  "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$",
  "working_dir": "$project_path",
  "env": {
    "PYTHONPATH": "$project_path"
  },
  "variants": [
    {
      "name": "Ruff Check",
      "cmd": ["ruff", "check", "$file"]
    }
  ]
}
```

### High-Speed Multi-Cursor Workflows

- Select word: `Ctrl+D` (macOS: `Cmd+D`) to select next matching occurrence.
- Select all matching occurrences in file: `Alt+F3` (macOS: `Ctrl+Cmd+G`).
- Split lines into selection: Select lines -> `Ctrl+Shift+L` (macOS: `Cmd+Shift+L`) -> edit every line simultaneously.
- Jump to file: `Ctrl+P` (macOS: `Cmd+P`).
- Jump to symbol: `Ctrl+R` (macOS: `Cmd+R`).

## Common Patterns

### Full LSP Integration (LSP + LSP-typescript)

**Problem**: Need modern TypeScript autocompletion, hover docs, and diagnostics inside Sublime Text.  
**Solution**: Install `LSP` and `LSP-typescript` via Package Control.

```json
// LSP.sublime-settings
{
  "clients": {
    "lsp-typescript": {
      "enabled": true,
      "settings": {
        "typescript.suggest.completeFunctionCalls": true
      }
    }
  }
}
```

### Project Workspace Management

**Problem**: Save project-specific folder configurations, excluded paths, and build targets.  
**Solution**: Create a `.sublime-project` file.

```json
{
  "folders": [
    {
      "path": ".",
      "folder_exclude_patterns": ["node_modules", ".git", "dist"],
      "file_exclude_patterns": ["*.min.js", "*.map"]
    }
  ],
  "settings": {
    "tab_size": 2,
    "translate_tabs_to_spaces": true
  }
}
```

## Best Practices

**Do**:

- Install **Package Control** and the **LSP** package (`LSP`, `LSP-pyright`, `LSP-typescript`) for IDE-grade completions.
- Enable `hardware_acceleration: "opengl"` for ultra-fluid 120Hz/144Hz scrolling on supported displays.
- Use `Ctrl+Shift+L` (`Cmd+Shift+L`) to convert multiple lines into independent cursor selections.
- Configure project files (`.sublime-project`) with explicit `folder_exclude_patterns` for `node_modules` and `.git`.

**Don't**:

- Leave file indexing enabled on massive multi-gigabyte build output directories.
- Install unmaintained legacy Sublime Text 2/3 plugins that block the UI thread.
- Store sensitive API keys in plaintext user snippets or build configurations.

## Troubleshooting

| Error                                                               | Cause                                                                | Solution                                                                                                            |
| ------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `Package Control: There are no packages available for installation` | SSL cert validation failure or network proxy interference            | Check `Preferences > Package Settings > Package Control > Settings` and add custom `http_proxy` or refresh channel. |
| High CPU usage by `plugin_host`                                     | Heavy file indexing on large dependency directories (`node_modules`) | Add `node_modules` to `binary_file_patterns` or `folder_exclude_patterns` in User Preferences.                      |
| LSP server fails to start                                           | Target runtime (`node`, `python`, etc.) not in Sublime's `$PATH`     | Add environment path in `LSP.sublime-settings` under `"env": { "PATH": "/usr/local/bin:$PATH" }`.                   |

## References

- [Sublime Text Documentation](https://www.sublimetext.com/docs/)
