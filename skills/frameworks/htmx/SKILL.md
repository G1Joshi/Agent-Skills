---
name: htmx
description: Expert htmx assistance covering hypermedia-driven UIs, AJAX swaps, out-of-band updates, and SSE/WebSockets. Use when building dynamic web interfaces without writing complex client JavaScript.
---

# htmx

High power tools for HTML. Allows you to build modern user interfaces with the simplicity of hypertext.

## When to Use

- **Hypermedia-Driven Web Architectures**: Building dynamic user interfaces using server-rendered HTML over the wire without heavy SPA frameworks.
- **CRUD Backends with Existing Templating**: Django, Rails, Laravel, Go templates, or Spring Boot apps wanting SPA-like responsiveness.
- **Instant Search, Inline Editing, and Polling**: Enhancing HTML forms and tables with declarative AJAX attributes.
- **Low-JavaScript Minimal Bundles**: Drastically reducing client bundle sizes and eliminating frontend state management complexity.

## Quick Start

```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>

<!-- When clicked, issue GET to /clicked, swap outerHTML with response -->
<button hx-get="/clicked" hx-swap="outerHTML">Click Me</button>
```

## Core Concepts

#Declarative AJAX with Trigger & Swap Directives

Making async requests and swapping server HTML directly into DOM targets:

```html
<!-- Instant search input with debouncing -->
<div class="search-widget">
  <input
    type="text"
    name="q"
    placeholder="Search users..."
    hx-post="/api/users/search"
    hx-trigger="keyup changed delay:300ms, search"
    hx-target="#search-results"
    hx-indicator="#loading-spinner"
    class="form-control"
  />
  <div id="loading-spinner" class="htmx-indicator">Searching...</div>
  <div id="search-results">
    <!-- Server returns <ul> list HTML here -->
  </div>
</div>
```

#Inline Editing with Target Swapping

Updating tabular records in-place without page reloads:

```html
<!-- Table Row Component -->
<tr id="user-row-42">
  <td>Alice Johnson</td>
  <td>alice@example.com</td>
  <td>
    <button
      class="btn btn-sm btn-primary"
      hx-get="/users/42/edit"
      hx-target="#user-row-42"
      hx-swap="outerHTML"
    >
      Edit
    </button>
  </td>
</tr>
```

#Out-of-Band (OOB) Updates & Server-Sent Events

Updating multiple disconnected DOM regions from a single response:

```html
<!-- Server response contains main payload and an OOB notification badge -->
<div id="order-details">
  <h4>Order #1029 Confirmed</h4>
  <p>Status: Processing</p>
</div>

<!-- Out-of-band swap updates the navbar cart badge automatically -->
<span id="cart-counter" hx-swap-oob="true" class="badge bg-danger"> 3 </span>
```

## Common Patterns

### Inline Search with Debounced Active Search

**Problem**: Building responsive autocomplete search typically requires heavy React/Vue state machines.

**Solution**:
Use declarative htmx attributes on standard HTML input:

```html
<input
  type="search"
  name="q"
  placeholder="Search users..."
  hx-post="/api/users/search"
  hx-trigger="keyup changed delay:300ms, search"
  hx-target="#search-results"
  hx-indicator="#loading-spinner"
/>

<div id="loading-spinner" class="htmx-indicator">Searching...</div>
<div id="search-results"></div>
```

## Best Practices (2026)

- **Do** return clean HTML partials/fragments from the server instead of entire HTML document trees for htmx endpoints.
- **Do** use `hx-indicator` to provide visual loading indicators and spinners for every network interaction.
- **Do** leverage `hx-boost="true"` on root layout links and forms for instant progressive enhancement.
- **Do** validate and sanitize all server-rendered HTML to neutralize Cross-Site Scripting (XSS).
- **Don't** return JSON from htmx endpoints; htmx is fundamentally designed for server-rendered HTML.
- **Don't** neglect accessibility; announce dynamic swaps to screen readers using `aria-live="polite"`.
- **Don't** overuse client-side scripting when declarative htmx attributes can achieve the desired interaction.

## Troubleshooting

| Error                                             | Cause                                                             | Solution                                                                         |
| :------------------------------------------------ | :---------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| `htmx:targetError: Target element does not exist` | Element specified in `hx-target` ID selector is missing from DOM. | Verify ID in DOM: `#search-results` must exist before request triggers.          |
| `Response received but nothing swapped`           | Server returned empty response or non-200 HTTP code.              | Verify server returns HTML with HTTP 200, or configure `hx-swap` response codes. |
| `Infinite request loop`                           | `hx-trigger="load"` placed inside swapped HTML fragment.          | Move load trigger to outer persistent container or remove trigger on swap.       |

## References

- [htmx.org](https://htmx.org/)
- [Hypermedia Systems Book](https://hypermedia.systems/)
