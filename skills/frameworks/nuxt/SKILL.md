---
name: nuxt
description: Expert Nuxt 3 assistance covering Vue 3, auto-imports, file-based routing, Nitro server engine, and universal rendering. Use when developing SEO-optimized full-stack Vue applications.
---

# Nuxt

Nuxt is the full-stack framework for Vue. Nuxt 4 (2025) simplifies directory structure and enhances performance with the Nitro server engine.

## When to Use

- **Full-Stack Vue 3 Web Applications**: Nuxt 3/4 with universal SSR, static generation (SSG), and auto-imports.
- **Enterprise SEO & Fast Loading Pages**: Marketing sites and e-commerce stores requiring dynamic meta tags and instant rendering.
- **Edge-Ready Server Engine (Nitro)**: Deploying serverless functions seamlessly across Cloudflare, Vercel, Netlify, and Node.
- **Modular Frontend Architecture**: Utilizing first-party modules (`@nuxtjs/tailwindcss`, `@pinia/nuxt`, `@vueuse/nuxt`).

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

#Universal Data Fetching with useFetch & useAsyncData

SSR-friendly data fetching with automated deduplication:

```vue
<!-- pages/products/[id].vue -->
<script setup lang="ts">
interface Product {
  id: number;
  title: string;
  price: number;
}

const route = useRoute();
const productId = route.params.id;

const {
  data: product,
  pending,
  error,
} = await useFetch<Product>(`/api/products/${productId}`, {
  key: `product-${productId}`,
  lazy: false,
});

useSeoMeta({
  title: () =>
    product.value?.title ? `${product.value.title} - Store` : "Loading...",
  description: () => `Buy ${product.value?.title} online now.`,
});
</script>

<template>
  <div class="product-page">
    <div v-if="pending">Loading product details...</div>
    <div v-else-if="error">Error loading product: {{ error.message }}</div>
    <div v-else-if="product">
      <h1>{{ product.title }}</h1>
      <p class="price">${{ product.price }}</p>
    </div>
  </div>
</template>
```

#Nitro Server Engine API Routes

Creating backend API endpoints directly inside `server/api`:

```typescript
// server/api/products/[id].ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, "id");

  if (!id || isNaN(Number(id))) {
    throw createError({
      statusCode: 400,
      statusMessage: "Invalid product ID",
    });
  }

  return {
    id: Number(id),
    title: `Premium Mechanical Keyboard #${id}`,
    price: 149.99,
  };
});
```

#Nuxt Middleware & Route Guards

Client and server route authentication verification:

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const user = useCookie("auth_token");

  if (!user.value && to.path.startsWith("/dashboard")) {
    return navigateTo("/login");
  }
});
```

## Common Patterns

### Server API Route with useFetch Data Hydration

**Problem**: Client-side fetch triggers content flash and hurts search engine indexing.

**Solution**:
Use Nuxt server routes with universal `useFetch`:

```typescript
// server/api/products.ts
export default defineEventHandler(async (event) => {
  return await db.products.findMany({ take: 20 });
});

// pages/products.vue
<script setup>
const { data: products, pending, error } = await useFetch('/api/products');
</script>

<template>
  <div v-if="pending">Loading products...</div>
  <ul v-else>
    <li v-for="p in products" :key="p.id">{{ p.name }} - ${{ p.price }}</li>
  </ul>
</template>
```

## Best Practices (2026)

- **Do** use `useFetch` inside `<script setup>` for top-level component data fetching to eliminate SSR double-fetch.
- **Do** leverage Nuxt Server API routes (`server/api/`) for backend proxying and secret key protection.
- **Do** use `useSeoMeta()` for reactive, type-safe SEO management.
- **Do** enable Nitro route rules (`routeRules`) for granular caching and ISR per page.
- **Don't** use standard `fetch()` directly in setup scripts; it executes on both server and client without hydration transfer.
- **Don't** access `window` or `document` outside `onMounted` or without checking `import.meta.client`.
- **Don't** mutate server-side state across user requests.

## Troubleshooting

| Error                                             | Cause                                                           | Solution                                                                    |
| :------------------------------------------------ | :-------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `window is not defined / document is not defined` | Accessing browser DOM during server-side prerender step.        | Wrap browser code in `onMounted(() => { ... })` or `<ClientOnly>`.          |
| `[nuxt] [request error] [unhandled] 500`          | Server route threw unhandled exception.                         | Check terminal console output for server stack trace and wrap in try/catch. |
| `Component not found on auto-import`              | Nested folder structure requires path prefix in component name. | Follow naming convention: `components/base/Button.vue` -> `<BaseButton />`. |

## References

- [Nuxt Documentation](https://nuxt.com/)
