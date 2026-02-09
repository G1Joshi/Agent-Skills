---
name: testing-library
description: Testing Library for user-centric component testing. Use for React/Vue/Angular tests.
---

# Testing Library

User-centric testing utilities for UI components.

## When to Use

- React/Vue/Angular component testing
- Accessibility-focused testing
- User interaction testing
- Integration testing

## Quick Start

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Button } from "./Button";

test("handles click events", async () => {
  const handleClick = jest.fn();
  render(<Button onClick={handleClick}>Click me</Button>);

  await userEvent.click(screen.getByRole("button", { name: "Click me" }));

  expect(handleClick).toHaveBeenCalled();
});
```

## Core Concepts

### Queries

```tsx
// Priority: Most accessible first
screen.getByRole('button', { name: 'Submit' });
screen.getByLabelText('Email');
screen.getByPlaceholderText('Enter name');
screen.getByText('Welcome');
screen.getByDisplayValue('current value');
screen.getByAltText('profile picture');
screen.getByTitle('tooltip');
screen.getByTestId('custom-element');

// Query variants
getBy...    // Throws if not found
queryBy...  // Returns null if not found
findBy...   // Async, waits for element
getAllBy... // Returns array
```

### User Events

```tsx
import userEvent from "@testing-library/user-event";

test("form interactions", async () => {
  const user = userEvent.setup();
  render(<Form />);

  await user.type(screen.getByLabelText("Name"), "John");
  await user.clear(screen.getByLabelText("Email"));
  await user.click(screen.getByRole("button", { name: "Submit" }));
  await user.selectOptions(screen.getByRole("combobox"), "option1");
  await user.keyboard("{Enter}");
});
```

## Common Patterns

### Async Rendering

```tsx
test("loads data", async () => {
  render(<UserProfile userId="123" />);

  // Wait for loading to finish
  expect(screen.getByText("Loading...")).toBeInTheDocument();

  // Wait for data
  await screen.findByText("John Doe");

  expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
});
```

### Custom Render

```tsx
// test-utils.tsx
import { render, RenderOptions } from "@testing-library/react";
import { ThemeProvider } from "./ThemeProvider";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

function AllProviders({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>{children}</ThemeProvider>
    </QueryClientProvider>
  );
}

const customRender = (ui: React.ReactElement, options?: RenderOptions) =>
  render(ui, { wrapper: AllProviders, ...options });

export * from "@testing-library/react";
export { customRender as render };
```

## Best Practices

**Do**:

- Use role-based queries
- Test user behavior
- Use userEvent over fireEvent
- Create custom render with providers

**Don't**:

- Test implementation details
- Use getByTestId as first choice
- Rely on CSS selectors
- Skip accessibility queries

## Troubleshooting

| Issue             | Cause           | Solution         |
| ----------------- | --------------- | ---------------- |
| Element not found | Query issue     | Check query type |
| Act warning       | Missing async   | Add await        |
| State not updated | Missing waitFor | Use findBy       |

## References

- [Testing Library Docs](https://testing-library.com/docs/)
- [Guiding Principles](https://testing-library.com/docs/guiding-principles)
