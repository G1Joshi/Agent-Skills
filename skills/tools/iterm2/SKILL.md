---
name: iterm2
description: Expert iTerm2 terminal assistance covering split panes, profiles, trigger alerts, tmux integration, and shell integration. Use when optimizing macOS terminal productivity and keyboard navigation.
---

# iTerm2

iTerm2 is an advanced terminal emulator for macOS, providing split panes, tmux integration, robust search, trigger automation, and customizable profiles.

## When to Use

- **Advanced macOS Terminal Emulator**: Multi-pane split terminals, session restoration, and custom profiles.
- **Shell Integration & Semantic Navigation**: Jumping between shell prompts (`Cmd+Up/Down`) and viewing command exit codes.
- **tmux Control Mode Integration (tmux -CC)**: Seamless integration where tmux windows become native iTerm2 tabs.
- **Triggers & Automated Highlights**: Highlighting error keywords, auto-logging passwords, and badges with dynamic status.

## Quick Start

```bash
# Install iTerm2 Shell Integration for advanced prompt markers and status bar
curl -L https://iterm2.com/shell_integration/install_shell_integration.sh | bash
```

Useful Shortcuts:

- `Cmd+D`: Split pane vertically
- `Cmd+Shift+D`: Split pane horizontally
- `Cmd+Option+Arrow`: Navigate between panes
- `Cmd+Shift+Enter`: Maximize active pane

## Core Concepts

### Shell Integration Installation & Benefits

Enabling semantic prompt navigation and status codes:

```bash
# Install iTerm2 shell integration for zsh or bash
curl -L https://iterm2.com/shell_integration/install_shell_integration.sh | zsh

# In ~/.zshrc or ~/.config/fish/config.fish
test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"
```

Features enabled:

- `Cmd + Shift + Up/Down`: Jump directly between prompt commands.
- Colored circle indicator showing command success (blue) or exit failure (red).
- `iterm2_set_user_var`: Inject custom variables into badge or status bar.

### tmux Integration via Control Mode (-CC)

Running remote persistent sessions as native local tabs:

```bash
# Connect to remote server and attach tmux session in control mode
ssh user@server.infra.internal -t "tmux -CC attach || tmux -CC new"
```

iTerm2 renders tmux windows as native tabs and panes with local mouse scrolling and clipboard integration.

### Setting Dynamic Badges and Status Bars

Displaying active AWS profile or Git branch in the terminal background:

```bash
# Function to set iTerm2 badge dynamically
function iterm2_print_badge() {
  printf "\e]1337;SetBadgeFormat=%s\a" $(echo -n "$1" | base64)
}

# In prompt hook:
iterm2_print_badge "PROD | $(git branch --show-current)"
```

## Common Patterns

### Native Tmux Integration with iTerm2 Windows

**Problem**: Traditional tmux requires complex keyboard leader keys that conflict with terminal shortcuts.

**Solution**:
Attach tmux in native iTerm2 control mode:

```bash
# Attach session; iTerm2 converts tmux windows into native GUI tabs
tmux -CC attach -t dev-session
```

## Best Practices

**Do**:

- Install and enable iTerm2 Shell Integration to jump between commands and capture exit statuses.
- Use `tmux -CC` when working over SSH to retain persistent sessions with native macOS UI shortcuts.
- Map Caps Lock to Control or Escape in macOS settings for ergonomic terminal navigation.
- Export iTerm2 profile settings to a shared JSON file or dotfiles repository.

**Don't**:

- Store plain passwords in iTerm2 password manager without system keychain encryption.
- Leave scrollback buffer unlimited on low-memory machines; set buffer to 10,000-50,000 lines.
- Use slow rendering drivers; enable GPU acceleration in **Preferences -> Advanced -> GPU Rendering**.

## Troubleshooting

| Error                                        | Cause                                                | Solution                                                                                               |
| :------------------------------------------- | :--------------------------------------------------- | :----------------------------------------------------------------------------------------------------- |
| `Broken symbols or question marks in prompt` | Powerline/Nerd font missing in terminal profile.     | Install a Nerd Font (e.g. JetBrainsMono Nerd Font) and select in iTerm2 Preferences > Profiles > Text. |
| `Option key not working as Meta/Alt key`     | Option key sends special characters instead of Esc+. | In Preferences > Profiles > Keys, set **Left Option Key to Esc+**.                                     |
| `Terminal bell beep annoying`                | Audio bell enabled by default.                       | In Preferences > Profiles > Terminal, check **Silence bell** or flash screen.                          |

## References

- [iTerm2 Documentation](https://iterm2.com/documentation.html)
