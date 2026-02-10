---
name: hexagonal
description: Hexagonal architecture ports and adapters. Use for testable systems.
---

# Hexagonal Architecture (Ports and Adapters)

Hexagonal Architecture aims to create a loosely coupled application component that can easily connect to their software environment by "ports" and "adapters". It treats the database, the web UI, and external APIs as interchangeable "details" (infrastructure).

## When to Use

- When you need to support multiple input channels (e.g., REST API, GraphQL, CLI, Message Queue) for the same business logic.
- When you want to be able to swap "driven" actors (e.g., verify logic with a Mock DB, then swap to Postgres).
- Developing standard microservices.

## Quick Start

```go
// --- CORE (Inside the Hexagon) ---

// Port (Driver Port - Input)
type UserService interface {
    Register(name string) error
}

// Port (Driven Port - Output)
type UserRepository interface {
    Save(user User) error
}

// Application Service (Implementation)
type UserServiceImpl struct {
    repo UserRepository
}

func (s *UserServiceImpl) Register(name string) error {
    return s.repo.Save(User{Name: name})
}

// --- ADAPTERS (Outside the Hexagon) ---

// Driving Adapter (REST API)
func HandleRegister(w http.ResponseWriter, r *http.Request, svc UserService) {
    svc.Register(r.FormValue("name"))
}

// Driven Adapter (Postgres)
type PostgresRepo struct { db *sql.DB }
func (r *PostgresRepo) Save(u User) error { ... }
```

## Core Concepts

### Ports

Interfaces that define the entry and exit points of the application.

- **Driving Ports (In)**: API surfaces (what the app _can do_).
- **Driven Ports (Out)**: Infrastructure dependencies (what the app _needs_).

### Adapters

Concrete implementations that bridge the gap between the Ports and the outside world.

- **Driving Adapters**: REST Controller, gRPC Handler, CLI Command.
- **Driven Adapters**: SQL Repository, SMTP Client, Redis Cache.

## Common Patterns

### Testing with Fake Adapters

Because the core depends on interfaces (Ports), you can implement "Fake" adapters (e.g., `InMemoryRepository`) to test complex business logic without spinning up Docker containers.

## Best Practices

**Do**:

- Keep the **Core** free of any framework dependencies (no HTTP, no SQL, no JSON tags).
- Define **Ports** in the Core, not in the adapters.
- Use **Hexagonal** for the domain layer of a microservice.

**Don't**:

- Don't leak implementation details (like `sql.Rows`) into the Core.
- Don't create an Adapter for every single class; focus on architectural boundaries.

## Troubleshooting

| Error        | Cause                                    | Solution                                                 |
| :----------- | :--------------------------------------- | :------------------------------------------------------- |
| `Leakage`    | Logic depends on specific library types. | Wrap external types in domain-specific DTOs/Interfaces.  |
| `Complexity` | Too many interfaces for simple logic.    | Start with a simple Service/Repository split and evolve. |

## References

- [Alistair Cockburn's Original Paper](https://alistair.cockburn.us/hexagonal-architecture/)
- [Hexagonal Architecture in Go](https://medium.com/@matiasvarela/hexagonal-architecture-in-go-cfd4e436bd57)
