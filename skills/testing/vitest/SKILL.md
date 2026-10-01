---
name: vitest
description: Expert Vitest testing assistance covering Vite-native test execution, mocking, snapshots, and ESM support. Use when writing fast unit and integration tests for Vite, Vue, React, or TypeScript projects.
---

# Vitest

Vitest is a next-generation testing framework powered by Vite. It uses the same configuration (vite.config.ts), transforms, and plugins as your app, making it incredibly fast and creating a unified dev/test environment.

## When to Use

- **Modern Vite & ESM Unit Testing**: The lightning-fast, native test runner for Vite-powered React, Vue, Svelte, Solid, and Node.js projects.
- **Drop-in Jest Replacement**: Migrating from Jest to Vitest with identical `describe`, `it`, `expect`, and `vi` APIs with zero config overhead.
- **Instant Watch Mode with HMR**: Re-running only affected tests instantaneously when source files change.
- **Native TypeScript & JSX Support**: Running TypeScript and JSX out of the box without separate transpilation pipelines (ts-jest/babel).

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

### Unified Vite Configuration (vite.config.ts)

Shares identical plugins, alias paths, and CSS pipelines between development and testing:

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "happy-dom",
    setupFiles: "./tests/setup.ts",
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
    },
  },
});
```

### Modern Mocking Utilities (`vi.fn()`, `vi.mock()`)

High-performance module and timer mocking engine:

```typescript
import { vi, test, expect } from "vitest";
import { fetchAnalytics } from "./analytics";

vi.mock("./analytics", () => ({
  fetchAnalytics: vi.fn().mockResolvedValue({ pageViews: 1420 }),
}));

test("loads analytics data cleanly", async () => {
  const data = await fetchAnalytics();
  expect(data.pageViews).toBe(1420);
  expect(fetchAnalytics).toHaveBeenCalledOnce();
});
```

### In-Source Testing

Write tests directly alongside source code (stripped automatically in production builds):

```typescript
// src/math.ts
export function add(a: number, b: number): number {
  return a + b;
}

if (import.meta.vitest) {
  const { it, expect } = import.meta.vitest;
  it("adds two numbers correctly", () => {
    expect(add(2, 3)).toBe(5);
  });
}
```

## Common Patterns

### In-Source Testing and Fast Mocking

**Problem**: Context switching between source files and test files for small pure utility functions.

**Solution**:
Use Vitest in-source testing or vi mocks:

```typescript
import { vi, test, expect } from "vitest";
import { sendNotification } from "./notifier";

vi.mock("./notifier", () => ({
  sendNotification: vi.fn(),
}));

test("triggers notification with formatted message", async () => {
  sendNotification("Welcome to Vitest");
  expect(sendNotification).toHaveBeenCalledWith("Welcome to Vitest");
});
```

## Best Practices

**Do**:

- Use `happy-dom` Instead of `jsdom`: Choose `environment: 'happy-dom'` for 2-3x faster DOM simulation performance.
- Leverage V8 Coverage Provider: Use `coverage.provider: 'v8'` for instant, precise native code coverage reports.
- Use `vi.hoisted()` for Dynamic Mock Pre-Execution: Initialize variables needed inside `vi.mock()` factories cleanly.
- Use In-Source Testing for Pure Utility Modules: Colocate tests inside utility files for rapid feedback during development.

**Don't**:

- Use separate Babel / ts-jest configurations: Rely on Vitest's native Vite pipeline; eliminate extra transpilers.
- Forget `vi.restoreAllMocks()`: Reset spies between tests to prevent test pollution in watch mode.
- Mock global fetch manually: Use `vi.spyOn(globalThis, 'fetch')` or MSW for standardized network mocks.

## Troubleshooting

| Error                                     | Cause                                                                   | Solution                                                                    |
| :---------------------------------------- | :---------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `Error: Failed to resolve import`         | Path alias defined in `tsconfig.json` not mirrored in `vite.config.ts`. | Install `vite-tsconfig-paths` plugin in `vite.config.ts`.                   |
| `ReferenceError: document is not defined` | Testing DOM/browser components without happy-dom or jsdom.              | Set `// @vitest-environment jsdom` at top of file or in `vitest.config.ts`. |
| `TypeError: vi.mock is not hoisted`       | Using variables defined outside `vi.mock` inside the mock factory.      | Pass inline implementations or use `vi.hoisted` to declare variables.       |

## References

- [Vitest Documentation](https://vitest.dev/)
