---
name: sveltekit
description: SvelteKit full-stack Svelte framework with SSR and routing. Use for Svelte applications.
---

# SvelteKit

SvelteKit is the meta-framework for Svelte, similar to Next.js for React. It uses standard Web APIs and provides routing, server-side rendering, and API endpoints.

## When to Use

- **Svelte Apps**: The standard way to build Svelte apps in 2025.
- **Full Stack**: Unified backend and frontend.
- **Edge Deployment**: Runs on any platform via Adapters (Vercel, Cloudflare, Netlify, Node).

## Quick Start

File-based routing in `src/routes`.

```svelte
<!-- src/routes/+page.svelte -->
<script>
  let { data } = $props(); // Received from +page.server.js
</script>

<h1>{data.title}</h1>
```

```javascript
// src/routes/+page.server.js
export function load() {
  return { title: "Hello from Server" };
}
```

## Core Concepts

### Load Functions

`load` functions in `+page.server.js` run before the page renders, fetching data. The data is typed automatically in the component.

### Form Actions

Handle form submissions in `+page.server.js` exports named `actions`.

```javascript
export const actions = {
  default: async ({ request }) => {
    const data = await request.formData();
    // save to db
  },
};
```

### Adapters

Deployment targets are plugins. `adapter-auto`, `adapter-node`, `adapter-cloudflare`.

## Best Practices (2025)

**Do**:

- **Use Svelte 5 Runes**: SvelteKit 2+ fully supports Runes mode.
- **Use `App.State`**: New SvelteKit interface for typesafe global app state.
- **Stream Data**: Return promises in `load` functions to stream non-critical data.

**Don't**:

- **Don't use `store` for server data**: Use `page.data` (Context) for data passing down the tree to avoid state leakage on valid server execution.

## References

- [SvelteKit Documentation](https://kit.svelte.dev/)
