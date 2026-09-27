---
name: playwright
description: Expert Playwright testing assistance covering cross-browser E2E, auto-waiting, visual comparisons, and tracing. Use when automating modern web applications, testing Chromium/Firefox/WebKit, or debugging flakiness.
---

# Playwright

Playwright is Microsoft's modern automation library. It enables reliable end-to-end testing for modern web apps across Chromium, WebKit, and Firefox.

## When to Use

- **Modern Web End-to-End Automation**: The industry standard for cross-browser testing across Chromium, WebKit (Safari), and Firefox.
- **Multi-Tab & Multi-Origin Testing**: Testing complex workflows spanning popups, payment gateways, and multiple browser tabs seamlessly.
- **Mobile Emulation & Geolocation**: Simulating iPhone, Pixel, network throttling, and geographic permissions reliably.
- **API Testing Alongside UI**: Sending REST and GraphQL requests directly within tests via `request` context.

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

#Auto-Waiting & Resilient Locators

Playwright automatically waits for elements to be attached, visible, stable, and receive events before clicking:

```typescript
// tests/checkout.spec.ts
import { test, expect } from "@playwright/test";

test("customer can complete checkout", async ({ page }) => {
  await page.goto("/catalog");

  // Locates using accessible role and auto-waits
  await page.getByRole("button", { name: "Add to Cart" }).first().click();
  await page.getByRole("link", { name: "View Cart" }).click();

  await expect(page.getByTestId("cart-total")).toHaveText("$49.99");
  await page.getByRole("button", { name: "Checkout" }).click();

  await expect(page).toHaveURL(/.*checkout\/success/);
});
```

#Trace Viewer for Post-Mortem Debugging

Records DOM snapshots, console logs, network waterfalls, and action videos during test runs:

```bash
# Run tests and record trace on failure
npx playwright test --trace on-first-retry

# View interactive trace viewer
npx playwright show-trace trace.zip
```

#Network Mocking & HAR Replay

Intercepts requests and fulfills them with mock responses:

```typescript
test("displays error banner on API failure", async ({ page }) => {
  await page.route("**/api/v1/inventory", (route) => {
    route.fulfill({
      status: 503,
      body: JSON.stringify({ error: "Service Unavailable" }),
    });
  });

  await page.goto("/inventory");
  await expect(
    page.getByText("Inventory service is currently offline"),
  ).toBeVisible();
});
```

## Common Patterns

### Page Object Model with Locator Auto-Waiting

**Problem**: Raw selector strings scattered across test files cause maintenance headaches when UI layouts change.

**Solution**:
Encapsulate selectors and actions in Page Objects:

```typescript
import { Page, Locator } from "@playwright/test";

export class LoginPage {
  readonly page: Page;
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.usernameInput = page.getByLabel("Username");
    this.passwordInput = page.getByLabel("Password");
    this.loginButton = page.getByRole("button", { name: "Log in" });
  }

  async login(user: string, pass: string) {
    await this.usernameInput.fill(user);
    await this.passwordInput.fill(pass);
    await this.loginButton.click();
  }
}
```

## Best Practices (2026)

**Do**:

- **Prefer User-Facing Locators**: Use `page.getByRole()`, `page.getByText()`, and `page.getByLabel()` over fragile CSS selectors.
- **Use Web-First Assertions**: Always use `await expect(locator).toBeVisible()` which automatically retries until passing.
- **Reuse Storage State for Fast Authentication**: Save auth cookies with `storageState` to log in once rather than in every test.
- **Run in Parallel Across Browsers**: Leverage Playwright's native worker parallelization across Chromium, WebKit, and Firefox.

**Don't**:

- **Don't use `page.waitForTimeout(5000)`**: Static delays cause flakiness; wait for locators or network states instead.
- **Don't rely on XPath selectors**: XPath selectors break easily when DOM hierarchies shift.
- **Don't share state between tests**: Use independent `BrowserContext` instances to ensure zero test cross-contamination.

## Troubleshooting

| Error                                                          | Cause                                                      | Solution                                                                    |
| :------------------------------------------------------------- | :--------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `TimeoutError: page.waitForSelector: Timeout 30000ms exceeded` | Target element never entered visible DOM state.            | Check selector in Playwright Inspector using `npx playwright test --debug`. |
| `Target closed / browser disconnected`                         | Container or system ran out of shared memory (`/dev/shm`). | Run container with `--shm-size=2gb` or set `chromiumSandbox: false`.        |
| `Strict mode violation: getByRole(...) resolved to 2 elements` | Selector matches more than one visible element.            | Disambiguate using `.first()`, index, or more specific locator text.        |

## References

- [Playwright Documentation](https://playwright.dev/)
