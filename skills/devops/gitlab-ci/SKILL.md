---
name: gitlab-ci
description: GitLab CI/CD pipelines with runners and stages. Use for GitLab automation.
---

# GitLab CI/CD

GitLab CI/CD is known for its robust pipeline definition (`.gitlab-ci.yml`) and Auto DevOps capabilities. In 2025, **CI Components** replace legacy templates for modular pipeline composition.

## When to Use

- **GitLab Users**: It's integrated and excellent.
- **Complex Pipelines**: The DAG (Directed Acyclic Graph) capabilities are sophisticated (`needs` keyword).
- **On-Prem**: Excellent support for air-gapped instances.

## Quick Start

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test

build-job:
  stage: build
  image: node:20
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/

test-job:
  stage: test
  image: node:20
  script:
    - npm test
  needs: [build-job]
```

## Core Concepts

### `.gitlab-ci.yml`

The heart of the pipeline. Defines stages, jobs, and environment variables.

### Runners

The agents that run jobs. Unique feature: **Docker-in-Docker** support is first-class (using `services: docker:dind`).

### CI Components (2025)

Reusable pipeline parts listed in the CI Catalog. Replaces the old `include: template` method with versioned, input-driven components.

## Best Practices (2025)

**Do**:

- **Use CI Components**: Adopt the module catalog.
- **Use `rules`**: Control when jobs run (e.g., only on Merge Requests, or only when `package.json` changes).
- **Use `cache` vs `artifacts`**: Use `cache` for dependencies (node_modules) and `artifacts` for output binaries passed between stages.

**Don't**:

- **Don't use `only`/`except`**: They are deprecated. Use `rules`.

## References

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
