---
name: prettier
description: Prettier code formatter for consistent style. Use for formatting.
---

# Prettier

Prettier ended the "Style Wars". It accepts your code and reprints it with its own rules. v3.x runs as ESM and supports plugins.

## When to Use

- **Always**: Every project should have a formatter.
- **Collaborating**: Eliminates "nitpick" comments in PRs about whitespace.

## Core Concepts

### Opinionated

Few options. Print width, tab width, semi, quotes. That's it.

### Editor Integration

"Format on Save".

### Plugins

`prettier-plugin-tailwindcss` sorts classes automatically.

## Best Practices (2025)

**Do**:

- **Run in CI**: Ensure code is formatted before merge (`prettier --check .`).
- **Ignore generated files**: Add `.prettierignore`.

**Don't**:

- **Don't argue about style**: Just run Prettier.

## References

- [Prettier Documentation](https://prettier.io/)
