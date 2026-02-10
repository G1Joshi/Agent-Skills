---
name: htmx
description: HTMX HTML-first approach with AJAX attributes. Use for server-rendered interactivity.
---

# htmx

High power tools for HTML. Allows you to build modern user interfaces with the simplicity of hypertext.

## When to Use

- Server-side rendered applications (Django, Flask, Rails, Go, PHP)
- You want SPA-like interactivity without the complexity of React/Vue
- "Hypermedia-driven" applications

## Quick Start

```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>

<!-- When clicked, issue GET to /clicked, swap outerHTML with response -->
<button hx-get="/clicked" hx-swap="outerHTML">Click Me</button>
```

## Core Concepts

### Attributes

`hx-get`, `hx-post`, `hx-trigger`, `hx-target`, `hx-swap`.

### Swapping

Replacing parts of the DOM with HTML returned from the server.

### HATEOAS

Hypermedia As The Engine Of Application State. The server returns HTML (state), not JSON.

## Best Practices

**Do**:

- Return partial HTML snippets from the server
- Use `hx-boost` to speed up navigation
- Use `hx-indicator` for loading states

**Don't**:

- Return full HTML pages for partial updates
- Use htmx if you need complex client-side state (offline mode, etc.)

## References

- [htmx.org](https://htmx.org/)
- [Hypermedia Systems Book](https://hypermedia.systems/)
