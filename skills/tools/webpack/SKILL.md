---
name: webpack
description: Webpack module bundler with loaders and plugins. Use for bundling.
---

# Webpack

Webpack is the grandfather of bundlers. While slower than Vite, it offers unparalleled **flexibility** and remains the engine behind Next.js (legacy), Angular, and enterprise apps.

## When to Use

- **Complex Federation**: Module Federation (Micro-frontends) is best in Webpack / Rspack.
- **Legacy Apps**: Migrating a massive app to Vite might be too costly.
- **Granular Control**: You need to control every byte of the chunk splitting algorithm.

## Core Concepts

### Loaders

Transform files. `ts-loader`, `css-loader`, `file-loader`.

### Plugins

Tap into the build lifecycle. `HtmlWebpackPlugin`, `DefinePlugin`.

### Module Federation

Allows a JavaScript application to dynamically load code from another application.

## Best Practices (2025)

**Do**:

- **Consider Rspack**: If Webpack is too slow, Rspack is a Rust-based drop-in replacement.
- **Use `swc-loader`**: Replace `babel-loader` with `swc-loader` for 20x speedup.

**Don't**:

- **Don't start new projects with it**: Use Vite or generic frameworks (Next.js) instead.

## References

- [Webpack Documentation](https://webpack.js.org/)
