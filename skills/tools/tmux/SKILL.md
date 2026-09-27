---
name: tmux
description: Expert tmux assistance covering terminal multiplexing, session management, window/pane layouts, tmux.conf customization, and scriptable session automation via tmuxp. Use when managing persistent remote sessions, splitting terminal windows, organizing multi-project workflows, or configuring custom keybindings.
---

# Tmux

Tmux decouples your terminal session from the window. Detach, go home, SSH in, attach, and your cursor is exactly where you left it. v3.5 adds extended keys.

## When to Use

- **Terminal Session Persistence**: Keeping background jobs, tests, and servers running across SSH disconnects and laptop restarts.
- **Complex Split-Pane Workspaces**: Organizing multi-window terminals with synchronized panes, log tailing, and editor buffers.
- **Remote Pair Programming**: Sharing a live terminal session with remote teammates over SSH with zero latency.
- **Scripted Environment Automation**: Bootstrapping reproducible development environments using `tmuxinator` or custom bash scripts.

## Quick Start

### 1. Minimal ~/.tmux.conf

```tmux
# Remap prefix from 'C-b' to 'C-a'
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# Split panes using | and -
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# Enable mouse mode & 256 colors
set -g mouse on
set -g default-terminal "tmux-256color"
```

### 2. Session Management

```bash
# Create new session
tmux new -s dev

# List active sessions
tmux ls

# Attach to session
tmux attach -t dev
```

## Core Concepts

### Production Tmux Configuration (`~/.tmux.conf`)

Configuring modern true-color support, mouse navigation, prefix remapping, and Vim-style pane switching:

```text
# ~/.tmux.conf
# Remap prefix from 'C-b' to 'C-a'
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# Quality of Life
set -g mouse on
set -g history-limit 50000
set -g escape-time 0
set -g base-index 1
setw -g pane-base-index 1
set -g renumber-windows on

# True Color Support
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-256color:RGB"

# Vim-style pane navigation
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Split panes using | and -
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# Reload config
bind r source-file ~/.tmux.conf \; display-message "Tmux config reloaded!"
```

### Tmux Plugin Manager (TPM) & Session Persistence

Installing TPM and configuring automatic session restore (`tmux-resurrect` and `tmux-continuum`):

```text
# Add to bottom of ~/.tmux.conf
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'

# Automatic restore on tmux start
set -g @continuum-restore 'on'

run '~/.tmux/plugins/tpm/tpm'
```

### Programmatic Session Bootstrapping Script

Creating a multi-window development workspace automatically:

```bash
#!/usr/bin/env bash
SESSION_NAME="core-api"

# Check if session exists
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
  # Create new detached session
  tmux new-session -d -s $SESSION_NAME -n "editor"
  tmux send-keys -t $SESSION_NAME:1 "nvim ." C-m

  # Window 2: Servers & Logs
  tmux new-window -t $SESSION_NAME:2 -n "services"
  tmux send-keys -t $SESSION_NAME:2 "docker compose up" C-m
  tmux split-window -h -t $SESSION_NAME:2
  tmux send-keys -t $SESSION_NAME:2.2 "npm run dev" C-m

  # Window 3: Terminal / Git
  tmux new-window -t $SESSION_NAME:3 -n "shell"
fi

# Attach to session
tmux attach-session -t $SESSION_NAME
```

## Common Patterns

### Vim-Style Pane Navigation

**Problem**: Navigate between split terminal panes using standard `h`, `j`, `k`, `l` directional keys.  
**Solution**: Bind keys in `~/.tmux.conf`.

```tmux
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Fast resize with capital letters
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5
```

### Automated Workspace Layout with tmuxp

**Problem**: Rebuild a multi-window development layout (server, client, logs) with one command.  
**Solution**: Define YAML workspace file for `tmuxp`.

```yaml
# ~/.tmuxp/myproject.yaml
session_name: myproject
windows:
  - window_name: code
    layout: main-vertical
    panes:
      - nvim
      - git status
  - window_name: server
    panes:
      - npm run dev
      - docker compose logs -f
```

Run `tmuxp load myproject` to restore.

## Best Practices (2026)

- **Do** set `escape-time 0` in `~/.tmux.conf` to eliminate input lag when using Neovim/Vim inside Tmux.
- **Do** enable `renumber-windows on` so window indexes remain sequential (1, 2, 3...) when closing intermediate tabs.
- **Do** leverage **TPM** with `tmux-resurrect` to persist active layouts and terminal state across machine reboots.
- **Do** use `#{pane_current_path}` when splitting panes so new panes open in the current working directory.
- **Don't** leave detached sessions consuming gigabytes of forgotten Docker build or process logs; kill dead sessions with `tmux kill-session`.
- **Don't** configure conflicting hotkeys between Tmux prefix and shell shortcuts (e.g. `C-a` for start of line).
- **Don't** run Tmux inside another nested Tmux session over SSH without adjusting the escape prefix.

## Troubleshooting

| Error / Symptom                                   | Cause                                                       | Solution                                                                                          |
| ------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Terminal colors washed out or italic text broken  | `default-terminal` not supporting true color in tmux        | Add `set-option -ga terminal-overrides ",xterm-256color:Tc"` to `~/.tmux.conf`.                   |
| Mouse copy-paste copies line numbers across panes | Mouse drag copies raw terminal buffer instead of pane text  | Hold `Option` (macOS) / `Shift` (Linux) while selecting, or use tmux vi copy mode (`prefix + [`). |
| `sessions should be nested with care` error       | Attempting to launch tmux from within an existing tmux pane | Detach first (`prefix + d`) or switch session via `prefix + s`.                                   |

## References

- [Tmux Wiki](https://github.com/tmux/tmux/wiki)
