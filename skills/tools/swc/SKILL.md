---
name: swc
description: Expert SWC assistance covering high-performance Rust-based JavaScript/TypeScript compilation, .swcrc configuration, Jest testing via @swc/jest, and minification. Use when replacing Babel with SWC for faster builds, accelerating test execution, or compiling modern ECMAScript features.
---

# SWC

SWC (Speedy Web Compiler) is a Rust-based extensible platform. It is the compiler inside **Next.js** and **Deno**.

## When to Use

- **High-Performance JavaScript/TypeScript Transpilation**: Replacing Babel with a Rust-based compiler up to 20x faster.
- **Next.js & Modern Bundler Pipelines**: Transpiling React JSX, TSX, modern ECMAScript features, and Webpack/Turbopack assets.
- **Programmatic AST Manipulation & Code Generation**: Building fast custom build tools using the `@swc/core` Node.js API.
- **Production Asset Minification**: Minifying JS and CSS bundles at extreme speeds using `@swc/core` minifier.

## Quick Start

### 1. Minimal .swcrc

```json
{
  "$schema": "https://json.schemastore.org/swcrc",
  "jsc": {
    "parser": {
      "syntax": "typescript",
      "tsx": true,
      "decorators": true
    },
    "transform": {
      "react": {
        "runtime": "automatic"
      }
    },
    "target": "es2022"
  },
  "minify": false
}
```

### 2. Compile via CLI

```bash
npx @swc/cli src -d dist
```

## Core Concepts

### Production SWC Configuration (`.swcrc`)

Configuring modern TypeScript, React 19 JSX runtime, and module transpilation:

```json
{
  "$schema": "https://json.schemastore.org/swcrc",
  "jsc": {
    "parser": {
      "syntax": "typescript",
      "tsx": true,
      "decorators": true,
      "dynamicImport": true
    },
    "transform": {
      "react": {
        "runtime": "automatic",
        "refresh": true
      }
    },
    "target": "es2022",
    "loose": false,
    "externalHelpers": true,
    "keepClassNames": true,
    "minify": {
      "compress": {
        "unused": true,
        "drop_console": true
      },
      "mangle": true
    }
  },
  "module": {
    "type": "es6"
  },
  "minify": true,
  "sourceMaps": true
}
```

### Programmatic Compilation with `@swc/core` API

Transpiling source files asynchronously in Node.js scripts:

```javascript
import swc from "@swc/core";
import fs from "node:fs/promises";

async function compileTypeScript(filePath) {
  const code = await fs.readFile(filePath, "utf-8");

  const output = await swc.transform(code, {
    filename: filePath,
    sourceMaps: true,
    jsc": {
      parser: { syntax: "typescript", tsx: true },
      target: "es2022",
    },
    module: { type: "commonjs" },
  });

  console.log("Transpiled Code:\n", output.code);
  if (output.map) {
    console.log("Source Map Generated");
  }
}

compileTypeScript("./src/index.ts");
```

### High-Speed CLI Transpilation

Compiling directory trees directly with the SWC command line:

```bash
# Transpile src/ to dist/ with source maps
npx swc src -d dist --copy-files --source-maps

# Transpile and bundle with swcpack
npx swc src/index.ts -o dist/bundle.js --minify
```

## Common Patterns

### Accelerating Jest Tests with @swc/jest

**Problem**: TypeScript transpilation with `ts-jest` makes test suites run very slowly.  
**Solution**: Swap `ts-jest` for `@swc/jest`.

```javascript
// jest.config.js
module.exports = {
  transform: {
    "^.+\.(t|j)sx?$": [
      "@swc/jest",
      {
        jsc: {
          transform: {
            react: { runtime: "automatic" },
          },
        },
      },
    ],
  },
};
```

### SWC Bundling & Minification Pipeline

**Problem**: Need fast minification for production build scripts.  
**Solution**: Enable `minify` options inside `.swcrc`.

```json
{
  "minify": true,
  "jsc": {
    "minify": {
      "compress": {
        "drop_console": true
      },
      "mangle": true
    }
  }
}
```

## Best Practices (2026)

- **Do** install `@swc/helpers` and enable `externalHelpers: true` to avoid duplicating transpiler runtime helper stubs.
- **Do** pair SWC with `tsc --noEmit` in CI/CD pipelines since SWC transpiles code without performing type checking.
- **Do** configure `target: "es2022"` or newer to take advantage of native modern browser capabilities.
- **Do** use `@swc/jest` or `@swc/register` to drastically accelerate unit test execution.
- **Don't** rely on Babel plugins unless strictly necessary; check if native SWC plugins (Wasm plugins) exist.
- **Don't** commit `.swc` build cache directories to Git repositories.
- **Don't** run SWC minification without generating source maps for production troubleshooting.

## Troubleshooting

| Error / Symptom                                                            | Cause                                                                              | Solution                                                                                              |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `failed to handle: error parsing typescript`                               | TypeScript syntax (e.g. JSX or decorators) used without enabling flags in `.swcrc` | Ensure `"syntax": "typescript"`, `"tsx": true`, and `"decorators": true` are present in `jsc.parser`. |
| Decorators metadata not emitting (`Reflect.getMetadata` returns undefined) | `transform.legacyDecorator` and `transform.decoratorMetadata` not configured       | Set `"legacyDecorator": true` and `"decoratorMetadata": true` inside `jsc.transform`.                 |
| `Cannot find module '@swc/core-darwin-arm64'`                              | Native binary install failed during npm/yarn install                               | Run `npm install --force @swc/core` to trigger native binary fetch for target architecture.           |

## References

- [SWC Documentation](https://swc.rs/)
