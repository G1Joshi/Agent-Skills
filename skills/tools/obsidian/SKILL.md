---
name: obsidian
description: Expert Obsidian assistance covering local markdown knowledge bases, frontmatter YAML schema, Dataview plugin queries, Canvas workflows, and community plugin automation. Use when structuring Obsidian vaults, writing DataviewJS queries, configuring sync workflows, or designing second-brain systems.
---

# Obsidian

Obsidian is a powerful knowledge base that operates on local plain-text Markdown files, featuring bi-directional linking, dynamic graph visualization, and extensive plugin ecosystems.

## When to Use

- **Local-First Knowledge Management**: Building a future-proof, plain Markdown personal wiki with bi-directional wikilinks.
- **Engineering Runbooks & Architecture Notes**: Maintaining searchable, Git-versioned documentation within source repositories.
- **Dataview Query Automation**: Generating dynamic indexes, project dashboards, and metadata tables across Markdown vaults.
- **Canvas Visual Systems Design**: Mapping distributed systems architectures and database schemas visually.

## Quick Start

### 1. Document Frontmatter Schema

```markdown
---
id: 2026-09-27-eng-sync
title: "Engineering Sync"
tags: [meeting, architecture]
attendees: ["[[Alice]]", "[[Bob]]"]
status: in-progress
created: 2026-09-27
---

# Engineering Sync

Discussing core distributed cache invalidation strategies.
See [[Architecture RFC 042]].
```

### 2. Basic Dataview Table Query

```dataview
TABLE status, created, attendees
FROM #meeting
WHERE status != "done"
SORT created DESC
```

## Core Concepts

### YAML Frontmatter & Dataview Query Language (DQL)

Structuring notes with metadata and querying them dynamically:

```markdown
---
title: Auth Service Architecture
type: architecture-decision-record
status: approved
created: 2026-03-15
tags:
  - backend
  - security
  - auth
author: Engineering Team
---

# Architecture Decision Record: Auth Service

## Context

Migrating from session cookies to stateless JWT verification.
```

Dynamic Dataview index query block in an index note:

```dataview
TABLE status AS "Status", author AS "Author", created AS "Created Date"
FROM #backend AND #security
WHERE status = "approved"
SORT created DESC
```

### DataviewJS for Advanced Dynamic Visualizations

Querying vault notes programmatically with JavaScript:

```javascript
const adrs = dv
  .pages("#backend")
  .where((p) => p.type === "architecture-decision-record")
  .sort((p) => p.created, "desc");

dv.table(
  ["Decision Title", "Status", "Tags"],
  adrs.map((p) => [p.file.link, p.status, p.file.tags.join(", ")]),
);
```

### Git-Backed Vault Synchronization

Automating backup, branching, and team collaboration on Markdown vaults:

```bash
# Initialize vault as a Git repository
cd ~/Documents/ObsidianVault
git init
git remote add origin git@github.com:my-org/engineering-vault.git

# Recommended .gitignore for Obsidian
cat << 'EOF' > .gitignore
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.trash/
.DS_Store
EOF

git add .
git commit -m "feat: initialize engineering markdown vault"
git push -u origin main
```

## Common Patterns

### DataviewJS Dynamic Task Aggregator

**Problem**: Aggregate open tasks across all project notes grouped by category.

**Solution**:
Write a DataviewJS script inside a code block:

```javascript
const pages = dv.pages("#project").where((p) => p.file.tasks.length > 0);

for (let group of pages.groupBy((p) => p.category)) {
  dv.header(3, group.key || "Uncategorized");
  dv.taskList(group.rows.file.tasks.where((t) => !t.completed));
}
```

### Git-Backed Automated Vault Sync

**Problem**: Keep markdown vault synchronized across desktop and mobile machines without proprietary cloud locks.

**Solution**:
Configure Obsidian Git community plugin or automated cron script:

```bash
#!/bin/bash
# sync_vault.sh
cd ~/Documents/ObsidianVault
git add -A
git commit -m "vault backup $(date '+%Y-%m-%d %H:%M:%S')"
git pull --rebase origin main
git push origin main
```

## Best Practices

**Do**:

- Use strict Wikilinks (`[[Note Name]]`) or Standard Markdown links (`[Title](note.md)`) consistently across the vault.
- Structure notes using standardized YAML frontmatter (`tags`, `date`, `status`, `aliases`) for reliable querying.
- Ignore `.obsidian/workspace.json` in `.gitignore` to prevent git conflict churn when syncing across machines.
- Leverage **Obsidian Canvas** (`.canvas` files) for interactive architecture and workflow diagrams.

**Don't**:

- Rely on proprietary plugins that alter raw markdown into non-portable custom syntax.
- Store large binary assets or videos directly in the Git vault; store them in cloud object storage (S3) and link them.
- Create deeply nested folder structures; favor atomic notes connected via bi-directional links and tags.

## Troubleshooting

| Error                                                | Cause                                                          | Solution                                                                                                    |
| ---------------------------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `Dataview: Evaluation Error`                         | Field syntax mismatch or accessing undefined object properties | Use defensive checks `p.category ?? "None"` and verify frontmatter YAML syntax with no unquoted colons.     |
| Broken wikilink `[[Note]]`                           | Note renamed outside Obsidian without updating file links      | Rename files inside Obsidian GUI so automatic internal link updater triggers across the vault.              |
| Sync merge conflicts in `.obsidian/` workspace cache | Workspace layout state JSON files committed directly to Git    | Add `.obsidian/workspace*` to `.gitignore` while committing `.obsidian/plugins/` and `.obsidian/snippets/`. |

## References

- [Obsidian Help](https://help.obsidian.md/)
