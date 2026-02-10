---
name: dependabot
description: Dependabot dependency updates. Use for security updates.
---

# Dependabot

Dependabot creates pull requests to keep your dependencies secure and up-to-date. It is integrated natively into GitHub.

## When to Use

- **GitHub Repos**: It's the default, easiest choice.
- **Security Patches**: "Dependabot alert: Critical severity in lodash".
- **Keeping deps fresh**: Automated weekly version bumps.

## Quick Start (`dependabot.yml`)

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    # Grouping (2025 feature) reduces noise
    groups:
      dependencies:
        patterns:
          - "*"
```

## Core Concepts

### Security Updates

Triggered automatically when GitHub detects a vulnerability in your dependencies (via Dependency Graph). These are distinct from Version Updates.

### Version Updates

Scheduled updates (Daily/Weekly) to newer versions, regardless of vulnerabilities. Driven by `dependabot.yml`.

### Grouped Updates

Combining multiple package updates into a single PR (e.g., "Bump 5 dependencies"). Drastically reduces PR noise.

## Best Practices (2025)

**Do**:

- **Enable Grouping**: Group non-critical updates to avoid "PR Fatigue".
- **Auto-Merge (safely)**: If tests pass and it's a minor/patch update, configure auto-merge to reduce manual review toil.
- **Check Compatibility Scores**: GitHub shows "% of CI runs that passed" for an update. Trust the crowd usage data.

**Don't**:

- **Don't ignore Alerts**: A critical alert usually means an exploit exists.
- **Don't blindly merge Major versions**: They usually contain breaking changes.

## Troubleshooting

| Error             | Cause                              | Solution                                                |
| :---------------- | :--------------------------------- | :------------------------------------------------------ |
| `No PRs created`  | Config error or no updates needed. | Check "Dependabot" tab in Insights -> Dependency Graph. |
| `Merge Conflicts` | Lockfile out of sync.              | Rebase the PR (`@dependabot rebase`).                   |

## References

- [GitHub Dependabot Docs](https://docs.github.com/en/code-security/dependabot)
