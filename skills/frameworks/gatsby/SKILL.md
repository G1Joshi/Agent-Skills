---
name: gatsby
description: Expert Gatsby assistance covering static site generation, GraphQL data layer, Head API, and Gatsby Cloud. Use when building performant marketing sites and content blogs with React.
---

# Gatsby

Gatsby v5 focuses on **Valhalla Content Hub** and improved build speeds (Slice API). While Next.js has overtaken it, Gatsby remains strong for complex CMS-driven sites.

## When to Use

- **Static Marketing Websites & Blogs**: Pre-rendering React pages with maximum SEO and instantaneous page loads.
- **Headless CMS Frontends**: Sourcing content from Contentful, Sanity, Strapi, or WordPress via unified GraphQL.
- **High-Performance Image Optimization**: Delivering responsive WebP/AVIF images with blur-up placeholders.
- **Documentation Sites**: Generating static documentation with MDX and Algolia search integrations.

## Quick Start

```jsx
// src/pages/index.js
import * as React from "react";
import { Link } from "gatsby";

export default function IndexPage() {
  return (
    <main>
      <h1>Welcome to Gatsby</h1>
      <Link to="/about">About Us</Link>
    </main>
  );
}

export function Head() {
  return <title>Home Page</title>;
}
```

## Core Concepts

#GraphQL Data Layer & Static Query

Querying build-time metadata and CMS content:

```tsx
import React from "react";
import { graphql, useStaticQuery, PageProps, Link } from "gatsby";

interface SiteMetaQuery {
  site: {
    siteMetadata: {
      title: string;
      description: string;
    };
  };
}

export default function IndexPage({ data }: PageProps) {
  const meta = useStaticQuery<SiteMetaQuery>(graphql`
    query SiteTitleQuery {
      site {
        siteMetadata {
          title
          description
        }
      }
    }
  `);

  return (
    <main>
      <h1>{meta.site.siteMetadata.title}</h1>
      <p>{meta.site.siteMetadata.description}</p>
      <Link to="/about">About Us</Link>
    </main>
  );
}
```

#Dynamic Page Creation with gatsby-node.ts

Programmatically generating pages from GraphQL queries at build time:

```typescript
import path from "path";
import { GatsbyNode } from "gatsby";

export const createPages: GatsbyNode["createPages"] = async ({
  graphql,
  actions,
}) => {
  const { createPage } = actions;
  const postTemplate = path.resolve("./src/templates/post.tsx");

  const result: any = await graphql(`
    query AllArticles {
      allMarkdownRemark {
        nodes {
          frontmatter {
            slug
          }
        }
      }
    }
  `);

  result.data.allMarkdownRemark.nodes.forEach((node: any) => {
    createPage({
      path: `/blog/${node.frontmatter.slug}`,
      component: postTemplate,
      context: {
        slug: node.frontmatter.slug,
      },
    });
  });
};
```

#High-Performance Images with Gatsby Image Plugin

Automated responsive image optimization:

```tsx
import React from "react";
import { StaticImage } from "gatsby-plugin-image";

export function HeroImage() {
  return (
    <StaticImage
      src="../images/hero-banner.png"
      alt="Modern Developer Platform"
      placeholder="blurred"
      layout="constrained"
      width={1200}
      height={600}
      quality={90}
    />
  );
}
```

## Common Patterns

### Static Page Query with GraphQL

**Problem**: Injecting build-time metadata or markdown content into React page components.

**Solution**:
Use Gatsby page queries:

```jsx
import * as React from "react";
import { graphql } from "gatsby";

export default function BlogList({ data }) {
  return (
    <div>
      <h2>Latest Posts ({data.site.siteMetadata.title})</h2>
      {data.allMarkdownRemark.nodes.map((node) => (
        <article key={node.id}>
          <h3>{node.frontmatter.title}</h3>
        </article>
      ))}
    </div>
  );
}

export const query = graphql`
  query {
    site {
      siteMetadata {
        title
      }
    }
    allMarkdownRemark(limit: 5) {
      nodes {
        id
        frontmatter {
          title
        }
      }
    }
  }
`;
```

## Best Practices (2026)

- **Do** use TypeScript (`gatsby-config.ts`, `gatsby-node.ts`) for compile-time configuration validation.
- **Do** use `StaticImage` and `GatsbyImage` to eliminate layout shifts (CLS) and automate responsive sizes.
- **Do** leverage Deferred Static Generation (DSG) for infrequently accessed archive pages to speed up builds.
- **Do** configure `gatsby-plugin-manifest` and `gatsby-plugin-offline` for PWA capabilities.
- **Don't** use standard `<img>` tags for local assets; always use the Gatsby image pipeline.
- **Don't** execute client-side API requests for data that can be queried at build time via GraphQL.
- **Don't** query full body content inside list queries; query only excerpt and frontmatter fields.

## Troubleshooting

| Error                                                 | Cause                                                    | Solution                                                                 |
| :---------------------------------------------------- | :------------------------------------------------------- | :----------------------------------------------------------------------- |
| `WebpackError: ReferenceError: window is not defined` | Accessing `window` or `document` during build-time SSR.  | Guard window access: `if (typeof window !== "undefined")`.               |
| `GraphQL query failed: Field ... does not exist`      | Field missing in data source or schema not yet inferred. | Verify schema in GraphiQL explorer (`http://localhost:8000/___graphql`). |
| `Gatsby clean required`                               | Cache corruption in `.cache/` or `public/` directory.    | Run `gatsby clean` and rebuild.                                          |

## References

- [Gatsby Documentation](https://www.gatsbyjs.com/)
