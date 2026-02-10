---
name: strapi
description: Strapi headless CMS with REST and GraphQL. Use for content APIs.
---

# Strapi

Strapi v5 (2025) introduces a **Document Service API**, Draft & Publish 2.0, and a content history feature. It is the leading self-hosted Headless CMS.

## When to Use

- **Custom Content**: You need a flexible schema builder.
- **Self-Hosted**: Data privacy requirements prevent SaaS CMS.
- **API First**: REST and GraphQL APIs generated automatically.

## Core Concepts

### Content Types

Builder UI to define `Articles`, `Products`.

### RBAC

Role-Based Access Control for content editors.

### Plugins

Marketplace for SEO, comments, auth providers.

## Best Practices (2025)

**Do**:

- **Use TypeScript**: v5 codebase is fully TypeScript.
- **Use Environment Variables**: For secrets configuration.
- **Use the Transfer Feature**: To move data between local/staging/production.

**Don't**:

- **Don't hack core**: Use the plugin system and middleware to extend functionality.

## References

- [Strapi Documentation](https://strapi.io/)
