---
name: delphi
description: Delphi Object Pascal for Windows applications. Use for .pas files.
---

# Delphi / Object Pascal

Delphi (RAD Studio) and Free Pascal (Lazarus) keep Object Pascal alive. It is famous for **Single EXE** deployment and instant compilation.

## When to Use

- **Windows Desktop Apps**: The VCL framework is still the fastest way to build native Windows GUIs.
- **Legacy Maintenance**: Massive industrial controllers in Europe use Delphi.
- **Cross-Platform**: FireMonkey (FMX) and Lazarus allow targeting Mac/Linux.

## Core Concepts

### VCL / LCL

Visual Component Library. Drag-and-drop UI building.

### Units

`interface`, `implementation` sections. Strict modularity.

### RTTI

Runtime Type Information (Reflection) was pioneered here.

## Best Practices (2025)

**Do**:

- **Use Generics**: `TList<T>` (modern Object Pascal).
- **Use `Lazarus`**: For open-source cross-platform development (Free Pascal 3.2+).
- **Manage Memory**: Use `try..finally` blocks for `Free`.

**Don't**:

- **Don't use `With`**: It makes scoping ambiguous.

## References

- [Free Pascal](https://www.freepascal.org/)
