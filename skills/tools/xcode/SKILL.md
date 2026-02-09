---
name: xcode
description: Xcode IDE for iOS/macOS development with SwiftUI and testing. Use for Apple platform development.
---

# Xcode

IDE for developing apps for Apple platforms.

## When to Use

- iOS/iPadOS app development
- macOS app development
- watchOS/tvOS development
- Swift Package development

## Quick Start

```swift
// App.swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

// ContentView.swift
struct ContentView: View {
    var body: some View {
        Text("Hello, World!")
    }
}
```

## Core Concepts

### Project Configuration

```swift
// Build Settings
// - Deployment Target: iOS 17.0
// - Swift Language Version: 6.0
// - Build Configuration: Debug/Release

// Info.plist keys
/*
<key>CFBundleDisplayName</key>
<string>My App</string>
<key>NSCameraUsageDescription</key>
<string>Camera access needed for photos</string>
*/
```

### Debugging

```swift
// LLDB commands
// po variableName
// expr variableName = newValue
// bt (backtrace)

// Breakpoint actions
// Log message: "Value: @value@"
// Shell command: say "breakpoint hit"

// View debugging
// Debug > View Debugging > Capture View Hierarchy
```

## Common Patterns

### Schemes & Configurations

```
Project Settings:
├── Configurations
│   ├── Debug
│   ├── Release
│   └── Staging (custom)
└── Schemes
    ├── MyApp (Debug)
    ├── MyApp (Release)
    └── MyApp (Staging)
```

### Code Signing

```bash
# Automatic signing
# - Team: Select your team
# - Automatically manage signing: ON

# Manual signing (CI)
# - Provisioning Profile: Select manually
# - Signing Certificate: Select manually

# Build from command line
xcodebuild -project MyApp.xcodeproj \
  -scheme MyApp \
  -configuration Release \
  -archivePath build/MyApp.xcarchive \
  archive
```

## Best Practices

**Do**:

- Use SwiftUI previews
- Enable strict concurrency checking
- Configure proper entitlements
- Use Instruments for profiling

**Don't**:

- Commit derived data
- Ignore deprecation warnings
- Skip accessibility testing
- Use force unwrapping

## Troubleshooting

| Issue          | Cause               | Solution                  |
| -------------- | ------------------- | ------------------------- |
| Signing error  | Certificate expired | Renew in developer portal |
| Preview crash  | Build error         | Check Preview canvas logs |
| Simulator slow | Resource constraint | Reset simulator           |

## References

- [Apple Developer Docs](https://developer.apple.com/documentation/)
- [Xcode Help](https://help.apple.com/xcode/)
