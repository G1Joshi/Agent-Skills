---
name: dependabot
description: Expert Dependabot automated dependency management covering daily/weekly vulnerability alerts, grouped updates, and PR automation. Use when configuring `dependabot.yml`, updating packages, or fixing CVEs.
---

# Dependabot

Dependabot creates pull requests to keep your dependencies secure and up-to-date. It is integrated natively into GitHub.

## When to Use

- **Automated Dependency Updates**: Keeping npm, pip, Maven, Cargo, Go modules, and Docker images updated automatically via GitHub PRs.
- **Security Vulnerability Remediation**: Generating automated pull requests to patch known Common Vulnerabilities and Exposures (CVEs).
- **SemVer-Grouped Pull Requests**: Grouping minor and patch dependency updates into unified PRs to prevent developer review fatigue.
- **Private Package Registry Scanning**: Scanning private npm or NuGet package registries for updates and security patches.

## Quick Start

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

#Declarative dependabot.yml Manifest

Configures ecosystem targets, schedules, directories, and grouping policies:

```yaml
# .github/dependabot.yml
version: 2
updates:
  # Maintain production npm dependencies
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "06:00"
    open-pull-requests-limit: 10
    groups:
      production-dependencies:
        patterns: ["*"]
        update-types: ["minor", "patch"]
  # Track GitHub Actions workflow versions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
```

#Security-Only vs Version-Update Modes

- **Security Updates**: Automatically triggered when a CVE alert is opened in GitHub Advisory Database.
- **Version Updates**: Scheduled cron checks that propose upgrading dependencies to latest stable releases:

```yaml
# Target security vulnerabilities only
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
    # Security updates trigger automatically; version updates restricted:
    open-pull-requests-limit: 0
```

#GitHub Actions Integration with Dependabot Secrets

Injects credentials for private artifactory and npm package registries:

```yaml
registries:
  enterprise-npm:
    type: npm-registry
    url: https://npm.pkg.github.com
    token: ${{ secrets.DEPENDABOT_NPM_TOKEN }}
```

## Common Patterns

### Grouped Security and Minor Updates

**Problem**: Dozens of individual dependency PRs flood repositories and exhaust CI runners.

**Solution**:
Group minor and patch updates together in `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      production-dependencies:
        patterns:
          - "*"
        exclude-patterns:
          - "major"
```

## Best Practices (2026)

**Do**:

- **Enable Grouped Updates**: Use `groups` in `dependabot.yml` to bundle minor/patch bumps into a single reviewable PR.
- **Require Passing CI/CD Status Checks**: Ensure automated test suites pass on Dependabot branches before merging.
- **Use Automated Merge Actions**: Combine Dependabot with GitHub Auto-Merge (`gh pr merge --auto --rebase`) for low-risk patch updates.
- **Pin GitHub Actions to Full Commit SHAs**: Require Dependabot to pin GitHub Actions to immutable SHAs rather than mutable tags.

**Don't**:

- **Don't set daily intervals for all ecosystems**: Daily updates cause PR spam; use weekly or grouped schedules for production dependencies.
- **Don't ignore Dependabot security alerts**: Treat critical security PRs with immediate priority.
- **Don't merge major version bumps without manual regression testing**: Major version upgrades introduce breaking API changes.

## Troubleshooting

| Error             | Cause                              | Solution                                                |
| :---------------- | :--------------------------------- | :------------------------------------------------------ |
| `No PRs created`  | Config error or no updates needed. | Check "Dependabot" tab in Insights -> Dependency Graph. |
| `Merge Conflicts` | Lockfile out of sync.              | Rebase the PR (`@dependabot rebase`).                   |

## References

- [GitHub Dependabot Docs](https://docs.github.com/en/code-security/dependabot)
