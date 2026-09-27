---
name: gitlab
description: Expert GitLab platform assistance covering Merge Requests, issue boards, package registry, releases, and glab CLI. Use when managing enterprise source control and DevOps workflows on GitLab.
---

# GitLab (Tool)

GitLab's CLI (`glab`) allows interaction with the GitLab instance (Cloud or Self-Managed) directly from the terminal.

## When to Use

- **Complete DevOps Lifecycle Platform**: Single unified platform for Git hosting, CI/CD, issue tracking, and container registry.
- **Self-Managed Private Cloud Deployments**: Running enterprise Git infrastructure with GitLab Dedicated or Omnibus.
- **Merge Request Approval Rules & Compliance**: Enforcing security approval gates, license compliance, and code coverage minimums.
- **GitLab REST API & Webhooks**: Automating repository provisioning, member access, and pipeline triggering.

## Quick Start

```bash
# Create Merge Request using GitLab CLI (glab)
glab mr create \
  --title "feat: implement caching layer" \
  --description "Improves read performance with Redis." \
  --target-branch main \
  --remove-source-branch
```

## Core Concepts

#Managing Merge Requests via GitLab REST API v4

Querying and creating merge requests programmatically:

```bash
# Create a Merge Request with automated labels and assignee
curl -s -X POST \
  -H "PRIVATE-TOKEN: $GITLAB_PERSONAL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "source_branch": "feature/rate-limiting",
    "target_branch": "main",
    "title": "feat: add token bucket rate limiter",
    "remove_source_branch": true,
    "squash": true
  }' \
  "https://gitlab.example.com/api/v4/projects/12345/merge_requests" | jq .
```

#Project Badges & Pipeline Status Tracking

Configuring pipeline status, test coverage, and release version badges:

```markdown
<!-- README.md badges linked to GitLab CI -->

[![pipeline status](https://gitlab.example.com/org/project/badges/main/pipeline.svg)](https://gitlab.example.com/org/project/-/commits/main)
[![coverage report](https://gitlab.example.com/org/project/badges/main/coverage.svg)](https://gitlab.example.com/org/project/-/commits/main)
[![Latest Release](https://gitlab.example.com/org/project/-/badges/release.svg)](https://gitlab.example.com/org/project/-/releases)
```

#Security Approval Policies & Protected Branches

Restricting production branch access:

1. Navigate to **Settings** -> **Repository** -> **Protected Branches**.
2. Set **Allowed to push**: _No one_ (forces all changes through Merge Requests).
3. Set **Allowed to merge**: _Maintainers_.
4. Enable **Require approval from Code Owners** and **Require all conversations to be resolved**.

## Common Patterns

### Generic Package Registry Upload via CI/CD

**Problem**: Distributing versioned build binaries without external artifact repositories.

**Solution**:
Publish binaries directly to GitLab Package Registry in `.gitlab-ci.yml`:

```yaml
upload_binary:
  stage: deploy
  script:
    - 'curl --header "JOB-TOKEN: $CI_JOB_TOKEN" --upload-file bin/app.tar.gz "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/generic/my-app/${CI_COMMIT_TAG}/app.tar.gz"'
  rules:
    - if: $CI_COMMIT_TAG
```

## Best Practices (2026)

- **Do** protect default branches (`main`) by allowing merges only through reviewed Merge Requests.
- **Do** leverage GitLab Container Registry and Dependency Proxy to speed up container caching in pipelines.
- **Do** configure Merge Request approval rules requiring Security and QA approval on sensitive repositories.
- **Do** rotate Personal Access Tokens (PATs) regularly or use short-lived Project Access Tokens.
- **Don't** allow force pushes to protected branches.
- **Don't** store unmasked secrets in CI/CD variables; mark variables as **Protected** and **Masked**.
- **Don't** allow unreviewed commits to bypass CI pipelines.

## Troubleshooting

| Error                                                            | Cause                                                           | Solution                                                               |
| :--------------------------------------------------------------- | :-------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `GitLab: You are not allowed to push code to protected branches` | Direct push attempted on branch protected by repository policy. | Create a feature branch and submit a Merge Request.                    |
| `glab: 401 Unauthorized`                                         | Invalid `GITLAB_TOKEN` personal access token.                   | Run `glab auth login` to refresh access credentials.                   |
| `MR cannot be merged: Merge conflict`                            | Target branch diverged with overlapping changes.                | Rebase locally: `git pull --rebase origin main` and resolve conflicts. |

## References

- [GitLab CLI](https://gitlab.com/gitlab-org/cli)
