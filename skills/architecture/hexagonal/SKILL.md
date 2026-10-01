---
name: hexagonal
description: Expert Hexagonal Architecture (Ports and Adapters) assistance covering driving/driven ports, infrastructure adapters, domain core isolation, and test stubbing. Use when decoupling domain logic from databases/HTTP frameworks, improving testability, or modernizing enterprise applications.
---

# Hexagonal Architecture (Ports and Adapters)

Hexagonal Architecture aims to create a loosely coupled application component that can easily connect to their software environment by "ports" and "adapters". It treats the database, the web UI, and external APIs as interchangeable "details" (infrastructure).

## When to Use

- **Core Business Logic Isolation**: Keeping domain models completely pure and independent of database choices, web frameworks, and messaging tools.
- **Pluggable Architecture**: Systems where components (e.g. storage engine, notification providers, payment gateways) must be easily swappable.
- **Automated Regression Testing**: Running full business scenario tests with fast, zero-dependency in-memory adapters.
- **Microservice Reusability**: Allowing the exact same business core to be driven by an HTTP REST controller, a gRPC server, and a CLI simultaneously.

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

### Ports and Adapters Topology

The application core sits at the center; Driving Ports receive input from the outside world; Driven Ports communicate with infrastructure:

```text
[ HTTP Controller ] ──(Driving Port)──→ [ APPLICATION CORE ] ──(Driven Port)──→ [ Postgres Adapter ]
[ CLI Command ]     ──(Driving Port)──→ [ APPLICATION CORE ] ──(Driven Port)──→ [ Mock DB Adapter ]
```

### Driving Port & Primary Adapter

The driving port defines what the application can do:

```typescript
// core/ports/driving/register-user.port.ts
export interface RegisterUserCommand {
  email: string;
  fullName: string;
}

export interface RegisterUserUseCase {
  execute(command: RegisterUserCommand): Promise<string>;
}
```

```typescript
// adapters/driving/http/user.controller.ts (Primary Adapter)
export class UserController {
  constructor(private readonly registerUserUseCase: RegisterUserUseCase) {}

  async handlePost(req: Request, res: Response) {
    const userId = await this.registerUserUseCase.execute(req.body);
    res.status(201).json({ id: userId });
  }
}
```

### Driven Port & Secondary Adapter

The driven port defines external capabilities needed by the core:

```typescript
// core/ports/driven/notification.port.ts
export interface NotificationPort {
  sendWelcomeEmail(email: string, name: string): Promise<void>;
}

// adapters/driven/resend-email.adapter.ts (Secondary Adapter)
export class ResendEmailAdapter implements NotificationPort {
  async sendWelcomeEmail(email: string, name: string) {
    await resend.emails.send({
      to: email,
      subject: `Welcome, ${name}!`,
      from: "app@example.com",
    });
  }
}
```

## Common Patterns

### Mock Adapter for Unit Testing Ports

**Problem**: Testing business core without spinning up actual databases or message brokers.  
**Solution**: Implement an in-memory stub that satisfies the driven port interface.

```typescript
// test/mocks/in-memory-order.repository.ts
export class InMemoryOrderRepository implements OrderRepositoryPort {
  private readonly items = new Map<string, Order>();

  async save(order: Order): Promise<void> {
    this.items.set(order.id, order);
  }

  async findById(id: string): Promise<Order | null> {
    return this.items.get(id) ?? null;
  }
}

// Unit test executes with zero I/O overhead:
const repo = new InMemoryOrderRepository();
const service = new OrderService(repo);
```

## Best Practices

**Do**:

- Define Ports as Interfaces Inside Core: Ensure driven ports are authored by the business domain team, not infrastructure engineers.
- Create In-Memory Adapters for Fast Testing: Implement mock adapters for all driven ports to enable sub-second test suite runs.
- Keep Domain Core Pure: Disallow any external library imports in the domain core (except language utilities).
- Use Dependency Injection: Bind ports to concrete adapters at application bootstrap time.

**Don't**:

- Let infrastructure types enter the domain: Map incoming database models and HTTP requests to domain types inside adapters.
- Bypass the ports: Never allow driving adapters (controllers) to communicate directly with driven adapters (databases).
- Over-engineer simple utility services: For simple scripts or read-only tools, Hexagonal Architecture adds unnecessary complexity.

## Troubleshooting

| Error        | Cause                                    | Solution                                                 |
| :----------- | :--------------------------------------- | :------------------------------------------------------- |
| `Leakage`    | Logic depends on specific library types. | Wrap external types in domain-specific DTOs/Interfaces.  |
| `Complexity` | Too many interfaces for simple logic.    | Start with a simple Service/Repository split and evolve. |

## References

- [Alistair Cockburn's Original Paper](https://alistair.cockburn.us/hexagonal-architecture/)
- [Hexagonal Architecture in Go](https://medium.com/@matiasvarela/hexagonal-architecture-in-go-cfd4e436bd57)
