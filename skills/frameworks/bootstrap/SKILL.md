---
name: bootstrap
description: Bootstrap CSS framework for responsive design. Use for quick styling.
---

# Bootstrap

Bootstrap 5 dropped jQuery and embraced modern CSS (Grid, Flexbox, Variables). It remains the **safest choice** for admin panels and internal tools.

## When to Use

- **Prototypes**: "Get it working" in 5 minutes.
- **Admin Panels**: Hundreds of templates available.
- **Quick MVP**: When custom design is a secondary concern.

## Core Concepts

### Grid System

The 12-column grid (`col-md-6`) is still the industry standard mental model.

### Utilities

`d-flex`, `mt-5`, `text-center`. (Influenced Tailwind).

### Components

Modals, Dropdowns, Navbars work out of the box (JS included).

## Best Practices (2025)

**Do**:

- **Use Data Attributes**: `data-bs-toggle="modal"` (No JS code needed).
- **Use CSS Variables**: `--bs-primary` makes theming easy.
- **Use SCSS**: Customize the build by importing only needed parts.

**Don't**:

- **Don't include jQuery**: Bootstrap 5 doesn't need it.

## References

- [GetBootstrap](https://getbootstrap.com/)
