---
name: nextjs
description: Next.js React framework with App Router, Server Components, and full-stack capabilities. Use for full-stack React.
---

# Next.js

Full-stack React framework with Server Components and App Router.

## When to Use

- Full-stack React applications
- Server-side rendering (SSR)
- Static site generation (SSG)
- API routes and edge functions

## Quick Start

```tsx
// app/page.tsx - Server Component by default
export default async function Home() {
  const posts = await db.posts.findMany();

  return (
    <main>
      <h1>Blog</h1>
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </main>
  );
}
```

## Core Concepts

### App Router Structure

```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Home page
├── loading.tsx         # Loading UI
├── error.tsx           # Error UI
├── blog/
│   ├── page.tsx        # /blog
│   └── [slug]/
│       └── page.tsx    # /blog/:slug
└── api/
    └── users/
        └── route.ts    # API route
```

### Server Components

```tsx
// Server Component - runs on server only
async function UserList() {
  const users = await db.users.findMany(); // Direct DB access
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

// Client Component - interactive
("use client");
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount((c) => c + 1)}>{count}</button>;
}
```

## Common Patterns

### Server Actions

```tsx
// app/actions.ts
"use server";

import { revalidatePath } from "next/cache";

export async function createPost(formData: FormData) {
  const title = formData.get("title") as string;

  await db.posts.create({ data: { title } });
  revalidatePath("/posts");
}

// In component
<form action={createPost}>
  <input name="title" required />
  <button type="submit">Create</button>
</form>;
```

### Data Fetching

```tsx
// Static data (cached)
async function getPost(slug: string) {
  return fetch(`/api/posts/${slug}`, { cache: "force-cache" });
}

// Dynamic data (no cache)
async function getUser() {
  return fetch("/api/user", { cache: "no-store" });
}

// Revalidate periodically
async function getPosts() {
  return fetch("/api/posts", { next: { revalidate: 60 } });
}
```

## Best Practices

**Do**:

- Use Server Components by default
- Use Server Actions for mutations
- Implement proper loading states
- Use `generateMetadata` for SEO

**Don't**:

- Add 'use client' unnecessarily
- Fetch in Client Components (use Server)
- Ignore error boundaries
- Block rendering with large fetches

## Troubleshooting

| Issue              | Cause                      | Solution               |
| ------------------ | -------------------------- | ---------------------- |
| Stale data         | Aggressive caching         | Use revalidatePath/Tag |
| Hydration mismatch | Server/client diff         | Check dynamic content  |
| Large bundle       | Too many client components | Move logic to server   |

## References

- [Next.js Documentation](https://nextjs.org/docs)
- [Vercel Blog](https://vercel.com/blog)
