---
name: vite
description: Expert Vite assistance covering modern frontend tooling, ESM development server, rollup-based production builds, Vite plugins, and framework integrations. Use when configuring vite.config.ts, setting up HMR, optimizing dependency pre-bundling, or building SPA/SSR applications.
---

# Vite

Vite is the modern frontend build tool providing an ultra-fast ESM development server, rich plugin ecosystem, and flexible Environment API for cross-runtime SSR.

## When to Use

- **High-Speed Frontend Application Development**: Instant dev server startup and lightning-fast HMR for React, Vue, Svelte, and Solid.
- **Optimized Production Bundling**: Generating tree-shaken, code-split production bundles using Rollup and esbuild.
- **Modern Full-Stack SSR & Library Development**: Building SSR setups, component libraries, and client-side SPAs.
- **Fast Unit & Component Testing with Vitest**: Executing unit tests using the identical Vite transform pipeline.

## Quick Start

### 1. Minimal vite.config.ts

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,
    open: true,
  },
  build: {
    target: "esnext",
    sourcemap: true,
  },
});
```

### 2. Scaffold and Run

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app && npm install && npm run dev
```

## Core Concepts

### Production Configuration (`vite.config.ts`)

Configuring plugins, build optimizations, path aliases, and local HTTPS:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "node:path";
import basicSsl from "@vitejs/plugin-basic-ssl";

export default defineConfig({
  plugins: [react(), basicSsl()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@components": path.resolve(__dirname, "./src/components"),
    },
  },
  server: {
    port: 3000,
    strictPort: true,
    open: true,
  },
  build: {
    target: "es2022",
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom", "react-router-dom"],
        },
      },
    },
    chunkSizeWarningLimit: 600,
  },
});
```

### Seamless Unit Testing with Vitest

Configuring Vitest directly within `vite.config.ts`:

```typescript
/// <reference types="vitest" />
import { defineConfig } from "vite";

export default defineConfig({
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
    },
  },
});
```

### Static Asset & Web Worker Handling

Importing assets and initializing Web Workers with native Vite syntax:

```typescript
// Import raw SVG string or URL
import logoUrl from "./assets/logo.svg";
import rawSvg from "./assets/logo.svg?raw";

// Spawn Web Worker with native ESM support
const worker = new Worker(new URL("./workers/compute.ts", import.meta.url), {
  type: "module",
});

worker.postMessage({ task: "PROCESS_IMAGE", data: [] });
worker.onmessage = (event) => console.log("Result:", event.data);
```

## Common Patterns

### Proxy API Requests in Development

**Problem**: Avoid CORS errors when frontend on `localhost:3000` talks to backend on `localhost:8080`.  
**Solution**: Configure dev server reverse proxy in `vite.config.ts`.

```typescript
export default defineConfig({
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8080",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
```

### Dynamic Code Splitting and Manual Chunks

**Problem**: Large vendor packages (e.g. `lodash`, `chart.js`) inflate initial bundle chunk.  
**Solution**: Configure `manualChunks` in Rollup output options.

```typescript
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          charts: ["chart.js"],
        },
      },
    },
  },
});
```

## Best Practices

**Do**:

- Use `@vitejs/plugin-react-swc` instead of Babel for maximum transpilation and HMR performance.
- Configure `manualChunks` in `rollupOptions` to split large vendor dependencies (React, UI libraries) into cached chunks.
- Pair Vite with **Vitest** to share the exact same configuration, plugins, and module resolution rules.
- Enforce `strictPort: true` in CI environments to prevent silent port fallback collisions.

**Don't**:

- Use Webpack-specific syntax (`require.context`, `module.hot`); use standard `import.meta.glob`.
- Leave source maps enabled in public production builds without uploading them to private error trackers (Sentry).
- Commit `dist/` or `.vite/` cache directories to Git.

## Troubleshooting

| Error                                                          | Cause                                                                          | Solution                                                                                  |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| `[vite] Internal server error: Failed to resolve import "..."` | Missing path alias or file extension                                           | Add alias in `resolve.alias` inside `vite.config.ts` and verify file exists.              |
| HMR stops updating in browser without full reload              | Circular dependencies or component missing explicit React default/named export | Break circular dependency chain; ensure React components have capitalized function names. |
| `Outdated optimize dep` warning                                | Dependencies changed without clearing Vite cache                               | Run `npx vite --force` or delete `node_modules/.vite`.                                    |

## References

- [Vite Documentation](https://vitejs.dev/)
