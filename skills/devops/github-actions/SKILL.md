---
name: github-actions
description: GitHub Actions CI/CD workflows, reusable actions, and deployment automation. Use for GitHub automation.
---

# GitHub Actions

CI/CD automation integrated with GitHub repositories.

## When to Use

- Continuous integration testing
- Automated deployments
- Code quality checks
- Workflow automation

## Quick Start

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"
      - run: npm ci
      - run: npm test
```

## Core Concepts

### Workflow Structure

```yaml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        required: true
        default: "staging"
        type: choice
        options: [staging, production]

env:
  NODE_VERSION: 20

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - uses: actions/checkout@v4

      - name: Get version
        id: version
        run: echo "version=$(node -p "require('./package.json').version")" >> $GITHUB_OUTPUT

      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment || 'staging' }}
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
```

### Matrix Strategy

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        node: [18, 20, 22]
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

## Common Patterns

### Reusable Workflow

```yaml
# .github/workflows/reusable-deploy.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy_token:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - run: echo "Deploying to ${{ inputs.environment }}"
        env:
          TOKEN: ${{ secrets.deploy_token }}

# Calling workflow
jobs:
  deploy:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
    secrets:
      deploy_token: ${{ secrets.DEPLOY_TOKEN }}
```

## Best Practices

**Do**:

- Pin action versions with SHA
- Use environments for deployments
- Cache dependencies
- Use concurrency controls

**Don't**:

- Expose secrets in logs
- Use `pull_request_target` carelessly
- Skip security scanning
- Ignore workflow permissions

## Troubleshooting

| Issue             | Cause               | Solution                  |
| ----------------- | ------------------- | ------------------------- |
| Permission denied | Missing permissions | Add permissions block     |
| Cache miss        | Wrong key           | Check cache key pattern   |
| Secret empty      | Wrong scope         | Check secret availability |

## References

- [GitHub Actions Docs](https://docs.github.com/actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)
