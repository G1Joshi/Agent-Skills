---
name: xamarin
description: Expert Xamarin assistance covering Xamarin.Forms cross-platform UI, .NET MAUI migration, XAML data binding, custom renderers, and platform dependency services. Use when maintaining Xamarin applications, migrating to .NET MAUI, or sharing C# code across mobile platforms.
---

# Xamarin (Legacy)

**⚠️ STATUS: LEGACY (MIGRATION TO .NET MAUI REQUIRED)**

Xamarin has reached official end-of-life status. Legacy Xamarin.Forms and native Xamarin codebases should be migrated to modern .NET MAUI.

Xamarin has officially reached End of Support. It was a cross-platform framework for building Android/iOS apps with .NET and C#. **All active development should move to .NET MAUI.**

## When to Use

- **Enterprise .NET Mobile Maintenance**: Maintaining existing enterprise Xamarin.Forms and Xamarin.iOS/Android applications.
- **Migration to .NET MAUI**: Planning and executing migrations from legacy Xamarin.Forms to modern unified .NET MAUI.
- **Shared C# Business Libraries**: Sharing .NET Core business logic, Entity Framework SQLite layers, and services across mobile.
- **XAML Declarative Mobile UI**: Building cross-platform user interfaces using XAML data binding and MVVM architectures.

## Quick Start

```bash
# Install the official .NET upgrade assistant tool
dotnet tool install -g upgrade-assistant

# Run upgrade analysis on the legacy Xamarin.Forms project or solution
upgrade-assistant analyze ./MyXamarinApp.sln

# Automatically apply project and namespace migrations to .NET MAUI
upgrade-assistant upgrade ./MyXamarinApp.sln --non-interactive
```

## Core Concepts

### XAML Data Binding & MVVM (Model-View-ViewModel)

Two-way data binding synchronizes native mobile controls with observable ViewModels:

```csharp
// ViewModels/ProfileViewModel.cs
using System.ComponentModel;
using System.Runtime.CompilerServices;

public class ProfileViewModel : INotifyPropertyChanged
{
    private string _username = "JaneDoe";
    public string Username
    {
        get => _username;
        set { _username = value; OnPropertyChanged(); }
    }

    public event PropertyChangedEventHandler PropertyChanged;
    protected void OnPropertyChanged([CallerMemberName] string name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}
```

```xml
<!-- Views/ProfilePage.xaml -->
<ContentPage xmlns="http://xamarin.com/schemas/2014/forms"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:vm="clr-namespace:MyApp.ViewModels"
             x:Class="MyApp.Views.ProfilePage">
    <ContentPage.BindingContext>
        <vm:ProfileViewModel />
    </ContentPage.BindingContext>
    <StackLayout Padding="20">
        <Entry Text="{Binding Username, Mode=TwoWay}" />
        <Label Text="{Binding Username, StringFormat='Active User: {0}'}" FontSize="18" />
    </StackLayout>
</ContentPage>
```

### DependencyService Platform Abstraction

Resolves platform-specific native implementations from shared code:

```csharp
// Shared Interface
public interface IDeviceStorage { string GetStorageDirectory(); }

// Android Implementation: [assembly: Dependency(typeof(AndroidStorage))]
public class AndroidStorage : IDeviceStorage
{
    public string GetStorageDirectory() => Android.App.Application.Context.FilesDir.AbsolutePath;
}

// Consumed in Shared ViewModel
var path = DependencyService.Get<IDeviceStorage>().GetStorageDirectory();
```

### Transition to .NET MAUI Architecture

Modernizes Xamarin codebases by unifying project structures into a single multi-targeted `.csproj`:

```xml
<!-- .NET MAUI Single Project Structure -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFrameworks>net8.0-android;net8.0-ios</TargetFrameworks>
    <UseMaui>true</UseMaui>
    <SingleProject>true</SingleProject>
  </PropertyGroup>
</Project>
```

### Migration to .NET MAUI Architecture

The primary focus for legacy Xamarin codebases is structured migration to modern .NET MAUI:

1. **Analyze Dependencies**: Run the `.NET Upgrade Assistant` to identify breaking APIs and obsolete NuGet packages.
2. **Consolidate Project Structure**: Merge separate iOS/Android head projects into a unified Single Project (`.csproj`) layout.
3. **Update Namespaces**: Migrate legacy `Xamarin.Forms` namespaces to `Microsoft.Maui.Controls`.
4. **Replace Framework APIs**: Replace legacy `Xamarin.Essentials` with unified `Microsoft.Maui.Devices` APIs.
5. **Convert Custom Renderers**: Migrate platform renderers to modern decoupled **Handlers** via mapped property mappers.

## Common Patterns

### XAML Namespace Modernization

**Problem**: Legacy Xamarin.Forms XAML namespaces cause build failures in modern .NET toolchains.

**Solution**:
Update the XML root declarations to .NET MAUI standard schemas:

```xml
<!-- Legacy Xamarin.Forms -->
<ContentPage xmlns="http://xamarin.com/schemas/2014/forms"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="MyApp.MainPage">
</ContentPage>

<!-- Upgraded .NET MAUI -->
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="MyApp.MainPage">
</ContentPage>
```

## Best Practices

**Do**:

- Migrate to .NET MAUI: Transition active projects to .NET 8/9 MAUI; Xamarin reached official end-of-support.
- Use CommunityToolkit.Mvvm: Replace repetitive `INotifyPropertyChanged` boilerplate with source-generator `[ObservableProperty]` and `[RelayCommand]`.
- Compile XAML with `[XamlCompilation(XamlCompilationOptions.Compile)]`: Enable XAMLC to catch XAML binding errors at build time.
- Use WeakReferenceMessenger: Decouple inter-view communications without leaking View references in event handlers.

**Don't**:

- Start greenfield apps on Xamarin: New .NET mobile applications should start directly on .NET MAUI.
- Write heavy custom renderers: Use lightweight Handlers (.NET MAUI style) rather than heavy legacy Xamarin Custom Renderers.
- Ignore Linker settings: Test release builds with Linker enabled (`Link SDK assemblies only`) to keep binary sizes compact.

## Troubleshooting

| Error                        | Cause                            | Solution                                                               |
| :--------------------------- | :------------------------------- | :--------------------------------------------------------------------- |
| `NuGet Package Incompatible` | Package dropped Xamarin support. | Find MAUI equivalent or fork legacy version.                           |
| `Build Errors`               | Toolchain conflicts (VS 2022+).  | Ensure legacy workloads are installed (check Visual Studio Installer). |

## References

- [Xamarin Support Policy](https://dotnet.microsoft.com/platform/support/policy/xamarin)
- [Upgrade from Xamarin to .NET MAUI](https://learn.microsoft.com/en-us/dotnet/maui/migration)
