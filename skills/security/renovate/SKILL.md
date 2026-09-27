---
name: renovate
description: Expert Renovate Bot dependency automation covering schedule presets, monorepo package grouping, and auto-merging. Use when configuring `renovate.json`, updating dependencies, or automating security patch management.
---

# Renovate

Renovate is the power-user alternative to Dependabot. It runs on any platform (GitHub, GitLab, Bitbucket, Azure) and offers extreme configurability for how and when dependencies are updated.

## When to Use

- **Multi-Platform Automated Dependency Maintenance**: Keeping dependencies updated across GitHub, GitLab, Bitbucket, and Azure DevOps.
- **Highly Configurable Update Automation**: Customizing update schedules, branch names, commit messages, and package grouping rules.
- **Monorepo Package Synchronization**: Updating interdependent packages across pnpm, Yarn, Cargo, Go, and Helm monorepo workspaces.
- **Automated Merge for Safe Updates**: Automatically rebasing and merging passing patch and minor dependency updates.

## Quick Start

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:base"],
  "packageRules": [
    {
      "matchPackagePatterns": ["^react", "^@types/react"],
      "groupName": "react monorepo"
    },
    {
      "matchUpdateTypes": ["minor", "patch"],
      "matchCurrentVersion": "!/^0/",
      "automerge": true
    }
  ]
}
```

## Core Concepts

#Declarative renovate.json Configuration

Centralizes dependency rules, schedules, and automation policies:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "timezone": "America/New_York",
  "schedule": ["before 6am on monday"],
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch", "pin", "digest"],
      "automerge": true,
      "automergeType": "branch"
    },
    {
      "matchPackageNames": ["react", "react-dom"],
      "groupName": "React core"
    }
  ]
}
```

#Automated Package Grouping & Monorepo Co-Updates

Groups related dependencies (e.g. all `@aws-sdk/*` or all ESLint plugins) into a single unified pull request:

```json
{
  "packageRules": [
    {
      "matchPackagePatterns": ["^@aws-sdk/"],
      "groupName": "AWS SDK monorepo"
    }
  ]
}
```

#Regex Managers for Non-Standard Files

Updates dependency versions declared inside custom shell scripts or Docker compose files:

```json
{
  "customManagers": [
    {
      "customType": "regex",
      "fileMatch": ["^Dockerfile$"],
      "matchStrings": ["ENV NODE_VERSION=(?<currentValue>.*?)\n"],
      "depNameTemplate": "nodejs/node",
      "datasourceTemplate": "github-releases"
    }
  ]
}
```

## Common Patterns

### Monorepo Grouping with Auto-Merge for Minor Patches

**Problem**: Multiple sub-packages in a monorepo trigger dozens of separate PRs that create merge conflicts.

**Solution**:
Configure `renovate.json` to group related packages and auto-merge safe patches:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "matchCurrentVersion": "!/^0/",
      "automerge": true,
      "automergeType": "branch"
    },
    {
      "groupName": "tailwind monorepo",
      "matchPackagePrefixes": ["@tailwindcss/", "tailwindcss"]
    }
  ]
}
```

## Best Practices (2026)

**Do**:

- **Enable Dependency Dashboard**: Keep `"dependencyDashboard": true` active to monitor upcoming PRs and trigger manual updates.
- **Automerge Safe Minor & Patch Updates**: Save engineering time by auto-merging updates that pass full CI/CD test suites.
- **Group Related Packages**: Bundle framework ecosystem packages (`vitest`, `@vitest/*`) into unified PRs.
- **Throttle Concurrent PRs**: Set `"prConcurrentLimit": 5` to prevent overwhelming CI runners with dozens of build jobs.

**Don't**:

- **Don't auto-merge major version updates**: Major releases contain breaking changes that require human code review and testing.
- **Don't run Renovate without robust CI/CD**: Automerging without thorough automated test suites introduces production regressions.
- **Don't hardcode host secrets in repository configs**: Use encrypted host rules or platform environment variables.

## Troubleshooting

| Error                                        | Cause                                                        | Solution                                                                    |
| :------------------------------------------- | :----------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `Renovate configuration error: invalid JSON` | Syntax error or unrecognized preset name in `renovate.json`. | Run `npx renovate-config-validator` locally to validate schema.             |
| `Automerge failing on GitHub PR`             | Branch protection rules require approvals or signed commits. | Configure Renovate GitHub App with auto-merge permissions and sign commits. |
| `PR rate limit reached`                      | Renovate creating too many concurrent PRs.                   | Configure `prConcurrentLimit: 10` and `prHourlyLimit: 2` in configuration.  |

## References

- [Renovate Docs](https://docs.renovatebot.com/)
- [Mend Renovate](https://www.mend.io/renovate/)
