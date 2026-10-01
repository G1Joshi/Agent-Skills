---
name: pnpm
description: Expert pnpm fast, disk-efficient package manager assistance covering hard links, symlinks, pnpm-workspace.yaml, and monorepos. Use when managing JavaScript/TypeScript packages with speed and zero duplication.
---

# pnpm

pnpm is a fast, disk-efficient package manager for JavaScript that uses a content-addressable store and symlinked node_modules to eliminate duplicate dependencies across projects.

## When to Use

- **Fast, Disk-Efficient JavaScript Package Management**: Saving gigabytes of disk space via a content-addressable hard-link store.
- **Strict Dependency Resolution**: Eliminating phantom dependencies (preventing access to unlisted transitive packages).
- **Enterprise Monorepos**: Scaling multi-package workspaces with `pnpm-workspace.yaml` and fast parallel execution.
- **Continuous Integration Optimization**: Slashing CI installation times by up to 2x-3x through global store caching.

## Quick Start

```bash
# Enable via Corepack
corepack enable
corepack prepare pnpm@latest --activate

pnpm add next
```

## Core Concepts

### Configuring Monorepo Workspaces (pnpm-workspace.yaml)

Declaring workspace packages and root settings:

```yaml
# pnpm-workspace.yaml
packages:
  - "packages/*"
  - "apps/*"
  - "!**/test/**"
```

```json
// packages/core-service/package.json
{
  "name": "@my-org/core-service",
  "version": "1.0.0",
  "dependencies": {
    "@my-org/shared-utils": "workspace:*" // Symlinks to local workspace package
  }
}
```

### Workspace Commands & Parallel Script Execution

Running builds and tests across packages:

```bash
# Run tests in parallel across all workspace packages
pnpm --recursive run test

# Run build only for packages modified since main branch
pnpm --filter "...[origin/main]" run build

# Install a shared dependency to a specific package
pnpm --filter @my-org/web-app add lucide-react
```

### Hard Links and Content-Addressable Store

Inspecting and pruning global package deduplication:

```bash
# Verify integrity of global content-addressable store
pnpm store status

# Clean up unreferenced packages to free disk space
pnpm store prune
```

## Common Patterns

### Monorepo Workspaces with Shared Internal Packages

**Problem**: Inefficient symlinking and phantom dependency hoisting in large JavaScript monorepos.

**Solution**:
Define clean workspace structure in `pnpm-workspace.yaml`:

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

Consume internal package with `workspace:*` protocol:

```json
{
  "dependencies": {
    "@myorg/ui": "workspace:*",
    "@myorg/utils": "workspace:*"
  }
}
```

## Best Practices

**Do**:

- Use `pnpm install --frozen-lockfile` in CI/CD pipelines to guarantee reproducible installs.
- Use `workspace:*` protocols for internal dependencies to ensure local development links without publishing.
- Leverage `--filter` to run commands only on modified packages and their dependents.
- Manage pnpm versions via Corepack (`corepack enable pnpm`) to align team versions.

**Don't**:

- Access transitive packages not explicitly declared in `package.json`; pnpm's strict layout prevents this.
- Commit the global `.pnpm-store` to version control.
- Mix multiple package managers (npm, yarn) in the same project directory.

## Troubleshooting

| Error                                               | Cause                                                                              | Solution                                                               |
| :-------------------------------------------------- | :--------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `ERR_PNPM_PEER_DEP_ISSUES: Unmet peer dependencies` | Strict peer dependency resolution blocking install.                                | Configure `.npmrc` with `auto-install-peers=true` or resolve versions. |
| `Cannot find module ... (phantom dependency)`       | Package relies on a transitive dependency not explicitly declared in package.json. | Explicitly add the missing package to `package.json` dependencies.     |
| `pnpm-lock.yaml out of date`                        | Running `pnpm install --frozen-lockfile` after package.json was modified.          | Run `pnpm install` locally to update lockfile and commit changes.      |

## References

- [pnpm Documentation](https://pnpm.io/)
