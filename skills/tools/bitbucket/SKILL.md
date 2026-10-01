---
name: bitbucket
description: Expert Atlassian Bitbucket assistance covering Bitbucket Pipelines, pull requests, branch permissions, and Jira integration. Use when managing repositories and CI/CD workflows on Bitbucket Cloud/Server.
---

# Bitbucket

Bitbucket is Atlassian's Git solution. Its superpower is **Jira Integration**.

## When to Use

- **Enterprise Git Hosting with Atlassian Ecosystem**: Tightly integrated Git repositories with Jira Software and Confluence.
- **Bitbucket Pipelines (CI/CD)**: Cloud-native CI/CD defined in `bitbucket-pipelines.yml` without external build servers.
- **Branch Permissions & Merge Checks**: Enforcing minimum approvals, successful builds, and resolved tasks before merging.
- **Bitbucket Cloud REST API v2**: Automating repository provisioning, PR management, and user permissions.

## Quick Start

```yaml
# bitbucket-pipelines.yml
image: node:20

pipelines:
  default:
    - step:
        name: Build and Test
        caches:
          - node
        script:
          - npm ci
          - npm test
```

## Core Concepts

### Declarative CI/CD Pipeline (bitbucket-pipelines.yml)

Automating test, build, and deployment pipelines:

```yaml
# bitbucket-pipelines.yml
image: node:22-alpine

pipelines:
  default:
    - step:
        name: Lint and Unit Tests
        caches:
          - node
        script:
          - npm ci
          - npm run lint
          - npm test -- --coverage
  branches:
    main:
      - step:
          name: Build and Push Container
          services:
            - docker
          caches:
            - docker
          script:
            - export IMAGE_TAG=$BITBUCKET_COMMIT
            - docker build -t myregistry.com/app:$IMAGE_TAG .
            - echo "$REGISTRY_PASSWORD" | docker login -u "$REGISTRY_USER" --password-stdin myregistry.com
            - docker push myregistry.com/app:$IMAGE_TAG
      - step:
          name: Deploy to Production
          deployment: production
          trigger: manual # Requires manual approval in UI
          script:
            - echo "Deploying version $BITBUCKET_COMMIT to production..."
```

### Bitbucket REST API v2 Operations with Curl

Querying pull requests and triggering builds programmatically:

```bash
# Fetch open pull requests using personal access token
curl -s -X GET \
  -H "Authorization: Bearer $BITBUCKET_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.bitbucket.org/2.0/repositories/my-workspace/my-repo/pullrequests?state=OPEN" | jq .
```

### Jira Smart Commits Integration

Transitioning Jira issues and logging time via Git commit messages:

```bash
# Commit message format: <Issue-Key> #<command> [optional comments]
git commit -m "PROJ-1029 #resolve Added rate limiting to billing endpoint"
git commit -m "PROJ-1029 #time 2h 30m #comment Refactored token validation"
```

## Common Patterns

### Deployment Environments with Manual Approval Gates

**Problem**: Continuous delivery deploying to production before QA review.

**Solution**:
Use Bitbucket environment triggers with manual gates:

```yaml
pipelines:
  branches:
    main:
      - step:
          name: Test & Build
          script:
            - npm test
      - step:
          name: Deploy to Staging
          deployment: staging
          script:
            - ./deploy-staging.sh
      - step:
          name: Deploy to Production
          trigger: manual
          deployment: production
          script:
            - ./deploy-prod.sh
```

## Best Practices

**Do**:

- Configure Merge Checks to require successful pipeline builds and minimum reviewer approvals on protected branches.
- Use Repository Variables (masked and secured) for cloud API credentials and deployment tokens.
- Use `deployment: production` steps to track deployment history and rollback status in Jira.
- Leverage Bitbucket Pipeline caches (`caches: - node`, `- docker`) to accelerate build execution.

**Don't**:

- Allow force-pushing (`git push --force`) to `main` or release branches.
- Store plaintext passwords or tokens in `bitbucket-pipelines.yml`.
- Run long deployment steps without explicit `trigger: manual` on production environments.

## Troubleshooting

| Error                                                    | Cause                                                             | Solution                                                            |
| :------------------------------------------------------- | :---------------------------------------------------------------- | :------------------------------------------------------------------ |
| `Configuration error in bitbucket-pipelines.yml`         | Invalid YAML indentation or unsupported pipeline keyword.         | Validate syntax using Bitbucket Pipelines Validator tool.           |
| `Pipeline build step timed out after 120 minutes`        | Long-running test or hanging process exceeded timeout.            | Add `max-time: 30` to step configuration and inspect logs.          |
| `Permission denied (publickey) on git clone in pipeline` | SSH key not added to Bitbucket Repository Settings > Access Keys. | Generate SSH key pair in Pipeline Settings and register public key. |

## References

- [Bitbucket Documentation](https://support.atlassian.com/bitbucket-cloud/)
