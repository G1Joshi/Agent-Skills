---
name: git
description: Git version control with branching, rebasing, and advanced workflows. Use for version control.
---

# Git

Distributed version control for source code management.

## When to Use

- Version control for any project
- Collaboration on code
- Code review workflows
- Release management

## Quick Start

```bash
# Initialize and first commit
git init
git add .
git commit -m "Initial commit"

# Clone existing
git clone https://github.com/user/repo.git
cd repo

# Basic workflow
git checkout -b feature/my-feature
git add .
git commit -m "Add feature"
git push -u origin feature/my-feature
```

## Core Concepts

### Branching & Merging

```bash
# Create and switch branch
git checkout -b feature/new-feature
# or
git switch -c feature/new-feature

# Update from main
git fetch origin
git rebase origin/main

# Merge
git checkout main
git merge feature/new-feature

# Delete branch
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

### Interactive Rebase

```bash
# Rebase last 3 commits
git rebase -i HEAD~3

# In editor:
# pick abc123 First commit
# squash def456 Fix typo
# reword ghi789 Add feature

# Abort if needed
git rebase --abort
```

## Common Patterns

### Stashing

```bash
# Save work in progress
git stash
git stash push -m "WIP: feature"

# List stashes
git stash list

# Apply and drop
git stash pop

# Apply specific
git stash apply stash@{1}
```

### Undoing Changes

```bash
# Unstage file
git reset HEAD file.txt

# Discard changes
git checkout -- file.txt
git restore file.txt  # modern

# Amend last commit
git commit --amend -m "New message"

# Reset to commit
git reset --soft HEAD~1  # keep changes staged
git reset --hard HEAD~1  # discard changes
```

### Git Hooks

```bash
# .git/hooks/pre-commit
#!/bin/sh
npm run lint
npm test

# .git/hooks/commit-msg
#!/bin/sh
if ! grep -qE "^(feat|fix|docs|style|refactor|test|chore):" "$1"; then
    echo "Invalid commit message format"
    exit 1
fi
```

## Best Practices

**Do**:

- Write meaningful commit messages
- Keep commits atomic and focused
- Use feature branches
- Rebase before merging

**Don't**:

- Commit secrets or credentials
- Force push to shared branches
- Create giant commits
- Ignore .gitignore

## Troubleshooting

| Issue          | Cause             | Solution                         |
| -------------- | ----------------- | -------------------------------- |
| Merge conflict | Divergent changes | Resolve manually                 |
| Detached HEAD  | Checkout commit   | Create branch or checkout branch |
| Lost commits   | Hard reset        | Use git reflog                   |

## References

- [Pro Git Book](https://git-scm.com/book)
- [Git Documentation](https://git-scm.com/docs)
