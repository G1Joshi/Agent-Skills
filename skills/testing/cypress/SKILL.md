---
name: cypress
description: Expert Cypress testing assistance covering end-to-end, component testing, and intercepting network calls. Use when writing E2E tests, automating user workflows, or mocking network endpoints.
---

# Cypress

Cypress is a next generation front end testing tool built for the modern web. It runs _inside_ the browser (unlike Selenium/Playwright) which gives it native access to the DOM.

## When to Use

- **Component & End-to-End Web Testing**: Running browser-based functional tests directly inside Chrome, Firefox, and Edge.
- **Time-Travel Debugging**: Stepping back through snapshots of DOM state taken during test command execution.
- **Network Interception & Mocking**: Stubbing API responses, delaying network latency, and testing edge error cases with `cy.intercept()`.
- **Component Isolation Testing**: Testing isolated React, Vue, Svelte, or Angular components without bootstrapping full backends.

## Quick Start

```javascript
describe("My First Test", () => {
  it("Visits the Kitchen Sink", () => {
    cy.visit("https://example.cypress.io");
    cy.contains("type").click();
    cy.url().should("include", "/commands/actions");
    cy.get(".action-email")
      .type("fake@email.com")
      .should("have.value", "fake@email.com");
  });
});
```

## Core Concepts

### Asynchronous Command Queuing & Automatic Retries

Cypress commands do not return standard promises; they queue actions that automatically retry until assertions pass or timeout:

```typescript
// cypress/e2e/login.cy.ts
describe("Authentication Flow", () => {
  it("logs in user and displays dashboard", () => {
    cy.visit("/login");

    // Automatically retries until element exists and is visible
    cy.get('input[name="email"]').type("jane@example.com");
    cy.get('input[name="password"]').type("Password123!");
    cy.get('button[type="submit"]').click();

    // Asserts on URL and DOM content
    cy.url().should("include", "/dashboard");
    cy.contains("h1", "Welcome back, Jane").should("be.visible");
  });
});
```

### Network Interception & Dynamic Fixture Stubbing (`cy.intercept`)

Controls and mocks network traffic without external proxy dependencies:

```typescript
it("handles network failure gracefully", () => {
  cy.intercept("GET", "/api/v1/projects", {
    statusCode: 500,
    body: { error: "Internal Server Error" },
  }).as("getProjectsError");

  cy.visit("/projects");
  cy.wait("@getProjectsError");

  cy.get(".error-banner").should("contain.text", "Failed to load projects");
});
```

### Custom Commands & Page Object Encapsulation

Encapsulates reusable user workflows:

```typescript
// cypress/support/commands.ts
Cypress.Commands.add("loginViaApi", (email: string, password: string) => {
  cy.request("POST", "/api/v1/auth/login", { email, password }).then((res) => {
    window.localStorage.setItem("authToken", res.body.token);
  });
});
```

## Common Patterns

### Network Request Interception and Waiting

**Problem**: Flaky tests caused by asserting UI before backend API responses have completed and rendered.

**Solution**:
Use `cy.intercept` with route aliases and `cy.wait`:

```javascript
it("loads and displays user profile data", () => {
  cy.intercept("GET", "/api/v1/user", { fixture: "user.json" }).as("getUser");
  cy.visit("/dashboard");
  cy.wait("@getUser");
  cy.get('[data-cy="user-name"]').should("contain.text", "Jane Doe");
});
```

## Best Practices

**Do**:

- Use Dedicated Test Attributes: Select elements using `data-cy` or `data-testid` (`cy.get('[data-cy="submit"]')`) rather than CSS classes.
- Log In Programmatically via API: Bypass UI login forms in setup hooks using `cy.request()` to accelerate test runs.
- Use `cy.intercept()` for Flake-Free Synchronization: Wait on explicit network aliases (`cy.wait('@loadData')`) rather than `cy.wait(3000)`.
- Keep Tests Independent: Each test must be able to run in isolation without depending on state left by previous tests.

**Don't**:

- Use `async/await` with Cypress commands: Cypress manages its own internal command queue; mixing with `async/await` breaks execution order.
- Use hardcoded `cy.wait(number)`: Static delays make test suites slow and flaky.
- Test third-party OAuth providers through the UI: Mock OAuth callbacks or use API token injection.

## Troubleshooting

| Error                                                | Cause                                                   | Solution                                                                             |
| :--------------------------------------------------- | :------------------------------------------------------ | :----------------------------------------------------------------------------------- |
| `CypressError: Timed out retrying after 4000ms`      | Element not found in DOM or covered by another element. | Check selector specificity and wait for loading spinners to detach.                  |
| `cy.visit() failed trying to load`                   | Target dev server is down or SSL certificate untrusted. | Verify base URL in `cypress.config.js` and set `chromeWebSecurity: false` if needed. |
| `Cannot read properties of undefined (reading 'as')` | Chaining assertions incorrectly on cy.intercept.        | Assign `.as('alias')` immediately on `cy.intercept(...)` declaration.                |

## References

- [Cypress Documentation](https://docs.cypress.io/)
