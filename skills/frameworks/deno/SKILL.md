---
name: deno
description: Deno secure JavaScript/TypeScript runtime. Use for modern JS backend.
---

# Deno

Deno v2.0 (2024/2025) focuses on **Node.js Compatibility**. It can now run most npm packages and `package.json` projects, removing the biggest barrier to entry.

## When to Use

- **Security**: Sandbox by default. No file/net access unless explicitly allowed.
- **All-in-One**: Built-in linter, formatter, test runner, bundler.
- **TypeScript**: Native support. No config needed.

## Core Concepts

### Permission Model

`deno run --allow-net --allow-read main.ts`.

### URL Imports (Legacy-ish)

`import ... from "https://deno.land/..."`. v2 supports npm specifiers too.

### Deno Deploy

The global edge network designed for Deno.

## Best Practices (2025)

**Do**:

- **Use `jsr`**: The new JavaScript Registry (superset of npm).
- **Use `deno serve`**: High-performance HTTP server.
- **Migrate Node apps**: Try running `deno run main.js` on existing Node projects.

**Don't**:

- **Don't rely heavily on `node_modules`**: Use native Deno/JSR patterns where possible for speed.

## References

- [Deno Documentation](https://deno.com/)
