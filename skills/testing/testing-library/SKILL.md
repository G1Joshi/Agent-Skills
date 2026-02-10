---
name: testing-library
description: Testing Library user-centric testing. Use for React testing.
---

# Testing Library (React/DOM)

The guiding principle: **"The more your tests resemble the way your software is used, the more confidence they can give you."**
It encourages testing _behavior_ (what the user sees) rather than implementation details (state, props).

## When to Use

- **React Components**: The industry standard (`@testing-library/react`).
- **Accessibility Testing**: It inherently encourages accessible code (`getByRole`).

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

### Queries (Priority)

1. `getByRole`: Best. Tests accessibility structure (button, heading).
2. `getByLabelText`: Good for forms.
3. `getByText`: Good for verifying content.
4. `getByTestId`: **Last Resort**. Only use if nothing else targets the element stable.

### User Event

`fireEvent` is low level. Use `@testing-library/user-event` to simulate real interactions (typing, hovering).

```javascript
import userEvent from "@testing-library/user-event";
await userEvent.click(screen.getByRole("button"));
```

## Best Practices (2025)

**Do**:

- **Use `screen`**: Always import `screen` for global queries.
- **Use `await findBy...`**: For async elements (fetching data). `getBy` fails immediately if not found.
- **Test User Flows**: Don't test valid state; test "User clicks button -> Text appears".

**Don't**:

- **Don't use `container.querySelector`**: Defeats the purpose.
- **Don't test implementation**: Don't check the component's state or class methods directly.

## References

- [Testing Library Docs](https://testing-library.com/)
