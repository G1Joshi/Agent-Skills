---
name: netlify
description: Expert Netlify assistance covering continuous deployments, Netlify Functions, edge redirects (_redirects), and form handling. Use when deploying frontend Jamstack applications and edge web services.
---

# Netlify

Netlify pioneered the Jamstack. In 2025, it focuses on "Platform Primitives" – giving frameworks low-level control over caching, image optimization, and routing.

## When to Use

- **Modern Frontend & Jamstack Deployment**: Automated git-triggered builds, preview URLs, and global edge CDN hosting.
- **Netlify Edge Functions**: Running low-latency serverless TypeScript code at the edge using Deno runtime.
- **Serverless Form Handling & Identity**: Zero-backend form submissions and user authentication.
- **Branch Previews & Collaborative Feedback**: Generating unique preview environments for every pull request with visual commenting.

## Quick Start

```bash
npm i -g netlify-cli

# Run local dev environment (simulates Lambda/Edge)
netlify dev

# Deploy
netlify deploy --prod
```

## Core Concepts

#Declarative Configuration with netlify.toml

Defining build commands, headers, and SPA redirects:

```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "22"

# Security headers across all pages
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Strict-Transport-Security = "max-age=63072000; includeSubDomains; preload"
    Referrer-Policy = "strict-origin-when-cross-origin"

# Single Page App redirect: forward all unhandled paths to index.html
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

# Proxy internal API to external microservice backend
[[redirects]]
  from = "/api/*"
  to = "https://api.backend-internal.com/:splat"
  status = 200
  force = true
```

#Netlify Edge Functions (Deno Runtime)

Running geolocation-based transforms directly at the edge:

```typescript
// netlify/edge-functions/geo-routing.ts
import type { Context } from "@netlify/edge-functions";

export default async (request: Request, context: Context) => {
  const country = context.geo?.country?.code || "US";

  // Redirect visitors from specific regions
  if (country === "FR") {
    return new Response(null, {
      status: 302,
      headers: { Location: "/fr" },
    });
  }

  // Pass request through to original destination with custom headers
  const response = await context.next();
  response.headers.set("x-visitor-country", country);
  return response;
};

export const config = {
  path: "/*",
};
```

#Automated Netlify Forms

Collecting form submissions without writing backend endpoints:

```html
<!-- Native Netlify form capture -->
<form
  name="contact-us"
  method="POST"
  data-netlify="true"
  netlify-honeypot="bot-field"
>
  <input type="hidden" name="form-name" value="contact-us" />
  <p class="hidden"><input name="bot-field" /></p>

  <label>Email: <input type="email" name="email" required /></label>
  <label>Message: <textarea name="message" required></textarea></label>
  <button type="submit">Send Message</button>
</form>
```

## Common Patterns

### Declarative netlify.toml with SPA Fallback and Security Headers

**Problem**: SPA routes returning 404 on browser refresh, combined with missing security response headers.

**Solution**:
Define routing and headers in `netlify.toml`:

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
```

## Best Practices (2026)

- **Do** store all routing, redirects, headers, and build commands in `netlify.toml` for version-controlled reproducibility.
- **Do** use `netlify-honeypot` on HTML forms to prevent automated spam bot submissions.
- **Do** use Netlify Edge Functions for auth checks, localized redirects, and A/B testing at the CDN layer.
- **Do** test builds and serverless functions locally using the Netlify CLI (`netlify dev`).
- **Don't** commit `.env` files containing production secrets; configure environment variables in Netlify UI.
- **Don't** use client-side redirects when Netlify edge redirects (`[[redirects]]`) execute significantly faster.
- **Don't** store large persistent media assets in Git; link to external storage like Cloudinary or S3.

## Troubleshooting

| Error                                         | Cause                                                           | Solution                                                               |
| :-------------------------------------------- | :-------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `Page Not Found (404) on route refresh`       | Missing SPA catch-all redirect rule to `/index.html`.           | Add `/* /index.html 200` to `_redirects` or `netlify.toml`.            |
| `Build failed: command not found: ...`        | Tool or framework dependency not declared in `package.json`.    | Ensure dependencies are in `dependencies` or `devDependencies`.        |
| `Function invocation timed out (default 10s)` | Netlify serverless function taking longer than execution limit. | Optimize database calls or request timeout extension in site settings. |

## References

- [Netlify Documentation](https://docs.netlify.com/)
