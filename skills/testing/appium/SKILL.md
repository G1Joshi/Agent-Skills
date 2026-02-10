---
name: appium
description: Appium mobile app automation. Use for mobile testing.
---

# Appium

Appium is an open-source framework for automating native, mobile web, and hybrid applications on iOS, mobile Android, and Windows desktop platforms. It uses the WebDriver protocol.

## When to Use

- **Real Device Testing**: Testing on physical iPhones/Androids.
- **Cross-Platform**: Write one test (mostly) for both iOS and Android.
- **Black-box Testing**: Testing the app from the outside (like a user) without needing source code access.

## Quick Start (WebdriverIO + Appium)

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

### Drivers

Appium uses drivers to interface with underlying frameworks:

- **XCUITest**: Apple's UI test framework (iOS).
- **UiAutomator2**: Google's UI test framework (Android).

### Appium Inspector

A GUI tool to inspect your mobile app's definition (XML), find element IDs, and record scripts.

## Best Practices (2025)

**Do**:

- **Use Accessibility IDs**: The most robust way to find elements (`~MyID`). Avoid XPath which is slow on mobile.
- **Use Appium 2.0**: The new standard. Driver-based architecture (`appium driver install uiautomator2`).
- **Parallelize**: Use device farms (BrowserStack, SauceLabs) for running on multiple devices.

**Don't**:

- **Don't use hard waits**: Mobile devices vary widely in speed.
- **Don't rely on coordinates**: Different screen sizes will break your tests.

## References

- [Appium Documentation](https://appium.io/docs/en/2.0/)
