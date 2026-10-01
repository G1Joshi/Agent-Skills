---
name: puppeteer
description: Expert Puppeteer automation covering headless Chrome, PDF generation, web scraping, and performance tracing. Use when generating screenshots/PDFs, automating browser interactions, or crawling JavaScript web apps.
---

# Puppeteer

Puppeteer is a Node library which provides a high-level API to control Chrome or Chromium over the DevTools Protocol.

## When to Use

- **Headless Chrome Automation & Scraping**: High-performance headless browser control for web scraping, automation, and crawling.
- **Server-Side PDF & Screenshot Generation**: Rendering HTML templates into pixel-perfect PDFs and high-resolution screenshots.
- **Single-Page App Prerendering**: Pre-rendering client-side SPAs into static HTML for SEO indexing.
- **Chrome DevTools Protocol (CDP) Access**: Tapping directly into raw Chrome DevTools Protocol events, performance profiling, and heap snapshots.

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

### Browser & Page Architecture over CDP

Puppeteer manages Chrome processes over WebSocket connections using the Chrome DevTools Protocol:

```typescript
import puppeteer from "puppeteer";

const browser = await puppeteer.launch({
  headless: "new",
  args: ["--no-sandbox", "--disable-setuid-sandbox"],
});

const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080 });
await page.goto("https://example.com", { waitUntil: "networkidle0" });
```

### PDF Generation with CSS Print Styles

Renders printable documents directly from HTML:

```typescript
await page.pdf({
  path: "invoice.pdf",
  format: "A4",
  printBackground: true,
  margin: { top: "20mm", bottom: "20mm", left: "15mm", right: "15mm" },
});
```

### Page Evaluation in Browser Context

Executes JavaScript inside the browser context and serializes results back to Node:

```typescript
const articleTitles = await page.evaluate(() => {
  return Array.from(document.querySelectorAll("h2.article-title")).map((el) =>
    el.textContent?.trim(),
  );
});
console.log("Scraped Titles:", articleTitles);
```

## Common Patterns

### PDF Generation with Clean Print Styles

**Problem**: Screen styles and dynamic elements render poorly when converting web pages to PDFs.

**Solution**:
Emulate print media before generating high-res PDF:

```javascript
import puppeteer from "puppeteer";

async function generateInvoicePdf(url, outputPath) {
  const browser = await puppeteer.launch({ headless: "new" });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: "networkidle0" });
  await page.emulateMediaType("print");
  await page.pdf({
    path: outputPath,
    format: "A4",
    printBackground: true,
    margin: { top: "20mm", bottom: "20mm", left: "15mm", right: "15mm" },
  });
  await browser.close();
}
```

## Best Practices

**Do**:

- Use `headless: 'new'`: Leverage Chrome's modern native headless mode for identical rendering to headful Chrome.
- Always Close Browsers in `finally` Blocks: Wrap browser actions in `try/finally` to prevent orphaned Chrome zombie processes.
- Block Unnecessary Assets during Scraping: Block images, fonts, and tracking scripts via `page.setRequestInterception(true)` to speed up scraping 3-5x.
- Use `waitUntil: 'networkidle0'` for SPAs: Ensure all client-side JavaScript hydration requests finish before taking screenshots.

**Don't**:

- Pass raw browser DOM elements back to Node: Serialize return values to JSON or extract primitive values inside `page.evaluate()`.
- Launch a new browser instance for every request: Reuse a single browser instance and create/close lightweight `page` contexts.
- Run Chrome as root without sandboxing precautions: Follow secure Docker non-root user setup guidelines.

## Troubleshooting

| Error                                                                  | Cause                                                                           | Solution                                                                          |
| :--------------------------------------------------------------------- | :------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------- |
| `Error: Failed to launch the browser process!`                         | Missing shared library dependencies (libnss3, libasound2) in Linux environment. | Install required dependencies or use `chrome-aws-lambda` in serverless.           |
| `Execution context was destroyed, most likely because of a navigation` | Attempting to interact with an element after page redirected.                   | Re-query locator after `page.waitForNavigation()` resolves.                       |
| `TimeoutError: Navigation timeout of 30000 ms exceeded`                | Network request still open preventing `networkidle0`.                           | Use `networkidle2` or set custom timeout in `page.goto(url, { timeout: 60000 })`. |

## References

- [Puppeteer Documentation](https://pptr.dev/)
