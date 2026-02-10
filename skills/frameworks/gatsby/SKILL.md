---
name: gatsby
description: Gatsby React static site generator with GraphQL. Use for static sites.
---

# Gatsby

Gatsby v5 focuses on **Valhalla Content Hub** and improved build speeds (Slice API). While Next.js has overtaken it, Gatsby remains strong for complex CMS-driven sites.

## When to Use

- **Data Integration**: You have content in Contentful, Shopify, and WordPress and need to merge it.
- **Static Sites**: Extremely optimized static output (Image optimization).
- **Plugin Ecosystem**: Thousands of "drops-in" plugins.

## Core Concepts

### GraphQL Data Layer

Gatsby pulls all data into a local GraphQL schema.

### Source Plugins

`gatsby-source-filesystem`, `gatsby-source-contentful`.

### React Hydration

Generated HTML rehydrates into a SPA.

## Best Practices (2025)

**Do**:

- **Use Slice API**: Updating a navbar shouldn't rebuild 10,000 pages.
- **Use Gatsby Image**: Unmatched image optimization features.
- **Use Adapters**: For zero-config deployment to Netlify/Vercel.

**Don't**:

- **Don't use for Dynamic Apps**: Use Next.js or Remix for dashboard-style apps.

## References

- [Gatsby Documentation](https://www.gatsbyjs.com/)
