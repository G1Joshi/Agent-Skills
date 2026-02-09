---
name: eslint
description: ESLint JavaScript/TypeScript linting with rules and plugins. Use for code quality.
---

# ESLint

Pluggable linting for JavaScript and TypeScript.

## When to Use

- Enforcing code style
- Catching bugs early
- TypeScript type checking
- CI/CD quality gates

## Quick Start

```bash
# Install
npm init @eslint/config@latest

# Run
npx eslint .
npx eslint --fix .
```

## Core Concepts

### Flat Config (ESLint 9+)

```javascript
// eslint.config.js
import js from "@eslint/js";
import typescript from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import react from "eslint-plugin-react";

export default [
  js.configs.recommended,
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        project: "./tsconfig.json",
      },
    },
    plugins: {
      "@typescript-eslint": typescript,
      react,
    },
    rules: {
      "@typescript-eslint/no-unused-vars": "error",
      "@typescript-eslint/no-explicit-any": "warn",
      "react/prop-types": "off",
    },
  },
  {
    ignores: ["dist/**", "node_modules/**"],
  },
];
```

### Custom Rules

```javascript
// Common rule configurations
{
  rules: {
    // Errors
    'no-console': ['error', { allow: ['warn', 'error'] }],
    'no-unused-vars': 'off',
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],

    // Warnings
    'max-lines': ['warn', { max: 300 }],
    'complexity': ['warn', { max: 10 }],

    // Style
    'quotes': ['error', 'single'],
    'semi': ['error', 'always'],
  }
}
```

## Common Patterns

### VS Code Integration

```json
// .vscode/settings.json
{
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```

### Pre-commit Hook

```json
// package.json
{
  "lint-staged": {
    "*.{js,ts,tsx}": ["eslint --fix", "prettier --write"]
  }
}
```

## Best Practices

**Do**:

- Use TypeScript-aware rules
- Configure per-project
- Integrate with CI/CD
- Use format on save

**Don't**:

- Disable rules globally
- Ignore all errors
- Mix legacy and flat config
- Skip TypeScript plugin for TS

## Troubleshooting

| Issue          | Cause            | Solution                      |
| -------------- | ---------------- | ----------------------------- |
| Parser error   | Wrong parser     | Use @typescript-eslint/parser |
| Rule not found | Missing plugin   | Install plugin package        |
| Slow linting   | Type-aware rules | Limit project scope           |

## References

- [ESLint Documentation](https://eslint.org/docs/)
- [TypeScript ESLint](https://typescript-eslint.io/)
