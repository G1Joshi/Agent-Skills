---
name: swift
description: Swift development best practices including protocol-oriented programming, async/await concurrency, SwiftUI patterns, and testing. Use for .swift files.
---

# Swift

Modern Swift development with protocol-oriented programming and async/await.

## When to Use

- Working with `.swift` files
- Building iOS/macOS applications
- SwiftUI development
- Server-side Swift with Vapor

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

### Value Types & Structs

```swift
// Prefer structs for data
struct User: Identifiable, Codable, Hashable {
    let id: UUID
    var name: String
    var email: String
    var createdAt: Date = .now
}

// Enums with associated values
enum NetworkError: Error, LocalizedError {
    case invalidURL
    case noData
    case decodingError(Error)

    var errorDescription: String? {
        switch self {
        case .invalidURL: return "Invalid URL"
        case .noData: return "No data received"
        case .decodingError(let error): return "Decoding failed: \(error)"
        }
    }
}
```

### Protocol-Oriented Programming

```swift
protocol Repository {
    associatedtype Entity: Identifiable

    func findById(_ id: Entity.ID) async throws -> Entity?
    func save(_ entity: Entity) async throws -> Entity
    func delete(_ entity: Entity) async throws
}

extension Repository {
    func saveAll(_ entities: [Entity]) async throws -> [Entity] {
        try await withThrowingTaskGroup(of: Entity.self) { group in
            for entity in entities {
                group.addTask { try await self.save(entity) }
            }
            return try await group.reduce(into: []) { $0.append($1) }
        }
    }
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

## Best Practices

**Do**:

- Prefer value types (structs, enums) over classes
- Use protocol-oriented programming
- Handle optionals safely with `if let`, `guard`
- Use async/await for concurrency

**Don't**:

- Force unwrap with `!` except for IBOutlets
- Use implicitly unwrapped optionals unnecessarily
- Ignore error handling
- Create reference cycles without `weak`/`unowned`

## Troubleshooting

| Error                     | Cause                                | Solution             |
| ------------------------- | ------------------------------------ | -------------------- |
| `unexpectedly found nil`  | Force unwrap of nil                  | Use optional binding |
| `Actor-isolated property` | Accessing actor from sync context    | Use `await`          |
| `Sendable closure`        | Non-sendable type across concurrency | Make type Sendable   |

## References

- [Swift.org Documentation](https://swift.org/documentation/)
- [Hacking with Swift](https://www.hackingwithswift.com/)
