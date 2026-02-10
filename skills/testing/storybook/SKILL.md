---
name: storybook
description: Storybook UI component development and testing. Use for component testing.
---

# Storybook

Storybook is a frontend workshop for building UI components and pages in isolation. It enables you to develop UI components without running your entire app (and logic/APIs).

## When to Use

- **Component Libraries**: Building a Design System.
- **Visual Testing**: Visualizing all states of a component (Loading, Error, Empty).
- **Documentation**: Auto-generating docs for your team.

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

### Stories

A capture of a component in a specific state. A file can have multiple stories (Primary, Secondary, Disabled).

### Controls

Auto-generated UI knobs that allow you to modify props (Change color, change text) live in the browser.

### Addons

Plugins that extend functionality. Key ones:

- `Actions`: Log events (`onClick`).
- `A11y`: Check accessibility compliance.
- `Interactions`: Run small tests inside the story (`play` function).

## Best Practices (2025)

**Do**:

- **Use the `play` function**: Allows interactive testing within Storybook (powered by Testing Library).
- **Use "Autodocs"**: Enable `tags: ['autodocs']` to generate automatic documentation pages.
- **Visual Regression**: Integrate with Chromatic (by Storybook maintainers) to detect visual changes in CI.

**Don't**:

- **Don't mix business logic**: Components in Storybook should be "dumb" (Presentational). If they need data, pass it via args (mocks), don't fetch from APIs inside the component if possible.

## References

- [Storybook Documentation](https://storybook.js.org/)
