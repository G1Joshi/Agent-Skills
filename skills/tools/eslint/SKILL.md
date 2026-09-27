---
name: eslint
description: Expert ESLint assistance covering Flat Config (eslint.config.js), typescript-eslint, custom rules, and automated formatting. Use when enforcing code quality and preventing bugs in JavaScript/TypeScript.
---

# ESLint

ESLint is the standard linter for JS/TS. v9 (2024/2025) moved to **Flat Config** (`eslint.config.js`), a major breaking change that simplifies configuration.

## When to Use

- **Static Code Analysis for JavaScript/TypeScript**: Catching bugs, anti-patterns, and syntax errors before code review.
- **Modern ESLint Flat Config (eslint.config.js)**: Unified, composable configuration format in ESLint v9+.
- **Enforcing TypeScript Best Practices**: Integrating `@typescript-eslint` with type-aware lint rules.
- **Team Code Standardization**: Automating rule compliance across React, Next.js, Vue, and Node.js codebases.

## Quick Start

```javascript
// eslint.config.mjs (Modern Flat Config)
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      "no-console": "warn",
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_" },
      ],
    },
  },
);
```

## Core Concepts

#Modern Flat Config Architecture (eslint.config.js)

Configuring ESLint v9+ with TypeScript and React:

```javascript
// eslint.config.js
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import reactPlugin from "eslint-plugin-react";
import reactHooksPlugin from "eslint-plugin-react-hooks";

export default tseslint.config(
  // Global ignore rules
  { ignores: ["dist/", "build/", "node_modules/", ".next/"] },

  // Base recommended JavaScript rules
  js.configs.recommended,

  // TypeScript recommended with type-checking rules
  ...tseslint.configs.recommendedTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        project: "./tsconfig.json",
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },

  // React and Hooks rules
  {
    files: ["**/*.{tsx,jsx}"],
    plugins: {
      react: reactPlugin,
      "react-hooks": reactHooksPlugin,
    },
    rules: {
      ...reactHooksPlugin.configs.recommended.rules,
      "react/react-in-jsx-scope": "off", // Not needed in React 17+
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_" },
      ],
      "no-console": ["warn", { allow: ["warn", "error"] }],
    },
  },
);
```

#Authoring a Custom Lint Rule

Creating a custom organizational lint rule:

```javascript
// rules/no-hardcoded-api-urls.js
export default {
  meta: {
    type: "problem",
    docs: {
      description: "Disallow hardcoded internal API URLs in client code",
    },
    messages: {
      noHardcodedUrl:
        "Hardcoded API URL detected. Use environment variables instead.",
    },
  },
  create(context) {
    return {
      Literal(node) {
        if (
          typeof node.value === "string" &&
          node.value.includes("api.internal.company.com")
        ) {
          context.report({ node, messageId: "noHardcodedUrl" });
        }
      },
    };
  },
};
```

#Executing ESLint via CLI

Running analysis and automated fixes:

```bash
# Lint entire repository
npx eslint .

# Automatically fix autofixable problems
npx eslint . --fix

# Lint with caching to speed up recurring runs
npx eslint . --cache --cache-location .eslintcache
```

## Common Patterns

### Strict React Hooks and Accessibility Guardrails

**Problem**: Silent memory leaks and unhandled dependency arrays in React components.

**Solution**:
Configure React and Hooks plugins in Flat Config:

```javascript
import reactHooks from "eslint-plugin-react-hooks";
import jsxA11y from "eslint-plugin-jsx-a11y";

export default [
  {
    plugins: {
      "react-hooks": reactHooks,
      "jsx-a11y": jsxA11y,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      "react-hooks/exhaustive-deps": "error",
      "jsx-a11y/alt-text": "error",
    },
  },
];
```

## Best Practices (2026)

- **Do** migrate to ESLint Flat Config (`eslint.config.js` / `eslint.config.mjs`); legacy `.eslintrc.*` is deprecated in ESLint v9+.
- **Do** enable `recommendedTypeChecked` from `typescript-eslint` for deep semantic type validation.
- **Do** use `--cache` in CI and local scripts to only lint modified files.
- **Do** ignore files via the top-level `{ ignores: [...] }` object in `eslint.config.js`.
- **Don't** use ESLint for code formatting (indentation, semicolons); delegate formatting to Biome or Prettier.
- **Don't** disable rules globally with inline comments (`/* eslint-disable */`); disable specifically with rationale.
- **Don't** enable type-aware rules without supplying `parserOptions.project`; it causes parser errors.

## Troubleshooting

| Error                                               | Cause                                                                                    | Solution                                                        |
| :-------------------------------------------------- | :--------------------------------------------------------------------------------------- | :-------------------------------------------------------------- |
| `ESLint couldn't find a configuration file`         | Project running ESLint v9+ without `eslint.config.js` or `ESLINT_USE_FLAT_CONFIG=false`. | Migrate to Flat Config (`eslint.config.js`) or set legacy flag. |
| `Parsing error: Cannot read file .../tsconfig.json` | `parserOptions.project` path incorrectly configured.                                     | Verify `tsconfig.json` path in `typescript-eslint` config.      |
| `Definition for rule '...' was not found`           | Plugin imported but missing in `plugins:` object.                                        | Declare plugin name in config `plugins` map.                    |

## References

- [ESLint Documentation](https://eslint.org/)
