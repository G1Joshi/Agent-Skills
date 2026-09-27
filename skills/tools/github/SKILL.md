---
name: github
description: Expert GitHub platform assistance covering pull requests, code reviews, branch protections, releases, and GitHub CLI (gh). Use when managing repositories, automating releases, and collaborating on GitHub.
---

# GitHub (Tool)

Beyond the platform, GitHub provides powerful **CLI tools (`gh`)** and **Desktop** apps that streamline workflows.

## When to Use

- **Global Enterprise Code Collaboration**: Version control, pull request code reviews, releases, and issue management.
- **GitHub CLI (gh) Automation**: Automating pull requests, releases, issue tracking, and secret management from terminal.
- **Repository Governance & Branch Protection**: Enforcing required status checks, signed commits, and CODEOWNERS approvals.
- **GitHub GraphQL & REST APIs**: Programmatically querying repository statistics, events, and enterprise audit logs.

## Quick Start

```bash
# Use GitHub CLI (gh) to create PR with title and body
gh pr create \
  --title "feat: add user authentication" \
  --body "Resolves issue #42. Adds OAuth2 login flow." \
  --base main \
  --web
```

## Core Concepts

#GitHub CLI (gh) Productivity & Scripting

Managing pull requests and releases from terminal:

```bash
# Create pull request with interactive template or flags
gh pr create \
  --title "feat: implement rate limiting on checkout endpoints" \
  --body "Resolves #1029. Adds token-bucket rate limiting via Redis." \
  --reviewer team-lead \
  --assignee @me

# Check PR review status and checks
gh pr status
gh pr checks

# Create signed release with auto-generated changelog notes
gh release create v2026.1.0 \
  --title "Release 2026.1.0" \
  --generate-notes \
  dist/app-v2026.1.0.tar.gz
```

#Repository Governance with CODEOWNERS

Automating code review assignments based on modified file paths:

```text
# .github/CODEOWNERS
# Global fallback reviewers
* @org/core-engineering

# Security critical paths
/.github/workflows/   @org/devops-security
/infrastructure/      @org/cloud-platform
/src/auth/            @org/security-team

# Frontend domain
/apps/web/            @org/frontend-leads
```

#Querying GitHub GraphQL API via gh api

Extracting structured data with GraphQL queries:

```bash
gh api graphql -f query='
  query($owner: String!, $repo: String!) {
    repository(owner: $owner, name: $repo) {
      stargazerCount
      openIssues: issues(states: OPEN) { totalCount }
      pullRequests(states: OPEN, first: 3) {
        nodes { title author { login } }
      }
    }
  }
' -F owner="facebook" -F repo="react" | jq .
```

## Common Patterns

### Automated Release with GitHub CLI and Artifacts

**Problem**: Manually uploading release binaries and drafting release notes in browser.

**Solution**:
Create semantic release with automated notes and binaries via CLI:

```bash
gh release create v1.4.0 \
  ./dist/binary-linux-amd64 \
  ./dist/binary-darwin-arm64 \
  --title "Release v1.4.0" \
  --generate-notes
```

## Best Practices (2026)

- **Do** configure strict Branch Protection or Rulesets on `main` requiring passing CI status checks and peer reviews.
- **Do** maintain a `.github/CODEOWNERS` file to route pull request reviews to domain owners automatically.
- **Do** use GitHub CLI (`gh secret set`) to inject secrets directly into repository or environment secret stores.
- **Do** require GPG/SSH commit signature verification on production repositories.
- **Don't** grant administrative permissions directly to individuals; manage access via GitHub Teams and RBAC.
- **Don't** store long-lived cloud credentials in repository secrets; authenticate via OpenID Connect (OIDC).
- **Don't** allow merge commits on linear history repos; enforce Squash Merge or Rebase Merge.

## Troubleshooting

| Error                                     | Cause                                                               | Solution                                                         |
| :---------------------------------------- | :------------------------------------------------------------------ | :--------------------------------------------------------------- |
| `gh: To authenticate, run: gh auth login` | GitHub CLI token missing or expired.                                | Run `gh auth login` and complete browser authentication.         |
| `Protected branch push rejected`          | Branch protection rule requires PR review or passing status checks. | Open a Pull Request instead of pushing directly to main branch.  |
| `fatal: Authentication failed for ...`    | GitHub removed password authentication for Git operations.          | Use a Personal Access Token (PAT) with `repo` scope or SSH keys. |

## References

- [GitHub CLI Manual](https://cli.github.com/manual/)
