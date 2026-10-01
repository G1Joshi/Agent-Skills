---
name: appium
description: Expert Appium mobile automation covering iOS, Android, and cross-platform UI testing. Use when automating mobile app workflows, end-to-end device testing, or configuring Appium drivers.
---

# Appium

Appium is an open-source framework for automating native, mobile web, and hybrid applications on iOS, mobile Android, and Windows desktop platforms. It uses the WebDriver protocol.

## When to Use

- **Cross-Platform Mobile UI Automation**: Automating functional end-to-end tests across native iOS, Android, and mobile web browsers.
- **Real Device Cloud Grid Testing**: Executing mobile regression suites across device clouds (BrowserStack, Sauce Labs, AWS Device Farm).
- **Hybrid & Native App Interactions**: Testing apps that transition between native UI components and embedded WebViews.
- **Physical Hardware Button Testing**: Automating device rotation, biometric dialogs, network toggles, and volume keys.

## Quick Start

```javascript
// wdio.conf.js
capabilities: [
  {
    platformName: "Android",
    "appium:deviceName": "Pixel_3a",
    "appium:app": "/path/to.apk",
    "appium:automationName": "UiAutomator2",
  },
];

// test.js
await $("~Login Button").click(); // Accessibility ID
await $('android=new UiSelector().text("Submit")').click();
```

## Core Concepts

### W3C WebDriver Protocol for Mobile

Appium translates standard W3C WebDriver HTTP wire protocol commands into platform-specific native automation drivers (XCUITest for iOS, UIAutomator2 for Android):

```text
[ Test Script (Node/Python/Java) ] ──(W3C WebDriver)──→ [ Appium Server (Port 4723) ]
                                                              ├──→ [ XCUITest Driver (iOS) ]
                                                              └──→ [ UIAutomator2 Driver (Android) ]
```

### Appium 2.0 Desired Capabilities (Options Classes)

Modern Appium 2.x replaces generic capability maps with strongly-typed platform options:

```typescript
import { remote } from "webdriverio";

const driver = await remote({
  protocol: "http",
  hostname: "127.0.0.1",
  port: 4723,
  path: "/",
  capabilities: {
    platformName: "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "Pixel_8_Pro",
    "appium:app": "/path/to/app-release.apk",
    "appium:autoGrantPermissions": true,
  },
});
```

### Mobile Element Locators & Explicit Waits

Locating elements safely using accessibility identifiers and explicit condition waits:

```typescript
// Prefer accessibility id (cross-platform and resilient)
const submitButton = await driver.$("~submit_order_button");
await submitButton.waitForDisplayed({ timeout: 10000 });
await submitButton.click();
```

## Common Patterns

### Explicit Wait for Dynamic Mobile Elements

**Problem**: Network or animation lag causes `NoSuchElementException` when interacting with mobile elements immediately after screen transitions.

**Solution**:
Use WebDriverWait with expected conditions rather than static sleeps:

```python
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def tap_when_ready(driver, accessibility_id: str, timeout: int = 10):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, accessibility_id))
    )
    element.click()
```

## Best Practices

**Do**:

- Always Prefer Accessibility IDs (`~locator`): Coordinate with mobile developers to assign `accessibilityIdentifier` (iOS) and `contentDescription` (Android).
- Use Appium 2.x Independent Drivers: Install only needed drivers (`appium driver install uiautomator2`) to keep server installations lightweight.
- Implement Explicit Waits Instead of Static Sleep: Use `.waitForDisplayed()` rather than arbitrary `sleep(5000)` pauses.
- Reset State with `noReset` / `fullReset` Intelligently: Use `noReset: true` to avoid reinstalling the app on every single test case.

**Don't**:

- Use XPath locators for mobile hierarchies: XPath traversal on mobile UI trees is extremely slow and brittle across OS updates.
- Hardcode absolute file paths: Use environment variables or relative paths for APK and IPA binaries.
- Ignore Appium Inspector: Use the official Appium Inspector GUI to verify element accessibility hierarchies and attributes.

## Troubleshooting

| Error                                          | Cause                                                 | Solution                                                                               |
| :--------------------------------------------- | :---------------------------------------------------- | :------------------------------------------------------------------------------------- |
| `NoSuchDriverException / Driver not installed` | Missing platform driver in Appium 2.x server.         | Run `appium driver install uiautomator2` or `appium driver install xcuitest`.          |
| `Original error: Could not find 'adb.html'`    | Android SDK `ANDROID_HOME` or `PATH` not set.         | Export `ANDROID_HOME` and add `$ANDROID_HOME/platform-tools` to system PATH.           |
| `WebDriverException: Session not created`      | Capabilities mismatch with connected device/emulator. | Verify `platformVersion`, `deviceName`, and `automationName` match connected hardware. |

## References

- [Appium Documentation](https://appium.io/docs/en/2.0/)
