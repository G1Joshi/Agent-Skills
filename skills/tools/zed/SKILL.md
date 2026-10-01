---
name: zed
description: Expert Zed editor assistance covering high-performance Rust-based text editing, multi-buffer editing, language server protocols (LSP), and AI assistant integrations. Use when configuring Zed settings.json, setting up language extensions, collaborating in real-time channels, or optimizing editor startup speed.
---

# Zed

Zed is a high-performance, multiplayer code editor written in Rust with a GPU-accelerated UI, native Tree-sitter parsing, and fast Language Server Protocol (LSP) intelligence.

## When to Use

- **High-Performance Rust-Engineered Code Editing**: Sub-millisecond typing latency, instant file opening, and smooth 120 FPS rendering.
- **Real-Time Multiplayer Pair Programming**: Collaborating directly in the editor buffer with audio chat and shared cursor sessions.
- **Integrated Language Model (LLM) Assistants**: Generating code, refactoring functions, and querying codebase context natively.
- **Modern Tree-sitter & LSP Polyglot Development**: Seamless out-of-the-box support for Rust, TypeScript, Python, and Go.

## Quick Start

### 1. Minimal ~/.config/zed/settings.json

```json
{
  "theme": "One Dark",
  "buffer_font_family": "JetBrains Mono",
  "buffer_font_size": 14,
  "tab_size": 2,
  "hard_tabs": false,
  "format_on_save": "on",
  "formatter": "auto",
  "lsp": {
    "rust-analyzer": {
      "initialization_options": {
        "checkOnSave": { "command": "clippy" }
      }
    }
  }
}
```

### 2. Core Shortcuts

- `Cmd + P`: File finder
- `Cmd + Shift + P`: Command palette
- `Cmd + Shift + F`: Project search
- `Cmd + ?`: Toggle AI Assistant panel

## Core Concepts

### Production Zed Configuration (`~/.config/zed/settings.json`)

Configuring typography, formatters, LSP language servers, and AI integration:

```json
{
  "theme": "One Dark",
  "ui_font_size": 15,
  "buffer_font_size": 14,
  "buffer_font_family": "JetBrains Mono",
  "autosave": "on_focus_change",
  "format_on_save": "on",
  "tab_size": 2,
  "telemetry": {
    "diagnostics": false,
    "metrics": false
  },
  "languages": {
    "TypeScript": {
      "language_servers": ["vtsls", "!typescript-language-server"],
      "formatter": {
        "external": {
          "command": "prettier",
          "arguments": ["--stdin-filepath", "{buffer_path}"]
        }
      }
    },
    "Rust": {
      "language_servers": ["rust-analyzer"]
    },
    "Python": {
      "language_servers": ["pyright", "ruff"]
    }
  },
  "assistant": {
    "default_model": {
      "provider": "anthropic",
      "model": "claude-3-5-sonnet"
    }
  }
}
```

### Custom Modal & Vim Keybindings (`~/.config/zed/keymap.json`)

Customizing keymaps for high-speed navigation:

```json
[
  {
    "context": "Editor && vim_mode == normal",
    "bindings": {
      "space f f": "file_finder::Toggle",
      "space f g": "pane::DeploySearch",
      "space b d": "pane::CloseActiveItem",
      "space c a": "editor::ToggleCodeActions",
      "g d": "editor::GoToDefinition",
      "g r": "editor::FindAllReferences"
    }
  }
]
```

### Instant Multiplayer Collaboration

- Click the **Collaborate** icon in the top right window header.
- Share your room link or invite team members via GitHub username.
- Teammates share editor views, follow cursors, and edit code concurrently without screen-sharing lag.

## Common Patterns

### Multi-Buffer Project Search & Replace

**Problem**: Searching across entire codebase and editing results simultaneously in a single unified buffer.

**Solution**:

```json
[
  {
    "context": "ProjectSearchView",
    "bindings": {
      "alt-enter": "project_search::OpenInMultiBuffer"
    }
  }
]
```

### Configuring Custom Language Servers in Zed

**Problem**: Configure specific language server arguments and formatters in Zed.  
**Solution**: Define server settings in `settings.json`.

```json
{
  "languages": {
    "Python": {
      "language_servers": ["pyright", "ruff"],
      "format_on_save": "on",
      "formatter": {
        "external": {
          "command": "ruff",
          "arguments": ["format", "--stdin-filename", "{buffer_path}"]
        }
      }
    }
  }
}
```

## Best Practices

**Do**:

- Configure `format_on_save: "on"` with external tools (Prettier, Ruff, Rustfmt) for automated code cleanliness.
- Use `vtsls` for TypeScript development in Zed for superior performance and memory efficiency.
- Enable Vim mode (`"vim_mode": true`) if accustomed to modal editing workflows.
- Leverage the native Assistant Panel (`Cmd + ?`) with codebase context for rapid refactoring.

**Don't**:

- Overload project folders with unexcluded build caches (`target`, `dist`, `.next`).
- Hardcode private API keys in `settings.json`; use system keychain or environment variables.
- Leave collaborative rooms open and public when editing sensitive production configuration files.

## Troubleshooting

| Error                                  | Cause                                                               | Solution                                                                                                    |
| -------------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Language server fails to initialize    | Server binary (e.g. `gopls`, `pyright`) not found in system `$PATH` | Install server binary globally or ensure it is accessible in user shell environment.                        |
| Keybinding clash with system shortcuts | Mac system keyboard shortcuts intercepting Zed keystrokes           | Check `settings.json` keymap overrides under `~/.config/zed/keymap.json`.                                   |
| Zed AI Assistant fails to respond      | Missing API key (OpenAI/Anthropic) or quota exceeded                | Open Zed settings and configure `"features": { "edit_prediction_provider": "copilot" }` or provide API key. |

## References

- [Zed Documentation](https://zed.dev/docs)
