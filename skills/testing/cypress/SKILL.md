---
name: cypress
description: Cypress end-to-end testing for web apps. Use for E2E testing.
---

# Cypress

Cypress is a next generation front end testing tool built for the modern web. It runs _inside_ the browser (unlike Selenium/Playwright) which gives it native access to the DOM.

## When to Use

- **Dev Experience**: The interactive GUI is best-in-class for debugging.
- **Component Testing**: Testing React/Vue/Angular components in isolation within a real browser.
- **Single Tab**: Testing flows that happen in a single tab/window.

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

### Chaining

Cypress commands run serially. `cy.get().click().should()` reads like a story.

### Automatic Retries

Cypress automatically retries assertions until they pass or timeout.
`cy.get('.todo-list li').should('have.length', 2)` will retry until the list has 2 items or 4 seconds elapse.

### Stubbing

Because it runs in-browser, intercepting network requests (`cy.intercept`) is fast and reliable.

## Best Practices (2025)

**Do**:

- **Use `cy.intercept`**: Wait for network calls to finish before asserting UI. `cy.wait('@apiCall')`.
- **Use Custom Commands**: Extract repetitive logic (login) into `cy.login()`.
- **Use Data Test Attributes**: `data-cy="submit-btn"` allows you to change CSS/JS without breaking tests.

**Don't**:

- **Don't use `wait(number)`**: Never hard-code waits. Wait for routes or elements.
- **Don't test 3rd party sites**: Cypress is for _your_ app. It has safeguards that make testing Google/Github hard.

## References

- [Cypress Documentation](https://docs.cypress.io/)
