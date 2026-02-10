---
name: nuxt
description: Nuxt.js Vue framework with SSR and auto-imports. Use for full-stack Vue applications.
---

# Nuxt

Nuxt is the full-stack framework for Vue. Nuxt 4 (2025) simplifies directory structure and enhances performance with the Nitro server engine.

## When to Use

- **Vue Applications**: The de-facto standard for production Vue apps.
- **Universal Rendering**: Switch between SSR, SSG, and CSR per-route.
- **Module Ecosystem**: rich modules (Nuxt Image, Nuxt Content, Pinia).

## Quick Start

Nuxt auto-imports components and composables.

```vue
<script setup>
// useFetch is auto-imported
const { data: quote } = await useFetch("/api/quote");
</script>

<template>
  <blockquote>{{ quote.text }}</blockquote>
</template>
```

## Core Concepts

### Nitro Engine

Nuxt's server engine. It builds your server to run anywhere (Node, Deno, Bun, Edge/Serverless) without config.

### Auto-Imports

You don't need to `import { ref } from 'vue'` or `import UserCard from './components/UserCard.vue'`. Nuxt does it for you.

### Server Routes

`server/api/hello.ts` creates an API endpoint `/api/hello`.

## Best Practices (2025)

**Do**:

- **Use `useFetch`**: It handles SSR data fetching correctly (preventing double-fetch on client).
- **Use Nuxt Modules**: Don't manually configure libraries. Use `@nuxt/image`, `@nuxtjs/tailwindcss`.
- **Use `app/` directory**: Nuxt 4 defaults code to `app/` to keep root clean.

**Don't**:

- **Don't use `axios`**: Use the built-in `$fetch` (OFetch) which is smarter and lighter.

## References

- [Nuxt Documentation](https://nuxt.com/)
