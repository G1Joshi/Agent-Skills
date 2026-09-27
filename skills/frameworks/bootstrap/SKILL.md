---
name: bootstrap
description: Expert Bootstrap 5 assistance covering 12-column grid system, flexbox utilities, components, and responsive breakpoints. Use when rapidly prototyping responsive, mobile-first web layouts.
---

# Bootstrap

Bootstrap 5 dropped jQuery and embraced modern CSS (Grid, Flexbox, Variables). It remains the **safest choice** for admin panels and internal tools.

## When to Use

- **Rapid Prototyping & MVPs**: Quickly laying out responsive pages with pre-built components and utilities.
- **Administrative Portals & Back-Office Dashboards**: Building clean, accessible user interfaces without a dedicated design team.
- **Responsive Grid Layouts**: Utilizing mobile-first 12-column flexbox and CSS Grid layout systems.
- **Design System Customization with Sass**: Overriding theme variables, color palettes, and breakpoints.

## Quick Start

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
    <title>Bootstrap Demo</title>
  </head>
  <body>
    <div class="container py-5">
      <div class="row g-4">
        <div class="col-md-6">
          <div class="card p-4 shadow-sm">
            <h2 class="card-title">Responsive Card</h2>
            <p class="text-muted">Built with Bootstrap 5 utilities.</p>
            <button class="btn btn-primary">Action</button>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
```

## Core Concepts

#Responsive 12-Column Grid & Flexbox Utilities

Mobile-first layout containers adapting to viewports:

```html
<div class="container-fluid px-4 py-5">
  <div class="row g-4 align-items-center">
    <div class="col-12 col-md-6 col-lg-4">
      <div class="card h-100 shadow-sm border-0">
        <div class="card-body d-flex flex-column justify-content-between">
          <h5 class="card-title text-primary">Standard Plan</h5>
          <p class="card-text text-muted">
            Complete features for growing teams.
          </p>
          <a href="#" class="btn btn-primary mt-3 w-100">Get Started</a>
        </div>
      </div>
    </div>
    <div class="col-12 col-md-6 col-lg-4">
      <div class="card h-100 shadow-lg border-primary">
        <div class="card-body d-flex flex-column justify-content-between">
          <h5 class="card-title text-success">Enterprise Plan</h5>
          <p class="card-text text-muted">
            Dedicated infrastructure and SLA guarantees.
          </p>
          <a href="#" class="btn btn-success mt-3 w-100">Contact Sales</a>
        </div>
      </div>
    </div>
  </div>
</div>
```

#Customizing Design Tokens with Sass

Overriding variables before compiling Bootstrap:

```scss
// Custom theme variable overrides
$primary: #4f46e5;
$secondary: #64748b;
$success: #10b981;
$enable-rounded: true;
$border-radius: 0.75rem;
$enable-shadows: true;

// Import Bootstrap source
@import "bootstrap/scss/bootstrap";
```

#Vanilla JavaScript Component Initialization

Programmatic control of interactive modals and toasts:

```javascript
import Modal from "bootstrap/js/dist/modal";
import Toast from "bootstrap/js/dist/toast";

// Initialize Modal programmatically
const modalEl = document.getElementById("confirmationModal");
const confirmModal = new Modal(modalEl, {
  backdrop: "static",
  keyboard: false,
});

// Initialize Toast notification
const toastEl = document.getElementById("statusToast");
const toast = new Toast(toastEl, { delay: 4000 });

document.getElementById("saveButton").addEventListener("click", () => {
  confirmModal.hide();
  toast.show();
});
```

## Common Patterns

### Responsive Flexbox Navbar with Toggler

**Problem**: Creating a clean mobile hamburger menu that expands smoothly on desktop viewports.

**Solution**:
Use the standard Bootstrap 5 navbar structure:

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Brand</a>
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navMenu"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
        <li class="nav-item"><a class="nav-link active" href="#">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Features</a></li>
      </ul>
    </div>
  </div>
</nav>
```

## Best Practices (2026)

- **Do** compile Bootstrap from source Sass to strip unused components and reduce CSS bundle size.
- **Do** import individual JavaScript component modules (`import Modal from 'bootstrap/js/dist/modal'`) instead of full bundles.
- **Do** utilize Bootstrap CSS variables (`var(--bs-primary)`) for runtime theme switching and dark mode.
- **Do** ensure proper ARIA attributes (`aria-expanded`, `aria-label`) on all interactive buttons and modals.
- **Don't** use `!important` to override Bootstrap styles; use Sass variables or CSS specificity.
- **Don't** include jQuery with Bootstrap 5+; all plugins use native vanilla DOM APIs.
- **Don't** hardcode pixel widths; use Bootstrap utility classes (`w-100`, `max-w-100`) and the responsive grid.

## Troubleshooting

| Error                                              | Cause                                                                 | Solution                                                                    |
| :------------------------------------------------- | :-------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `Dropdown / Modal / Collapse not opening on click` | Bootstrap JavaScript bundle (`bootstrap.bundle.min.js`) not imported. | Add `<script src=".../bootstrap.bundle.min.js"></script>` before `</body>`. |
| `Columns not wrapping on mobile viewports`         | Using fixed `.col-6` without responsive prefixes like `.col-md-6`.    | Use responsive breakpoint classes (`col-12 col-md-6 col-lg-4`).             |
| `Custom CSS styles overwritten by Bootstrap`       | Custom stylesheet imported before Bootstrap CSS in `<head>`.          | Import custom CSS file _after_ the Bootstrap CSS link tag.                  |

## References

- [GetBootstrap](https://getbootstrap.com/)
