---
name: vitest
description: Vitest fast Vite-native testing. Use for Vite projects.
---

# Vitest

Vitest is a next-generation testing framework powered by Vite. It uses the same configuration (vite.config.ts), transforms, and plugins as your app, making it incredibly fast and creating a unified dev/test environment.

## When to Use

- **Vite Projects**: If you use Vite, Vitest is the no-brainer choice. It reuses your plugins/config.
- **Performance**: It is significantly faster than Jest because it uses native ESM and doesn't bundle the app.
- **Watch Mode**: Instant HMR-style updates for tests.

## Quick Start

```typescript
// vite.config.ts
/// <reference types="vitest" />
import { defineConfig } from "vite";

export default defineConfig({
  test: {
    globals: true, // enables 'describe', 'test', 'expect' globally
    environment: "jsdom",
  },
});

// basic.test.ts
import { expect, test } from "vitest";

test("math", () => {
  expect(1 + 1).toBe(2);
});
```

## Core Concepts

### Jest Compatible

Vitest's API (`describe`, `it`, `expect`, `vi.fn`) is designed to be compatible with Jest. Migration is often just changing imports.

### In-Source Testing

Vitest allows running tests within your source code blocks (Rust-style), though separating them is still common practice.

```typescript
if (import.meta.vitest) {
  const { it, expect } = import.meta.vitest;
  it("add", () => {
    expect(add()).toBe(0);
  });
}
```

## Best Practices (2025)

**Do**:

- **Use Native ESM**: Stop fighting with Babel/ts-jest. Vitest handles ESM natively.
- **Use Workspace Mode**: For monorepos, Vitest works beautifully with workspace packages.
- **Switch from Jest**: If you are starting a new project, choose Vitest.

**Don't**:

- **Don't rely on global state**: Vitest runs tests in parallel.
- **Don't import Jest types**: Ensure `types` in `tsconfig.json` points to `vitest/globals` if using globals.

## References

- [Vitest Documentation](https://vitest.dev/)
