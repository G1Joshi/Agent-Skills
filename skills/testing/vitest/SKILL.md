---
name: vitest
description: Vitest Vite-native testing with ESM and TypeScript. Use for modern frontend tests.
---

# Vitest

Vite-native testing framework for modern JavaScript.

## When to Use

- Vite-based projects
- ESM-first testing
- TypeScript testing
- Fast unit testing

## Quick Start

```typescript
// sum.test.ts
import { describe, it, expect } from "vitest";
import { sum } from "./sum";

describe("sum", () => {
  it("adds two numbers", () => {
    expect(sum(1, 2)).toBe(3);
  });
});
```

## Core Concepts

### Configuration

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "html"],
    },
  },
});
```

### Mocking

```typescript
import { vi, describe, it, expect } from "vitest";
import { fetchUser } from "./api";
import { UserService } from "./UserService";

vi.mock("./api");

describe("UserService", () => {
  it("fetches user data", async () => {
    vi.mocked(fetchUser).mockResolvedValue({ id: "1", name: "John" });

    const service = new UserService();
    const user = await service.getUser("1");

    expect(user.name).toBe("John");
    expect(fetchUser).toHaveBeenCalledWith("1");
  });
});
```

## Common Patterns

### Component Testing

```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';

describe('Counter', () => {
  it('increments count', async () => {
    render(<Counter />);

    await userEvent.click(screen.getByRole('button', { name: 'Increment' }));

    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });
});
```

### In-source Testing

```typescript
// math.ts
export function add(a: number, b: number): number {
  return a + b;
}

if (import.meta.vitest) {
  const { describe, it, expect } = import.meta.vitest;

  describe("add", () => {
    it("adds numbers", () => {
      expect(add(1, 2)).toBe(3);
    });
  });
}
```

## Best Practices

**Do**:

- Use v8 coverage provider
- Enable globals for cleaner tests
- Use in-source testing for utils
- Configure proper environment

**Don't**:

- Mix with Jest unnecessarily
- Skip TypeScript config
- Ignore test isolation
- Use require() in tests

## Troubleshooting

| Issue            | Cause         | Solution       |
| ---------------- | ------------- | -------------- |
| Import error     | ESM issue     | Check config   |
| Mock not working | Wrong vi.mock | Check path     |
| Slow tests       | No pooling    | Enable threads |

## References

- [Vitest Documentation](https://vitest.dev/)
- [Vitest Config](https://vitest.dev/config/)
