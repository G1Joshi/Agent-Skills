---
name: planetscale
description: PlanetScale serverless MySQL with branching. Use for scalable MySQL.
---

# PlanetScale

PlanetScale is a serverless database platform compatible with MySQL. It is built on **Vitess**, the technology used by YouTube/Slack to scale massively.

## When to Use

- **High Traffic MySQL**: When you need "sharding" but don't want to build it yourself.
- **Schema Management**: excellent "Branching" workflow (Development -> Staging -> Production) without downtime (Online DDL).
- **Connections**: Handles 100,000s of concurrent connections (Vitess architecture).

## Quick Start

Uses standard MySQL drivers.

```bash
# Connect via CLI
pscale shell my-database main
```

## Core Concepts

### Branching

Treat your database schema like Git code.

1. Create a `dev` branch from `main`.
2. Apply migrations to `dev`.
3. Open a "Deploy Request" to merge `dev` to `main`.
4. PlanetScale runs the schema change online without locking tables.

### Vitess

Abstracts the sharding. Your app sees one big DB, but behind scenes it might be 100 shards.

### Non-Blocking Schema Changes

Ghost/PT-OSC style schema changes standard. You never lock the table for "ALTER TABLE".

## Best Practices (2025)

**Do**:

- **Use Foreign Keys carefully**: PlanetScale supports them now (mostly), but conceptually in sharded systems, application-level joins are often safer/faster.
- **Use `pscale` CLI**: Great developer experience for managing branches.
- **Safe Migrations**: Use the Branching workflow. Never run `ALTER TABLE` directly on production `main` branch.

**Don't**:

- **Don't use stored procedures/triggers**: Vitess generally discourages logic in the DB. Move logic to app.

## References

- [PlanetScale Documentation](https://planetscale.com/docs)
