---
name: clean-architecture
description: Expert Clean Architecture assistance covering Onion/Hexagonal layered boundaries, dependency inversion, use case interactors, entities, and repository interfaces. Use when designing maintainable software architectures, decoupling business logic from frameworks, or structuring testable domain models.
---

# Clean Architecture

Clean Architecture, popularized by Robert C. Martin (Uncle Bob), separates software into layers to ensure independence from frameworks, databases, and UIs. The core principle is the **Dependency Rule**: source code dependencies can only point inwards.

## When to Use

- **Long-Lived Enterprise Applications**: Building systems designed to evolve over 5-10+ years without being held hostage by framework obsolescence.
- **Framework & Database Decoupling**: Structuring codebases where swapping ORMs (Prisma -> Drizzle) or delivery mechanisms (REST -> gRPC) requires zero domain changes.
- **Comprehensive Unit Testing**: Enabling fast, isolated unit tests for core business use cases without requiring running databases or network stubs.
- **Complex Business Rule Isolation**: Separating intricate domain invariants from presentation controllers and database migration scripts.

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

#Dependency Inversion Principle (The Dependency Rule)

Source code dependencies must point inward only. Inner circles (Entities, Use Cases) know nothing about outer circles (Web, DB, CLI):

```
       [ Frameworks & Drivers (DB, Web, Devices) ]
                         ↓
             [ Interface Adapters (Controllers, Gateways) ]
                               ↓
                 [ Application Business Rules (Use Cases) ]
                                     ↓
                     [ Enterprise Business Rules (Entities) ]
```

#Domain Entities (Pure Business Objects)

Encapsulates core business data and invariants without external annotations or framework decorators:

```typescript
// domain/entities/subscription.entity.ts
export class Subscription {
  constructor(
    public readonly id: string,
    public readonly customerId: string,
    private _status: "ACTIVE" | "PAST_DUE" | "CANCELED",
    private _validUntil: Date,
  ) {}

  public renew(durationDays: number): void {
    if (this._status === "CANCELED") {
      throw new Error("Cannot renew a canceled subscription");
    }
    this._validUntil = new Date(
      this._validUntil.getTime() + durationDays * 86400000,
    );
    this._status = "ACTIVE";
  }

  get isValid(): boolean {
    return this._status === "ACTIVE" && this._validUntil > new Date();
  }
}
```

#Use Case Interactors & Boundary Ports

Coordinates the flow of data to and from entities, defining input/output boundary interfaces:

```typescript
// application/use-cases/renew-subscription.use-case.ts
export interface SubscriptionRepositoryPort {
  findById(id: string): Promise<Subscription | null>;
  save(sub: Subscription): Promise<void>;
}

export class RenewSubscriptionUseCase {
  constructor(private readonly repo: SubscriptionRepositoryPort) {}

  async execute(subscriptionId: string, days: number): Promise<void> {
    const sub = await this.repo.findById(subscriptionId);
    if (!sub) throw new Error("Subscription not found");
    sub.renew(days);
    await this.repo.save(sub);
  }
}
```

## Common Patterns

#Inverted Repository Dependency (Domain -> Infrastructure)
**Problem**: Business logic becomes tightly coupled to SQL ORM models and database drivers.  
**Solution**: Declare repository interfaces inside domain layer; implement them in infrastructure layer.

```typescript
// 1. Domain Layer (core/ports/user-repository.port.ts) - Zero external dependencies
export interface UserRepositoryPort {
  findById(id: string): Promise<UserEntity | null>;
  save(user: UserEntity): Promise<void>;
}

// 2. Application Layer (use-cases/create-user.use-case.ts)
export class CreateUserUseCase {
  constructor(private readonly userRepo: UserRepositoryPort) {}
  async execute(dto: CreateUserDto): Promise<UserEntity> {
    const user = new UserEntity(dto.email, dto.name);
    await this.userRepo.save(user);
    return user;
  }
}

// 3. Infrastructure Layer (adapters/drizzle-user.repository.ts)
export class DrizzleUserRepository implements UserRepositoryPort {
  async save(user: UserEntity): Promise<void> {
    await db.insert(usersTable).values({ id: user.id, email: user.email });
  }
  async findById(id: string): Promise<UserEntity | null> {
    const [row] = await db
      .select()
      .from(usersTable)
      .where(eq(usersTable.id, id));
    return row ? new UserEntity(row.email, row.name, row.id) : null;
  }
}
```

## Best Practices (2026)

**Do**:

- **Keep Domain Entities Free of Framework Imports**: Never import `@Entity`, `drizzle-orm`, or HTTP request classes in the domain layer.
- **Define Ports as Interfaces in the Domain**: Let the domain dictate its persistence requirements; implement adapters in the infrastructure layer.
- **Test Use Cases with In-Memory Mocks**: Execute thousands of unit tests in milliseconds using plain in-memory array/map repository stubs.
- **Use DTOs across Boundaries**: Map between HTTP JSON payloads and domain entities using validation schemas (Zod/Valibot).

**Don't**:

- **Don't return database ORM entities to API controllers**: Prevent database schema changes from leaking into external API contracts.
- **Don't create anemic domain models**: Do not use entities as dumb data bags with getters/setters; encapsulate operations and invariants inside methods.
- **Don't over-engineer simple CRUD apps**: Clean Architecture carries cognitive and boilerplate overhead; avoid using it for trivial prototypes.

## Troubleshooting

| Error                  | Cause                                   | Solution                                                                        |
| :--------------------- | :-------------------------------------- | :------------------------------------------------------------------------------ |
| `Circular Dependency`  | Violating the dependency rule.          | Use Dependency Inversion (Interfaces) to break the cycle.                       |
| `Boilerplate Overload` | Creating strict layers for simple CRUD. | Consider "Vertical Slice Architecture" or Modular Monolith for simpler domains. |

## References

- [The Clean Architecture Blog](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Clean Architecture vs. Hexagonal](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/)
