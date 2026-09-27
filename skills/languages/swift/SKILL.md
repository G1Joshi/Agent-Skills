---
name: swift
description: Expert Swift assistance covering Swift 6 strict concurrency, async/await, actors, protocols, generics, memory management with ARC, and SwiftUI integration. Use when writing iOS/macOS applications, debugging concurrency warnings, or building robust Swift codebases.
---

# Swift

Modern Swift development with protocol-oriented programming and async/await.

## When to Use

- **Apple Ecosystem Native Applications**: iOS, iPadOS, macOS, watchOS, and visionOS applications using SwiftUI.
- **Modern Concurrent Systems**: Utilizing Swift 6 complete concurrency checking, actors, and structured `Task` trees.
- **Cross-Platform Server-Side Swift**: High-performance backends and microservices built with Hummingbird or Vapor.
- **Embedded & Real-Time Edge Processing**: Utilizing Embedded Swift for microcontrollers and real-time audio engines.

## Quick Start

```swift
struct User: Identifiable, Codable {
    let id: UUID
    var name: String
    var email: String

    var displayName: String {
        name.capitalized
    }
}
```

## Core Concepts

#Modern Swift 6 Concurrency: Actors & Structured Tasks

Data-race safety guaranteed at compile time with Sendable enforcement and actors:

```swift
import Foundation

// Thread-safe state isolation via actor
actor AccountManager {
    private var balances: [UUID: Decimal] = [:]

    func deposit(to accountId: UUID, amount: Decimal) {
        guard amount > 0 else { return }
        balances[accountId, default: 0] += amount
    }

    func balance(for accountId: UUID) -> Decimal {
        balances[accountId, default: 0]
    }
}

// Structured concurrency with TaskGroup
func fetchUserMetrics(userIds: [UUID]) async throws -> [UUID: Decimal] {
    let manager = AccountManager()

    return try await withThrowingTaskGroup(of: (UUID, Decimal).self) { group in
        for id in userIds {
            group.addTask {
                let bal = await manager.balance(for: id)
                return (id, bal)
            }
        }

        var results: [UUID: Decimal] = [:]
        for try await (id, bal) in group {
            results[id] = bal
        }
        return results
    }
}
```

#Protocol-Oriented Architecture & Primary Associated Types

Expressive type contracts using Swift 5.7+ `some` and `any` semantics:

```swift
// Protocol with primary associated type
protocol Repository<Entity>: Sendable {
    associatedtype Entity: Identifiable, Sendable
    func fetch(by id: Entity.ID) async throws -> Entity?
    func save(_ entity: Entity) async throws
}

struct User: Identifiable, Sendable {
    let id: UUID
    let name: String
}

final class InMemoryUserRepository: Repository {
    private var store: [UUID: User] = [:]

    func fetch(by id: UUID) async throws -> User? {
        store[id]
    }

    func save(_ entity: User) async throws {
        store[entity.id] = entity
    }
}

// Opaque return type using 'some' for static dispatch performance
func makeDefaultRepo() -> some Repository<User> {
    InMemoryUserRepository()
}
```

#Result Builders & Custom DSLs

Constructing declarative hierarchies modeled after SwiftUI:

```swift
@resultBuilder
struct HTMLBuilder {
    static func buildBlock(_ components: String...) -> String {
        components.joined(separator: "
")
    }

    static func buildOptional(_ component: String?) -> String {
        component ?? ""
    }
}

func htmlDoc(@HTMLBuilder content: () -> String) -> String {
    "<html>
<body>
\(content())
</body>
</html>"
}

let page = htmlDoc {
    "<h1>Welcome to Swift 6</h1>"
    "<p>Safe, fast, and expressive systems programming.</p>"
}
```

## Common Patterns

### Async/Await

```swift
func fetchUser(id: UUID) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, response) = try await URLSession.shared.data(from: url)

    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw NetworkError.invalidResponse
    }

    return try JSONDecoder().decode(User.self, from: data)
}

// Parallel execution
async let user = fetchUser(id: userId)
async let orders = fetchOrders(userId: userId)
let (userResult, ordersResult) = try await (user, orders)
```

### Actors

```swift
actor UserCache {
    private var cache: [UUID: User] = [:]

    func get(_ id: UUID) -> User? { cache[id] }
    func set(_ user: User) { cache[user.id] = user }
}
```

## Best Practices (2026)

- **Do** enable Swift 6 complete concurrency checking (`-strict-concurrency=complete`) to catch data races at compile time.
- **Do** prefer `struct` and value types over `class` unless reference identity or Objective-C runtime bridging is explicitly required.
- **Do** favor `some Protocol` (opaque types) over `any Protocol` (existential types) to eliminate dynamic dispatch overhead.
- **Do** use `async/await` and structured `withTaskGroup` rather than legacy completion handlers and Grand Central Dispatch (`DispatchQueue`).
- **Don't** force unwrap optionals (`!`) in production; use `guard let`, `if let`, or default coalescing (`??`).
- **Don't** capture strong `self` references in escaping closures; use `[weak self]` to avoid retain cycles.
- **Don't** bypass actor isolation with `@unchecked Sendable` without verifying thread-safety invariants.

## Troubleshooting

| Error                     | Cause                                | Solution             |
| ------------------------- | ------------------------------------ | -------------------- |
| `unexpectedly found nil`  | Force unwrap of nil                  | Use optional binding |
| `Actor-isolated property` | Accessing actor from sync context    | Use `await`          |
| `Sendable closure`        | Non-sendable type across concurrency | Make type Sendable   |

## References

- [Swift.org Documentation](https://swift.org/documentation/)
- [Hacking with Swift](https://www.hackingwithswift.com/)
