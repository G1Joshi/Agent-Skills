---
name: storybook
description: Expert Storybook component workshop assistance covering CSF 3 stories, args, controls, and visual regression. Use when developing isolated UI components, building design systems, or documenting frontend widgets.
---

# Storybook

Storybook is a frontend workshop for building UI components and pages in isolation. It enables you to develop UI components without running your entire app (and logic/APIs).

## When to Use

- **Isolated UI Component Development**: Developing React, Vue, Svelte, or Angular components in isolation without launching backends.
- **Interactive Design System Documentation**: Publishing living styleguides and component catalogs for designer and developer handoff.
- **Visual Regression Testing**: Detecting unexpected visual pixel shifts across browser viewports with Chromatic.
- **Accessibility (a11y) Auditing**: Automated component accessibility testing via the `@storybook/addon-a11y` plugin.

## Quick Start

```bash
npx storybook@latest init
npm run storybook
```

Snippet:

```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  component: Button,
};
export default meta;

type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    primary: true,
    label: "Button",
  },
};
```

## Core Concepts

#Component Story Format (CSF 3)

Defines component variants using declarative, typed JavaScript exports:

```tsx
// src/components/Button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  title: "Components/Button",
  component: Button,
  tags: ["autodocs"],
  argTypes: {
    variant: { control: "select", options: ["primary", "secondary", "danger"] },
    onClick: { action: "clicked" },
  },
};
export default meta;

type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    variant: "primary",
    label: "Confirm Payment",
  },
};

export const Disabled: Story = {
  args: {
    variant: "primary",
    label: "Processing...",
    disabled: true,
  },
};
```

#Component Interaction Testing (`play` Function)

Simulates user interactions inside the story using Testing Library and asserts on outcomes:

```tsx
import { within, userEvent, expect } from "@storybook/test";

export const InteractiveLoginForm: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.type(canvas.getByLabelText(/email/i), "alice@example.com");
    await userEvent.type(canvas.getByLabelText(/password/i), "Secret123!");
    await userEvent.click(canvas.getByRole("button", { name: /log in/i }));

    await expect(canvas.getByText(/dashboard/i)).toBeInTheDocument();
  },
};
```

#Mocking API Calls with MSW Addon

Intercepts component network requests inside the Storybook canvas:

```tsx
import { http, HttpResponse } from "msw";

export const LoadedUserProfile: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get("/api/user", () =>
          HttpResponse.json({ name: "Alice", role: "Admin" }),
        ),
      ],
    },
  },
};
```

## Common Patterns

### Interactive Story with Controls and Play Function

**Problem**: Static component stories do not verify whether clicks and state transitions function properly.

**Solution**:
Use CSF 3 with args and `play` function testing:

```typescript
import type { Meta, StoryObj } from "@storybook/react";
import { userEvent, within, expect } from "@storybook/test";
import { LoginForm } from "./LoginForm";

const meta: Meta<typeof LoginForm> = {
  title: "Components/LoginForm",
  component: LoginForm,
};
export default meta;

type Story = StoryObj<typeof LoginForm>;

export const ValidSubmission: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.type(canvas.getByLabelText(/email/i), "user@test.com");
    await userEvent.type(canvas.getByLabelText(/password/i), "secret123");
    await userEvent.click(canvas.getByRole("button", { name: /submit/i }));
    await expect(canvas.getByText(/welcome/i)).toBeInTheDocument();
  },
};
```

## Best Practices (2026)

**Do**:

- **Adopt CSF 3 Standard**: Use object-based CSF 3 stories for cleaner syntax and reduced boilerplate.
- **Enable `@storybook/addon-a11y`**: Catch WCAG accessibility violations directly inside the component development workflow.
- **Automate Visual Testing with Chromatic**: Capture regression snapshots of all stories on every pull request.
- **Use Mock Service Worker (MSW)**: Mock API backends to enable stories to render realistic asynchronous states.

**Don't**:

- **Don't import application routers or global state in components**: Pass callbacks and state down as props to keep components isolated.
- **Don't hardcode static story args**: Leverage Storybook controls (`args`) to allow designers to test edge-case content lengths.
- **Don't neglect loading and error states**: Create dedicated stories for loading skeletons, empty data, and network error states.

## Troubleshooting

| Error                                                   | Cause                                                                  | Solution                                                            |
| :------------------------------------------------------ | :--------------------------------------------------------------------- | :------------------------------------------------------------------ |
| `Cannot find module in .storybook/preview`              | Path alias or CSS import not recognized by Storybook builder.          | Add path aliases to `.storybook/main.ts` webpackFinal or viteFinal. |
| `No stories found`                                      | Stories glob pattern in `main.ts` does not match component file paths. | Verify `stories: ['../src/**/*.stories.@(js                         | jsx | ts  | tsx)']` in config. |
| `Component won't render: hook called outside component` | Decorator missing required React context or router provider.           | Wrap story with appropriate context provider in preview decorators. |

## References

- [Storybook Documentation](https://storybook.js.org/)
