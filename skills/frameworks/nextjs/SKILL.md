---
name: nextjs
description: Next.js React framework with SSR, App Router, and server components. Use for full-stack React.
---

# Next.js

Next.js is the leading full-stack framework for React. Next.js 15 (2025) stabilizes the App Router and Server Actions, making it a robust platform for modern web apps.

## When to Use

- **Full-Stack React**: You need API routes, DB access, and UI in one codebase.
- **SEO Critical**: Server-Side Rendering (SSR) is first-class.
- **Vercel Ecosystem**: seamless deployment to Vercel's edge network.

## Quick Start (App Router)

```tsx
// app/page.tsx (Server Component by default)
import { db } from "@/lib/db";

export default async function Page() {
  const posts = await db.post.findMany(); // Direct DB access!

  return (
    <main>
      <h1>Blog</h1>
      {posts.map((post) => (
        <p key={post.id}>{post.title}</p>
      ))}
    </main>
  );
}
```

## Core Concepts

### App Router (`app/` dir)

File-system based routing where `page.tsx` is the UI, `layout.tsx` wraps children, and `loading.tsx` defines Suspense boundaries.

### Server Components (RSC)

Components in `app/` are Server Components by default. They can't use `useState` or `useEffect`. To add interactivity, add `'use client'` to the top of a file.

### Server Actions

Functions that run on the server, callable from the client (forms, buttons).

```tsx
// actions.ts
'use server'
export async function create(formData) {
  await db.post.create({ data: ... });
}
```

## Best Practices (2025)

**Do**:

- **Fetch in Server Components**: Fetch data directly in your content (async components). No `useEffect`.
- **Use `revalidatePath`**: Revalidate cache on-demand after mutations (Server Actions).
- **Partial Prerendering (PPR)**: (Experimental in '24, Stable in '25) Mix static shell with dynamic holes.

**Don't**:

- **Don't leak secrets**: Ensure `'use server'` files don't export sensitive data.
- **Don't `use client` everything**: Only put `'use client'` at the leaves of your tree (buttons, inputs). Keep high-level layouts as Server Components.

## References

- [Next.js Documentation](https://nextjs.org/docs)
