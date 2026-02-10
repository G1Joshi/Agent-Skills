---
name: swiftui
description: SwiftUI declarative Apple UI framework. Use for iOS/macOS.
---

# SwiftUI

SwiftUI is Apple's declarative framework for building user interfaces across all Apple platforms (iOS, macOS, watchOS, tvOS, visionOS) with the power of Swift.

## When to Use

- Building modern iOS and macOS applications.
- Targeting multiple Apple platforms with shared UI code.
- Implementing complex animations and transitions with less code.
- Utilizing live previews for rapid UI iteration.

## Quick Start

```swift
import SwiftUI

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

// Observation Framework (iOS 17+)
@Observable
class UserSettings {
    var username = "Guest"
    var isLoggedIn = false
}

struct ContentView: View {
    @State private var settings = UserSettings()

    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                Text("Hello, \(settings.username)!")
                    .font(.largeTitle)

                Button("Log In") {
                    settings.username = "User"
                    settings.isLoggedIn = true
                }
                .buttonStyle(.borderedProminent)

                NavigationLink("Settings", value: "settings")
            }
            .navigationDestination(for: String.self) { path in
                if path == "settings" {
                    Text("Settings Page")
                }
            }
        }
    }
}
```

## Core Concepts

### Declarative Syntax

Instead of imperatively mutating UI views (like UIKit), you describe **what** the UI should look like for a given state. The system handles the updates.

### State & Data Flow (Modern)

- **@State**: Source of truth for simple, view-local value types.
- **@Binding**: Two-way connection to a value owned by another view.
- **@Observable**: (iOS 17+) Macro for creating observable reference types. Replaces `@StateObject` and `@ObservedObject` for cleaner data flow.

### Modifiers

Methods called on views that wrap the view and return a new view with the modification applied (e.g., `.padding()`, `.background()`). Order matters.

## Common Patterns

### NavigationStack (Path-based)

Replace `NavigationView` with `NavigationStack` for robust programmatic navigation.

- Use `.navigationDestination(for:)` to decouple navigation logic from views.
- Manage navigation state (`NavigationPath`) in a model for deep linking support.

### MVVM with Observation

Bind Views to ViewModels marked with `@Observable`. The View purely renders the state exposed by the ViewModel.

```swift
@Observable class ProfileViewModel {
    var profile: Profile?

    func loadProfile() async { /* ... */ }
}
```

## Best Practices

**Do**:

- Use **@Observable** for data models in iOS 17+ targets.
- Break down large views into smaller, reusable subviews (`Extract Subview`).
- Use **Previews** with different configurations (Dark Mode, Dynamic Type) to catch UI issues early.
- Use `Environment` for global dependencies (like themes or user session).

**Don't**:

- Don't perform heavy work in the `body` property (it's computed frequently).
- Don't use `AnyView` unless absolutely necessary (kills performance/diffing).
- Don't force imperative patterns (like trying to "refresh" a view manually); change the state instead.

## Troubleshooting

| Error                                             | Cause                                                         | Solution                                                     |
| :------------------------------------------------ | :------------------------------------------------------------ | :----------------------------------------------------------- |
| `Type '...' does not conform to protocol 'View'`  | The `body` property is missing or doesn't return `some View`. | Ensure `var body: some View` returns a valid view hierarchy. |
| `Modifying state during view update`              | Changing `@State` directly inside the `body` calculation.     | Move side effects to `.onAppear` or buttons/actions.         |
| `Trailing closure passed to parameter of type...` | Syntax error in view builder structure.                       | Check braces `{}` and modifier placement.                    |

## References

- [Apple SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)
- [WWDC23: Discover Observation](https://developer.apple.com/videos/play/wwdc2023/10149/)
- [Hacking with Swift - SwiftUI](https://www.hackingwithswift.com/quick-start/swiftui)
