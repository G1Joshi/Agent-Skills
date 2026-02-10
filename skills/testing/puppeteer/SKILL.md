---
name: puppeteer
description: Puppeteer headless Chrome automation. Use for browser automation.
---

# Puppeteer

Puppeteer is a Node library which provides a high-level API to control Chrome or Chromium over the DevTools Protocol.

## When to Use

- **Chrome Specific**: If testing cross-browser isn't a priority (or you only care about Chromium).
- **Web Scraping**: Excellent for scraping SPAs because it renders JS.
- **PDF/Screenshots**: The industry standard for "HTML to PDF" generation.

## Quick Start

```javascript
import puppeteer from "puppeteer";

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto("https://developer.chrome.com/");
  await page.pdf({ path: "dv.pdf", format: "A4" });

  await browser.close();
})();
```

## Core Concepts

### DevTools Protocol (CDP)

Puppeteer talks directly to Chrome via CDP. This allows deeper control (intercepting network at a low level, CPU profiling) than WebDriver.

### Headless by Default

Puppeteer launches Chrome in headless mode by default. Use `headless: false` to see it.

## Best Practices (2025)

**Do**:

- **Use `page.waitForSelector`**: Before clicking or scraping.
- **Use `stealth` plugins**: If scraping, use `puppeteer-extra-plugin-stealth` to avoid detection.
- **Use Playwright**: _Consider_ switching. Playwright is maintained by the team that built Puppeteer (after moving to Microsoft) and has a better API.

**Don't**:

- **Don't leak browsers**: Always ensure `browser.close()` is called in a `finally` block or via a test runner hook.

## References

- [Puppeteer Documentation](https://pptr.dev/)
