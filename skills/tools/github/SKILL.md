---
name: github
description: GitHub platform features including PRs, Issues, Actions, and collaboration. Use for GitHub workflows.
---

# GitHub

Platform for hosting, collaborating on, and managing code repositories.

## When to Use

- Hosting Git repositories
- Code review with Pull Requests
- Issue tracking and project management
- CI/CD with GitHub Actions

## Quick Start

```bash
# Create repo from CLI
gh repo create my-project --public --source=. --remote=origin --push

# Clone with GitHub CLI
gh repo clone username/repo

# Create PR
gh pr create --title "Add feature" --body "Description"
```

## Core Concepts

### Pull Requests

```bash
# Create PR
gh pr create --base main --head feature/my-feature

# View PRs
gh pr list
gh pr view 123

# Checkout PR locally
gh pr checkout 123

# Merge PR
gh pr merge 123 --squash --delete-branch
```

### Issues & Projects

```bash
# Create issue
gh issue create --title "Bug report" --body "Description"

# List issues
gh issue list --state open --label bug

# Close issue
gh issue close 123 --comment "Fixed in #456"
```

## Common Patterns

### Branch Protection

```yaml
# Settings -> Branches -> Branch protection rules
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date
- Include administrators
```

### CODEOWNERS

```text
# .github/CODEOWNERS
* @default-team
/src/api/ @backend-team
/src/ui/ @frontend-team
*.md @docs-team
```

### Issue Templates

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
description: Report a bug
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear description of the bug
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
```

## Best Practices

**Do**:

- Use branch protection rules
- Create issue/PR templates
- Set up CODEOWNERS
- Enable security features

**Don't**:

- Commit directly to main
- Skip code review
- Ignore dependabot alerts
- Use personal tokens in Actions

## Troubleshooting

| Issue             | Cause          | Solution                    |
| ----------------- | -------------- | --------------------------- |
| PR blocked        | Failed checks  | Fix failing tests           |
| Permission denied | Missing access | Check collaborator settings |
| Action failed     | Config error   | Check workflow syntax       |

## References

- [GitHub Docs](https://docs.github.com)
- [GitHub CLI](https://cli.github.com/)
