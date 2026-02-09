---
name: playwright
description: Playwright cross-browser testing with auto-wait and tracing. Use for E2E browser automation.
---

# Playwright

Cross-browser testing with auto-waiting and powerful debugging.

## When to Use

- Cross-browser E2E testing
- Multi-page/context testing
- Visual regression testing
- API testing integration

## Quick Start

```typescript
// tests/login.spec.ts
import { test, expect } from "@playwright/test";

test("should login successfully", async ({ page }) => {
  await page.goto("/login");
  await page.fill('[data-testid="email"]', "user@example.com");
  await page.fill('[data-testid="password"]', "password123");
  await page.click('[data-testid="submit"]');
  await expect(page).toHaveURL(/dashboard/);
});
```

## Core Concepts

### Locators & Actions

```typescript
// Locators (recommended)
page.getByRole("button", { name: "Submit" });
page.getByTestId("email");
page.getByLabel("Email");
page.getByPlaceholder("Enter email");
page.getByText("Welcome");

// Actions
await page.fill("input", "text");
await page.click("button");
await page.selectOption("select", "value");
await page.check('input[type="checkbox"]');
await page.waitForSelector(".loaded");
```

### Assertions

```typescript
// Auto-retrying assertions
await expect(page.getByRole("heading")).toBeVisible();
await expect(page.getByTestId("count")).toHaveText("5");
await expect(page).toHaveURL("/dashboard");
await expect(page).toHaveTitle(/My App/);
await expect(locator).toHaveAttribute("href", "/link");
```

## Common Patterns

### Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.getByTestId("email").fill(email);
    await this.page.getByTestId("password").fill(password);
    await this.page.getByRole("button", { name: "Login" }).click();
  }
}

// Usage in test
test("login flow", async ({ page }) => {
  const loginPage = new LoginPage(page);
  await page.goto("/login");
  await loginPage.login("user@example.com", "password");
});
```

### API Mocking

```typescript
test("mocked api", async ({ page }) => {
  await page.route("/api/users", async (route) => {
    await route.fulfill({
      status: 200,
      body: JSON.stringify([{ id: 1, name: "John" }]),
    });
  });

  await page.goto("/users");
  await expect(page.getByText("John")).toBeVisible();
});
```

## Best Practices

**Do**:

- Use role-based locators
- Leverage auto-waiting
- Use Page Object Model
- Enable tracing for CI

**Don't**:

- Use hardcoded waits
- Chain too many assertions
- Skip accessibility locators
- Ignore test isolation

## Troubleshooting

| Issue          | Cause          | Solution                 |
| -------------- | -------------- | ------------------------ |
| Element hidden | Timing issue   | Use proper locator       |
| Timeout error  | Slow page      | Increase timeout         |
| Flaky test     | Race condition | Use web-first assertions |

## References

- [Playwright Documentation](https://playwright.dev/docs/)
- [Playwright Test](https://playwright.dev/docs/test-intro)
