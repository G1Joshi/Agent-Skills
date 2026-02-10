---
name: shadcnui
description: shadcn/ui copy-paste React components. Use for modern React UI.
---

# shadcn/ui

shadcn/ui is not a component library; it's a **collection of reusable components** that you copy and paste into your apps. Built on Radix UI and Tailwind.

## When to Use

- **Ownership**: You want full control over the component code.
- **Next.js**: The de facto standard for modern Next.js apps.
- **Modern**: The "Vercel Aesthetic".

## Core Concepts

### Copy/Paste

`npx shadcn-ui@latest add button`. This adds `components/ui/button.tsx` to YOUR project.

### Radix UI

The headless, accessible primitives (Dialog, Tooltip) that power the interactions.

### `cn` Utility

A helper to merge Tailwind classes conditionally (`clsx` + `tailwind-merge`).

## Best Practices (2025)

**Do**:

- **Customize**: Edit the component code! That's the point.
- **Use `lucide-react`**: The standard icon set.
- **Use Blocks**: Copy larger blocks (Login Forms, Dashboards) from the registry.

**Don't**:

- **Don't treat it like MUI**: There is no npm package to update. You own the code.

## References

- [shadcn/ui Documentation](https://ui.shadcn.com/)
