---
name: ios-sdk
description: iOS SDK for native iOS development with Foundation and UIKit. Use for native iOS.
---

# iOS SDK

Native iOS development with Swift and Apple frameworks.

## When to Use

- Native iOS apps
- System integrations
- Apple platform features
- Performance-critical apps

## Quick Start

```swift
import UIKit

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        return true
    }
}
```

## Core Concepts

### App Lifecycle

```swift
class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?

    func scene(
        _ scene: UIScene,
        willConnectTo session: UISceneSession,
        options connectionOptions: UIScene.ConnectionOptions
    ) {
        guard let windowScene = scene as? UIWindowScene else { return }
        window = UIWindow(windowScene: windowScene)
        window?.rootViewController = MainViewController()
        window?.makeKeyAndVisible()
    }

    func sceneDidEnterBackground(_ scene: UIScene) {
        // Save state
    }
}
```

### Networking

```swift
func fetchUser(id: String) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, response) = try await URLSession.shared.data(from: url)

    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw NetworkError.invalidResponse
    }

    return try JSONDecoder().decode(User.self, from: data)
}
```

## Common Patterns

### UserDefaults

```swift
extension UserDefaults {
    enum Key: String {
        case isOnboarded
        case authToken
    }

    var isOnboarded: Bool {
        get { bool(forKey: Key.isOnboarded.rawValue) }
        set { set(newValue, forKey: Key.isOnboarded.rawValue) }
    }
}
```

### Push Notifications

```swift
func registerForPushNotifications() {
    UNUserNotificationCenter.current().requestAuthorization(
        options: [.alert, .badge, .sound]
    ) { granted, _ in
        guard granted else { return }
        DispatchQueue.main.async {
            UIApplication.shared.registerForRemoteNotifications()
        }
    }
}

func application(
    _ application: UIApplication,
    didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data
) {
    let token = deviceToken.map { String(format: "%02.2hhx", $0) }.joined()
    // Send token to server
}
```

## Best Practices

**Do**:

- Use async/await for networking
- Respect user privacy
- Support accessibility
- Handle edge cases

**Don't**:

- Block main thread
- Force unwrap optionals
- Ignore error handling
- Skip device testing

## Troubleshooting

| Issue           | Cause               | Solution            |
| --------------- | ------------------- | ------------------- |
| UI freeze       | Main thread blocked | Use async           |
| Memory warning  | Leaks               | Use Instruments     |
| Crash on launch | Missing permissions | Add Info.plist keys |

## References

- [Apple Developer Docs](https://developer.apple.com/documentation/)
- [App Store Guidelines](https://developer.apple.com/app-store/review/guidelines/)
