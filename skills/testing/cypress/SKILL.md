---
name: cypress
description: Cypress end-to-end testing with time travel and debugging. Use for E2E browser tests.
---

# Cypress

End-to-end testing framework for web applications.

## When to Use

- End-to-end web testing
- Component testing
- Visual regression testing
- API testing

## Quick Start

```typescript
// cypress/e2e/login.cy.ts
describe("Login", () => {
  it("should login successfully", () => {
    cy.visit("/login");
    cy.get('[data-testid="email"]').type("user@example.com");
    cy.get('[data-testid="password"]').type("password123");
    cy.get('[data-testid="submit"]').click();
    cy.url().should("include", "/dashboard");
  });
});
```

## Core Concepts

### Selectors & Actions

```typescript
// Selecting elements
cy.get(".class-name");
cy.get("#id");
cy.get('[data-testid="element"]');
cy.contains("Button Text");
cy.get("input").first();
cy.get("li").eq(2);

// Actions
cy.get("input").type("text");
cy.get("button").click();
cy.get("select").select("option");
cy.get("input").clear();
cy.get("form").submit();
```

### Assertions

```typescript
// Should assertions
cy.get("h1").should("be.visible");
cy.get("input").should("have.value", "text");
cy.url().should("include", "/page");
cy.get(".list").should("have.length", 3);

// Chained assertions
cy.get("button")
  .should("be.visible")
  .and("be.enabled")
  .and("contain", "Submit");
```

## Common Patterns

### Custom Commands

```typescript
// cypress/support/commands.ts
Cypress.Commands.add("login", (email: string, password: string) => {
  cy.visit("/login");
  cy.get('[data-testid="email"]').type(email);
  cy.get('[data-testid="password"]').type(password);
  cy.get('[data-testid="submit"]').click();
});

// Usage
cy.login("user@example.com", "password");
```

### API Mocking

```typescript
describe("Users", () => {
  beforeEach(() => {
    cy.intercept("GET", "/api/users", {
      fixture: "users.json",
    }).as("getUsers");
  });

  it("displays users", () => {
    cy.visit("/users");
    cy.wait("@getUsers");
    cy.get('[data-testid="user-card"]').should("have.length", 3);
  });
});
```

## Best Practices

**Do**:

- Use data-testid attributes
- Create custom commands
- Use fixtures for test data
- Implement proper waits

**Don't**:

- Use CSS selectors only
- Chain too many actions
- Skip cleanup between tests
- Ignore flaky test patterns

## Troubleshooting

| Issue             | Cause          | Solution           |
| ----------------- | -------------- | ------------------ |
| Element not found | Timing issue   | Use proper waits   |
| Flaky tests       | Race condition | Use intercept/wait |
| Timeout error     | Slow response  | Increase timeout   |

## References

- [Cypress Documentation](https://docs.cypress.io/)
- [Cypress Best Practices](https://docs.cypress.io/guides/references/best-practices)
