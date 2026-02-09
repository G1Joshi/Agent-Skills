---
name: detox
description: Detox end-to-end testing for React Native apps. Use for mobile E2E tests.
---

# Detox

End-to-end testing framework for React Native.

## When to Use

- React Native E2E testing
- Automated UI testing
- CI/CD mobile testing
- Cross-platform test suites

## Quick Start

```typescript
// e2e/login.test.ts
describe("Login", () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  it("should login successfully", async () => {
    await element(by.id("email")).typeText("user@example.com");
    await element(by.id("password")).typeText("password123");
    await element(by.id("login-button")).tap();
    await expect(element(by.text("Welcome"))).toBeVisible();
  });
});
```

## Core Concepts

### Matchers

```typescript
// By ID (recommended)
element(by.id("button"));

// By text
element(by.text("Submit"));

// By label (accessibility)
element(by.label("Close"));

// Nested
element(by.id("list")).atIndex(0);
```

### Actions

```typescript
await element(by.id("input")).typeText("Hello");
await element(by.id("input")).clearText();
await element(by.id("button")).tap();
await element(by.id("button")).longPress();
await element(by.id("scroll")).scroll(200, "down");
await element(by.id("refresh")).swipe("down");
```

### Expectations

```typescript
await expect(element(by.id("title"))).toBeVisible();
await expect(element(by.id("title"))).toHaveText("Hello");
await expect(element(by.id("input"))).toHaveFocus();
await expect(element(by.id("modal"))).not.toExist();
```

## Best Practices

**Do**: Use testID props, reset state between tests
**Don't**: Use platform-specific selectors, rely on timing

## References

- [Detox Documentation](https://wix.github.io/Detox/)
