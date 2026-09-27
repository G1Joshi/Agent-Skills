---
name: homebrew
description: Expert Homebrew package manager assistance covering formulae, casks, taps, services, and bundle files (Brewfile). Use when managing developer tools and macOS/Linux system dependencies.
---

# Homebrew

Homebrew is the standard package manager for macOS. v4.2 (2025) is faster (JSON API) and supports declarative `Brewfile`.

## When to Use

- **macOS & Linux Developer Environment Setup**: Installing command-line utilities, programming runtimes, and GUI applications.
- **Automating Workstation Provisioning with Brewfile**: Declaring team development environments using `brew bundle`.
- **Authoring Custom Enterprise Formulae & Taps**: Distributing internal CLI tools and binaries via private GitHub taps.
- **System Service Management**: Managing background daemons (PostgreSQL, Redis, Nginx) using `brew services`.

## Quick Start

```bash
# Install wget
brew install wget

# Install VS Code (Cask)
brew install --cask visual-studio-code
```

## Core Concepts

#Declarative Workstation Setup with Brewfile

Specifying developer dependencies for automated bootstrapping:

```ruby
# Brewfile in repository root
tap "homebrew/bundle"
tap "hashicorp/tap"

# CLI Utilities & Runtimes
brew "git"
brew "zsh"
brew "node@22"
brew "python@3.12"
brew "rust"
brew "hashicorp/tap/terraform"
brew "gh"
brew "jq"

# Background Development Daemons
brew "postgresql@16", restart_service: true
brew "redis", restart_service: true

# GUI Applications (macOS Casks)
cask "visual-studio-code"
cask "docker"
cask "raycast"
cask "postman"
```

```bash
# Install all dependencies declared in Brewfile
brew bundle --file=./Brewfile

# Check for unmanaged or missing dependencies
brew bundle check
```

#Authoring a Custom Formula in Ruby

Packaging a CLI tool for distribution via a custom tap:

```ruby
# Formula/mytool.rb
class Mytool < Formula
  desc "Cloud deployment and verification CLI for enterprise platforms"
  homepage "https://github.com/my-org/mytool"
  url "https://github.com/my-org/mytool/releases/download/v1.0.0/mytool-1.0.0.tar.gz"
  sha256 "a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0"
  license "MIT"

  depends_on "node@22"

  def install
    bin.install "bin/mytool"
    prefix.install "lib"
  end

  test do
    assert_match "mytool version 1.0.0", shell_output("#{bin}/mytool --version")
  end
end
```

#Managing Background Services with brew services

Starting and monitoring local services:

```bash
# Start PostgreSQL service in background
brew services start postgresql@16

# Inspect running services status
brew services list

# Stop service
brew services stop postgresql@16
```

## Common Patterns

### Reproducible Developer Machine Setup with Brewfile

**Problem**: Onboarding new developers requires manually running dozens of brew install commands.

**Solution**:
Define team developer tooling in a version-controlled `Brewfile`:

```ruby
# Brewfile
tap "homebrew/bundle"

brew "git"
brew "node@20"
brew "postgresql@16", restart_service: true
brew "gh"

cask "docker"
cask "visual-studio-code"
```

Execute setup: `brew bundle install`

## Best Practices (2026)

- **Do** maintain a `Brewfile` in dotfiles or team repos to make onboarding new engineers reproducible.
- **Do** run `brew update` and `brew upgrade` regularly to receive security patches and updated formulae.
- **Do** pin major versions of runtimes (`brew "node@22"`, `brew "postgresql@16"`) to avoid breaking updates.
- **Do** run `brew doctor` if build links or dependency paths become corrupted.
- **Don't** run `sudo brew ...`; Homebrew is explicitly designed to run as an unprivileged user.
- **Don't** modify files directly inside `/opt/homebrew` or `/usr/local/Homebrew` manually.
- **Don't** leave orphaned dependencies; clean up disk space periodically with `brew cleanup`.

## Troubleshooting

| Error                                                        | Cause                                                           | Solution                                                         |
| :----------------------------------------------------------- | :-------------------------------------------------------------- | :--------------------------------------------------------------- |
| `Error: Your CLT does not support macOS ...`                 | Outdated Xcode Command Line Tools.                              | Reinstall tools: `xcode-select --install` and run `brew doctor`. |
| `Error: Formula '...' is not installed`                      | Attempting to link or start service for uninstalled formula.    | Install formula first: `brew install <formula>`.                 |
| `brew doctor reporting permission warnings in /opt/homebrew` | Files in Homebrew prefix owned by root instead of current user. | Fix ownership: `sudo chown -R $(whoami) $(brew --prefix)/*`.     |

## References

- [Homebrew Documentation](https://brew.sh/)
