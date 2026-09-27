---
name: testing-library
description: Expert Testing Library assistance covering user-centric queries, async assertions, and accessibility locators. Use when testing React, Vue, or Angular components with `@testing-library`.
---

# Testing Library (React/DOM)

The guiding principle: **"The more your tests resemble the way your software is used, the more confidence they can give you."**
It encourages testing _behavior_ (what the user sees) rather than implementation details (state, props).

## When to Use

- **User-Centric Component Testing**: Testing React, Vue, Angular, or Svelte components the way actual end users interact with them.
- **Accessible Query Prioritization**: Selecting elements by accessibility roles (`getByRole`), labels, and text rather than implementation details.
- **Async DOM State Synchronization**: Waiting for elements to appear or disappear using `findBy*` queries.
- **Refactoring-Resilient Test Suites**: Ensuring tests don't break when internal component implementation details change.

## Quick Start

```javascript
import { render, screen, fireEvent } from "@testing-library/react";
import App from "./App";

test("renders learn react link", () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});

test("button click", () => {
  render(<Button />);
  const btn = screen.getByRole("button", { name: /submit/i });
  fireEvent.click(btn);
  expect(btn).toBeDisabled();
});
```

## Core Concepts

#Guiding Principle: "The More Your Tests Resemble..."

"The more your tests resemble the way your software is used, the more confidence they can give you." Tests avoid inspecting internal component state:

```
[ User Interaction ] ──Finds by Role / Text──→ [ Clicks / Enters Text ] ──→ [ Asserts on DOM Text Output ]
```

#The Query Priority Hierarchy

Selects elements following user-accessible priority:

1. `getByRole(role, { name })` - Most preferred (matches assistive technology accessibility tree)
2. `getByLabelText(text)` - Form inputs
3. `getByPlaceholderText(text)` - Secondary inputs
4. `getByText(text)` - Non-interactive text content
5. `getByTestId(id)` - Fallback for dynamic/arbitrary elements only

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LoginForm } from "./LoginForm";

test("submits login credentials correctly", async () => {
  const user = userEvent.setup();
  const onSubmit = jest.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  // Queries mirror user perceptions
  await user.type(
    screen.getByRole("textbox", { name: /email/i }),
    "user@example.com",
  );
  await user.type(screen.getByLabelText(/password/i), "Password123!");
  await user.click(screen.getByRole("button", { name: /sign in/i }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: "user@example.com",
    password: "Password123!",
  });
});
```

#Async Queries (`findBy*`) & Element Disappearance (`waitForElementToBeRemoved`)

```tsx
// Waits automatically for async element to render in DOM
const successMessage = await screen.findByRole("alert");
expect(successMessage).toHaveTextContent("Order Confirmed!");

// Asserts loading spinner disappears
await waitForElementToBeRemoved(() => screen.queryByRole("progressbar"));
```

## Common Patterns

### User-Event Interactions with Accessible Queries

**Problem**: Using `fireEvent` misses realistic focus, keyboard, and click event bubbling sequences.

**Solution**:
Use `@testing-library/user-event` with accessible queries:

```typescript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Counter } from "./Counter";

test("increments count on button click", async () => {
  const user = userEvent.setup();
  render(<Counter initialCount={0} />);

  const button = screen.getByRole("button", { name: /increment/i });
  await user.click(button);

  expect(screen.getByRole("status")).toHaveTextContent("Count: 1");
});
```

## Best Practices (2026)

**Do**:

- **Use `@testing-library/user-event` Over `fireEvent`**: `userEvent` dispatches realistic browser events (focus, hover, keydown, click).
- **Use `getByRole` with the `name` Option**: Ensure your accessibility tree is sound by querying elements by role and accessible name.
- **Use `screen` for Querying**: Query via `screen.getByRole` rather than destructuring from `render()`.
- **Install `jest-dom` / `vitest-dom` Matchers**: Write fluent assertions like `expect(btn).toBeDisabled()`.

**Don't**:

- **Don't query by class name or tag name**: `container.querySelector('.btn')` couples tests to volatile CSS details.
- **Don't use `waitFor` with empty callbacks**: Never write `await waitFor(() => {})`; assert on specific element conditions inside the callback.
- **Don't use `getByTestId` as the primary selector**: Rely on accessibility roles; use test IDs only when semantic roles cannot apply.

## Troubleshooting

| Error                                                                       | Cause                                                          | Solution                                                                           |
| :-------------------------------------------------------------------------- | :------------------------------------------------------------- | :--------------------------------------------------------------------------------- |
| `Unable to find an accessible element with role`                            | Element is missing ARIA role or label, or hasn't rendered yet. | Use `screen.findByRole` for async items, or inspect output with `screen.debug()`.  |
| `Warning: An update to Component inside a test was not wrapped in act(...)` | State update occurred after test assertion finished.           | Ensure all async actions and user events are awaited with `await user.click(...)`. |
| `Found multiple elements with role`                                         | Query matched multiple items on screen.                        | Scope query using `within(container)` or specify `{ name: 'Specific Label' }`.     |

## References

- [Testing Library Docs](https://testing-library.com/)
