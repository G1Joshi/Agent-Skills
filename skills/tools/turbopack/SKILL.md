---
name: turbopack
description: Expert Turbopack assistance covering Next.js incremental compilation, Rust-based bundler architecture, dev server acceleration, and Webpack loader compatibility. Use when enabling Turbopack in Next.js projects, diagnosing build cache invalidations, or migrating from Webpack.
---

# Turbopack

Turbopack is the build engine built by Vercel. In 2025, it is **Stable** in Next.js and powers the fastest dev server in the ecosystem.

## When to Use

- **High-Speed Next.js Development Server**: Sub-second dev server boot and instantaneous Hot Module Replacement (HMR).
- **Large Monorepo Web Applications**: Replacing Webpack with Rust-based compilation engineered for massive TypeScript codebases.
- **Zero-Config Asset Pipelines**: Bundling modern ECMAScript, JSX, TSX, CSS Modules, Tailwind, and PostCSS out of the box.
- **Turborepo Monorepo Orchestration**: Leveraging Turbopack inside Turbo-managed multi-package workspaces with remote caching.

## Quick Start

### 1. Enable Turbopack in Next.js

```json
// package.json
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build --turbopack"
  }
}
```

### 2. Run Dev Server

```bash
npm run dev
# Turbopack compiles pages on-demand with instant HMR
```

## Core Concepts

### Enabling Turbopack in Next.js (`package.json`)

Activating Turbopack dev server and production builds:

```json
{
  "name": "enterprise-web",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev --turbopack --port 3000",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "typescript": "^5.4.0",
    "@types/react": "^19.0.0"
  }
}
```

### Custom Loader Configuration (`next.config.mjs`)

Configuring Turbopack rules for SVGs and custom transformers:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  turbopack: {
    rules: {
      "*.svg": {
        loaders: ["@svgr/webpack"],
        as: "*.js",
      },
    },
    resolveAlias: {
      "@components/*": ["./src/components/*"],
      "@lib/*": ["./src/lib/*"],
    },
  },
  experimental: {
    turbo: {
      resolveExtensions: [".mdx", ".tsx", ".ts", ".jsx", ".js", ".json"],
    },
  },
};

export default nextConfig;
```

### Turborepo Workspace Integration (`turbo.json`)

Orchestrating Turbopack builds with remote caching across micro-frontends:

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"],
      "env": ["NEXT_PUBLIC_API_URL", "NODE_ENV"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^lint"]
    }
  }
}
```

## Common Patterns

### Configuring Custom Webpack Loaders with Turbopack

**Problem**: Need SVG inlining or custom loader processing while running Next.js under Turbopack.  
**Solution**: Configure `experimental.turbo` rules in `next.config.js`.

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    turbo: {
      rules: {
        "*.svg": {
          loaders: ["@svgr/webpack"],
          as: "*.js",
        },
      },
    },
  },
};

module.exports = nextConfig;
```

### Incremental File System Caching

**Problem**: Maximize build speed on large monorepos with hundreds of routes.  
**Solution**: Ensure persistent disk caching is enabled in Turborepo configuration (`turbo.json`).

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**"]
    }
  }
}
```

## Best Practices (2026)

- **Do** run `next dev --turbopack` during local development to gain up to 10x faster startup and HMR times.
- **Do** define path aliases in `tsconfig.json` so Turbopack automatically resolves module imports.
- **Do** use native CSS Modules and Tailwind CSS, which are deeply optimized for Turbopack compilation.
- **Do** monitor memory consumption on massive monorepos using Turborepo daemon (`turbo daemon`).
- **Don't** use legacy Webpack plugins that do not have Turbopack loader equivalents.
- **Don't** disable persistent caching in production CI pipelines; configure Turborepo Remote Caching.
- **Don't** perform heavy synchronous file system reads inside client component code.

## Troubleshooting

| Error / Symptom                    | Cause                                                                 | Solution                                                                                               |
| ---------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Unsupported Webpack plugin warning | Custom Webpack plugins in `next.config.js` not supported in Turbopack | Migrate logic to Turbopack loader rules under `experimental.turbo.rules` or run without `--turbopack`. |
| CSS module class name mismatch     | Conflicting PostCSS or Tailwind CSS configuration                     | Verify `postcss.config.js` uses standard `@tailwindcss/postcss` plugin compatible with Rust compiler.  |
| Cache invalidation on every run    | Dynamic environment variable or non-deterministic build script        | Specify explicit `env` variables in `turbo.json` task inputs.                                          |

## References

- [Turbopack Documentation](https://turbo.build/pack)
