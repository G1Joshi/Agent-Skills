---
name: github-actions
description: GitHub Actions CI/CD workflows with reusable actions. Use for GitHub automation.
---

# GitHub Actions

GitHub Actions is the CI/CD platform native to GitHub. In 2025, it is the dominant CI/CD tool, characterized by **Reusable Workflows** and **OIDC** integration for passwordless deployments.

## When to Use

- **GitHub-Hosted**: Your code is already on GitHub. Deep integration with Issues/PRs.
- **Simplicity**: No servers to manage (unlike Jenkins).
- **Marketplace**: Thousands of pre-built actions (setup-node, docker-build-push).

## Quick Start

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: npm ci
      - run: npm test
```

## Core Concepts

### Workflows

Defined in `.github/workflows/*.yml`. Triggered by events (`push`, `release`, `schedule`).

### Runners

Virtual machines (Ubuntu/Windows/MacOS) that run your jobs. You can also host **Self-Hosted Runners** for cheaper/faster builds in your VPC.

### Actions

Reusable steps. `actions/checkout` is an action. You can write your own in JS or Docker.

## Best Practices (2025)

**Do**:

- **Use Reusable Workflows**: Define a standard "Deploy to Prod" workflow in one repo, and call it from 50 microservices.
- **Use OIDC**: Authenticate to AWS/Azure/GCP using `permissions: id-token: write` instead of long-lived secrets.
- **Pin Actions**: Use `actions/checkout@v4` or a specific SHA for immutability.

**Don't**:

- **Don't hardcode secrets**: Use Repository Secrets or Environment Secrets.
- **Don't write huge shell scripts**: If a step is >10 lines of bash, move it to a script file or a custom Action.

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
