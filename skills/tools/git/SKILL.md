---
name: git
description: Expert Git version control assistance covering branching, interactive rebase, cherry-pick, submodules, worktrees, and conflict resolution. Use when managing source code history and collaboration workflows.
---

# Git

Git is the foundation of modern software. In 2025, features like **Sparse Checkout** and **Scalar** (for monorepos) are becoming mainstream.

## When to Use

- **Branching & Collaboration**: Managing feature isolation, pull requests, trunk-based development, and code reviews across distributed teams.
- **History Rewriting & Cleanup**: Linearizing commit graphs, squashing WIP commits, and editing messages via `git rebase -i` before merging into mainline branches.
- **Automated Bug Hunting**: Isolating regression-introducing commits across thousands of revisions via binary search using `git bisect`.
- **Concurrent Workspace Contexts**: Working on urgent hotfixes without stashing or branching context switching using `git worktree`.
- **Large Repository Scaling**: Optimizing performance in massive monorepos using Git Sparse Checkout, Scalar, and shallow clones.

## Quick Start

```bash
# Clone repository and create a new feature branch
git clone https://github.com/myorg/project.git
cd project

# Create and switch to new branch using modern command
git switch -c feature/auth-flow

# Stage, commit, and push with upstream tracking
git add .
git commit -m "feat(auth): implement oauth2 authorization code flow"
git push -u origin feature/auth-flow
```

## Core Concepts

### The 3-Tree Architecture (Working Tree, Index, HEAD)

Git manages files across three distinct states rather than simply tracking changes between revisions:

```bash
# 1. Working Tree: Modified uncommitted files in your editor
echo "export const API_URL = 'https://api.v2.internal';" >> config.ts

# 2. Index (Staging Area): Content prepped for the next commit
git add config.ts

# 3. HEAD: The last committed snapshot on the active branch
git diff --staged  # Inspect difference between Staging and HEAD
git commit -m "chore(config): update internal API endpoint"
```

### Directed Acyclic Graph (DAG) and Immutable Objects

Every commit in Git is an immutable node pointing to parent hashes and a root tree of blob snapshots.

```bash
# Inspect the raw object behind any commit hash or HEAD
git cat-file -p HEAD
# Output:
# tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904
# parent 8f3d1e1c3a628a58a98b47cf7d12a9e32049e712
# author Alice <alice@example.com> 1727420400 +0000
# committer Alice <alice@example.com> 1727420400 +0000
#
# feat(auth): implement oauth2 authorization code flow
```

### Modern Branch Navigation (`git switch` vs `git restore`)

Modern Git disambiguates the overloaded `git checkout` command into dedicated operations:

```bash
# Branch Switching (replaces git checkout <branch>)
git switch main
git switch -c feature/payments   # Create and switch

# File Restoration (replaces git checkout -- <file>)
git restore src/app.ts           # Discard uncommitted working directory changes
git restore --staged src/app.ts  # Unstage file from index back to working tree
```

### Rebase vs Merge Strategies

- **Merge (`git merge <branch>`)**: Preserves complete historical context with a two-parent merge commit. Ideal for integrating long-lived release branches.
- **Rebase (`git rebase <upstream>`)**: Replays topic commits linearly on top of upstream HEAD, preventing tangled "railroad track" graphs. Ideal for cleaning feature branches prior to PR review.

```bash
# Rebase feature branch onto latest main cleanly
git switch feature/auth-flow
git fetch origin main
git rebase origin/main
```

## Common Patterns

### Multi-Branch Development with Git Worktrees

**Problem**: Stashing uncommitted work to switch branches to fix an urgent production bug.

**Solution**:
Check out multiple branches into separate directories simultaneously:

```bash
# Create parallel worktree folder for hotfix branch
git worktree add ../hotfix-branch main

# Work on hotfix in separate directory without touching current workspace
cd ../hotfix-branch
git commit -am "fix: patch critical auth vulnerability"
git push origin hotfix-branch

# Clean up worktree when finished
cd ../project
git worktree remove ../hotfix-branch
```

### Interactive Rebase for Clean Pull Request History

**Problem**: Feature branch contains dozens of messy "WIP", "fix typo", or "checkpoint" commits.  
**Solution**: Squash and clean history interactively before opening a pull request.

```bash
# Rebase the last 4 commits interactively
git rebase -i HEAD~4

# In interactive editor:
# pick 8f3d1e1 feat(auth): add token generation
# squash 4b825dc fix typo in token payload
# squash a1c94e2 add missing import
# reword 91f7a02 feat(auth): add refresh token endpoint
```

### Automated Regression Hunting with Git Bisect

**Problem**: A bug was introduced somewhere across 500 commits, but the exact commit is unknown.  
**Solution**: Run binary search with automated test execution script.

```bash
# Start bisect session
git bisect start
git bisect bad HEAD                  # Current HEAD is broken
git bisect good v2.1.0               # v2.1.0 was known working

# Automatically run test script on each bisect step
git bisect run npm test -- --runInBand

# Git terminates at the exact first commit that broke the test suite
git bisect reset
```

## Best Practices (2026)

**Do**:

- **Use `git switch` and `git restore`**: Avoid overloaded `git checkout` to prevent accidental branch switches or file overwrites.
- **Push with `--force-with-lease`**: Protect against overwriting colleagues' commits on remote branches.
- **Enable Background Maintenance**: Run `git maintenance start` to optimize packfiles, commit graphs, and fetch performance.
- **Sign Commits with SSH / GPG**: Guarantee authenticity of commit authorship in production pipelines.
- **Write Conventional Commits**: Use standardized prefixes (`feat:`, `fix:`, `chore:`, `refactor:`) to automate semantic versioning and changelogs.

**Don't**:

- **Don't force push to protected branches**: Never rewrite history on `main`, `master`, or shared release branches.
- **Don't commit secrets or credentials**: Use `.gitignore` and git-secrets/trufflehog; once committed, credentials persist in packfile blobs even if deleted later.
- **Don't use huge binary files directly**: Store large model weights or media in Git LFS (Large File Storage) or S3.
- **Don't merge dirty working trees**: Stash or commit changes before pulling or rebasing to avoid accidental file conflicts.

## Troubleshooting

| Error                                          | Cause                                                                           | Solution                                                                            |
| :--------------------------------------------- | :------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------- |
| `fatal: refusing to merge unrelated histories` | Pulling from a repository initialized independently without shared root commit. | Run `git pull origin main --allow-unrelated-histories`.                             |
| `HEAD detached at ...`                         | Checked out a specific commit hash rather than a branch name.                   | Create branch from current position: `git switch -c recovery-branch`.               |
| `Merge conflict in file.txt`                   | Concurrent commits modified identical lines in opposing branches.               | Resolve conflict markers (`<<<<<<<`), stage file (`git add`), and run `git commit`. |

## References

- [Git Documentation](https://git-scm.com/doc)
