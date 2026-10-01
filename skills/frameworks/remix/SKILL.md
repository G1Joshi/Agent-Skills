---
name: remix
description: Expert Remix (React Router v7) assistance covering Loaders, Actions, nested routing, optimistic UI, and Web Fetch standards. Use when developing resilient, full-stack React web applications.
---

# Remix

Remix is a full-stack web framework built on web standards (Fetch API, Request/Response), providing nested routing, resilient form mutations, and seamless Vite integration.

## When to Use

- **Web Standards-First Full-Stack Applications**: Utilizing standard `Request`, `Response`, and HTML forms via Remix / React Router v7.
- **High-Performance Server-Rendered Applications**: Instant page transitions with nested routing and parallel data loading.
- **Resilient Web Apps with Progressive Enhancement**: Applications that function reliably before JavaScript has loaded.
- **Optimistic UI & Mutation Heavy Interfaces**: Using `useFetcher` and server actions without bespoke client state machines.

## Quick Start

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

### Nested Routing & Parallel Loader Data Loading

Fetching server-side data per route segment in parallel:

```tsx
// app/routes/users.$id.tsx
import { json, type LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData, Link } from "@remix-run/react";

export async function loader({ params }: LoaderFunctionArgs) {
  const userId = params.id;
  const user = await db.user.findUnique({ where: { id: userId } });

  if (!user) {
    throw new Response("User Not Found", { status: 404 });
  }

  return json({ user });
}

export default function UserDetailRoute() {
  const { user } = useLoaderData<typeof loader>();

  return (
    <div className="user-card">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <Link to="edit">Edit Profile</Link>
    </div>
  );
}
```

### Route Actions & HTML Form Submission

Standard HTTP POST handling with automatic revalidation:

```tsx
// app/routes/users.$id.edit.tsx
import { redirect, type ActionFunctionArgs } from "@remix-run/node";
import { Form, useActionData } from "@remix-run/react";

export async function action({ request, params }: ActionFunctionArgs) {
  const formData = await request.formData();
  const name = formData.get("name") as string;

  if (!name || name.length < 3) {
    return { error: "Name must be at least 3 characters" };
  }

  await db.user.update({ where: { id: params.id }, data: { name } });
  return redirect(`/users/${params.id}`);
}

export default function EditUserRoute() {
  const actionData = useActionData<typeof action>();

  return (
    <Form method="post">
      <input name="name" placeholder="Full Name" />
      {actionData?.error && <span className="error">{actionData.error}</span>}
      <button type="submit">Update</button>
    </Form>
  );
}
```

### Granular ErrorBoundaries per Route Segment

Isolating errors without crashing the entire page hierarchy:

```tsx
import { isRouteErrorResponse, useRouteError } from "@remix-run/react";

export function ErrorBoundary() {
  const error = useRouteError();

  if (isRouteErrorResponse(error)) {
    return (
      <div className="route-error">
        <h1>
          {error.status} {error.statusText}
        </h1>
        <p>{error.data}</p>
      </div>
    );
  }

  return (
    <div className="route-error">Unexpected application error occurred.</div>
  );
}
```

## Common Patterns

### Loader and Action Data Cycle

**Problem**: Managing separate state stores, loading states, and error handling for form submissions.

**Solution**:
Use Remix loaders and actions for declarative data synchronization:

```tsx
import {
  json,
  type LoaderFunctionArgs,
  type ActionFunctionArgs,
} from "@remix-run/node";
import { useLoaderData, Form } from "@remix-run/react";

export async function loader({ request }: LoaderFunctionArgs) {
  const todos = await db.todos.findMany();
  return json({ todos });
}

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  await db.todos.create({ title: formData.get("title") });
  return json({ ok: true });
}

export default function TodosPage() {
  const { todos } = useLoaderData<typeof loader>();
  return (
    <div>
      <Form method="post">
        <input name="title" required />
        <button type="submit">Add Todo</button>
      </Form>
      <ul>
        {todos.map((t) => (
          <li key={t.id}>{t.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

## Best Practices

**Do**:

- Leverage Remix / React Router v7 unified framework features for universal full-stack execution.
- Build mutations with native `<Form>` components to guarantee progressive enhancement.
- Co-locate `loader`, `action`, and component in the same route file for atomic cohesion.
- Use `useFetcher` for mutations that do not require full page navigation (e.g. upvotes, inline toggles).

**Don't**:

- Manage client cache state manually; Remix automatically revalidates loader data after actions.
- Return huge, unneeded relational payloads from loaders; return lean, serialized data.
- Use client-side `useEffect` for data fetching when `loader` functions exist.

## Troubleshooting

| Error                                                  | Cause                                                          | Solution                                                              |
| :----------------------------------------------------- | :------------------------------------------------------------- | :-------------------------------------------------------------------- |
| `Error: You must return a Response from loader/action` | Loader or action did not return a value or returned undefined. | Return `json({ data })` or `new Response(...)`.                       |
| `Form data empty in action`                            | Form inputs missing `name` attribute.                          | Ensure every `<input>` inside `<Form>` has a unique `name` attribute. |
| `Root boundary caught error`                           | Unhandled error in child route without local ErrorBoundary.    | Export `ErrorBoundary` component in route to catch local exceptions.  |

## References

- [Remix Documentation](https://remix.run/)
