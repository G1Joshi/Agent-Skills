---
name: homebrew
description: Homebrew macOS/Linux package manager. Use for system tools.
---

# Homebrew

Homebrew is the standard package manager for macOS. v4.2 (2025) is faster (JSON API) and supports declarative `Brewfile`.

## When to Use

- **macOS Dev Setup**: Installing Node, Python, Git, Docker, Postgres.
- **Casks**: Installing GUI apps (VS Code, Slack, Chrome).
- **Dotfiles**: Automating machine setup.

## Quick Start

```bash
# Install wget
brew install wget

# Install VS Code (Cask)
brew install --cask visual-studio-code
```

## Core Concepts

### Formulae

CLI tools compiled from source (or bottles).

### Casks

macOS native applications (drag-and-drop apps automation).

### Brewfile

Dependency list. `brew bundle` installs everything listed.

## Best Practices (2025)

**Do**:

- **Use Brewfile**: Commit a `Brewfile` to your dotfiles repo. `brew bundle dump` generates it.
- **Cleanup**: `brew cleanup` frees up GBs of old versions.
- **Pin versions**: If you need stability, use `brew pin postgresql@14`.

**Don't**:

- **Don't run as sudo**: Homebrew manages permissions.

## References

- [Homebrew Documentation](https://brew.sh/)
