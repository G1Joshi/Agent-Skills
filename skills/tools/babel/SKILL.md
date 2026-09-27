---
name: babel
description: Expert Babel compiler assistance covering AST transforms, presets (@babel/preset-env, @babel/preset-react), and polyfilling via core-js. Use when transpiling modern ECMAScript/TypeScript for legacy targets.
---

# Babel

Babel is the transpiler that made ES6+ possible. While slower than SWC/esbuild, it remains the most **extensible** compiler with the largest plugin ecosystem.

## When to Use

- **JavaScript / TypeScript Transpilation**: Compiling modern ESNext, JSX, and TypeScript into backward-compatible JavaScript.
- **Custom AST Code Transformations**: Developing Babel plugins to automate code instrumentation, stripping, or macro generation.
- **Polyfill Injection via core-js**: Automatically injecting polyfills for target browser matrices using `@babel/preset-env`.
- **Legacy Framework Support**: Maintaining React and Webpack toolchains that depend on Babel transpilation.

## Quick Start

```json
// babel.config.json
{
  "presets": [
    [
      "@babel/preset-env",
      {
        "targets": "> 0.25%, not dead",
        "useBuiltIns": "usage",
        "corejs": 3
      }
    ],
    ["@babel/preset-react", { "runtime": "automatic" }],
    "@babel/preset-typescript"
  ]
}
```

## Core Concepts

#Modern Project Configuration (babel.config.json)

Transpiling modern TypeScript and React for targeted browsers:

```json
{
  "presets": [
    [
      "@babel/preset-env",
      {
        "targets": "> 0.5%, last 2 versions, not dead",
        "useBuiltIns": "usage",
        "corejs": "3.38",
        "modules": false
      }
    ],
    [
      "@babel/preset-react",
      {
        "runtime": "automatic"
      }
    ],
    "@babel/preset-typescript"
  ],
  "plugins": ["@babel/plugin-transform-runtime"]
}
```

#Authoring a Custom Babel AST Transformation Plugin

Writing an AST visitor that removes `console.log` statements in production:

```javascript
// plugins/babel-plugin-strip-console.js
export default function ({ types: t }) {
  return {
    name: "strip-console-plugin",
    visitor: {
      CallExpression(path) {
        const callee = path.node.callee;
        if (
          t.isMemberExpression(callee) &&
          t.isIdentifier(callee.object, { name: "console" }) &&
          t.isIdentifier(callee.property, { name: "log" })
        ) {
          path.remove();
        }
      },
    },
  };
}
```

#Executing Babel via CLI

Transpiling directories from command line:

```bash
# Compile src/ directory to dist/ with source maps
npx babel src --out-dir dist --extensions ".ts,.tsx,.js" --source-maps inline
```

## Common Patterns

### Custom AST Plugin for Code Transformation

**Problem**: Stripping proprietary debug statements or injecting telemetry tokens during build time.

**Solution**:
Write a Babel visitor plugin:

```javascript
module.exports = function ({ types: t }) {
  return {
    visitor: {
      CallExpression(path) {
        if (path.get("callee").matchesPattern("console.debug")) {
          path.remove();
        }
      },
    },
  };
};
```

## Best Practices (2026)

- **Do** use `useBuiltIns: "usage"` with `core-js` to import only the exact polyfills referenced in your source code.
- **Do** prefer `babel.config.json` over legacy `.babelrc` for consistent monorepo root-level configuration.
- **Do** evaluate whether modern native build tools (SWC, esbuild, Biome) can replace Babel for 10x-50x faster builds.
- **Do** use `@babel/plugin-transform-runtime` to prevent duplicate helper functions across modules.
- **Don't** transpile `node_modules` with Babel unless a third-party package ships untranspiled modern ES features.
- **Don't** set `modules: "commonjs"` if your bundler (Vite, Rollup, Webpack) supports native ES modules.
- **Don't** use Babel for type checking; use `tsc --noEmit` alongside Babel.

## Troubleshooting

| Error                                                                          | Cause                                                                | Solution                                                           |
| :----------------------------------------------------------------------------- | :------------------------------------------------------------------- | :----------------------------------------------------------------- |
| `SyntaxError: Support for the experimental syntax ... isn't currently enabled` | Missing specific Babel plugin or preset for experimental JS feature. | Install and add the required `@babel/plugin-proposal-*` to config. |
| `Cannot find module '@babel/core'`                                             | Peer dependency `@babel/core` missing from project root.             | Run `npm install --save-dev @babel/core`.                          |
| `Duplicate helper functions in output bundle`                                  | Helpers inlined into every file instead of imported.                 | Install `@babel/plugin-transform-runtime` and `@babel/runtime`.    |

## References

- [Babel Documentation](https://babeljs.io/)
