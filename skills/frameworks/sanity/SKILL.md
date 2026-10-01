---
name: sanity
description: Expert Sanity.io headless CMS assistance covering GROQ queries, Content Lake, schema definitions, and Sanity Studio. Use when building structured content platforms and headless digital experiences.
---

# Sanity

Sanity is "Content as Data". The **Studio v3** is a real-time React application that you host, giving you complete control over the editing experience.

## When to Use

- **Structured Content Platforms**: Headless CMS providing real-time collaboration and custom editing studios.
- **Multi-Channel Omnichannel Publishing**: Distributing content to websites, mobile apps, e-commerce, and signage.
- **Sanity Studio v3 Customization**: Customizing React-based editorial workspaces with schema-as-code.
- **Real-Time Visual Editing**: Combining GROQ queries with Vercel Visual Editing and live content previews.

## Quick Start

```typescript
// schemaTypes/post.ts
import { defineField, defineType } from "sanity";

export const postType = defineType({
  name: "post",
  title: "Blog Post",
  type: "document",
  fields: [
    defineField({
      name: "title",
      type: "string",
      validation: (rule) => rule.required(),
    }),
    defineField({ name: "slug", type: "slug", options: { source: "title" } }),
    defineField({ name: "publishedAt", type: "datetime" }),
  ],
});
```

## Core Concepts

### Declarative Schema-as-Code

Defining content types, fields, and validation rules:

```typescript
// schemas/post.ts
import { defineType, defineField } from "sanity";

export const postType = defineType({
  name: "post",
  title: "Blog Post",
  type: "document",
  fields: [
    defineField({
      name: "title",
      title: "Title",
      type: "string",
      validation: (Rule) => Rule.required().min(10).max(100),
    }),
    defineField({
      name: "slug",
      title: "Slug",
      type: "slug",
      options: { source: "title", maxLength: 96 },
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: "publishedAt",
      title: "Published At",
      type: "datetime",
      initialValue: () => new Date().toISOString(),
    }),
    defineField({
      name: "content",
      title: "Body Content",
      type: "array",
      of: [{ type: "block" }, { type: "image" }],
    }),
  ],
});
```

### Type-Safe GROQ Queries with Sanity TypeGen

Querying structured content with filter and projection:

```typescript
import { createClient, groq } from "next-sanity";

export const client = createClient({
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!,
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET!,
  apiVersion: "2026-01-01",
  useCdn: false, // false for fresh drafts in preview mode
});

// GROQ query projection
export const POSTS_QUERY = groq`
  *[_type == "post" && defined(slug.current)] | order(publishedAt desc)[0...10] {
    _id,
    title,
    "slug": slug.current,
    publishedAt,
    "authorName": author->name
  }
`;
```

### Portable Text Rendering in React

Rendering structured block content with custom components:

```tsx
import { PortableText, PortableTextComponents } from "@portabletext/react";

const customComponents: PortableTextComponents = {
  types: {
    image: ({ value }) => (
      <img
        src={value.imageUrl}
        alt={value.alt || "Content image"}
        className="rounded-lg my-4"
      />
    ),
  },
  marks: {
    link: ({ children, value }) => {
      const target = (value?.href || "").startsWith("http")
        ? "_blank"
        : undefined;
      return (
        <a
          href={value?.href}
          target={target}
          rel="noopener noreferrer"
          className="text-blue-500 underline"
        >
          {children}
        </a>
      );
    },
  },
};

export function ArticleBody({ value }: { value: any }) {
  return <PortableText value={value} components={customComponents} />;
}
```

## Common Patterns

### GROQ Query with Projection and Filter

**Problem**: Fetching complete nested documents when only a few fields are needed by the frontend.

**Solution**:
Use GROQ projections:

```typescript
import { createClient } from "@sanity/client";

const client = createClient({
  projectId: "your-project-id",
  dataset: "production",
  useCdn: true,
  apiVersion: "2024-01-01",
});

const query = `*[_type == "post" && defined(slug.current)] | order(publishedAt desc)[0...10] {
  _id,
  title,
  "slug": slug.current,
  "authorName": author->name
}`;

const posts = await client.fetch(query);
```

## Best Practices

**Do**:

- Use Sanity TypeGen (`sanity typegen generate`) to generate TypeScript types from GROQ queries automatically.
- Configure fine-grained webhook listeners for On-Demand Revalidation in Next.js / Nuxt / Remix.
- Pin the `apiVersion` parameter (`'2026-01-01'`) to prevent breaking changes.
- Use Portable Text for rich editorial content rather than raw HTML or Markdown.

**Don't**:

- Use `*[]` without type constraints in GROQ; always specify `_type == "..."` for indexing.
- Expose write tokens (`SANITY_API_WRITE_TOKEN`) to client-side bundles.
- Query entire document trees without projections; project only the fields required by the UI.

## Troubleshooting

| Error                                    | Cause                                                                      | Solution                                                                    |
| :--------------------------------------- | :------------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `ClientError: Project ID not configured` | Missing `projectId` in client options or environment variables.            | Provide valid `projectId` in `createClient(...)`.                           |
| `Unknown type "..." in schema`           | Referenced schema type not imported or exported in `schemaTypes/index.ts`. | Add missing type definition to the `schemaTypes` array in sanity.config.ts. |
| `CORS Error: Origin not allowed`         | Frontend domain not added to Sanity API Allowed Origins.                   | Add domain in Sanity management dashboard under API settings.               |

## References

- [Sanity Documentation](https://www.sanity.io/)
