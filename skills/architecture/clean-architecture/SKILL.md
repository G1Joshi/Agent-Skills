---
name: clean-architecture
description: Clean Architecture layered design. Use for maintainable code.
---

# Clean Architecture

Clean Architecture, popularized by Robert C. Martin (Uncle Bob), separates software into layers to ensure independence from frameworks, databases, and UIs. The core principle is the **Dependency Rule**: source code dependencies can only point inwards.

## When to Use

- Building enterprise applications with complex business logic.
- Long-lived projects where frameworks/databases might change over time.
- Large teams requiring clear separation of concerns to work in parallel.

## Quick Start

```typescript
// 1. Entity (Enterprise Logic) - Inner Layer
class User {
  constructor(
    public id: string,
    public name: string,
  ) {
    if (name.length < 2) throw new Error("Name too short");
  }
}

// 2. Use Case (Application Logic)
class CreateUserUseCase {
  constructor(private userRepository: UserRepository) {} // Depends on interface

  async execute(name: string): Promise<User> {
    const user = new User(crypto.randomUUID(), name);
    await this.userRepository.save(user);
    return user;
  }
}

// 3. Interface Adapter (Repository Interface)
interface UserRepository {
  save(user: User): Promise<void>;
}

// 4. Frameworks & Drivers (Implementation) - Outer Layer
class SqlUserRepository implements UserRepository {
  async save(user: User): Promise<void> {
    await db.query("INSERT INTO users ...", [user.id, user.name]);
  }
}
```

## Core Concepts

### The Dependency Rule

Inner layers (Entities) know nothing about outer layers (Controllers, Presenters). Outer layers depend on inner layers.

### Entities

Enterprise-wide business rules. These are the least likely to change when something external changes (e.g., page navigation security).

### Application Business Rules (Use Cases)

Orchestrate the flow of data to and from the entities. They contain the specific business rules of the application (e.g., "Create Order").

## Common Patterns

### Dependency Injection

The glue that makes Clean Architecture possible. Outer layers inject concrete implementations (e.g., `SqlUserRepository`) into inner layers (which expect `UserRepository` interface).

### DTOs (Data Transfer Objects)

Use simple objects (DTOs) to cross boundaries. Do not pass Entities to the UI or Database rows to the Use Case.

## Best Practices

**Do**:

- Define **Interfaces** in the layer that uses them (Interface Segregation).
- Test **Use Cases** in isolation using mocks for repositories.
- Keep **Frameworks** (React, NestJS, Spring) at the outermost layer.

**Don't**:

- Don't let **database entities** (ORM models) leak into the inner layers. Map them to domain Entities.
- Don't skip layers "for speed" (e.g., Controller calling DB directly) in complex apps.

## Troubleshooting

| Error                  | Cause                                   | Solution                                                                        |
| :--------------------- | :-------------------------------------- | :------------------------------------------------------------------------------ |
| `Circular Dependency`  | Violating the dependency rule.          | Use Dependency Inversion (Interfaces) to break the cycle.                       |
| `Boilerplate Overload` | Creating strict layers for simple CRUD. | Consider "Vertical Slice Architecture" or Modular Monolith for simpler domains. |

## References

- [The Clean Architecture Blog](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Clean Architecture vs. Hexagonal](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/)
