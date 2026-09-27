---
name: jest
description: Expert Jest testing assistance covering unit testing, snapshot testing, mocking, and coverage reports. Use when writing tests for JavaScript/TypeScript, React, Node.js, or Next.js applications.
---

# Jest

Jest is a delightful JavaScript Testing Framework with a focus on simplicity. It works with projects using: Babel, TypeScript, Node, React, Angular, Vue, and more.

## When to Use

- **JavaScript & TypeScript Unit Testing**: Standard, battery-included test runner for React, Node.js, and legacy frontend projects.
- **Snapshot Testing**: Freezing and asserting on large rendered component output, GraphQL responses, or JSON configurations.
- **Comprehensive Mocking Engine**: Spying on, mocking, and stubbing functions, timers, and entire modules with `jest.mock()`.
- **Code Coverage Reporting**: Generating built-in Istanbul code coverage metrics without external plugins.

## Quick Start

```javascript
// sum.js
function sum(a, b) {
  return a + b;
}
module.exports = sum;

// sum.test.js
const sum = require("./sum");

test("adds 1 + 2 to equal 3", () => {
  expect(sum(1, 2)).toBe(3);
});
```

## Core Concepts

#Module Mocking & Function Spies (`jest.fn()`, `jest.mock()`)

Replaces dependencies with mock implementations:

```typescript
// service.test.ts
import { sendWelcomeEmail } from "./mailer";
import { registerUser } from "./user.service";

jest.mock("./mailer", () => ({
  sendWelcomeEmail: jest.fn().mockResolvedValue(true),
}));

test("sends welcome email upon registration", async () => {
  const result = await registerUser("test@example.com");
  expect(result.success).toBe(true);
  expect(sendWelcomeEmail).toHaveBeenCalledWith("test@example.com");
  expect(sendWelcomeEmail).toHaveBeenCalledTimes(1);
});
```

#Fake Timers for Asynchronous Delays

Fast-forwards debounce timers, intervals, and timeouts instantaneously:

```typescript
test("debounced search triggers after 300ms", () => {
  jest.useFakeTimers();
  const searchMock = jest.fn();

  triggerDebouncedSearch(searchMock, "query");
  expect(searchMock).not.toHaveBeenCalled();

  // Fast forward clock
  jest.advanceTimersByTime(300);
  expect(searchMock).toHaveBeenCalledWith("query");
  jest.useRealTimers();
});
```

#Snapshot Assertions

Detects unintended regressions in complex structures:

```typescript
test("matches expected invoice schema snapshot", () => {
  const invoice = generateInvoiceTemplate();
  expect(invoice).toMatchSnapshot();
});
```

## Common Patterns

### Mocking External Modules and Spying on Calls

**Problem**: Unit tests hitting third-party SDKs or database clients slow down test runs and produce side effects.

**Solution**:
Use `jest.mock` and `jest.spyOn`:

```typescript
import axios from "axios";
import { fetchUserData } from "./userService";

jest.mock("axios");
const mockedAxios = axios as jest.Mocked<typeof axios>;

test("fetches successfully data from an API", async () => {
  const data = { id: 1, name: "John" };
  mockedAxios.get.mockResolvedValueOnce({ data });

  const result = await fetchUserData(1);
  expect(result).toEqual(data);
  expect(mockedAxios.get).toHaveBeenCalledWith("/api/users/1");
});
```

## Best Practices (2026)

**Do**:

- **Clear Mocks Between Tests**: Enable `clearMocks: true` in `jest.config.js` to prevent call count contamination across tests.
- **Use `@swc/jest` for Fast TypeScript Compilation**: Replace slow `ts-jest` with SWC compiler to dramatically accelerate execution.
- **Use `test.each` for Table-Driven Test Cases**: Consolidate repetitive test scenarios into parameterized tables.
- **Keep Snapshots Small**: Avoid snapshotting massive DOM trees; snapshot focused component states and data contracts.

**Don't**:

- **Don't blindly update snapshots (`-u`)**: Review snapshot diffs carefully before accepting changes to prevent approving bugs.
- **Don't mock what you don't own**: Avoid mocking third-party libraries excessively; prefer integration tests with real adapters where possible.
- **Don't leave hanging asynchronous promises**: Always return promises or `await` async calls to avoid unhandled rejections.

## Troubleshooting

| Error                                            | Cause                                                                        | Solution                                                            |
| :----------------------------------------------- | :--------------------------------------------------------------------------- | :------------------------------------------------------------------ |
| `Cannot use import statement outside a module`   | Jest attempting to execute ESM files without proper Babel/ts-jest transform. | Configure `ts-jest` or set `"transform": {}` in `jest.config.js`.   |
| `A worker process has failed to exit gracefully` | Open handles, database connections, or active timers remaining.              | Run with `--detectOpenHandles` and close connections in `afterAll`. |
| `Snapshot mismatch error`                        | Intended UI or markup change failed snapshot assertion.                      | Review diff and update snapshots with `jest -u`.                    |

## References

- [Jest Documentation](https://jestjs.io/)
