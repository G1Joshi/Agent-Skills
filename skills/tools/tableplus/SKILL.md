---
name: tableplus
description: TablePlus modern database GUI. Use for database management.
---

# TablePlus

TablePlus is a native app (Swift on Mac, C# on Windows) known for being incredibly **fast** and **lightweight**.

## When to Use

- **MacOS / Windows**: Native experience (not Electron).
- **Speed**: Starts instantly.
- **Security**: Built-in SSH tunneling and TLLS.

## Core Concepts

### Workspaces

Tabs, separate windows, inline editing.

### Safe Mode

Requires password/confirmation to run destructive queries (`DELETE`, `UPDATE`) in Production.

### Plugin System

Extend functionality with JavaScript plugins.

## Best Practices (2025)

**Do**:

- **Use Safe Mode**: Always enable it for production connections.
- **Use Multiple Tabs**: Cmd+T to open new query tabs.
- **Use "Open Anything"**: Cmd+P to jump to tables.

**Don't**:

- **Don't use for Oracle**: Support is there but DBeaver is better for legacy DBs. TablePlus shines on Postgres/MySQL.

## References

- [TablePlus Documentation](https://tableplus.com/)
