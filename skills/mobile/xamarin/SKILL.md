---
name: xamarin
description: Xamarin cross-platform with .NET. Use for .NET mobile.
---

# Xamarin (Legacy)

**⚠️ STATUS: END OF LIFE (May 2024)**

Xamarin has officially reached End of Support. It was a cross-platform framework for building Android/iOS apps with .NET and C#. **All active development should move to .NET MAUI.**

## When to Use

- **DO NOT USE** for new projects.
- Only for maintaining legacy applications that have not yet been migrated to .NET MAUI.
- Reference for migration strategies.

## Migration to .NET MAUI

The primary "skill" for Xamarin developers in 2025 is **Migration**.

### High-Level Steps:

1.  **Analyze**: Use `.NET Upgrade Assistant`.
2.  **Project Structure**: Merge separate iOS/Android projects into the new Single Project structure (optional but recommended).
3.  **Namespace Updates**: `Xamarin.Forms` -> `Microsoft.Maui.Controls`.
4.  **Dependencies**: Replace Xamarin.Essentials with MAUI Essentials.
5.  **Renderers**: Convert Custom Renderers to **Handlers** (Mapped architecture).

## Core Concepts (Legacy)

### Xamarin.Forms

The UI abstraction layer sharing XAML code across platforms. Replaced by MAUI.

### Custom Renderers

The mechanism to customize native controls. Heavy and slow. Replaced by MAUI Handlers (interface-based).

### Xamarin.Native (Classic)

Writing UI in Storyboards (.xib) and Android XML but utilizing C# logic.

## Best Practices (Maintenance)

**Do**:

- **Plan your migration** immediately. Security patches are no longer guaranteed.
- Isolate platform-specific code to make migration to MAUI Handlers easier.

**Don't**:

- Don't start new features in Xamarin.Forms.
- Don't rely on unmaintained NuGet packages.

## Troubleshooting

| Error                        | Cause                            | Solution                                                               |
| :--------------------------- | :------------------------------- | :--------------------------------------------------------------------- |
| `NuGet Package Incompatible` | Package dropped Xamarin support. | Find MAUI equivalent or fork legacy version.                           |
| `Build Errors`               | Toolchain conflicts (VS 2022+).  | Ensure legacy workloads are installed (check Visual Studio Installer). |

## References

- [Xamarin Support Policy](https://dotnet.microsoft.com/platform/support/policy/xamarin)
- [Upgrade from Xamarin to .NET MAUI](https://learn.microsoft.com/en-us/dotnet/maui/migration)
