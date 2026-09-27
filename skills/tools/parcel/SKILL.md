---
name: parcel
description: Expert Parcel assistance covering zero-configuration bundling, transformer plugins, SVG/CSS/SCSS asset pipelines, code splitting, and multi-target builds. Use when bundling web apps without complex Webpack setups, configuring .parcelrc, debugging build caches, or compiling modern JavaScript.
---

# Parcel

Parcel is the "Zero Config" bundler. It works out of the box for React, Vue, Rust (Wasm), and more. v2.12 uses **Lightning CSS** for extreme performance.

## When to Use

- **Zero-Config Web Application Bundling**: Bundling modern web apps, TypeScript, JSX, SCSS, and HTML without manual configuration.
- **High-Performance Rust-Based Compilation**: Leveraging SWC-based transpilation and multithreaded caching out of the box.
- **Full-Stack Asset Pipelines**: Bundling SPAs, web workers, WebAssembly, and service workers automatically from HTML entrypoints.
- **Micro-Frontend & Library Building**: Outputting ESM, CommonJS, and UMD bundles with automated source maps.

## Quick Start

### 1. Initialize and Run Parcel

```bash
npm install --save-dev parcel
```

```json
// package.json
{
  "name": "my-app",
  "source": "src/index.html",
  "scripts": {
    "start": "parcel",
    "build": "parcel build"
  },
  "devDependencies": {
    "parcel": "^2.12.0"
  }
}
```

### 2. Start Dev Server

```bash
npm start
# Server listening on http://localhost:1234
```

## Core Concepts

### HTML-First Bundling & Zero-Config Setup

Building a TypeScript React application starting directly from `index.html`:

```html
<!-- src/index.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Parcel React App</title>
    <link rel="stylesheet" href="./styles.scss" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="./index.tsx"></script>
  </body>
</html>
```

### Production Build & Library Configuration (`package.json`)

Configuring dual ESM and CommonJS library output with automated types:

```json
{
  "name": "my-shared-library",
  "version": "1.0.0",
  "source": "src/index.ts",
  "main": "dist/index.cjs",
  "module": "dist/index.mjs",
  "types": "dist/index.d.ts",
  "scripts": {
    "start": "parcel src/index.html --port 3000 --open",
    "build": "parcel build src/index.html --dist-dir build --public-url /",
    "build:lib": "parcel build"
  },
  "devDependencies": {
    "@parcel/packager-ts": "^2.12.0",
    "@parcel/transformer-sass": "^2.12.0",
    "@parcel/transformer-typescript-types": "^2.12.0",
    "parcel": "^2.12.0"
  }
}
```

### Advanced Pipeline Customization (`.parcelrc`)

Extending the default pipeline with custom transformers and compressors:

```json
{
  "extends": "@parcel/config-default",
  "transformers": {
    "*.svg": ["@parcel/transformer-svg", "@parcel/transformer-svgo"]
  },
  "compressors": {
    "*.{html,css,js,svg}": [
      "@parcel/compressor-gzip",
      "@parcel/compressor-brotli"
    ]
  }
}
```

## Common Patterns

### Custom .parcelrc Pipeline Extension

**Problem**: Need custom asset transformation (e.g. SVG inlining or custom minifier) alongside default presets.  
**Solution**: Create `.parcelrc` extending default config.

```json
{
  "extends": "@parcel/config-default",
  "transformers": {
    "*.svg": ["@parcel/transformer-svg", "..."]
  },
  "reporters": ["...", "@parcel/reporter-bundle-analyzer"]
}
```

### Multi-Target Library and Browser Output

**Problem**: Build a library for both modern browser ESM and CommonJS node usage.  
**Solution**: Declare multiple targets in `package.json`.

```json
{
  "name": "lib-core",
  "source": "src/index.ts",
  "main": "dist/index.cjs",
  "module": "dist/index.mjs",
  "types": "dist/index.d.ts",
  "targets": {
    "main": {},
    "module": {}
  }
}
```

## Best Practices (2026)

- **Do** use HTML files as entrypoints (`parcel src/index.html`) so Parcel automatically detects all dependent scripts, styles, and assets.
- **Do** configure `targets` in `package.json` with Browserslist queries for precise polyfill generation.
- **Do** cache `.parcel-cache` across CI/CD pipeline runs to achieve instantaneous subsequent builds.
- **Do** enable `--detailed-report` during production builds to analyze asset bundle weights.
- **Don't** mix conflicting custom webpack configs inside Parcel projects; rely on `.parcelrc`.
- **Don't** commit `.parcel-cache` or `dist/` directories to version control.
- **Don't** manually compile Sass or TypeScript before passing files to Parcel; let Parcel handle the transformation pipeline.

## Troubleshooting

| Error / Symptom                                                                            | Cause                                                                      | Solution                                                                         |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Stale build output or cache corruption                                                     | `.parcel-cache/` containing invalid serialized graph states                | Run `rm -rf .parcel-cache dist` and restart `parcel`.                            |
| `@parcel/core: Failed to resolve module`                                                   | Relative import missing extension or package missing in dependencies       | Verify file path casing, ensure module is listed in `package.json` dependencies. |
| Production build fail: `Target "main" declared in package.json but source is an HTML file` | `main` field mistakenly points to `.js` when bundling single-page HTML app | Remove `"main": "index.js"` from `package.json` when building web applications.  |

## References

- [Parcel Documentation](https://parceljs.org/)
