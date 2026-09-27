---
name: zsh
description: Expert Zsh assistance covering shell customization, Oh My Zsh plugins, Zinit plugin manager, prompt engineering (Starship/Powerlevel10k), and shell scripting. Use when configuring .zshrc, writing Zsh automation scripts, optimizing shell startup time, or configuring tab-completion.
---

# Zsh

Zsh is the default shell on macOS. It is highly customizable and compatible with Bash.

## When to Use

- **High-Productivity Interactive Shell**: Interactive autocompletion, fuzzy navigation, history search, and branch indicators.
- **Modern CLI Plugin Ecosystem**: Accelerating shell workflows with `zsh-autosuggestions`, `zsh-syntax-highlighting`, and Starship prompt.
- **Robust Shell Scripting**: Authoring POSIX-compatible and Zsh-extended automation scripts with array manipulation and globbing.
- **Enterprise Environment Management**: Managing SDK versions, PATH exports, and aliases across macOS and Linux servers.

## Quick Start

### 1. Minimal ~/.zshrc Setup

```zsh
# History configuration
HISTFILE="$HOME/.zsh_history"
HISTSIZE=50000
SAVEHIST=50000
setopt HIST_IGNORE_DUPS
setopt SHARE_HISTORY

# Key bindings (emacs mode)
bindkey -e

# Autocompletion
autoload -Uz compinit && compinit

# Aliases
alias ll="ls -lah"
alias g="git"
alias gs="git status -sb"
```

### 2. Benchmark Startup Time

```bash
# Profile zsh startup duration
time zsh -i -c exit
```

## Core Concepts

### High-Speed Modern Zshrc (`~/.zshrc`)

Configuring sub-20ms shell startup, smart completion, and history:

```zsh
# ~/.zshrc
# History configuration
HISTFILE="$HOME/.zsh_history"
HISTSIZE=50000
SAVEHIST=50000
setopt EXTENDED_HISTORY
setopt HIST_EXPIRE_DUPS_FIRST
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_VERIFY
setopt SHARE_HISTORY

# Directory navigation options
setopt AUTO_CD
setopt AUTO_PUSHD
setopt PUSHD_IGNORE_DUPS
setopt PUSHD_SILENT

# Fast Completion System (with caching)
autoload -Uz compinit
typeset -i updated_at=$(date +'%j' -r ~/.zcompdump 2>/dev/null || stat -f '%Sm' -t '%j' ~/.zcompdump 2>/dev/null)
if [ $(date +'%j') != $updated_at ]; then
  compinit -i
else
  compinit -C -i
fi

# Modern Keybindings: History search
bindkey -e
bindkey '^[[A' history-search-backward
bindkey '^[[B' history-search-forward

# Initialize Starship Prompt (if installed)
if command -v starship &> /dev/null; then
  eval "$(starship init zsh)"
fi
```

### Lightweight Plugin Loading without Heavy Frameworks

Loading autosuggestions and syntax highlighting directly:

```zsh
# Clone plugins to ~/.zsh/plugins/
# git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/plugins/zsh-autosuggestions
# git clone https://github.com/zsh-users/zsh-syntax-highlighting ~/.zsh/plugins/zsh-syntax-highlighting

source ~/.zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
source ~/.zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# Configure suggestion color
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=8'
```

### Advanced Zsh Globbing & Parameter Expansion

Leveraging recursive globbing and modifiers:

```zsh
# List all TypeScript files modified in the last 24 hours
ls -lh **/*.ts(m-1)

# Delete all empty directories recursively
rmdir -p **/*(/^F) 2>/dev/null

# Select only executable files in bin/
chmod +x bin/*(*)
```

## Common Patterns

### High-Speed Plugin Loading with Zinit

**Problem**: Oh My Zsh startup takes hundreds of milliseconds due to heavy eager loading.  
**Solution**: Use Zinit with turbo mode (deferred loading).

```zsh
# Install Zinit if missing
source ~/.local/share/zinit/zinit.git/zinit.zsh

# Turbo load syntax highlighting and autosuggestions asynchronously
zinit wait lucid for \
  atinit"ZINIT[COMPINIT_OPTS]=-C; zicompinit; zicdreplay" \
    zdharma-continuum/fast-syntax-highlighting \
  atload"_zsh_autosuggest_start" \
    zsh-users/zsh-autosuggestions \
  blockf \
    zsh-users/zsh-completions
```

### Robust Shell Scripting Functions

**Problem**: Write reusable shell functions with option parsing and error handling.  
**Solution**: Use standard Zsh parameter expansions.

```zsh
# mkcd: Create directory and cd into it
mkcd() {
  if [[ -z "$1" ]]; then
    echo "Usage: mkcd <dir>" >&2
    return 1
  fi
  mkdir -p "$1" && cd "$1"
}
```

## Best Practices (2026)

- **Do** compile `~/.zcompdump` into a byte-compiled file (`compdump.zwc`) to accelerate shell startup time.
- **Do** set `setopt SHARE_HISTORY` to synchronize command history across all active terminal tabs.
- **Do** use **Starship** or a lean native prompt rather than bloated legacy prompt themes.
- **Do** profile startup latency using `zmodload zsh/zprof` at top and bottom of `~/.zshrc`.
- **Don't** use heavy, bloated framework configurations (monolithic Oh-My-Zsh configurations) with dozens of unneeded plugins.
- **Don't** store plaintext cloud credentials, API tokens, or secrets in `~/.zshrc`; use private `.env` files or secret vaults.
- **Don't** run slow external commands (`nvm`, `brew doctor`) synchronously on every interactive shell launch.

## Troubleshooting

| Error / Symptom                                      | Cause                                                                           | Solution                                                                                                  |
| ---------------------------------------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `zsh: command not found: ...` after editing `.zshrc` | Syntax error in `.zshrc` or `$PATH` assignment overwritten instead of prepended | Prepend paths properly: `export PATH="$HOME/bin:$PATH"` and run `source ~/.zshrc`.                        |
| `zsh compinit: insecure directories, run compaudit`  | Insecure file permissions on `/usr/local/share/zsh`                             | Run `compaudit                                                                                            | xargs chmod g-w,o-w` to fix directory permissions. |
| Zsh starts very slowly (> 500ms)                     | Synchronous `nvm` or heavy plugin initialization                                | Use lazy loading for `nvm` or profile with `zmodload zsh/zprof` at top of `.zshrc` and `zprof` at bottom. |

## References

- [Zsh Documentation](https://zsh.sourceforge.io/Doc/Release/index.html)
