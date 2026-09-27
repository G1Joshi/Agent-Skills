---
name: tig
description: Expert Tig assistance covering text-mode interface for Git, interactive staging, commit graph visualization, diff exploration, and blame navigation. Use when navigating Git commit history in the terminal, staging hunks interactively, browsing file changes, or reviewing revisions.
---

# Tig

Tig is an ncurses-based text-mode interface for git. It functions mainly as a Git repository browser.

## When to Use

- **Terminal-Based Git History Navigation**: Browsing commit graphs, branches, and tags rapidly in headless server environments.
- **Interactive Staging & Chunk Commits**: Reviewing diffs, staging hunks, and reverting unstaged lines without leaving the terminal.
- **Blame & Annotate Code**: Inspecting commit authors, timestamps, and commit logs per line of code (`tig blame`).
- **Low-Overhead Git Auditing**: Auditing large enterprise git repositories over SSH connections with zero GUI lag.

## Quick Start

### 1. Common Invocations

```bash
# Open main branch commit graph
tig

# View history of specific file
tig path/to/file.ts

# View diff of uncommitted changes (Status view)
tig status

# Interactive blame view
tig blame path/to/file.ts
```

### 2. Essential Navigation Keys

- `m`: Switch to Main (commit graph) view
- `s`: Switch to Status (staging) view
- `d`: View Diff of selected commit
- `b`: Blame view
- `u`: Stage / unstage selected file or diff hunk
- `q`: Close active view / Quit

## Core Concepts

### Production Tig Configuration (`~/.tigrc`)

Customizing colors, keybindings, and view layouts:

```text
# ~/.tigrc
# General settings
set line-graphics = utf-8
set tab-size = 2
set main-view = id date:relative author:email-user commit-title:graph=yes,refs=yes
set diff-view = line-number:yes,interval=5
set status-view = line-number:yes

# Keybindings: Vim navigation
bind generic j move-down
bind generic k move-up
bind generic g move-first-line
bind generic G move-last-line
bind generic <Ctrl-f> page-down
bind generic <Ctrl-b> page-up

# Fast Actions
bind main <Enter> view-diff
bind status u stage-update
bind status s stage-update
bind status c !git commit -v
```

### Interactive Stage View & Hunk Staging

Navigating the Status View to review and stage changes:

```bash
# Open Tig directly in status mode
tig status

# Keys in Status View:
# - Press 'u' to stage/unstage a file or hunk
# - Press 'Enter' to open diff view of the selected file
# - Press '1' to stage individual line
# - Press 'c' to open editor and create a commit
```

### Investigating Regressions with `tig blame`

Tracing line modifications through repository history:

```bash
# Launch interactive blame viewer for a specific file
tig blame src/auth/jwt_validator.go

# Navigation in Blame View:
# - Press 'Enter' on any line to view the full commit diff that introduced it
# - Press ',' to blame the parent commit before that change
# - Press 'q' to return to previous view
```

## Common Patterns

#Custom Tig Keybindings (~/.tigrc)
**Problem**: Quick terminal staging, rebasing, and branch checkout.  
**Solution**: Define custom hotkeys in `~/.tigrc`.

```ini
# ~/.tigrc
# Bind 'F' to fetch from origin
bind generic F !git fetch origin

# Bind 'C' in status view to fast-commit
bind status C !git commit -v

# Bind 'P' to push current branch
bind generic P !git push origin HEAD
```

## Best Practices (2026)

- **Do** configure `main-view` in `~/.tigrc` with `commit-title:graph=yes,refs=yes` to display clear branch hierarchies.
- **Do** use `tig blame` to quickly discover which PR or commit introduced a breaking line of code.
- **Do** utilize `tig status` to review and stage individual line hunks (`1`) for granular, clean git commits.
- **Do** remap default navigation keys to `j`/`k` in `.tigrc` if accustomed to Vim keybindings.
- **Don't** leave unresolved merge conflicts open in Tig; use Tig to view the conflict status and resolve in your editor.
- **Don't** run heavy full-history Tig views on multi-gigabyte repositories without specifying branch or path limits.
- **Don't** forget to press `q` to ascend up the view hierarchy without killing the session.

## Troubleshooting

| Error / Symptom                        | Cause                                                           | Solution                                                                      |
| -------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Colors hard to read in terminal        | Terminal theme contrast clash with default Tig palette          | Configure custom colors in `~/.tigrc` (e.g. `color diff-stat green default`). |
| Tig opens in wrong git repository root | Current working directory is inside a submodule or outside repo | Check `git rev-parse --show-toplevel` before invoking `tig`.                  |
| `cannot open file: ...` on blame view  | File was renamed or deleted in working tree                     | Pass commit ref explicitly: `tig blame HEAD~2 -- path/to/file`.               |

## References

- [Tig Documentation](https://jonas.github.io/tig/)
