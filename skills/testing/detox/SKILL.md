---
name: detox
description: Detox React Native E2E testing. Use for RN testing.
---

# Detox

Detox is designed for React Native. Unlike Appium (Black-box), Detox works "Gray-box" by running _inside_ your app, monitoring the main thread. It _knows_ when the app is busy/idle, eliminating flaky waits.

## When to Use

- **React Native Apps**: The gold standard for RN E2E.
- **Speed & Stability**: Much less flaky than Appium for RN because of synchronization.
- **CI/CD**: Designed to be fast enough for CI.

## Quick Start

```javascript
describe("Example", () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  it("should show hello screen after tap", async () => {
    await element(by.id("hello_button")).tap();
    await expect(element(by.text("Hello!!!"))).toBeVisible();
  });
});
```

## Core Concepts

### Synchronization

Detox monitors network requests, animations, and timers. It waits for the app to go "Idle" before executing the next command. No `sleep()` needed.

### Matchers

`by.id()`, `by.text()`, `by.label()`. Needs `testID` props on React Native components.

## Best Practices (2025)

**Do**:

- **Add `testID` props**: Add them to all interactive elements in your React Native code.
- **Use `device.reloadReactNative()`**: Faster than relaunching the whole app for every test.
- **Mock Metro**: Mock JS bundles to avoid network flakes in CI.

**Don't**:

- **Don't run animations**: Disable them in the test build for speed and stability.
- **Don't combine with Appium**: Choose one for your project.

## References

- [Detox Documentation](https://wix.github.io/Detox/)
