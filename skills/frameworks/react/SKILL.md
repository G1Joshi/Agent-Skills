---
name: react
description: React component-based UI with hooks, context, and state management. Use for .jsx/.tsx files.
---

# React

React is the standard library for building user interfaces. React 19 (2025) introduces a new era with the React Compiler, Server Components, and Actions.

## When to Use

- **Single Page Apps (SPA)**: Rich, interactive dashboards.
- **Complex UI**: Applications with many moving parts and state.
- **Ecosystem**: When you need the largest library of 3rd party components.

## Quick Start (React 19)

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

## Best Practices (2025)

**Do**:

- **Trust the Compiler**: Stop writing `useMemo`/`useCallback` unless you are building a library or strictly optimizing.
- **Use Server Actions**: Replace manual `fetch('/api/...')` with robust Server Actions for data mutations.
- **Use `ref` as a prop**: In React 19, `ref` is a plain prop. No more `forwardRef`.

**Don't**:

- **Don't overuse `useEffect`**: Effects are for synchronization with external systems, not for data fetching or derived state.
- **Don't spread props blindly**: Pass explicit props to make components easier to debug.

## References

- [React 19 Blog](https://react.dev/blog/2024/04/25/react-19)
- [React Documentation](https://react.dev/)
