---
name: playwright
description: Playwright end-to-end testing for web. Use for browser automation.
---

# Playwright

Playwright is Microsoft's modern automation library. It enables reliable end-to-end testing for modern web apps across Chromium, WebKit, and Firefox.

## When to Use

- **Cross-Browser**: Testing Chrome, Safari, and Firefox with one API.
- **Speed**: It is significantly faster than Cypress and Selenium due to parallel execution and fast context creation.
- **Modern Features**: Native support for Auto-waiting (no more `sleep(1000)`), Network interception, and Mobile emulation.

## Quick Start

```typescript
import { test, expect } from "@playwright/test";

test.describe("Navigation", () => {
  test("should navigate to login", async ({ page }) => {
    await page.goto("https://example.com");
    await page.getByRole("button", { name: "Log in" }).click();
    await expect(page).toHaveURL(/.*login/);
  });
});
```

## Core Concepts

### Auto-waiting

Playwright waits for elements to be actionable (visible, stable, not obscured) before performing actions.

### Browser Contexts

Playwright creates a fresh "Context" (Incognito profile) for each test in milliseconds. This provides full isolation without the overhead of restarting the browser process.

### Locators

`page.getByRole('button')` is strict. If it finds two buttons, it throws an error (forcing you to be specific), avoiding flakiness.

## Best Practices (2025)

**Do**:

- **Use Locators**: `page.locator()` or `page.getByRole()` instead of `$` or `$$`.
- **Use `codegen`**: Run `npx playwright codegen` to record user interactions and generate test code automatically.
- **Use UI Mode**: `npx playwright test --ui` for a time-travel debugging experience.

**Don't**:

- **Don't use Xpath/CSS selectors**: They are brittle. Use user-facing locators (Role, Text).
- **Don't use extensive waits**: Trust the auto-waiting mechanism.

## References

- [Playwright Documentation](https://playwright.dev/)
