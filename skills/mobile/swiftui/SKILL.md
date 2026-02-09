---
name: swiftui
description: SwiftUI declarative UI framework for Apple platforms. Use for iOS/macOS development.
---

# SwiftUI

Declarative UI framework for Apple platforms.

## When to Use

- iOS/iPadOS/macOS development
- Declarative UI patterns
- Cross-Apple platform apps
- Modern Swift development

## Quick Start

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {
            Text("Hello, SwiftUI!")
                .font(.largeTitle)
            Button("Tap me") {
                print("Tapped!")
            }
        }
    }
}
```

## Core Concepts

### State Management

```swift
struct Counter: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") {
                count += 1
            }
        }
    }
}

// Observable model (iOS 17+)
@Observable class UserModel {
    var name: String = ""
    var isLoggedIn: Bool = false
}

struct ProfileView: View {
    @Environment(UserModel.self) var user

    var body: some View {
        Text("Hello, \(user.name)")
    }
}
```

### Navigation

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        NavigationStack {
            List(users) { user in
                NavigationLink(value: user) {
                    Text(user.name)
                }
            }
            .navigationTitle("Users")
            .navigationDestination(for: User.self) { user in
                UserDetailView(user: user)
            }
        }
    }
}
```

## Common Patterns

### Lists & Data

```swift
struct UserList: View {
    let users: [User]

    var body: some View {
        List(users) { user in
            HStack {
                AsyncImage(url: user.avatarURL) { image in
                    image.resizable().frame(width: 40, height: 40)
                } placeholder: {
                    ProgressView()
                }
                VStack(alignment: .leading) {
                    Text(user.name).font(.headline)
                    Text(user.email).font(.caption)
                }
            }
        }
    }
}
```

### Async Data

```swift
struct UserView: View {
    let userId: String
    @State private var user: User?
    @State private var isLoading = true

    var body: some View {
        Group {
            if isLoading {
                ProgressView()
            } else if let user {
                UserCard(user: user)
            }
        }
        .task {
            user = try? await fetchUser(id: userId)
            isLoading = false
        }
    }
}
```

## Best Practices

**Do**:

- Use @Observable for models (iOS 17+)
- Prefer small, composable views
- Use environment for dependency injection
- Test with PreviewProvider

**Don't**:

- Put complex logic in views
- Use force unwrapping
- Ignore accessibility
- Skip dark mode support

## Troubleshooting

| Issue             | Cause        | Solution                |
| ----------------- | ------------ | ----------------------- |
| View not updating | State issue  | Check property wrappers |
| Preview crash     | Missing data | Add mock data           |
| Navigation broken | Stack issue  | Check NavigationStack   |

## References

- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)
- [Hacking with Swift](https://www.hackingwithswift.com/quick-start/swiftui)
