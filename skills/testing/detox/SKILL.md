---
name: detox
description: Expert Detox mobile E2E automation for React Native applications on iOS and Android. Use when running gray-box integration tests, simulating device interactions, or debugging mobile flakiness.
---

# Detox

Detox is designed for React Native. Unlike Appium (Black-box), Detox works "Gray-box" by running _inside_ your app, monitoring the main thread. It _knows_ when the app is busy/idle, eliminating flaky waits.

## When to Use

- **Gray-Box Mobile E2E Automation**: Testing React Native mobile apps with internal synchronization on iOS and Android.
- **Flake-Free Mobile Testing**: Eliminating manual `sleep()` calls by synchronizing automatically with React Native's bridge and event queue.
- **High-Velocity Release Validation**: Validating critical user journeys on simulators and emulators in mobile CI/CD pipelines.
- **Fast Local Feedback**: Running automated mobile UI tests alongside the React Native packager.

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

### Gray-Box Synchronization Architecture

Detox monitors the app internally (network requests, animations, timers, UI layout passes) and executes actions only when the app is completely idle:

```text
[ Detox Test Runner ] ──(WebSocket)──→ [ Native Detox Agent (Inside App) ]
                                              ├── Monitors React Native Bridge
                                              ├── Tracks Ongoing Network Requests
                                              └── Waits for Zero Pending Animations
```

### Matchers & Actions Hierarchy

Interacts with native elements using accessibility IDs:

```typescript
// e2e/checkout.test.ts
import { by, element, expect } from "detox";

describe("Checkout Flow", () => {
  beforeAll(async () => {
    await device.launchApp({ newInstance: true });
  });

  it("adds item to cart and proceeds to payment", async () => {
    await element(by.id("item_card_101")).tap();
    await element(by.id("add_to_cart_btn")).tap();

    await expect(element(by.id("cart_badge"))).toHaveText("1");
    await element(by.id("cart_icon")).tap();
    await element(by.id("checkout_button")).tap();

    await expect(element(by.text("Payment Options"))).toBeVisible();
  });
});
```

### Device Control & Deep Linking

Controls simulator state, permissions, and URL schemes:

```typescript
it("handles incoming deep links", async () => {
  await device.openURL({ url: "myapp://promo/summer2026" });
  await expect(element(by.id("promo_banner"))).toBeVisible();
});
```

## Common Patterns

### Synchronized User Flow with Test IDs

**Problem**: Test flakiness due to timing differences across mobile platforms.

**Solution**:
Assign `testID` props in React Native and query using `by.id`:

```javascript
describe("Authentication Flow", () => {
  beforeAll(async () => {
    await device.launchApp({ delete: true });
  });

  it("logs in with valid credentials", async () => {
    await element(by.id("email_input")).typeText("user@example.com");
    await element(by.id("password_input")).typeText("secret123");
    await element(by.id("login_button")).tap();
    await expect(element(by.id("welcome_header"))).toBeVisible();
  });
});
```

## Best Practices

**Do**:

- Use `testID` for Element Matching: Assign `testID="my_element"` on React Native components for unambiguous cross-platform matching.
- Disable Infinite Animations during Tests: Infinite loops keep the app permanently busy, preventing Detox from synchronizing.
- Run on Release/Staging Builds in CI: Test release configurations (`configuration: "ios.sim.release"`) for accurate performance metrics.
- Use Mock Servers (MSW or MockServer): Keep external API calls deterministic and isolated from external network outages.

**Don't**:

- Use sleep timeouts: Trust Detox's automatic idle synchronization instead of arbitrary delays.
- Test third-party social auth webviews with Detox: Mock the auth response in the React Native state layer.
- Ignore detox build artifacts: Capture videos and artifacts on failure (`--record-videos failing --take-screenshots failing`).

## Troubleshooting

| Error                                           | Cause                                                             | Solution                                                                            |
| :---------------------------------------------- | :---------------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| `DetoxRuntimeError: App synchronization failed` | Continuous background loops, animations, or timers blocking sync. | Disable indefinite timers in test mode or use `device.disableSynchronization()`.    |
| `Cannot find simulator/emulator`                | Device name in detox configuration does not exist in local SDK.   | Run `xcrun simctl list` or `emulator -list-avds` and update `.detoxrc.js`.          |
| `Test failed: Element not found`                | Native view missing `testID` or collapsed in hierarchy.           | Ensure `testID` is passed to the underlying native component and visible on screen. |

## References

- [Detox Documentation](https://wix.github.io/Detox/)
