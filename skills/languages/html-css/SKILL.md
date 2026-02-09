---
name: html-css
description: HTML5 and CSS3 for web structure, styling, flexbox, grid, and responsive layouts. Use for .html and .css files.
---

# HTML & CSS

Modern HTML5 and CSS3 for semantic web structure and responsive styling.

## When to Use

- Working with `.html` and `.css` files
- Building responsive web layouts
- Creating accessible web interfaces
- Styling web components

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

### Semantic HTML

```html
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <header>
      <h1>Article Title</h1>
      <time datetime="2024-01-15">January 15, 2024</time>
    </header>
    <p>Content...</p>
  </article>
</main>

<footer>
  <p>&copy; 2024 Company</p>
</footer>
```

### CSS Custom Properties

```css
:root {
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  --spacing-md: 1rem;
  --radius-md: 0.5rem;
  --font-sans: system-ui, sans-serif;
}

.button {
  background: var(--color-primary);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
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

## Best Practices

**Do**:

- Use semantic HTML elements
- Mobile-first responsive design
- Use CSS custom properties for theming
- Include proper accessibility attributes

**Don't**:

- Use `<div>` for everything (use semantic tags)
- Use inline styles for complex styling
- Forget viewport meta tag
- Ignore color contrast requirements

## Troubleshooting

| Issue                   | Cause               | Solution                  |
| ----------------------- | ------------------- | ------------------------- |
| Layout overflow         | Fixed widths        | Use percentage or min/max |
| Flex items not wrapping | Missing `flex-wrap` | Add `flex-wrap: wrap`     |
| Grid gaps not showing   | Old browser         | Check browser support     |

## References

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web)
- [CSS-Tricks](https://css-tricks.com/)
