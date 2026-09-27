---
name: strapi
description: Expert Strapi headless CMS assistance covering content types, plugins, REST/GraphQL APIs, and custom controllers. Use when building self-hosted, customizable Node.js headless CMS backends.
---

# Strapi

Strapi v5 (2025) introduces a **Document Service API**, Draft & Publish 2.0, and a content history feature. It is the leading self-hosted Headless CMS.

## When to Use

- **Self-Hosted Open Source Headless CMS**: Complete ownership of content data, database schemas, and hosting infrastructure.
- **Customizable Admin Dashboard**: Building content management workflows for editorial and marketing teams.
- **Automated REST & GraphQL Endpoints**: Instantly exposing type-safe APIs for frontends (Next.js, Nuxt, mobile).
- **Role-Based Content Governance**: Granular permissions, internationalization (i18n), and draft/publish workflows.

## Quick Start

```bash
# Create a new Strapi project with quickstart SQLite
npx create-strapi-app@latest my-cms --quickstart
```

```javascript
// src/api/article/controllers/article.js
const { createCoreController } = require("@strapi/strapi").factories;

module.exports = createCoreController("api::article.article", ({ strapi }) => ({
  async findCustom(ctx) {
    const entries = await strapi.entityService.findMany(
      "api::article.article",
      {
        populate: ["author", "coverImage"],
      },
    );
    return ctx.send(entries);
  },
}));
```

## Core Concepts

#Content-Type Schema Definition

Declaring entities, attributes, and relationships via JSON schema:

```json
{
  "kind": "collectionType",
  "collectionName": "articles",
  "info": {
    "singularName": "article",
    "pluralName": "articles",
    "displayName": "Article",
    "description": "Editorial blog articles"
  },
  "options": {
    "draftAndPublish": true
  },
  "attributes": {
    "title": {
      "type": "string",
      "required": true,
      "minLength": 5
    },
    "slug": {
      "type": "uid",
      "targetField": "title",
      "required": true
    },
    "content": {
      "type": "richtext"
    },
    "author": {
      "type": "relation",
      "relation": "manyToOne",
      "target": "plugin::users-permissions.user"
    }
  }
}
```

#Custom Controllers & Lifecycle Hooks

Extending core business logic with automated side-effects:

```typescript
// src/api/article/content-types/article/lifecycles.ts
export default {
  async beforeCreate(event) {
    const { data } = event.params;
    if (data.title) {
      data.slug = data.title.toLowerCase().replace(/[^a-z0-9]+/g, "-");
    }
  },

  async afterCreate(event) {
    const { result } = event;
    strapi.log.info(
      `New article published: ${result.title} (ID: ${result.id})`,
    );
    // Trigger external notification or webhook
  },
};
```

#Custom Service & Query API

Querying database using the Strapi Document Service:

```typescript
// src/api/article/services/article.ts
import { factories } from "@strapi/strapi";

export default factories.createCoreService(
  "api::article.article",
  ({ strapi }) => ({
    async findFeaturedArticles() {
      return await strapi.documents("api::article.article").findMany({
        filters: { featured: true },
        populate: ["author", "coverImage"],
        sort: { publishedAt: "desc" },
        limit: 5,
      });
    },
  }),
);
```

## Common Patterns

### Custom Lifecycle Hooks for Document Processing

**Problem**: Automatically generating slugs or sending notification emails on content creation.

**Solution**:
Use Strapi content type lifecycles:

```javascript
// src/api/article/content-types/article/lifecycles.js
const slugify = require("slugify");

module.exports = {
  beforeCreate(event) {
    const { data } = event.params;
    if (data.title && !data.slug) {
      data.slug = slugify(data.title, { lower: true, strict: true });
    }
  },
};
```

## Best Practices (2026)

- **Do** target Strapi v5 with the modern Document Service API and enhanced content versioning.
- **Do** configure API tokens with minimum necessary permissions for frontend consumer applications.
- **Do** use `populate` parameters selectively to prevent over-fetching relational data.
- **Do** store uploaded media in external object storage (AWS S3, Cloudinary) rather than the local filesystem.
- **Don't** expose admin panel routes (`/admin`) publicly without VPN or strict IP whitelisting in production.
- **Don't** edit generated content-type schema files manually while the Strapi development server is running.
- **Don't** query private fields (like user password hashes) in public controller responses.

## Troubleshooting

| Error                                         | Cause                                                            | Solution                                                                            |
| :-------------------------------------------- | :--------------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| `ForbiddenError: 403 Forbidden`               | API role permissions not enabled for public/authenticated users. | Enable permissions in Strapi Admin > Settings > Users & Permissions Plugin > Roles. |
| `Relations not returned in REST API response` | Strapi v4+ does not populate relations by default.               | Append query param: `?populate=*` or specify specific relation names.               |
| `Database migration error on server start`    | Schema changes in development conflicting with DB columns.       | Delete conflicting column or review schema in `content-types/schema.json`.          |

## References

- [Strapi Documentation](https://strapi.io/)
