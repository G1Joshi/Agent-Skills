---
name: esbuild
description: Expert esbuild bundler assistance covering blazing-fast Go-based bundling, JSX/TS transforms, minification, and API usage. Use when bundling modern web apps, TypeScript libraries, or Node.js backends.
---

# esbuild

esbuild changed the industry by proving that build tools could be 100x faster if written in Go/Rust. It is not just a bundler but a transpiler.

## When to Use

- **Ultra-Fast JavaScript/TypeScript Bundling**: Compiling and bundling web applications 10x-100x faster than Webpack or Rollup.
- **Underlying Bundling Engine for Modern Tools**: Powering Vite, AWS CDK, and serverless deployment packagers.
- **High-Speed Code Minification**: Minifying JS and CSS bundles in CI/CD pipelines with minimal memory overhead.
- **Custom Build Scripts via Go/JS API**: Orchestrating complex builds, asset copying, and source map generation programmatically.

## Quick Start

```bash
# Bundle and minify TypeScript CLI or application in milliseconds
npx esbuild src/index.ts \
  --bundle \
  --platform=node \
  --target=node20 \
  --outfile=dist/bundle.js \
  --minify \
  --sourcemap
```

## Core Concepts

#Programmatic Build API with esbuild.build()

Configuring a production bundle script in Node.js:

```javascript
// build.js
import * as esbuild from "esbuild";

const isProduction = process.env.NODE_ENV === "production";

await esbuild.build({
  entryPoints: ["src/index.ts"],
  bundle: true,
  outfile: "dist/bundle.js",
  platform: "browser",
  target: ["es2022", "chrome100", "firefox100", "safari15"],
  format: "esm",
  minify: isProduction,
  sourcemap: !isProduction,
  treeShaking: true,
  loader: {
    ".png": "dataurl",
    ".svg": "text",
  },
  define: {
    "process.env.NODE_ENV": JSON.stringify(
      process.env.NODE_ENV || "development",
    ),
  },
  logLevel: "info",
});

console.log("Build completed successfully.");
```

#Authoring a Custom esbuild Plugin

Intercepting imports and resolving virtual modules:

```javascript
const envPlugin = {
  name: "env-virtual-module",
  setup(build) {
    // Intercept import statements matching 'virtual:env'
    build.onResolve({ filter: /^virtual:env$/ }, (args) => ({
      path: args.path,
      namespace: "env-ns",
    }));

    // Return virtual content
    build.onLoad({ filter: /.*/, namespace: "env-ns" }, () => ({
      contents: JSON.stringify({
        BUILD_TIME: new Date().toISOString(),
        VERSION: "2026.1.0",
      }),
      loader: "json",
    }));
  },
};
```

#High-Speed CLI Minification

Minifying assets from command line:

```bash
# Minify JavaScript bundle with sourcemap
npx esbuild src/index.ts --bundle --minify --sourcemap --outfile=dist/app.min.js

# Minify CSS stylesheet
npx esbuild styles/main.css --minify --outfile=dist/main.min.css
```

## Common Patterns

### Build Script with Watch Mode and Development Server

**Problem**: Fast iterative local development without heavy Webpack/Vite overhead.

**Solution**:
Use esbuild's asynchronous JavaScript API:

```javascript
import * as esbuild from "esbuild";

const ctx = await esbuild.context({
  entryPoints: ["src/app.tsx"],
  bundle: true,
  outfile: "public/bundle.js",
  sourcemap: true,
  target: ["es2022"],
});

// Watch files for changes and serve on localhost
await ctx.watch();
const { host, port } = await ctx.serve({ servedir: "public" });
console.log(`Server listening on http://${host}:${port}`);
```

## Best Practices (2026)

- **Do** target `platform: 'neutral'` or `format: 'esm'` for modern library bundling.
- **Do** enable `treeShaking: true` to eliminate dead code from external dependencies.
- **Do** use `esbuild.context()` when building local development servers with instant hot rebuilding.
- **Do** use `define` to statically replace environment variables at build time.
- **Don't** rely on esbuild for TypeScript type checking; always run `tsc --noEmit` alongside esbuild in CI.
- **Don't** use esbuild for legacy ES5 transpilation; esbuild focuses on modern ES2015+ targets.
- **Don't** author complex AST code transformation plugins in esbuild; esbuild intentionally does not expose an AST.

## Troubleshooting

| Error                                             | Cause                                               | Solution                                                                |
| :------------------------------------------------ | :-------------------------------------------------- | :---------------------------------------------------------------------- |
| `Dynamic require of "..." is not supported`       | Bundling CommonJS dynamic requires into ESM bundle. | Set `--platform=node` or add external module: `--external:module_name`. |
| `Type annotations stripped without type checking` | esbuild does not type-check (transpiles only).      | Run `tsc --noEmit` concurrently in your build script.                   |
| `Unexpected character in CSS file`                | Bundling CSS without appropriate loader configured. | Add `--loader:.css=css` or `--loader:.png=file`.                        |

## References

- [esbuild Documentation](https://esbuild.github.io/)
