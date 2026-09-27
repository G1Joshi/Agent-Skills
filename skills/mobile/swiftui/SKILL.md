---
name: swiftui
description: Expert SwiftUI assistance covering declarative iOS/macOS layouts, @Observable / ObservableObject state propagation, view modifiers, custom animations, and NavigationStack. Use when creating modern Apple platform user interfaces, widgets, and multi-platform apps.
---

# SwiftUI

SwiftUI is Apple's declarative framework for building user interfaces across all Apple platforms (iOS, macOS, watchOS, tvOS, visionOS) with the power of Swift.

## When to Use

- **Modern Apple Platform Apps**: Building user interfaces for iOS, iPadOS, macOS, watchOS, and visionOS from a unified declarative syntax.
- **State-Driven Interactive Interfaces**: Creating fluid, animated user experiences using `@Observable`, Swift 6 concurrency, and `@State`.
- **Dynamic Layout Adaptability**: Designing views that adapt smoothly to Dynamic Type, Dark Mode, and diverse Apple device form factors.
- **Interactive Widgets & Live Activities**: Implementing Lock Screen widgets, Home Screen widgets, and Dynamic Island activities.

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

#Modern `@Observable` Architecture (iOS 17+)

Replaces legacy `ObservableObject` and `@Published` with compiler-macro observations, tracking only properties actually read in the view:

```swift
import SwiftUI
import Observation

@Observable
final class WalletViewModel {
    var balance: Double = 1420.50
    var isRefreshing: Bool = false

    func loadBalance() async {
        isRefreshing = true
        defer { isRefreshing = false }
        // Async network fetch
        try? await Task.sleep(nanoseconds: 500_000_000)
        balance += 50.0
    }
}

struct WalletView: View {
    @State private var viewModel = WalletViewModel()

    var body: some View {
        VStack(spacing: 12) {
            Text("Available Balance")
                .font(.subheadline)
                .foregroundStyle(.secondary)
            Text(viewModel.balance, format: .currency(code: "USD"))
                .font(.system(size: 34, weight: .bold))
            Button("Add Funds") {
                Task { await viewModel.loadBalance() }
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
```

#Declarative View Modifiers & Composition

Modifiers return new view structures, composing functionality through ordered transformations:

```swift
struct PrimaryButtonModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .font(.headline)
            .foregroundStyle(.white)
            .frame(maxWidth: .infinity)
            .padding()
            .background(Color.indigo, in: RoundedRectangle(cornerRadius: 14))
            .shadow(color: .indigo.opacity(0.3), radius: 8, y: 4)
    }
}

extension View {
    func primaryButtonStyle() -> some View {
        modifier(PrimaryButtonModifier())
    }
}
```

#NavigationStack & Value-Based Routing

Modern type-safe navigation using `NavigationStack` and `navigationDestination`:

```swift
enum AppRoute: Hashable {
    case orderDetail(id: String)
    case settings
}

struct MainCoordinator: View {
    @State private var path: [AppRoute] = []

    var body: some View {
        NavigationStack(path: $path) {
            List {
                Button("View Order #415") { path.append(.orderDetail(id: "415")) }
            }
            .navigationDestination(for: AppRoute.self) { route in
                switch route {
                case .orderDetail(let id): Text("Order Detail: \(id)")
                case .settings: Text("App Settings")
                }
            }
        }
    }
}
```

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

## Best Practices (2026)

**Do**:

- **Adopt Swift 6 Strict Concurrency**: Ensure all view models and background tasks conform to `@MainActor` and Sendable protocols.
- **Decompose Large Views into Subviews**: Break body properties into discrete subviews to allow SwiftUI to localize re-evaluations.
- **Leverage Standard Semantic Colors**: Use `.foregroundStyle(.primary)` and `.background(.background)` to support Light and Dark modes automatically.
- **Provide View Previews with Static Mock Data**: Utilize `#Preview` macro with sample models for instant canvas rendering.

**Don't**:

- **Don't store non-transient state in `@State`**: `@State` is for view-owned local state; domain business models belong in observable ViewModels.
- **Don't block the main actor with heavy computations**: Move image processing and JSON decoding to non-isolated background actor tasks.
- **Don't overuse `AnyView`**: Type-erasure prevents SwiftUI from performing structural diffing optimizations; use `@ViewBuilder` instead.

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
