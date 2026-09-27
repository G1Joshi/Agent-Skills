---
name: solidjs
description: Expert SolidJS assistance covering fine-grained reactivity, signals, zero Virtual DOM, and SolidStart. Use when building high-performance reactive web applications.
---

# SolidJS

SolidJS looks like React but has **no Virtual DOM**. It compiles to direct DOM updates using fine-grained reactivity (Signals). 2025 focuses on SolidStart (meta-framework).

## When to Use

- **High-Performance Reactive Web Applications**: Fine-grained reactivity without Virtual DOM overhead.
- **Real-Time Dashboards & Data Streaming**: Rapid UI updates directly mapped to granular DOM mutations.
- **Low-Memory Resource-Constrained Devices**: Embedded screens, smart TVs, and low-end mobile devices.
- **SolidStart Full-Stack Web Development**: Building SSR/SSG full-stack applications with JSX simplicity.

## Quick Start

```tsx
import { createSignal, onCleanup } from "solid-js";

export function Counter() {
  const [count, setCount] = createSignal(0);
  const timer = setInterval(() => setCount((c) => c + 1), 1000);
  onCleanup(() => clearInterval(timer));

  return <div>Count: {count()}</div>;
}
```

## Core Concepts

#Fine-Grained Reactive Primitives: Signals & Memos

Components execute only once; signals trigger targeted DOM node updates:

```tsx
import { createSignal, createMemo, createEffect, onCleanup } from "solid-js";

export function Counter() {
  const [count, setCount] = createSignal(0);
  const doubleCount = createMemo(() => count() * 2);

  createEffect(() => {
    console.log(`Current count: ${count()}, Doubled: ${doubleCount()}`);
  });

  const timer = setInterval(() => setCount((c) => c + 1), 1000);
  onCleanup(() => clearInterval(timer));

  return (
    <div class="p-4 border rounded">
      <h3>Count: {count()}</h3>
      <p>Double: {doubleCount()}</p>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
    </div>
  );
}
```

#Asynchronous Data with createResource & Suspense

Declarative async data fetching with Suspense boundaries:

```tsx
import { createResource, Suspense } from "solid-js";

interface UserProfile {
  id: number;
  name: string;
}

const fetchUser = async (id: number): Promise<UserProfile> => {
  const res = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
  return res.json();
};

export function UserView(props: { userId: number }) {
  const [user] = createResource(() => props.userId, fetchUser);

  return (
    <Suspense fallback={<p>Loading user profile...</p>}>
      <div>
        <h3>{user()?.name}</h3>
        <p>User ID: {user()?.id}</p>
      </div>
    </Suspense>
  );
}
```

#Control Flow with For, Show, and Switch

Optimized DOM rendering primitives replacing array `.map()`:

```tsx
import { For, Show } from "solid-js";

export function ProductList(props: {
  products: { id: number; name: string; inStock: boolean }[];
}) {
  return (
    <div>
      <Show
        when={props.products.length > 0}
        fallback={<p>No products found.</p>}
      >
        <ul>
          <For each={props.products}>
            {(product) => (
              <li>
                {product.name} -{" "}
                {product.inStock ? "Available" : "Out of Stock"}
              </li>
            )}
          </For>
        </ul>
      </Show>
    </div>
  );
}
```

## Common Patterns

### Fine-Grained Reactive Store for Complex Objects

**Problem**: Re-rendering an entire list when only a single property of one item changed.

**Solution**:
Use `createStore` for deep nested mutations:

```typescript
import { createStore } from "solid-js/store";

export function TodoApp() {
  const [todos, setTodos] = createStore([
    { id: 1, text: "Learn SolidJS", done: false },
    { id: 2, text: "Build App", done: false },
  ]);

  const toggleTodo = (id: number) => {
    setTodos(
      (todo) => todo.id === id,
      "done",
      (done) => !done
    );
  };

  return (
    <ul>
      <For each={todos}>
        {(todo) => (
          <li onClick={() => toggleTodo(todo.id)}>
            {todo.text} - {todo.done ? "✓" : "○"}
          </li>
        )}
      </For>
    </ul>
  );
}
```

## Best Practices (2026)

- **Do** use `<For>` and `<Show>` instead of `.map()` or ternary operators to minimize unnecessary DOM recreations.
- **Do** remember that Solid components run only once; never destructure `props` directly (use `props.title` or `mergeProps`).
- **Do** use `createResource` for async data loading with `<Suspense>`.
- **Do** call `onCleanup` inside effects and primitives to clear timers and event listeners.
- **Don't** destructure props in component argument signatures; it breaks fine-grained reactivity tracking.
- **Don't** update signals inside `createMemo`; memos must remain pure derivation functions.
- **Don't** use Virtual DOM assumptions (like re-rendering whole component trees).

## Troubleshooting

| Error                                   | Cause                                                                | Solution                                                                     |
| :-------------------------------------- | :------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| `Signal value not updating in UI`       | Destructuring props or signals, breaking reactive tracking.          | Access props directly (`props.name`) or use `splitProps()`.                  |
| `TypeError: count is not a function`    | Accessing signal as a raw value instead of calling getter `count()`. | Call signal as function: `count()`.                                          |
| `Component function executes only once` | Solid components are setup functions, not render functions.          | Place reactive logic inside effects or JSX getters, not bare component body. |

## References

- [SolidJS Documentation](https://www.solidjs.com/)
