---
name: bun
description: Bun fast JavaScript runtime and bundler. Use for fast JS development.
---

# Bun

Bun is a drop-in replacement for Node.js, written in Zig. It is **fast**. v1.1 brings Windows support.

## When to Use

- **Speed**: `bun install` is instant. `bun run` starts instantly.
- **Local Dev**: Use it as a package manager even if you use Node.js for production.
- **Testing**: `bun test` is a fast, Jest-compatible test runner.

## Core Concepts

### Drop-in Replacement

Implements Node APIs (`fs`, `http`, `path`).

### Bundle / Transpile

Built-in transpiler for TS/JSX.

### Macros

Run code at build time.

## Best Practices (2025)

**Do**:

- **Use `bun install`**: It's compatible with `package-lock.json` but faster.
- **Use `bun test`**: It's much faster than Jest/Vitest.
- **Use `Bun.serve`**: For max performance HTTP servers.

**Don't**:

- **Don't use for everything**: Some niche Node C++ addons might still have issues.

## References

- [Bun Documentation](https://bun.sh/)
