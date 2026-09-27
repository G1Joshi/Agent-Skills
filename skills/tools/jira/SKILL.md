---
name: jira
description: Expert Atlassian Jira assistance covering agile boards (Scrum/Kanban), JQL (Jira Query Language), automation rules, and REST APIs. Use when managing software sprints, tracking bugs, and automating project workflows.
---

# Jira Software

Jira is the industry standard for enterprise agile planning. 2025 includes **Atlassian Intelligence** to auto-fill fields and predict sprint completion.

## When to Use

- **Enterprise Agile Project Management**: Sprint planning, backlog grooming, Kanban boards, and issue tracking.
- **Automated Workflow Transitions via API**: Transitioning issues and assigning tasks via Jira REST API v3.
- **Advanced JQL (Jira Query Language)**: Querying issues across projects, sprints, releases, and epics.
- **DevOps Toolchain Integration**: Linking Jira tickets to GitHub PRs, Bitbucket commits, and deployment pipelines.

## Quick Start

```bash
# Search issues via Jira REST API using JQL
curl -X GET "https://mycompany.atlassian.net/rest/api/3/search?jql=project=PROJ+AND+status='In+Progress'+ORDER+BY+created+DESC" \
  -u "dev@example.com:$JIRA_API_TOKEN" \
  -H "Accept: application/json" | jq '.issues[] | {key, summary: .fields.summary}'
```

## Core Concepts

#Querying and Filtering with Advanced JQL

Precise issue queries for engineering metrics:

```text
# High-priority bugs in active sprint assigned to backend team
project = "CORE" AND issuetype = "Bug" AND priority in ("High", "Highest") AND sprint in openSprints() ORDER BY rank ASC

# Issues completed in the last 7 days without resolution notes
project = "CORE" AND status = "Done" AND updated >= -7d AND resolution = Unresolved

# Unassigned tickets blocking the current release
fixVersion = "2026.1.0" AND assignee is EMPTY AND statusCategory != Done
```

#Jira REST API v3 Integration with Python

Creating and transitioning issues programmatically:

```python
import requests
import json
import os

url = "https://your-company.atlassian.net/rest/api/3/issue"
auth = (os.environ["JIRA_EMAIL"], os.environ["JIRA_API_TOKEN"])
headers = {"Accept": "application/json", "Content-Type": "application/json"}

# Create issue with structured Atlassian Document Format (ADF) description
payload = {
    "fields": {
        "project": {"key": "CORE"},
        "summary": "Implement Redis rate limiting on checkout endpoints",
        "issuetype": {"name": "Task"},
        "priority": {"name": "High"},
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "Token-bucket rate limiter must be integrated to prevent checkout abuse."}
                    ]
                }
            ]
        }
    }
}

response = requests.post(url, json=payload, headers=headers, auth=auth)
print("Created Ticket Key:", response.json().get("key"))
```

#Transitioning Issue Status Programmatically

Moving an issue along workflow states:

```bash
# Transition issue to 'In Progress' (transition ID: 21)
curl -s -X POST \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"transition": {"id": "21"}}' \
  "https://your-company.atlassian.net/rest/api/3/issue/CORE-1029/transitions"
```

## Common Patterns

### Advanced JQL Queries for Sprint Health

**Problem**: Identifying high-priority tickets that are at risk of missing sprint completion.

**Solution**:
Use precise JQL filter expressions:

```text
# Stalled high-priority bugs in active sprint
project = "PAYMENTS" AND issuetype in (Bug, Incident)
  AND sprint in openSprints()
  AND status not in (Resolved, Closed)
  AND updated <= -2d
  ORDER BY priority DESC, created ASC
```

## Best Practices (2026)

- **Do** target the Jira Cloud REST API v3 using Atlassian Document Format (ADF) for rich text descriptions.
- **Do** reference Jira ticket keys (`CORE-1029`) in branch names and commit messages for automatic activity linking.
- **Do** save complex JQL queries as shared filters and create custom team dashboard gadgets.
- **Do** use Jira Automation rules to auto-transition issues when pull requests are opened or merged.
- **Don't** leave issues in ambiguous states; close or transition issues promptly to maintain sprint velocity accuracy.
- **Don't** expose Jira API tokens in public repositories; use encrypted environment variables.
- **Don't** create dozens of custom fields that slow down Jira instance indexing and search performance.

## Troubleshooting

| Error                                                       | Cause                                                        | Solution                                                             |
| :---------------------------------------------------------- | :----------------------------------------------------------- | :------------------------------------------------------------------- |
| `401 Unauthorized in Jira REST API`                         | Using Atlassian password instead of API Token.               | Generate token at `id.atlassian.com` and use Basic Auth with email.  |
| `Field '...' cannot be set: Field does not exist on screen` | Custom field missing on the issue type's Create/Edit screen. | Add custom field to issue screen in Jira Project Settings > Screens. |
| `Automation rule execution limit reached`                   | Infinite loop or high-frequency trigger in Jira Automation.  | Check Automation Audit Log and restrict trigger conditions.          |

## References

- [Jira Documentation](https://support.atlassian.com/jira-software-cloud/)
