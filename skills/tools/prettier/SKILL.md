---
name: prettier
description: Expert Prettier assistance covering opinionated code formatting, .prettierrc configuration, editor integration, ESLint conflict resolution via eslint-config-prettier, and CI lint checks. Use when enforcing consistent code formatting, setting up pre-commit formatting hooks, or resolving syntax parser conflicts.
---

# Prettier

Prettier ended the "Style Wars". It accepts your code and reprints it with its own rules. v3.x runs as ESM and supports plugins.

## When to Use

- **Opinionated Code Formatting**: Enforcing consistent code formatting across JavaScript, TypeScript, CSS, HTML, JSON, and Markdown.
- **Automated CI/CD Quality Gates**: Verifying formatting compliance using `prettier --check` before merging pull requests.
- **Pre-Commit Hook Formatting**: Automatically formatting staged files with Husky and `lint-staged`.
- **Framework Plugin Integration**: Sorting Tailwind CSS classes (`prettier-plugin-tailwindcss`) and Prisma schemas.

## Quick Start

### 1. Minimal .prettierrc

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2
}
```

### 2. Format and Check Commands

```bash
# Format entire repository
npx prettier --write .

# Check without modifying (CI mode)
npx prettier --check .
```

## Core Concepts

### Modern Production Configuration (`.prettierrc.json`)

Defining standard formatting rules and plugin integrations:

```json
{
  "$schema": "https://json.schemastore.org/prettierrc",
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": false,
  "trailingComma": "all",
  "bracketSpacing": true,
  "bracketSameLine": false,
  "arrowParens": "always",
  "endOfLine": "lf",
  "plugins": ["prettier-plugin-tailwindcss"],
  "overrides": [
    {
      "files": "*.md",
      "options": {
        "proseWrap": "always"
      }
    }
  ]
}
```

### Prettier Ignore File (`.prettierignore`)

Excluding build artifacts, lockfiles, and generated files:

```text
# .prettierignore
node_modules
dist
build
.next
.turbo
coverage
package-lock.json
pnpm-lock.yaml
yarn.lock
*.min.js
```

### Git Pre-Commit Hook Integration (`lint-staged`)

Formatting only staged files on commit using `package.json`:

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx,css,md,json}": ["prettier --write"]
  },
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

## Common Patterns

### ESLint and Prettier Integration Without Conflicts

**Problem**: ESLint formatting rules collide with Prettier's layout choices.  
**Solution**: Disable all styling rules in ESLint using `eslint-config-prettier`.

```json
// package.json / eslint.config.js (ESLint v9 Flat Config)
import eslintConfigPrettier from "eslint-config-prettier";

export default [
  // ... base JS/TS rules
  eslintConfigPrettier, // must be last to override conflicting rules
];
```

### Pre-commit Formatting Hook with lint-staged

**Problem**: Automatically format modified files before git commit to keep commit history clean.  
**Solution**: Combine `husky` and `lint-staged`.

```json
// package.json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx,json,css,md}": ["prettier --write"]
  }
}
```

## Best Practices

**Do**:

- Run `prettier --check .` in CI pipelines to ensure zero unformatted code enters the repository.
- Install official plugins such as `prettier-plugin-tailwindcss` to enforce deterministic class sorting.
- Disable all conflicting ESLint formatting rules using `eslint-config-prettier`.
- Specify `endOfLine: "lf"` to avoid cross-platform git line-ending conflicts between Windows and Unix.

**Don't**:

- Argue over code style details in code reviews; let Prettier make the formatting decisions automatically.
- Run formatting on minified or third-party vendor bundles; exclude them via `.prettierignore`.
- Configure ESLint rules that duplicate formatting (e.g. quotes, semi); delegate formatting exclusively to Prettier.

## Troubleshooting

| Error                                                | Cause                                                     | Solution                                                                                       |
| ---------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `Code style issues found in 12 files` in CI          | Files modified without running Prettier before commit     | Add pre-commit hook with `lint-staged` or run `npx prettier --write .` and commit changes.     |
| ESLint and Prettier fighting over quotes or indent   | ESLint rule `semi` or `quotes` enabled alongside Prettier | Add `eslint-config-prettier` to end of ESLint config to deactivate formatting rules in ESLint. |
| Syntax error parsing modern syntax (e.g. decorators) | Outdated parser selected for file type                    | Specify parser explicitly in `.prettierrc` under `overrides` (e.g. `parser: "typescript"`).    |

## References

- [Prettier Documentation](https://prettier.io/)
