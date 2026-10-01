---
name: rollup
description: Expert Rollup assistance covering JavaScript library bundling, ESM/CJS output formats, tree-shaking, Rollup plugins, and TypeScript compilation. Use when bundling npm libraries, configuring rollup.config.mjs, minimizing bundle size via dead-code elimination, or building multi-format outputs.
---

# Rollup

Rollup (v4) is the bundler of choice for **libraries**. It produces smaller, cleaner code than Webpack and pioneered Tree Shaking.

## When to Use

- **Modern JavaScript/TypeScript Library Packaging**: Generating optimized ESM and CommonJS bundles with tree-shaking.
- **Zero-Overhead Code Splitting**: Emitting dynamic import chunks and shared modules with minimal wrapper boilerplate.
- **Design System & Component Library Distribution**: Bundling React, Vue, or Web Components with externalized peer dependencies.
- **Custom Toolchain Compilation**: Powering modern bundlers (such as Vite) under the hood for production build generation.

## Quick Start

### 1. Minimal rollup.config.mjs

```javascript
import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import typescript from "@rollup/plugin-typescript";
import terser from "@rollup/plugin-terser";

export default {
  input: "src/index.ts",
  output: [
    { file: "dist/index.cjs", format: "cjs", sourcemap: true },
    { file: "dist/index.mjs", format: "esm", sourcemap: true },
  ],
  plugins: [
    resolve(),
    commonjs(),
    typescript({ tsconfig: "./tsconfig.json" }),
    terser(),
  ],
  external: ["react", "react-dom"],
};
```

### 2. Build via CLI

```bash
npx rollup -c --bundleConfigAsCjs
```

## Core Concepts

### Production ESM / CJS Library Configuration (`rollup.config.mjs`)

Building a TypeScript library with external dependencies and source maps:

```javascript
import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import typescript from "@rollup/plugin-typescript";
import terser from "@rollup/plugin-terser";
import peerDepsExternal from "rollup-plugin-peer-deps-external";

export default {
  input: "src/index.ts",
  output: [
    {
      file: "dist/index.mjs",
      format: "esm",
      sourcemap: true,
    },
    {
      file: "dist/index.cjs",
      format: "cjs",
      sourcemap: true,
      exports: "named",
    },
  ],
  plugins: [
    peerDepsExternal(),
    resolve({ extensions: [".ts", ".js"] }),
    commonjs(),
    typescript({
      tsconfig: "./tsconfig.json",
      declaration: true,
      declarationDir: "dist/types",
    }),
    terser({
      format: { comments: false },
      compress: { drop_console: true },
    }),
  ],
  external: ["react", "react-dom"],
};
```

### Tree-Shaking Verification & Pure Annotations

Optimizing tree-shaking by marking side-effect-free packages and pure function calls:

```javascript
// package.json
{
  "name": "my-math-lib",
  "sideEffects": false
}

// src/utils.ts
/* @__PURE__ */
export const complexCalculation = (a, b) => {
  return a * 1000 + b;
};
```

### Multi-Entrypoint Build Automation

Bundling multiple package subpath exports (`my-lib/core`, `my-lib/react`):

```javascript
export default [
  {
    input: "src/core/index.ts",
    output: { dir: "dist/core", format: "esm" },
    plugins: [typescript()],
  },
  {
    input: "src/react/index.ts",
    output: { dir: "dist/react", format: "esm" },
    plugins: [typescript()],
    external: ["react"],
  },
];
```

## Common Patterns

### Library Bundling with External Dependencies

**Problem**: Third-party peer dependencies (e.g. `lodash`, `react`) get bundled into output library instead of being treated as externals.  
**Solution**: Declare externals using regular expression or `peerDependencies` keys.

```javascript
import pkg from "./package.json" assert { type: "json" };

export default {
  input: "src/index.ts",
  external: [
    ...Object.keys(pkg.dependencies || {}),
    ...Object.keys(pkg.peerDependencies || {}),
    /^node:/, // Mark node built-ins external
  ],
  // ...
};
```

### Preserving Directory Structure (Multi-entry Code Splitting)

**Problem**: Need to build a library where users can import submodules (e.g. `import { helper } from 'my-lib/utils'`).  
**Solution**: Set `output.preserveModules = true`.

```javascript
export default {
  input: ["src/index.ts", "src/utils.ts"],
  output: {
    dir: "dist",
    format: "esm",
    preserveModules: true,
    preserveModulesRoot: "src",
  },
};
```

## Best Practices

**Do**:

- Externalize runtime peer dependencies (`react`, `lodash`) to avoid bundling duplicate copies into consumer packages.
- Set `"sideEffects": false` in `package.json` to enable consumer bundlers to aggressively tree-shake unused code.
- Emit TypeScript declaration files (`.d.ts`) alongside bundles using `@rollup/plugin-typescript`.
- Use `.mjs` extension for Rollup configuration files to ensure native ESM loading in modern Node.js.

**Don't**:

- Use Rollup for complex SPAs when modern bundlers like Vite or Turbopack provide superior dev server workflows.
- Disable source maps for production library builds; consumers need them for stack trace debugging.
- Bundle large Node.js built-ins (`fs`, `path`) into browser library targets without polyfill wrappers.

## Troubleshooting

| Error                                                           | Cause                                                  | Solution                                                                                    |
| --------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| `Unresolved dependencies: '...' treated as external`            | Package import not found by Rollup resolver            | Add `@rollup/plugin-node-resolve` to the `plugins` array.                                   |
| `Cannot find module ... or its corresponding type declarations` | TypeScript plugin tsconfig path mismatch               | Configure `typescript({ tsconfig: "./tsconfig.json", declaration: true, outDir: "dist" })`. |
| `Circular dependency: a.js -> b.js -> a.js`                     | Circular imports causing runtime initialization issues | Refactor circular references or suppress specific warning via `onwarn(warning, warn)` hook. |

## References

- [Rollup Documentation](https://rollupjs.org/)
