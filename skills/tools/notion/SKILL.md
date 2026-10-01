---
name: notion
description: Expert Notion assistance covering relational database design, formula 2.0 expressions, API integration via @notionhq/client, workspace automation, and template architectures. Use when building Notion databases, writing Notion formulas, syncing data with the Notion API, or designing team wikis.
---

# Notion

Notion is an all-in-one collaborative workspace combining technical documentation wikis, relational databases, project roadmaps, and API integrations.

## When to Use

- **Engineering Knowledge Bases**: Creating team documentation, API design RFCs, and incident post-mortems.
- **Programmatic Database Sync**: Syncing GitHub PRs, Jira tickets, and deployment logs into Notion via Official SDK.
- **Task & Sprint Tracking**: Organizing engineering backlogs, milestone roadmaps, and sprint boards with linked relations.
- **Automated Report Generation**: Publishing automated daily metrics summaries into Notion pages via Scheduled Lambdas/Workflows.

## Quick Start

### 1. Official Notion SDK Query

```javascript
import { Client } from "@notionhq/client";

const notion = new Client({ auth: process.env.NOTION_API_KEY });

const response = await notion.databases.query({
  database_id: process.env.NOTION_DATABASE_ID,
  filter: {
    property: "Status",
    status: { equals: "In Progress" },
  },
  sorts: [{ property: "Due Date", direction: "ascending" }],
});
console.log(
  response.results.map((page) => page.properties.Name.title[0]?.plain_text),
);
```

### 2. Install Notion SDK

```bash
npm install @notionhq/client
```

## Core Concepts

### Querying Notion Databases via JavaScript SDK

Querying sprint tasks with filters and sorting using `@notionhq/client`:

```javascript
import { Client } from "@notionhq/client";

const notion = new Client({ auth: process.env.NOTION_API_KEY });
const DATABASE_ID = process.env.NOTION_DATABASE_ID;

async function getUrgentSprintTasks() {
  const response = await notion.databases.query({
    database_id: DATABASE_ID,
    filter: {
      and: [
        {
          property: "Status",
          status: { equals: "In Progress" },
        },
        {
          property: "Priority",
          select: { equals: "High" },
        },
      ],
    },
    sorts: [
      {
        property: "Due Date",
        direction: "ascending",
      },
    ],
  });

  return response.results.map((page) => ({
    id: page.id,
    title: page.properties.Name.title[0]?.plain_text,
    assignee: page.properties.Assignee.people[0]?.name,
  }));
}
```

### Programmatic Page Creation & Block Insertion

Creating an automated deployment log page within an engineering database:

```javascript
async function createDeploymentLog(version, environment, commitHash) {
  const newPage = await notion.pages.create({
    parent: { database_id: DATABASE_ID },
    properties: {
      Name: {
        title: [{ text: { content: `Release ${version} [${environment}]` } }],
      },
      Environment: {
        select: { name: environment },
      },
      Timestamp: {
        date: { start: new Date().toISOString() },
      },
    },
    children: [
      {
        object: "block",
        type: "heading_2",
        heading_2: {
          rich_text: [
            { type: "text", text: { content: "Deployment Details" } },
          ],
        },
      },
      {
        object: "block",
        type: "code",
        code: {
          language: "json",
          rich_text: [
            {
              type: "text",
              text: {
                content: JSON.stringify(
                  { commit: commitHash, status: "SUCCESS" },
                  null,
                  2,
                ),
              },
            },
          ],
        },
      },
    ],
  });

  return newPage.id;
}
```

### Formula 2.0 Calculations

Using Notion Formulas 2.0 for business logic and progress tracking:

```text
// Sprint Progress Bar Formula (2.0)
let(
  total, prop("Total Tasks"),
  done, prop("Completed Tasks"),
  percent, if(total > 0, round(done / total * 100), 0),
  percent + "% " + substring("■■■■■■■■■■", 0, round(percent / 10)) + substring("□□□□□□□□□□", 0, 10 - round(percent / 10))
)
```

## Common Patterns

### Advanced Formula 2.0 (Progress Bar & Date Math)

**Problem**: Display dynamic progress bar and overdue indicator without external rollup plugins.  
**Solution**: Use Formulas 2.0 functions `let()`, `repeat()`, and `dateBetween()`.

```notion
/* Formula for Progress Percentage & Bar */
let(
  pct, round(prop("Tasks Completed") / max(prop("Total Tasks"), 1) * 100),
  let(
    filled, round(pct / 10),
    repeat("█", filled) + repeat("░", 10 - filled) + " " + pct + "%"
  )
)
```

### Append Blocks via Notion API

**Problem**: Programmatically inject markdown or structured notes into a Notion page.  
**Solution**: Call `notion.blocks.children.append()`.

```javascript
await notion.blocks.children.append({
  block_id: pageId,
  children: [
    {
      object: "block",
      type: "heading_2",
      heading_2: {
        rich_text: [
          { type: "text", text: { content: "Automated Deploy Summary" } },
        ],
      },
    },
    {
      object: "block",
      type: "bulleted_list_item",
      bulleted_list_item: {
        rich_text: [
          { type: "text", text: { content: "Build hash: 8f3d1e (Success)" } },
        ],
      },
    },
  ],
});
```

## Best Practices

**Do**:

- Store integration tokens securely in environment variables and grant integrations access only to specific parent pages.
- Utilize Database Rollups and 2-way Relations to link Sprints, Epics, and individual Engineering Tasks.
- Handle API rate limits (average 3 requests per second) with exponential backoff and jitter.
- Paginate database query results using `start_cursor` and `has_more` for datasets larger than 100 records.

**Don't**:

- Store sensitive API secrets, database passwords, or private SSH keys in Notion pages.
- Create deep, unorganized page hierarchies; rely on searchable relational databases with views.
- Perform unbounded queries without filters on databases containing thousands of historical rows.

## Troubleshooting

| Error                    | Cause                                                           | Solution                                                                                      |
| ------------------------ | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `object_not_found` (404) | Integration does not have access to the target page or database | In Notion UI, open page menu (`...`), go to **Connections**, and invite/add your Integration. |
| `rate_limited` (429)     | Exceeded 3 requests per second limit                            | Implement exponential backoff retry logic in API client wrappers.                             |
| Formula 2.0 syntax error | Type mismatch (e.g. attempting arithmetic on string rollups)    | Wrap property values with `toNumber()` or use `.map()` array syntax for rollup lists.         |

## References

- [Notion Help Center](https://www.notion.so/help)
