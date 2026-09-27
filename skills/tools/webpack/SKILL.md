---
name: webpack
description: Expert Webpack assistance covering asset bundling, code splitting, loaders, plugins, caching strategies, and webpack.config.js optimization. Use when configuring Webpack 5, optimizing bundle sizes, setting up Babel/TypeScript loaders, or configuring Module Federation.
---

# Webpack

Webpack is the grandfather of bundlers. While slower than Vite, it offers unparalleled **flexibility** and remains the engine behind Next.js (legacy), Angular, and enterprise apps.

## When to Use

- **Enterprise Webpack 5 Bundling**: Managing complex enterprise web applications with custom asset transformations and polyfills.
- **Module Federation Micro-Frontends**: Sharing modules, components, and runtime state dynamically across distributed micro-apps.
- **Granular Code Splitting & Caching**: Fine-tuning split chunks, vendor optimization, and deterministic bundle hashing.
- **Custom Loader & Plugin Architectures**: Extending compilation pipelines with custom AST manipulation and build hooks.

## Quick Start

### 1. Minimal webpack.config.js

```javascript
const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "[name].[contenthash].js",
    clean: true,
  },
  module: {
    rules: [
      { test: /\.css$/i, use: ["style-loader", "css-loader"] },
      { test: /\.(png|svg|jpg)$/i, type: "asset/resource" },
    ],
  },
  plugins: [new HtmlWebpackPlugin({ template: "./public/index.html" })],
  optimization: {
    splitChunks: { chunks: "all" },
  },
};
```

### 2. Build via CLI

```bash
npx webpack --mode production
```

## Core Concepts

### Production Webpack 5 Configuration (`webpack.config.js`)

Configuring modern performance, caching, and splitChunks optimization:

```javascript
const path = require("node:path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");

const isProd = process.env.NODE_ENV === "production";

module.exports = {
  mode: isProd ? "production" : "development",
  entry: "./src/index.tsx",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: isProd ? "js/[name].[contenthash:8].js" : "js/[name].js",
    chunkFilename: isProd
      ? "js/[name].[contenthash:8].chunk.js"
      : "js/[name].chunk.js",
    clean: true,
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  module: {
    rules: [
      {
        test: /\.(ts|tsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "swc-loader",
        },
      },
      {
        test: /\.css$/,
        use: [
          isProd ? MiniCssExtractPlugin.loader : "style-loader",
          "css-loader",
          "postcss-loader",
        ],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: "asset",
        parser: {
          dataUrlCondition: { maxSize: 8 * 1024 }, // Inline under 8KB
        },
      },
    ],
  },
  optimization: {
    minimize: isProd,
    minimizer: [new TerserPlugin(), new CssMinimizerPlugin()],
    splitChunks: {
      chunks: "all",
      cacheGroups: {
        defaultVendors: {
          test: /[\\/]node_modules[\\/]/,
          name: "vendors",
          priority: -10,
          reuseExistingChunk: true,
        },
      },
    },
  },
  plugins: [
    ...(isProd
      ? [
          new MiniCssExtractPlugin({
            filename: "css/[name].[contenthash:8].css",
          }),
        ]
      : []),
  ],
  devServer: {
    port: 3000,
    hot: true,
    historyApiFallback: true,
  },
};
```

### Module Federation Micro-Frontend Configuration

Exposing and consuming shared components at runtime:

```javascript
const { ModuleFederationPlugin } = require("webpack").container;

module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: "host_app",
      remotes: {
        checkout: "checkout@https://cdn.example.com/checkout/remoteEntry.js",
      },
      shared: {
        react: { singleton: true, requiredVersion: "^19.0.0" },
        "react-dom": { singleton: true, requiredVersion: "^19.0.0" },
      },
    }),
  ],
};
```

### Filesystem Caching for Accelerated Builds

Enabling persistent caching to cut subsequent build times by over 80%:

```javascript
module.exports = {
  cache: {
    type: "filesystem",
    buildDependencies: {
      config: [__filename],
    },
  },
};
```

## Common Patterns

### Code Splitting via Dynamic Imports

**Problem**: Reduce initial page weight by deferring heavy components until needed.  
**Solution**: Use ECMAScript dynamic `import()`.

```javascript
// Dynamic route or modal loading
button.addEventListener("click", async () => {
  const { renderModal } = await import(
    /* webpackChunkName: "modal" */ "./components/Modal"
  );
  renderModal();
});
```

### Long-Term Caching Optimization

**Problem**: Ensure updated bundles bust browser cache while unchanged vendor libraries remain cached.  
**Solution**: Separate runtime chunk and extract vendor libraries.

```javascript
module.exports = {
  optimization: {
    runtimeChunk: "single",
    splitChunks: {
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: "vendors",
          chunks: "all",
        },
      },
    },
  },
};
```

## Best Practices (2026)

- **Do** enable `cache: { type: "filesystem" }` in Webpack 5 to dramatically reduce CI/CD build times.
- **Do** use `swc-loader` or `esbuild-loader` in place of `babel-loader` for up to 10x faster transpilation.
- **Do** use `[contenthash:8]` in production output filenames for optimal long-term browser HTTP caching.
- **Do** externalize and isolate shared dependencies with `singleton: true` in Module Federation.
- **Don't** build large production SPAs without configuring `splitChunks` to separate vendor and application code.
- **Don't** include expensive development plugins (e.g. detailed source map generators) in production configurations.
- **Don't** commit `dist/` or `.cache/` build output directories to version control.

## Troubleshooting

| Error / Symptom                                 | Cause                                                          | Solution                                                                                                 |
| ----------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `Module not found: Error: Can't resolve '...'`  | File extension missing from `resolve.extensions` array         | Add `resolve: { extensions: ['.ts', '.tsx', '.js', '.json'] }` to `webpack.config.js`.                   |
| Out of memory (`JavaScript heap out of memory`) | Heavy source maps or source analysis on large dependency graph | Switch `devtool` to `eval-cheap-module-source-map` for development; exclude `node_modules` from loaders. |
| Injected styles not showing in production       | `style-loader` used instead of extracting CSS in production    | Use `MiniCssExtractPlugin.loader` in production builds instead of `style-loader`.                        |

## References

- [Webpack Documentation](https://webpack.js.org/)
