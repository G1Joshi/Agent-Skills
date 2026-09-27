---
name: circleci
description: Expert CircleCI assistance covering config.yml, orbs, docker executors, workflows, caching, and parallelism. Use when automating continuous integration and deployment pipelines on CircleCI.
---

# CircleCI

CircleCI is a cloud-native CI/CD platform focused on speed and parallelism. In 2025, **Dynamic Config** and **Orbs** are the key drivers of efficiency.

## When to Use

- **High-Velocity Cloud CI/CD Pipelines**: Automating builds, tests, and deployments with Docker, Machine, and macOS executors.
- **Reusable Pipeline Architecture with Orbs**: Sharing validated workflows using certified CircleCI Orbs (AWS, Slack, Docker).
- **Test Splitting & Parallelism**: Accelerating slow test suites across dozens of concurrent execution containers.
- **Complex Multi-Stage Workflows**: Approval gates, scheduled nightlies, and matrix build pipelines.

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

#Multi-Job Workflow with Caching & Docker Executor

Fast build and test pipeline with dependency caching:

```yaml
version: 2.1

orbs:
  node: circleci/node@6.0.0
  slack: circleci/slack@4.13.0

executors:
  app-executor:
    docker:
      - image: cimg/node:22.0.0
    resource_class: medium

jobs:
  build-and-test:
    executor: app-executor
    steps:
      - checkout
      - restore_cache:
          keys:
            - v1-deps-{{ checksum "package-lock.json" }}
            - v1-deps-
      - run:
          name: Install Dependencies
          command: npm ci
      - save_cache:
          key: v1-deps-{{ checksum "package-lock.json" }}
          paths:
            - ~/.npm
      - run:
          name: Execute Static Analysis & Tests
          command: |
            npm run lint
            npm test -- --coverage
      - store_test_results:
          path: junit.xml
      - store_artifacts:
          path: coverage

workflows:
  build-test-deploy:
    jobs:
      - build-and-test
      - hold-for-approval:
          type: approval
          requires:
            - build-and-test
          filters:
            branches:
              only: main
```

#Test Splitting by Timing for Concurrent Runners

Distributing tests across parallel containers based on historical execution duration:

```yaml
jobs:
  parallel-tests:
    parallelism: 4 # Run across 4 parallel containers
    docker:
      - image: cimg/python:3.12
    steps:
      - checkout
      - run:
          name: Run Split Tests
          command: |
            TEST_FILES=$(circleci tests glob "tests/**/*.py" | circleci tests split --split-by=timings)
            pytest $TEST_FILES --junitxml=test-results/junit.xml
      - store_test_results:
          path: test-results
```

#OIDC Authentication with Cloud Providers

Authenticating to AWS/GCP without permanent secrets:

```yaml
jobs:
  deploy-aws:
    docker:
      - image: cimg/aws:2026.01
    steps:
      - run:
          name: Assume AWS Role via OIDC
          command: |
            # CircleCI OpenID Connect token exchange
            echo "Authenticating via $CIRCLE_OIDC_TOKEN"
```

## Common Patterns

### Caching Dependencies and Docker Layer Caching

**Problem**: Installing npm/cargo dependencies from scratch on every commit inflates CI build duration.

**Solution**:
Use CircleCI cache keys:

```yaml
version: 2.1

jobs:
  build_and_test:
    docker:
      - image: cimg/node:20.10
    steps:
      - checkout
      - restore_cache:
          keys:
            - v1-deps-{{ checksum "package-lock.json" }}
            - v1-deps-
      - run: npm ci
      - save_cache:
          key: v1-deps-{{ checksum "package-lock.json" }}
          paths:
            - ~/.npm
      - run: npm test

workflows:
  build:
    jobs:
      - build_and_test
```

## Best Practices (2026)

- **Do** leverage CircleCI test splitting (`circleci tests split --split-by=timings`) to minimize CI pipeline wall-clock time.
- **Do** use `cimg/*` official convenience images optimized for caching and performance.
- **Do** authenticate to cloud platforms (AWS, GCP, Azure) via OIDC tokens instead of static credentials.
- **Do** store test results with `store_test_results` to view flaky test analytics and trends.
- **Don't** use resource classes larger than needed (`xlarge`); right-size containers to optimize credits.
- **Don't** store unencrypted credentials in repository config files; use Project Environment Variables or Contexts.
- **Don't** re-run entire workflows on minor test failures; use 'Rerun failed tests' functionality.

## Troubleshooting

| Error                                             | Cause                                                                      | Solution                                                      |
| :------------------------------------------------ | :------------------------------------------------------------------------- | :------------------------------------------------------------ |
| `CircleCI config error: Schema validation failed` | YAML syntax error or invalid orb/step parameter in `.circleci/config.yml`. | Validate locally with `circleci config validate`.             |
| `Job exceeded memory limit and was killed`        | Build task exceeded RAM limit of selected resource class.                  | Upgrade resource class: `resource_class: medium+` or `large`. |
| `Cannot find environment variable`                | Context or project environment variable not linked to job.                 | Link context under `workflows.jobs.context` in `config.yml`.  |

## References

- [CircleCI Documentation](https://circleci.com/docs/)
