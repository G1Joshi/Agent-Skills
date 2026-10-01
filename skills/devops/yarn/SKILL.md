---
name: yarn
description: Expert Yarn package manager assistance covering Yarn Berry (v4+), Zero-Installs, PnP (Plug'n'Play), and workspaces. Use when managing fast, deterministic JavaScript monorepo dependencies.
---

# Yarn

Yarn (Berry) is a modern package manager. It introduced Plug'n'Play (PnP) to eliminate `node_modules` and support **Zero Installs**.

## When to Use

- **Modern JavaScript Package Management (Yarn v4+)**: Fast, reliable dependency management with Corepack support.
- **Plug'n'Play (PnP) & Zero-Installs**: Eliminating `node_modules` folders for instant workspace switching and CI runs.
- **Enterprise Monorepos**: Coordinated workspace resolution, constraints, and release workflows.
- **Hardened Security & Integrity**: Strict lockfile checksums and automated dependency audits.

## Quick Start

```bash
corepack enable
yarn set version stable
yarn init -2

# Install
yarn add react
```

## Core Concepts

### Modern Yarn Configuration (.yarnrc.yml)

Configuring node-modules linker or Plug'n'Play:

```yaml
# .yarnrc.yml
nodeLinker: node-modules # Use 'pnp' for Zero-Installs, 'node-modules' for standard compatibility
compressionLevel: mixed
enableGlobalCache: true

packageExtensions:
  "@types/react@*":
    peerDependencies:
      react: "*"
```

### Workspace Commands in Monorepos

Executing commands across workspaces:

```bash
# Run build command in parallel across all workspaces
yarn workspaces foreach --parallel --verbose run build

# Run tests only on workspaces changed relative to main branch
yarn workspaces foreach --since=main run test

# Add dependency to a specific workspace
yarn workspace @my-org/web-app add swr
```

### Upgrading Dependencies with Interactive CLI

Upgrading packages adhering to SemVer:

```bash
# Interactively review and upgrade outdated packages
yarn upgrade-interactive

# Re-validate lockfile integrity
yarn install --immutable
```

## Common Patterns

### Yarn Berry Monorepo Workspaces with TypeScript Loose Mode

**Problem**: Slow installs and node_modules bloat across multiple internal monorepo packages.

**Solution**:
Configure Yarn Berry workspaces with `.yarnrc.yml`:

```yaml
# .yarnrc.yml
nodeLinker: node-modules # Use node-modules linker for maximum ecosystem compatibility
yarnPath: .yarn/releases/yarn-4.5.0.cjs

packageExtensions:
  "react-scripts@*":
    dependencies:
      "typescript": "*"
```

Root `package.json`:

```json
{
  "private": true,
  "workspaces": ["apps/*", "packages/*"]
}
```

## Best Practices

**Do**:

- Target modern Yarn (v4+) enabled through Corepack (`corepack enable yarn`).
- Use `yarn install --immutable` in CI/CD pipelines to prevent unintended lockfile updates.
- Leverage `yarn workspaces foreach` with `--since=main` to test only modified packages in monorepos.
- Use `packageExtensions` in `.yarnrc.yml` to cleanly resolve missing peer dependency warnings from older third-party packages.

**Don't**:

- Use legacy Yarn 1.x (Classic); migrate to modern Yarn v4+ for enhanced performance and security.
- Edit `yarn.lock` manually; resolve conflicts via `yarn install`.
- Mix npm or pnpm lockfiles within a Yarn repository.

## Troubleshooting

| Error                                                    | Cause                                                            | Solution                                                                |
| :------------------------------------------------------- | :--------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `Usage Error: Couldn't find the node_modules state file` | Project running under PnP mode when tools expect `node_modules`. | Set `nodeLinker: node-modules` in `.yarnrc.yml` and run `yarn install`. |
| `YN0002: Missing peer dependency`                        | Package requires peer dependency not declared in consumer.       | Declare missing package in root `.yarnrc.yml` `packageExtensions`.      |
| `Yarn command not found`                                 | Yarn Berry binary missing in `.yarn/releases/`.                  | Run `corepack enable && corepack use yarn@stable`.                      |

## References

- [Yarn Documentation](https://yarnpkg.com/)
