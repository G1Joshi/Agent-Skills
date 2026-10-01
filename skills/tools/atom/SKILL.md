---
name: atom
description: Expert legacy Atom editor assistance covering packages, keymaps, and migration paths to modern successors (VS Code, Pulsar, Zed). Use when reviewing legacy Atom packages or migrating configurations.
---

# Atom (Legacy)

> **Atom is Discontinued**. The project has been officially archived by GitHub; modern alternatives include VS Code, Zed, and Pulsar.

Atom pioneered Electron-based editors and the modern extension model. Its spirit lives on in **VS Code** (Microsoft) and **Zed** (created by Atom's founder).

## When to Use

- **Legacy Atom Editor Maintenance & Migration**: Migrating legacy Atom packages and configurations to Pulsar, VS Code, or Zed.
- **Pulsar Community Fork**: Continuing to run the open-source community successor to the retired GitHub Atom editor.
- **Custom Electron-Based Text Editor Tooling**: Analyzing Atom's architecture for desktop editor extensions.
- **CSON & Keymap Configuration**: Converting `.cson` keymaps and snippet definitions to modern JSON/YAML formats.

## Quick Start

```bash
# Atom is officially discontinued. Migrate packages and configs to Pulsar or VS Code:
# Export installed package names:
apm list --installed --bare > atom-packages.txt
```

## Core Concepts

### Modern Migration Alternatives

1. **VS Code**: Direct successor in spirit, architecture, and extension ecosystem.
2. **Zed**: High-performance Rust-based editor created by Atom's original author.
3. **Pulsar**: Community-driven open-source fork maintaining backward compatibility with Atom packages.

### Migrating CSON Configuration to Modern JSON

Converting legacy Atom CoffeeScript Object Notation:

```cson
# Legacy ~/.atom/config.cson
"*":
  core:
    telemetryConsent: "no"
    themes: [
      "one-dark-ui"
      "one-dark-syntax"
    ]
  editor:
    fontFamily: "Fira Code"
    fontSize: 14
    tabLength: 2
    showInvisibles: true
```

Converted to modern VS Code / Pulsar `settings.json`:

```json
{
  "editor.fontFamily": "Fira Code",
  "editor.fontSize": 14,
  "editor.tabSize": 2,
  "editor.renderWhitespace": "all",
  "telemetry.telemetryLevel": "off",
  "workbench.colorTheme": "One Dark Pro"
}
```

### Keybindings & Package Management (APM)

Historical package inspection and migration:

```bash
# List installed legacy packages
apm list --installed --bare

# Migrate package list to modern editor extensions
apm list --installed --bare | cut -d'@' -f1 > installed_packages.txt
```

### TextMate Scope & Grammar Definitions

Understanding syntax highlighting scope selectors:

```json
{
  "scopeName": "source.custom-dsl",
  "patterns": [
    {
      "name": "keyword.control.custom-dsl",
      "match": "\\b(if|else|while|return)\\b"
    }
  ]
}
```

## Common Patterns

### Converting Atom Keybindings to VS Code keybindings.json

**Problem**: Retaining hardwired muscle memory for Atom keyboard shortcuts in VS Code.

**Solution**:
Install the official "Atom Keymap" extension in VS Code:

```bash
code --install-extension ms-vscode.atom-keybindings
```

## Best Practices

**Do**:

- Migrate active development workflows from retired Atom to modern actively maintained editors (Zed, VS Code, Pulsar, Neovim).
- Convert `.cson` configuration files and keymaps into standardized `.json` files.
- Use Tree-sitter grammars rather than legacy TextMate regex grammars for syntax parsing.
- Back up legacy snippet libraries to standard snippets directories.

**Don't**:

- Install unverified packages from defunct repositories that no longer receive security patches.
- Use Atom in production or security-critical environments where patched Electron runtimes are required.
- Expect Atom Package Manager (`apm`) registries to be permanently available.

## Troubleshooting

| Error                                             | Cause                                                   | Solution                                                        |
| :------------------------------------------------ | :------------------------------------------------------ | :-------------------------------------------------------------- |
| `apm install fails: EACCES / 404`                 | Atom package registry servers decommissioned by GitHub. | Switch to community fork Pulsar (`pulsar-edit.dev`) or VS Code. |
| `Security vulnerability warning in Electron core` | Obsolete Chromium engine in archived Atom binary.       | Cease running legacy Atom on untrusted source repositories.     |
| `Uncaught Exception in Atom Core`                 | Node.js version incompatibility on modern OS.           | Migrate projects to Zed or modern VS Code.                      |

## References

- [Atom Sunsetting](https://github.blog/2022-06-08-sunsetting-atom/)
