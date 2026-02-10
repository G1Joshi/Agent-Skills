---
name: wordpress
description: WordPress CMS development with themes, plugins, and Gutenberg. Use for content sites.
---

# WordPress

WordPress 6.6 (2025) continues the **Full Site Editing (FSE)** revolution. Everything is a block.

## When to Use

- **Content Sites**: Blogs, News, Marketing sites.
- **Client Handoff**: Clients know the WP Admin interface.
- **E-commerce**: WooCommerce is standard.

## Core Concepts

### Gutenberg (Block Editor)

React-based editor. `blocks` are the unit of content.

### Themes (Block Themes)

composed of `html` parts and `theme.json`, reducing PHP usage.

### Plugins

The ecosystem hook system (actions/filters).

## Best Practices (2025)

**Do**:

- **Use `theme.json`**: For defining global styles.
- **Use Bedrock**: For 12-factor (Git-controlled) WordPress.
- **Use Headless**: WP as an API (GraphQL) + Next.js frontend if needed.

**Don't**:

- **Don't edit core**: Never touch `wp-includes`.

## References

- [WordPress Developer](https://developer.wordpress.org/)
