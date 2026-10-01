---
name: astro
description: Expert Astro framework assistance covering content collections, Islands architecture, zero-JS by default, and multi-framework integration. Use when building content-focused websites, blogs, documentation, or marketing pages.
---

# Astro

Astro is a content-driven web framework pioneering Islands Architecture, shipping zero client-side JavaScript by default and hydrating interactive components on demand.

## When to Use

- **Content-Driven Websites & Portals**: Blogs, documentation, marketing sites, and e-commerce product catalogs.
- **Zero-JS Default Architecture**: Delivering maximum Lighthouse performance with Islands Architecture.
- **Multi-Framework Integrations**: Mixing React, Vue, Svelte, and Solid components in a single project.
- **Hybrid Static & Server-Rendered Sites**: Pre-rendering static pages while utilizing SSR routes for authenticated dashboards.

## Quick Start

```astro
---
// Server-side code (Frontmatter) runs at build/request time
const data = await fetch('https://api.myjson.com').then(r => r.json());
---

<html>
  <body>
    <h1>{data.title}</h1>
    <!-- Client Directive: This React component hydrates on load -->
    <MyReactComponent client:load />

    <!-- This Svelte component hydrates only when visible -->
    <MySvelteComponent client:visible />
  </body>
</html>
```

## Core Concepts

### Component Islands & Client Directives

Hydrating JavaScript only where interactive functionality is required:

```astro
---
// Server-side script runs only during build or request rendering
import Header from '../components/Header.astro';
import InteractiveCart from '../components/InteractiveCart.jsx';
import Footer from '../components/Footer.astro';

const pageTitle = "Astro 5 E-Commerce";
---

<html lang="en">
  <head>
    <title>{pageTitle}</title>
  </head>
  <body>
    <!-- 0KB JavaScript: Static HTML -->
    <Header title={pageTitle} />

    <main>
      <h1>Featured Catalog</h1>
      <!-- Island hydrated only when visible in viewport -->
      <InteractiveCart client:visible initialCount={0} />
    </main>

    <!-- 0KB JavaScript -->
    <Footer />
  </body>
</html>
```

### Content Collections with Type-Safe Schemas

Validating Markdown and MDX content with Zod schemas:

```typescript
// src/content/config.ts
import { defineCollection, z } from "astro:content";

const blogCollection = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    publishDate: z.date(),
    author: z.string().default("Core Team"),
    tags: z.array(z.string()),
    draft: z.boolean().default(false),
  }),
});

export const collections = {
  blog: blogCollection,
};
```

### Server Endpoints & Dynamic API Routes

Exposing REST endpoints for dynamic data fetching:

```typescript
// src/pages/api/newsletter.ts
import type { APIRoute } from "astro";

export const POST: APIRoute = async ({ request }) => {
  const data = await request.json();
  const email = data.email;

  if (!email || !email.includes("@")) {
    return new Response(JSON.stringify({ error: "Valid email required" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  return new Response(JSON.stringify({ message: "Subscribed successfully" }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
};
```

## Common Patterns

### Interactive Component Island with Client Directives

**Problem**: Shipping unnecessary JavaScript for largely static content pages.

**Solution**:
Use Astro Islands architecture with `client:visible` or `client:idle`:

```astro
---
// src/pages/index.astro
import Layout from '../layouts/Layout.astro';
import StaticHero from '../components/StaticHero.astro';
import SearchBar from '../components/SearchBar.jsx'; // React component
---

<Layout title="Welcome">
  <!-- Rendered to pure zero-JS HTML -->
  <StaticHero title="Fast by default" />

  <!-- Hydrated only when visible in viewport -->
  <SearchBar client:visible />
</Layout>
```

## Best Practices

**Do**:

- Use Astro Server Islands (`server:defer`) to defer slow, dynamic parts of static pages for instant TTFB.
- Leverage Content Collections for all Markdown and MDX files to ensure compile-time schema validation.
- Use `<Image />` component from `astro:assets` to automate WebP conversion and responsive `srcset`.
- Keep interactive islands isolated and small (`client:idle` or `client:visible`).

**Don't**:

- Use `client:load` on components below the fold; hydrate only when necessary.
- Import client UI framework libraries into `.astro` frontmatter unless rendering them as islands.
- Use client-side navigation (`ViewTransitions`) without auditing third-party script re-execution.

## Troubleshooting

| Error                                         | Cause                                                                      | Solution                                                                    |
| :-------------------------------------------- | :------------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `Cannot find module '../components/...'`      | Typo in component import or missing `.astro` file extension.               | Explicitly include `.astro` extension on all Astro component imports.       |
| `document is not defined`                     | Accessing browser DOM during static build SSR phase.                       | Guard DOM access inside `typeof document !== 'undefined'` or `client:only`. |
| `Content collection schema validation failed` | Markdown frontmatter does not match Zod schema in `src/content/config.ts`. | Correct frontmatter fields to adhere to the defined collection schema.      |

## References

- [Astro Documentation](https://astro.build/)
