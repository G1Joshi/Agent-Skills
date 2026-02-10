---
name: astro
description: Astro static site builder with islands architecture and content collections. Use for content sites.
---

# Astro

Astro is a web framework popularized for "Islands Architecture". It ships **zero JavaScript** to the client by default, hydrating only the interactive parts. Astro 5 (2025) introduces Server Islands.

## When to Use

- **Content Sites**: Blogs, Documentation, Marketing sites.
- **Multi-Framework**: Use React, Vue, and Svelte components on the same page.
- **Performance**: Hard to beat for static content.

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

### Islands Architecture

The page is static HTML. Interactive widgets are "islands" floating in it. They hydrate independently.

### Server Islands (Astro 5)

Async islands. The page loads instantly (static), and a specific island (e.g., "User Profile") loads asynchronously from the server and fades in.

### Content Collections

Type-safe way to manage Markdown/MDX content.

```ts
const blogCollection = defineCollection({
  schema: z.object({ title: z.string(), date: z.date() }),
});
```

## Best Practices (2025)

**Do**:

- **Use Server Islands**: For dynamic personalization (e.g., "Logged in as Jeevan") without forcing the whole page to be dynamic (SSR).
- **Use `<Image />`**: Astro's optimized image component is essential for LCP.
- **Mix Frameworks**: Don't be afraid to use React for a complex search bar and Svelte for a simple toggle on the same site.

**Don't**:

- **Don't use for complex dashboards**: While possible (Hybrid Rendering), Next.js or Remix are often better suited for highly dynamic, authenticated apps.

## References

- [Astro Documentation](https://astro.build/)
