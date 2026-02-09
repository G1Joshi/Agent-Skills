---
name: vite
description: Vite build tool for modern frontend development with HMR. Use for fast dev server and bundling.
---

# Vite

Next-generation frontend build tool with instant HMR.

## When to Use

- Modern frontend development
- React/Vue/Svelte projects
- Fast development server
- Library bundling

## Quick Start

```bash
# Create project
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm run dev
```

## Core Concepts

### Configuration

```typescript
// vite.config.ts
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
    proxy: {
      "/api": {
        target: "http://localhost:8080",
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
        },
      },
    },
  },
});
```

### Environment Variables

```bash
# .env
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My App

# .env.production
VITE_API_URL=https://api.prod.example.com
```

```typescript
// Usage in code
const apiUrl = import.meta.env.VITE_API_URL;
const isDev = import.meta.env.DEV;
```

## Common Patterns

### CSS & Assets

```typescript
// Import CSS
import "./styles.css";
import styles from "./Component.module.css";

// Import assets
import logo from "./logo.svg";
import url from "./image.png?url";
import raw from "./file.txt?raw";
```

### TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "types": ["vite/client"],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"]
}
```

## Best Practices

**Do**:

- Use path aliases for imports
- Configure proper proxy for API
- Enable sourcemaps in dev
- Use environment variables

**Don't**:

- Import from node_modules manually
- Skip TypeScript client types
- Ignore build warnings
- Use CommonJS in ESM project

## Troubleshooting

| Issue            | Cause            | Solution                     |
| ---------------- | ---------------- | ---------------------------- |
| HMR not working  | Browser cache    | Hard refresh or check config |
| Module not found | Path alias issue | Check vite/ts config         |
| Build error      | Dependency issue | Check for CJS/ESM conflicts  |

## References

- [Vite Documentation](https://vitejs.dev/)
- [Vite Plugins](https://vitejs.dev/plugins/)
