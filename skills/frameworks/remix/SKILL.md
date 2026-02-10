---
name: remix
description: Remix React framework with nested routing and data loading. Use for full-stack React.
---

# Remix

Remix is a full-stack web framework that focuses on web standards (Fetch API, Forms). In 2025, it has largely converged with **React Router 7**, offering a "Vite-native" experience.

## When to Use

- **Data-Heavy Apps**: Excellent handling of nested data loading and parallel fetching.
- **Web Standards**: If you like standard `<form>` and `FormData` over complex RPC layers.
- **Optimistic UI**: Built-in support for optimistic UI makes apps feel instant.

## Quick Start (Loader/Action)

```tsx
import { json } from "@remix-run/node";
import { useLoaderData, Form } from "@remix-run/react";

// Functions run on server
export async function loader() {
  return json(await db.getTasks());
}

export async function action({ request }) {
  const formData = await request.formData();
  await db.createTask(formData.get("title"));
  return json({ ok: true });
}

// Component runs on Client + Server
export default function Tasks() {
  const tasks = useLoaderData<typeof loader>();
  return (
    <Form method="post">
      <input name="title" />
      <button>Add</button>
    </Form>
  );
}
```

## Core Concepts

### Nested Routing

Remix loads data _in parallel_ for every segment of the URL. `/sales/invoices/1023` loads data for Sales Layout, Invoices List, and Invoice Details simultaneously.

### Progressive Enhancement

Apps work without JavaScript by default (mostly). Form submissions work via standard browser POST if JS fails.

### Actions & Loaders

The "Backend for Frontend" is co-located in the same file as the UI.

## Best Practices (2025)

**Do**:

- **Use Single Fetch**: The new 2025 data loading pattern that combines multiple loaders into one HTTP request.
- **Flat Routes**: Use the flat file convention (`routes/dashboard.settings.tsx`) to avoid deep folder nesting.
- **Use `defer`**: Stream slow data (like third party APIs) while showing the critical UI immediately.

**Don't**:

- **Don't manage global state for server data**: `useLoaderData` _is_ your state manager. You don't often need Redux/Context.

## References

- [Remix Documentation](https://remix.run/)
