---
name: tailwindcss
description: Expert Tailwind CSS assistance covering utility classes, responsive variants, arbitrary values, and configuration. Use when styling modern web applications with speed and consistency.
---

# Tailwind CSS

Tailwind v4 (2024/2025) introduces the **Oxide Engine**: a Rust-based, unified toolchain that is 10x faster and requires no configuration (`tailwind.config.js` is optional).

## When to Use

- **Modern Utility-First Web Design**: Rapidly styling HTML without leaving JSX/HTML templates.
- **Tailwind CSS v4 CSS-First Projects**: Streamlined setup using `@theme` and native CSS engine without JavaScript config files.
- **Responsive & Dark-Mode Interfaces**: Instant responsive breakpoint variants (`md:`, `lg:`) and dark mode (`dark:`).
- **Design System Consistency**: Enforcing standardized spacing scales, typography, and color tokens.

## Quick Start

```html
<div
  class="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl m-8"
>
  <div class="md:flex">
    <div class="p-8">
      <div
        class="uppercase tracking-wide text-sm text-indigo-500 font-semibold"
      >
        Tailwind CSS
      </div>
      <p class="mt-2 text-slate-500">
        Utility-first CSS framework packed with classes.
      </p>
      <button
        class="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
      >
        Action
      </button>
    </div>
  </div>
</div>
```

## Core Concepts

#Tailwind CSS v4 CSS-First Configuration

Configuring design tokens directly in native CSS with `@theme`:

```css
/* main.css */
@import "tailwindcss";

@theme {
  --color-brand-primary: #4f46e5;
  --color-brand-accent: #06b6d4;
  --font-display: "Outfit", sans-serif;
  --radius-custom: 1rem;
}
```

#Responsive, Accessible Card Layout

Combining flexbox, grid, hover states, and dark mode variants:

```html
<div
  class="max-w-md mx-auto p-6 bg-white dark:bg-slate-900 rounded-2xl shadow-lg border border-slate-100 dark:border-slate-800 transition hover:shadow-xl"
>
  <div class="flex items-center space-x-4">
    <div
      class="flex-shrink-0 w-12 h-12 bg-indigo-100 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 rounded-xl flex items-center justify-center font-bold text-lg"
    >
      TS
    </div>
    <div>
      <h3 class="text-lg font-semibold text-slate-900 dark:text-white">
        Enterprise Scalability
      </h3>
      <p class="text-sm text-slate-500 dark:text-slate-400">
        Tailwind CSS v4 Engine
      </p>
    </div>
  </div>
  <p class="mt-4 text-sm leading-relaxed text-slate-600 dark:text-slate-300">
    Ultra-fast build performance with zero config file ceremony.
  </p>
  <button
    class="mt-6 w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white font-medium text-sm rounded-lg transition focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
  >
    View Architecture
  </button>
</div>
```

#Container Queries & Modern Micro-Animations

Adapting component appearance to container dimensions:

```html
<!-- Container query parent and child -->
<div class="@container">
  <div class="flex flex-col @sm:flex-row items-center gap-4 p-4">
    <span class="w-full @sm:w-auto text-center font-medium"
      >Responsive inside container</span
    >
  </div>
</div>
```

## Common Patterns

### Dynamic Class Composition with cn Utility (clsx + tailwind-merge)

**Problem**: Conditional string concatenation produces conflicting Tailwind classes (e.g. `p-4` and `p-8`).

**Solution**:
Use the `cn()` helper:

```typescript
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// In component:
// cn("px-4 py-2 bg-blue-500", isPrimary && "bg-indigo-600", className);
```

## Best Practices (2026)

- **Do** target Tailwind CSS v4 with native CSS `@theme` variables for lightning-fast compilation.
- **Do** use `clsx` and `tailwind-merge` (`cn()`) when dynamically constructing conditional class strings.
- **Do** design mobile-first: use unprefixed utilities for mobile, and override with `md:`, `lg:` prefixes.
- **Do** leverage container queries (`@container`) for modular UI components embedded in arbitrary layouts.
- **Don't** write arbitrary values (`w-[347px]`) when standardized design scale values exist.
- **Don't** overuse `@apply` in CSS files; it re-introduces CSS naming overhead and defeats utility advantages.
- **Don't** concatenate partial dynamic classes (e.g. `text-${color}-500`); always use complete string literals.

## Troubleshooting

| Error                                                      | Cause                                                               | Solution                                                                  |
| :--------------------------------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------------------------------ |
| `Tailwind classes not rendering in browser`                | Class not included in `content` purge glob in `tailwind.config.js`. | Verify file paths in `tailwind.config.js` `content` array.                |
| `Dynamic class strings like text-${color}-500 not working` | Tailwind scanner cannot evaluate dynamic string interpolation.      | Use complete class names in lookup maps: `{ red: 'text-red-500' }`.       |
| `Custom CSS directive @tailwind unknown at-rule`           | Editor CSS linter not configured for PostCSS/Tailwind.              | Install Tailwind CSS IntelliSense extension or set CSS validate to false. |

## References

- [Tailwind CSS Documentation](https://tailwindcss.com/)
