---
name: biome
description: Expert Biome toolchain assistance covering ultra-fast Rust-based formatting, linting, and imports sorting. Use when configuring Biome, replacing Prettier and ESLint, or enforcing sub-millisecond CI lint gates in JavaScript/TypeScript projects.
---

# Biome

Biome is a unified, high-performance toolchain written in Rust that provides sub-millisecond code formatting and linting for JavaScript, TypeScript, and JSON.

## When to Use

- **Ultra-Fast Rust-Powered Linter & Formatter**: Formatting and linting JavaScript, TypeScript, JSX, and JSON 25x faster than Prettier/ESLint.
- **Unified Toolchain Setup**: Replacing separate ESLint, Prettier, and import-sorter configs with a single `biome.json`.
- **Instant CI Verification**: Checking formatting, imports, and syntax in sub-seconds in automated CI pipelines.
- **Prettier & ESLint Migration**: Automated zero-friction migration using `biome migrate`.

## Quick Start

```bash
# Initialize Biome configuration in project
npx @biomejs/biome init

# Format and lint entire workspace in milliseconds
npx @biomejs/biome check --write ./src
```

## Core Concepts

### Declarative Configuration (biome.json)

Consolidating formatting, linting, and import sorting:

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "formatter": {
    "enabled": true,
    "formatWithErrors": false,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "suspicious": {
        "noExplicitAny": "error"
      },
      "style": {
        "useConst": "error"
      }
    }
  },
  "organizeImports": {
    "enabled": true
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "semicolons": "always"
    }
  }
}
```

### Biome CLI Execution in Workflows

Formatting, checking, and applying autofixes:

```bash
# Check formatting, lint rules, and import ordering
npx @biomejs/biome check .

# Automatically apply safe fixes and formatting across all files
npx @biomejs/biome check --write .

# Format only (drop-in Prettier replacement)
npx @biomejs/biome format --write ./src

# CI verification (fails with non-zero exit code if changes needed)
npx @biomejs/biome ci .
```

### Migrating from Prettier & ESLint

Importing existing rules automatically:

```bash
# Migrate from Prettier configuration
npx @biomejs/biome migrate prettier --write

# Migrate from ESLint configuration
npx @biomejs/biome migrate eslint --write
```

## Common Patterns

### Complete biome.json Configuration with Recommended Rules

**Problem**: Slow CI linters (ESLint + Prettier taking >60s on large codebases).

**Solution**:
Adopt unified `biome.json` replacing both:

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "organizeImports": { "enabled": true },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "correctness": { "noUnusedVariables": "error" }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  }
}
```

## Best Practices

**Do**:

- Target Biome 1.9+ as a unified linter, formatter, and import-sorter to eliminate multiple competing tools.
- Run `biome ci .` in CI pipelines to enforce formatting and lint rules in a fraction of a second.
- Enable `useIgnoreFile: true` so Biome automatically respects your `.gitignore` rules.
- Install the official Biome VS Code / Neovim extension for instant formatting on save.

**Don't**:

- Run Prettier and Biome simultaneously on the same files; they will conflict.
- Use `--unsafe` autofix flags in automated CI jobs without human review.
- Ignore schema validation; keep `$schema` set in `biome.json` for IDE autocomplete.

## Troubleshooting

| Error                                       | Cause                                                  | Solution                                                                                               |
| :------------------------------------------ | :----------------------------------------------------- | :----------------------------------------------------------------------------------------------------- |
| `Biome failed to parse file`                | Unsupported syntax or invalid JSON/CSS file extension. | Add path glob to `files.ignore` in `biome.json`.                                                       |
| `Conflict with ESLint / Prettier in editor` | Multiple formatters configured simultaneously in IDE.  | Set Biome as default formatter in `.vscode/settings.json`: `editor.defaultFormatter: "biomejs.biome"`. |
| `biome command not found in CI`             | Package not installed in dependencies.                 | Use `npx @biomejs/biome ci ./src` in CI pipeline.                                                      |

## References

- [Biome Documentation](https://biomejs.dev/)
