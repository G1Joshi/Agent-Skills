---
name: solidjs
description: SolidJS reactive UI library with fine-grained reactivity and JSX. Use for performant React-like apps.
---

# SolidJS

SolidJS looks like React but has **no Virtual DOM**. It compiles to direct DOM updates using fine-grained reactivity (Signals). 2025 focuses on SolidStart (meta-framework).

## When to Use

- **Performance**: Consistently tops benchmarks.
- **Real-time**: Fine-grained updates make it ideal for dashboards.
- **Mental Model**: If you prefer "it only runs once" components vs React's re-renders.

## Core Concepts

### Signals (`createSignal`)

The atom of state. `const [count, setCount] = createSignal(0)`.

### Effects (`createEffect`)

Runs when dependencies change. Automatic dependency tracking.

### Show / For

Control flow components (`<Show when={...}>`) instead of `map`.

## Best Practices (2025)

**Do**:

- **Use `createResource`**: For async data fetching.
- **Access signals as functions**: `count()` not `count`.
- **Use SolidStart**: For file-system routing and SSR.

**Don't**:

- **Don't destructure props**: Reactivity is lost if you destructure `props`.

## References

- [SolidJS Documentation](https://www.solidjs.com/)
