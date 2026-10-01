---
name: nextjs
description: Expert Next.js assistance covering App Router, Server Components (RSC), Server Actions, metadata SEO, and edge runtime. Use when building high-performance full-stack React applications.
---

# Next.js

Next.js is a full-stack React framework featuring App Router architecture, React Server Components (RSC), Server Actions, and hybrid static/dynamic streaming.

## When to Use

- **Full-Stack React**: You need API routes, DB access, and UI in one codebase.
- **SEO Critical**: Server-Side Rendering (SSR) is first-class.
- **Vercel Ecosystem**: seamless deployment to Vercel's edge network.

## Quick Start

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

## Common Patterns

### Server Action with Optimistic UI Mutation

**Problem**: Form submission requires manual API route handlers and triggers full page reloads.

**Solution**:
Use React 19 Server Actions in Next.js App Router:

```tsx
// app/actions.ts
"use server";
import { revalidatePath } from "next/cache";

export async function addComment(formData: FormData) {
  const text = formData.get("comment") as string;
  await db.comments.create({ data: { text } });
  revalidatePath("/posts/[id]");
}

// app/CommentForm.tsx
import { addComment } from "./actions";

export function CommentForm() {
  return (
    <form action={addComment}>
      <input name="comment" required />
      <button type="submit">Post Comment</button>
    </form>
  );
}
```

## Best Practices

**Do**:

- Fetch in Server Components: Fetch data directly in your content (async components). No `useEffect`.
- Use `revalidatePath`: Revalidate cache on-demand after mutations (Server Actions).
- Partial Prerendering (PPR): (Experimental in '24, Stable in '25) Mix static shell with dynamic holes.

**Don't**:

- Leak secrets: Ensure `'use server'` files don't export sensitive data.
- `use client` everything: Only put `'use client'` at the leaves of your tree (buttons, inputs). Keep high-level layouts as Server Components.

## Troubleshooting

| Error                                                                       | Cause                                                                           | Solution                                                                                 |
| :-------------------------------------------------------------------------- | :------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------- |
| `Error: Event handlers cannot be passed to Client Component props`          | Passing client function from Server Component to Client Component.              | Mark file with `'use client'` at the very top.                                           |
| `Hydration failed because the server rendered HTML didn't match the client` | Browser-specific values (`window`, date/time, random IDs) evaluated during SSR. | Move browser-only evaluations to `useEffect` or wrap in dynamic import `{ ssr: false }`. |
| `Dynamic server usage: headers() / cookies() used in static page`           | Component marked static accessed request-time headers or searchParams.          | Export `export const dynamic = 'force-dynamic'` in page file.                            |

## References

- [Next.js Documentation](https://nextjs.org/docs)
