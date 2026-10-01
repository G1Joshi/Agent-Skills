---
name: confluence
description: Expert Atlassian Confluence assistance covering technical documentation, REST APIs, templates, blueprints, and macro management. Use when structuring engineering runbooks, ADRs, and team wikis.
---

# Confluence

Confluence is the wiki for Jira users. It excels at **structured documentation** and deep Jira integration (embedding live Jira tables).

## When to Use

- **Enterprise Technical Documentation**: Centralizing system architecture, engineering runbooks, and design decisions.
- **Automated Documentation Publishing**: Generating Confluence pages from Markdown / CI/CD pipelines via REST API v2.
- **Atlassian Document Format (ADF)**: Creating rich structured documents with code blocks, tables, and callout macros.
- **Jira & Confluence Integration**: Linking engineering requirements to active Jira sprints and issues.

## Quick Start

```bash
# Query Confluence Cloud REST API for page content via curl
curl -X GET "https://mycompany.atlassian.net/wiki/api/v2/pages/{page-id}" \
  -u "developer@example.com:$CONFLUENCE_API_TOKEN" \
  -H "Accept: application/json" | jq '.title, .body.storage.value'
```

## Core Concepts

### Publishing Documentation via Confluence REST API v2

Creating a technical architecture page programmatically using Python:

```python
import requests
import json
import os

url = "https://your-company.atlassian.net/wiki/api/v2/pages"
auth = (os.environ["ATLASSIAN_EMAIL"], os.environ["ATLASSIAN_API_TOKEN"])
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Storage format body (XHTML)
body_content = '''
<p>This document details the production authentication architecture.</p>
<h2>Key Components</h2>
<ul>
  <li>OAuth 2.0 / OpenID Connect Identity Provider</li>
  <li>Stateless RS256 JWT validation at Edge Ingress</li>
</ul>
<ac:structured-macro ac:name="info">
  <ac:rich-text-body>
    <p>All tokens must be signed by the corporate Keycloak realm.</p>
  </ac:rich-text-body>
</ac:structured-macro>
'''

payload = {
    "spaceId": "123456",
    "status": "current",
    "title": "Authentication Architecture Overview (2026)",
    "body": {
        "representation": "storage",
        "value": body_content
    }
}

response = requests.post(url, json=payload, headers=headers, auth=auth)
print(f"Created Page ID: {response.json().get('id')}")
```

### Searching Pages with Confluence Query Language (CQL)

Searching across spaces programmatically:

```bash
# Search for runbooks modified recently
curl -s -u "$ATLASSIAN_EMAIL:$ATLASSIAN_API_TOKEN" \
  "https://your-company.atlassian.net/wiki/rest/api/content/search?cql=space=ENG+and+title~'Runbook'+order+by+lastmodified+desc" | jq .
```

### Architecture Decision Records (ADRs)

Documenting engineering trade-offs in Confluence:

```html
<!-- Standard ADR Layout -->
<h2>Status</h2>
<p>Accepted</p>
<h2>Context</h2>
<p>
  Our monolithic database connection pool frequently exhausted under burst
  traffic.
</p>
<h2>Decision</h2>
<p>Adopted pgBouncer connection pooler in transaction pooling mode.</p>
<h2>Consequences</h2>
<p>
  Sub-millisecond connection times, but session-level prepared statements are
  restricted.
</p>
```

## Common Patterns

### Automated Page Generation via REST API

**Problem**: Manually updating release notes and deployment runbooks is time consuming and error prone.  
**Solution**: Publish documentation updates automatically using the Confluence Cloud API.

```bash
curl -X POST "https://your-domain.atlassian.net/wiki/api/v2/pages" \
  -H "Authorization: Basic $(echo -n 'user@example.com:API_TOKEN' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "spaceId": "123456",
    "status": "current",
    "title": "Release Notes v2.4.0",
    "body": {
      "representation": "storage",
      "value": "<p>Automated build artifacts deployed successfully to production.</p>"
    }
  }'
```

## Best Practices

**Do**:

- Target the modern Confluence REST API v2 for all automated documentation scripts.
- Organize engineering spaces with structured hierarchies (Architecture, Runbooks, ADRs, Postmortems).
- Automate the publication of API documentation and schemas from CI/CD pipelines to Confluence.
- Use scoped Atlassian API tokens with least privilege rather than raw user passwords.

**Don't**:

- Leave obsolete documentation active; archive pages or flag them with deprecation notices.
- Store plain credentials or internal network passwords in Confluence pages.
- Paste unformatted text; use structured macros (Code Block, Info/Warning panels, Tables).

## Troubleshooting

| Error                                       | Cause                                                   | Solution                                                                     |
| :------------------------------------------ | :------------------------------------------------------ | :--------------------------------------------------------------------------- |
| `401 Unauthorized in Confluence API`        | Using standard password instead of Atlassian API Token. | Generate API token at `id.atlassian.com/manage-profile/security/api-tokens`. |
| `403 Forbidden: Content editing restricted` | Page permissions restrict editing to specific groups.   | Request page access permissions from space administrator.                    |
| `Macro failed to render in export`          | Third-party plugin macro incompatible with PDF export.  | Replace dynamic macro with standard markdown or HTML storage format.         |

## References

- [Confluence Documentation](https://support.atlassian.com/confluence-cloud/)
