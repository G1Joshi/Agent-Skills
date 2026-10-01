---
name: github-actions
description: Expert GitHub Actions assistance covering workflow syntax, matrices, composite actions, caching, environments, and OIDC AWS/GCP auth. Use when building robust CI/CD automation pipelines.
---

# GitHub Actions

GitHub Actions is the CI/CD platform native to GitHub, characterized by Reusable Workflows, matrix builds, and OIDC integration for secure, passwordless cloud deployments.

## When to Use

- **Cloud CI/CD Integrated with GitHub**: Building, testing, and releasing software directly inside GitHub repositories.
- **Automated Pull Request Checks**: Enforcing linting, type-checking, unit tests, and security scans on PR branches.
- **OIDC Cloud Deployments**: Deploying to AWS, Azure, and GCP securely without storing permanent cloud access keys.
- **Matrix Multi-Platform Builds**: Testing packages across OS matrices (Ubuntu, macOS, Windows) and language versions.

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

### Production CI/CD Workflow with Dependency Caching

Comprehensive workflow for testing and publishing:

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Node.js Environment
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: "npm"

      - name: Install Dependencies
        run: npm ci

      - name: Static Analysis & Tests
        run: |
          npm run lint
          npm run typecheck
          npm test -- --coverage

      - name: Upload Test Coverage Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/
```

### OIDC Authentication with Cloud Providers (AWS / GCP)

Deploying securely without long-lived secret keys:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    needs: validate
    if: github.ref == 'refs/heads/main'
    permissions:
      id-token: write # Required for requesting OIDC JWT
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure AWS Credentials via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsDeployRole
          aws-region: us-east-1

      - name: Deploy Infrastructure
        run: |
          aws s3 sync dist/ s3://my-prod-bucket/ --delete
```

### Matrix Builds Across OS and Versions

Testing compatibility across platforms:

```yaml
jobs:
  matrix-test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node-version: [20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

## Common Patterns

### OIDC Authentication with AWS / GCP (Keyless Deployments)

**Problem**: Storing long-lived cloud credentials in GitHub Secrets creates security risks.

**Solution**:
Use GitHub OpenID Connect (OIDC) token exchange:

```yaml
name: Deploy to Production
on:
  push:
    branches: [main]

permissions:
  id-token: write # Required for requesting OIDC JWT token
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubDeployRole
          aws-region: us-east-1
      - run: aws s3 sync ./dist s3://my-prod-bucket
```

## Best Practices

**Do**:

- Pin third-party actions to explicit commit SHAs (or trusted `@v4` releases) to protect against supply chain tampering.
- Use `concurrency` with `cancel-in-progress: true` to abort outdated CI runs on subsequent pushes.
- Authenticate to cloud infrastructure via OIDC (`permissions: id-token: write`) rather than long-lived API keys.
- Restrict workflow permissions explicitly with top-level `permissions` block following least privilege.

**Don't**:

- Use `pull_request_target` without strict sanitization of untrusted code from public repository forks.
- Log sensitive variables or secrets in shell execution steps.
- Run CI without dependency caching (`setup-node`, `setup-python`, `cache-action`); caching cuts runtime in half.

## Troubleshooting

| Error                                                  | Cause                                                                | Solution                                                                |
| :----------------------------------------------------- | :------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `Error: Resource not accessible by integration`        | Workflow missing required permissions block for GITHUB_TOKEN.        | Add explicit `permissions: { contents: write, id-token: write }` block. |
| `Action failed: Node.js 16 actions are deprecated`     | Workflow uses outdated action version relying on Node 16 runner.     | Upgrade action versions to `@v4` (e.g. `actions/checkout@v4`).          |
| `The process '/usr/bin/git' failed with exit code 128` | Submodule checkout or private repository clone missing access token. | Pass personal access token: `with: { token: secrets.GH_PAT }`.          |

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
