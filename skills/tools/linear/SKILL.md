---
name: linear
description: Expert Linear issue tracking assistance covering cycles, projects, triage, keyboard-first workflows, and GraphQL API integration. Use when managing fast software development workflows and bug tracking.
---

# Linear

Linear is the issue tracker that engineers actually like. It is famous for its **keyboard-first** design and speed. 2025 features **AI Prioritization** and **Triage Agents**.

## When to Use

- **High-Velocity Issue Tracking for Engineering Teams**: Fast, keyboard-first issue tracking and project management.
- **Cycles & Project Roadmapping**: Planning 2-week engineering cycles, tracking velocity, and milestones.
- **GitHub & GitLab PR Synchronization**: Automatically moving issues to _In Progress_ on branch creation and _Done_ on PR merge.
- **Linear GraphQL API Automation**: Automating issue creation, triage bots, and metrics collection via GraphQL.

## Quick Start

```bash
# Query Linear GraphQL API for assigned issues
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { assignedIssues(filter: { state: { type: { eq: \"started\" } } }) { nodes { id identifier title } } } }"}'
```

## Core Concepts

#Linear GraphQL API Integration with Python

Querying and creating issues programmatically:

```python
import requests
import os

LINEAR_API_URL = "https://api.linear.app/graphql"
API_KEY = os.environ["LINEAR_API_KEY"]

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

# GraphQL Mutation to create an engineering issue
create_issue_mutation = '''
mutation CreateIssue($teamId: String!, $title: String!, $description: String!) {
  issueCreate(input: {
    teamId: $teamId
    title: $title
    description: $description
    priority: 1 # Urgent
  }) {
    success
    issue {
      id
      identifier
      url
    }
  }
}
'''

variables = {
    "teamId": "TEAM_UUID_HERE",
    "title": "Investigate elevated latency on payment webhook worker",
    "description": "P99 latency spiked above 1200ms following deployment v2026.1.0."
}

res = requests.post(LINEAR_API_URL, json={"query": create_issue_mutation, "variables": variables}, headers=headers)
print("Created Issue:", res.json())
```

#Git Branch & PR Automation Rules

Linking code to Linear issues automatically:

```bash
# Branch naming convention: <username>/<issue-identifier>-<description>
git checkout -b alice/eng-402-checkout-rate-limit

# Commit message linking
git commit -m "fix(checkout): enforce rate limiting on token endpoint (Fixes ENG-402)"
```

Linear automatically moves `ENG-402` to:

- **In Progress** when the branch is pushed.
- **In Review** when a Pull Request is opened.
- **Done** when the Pull Request is merged into `main`.

#Essential Keyboard Shortcuts

Operating Linear with speed:

- `C`: Create new issue.
- `Cmd + K`: Open Command Menu.
- `S`: Change issue state (Todo, In Progress, Done).
- `P`: Change priority (Urgent, High, Medium, Low).
- `A`: Assign issue to team member.

## Common Patterns

#Automated Issue Creation via GraphQL API
**Problem**: Creating Linear tickets automatically from CI/CD alert hooks.  
**Solution**: Execute Linear GraphQL mutation via curl or script.

```bash
curl -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation IssueCreate($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { id title url } } }",
    "variables": {
      "input": {
        "teamId": "TEAM_UUID",
        "title": "Bug: Production CPU Spike",
        "description": "CPU exceeded 90% on api-gateway-pod-3."
      }
    }
  }'
```

## Best Practices (2026)

- **Do** name Git branches using the Linear issue identifier (`eng-102-fix-auth`) to enable automated status synchronization.
- **Do** use Linear's Triage inbox to review and accept incoming bugs and feature requests before backlog addition.
- **Do** set issue estimates (points or t-shirt sizes) to track team velocity across cycles.
- **Do** use the Linear GraphQL API for automated triage bots and Slack integrations.
- **Don't** leave completed issues un-merged or open; link pull requests so status updates automatically.
- **Don't** create massive multi-month tickets; break large epics into distinct sub-issues.
- **Don't** commit `LINEAR_API_KEY` to public repositories.

## Troubleshooting

| Error                                    | Cause                                                                         | Solution                                                              |
| :--------------------------------------- | :---------------------------------------------------------------------------- | :-------------------------------------------------------------------- |
| `GraphQL error: 401 Unauthorized`        | Invalid `LINEAR_API_KEY` or missing scopes.                                   | Generate API key in Linear Settings > API > Personal API Keys.        |
| `GitHub integration not updating issues` | Webhook disconnected or repository not linked in Linear integration settings. | Re-authenticate GitHub integration in Linear Settings > Integrations. |
| `Cycle burndown chart not updating`      | Issues added to cycle without estimate story points.                          | Assign points/estimates to issues in cycle backlog.                   |

## References

- [Linear Documentation](https://linear.app/docs)
