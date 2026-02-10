---
name: netlify
description: Netlify web deployment with serverless functions. Use for static hosting.
---

# Netlify

Netlify pioneered the Jamstack. In 2025, it focuses on "Platform Primitives" – giving frameworks low-level control over caching, image optimization, and routing.

## When to Use

- **Static Sites**: Gatsby, Hugo, Astro. Best-in-class CDN.
- **Framework Agnostic**: Great support for Remix, Nuxt, SvelteKit, not just Next.js.
- **Netlify Create**: Visual editor integration for CMS-driven sites.

## Quick Start

```bash
npm i -g netlify-cli

# Run local dev environment (simulates Lambda/Edge)
netlify dev

# Deploy
netlify deploy --prod
```

## Core Concepts

### Deploy Previews

Every Pull Request gets a URL. It stays alive forever (immutable).

### Netlify Drawer

Collaboration tool overlay on preview builds.

### Edge Functions (Deno)

Run logic at the edge using Deno. Good for A/B testing, Geolocation, Auth middleware.

## Best Practices (2025)

**Do**:

- **Use `netlify.toml`**: configure redirects, headers, and build settings as code.
- **Use Netlify Image CDN**: Automatic format optimization (AVIF/WebP).
- **Use Blob Storage**: For large assets / user uploads.

**Don't**:

- **Don't hardcode redirects in JS**: Use `_headers` or `_redirects` files for CDN-level performance.

## References

- [Netlify Documentation](https://docs.netlify.com/)
