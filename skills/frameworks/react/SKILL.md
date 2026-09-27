---
name: react
description: Expert React assistance covering React 19, Server Components (RSC), hooks, compiler optimizations, and concurrent features. Use when building modern web user interfaces and single-page apps.
---

# React

React is the standard library for building user interfaces. React 19 (2025) introduces a new era with the React Compiler, Server Components, and Actions.

## When to Use

- **Single Page Apps (SPA)**: Rich, interactive dashboards.
- **Complex UI**: Applications with many moving parts and state.
- **Ecosystem**: When you need the largest library of 3rd party components.

## Quick Start

```tsx
import { use, Suspense } from "react";

// New: 'use' hook for promises
function Comments({ commentsPromise }) {
  const comments = use(commentsPromise);
  return comments.map((c) => <p key={c.id}>{c.text}</p>);
}

export default function Page({ id }) {
  const commentsPromise = fetchComments(id);

  return (
    <Suspense fallback={<p>Loading...</p>}>
      <Comments commentsPromise={commentsPromise} />
    </Suspense>
  );
}
```

## Core Concepts

### React Compiler

React 19 introduces an auto-memoizing compiler. You no longer need `useMemo` or `useCallback` manually in 99% of cases. The compiler treats code as "memoized by default".

### Server Components (RSC)

Components that run _only_ on the server. They don't send JS to the client.

- **`'use server'`**: Marks a function as a Server Action (callable from client).
- **`'use client'`**: Marks a component as interactive (hydrated on client).

### Actions and `useActionState`

Native support for async form submission.

```tsx
function Form() {
  const [error, submitAction, isPending] = useActionState(
    async (prev, formData) => {
      const error = await updateProfile(formData);
      if (error) return error;
      return null;
    },
    null,
  );

  return (
    <form action={submitAction}>
      <input name="name" />
      <button disabled={isPending}>Save</button>
      {error && <p>{error}</p>}
    </form>
  );
}
```

## Common Patterns

### Custom Reusable Hook with Cleanup

**Problem**: Duplicating event listeners or subscription lifecycles across UI components.

**Solution**:
Encapsulate logic in a typed custom hook:

```typescript
import { useState, useEffect } from "react";

export function useWindowWidth() {
  const [width, setWidth] = useState(() =>
    typeof window !== "undefined" ? window.innerWidth : 1024,
  );

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return width;
}
```

## Best Practices (2026)

**Do**:

- **Trust the Compiler**: Stop writing `useMemo`/`useCallback` unless you are building a library or strictly optimizing.
- **Use Server Actions**: Replace manual `fetch('/api/...')` with robust Server Actions for data mutations.
- **Use `ref` as a prop**: In React 19, `ref` is a plain prop. No more `forwardRef`.

**Don't**:

- **Don't overuse `useEffect`**: Effects are for synchronization with external systems, not for data fetching or derived state.
- **Don't spread props blindly**: Pass explicit props to make components easier to debug.

## Troubleshooting

| Error                                                                                 | Cause                                                                         | Solution                                                                          |
| :------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------- | :-------------------------------------------------------------------------------- |
| `Too many re-renders. React limits the number of renders to prevent an infinite loop` | State setter invoked directly in component body instead of handler/useEffect. | Wrap setter call inside an event handler or `useEffect`: `() => setCount(c + 1)`. |
| `Rendered fewer hooks than expected`                                                  | Hook called inside a conditional `if` statement or loop.                      | Always call React hooks at the top level of component before conditionals.        |
| `Hydration mismatch: Text content does not match server-rendered HTML`                | Client-only values evaluated during initial server render.                    | Use `suppressHydrationWarning` on element or load after mount.                    |

## References

- [React 19 Blog](https://react.dev/blog/2024/04/25/react-19)
- [React Documentation](https://react.dev/)
