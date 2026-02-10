---
name: jquery
description: jQuery DOM manipulation and AJAX for legacy projects. Use for older web projects.
---

# jQuery

jQuery v4.0 (2025) is a cleanup release, removing IE support and shrinking the file size. While not for new apps, it remains vital for legacy maintenance and WordPress.

## When to Use

- **Legacy Maintenance**: Supporting 2010-era websites.
- **WordPress**: Heavily relied upon by WP plugins.
- **Quick Scripts**: Sometimes `$('.class').hide()` is all you need.

## Core Concepts

### The `$` function

DOM selection shorthand.

### Chaining

`$('#id').css('color', 'red').slideUp(2000)`.

### AJAX

`$.ajax({...})`. (Use `fetch` in modern JS).

## Best Practices (2025)

**Do**:

- **Upgrade to v4**: Drop support for IE11.
- **Use Vanilla JS**: For new features (`document.querySelector`).

**Don't**:

- **Don't verify new projects**: Use React/Vue/Svelte/Vanilla.

## References

- [jQuery Documentation](https://jquery.com/)
