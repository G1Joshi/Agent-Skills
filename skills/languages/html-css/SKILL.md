---
name: html-css
description: Expert modern HTML5 and CSS3 assistance covering semantic markup, Flexbox, CSS Grid, container queries, CSS custom properties, and responsive design systems. Use when crafting accessible web interfaces, building resilient UI layouts, or optimizing render performance.
---

# HTML & CSS

Modern HTML5 and CSS3 for semantic web structure and responsive styling.

## When to Use

- **Semantic Web Structure & Accessibility**: Crafting accessible, WCAG-compliant, SEO-optimized web documents with HTML5 elements.
- **Modern Responsive Layouts (CSS Grid & Flexbox)**: Designing fluid, adaptable screen layouts across mobile, tablet, desktop, and TV viewports.
- **Component-Driven Theming (CSS Custom Properties)**: Implementing zero-runtime dark/light mode themes and design tokens.
- **Modern CSS Features (Container Queries & `:has()`)**: Styling components based on their immediate container width and parent-child states.

## Quick Start

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Page Title</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <main class="container">
      <h1>Hello World</h1>
    </main>
  </body>
</html>
```

## Core Concepts

#Semantic HTML5 & Accessible Landmark Roles

Replaces generic `<div>` soup with structural elements that assistive technologies understand:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Enterprise Portal</title>
  </head>
  <body>
    <header role="banner">
      <nav aria-label="Main Navigation">
        <ul>
          <li><a href="/dashboard">Dashboard</a></li>
        </ul>
      </nav>
    </header>
    <main id="main-content">
      <article>
        <h1>System Architecture 2026</h1>
        <p>Modern web applications prioritize semantic accessibility.</p>
      </article>
    </main>
    <footer role="contentinfo">
      <p>&copy; 2026 Enterprise Corp.</p>
    </footer>
  </body>
</html>
```

#Modern CSS Layout (Grid & Subgrid)

Builds responsive multi-column layouts without external CSS frameworks:

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3;
  padding: 1.5rem;
  background-color: var(--color-surface);
  border-radius: 0.75rem;
}
```

#Container Queries & CSS Custom Properties

Adapts styling based on container container width rather than the global browser viewport:

```css
:root {
  --color-primary: #4f46e5;
  --color-surface: #ffffff;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-surface: #0f172a;
  }
}

.card-container {
  container-type: inline-size;
}

@container (min-width: 450px) {
  .card-content {
    display: flex;
    gap: 1rem;
  }
}
```

## Common Patterns

### Flexbox Layout

```css
/* Center content */
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Navigation bar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

/* Card grid with wrap */
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.card {
  flex: 1 1 300px;
}
```

### CSS Grid

```css
/* Responsive grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

/* Page layout */
.layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.header {
  grid-area: header;
}
.sidebar {
  grid-area: sidebar;
}
.main {
  grid-area: main;
}
.footer {
  grid-area: footer;
}
```

### Responsive Design

```css
/* Mobile-first approach */
.container {
  padding: 1rem;
}

@media (min-width: 768px) {
  .container {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* Container queries */
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: flex;
    gap: 1rem;
  }
}
```

## Best Practices (2026)

**Do**:

- **Always Include Viewport Meta Tag**: Ensure `<meta name="viewport" content="width=device-width, initial-scale=1.0">` is present.
- **Use Native CSS Nesting and `:has()`**: Eliminate Sass build steps by leveraging native browser CSS nesting and relational selectors.
- **Design with Accessibility in Mind**: Ensure color contrast ratios meet WCAG AA standards (4.5:1) and all images have descriptive `alt` tags.
- **Implement Fluid Typography with `clamp()`**: Use `font-size: clamp(1rem, 2.5vw, 2rem);` for seamless responsive scaling.

**Don't**:

- **Don't use `!important` to resolve specificity issues**: Structure cascade layers with `@layer` instead of overriding specificity brute-force.
- **Don't disable focus outlines without alternatives**: Never write `outline: none;` without providing an accessible `:focus-visible` ring.
- **Don't use non-semantic elements for interactive buttons**: Never use `<div onclick="...">`; always use `<button>` to ensure keyboard accessibility.

## Troubleshooting

| Issue                   | Cause               | Solution                  |
| ----------------------- | ------------------- | ------------------------- |
| Layout overflow         | Fixed widths        | Use percentage or min/max |
| Flex items not wrapping | Missing `flex-wrap` | Add `flex-wrap: wrap`     |
| Grid gaps not showing   | Old browser         | Check browser support     |

## References

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web)
- [CSS-Tricks](https://css-tricks.com/)
