---
name: chai
description: Expert Chai assertion library assistance covering Should, Expect, and Assert styles. Use when writing BDD/TDD assertions, testing JavaScript/TypeScript applications, or validating API responses.
---

# Chai

Chai is an assertion library. It pairs naturally with Mocha. It supports TDD (`assert`) and BDD (`expect`, `should`) styles.

## When to Use

- **BDD/TDD Assertion Library**: Pairing with test runners like Mocha to write expressive, human-readable assertions in JavaScript/TypeScript.
- **Expect / Should / Assert Syntax**: Choosing between chainable BDD assertions (`expect(foo).to.be.a('string')`) and classical TDD `assert`.
- **Deep Object & Array Equality**: Comparing nested objects, array sets, and property structures effortlessly.
- **Plugin Ecosystem (chai-as-promised, chai-http)**: Extending assertion vocabularies with async promises and HTTP response assertions.

## Quick Start

```javascript
import { expect } from "chai";

const foo = "bar";
const beverages = { tea: ["chai", "matcha", "oolong"] };

expect(foo).to.be.a("string");
expect(foo).to.equal("bar");
expect(foo).to.have.lengthOf(3);
expect(beverages).to.have.property("tea").with.lengthOf(3);
```

## Core Concepts

#Chainable Language Chains (BDD Style)

Chai uses natural English chaining words (`to`, `be`, `have`, `and`, `with`, `at`, `of`):

```typescript
import { expect } from "chai";

expect(user).to.be.an("object").that.has.property("email");
expect(user.roles).to.be.an("array").that.includes("admin");
expect(user.score).to.be.at.least(0).and.below(100);
```

#Deep Equality vs Strict Identity

Distinguishes between memory reference equality and structural value equality:

```typescript
const actual = { id: 1, tags: ["web", "api"] };
const expected = { id: 1, tags: ["web", "api"] };

// Strict reference identity (FAILS)
// expect(actual).to.equal(expected);

// Deep structural equality (PASSES)
expect(actual).to.deep.equal(expected);
```

#Asynchronous Promise Assertions (chai-as-promised)

Asserts on resolved and rejected promise outcomes cleanly:

```typescript
import chai, { expect } from "chai";
import chaiAsPromised from "chai-as-promised";
chai.use(chaiAsPromised);

await expect(fetchUserData("invalid_id")).to.be.rejectedWith(
  Error,
  "User not found",
);
```

## Common Patterns

### Deep Object and Schema Verification

**Problem**: Standard shallow equality fails to detect deeply nested object mismatches or unexpected keys.

**Solution**:
Combine `to.deep.include` and type assertions:

```javascript
import { expect } from "chai";

it("validates nested user response", () => {
  const user = {
    id: 1,
    profile: { name: "Alice", roles: ["admin", "editor"] },
  };
  expect(user).to.be.an("object");
  expect(user).to.have.nested.property("profile.name", "Alice");
  expect(user.profile.roles).to.include("admin").and.have.lengthOf(2);
});
```

## Best Practices (2026)

**Do**:

- **Prefer `expect` over `should`**: `expect` works cleanly with `null` and `undefined` without extending `Object.prototype`.
- **Use `deep.equal` for Objects and Arrays**: Prevent false negatives caused by comparing distinct object references.
- **Provide Custom Assertion Failure Messages**: Pass custom descriptions as the second argument (`expect(val, 'User balance must match ledger').to.equal(100)`).
- **Always Await `chai-as-promised`**: Forgetting `await` on promise assertions results in unhandled promise rejections.

**Don't**:

- **Don't write orphan chains**: Writing `expect(val).to.be.true;` in environments without function call getters can lead to silent passes if mistyped.
- **Don't use `assert` and `expect` interchangeably in the same suite**: Standardize on one assertion style across the team.
- **Don't forget to install `@types/chai`**: Ensure strict TypeScript typings are active in TS projects.

## Troubleshooting

| Error                                                 | Cause                                                    | Solution                                                         |
| :---------------------------------------------------- | :------------------------------------------------------- | :--------------------------------------------------------------- |
| `AssertionError: expected { ... } to equal { ... }`   | Using `equal` (strict equality) instead of `deep.equal`. | Replace `.to.equal()` with `.to.deep.equal()`.                   |
| `TypeError: expect(...).to.be.true is not a function` | Calling Chai properties as functions.                    | Use `.to.be.true` as a property getter, or install `dirty-chai`. |
| `UnhandledPromiseRejection in chai-as-promised`       | Missing `await` before asynchronous expectation.         | Prefix assertion with `await expect(promise).to.eventually...`.  |

## References

- [Chai Documentation](https://www.chaijs.com/)
