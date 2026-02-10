---
name: renovate
description: Renovate dependency updates. Use for automated updates.
---

# Renovate

Renovate is the power-user alternative to Dependabot. It runs on any platform (GitHub, GitLab, Bitbucket, Azure) and offers extreme configurability for how and when dependencies are updated.

## When to Use

- **Monorepos**: Handles complex multi-package repos better than Dependabot.
- **Non-GitHub**: If you use GitLab or Bitbucket.
- **Complex Schedules**: "Only update devDependencies on weekends", "Group all React related packages together".
- **Dashboard**: Need a dashboard to see all pending updates.

## Quick Start (`renovate.json`)

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

### Dependency Dashboard

Renovate creates a persistent "Issue" in your repo that acts as a dashboard. You can tick checkboxes to force-retry updates or see what's blocked.

### Presets

Shareable configuration bundles (`config:base`, `group:allNonMajor`).

### Automerge

Renovate's automerge is highly granular. You can automerge only linters, or only patch releases that pass CI.

## Best Practices (2025)

**Do**:

- **Use the Dependency Dashboard**. It's the control center.
- **Group Updates**: E.g., Group all `aws-sdk` packages.
- **Rate Limit**: Set `prHourlyLimit` or `prConcurrentLimit` to avoid DDoSing your CI system.

**Don't**:

- **Don't start with zero config**: The noise will overwhelm you. Start with conservative settings and expand.

## References

- [Renovate Docs](https://docs.renovatebot.com/)
- [Mend Renovate](https://www.mend.io/renovate/)
