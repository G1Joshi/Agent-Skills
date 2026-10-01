---
name: lazygit
description: Expert Lazygit terminal UI assistance covering git staging, interactive rebasing, branch management, cherry-picking, and diff inspection. Use when managing Git repositories with keyboard speed.
---

# Lazygit

Lazygit is a TUI for Git. It makes complex operations (interactive rebase, partial staging) accessible via intuitive keyboard shortcuts.

## When to Use

- **Interactive Terminal Git UI**: Fast, keyboard-centric interface for staging, committing, branching, and rebasing.
- **Interactive Rebase & Cherry-Picking**: Squashing, rewording, dropping, and reordering commits visually.
- **Partial Line-by-Line Staging**: Staging specific lines or code hunks within modified files via keybindings.
- **Git Worktree & Submodule Management**: Switching worktrees and managing submodules without memorizing flags.

## Quick Start

```bash
# Launch lazygit inside any Git repository
lazygit

# Key Navigation:
# 1, 2, 3, 4, 5: Jump between Files, Branches, Commits, Stash panels
# Space: Stage/unstage selected file or hunk
# c: Commit staged changes
# P: Push to upstream
# p: Pull from upstream
# r: Interactive rebase on selected commit
```

## Core Concepts

### Core Keybindings & Panel Navigation

Navigating git repository state with single keystrokes:

- `1` through `5`: Jump between panels (`1`: Status, `2`: Files, `3`: Branches, `4`: Commits, `5`: Stash).
- `Space`: Stage/unstage selected file or line.
- `a`: Stage all modified files.
- `c`: Open commit message prompt.
- `P`: Push to remote branch (`p`: Pull from remote).
- `b`: Create or checkout branch.
- `z`: Undo last Git action (uses Git reflog).

### Interactive Rebase & Commit Squashing

Streamlining commit histories visually:

1. Press `4` to navigate to the **Commits** panel.
2. Highlight the base commit before your branch changes.
3. Press `i` to start an interactive rebase.
4. Highlight commits to modify:
   - `s`: Squash into previous commit.
   - `r`: Reword commit message.
   - `d`: Drop commit entirely.
   - `e`: Edit commit contents.
5. Press `m` to open merge / rebase options.

### Custom Commands Configuration (config.yml)

Adding customized workflows to Lazygit:

```yaml
# ~/.config/lazygit/config.yml
gui:
  theme:
    selectedLineBgColor:
      - reverse
  nerdFontsVersion: "3"

customCommands:
  - key: "P"
    command: "git push --force-with-lease origin {{.SelectedLocalBranch.Name}}"
    context: "localBranches"
    description: "Force push with lease safely"
    prompts:
      - type: "confirm"
        title: "Force Push"
        body: "Are you sure you want to force push with lease?"
```

## Common Patterns

### Custom Lazygit Commands

**Problem**: Need one-key git workflow actions (e.g. git standup, prune remote branches).  
**Solution**: Define custom keybindings in `~/.config/lazygit/config.yml`.

```yaml
# ~/.config/lazygit/config.yml
customCommands:
  - key: "P"
    command: "git remote prune origin"
    context: "remotes"
    loadingText: "Pruning stale branches..."
  - key: "b"
    command: 'git branch --merged | grep -v "\*" | xargs -n 1 git branch -d'
    context: "branches"
    prompts:
      - type: "confirm"
        title: "Delete Merged Branches"
        body: "Are you sure you want to delete all merged local branches?"
```

## Best Practices

**Do**:

- Use `v` in the diff panel to enter line-by-line staging mode for atomic commits.
- Use `git push --force-with-lease` rather than raw `--force` when pushing rebased feature branches.
- Press `z` in Lazygit to safely undo accidental rebases or commits using the reflog.
- Configure Nerd Fonts support in `config.yml` for clean file and branch iconography.

**Don't**:

- Perform interactive rebases on shared public branches (`main`, `production`).
- Stage files without reviewing the visual diff panel on the right.
- Leave abandoned rebases in progress; abort with `m -> Abort rebase`.

## Troubleshooting

| Error                                | Cause                                                         | Solution                                                                                    |
| :----------------------------------- | :------------------------------------------------------------ | :------------------------------------------------------------------------------------------ |
| `lazygit: command not found`         | Binary not installed in system PATH.                          | Install via `brew install lazygit` or Linux package manager.                                |
| `Rebase conflict screen in Lazygit`  | Interactive rebase paused due to merge conflict.              | Resolve conflicting files, stage with `Space`, and press `m` to choose "Continue rebase".   |
| `Cannot push: credentials not found` | Git credential helper not configured in terminal environment. | Configure credential cache: `git config --global credential.helper osxkeychain` (or store). |

## References

- [Lazygit GitHub](https://github.com/jesseduffield/lazygit)
