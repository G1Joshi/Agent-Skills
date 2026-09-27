---
name: gitlab-ci
description: Expert GitLab CI/CD assistance covering .gitlab-ci.yml, stages, artifacts, caching, GitLab Runners, and Auto DevOps. Use when configuring continuous integration and deployment pipelines on GitLab.
---

# GitLab CI/CD

GitLab CI/CD is known for its robust pipeline definition (`.gitlab-ci.yml`) and Auto DevOps capabilities. In 2025, **CI Components** replace legacy templates for modular pipeline composition.

## When to Use

- **Self-Hosted & Enterprise GitOps CI/CD**: Running pipelines within GitLab EE/CE and private runner infrastructures.
- **Container Registry & Helm Package Integration**: Built-in GitLab Container Registry, Package Registry, and Dependency Proxy.
- **Multi-Project & Downstream Pipelines**: Triggering coordinated cross-repository builds in complex enterprise architectures.
- **Dynamic Parent-Child Pipelines**: Generating build steps dynamically at runtime based on modified monorepo paths.

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

#Declarative Pipeline with Stages, Caching & Artifacts

Clean, structured `.gitlab-ci.yml` pipeline:

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

default:
  image: node:22-alpine
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - .npm/

variables:
  npm_config_cache: "$CI_PROJECT_DIR/.npm"

lint:
  stage: lint
  script:
    - npm ci
    - npm run lint
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

test:
  stage: test
  script:
    - npm ci
    - npm test -- --ci --reporters=default --reporters=jest-junit
  artifacts:
    when: always
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

build-container:
  stage: build
  image: docker:27-cli
  services:
    - docker:27-dind
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
    IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

#Monorepo Path Filtering with rules:changes

Executing jobs only when relevant subdirectories are modified:

```yaml
frontend-job:
  stage: test
  script:
    - cd frontend && npm test
  rules:
    - changes:
        - frontend/**/*

backend-job:
  stage: test
  script:
    - cd backend && cargo test
  rules:
    - changes:
        - backend/**/*
```

#Protected Environments & Manual Deployment Gates

Requiring manual approval for production releases:

```yaml
deploy-production:
  stage: deploy
  environment:
    name: production
    url: https://api.example.com
  script:
    - echo "Deploying version $CI_COMMIT_SHA to production cluster"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual # Requires manual trigger in GitLab UI
```

## Common Patterns

### Multi-Stage Pipeline with Artifact Passing and Rule Conditions

**Problem**: Running tests and security scans on draft branches before code is ready for deployment.

**Solution**:
Use `.gitlab-ci.yml` stages with `rules:` conditions:

```yaml
stages:
  - test
  - deploy

run_tests:
  stage: test
  image: node:20-alpine
  script:
    - npm ci
    - npm test
  artifacts:
    when: on_failure
    paths:
      - test-results/

deploy_prod:
  stage: deploy
  image: alpine/k8s:1.28.2
  script:
    - kubectl apply -f k8s/production/
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: manual
```

## Best Practices (2026)

- **Do** use `rules:changes` in monorepos to avoid running redundant jobs when unrelated code is modified.
- **Do** configure GitLab `reports:junit` and `reports:coverage_report` to view test insights in merge requests.
- **Do** use GitLab Dependency Proxy to cache container images from Docker Hub, eliminating rate limit throttling.
- **Do** mark production deploy jobs with `when: manual` and assign them to protected environments with approver policies.
- **Don't** use deprecated `only`/`except` syntax; migrate to modern `rules:` directives.
- **Don't** store plaintext passwords in `.gitlab-ci.yml`; use Masked and Protected CI/CD Variables.
- **Don't** run Docker-in-Docker (`dind`) with privileged flags in shared environments; use Kaniko for rootless builds.

## Troubleshooting

| Error                                                          | Cause                                                              | Solution                                                            |
| :------------------------------------------------------------- | :----------------------------------------------------------------- | :------------------------------------------------------------------ |
| `yaml invalid: jobs:run_tests config key may not be used with` | Incompatible keyword combinations (e.g. `only` used with `rules`). | Migrate legacy `only/except` syntax to modern `rules:` conditions.  |
| `Job failed: execution took longer than ...`                   | Job exceeded runner timeout setting.                               | Increase timeout in project Settings > CI/CD > General pipelines.   |
| `Artifacts not found in downstream job`                        | Artifact expiration reached or `dependencies:` list omitted.       | Explicitly declare `dependencies: [build_job]` in the consumer job. |

## References

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
