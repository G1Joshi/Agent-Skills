---
name: tailwindcss
description: Tailwind CSS utility-first framework. Use for custom designs.
---

# Tailwind CSS

Tailwind v4 (2024/2025) introduces the **Oxide Engine**: a Rust-based, unified toolchain that is 10x faster and requires no configuration (`tailwind.config.js` is optional).

## When to Use

- **Custom Design**: When you don't want the "Bootstrap look".
- **Performance**: Generates tiny CSS files (only used classes).
- **Design Systems**: Configuring tokens (colors, spacing) enforces consistency.

## Core Concepts

### Utility Classes

`flex`, `text-red-500`, `p-4`.

### Arbitrary Values

`w-[500px]`, `bg-[#1da1f2]`.

### Modifiers

`hover:bg-blue-700`, `md:w-1/2`, `dark:text-white`.

## Best Practices (2025)

**Do**:

- **Use v4 Oxide**: No more separate PostCSS watcher needed.
- **Use `@apply` sparingly**: Keep utilities in HTML for grep-ability.
- **Use `prettier-plugin-tailwindcss`**: Automatically sorts classes.

**Don't**:

- **Don't string concat**: `class="text-" + color` breaks the purge engine. Use `clsx`.

## References

- [Tailwind CSS Documentation](https://tailwindcss.com/)
