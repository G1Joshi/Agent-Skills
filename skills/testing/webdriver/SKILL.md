---
name: webdriver
description: WebDriver browser automation protocol. Use for cross-browser testing.
---

# WebDriver

WebDriver is the W3C standard protocol for controlling web browsers. It is the underlying technology behind Selenium, Appium, WebdriverIO, and more. Even if you use a high-level tool, understanding WebDriver helps debug low-level issues.

## When to Use

- **Protocol Knowledge**: Understanding why `stale element reference` happens.
- **Custom Integration**: Building your own test runner or browser automation tool.
- **WebdriverIO**: A popular Node.js implementation of the WebDriver protocol (often used over raw Selenium).

## Quick Start (WebdriverIO)

```javascript
import { remote } from "webdriverio";

const browser = await remote({
  capabilities: {
    browserName: "chrome",
    "goog:chromeOptions": { args: ["headless", "disable-gpu"] },
  },
});

await browser.url("https://webdriver.io");
const title = await browser.getTitle();
console.log(title); // outputs: "WebdriverIO · Next-gen browser and mobile automation test framework for Node.js"

await browser.deleteSession();
```

## Core Concepts

### Client-Server Architecture

- **Client**: Your test script (Node/Java/Python).
- **Server**: The Browser Driver (chromedriver, geckodriver) or Grid.
- **Protocol**: REST-ish JSON commands (`POST /session/:id/element`).

### Stale Element Reference

A common error. You got a reference to a DOM element (ID: 123), but the page refreshed or JS updated the DOM. ID 123 is gone. You must find the element again.

## Best Practices (2025)

**Do**:

- **Use WebdriverIO (WDIO)**: If you want to use WebDriver in Node.js. It wraps the low-level protocol in a nice, synchronous-looking API.
- **Understand the network**: WebDriver is chatty (many HTTP requests). Running tests "remote" (e.g., SauceLabs) is slower than local due to latency.

**Don't**:

- **Don't mix protocols**: Don't confuse CDP (Puppeteer/Playwright) with WebDriver. They work differently.

## References

- [W3C WebDriver Spec](https://w3c.github.io/webdriver/)
- [WebdriverIO](https://webdriver.io/)
