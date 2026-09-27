---
name: mocha
description: Expert Mocha testing assistance covering test runners, hooks, asynchronous assertions, and reporters. Use when structuring Node.js test suites, running unit tests, or configuring CI test reporters.
---

# Mocha

Mocha is a flexible JavaScript test framework. Unlike Jest, it does _not_ come with an assertion library, mocking, or snapshotting built-in. It is a runner that allows you to choose your own tools (usually Chai + Sinon).

## When to Use

- **Flexible Node.js & Browser Testing**: A customizable test runner providing BDD (`describe`/`it`) and TDD test interfaces.
- **Customizable Assertion & Mocking Pairs**: Pairing with preferred assertion libraries (Chai) and mocking toolkits (Sinon.js).
- **Asynchronous Execution Control**: Testing callbacks, promises, and async/await with granular timeout controls.
- **Established Node.js Codebases**: Maintaining and extending mature enterprise backend JavaScript services.

## Quick Start

```javascript
// npm install --save-dev mocha chai
const assert = require("chai").assert;

describe("Array", function () {
  describe("#indexOf()", function () {
    it("should return -1 when the value is not present", function () {
      assert.equal([1, 2, 3].indexOf(4), -1);
    });
  });
});
```

## Core Concepts

#BDD Interface & Hooks Lifecycle

Coordinates test execution and lifecycle fixtures cleanly:

```typescript
import { expect } from "chai";

describe("Payment Gateway Service", () => {
  before(async () => {
    // Run once before all tests in this block (e.g. connect to DB)
  });

  beforeEach(() => {
    // Run before each test (e.g. reset state)
  });

  it("successfully processes valid card charge", async () => {
    const receipt = await processCharge(100);
    expect(receipt.status).to.equal("SUCCESS");
  });

  after(() => {
    // Run once after all tests (e.g. close connection)
  });
});
```

#Granular Timeout & Retry Configuration

Controls timeouts for slow network or integration operations:

```typescript
it("completes slow third-party reconciliation", function (done) {
  this.timeout(5000); // Override default 2000ms timeout
  this.retries(2); // Retry up to 2 times on intermittent failure

  reconcileLedgers()
    .then(() => done())
    .catch(done);
});
```

#Declarative .mocharc.json Configuration

```json
{
  "extension": ["ts"],
  "spec": "tests/**/*.spec.ts",
  "require": "ts-node/register",
  "timeout": 4000,
  "reporter": "spec"
}
```

## Common Patterns

### Test Fixture Hooks with Cleanup

**Problem**: Leaked database state across test suites causes cascading false-positive failures.

**Solution**:
Use `before`, `beforeEach`, and `afterEach` lifecycle hooks:

```javascript
describe("Order Processing Service", () => {
  let dbConnection;

  before(async () => {
    dbConnection = await createTestDatabase();
  });

  after(async () => {
    await dbConnection.close();
  });

  beforeEach(async () => {
    await dbConnection.truncateAll();
  });

  it("creates an order successfully", async () => {
    const order = await createOrder({ item: "book" });
    assert.strictEqual(order.status, "CONFIRMED");
  });
});
```

## Best Practices (2026)

**Do**:

- **Use Regular Functions When Accessing `this.timeout()`**: Arrow functions bind lexical context and break Mocha's `this` context binding.
- **Commit a `.mocharc.json` Config**: Centralize timeout, reporter, and file patterns in a committed configuration file.
- **Use Parallel Test Execution**: Enable `--parallel` in `.mocharc.json` on multi-core CI runners to accelerate test runs.
- **Pair with Sinon for Stubs**: Use `sinon.stub()` and `sinon.spy()` for isolated unit test dependencies.

**Don't**:

- **Don't mix callback `done()` and `async/await`**: Mixing both causes multiple callback invocation errors.
- **Don't leave `.only()` committed**: Use ESLint rules (`no-exclusive-tests`) to prevent committed `.only` blocks from skipping test suites.
- **Don't rely on arbitrary static delays**: Use explicit polling helpers rather than `setTimeout` delays.

## Troubleshooting

| Error                                 | Cause                                                                 | Solution                                                                       |
| :------------------------------------ | :-------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| `Error: Timeout of 2000ms exceeded`   | Asynchronous test did not complete within default 2-second timeout.   | Increase timeout using `this.timeout(5000)` or pass `--timeout 5000` CLI flag. |
| `Error: done() called multiple times` | Callback-style test invoked `done()` both in success and error paths. | Return a Promise instead of using the `done` callback.                         |
| `TypeError: describe is not defined`  | Executing test file with `node` instead of `npx mocha`.               | Run using `npx mocha path/to/test.js`.                                         |

## References

- [Mocha Documentation](https://mochajs.org/)
