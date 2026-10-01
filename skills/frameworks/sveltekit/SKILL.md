---
name: sveltekit
description: Expert SvelteKit assistance covering file-based routing (+page.svelte, +page.server.ts), form actions, hooks, and adapters. Use when developing full-stack, server-rendered Svelte web applications.
---

# SvelteKit

SvelteKit is the meta-framework for Svelte, similar to Next.js for React. It uses standard Web APIs and provides routing, server-side rendering, and API endpoints.

## When to Use

- **Svelte Apps**: The standard framework for building full-stack Svelte applications.
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

## Common Patterns

### Form Actions with Progressive Enhancement

**Problem**: Writing separate API endpoints and client fetch handlers for simple form submissions.

**Solution**:
Use SvelteKit Form Actions with `use:enhance`:

```typescript
// src/routes/login/+page.server.ts
import { fail, redirect, type Actions } from "@sveltejs/kit";

export const actions: Actions = {
  default: async ({ request }) => {
    const data = await request.formData();
    const email = data.get("email");
    if (!email) return fail(400, { email, missing: true });
    // Process login
    throw redirect(303, "/dashboard");
  },
};
```

```svelte
<!-- src/routes/login/+page.svelte -->
<script>
  import { enhance } from '$app/forms';
  export let form;
</script>

<form method="POST" use:enhance>
  <input name="email" value={form?.email ?? ''} />
  <button type="submit">Log In</button>
</form>
```

## Best Practices

**Do**:

- Use Svelte 5 Runes: SvelteKit 2+ fully supports Runes mode.
- Use `App.State`: New SvelteKit interface for typesafe global app state.
- Stream Data: Return promises in `load` functions to stream non-critical data.

**Don't**:

- Use `store` for server data: Use `page.data` (Context) for data passing down the tree to avoid state leakage on valid server execution.
- Perform sensitive database queries or secret token lookups in client-facing `+page.ts` files; place them in `+page.server.ts` instead.

## Troubleshooting

| Error                                               | Cause                                                         | Solution                                                                    |
| :-------------------------------------------------- | :------------------------------------------------------------ | :-------------------------------------------------------------------------- |
| `500 Internal Error: Cannot load module ... in SSR` | Client-only library imported directly in SSR bundle.          | Use dynamic import in `onMount()` or check `browser` in `$app/environment`. |
| `Not found: /route`                                 | File naming convention mismatch.                              | Ensure route page is named `+page.svelte` (with leading plus sign).         |
| `Adapter not specified`                             | `svelte.config.js` missing build adapter for target platform. | Install and configure `@sveltejs/adapter-auto` or `@sveltejs/adapter-node`. |

## References

- [SvelteKit Documentation](https://kit.svelte.dev/)
