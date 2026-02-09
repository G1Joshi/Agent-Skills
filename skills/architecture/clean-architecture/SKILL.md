---
name: clean-architecture
description: Clean Architecture with layers, dependency injection, and SOLID principles. Use for maintainable code.
---

# Clean Architecture

Layered architecture for maintainable, testable applications.

## When to Use

- Long-lived applications
- Complex business logic
- Testable codebase
- Framework independence

## Quick Start

```
src/
├── domain/           # Entities, value objects
├── application/      # Use cases, DTOs
├── infrastructure/   # Database, external APIs
└── presentation/     # Controllers, routes
```

## Core Concepts

### Layers

```typescript
// Domain - Entities
class User {
  constructor(
    public readonly id: string,
    public readonly email: Email,
    public readonly name: string,
  ) {}

  changeEmail(newEmail: Email): User {
    return new User(this.id, newEmail, this.name);
  }
}

// Application - Use Cases
class CreateUserUseCase {
  constructor(private userRepository: UserRepository) {}

  async execute(input: CreateUserInput): Promise<User> {
    const email = new Email(input.email);
    const user = new User(generateId(), email, input.name);
    await this.userRepository.save(user);
    return user;
  }
}

// Infrastructure - Repository Implementation
class PrismaUserRepository implements UserRepository {
  async save(user: User): Promise<void> {
    await prisma.user.create({
      data: {
        id: user.id,
        email: user.email.value,
        name: user.name,
      },
    });
  }
}
```

### Dependency Injection

```typescript
// Interfaces in domain
interface UserRepository {
  save(user: User): Promise<void>;
  findById(id: string): Promise<User | null>;
}

// Container setup
const container = {
  userRepository: new PrismaUserRepository(),
  createUser: new CreateUserUseCase(this.userRepository),
};

// Controller uses use case
class UserController {
  constructor(private createUser: CreateUserUseCase) {}

  async create(req: Request, res: Response) {
    const user = await this.createUser.execute(req.body);
    res.status(201).json(user);
  }
}
```

## Common Patterns

### Value Objects

```typescript
class Email {
  constructor(public readonly value: string) {
    if (!this.isValid(value)) {
      throw new Error("Invalid email");
    }
  }

  private isValid(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }
}
```

### Result Pattern

```typescript
type Result<T, E = Error> =
  | { success: true; value: T }
  | { success: false; error: E };

class CreateUserUseCase {
  async execute(input: CreateUserInput): Promise<Result<User>> {
    try {
      const email = new Email(input.email);
      const user = new User(generateId(), email, input.name);
      await this.userRepository.save(user);
      return { success: true, value: user };
    } catch (error) {
      return { success: false, error: error as Error };
    }
  }
}
```

## Best Practices

**Do**:

- Depend on abstractions
- Keep domain pure
- Use constructor injection
- Test use cases in isolation

**Don't**:

- Reference infrastructure from domain
- Put business logic in controllers
- Skip value object validation
- Tightly couple to frameworks

## Troubleshooting

| Issue               | Cause                 | Solution                   |
| ------------------- | --------------------- | -------------------------- |
| Circular dependency | Wrong layer           | Check dependency direction |
| Hard to test        | Concrete dependencies | Use interfaces             |
| Anemic domain       | Logic in services     | Move to entities           |

## References

- [Clean Architecture Book](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
- [DDD Reference](https://www.domainlanguage.com/ddd/reference/)
