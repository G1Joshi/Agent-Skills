---
name: jest
description: Jest testing framework with mocking and snapshot testing. Use for JavaScript/TypeScript tests.
---

# Jest

JavaScript testing framework with built-in mocking.

## When to Use

- Unit testing JavaScript/TypeScript
- React component testing
- Snapshot testing
- Mocking dependencies

## Quick Start

```typescript
// sum.test.ts
import { sum } from "./sum";

describe("sum", () => {
  it("adds two numbers", () => {
    expect(sum(1, 2)).toBe(3);
  });

  it("handles negative numbers", () => {
    expect(sum(-1, 1)).toBe(0);
  });
});
```

## Core Concepts

### Matchers

```typescript
// Common matchers
expect(value).toBe(expected); // Strict equality
expect(value).toEqual(expected); // Deep equality
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(array).toContain(item);
expect(string).toMatch(/regex/);
expect(fn).toThrow(Error);
expect(promise).resolves.toBe(value);
expect(promise).rejects.toThrow();
```

### Mocking

```typescript
import { fetchUser } from "./api";
import { UserService } from "./UserService";

jest.mock("./api");

const mockedFetchUser = fetchUser as jest.MockedFunction<typeof fetchUser>;

describe("UserService", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("fetches user data", async () => {
    mockedFetchUser.mockResolvedValue({ id: "1", name: "John" });

    const service = new UserService();
    const user = await service.getUser("1");

    expect(user.name).toBe("John");
    expect(mockedFetchUser).toHaveBeenCalledWith("1");
  });
});
```

## Common Patterns

### Async Testing

```typescript
it("handles async operations", async () => {
  const result = await fetchData();
  expect(result).toBeDefined();
});

it("handles promises", () => {
  return expect(asyncFn()).resolves.toBe("value");
});

it("handles callbacks", (done) => {
  callback((result) => {
    expect(result).toBe("value");
    done();
  });
});
```

### Snapshot Testing

```typescript
import { render } from '@testing-library/react';
import { Button } from './Button';

it('matches snapshot', () => {
  const { container } = render(<Button label="Click me" />);
  expect(container).toMatchSnapshot();
});
```

## Best Practices

**Do**:

- Use descriptive test names
- Mock external dependencies
- Test edge cases
- Keep tests isolated

**Don't**:

- Test implementation details
- Share state between tests
- Use too many snapshots
- Skip cleanup

## Troubleshooting

| Issue            | Cause             | Solution               |
| ---------------- | ----------------- | ---------------------- |
| Test timeout     | Async not awaited | Add await or done()    |
| Mock not working | Wrong path        | Check module path      |
| Flaky tests      | Shared state      | Use beforeEach cleanup |

## References

- [Jest Documentation](https://jestjs.io/docs/)
- [Testing Library](https://testing-library.com/)
