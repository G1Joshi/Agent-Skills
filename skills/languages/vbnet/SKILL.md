---
name: vbnet
description: Visual Basic .NET for legacy .NET applications. Use for .vb files.
---

# VB.NET

VB.NET is a first-class citizen on .NET, sharing the same runtime/libraries as C#. While C# gets new syntax first, VB.NET remains supported in .NET 8+.

## When to Use

- **Legacy Migration**: Porting VB6 apps to .NET.
- **Readability**: Specific industries prefer the verbose, English-like syntax (`End If`).
- **Office Automation**: Integration with massive Excel/Access logic.

## Core Concepts

### Case Insensitivity

`Dim X` and `dim x` are the same.

### Modules

Equivalent to static classes.

### My Namespace

`My.Computer`, `My.User`. Shortcuts for common tasks.

## Best Practices (2025)

**Do**:

- **Use `Option Strict On`**: Disables implicit casting (critical for bugs).
- **Target .NET 8**: Move away from .NET Framework 4.8.
- **Use String Interpolation**: `$"Hello {Name}"`.

**Don't**:

- **Don't use `On Error Resume Next`**: Use structured `Try...Catch`.

## References

- [Microsoft VB.NET Guide](https://learn.microsoft.com/en-us/dotnet/visual-basic/)
