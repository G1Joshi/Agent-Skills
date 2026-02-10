---
name: circleci
description: CircleCI cloud CI/CD platform. Use for continuous integration.
---

# CircleCI

CircleCI is a cloud-native CI/CD platform focused on speed and parallelism. In 2025, **Dynamic Config** and **Orbs** are the key drivers of efficiency.

## When to Use

- **Speed**: Best-in-class caching, test splitting, and parallelism.
- **Complexity**: Dynamic Configuration allows pipelines to change structure based on changed files (Monorepo support).
- **Compliance**: FedRAMP / SOC2 compliance is strong.

## Quick Start

```yaml
# .circleci/config.yml
version: 2.1
orbs:
  node: circleci/node@5.1
jobs:
  build:
    executor: node/default
    steps:
      - checkout
      - node/install-packages:
          pkg-manager: npm
      - run: npm run test

workflows:
  build-and-test:
    jobs:
      - build
```

## Core Concepts

### Orbs

Shareable packages of config. `circleci/aws-s3@3.0` encapsulates 500 lines of bash into one line of YAML.

### Test Splitting

Intelligently divides test files across N parallel nodes to reduce build time from 30m to 3m.

### Dynamic Config (2025)

A setup workflow generates the _real_ workflow. Allows logic like "If only /backend changed, don't run frontend tests".

## Best Practices (2025)

**Do**:

- **Use Dynamic Config**: Essential for monorepos to save credits.
- **Use Contexts**: Securely share secrets across projects (e.g., `AWS_CREDS`).
- **Use `docker` executor**: It is faster than `machine` executor for most tasks.

**Don't**:

- **Don't reinvent the wheel**: Check the Orb Registry before writing custom commands.

## References

- [CircleCI Documentation](https://circleci.com/docs/)
