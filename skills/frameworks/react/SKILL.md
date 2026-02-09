---
name: react
description: React component-based UI with hooks, context, state management, and performance optimization. Use for .jsx/.tsx files.
---

# React

Component-based UI library with hooks, state management, and modern patterns.

## When to Use

- Building interactive web UIs
- Single-page applications
- Component libraries
- Server-side rendered apps (with Next.js)

## Quick Start

```tsx
import { useState } from "react";

interface Props {
  initialCount?: number;
}

export function Counter({ initialCount = 0 }: Props) {
  const [count, setCount] = useState(initialCount);

  return <button onClick={() => setCount((c) => c + 1)}>Count: {count}</button>;
}
```

## Core Concepts

### Hooks

```tsx
import { useState, useEffect, useCallback, useMemo } from "react";

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      const data = await fetchUser(userId);
      if (!cancelled) {
        setUser(data);
        setLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [userId]);

  const displayName = useMemo(
    () => (user ? `${user.firstName} ${user.lastName}` : ""),
    [user],
  );

  const handleSave = useCallback(
    async (updates: Partial<User>) => {
      await updateUser(userId, updates);
    },
    [userId],
  );

  if (loading) return <Spinner />;
  return <ProfileForm user={user} onSave={handleSave} />;
}
```

### Custom Hooks

```tsx
function useLocalStorage<T>(key: string, initial: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initial;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}

// Usage
const [theme, setTheme] = useLocalStorage("theme", "light");
```

## Common Patterns

### Context for State

```tsx
interface AppState {
  user: User | null;
  theme: "light" | "dark";
}

type Action =
  | { type: "SET_USER"; user: User }
  | { type: "LOGOUT" }
  | { type: "TOGGLE_THEME" };

const AppContext = createContext<{
  state: AppState;
  dispatch: Dispatch<Action>;
} | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) throw new Error("useApp must be within AppProvider");
  return context;
}
```

## Best Practices

**Do**:

- Use TypeScript for type safety
- Colocate state near where it's used
- Memoize callbacks passed to children
- Use React Query/TanStack for server state

**Don't**:

- Overuse useEffect (prefer event handlers)
- Mutate state directly
- Use indexes as keys for dynamic lists
- Create new objects in render

## Troubleshooting

| Issue              | Cause                      | Solution                |
| ------------------ | -------------------------- | ----------------------- |
| Infinite re-render | useEffect dependency issue | Check dependency array  |
| Stale closure      | Missing dependency         | Add to dependency array |
| Slow render        | Large lists                | Use virtualization      |

## References

- [React Documentation](https://react.dev/)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
