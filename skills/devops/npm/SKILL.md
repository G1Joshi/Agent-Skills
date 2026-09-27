---
name: npm
description: Expert npm package manager assistance covering package.json, lockfiles, workspaces (monorepos), scripts, and security audits. Use when managing JavaScript/Node.js dependencies and publishing packages.
---

# npm

npm is the default package manager for Node.js. v11 (2025) introduces strict publishing rules and `npx` caching improvements.

## When to Use

- **JavaScript / TypeScript Package Management**: Installing, publishing, and managing npm modules and dependencies.
- **Multi-Package Monorepos (npm Workspaces)**: Coordinating interconnected local packages with unified dependency resolution.
- **Supply Chain Security & Provenance**: Publishing packages with cryptographically verifiable build provenance.
- **Vulnerability Auditing & Dependency Overrides**: Resolving transitively vulnerable packages using `overrides`.

## Quick Start

```bash
npm init -y
npm install lodash
npm install --save-dev jest

# Monorepo
npm init -w packages/my-lib
```

## Core Concepts

#Configuring npm Workspaces in Monorepos

Declaring multi-package structures in root `package.json`:

```json
{
  "name": "enterprise-monorepo",
  "private": true,
  "workspaces": ["packages/*", "apps/*"],
  "scripts": {
    "build": "npm run build --workspaces --if-present",
    "test": "npm test --workspaces --if-present"
  },
  "overrides": {
    "glob": "^10.4.0",
    "semver": "^7.6.0"
  }
}
```

#Clean Installations & Deterministic Lockfiles

Installing dependencies in continuous integration:

```bash
# Clean install adhering strictly to package-lock.json (never mutates lockfile)
npm ci

# Audit dependencies for known CVEs
npm audit --audit-level=high

# Run targeted script across all workspaces
npm run test --workspace=packages/core-utils
```

#Publishing Packages with Cryptographic Provenance

Publishing to the npm registry with supply-chain verification:

```bash
# Publish package with Sigstore verifiable provenance
npm publish --access public --provenance
```

## Common Patterns

### Monorepo Workspaces Configuration

**Problem**: Managing shared libraries across multiple internal packages without publishing to external registries.

**Solution**:
Use native npm workspaces in root `package.json`:

```json
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": ["packages/*", "apps/*"],
  "scripts": {
    "build": "npm run build --workspaces --if-present",
    "test": "npm test --workspaces"
  }
}
```

## Best Practices (2026)

- **Do** always use `npm ci` in CI/CD pipelines instead of `npm install` to enforce exact lockfile dependencies.
- **Do** publish public packages with `--provenance` to establish cryptographic build transparency.
- **Do** use `overrides` in root `package.json` to resolve security vulnerabilities in deep transitive dependencies.
- **Do** commit `package-lock.json` to version control in all projects.
- **Don't** use `npm install --force` or `--legacy-peer-deps` in production builds; resolve peer version conflicts cleanly.
- **Don't** publish packages containing sensitive files; maintain an explicit `.npmignore` or `"files"` whitelist.
- **Don't** execute untrusted scripts during install without verifying packages (`npm install --ignore-scripts`).

## Troubleshooting

| Error                                                  | Cause                                                                    | Solution                                                                    |
| :----------------------------------------------------- | :----------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `npm ERR! code ERESOLVE: could not resolve dependency` | Peer dependency version conflict.                                        | Run `npm install --legacy-peer-deps` or align conflicting package versions. |
| `npm ERR! code EACCES: permission denied`              | Installing global packages without permissions on system node directory. | Configure user npm prefix: `npm config set prefix ~/.npm-global`.           |
| `package-lock.json out of sync`                        | Dependencies installed with different npm major versions.                | Delete `node_modules` and run `npm ci` for strict deterministic installs.   |

## References

- [npm Documentation](https://docs.npmjs.com/)
