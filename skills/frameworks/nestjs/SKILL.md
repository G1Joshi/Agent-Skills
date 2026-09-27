---
name: nestjs
description: Expert NestJS assistance covering modular architecture, dependency injection, decorators, guards, interceptors, and Prisma/TypeORM. Use when building enterprise-grade, scalable TypeScript backends.
---

# NestJS

NestJS is a structured, opinionated framework for Node.js, heavily inspired by Angular. NestJS 10 (2025) focuses on performance with SWC integration and refined standalone modules.

## When to Use

- **Enterprise Node.js Backend Microservices**: Architecture inspired by Angular with modules, providers, and dependency injection.
- **Domain-Driven Modular Applications**: Structuring large codebases with clear domain separation and clean layering.
- **Multi-Transport Microservices**: Seamlessly switching between HTTP, gRPC, RabbitMQ, Kafka, and Redis transports.
- **Type-Safe REST & GraphQL Backends**: Combining TypeORM/Prisma, class-validator, and auto-generated Swagger documentation.

## Quick Start

```typescript
// cats.controller.ts
@Controller("cats")
export class CatsController {
  constructor(private catsService: CatsService) {}

  @Get()
  async findAll(): Promise<Cat[]> {
    return this.catsService.findAll();
  }
}
```

## Core Concepts

#Modular Architecture & Dependency Injection

Structuring modules, controllers, and injectable services:

```typescript
// users.service.ts
import { Injectable, NotFoundException } from "@nestjs/common";

export interface User {
  id: string;
  email: string;
}

@Injectable()
export class UsersService {
  private users: User[] = [{ id: "1", email: "admin@example.com" }];

  async findById(id: string): Promise<User> {
    const user = this.users.find((u) => u.id === id);
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    return user;
  }
}

// users.controller.ts
import { Controller, Get, Param } from "@nestjs/common";

@Controller("users")
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get(":id")
  async getUser(@Param("id") id: string) {
    return this.usersService.findById(id);
  }
}
```

#Request Validation with Pipes & Class-Validator

Validating incoming JSON payloads before controller execution:

```typescript
// create-user.dto.ts
import { IsEmail, IsNotEmpty, MinLength } from "class-validator";

export class CreateUserDto {
  @IsEmail({}, { message: "Invalid email address" })
  email: string;

  @IsNotEmpty()
  @MinLength(8, { message: "Password must be at least 8 characters" })
  password: string;
}

// main.ts
import { ValidationPipe } from "@nestjs/common";
import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true, // Strip unvalidated properties
      forbidNonWhitelisted: true,
      transform: true,
    }),
  );
  await app.listen(3000);
}
bootstrap();
```

#Execution Guards & Role-Based Access Control (RBAC)

Protecting endpoints with custom authentication guards:

```typescript
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  UnauthorizedException,
} from "@nestjs/common";
import { Request } from "express";

@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest<Request>();
    const authHeader = request.headers.authorization;

    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      throw new UnauthorizedException("Valid authorization token required");
    }

    // Attach verified user payload
    request["user"] = { id: "usr_101", role: "admin" };
    return true;
  }
}
```

## Common Patterns

### Role-Based Access Control (RBAC) Guard with Reflector

**Problem**: Duplicating role checks across individual controller route handlers.

**Solution**:
Use custom SetMetadata decorator and global RolesGuard:

```typescript
import { Injectable, CanActivate, ExecutionContext } from "@nestjs/common";
import { Reflector } from "@nestjs/core";

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<string[]>(
      "roles",
      context.getHandler(),
    );
    if (!requiredRoles) return true;
    const request = context.switchToHttp().getRequest();
    const user = request.user;
    return requiredRoles.some((role) => user?.roles?.includes(role));
  }
}
```

## Best Practices (2026)

- **Do** enable `whitelist: true` and `forbidNonWhitelisted: true` in global `ValidationPipe` to prevent mass-assignment attacks.
- **Do** split applications into discrete domain modules (`UserModule`, `OrderModule`, `AuthModule`) with explicit exports.
- **Do** use Fastify adapter (`@nestjs/platform-fastify`) for performance-sensitive microservices.
- **Do** handle configuration with `@nestjs/config` and validate environment variables with Joi or Zod.
- **Don't** put business logic inside controllers; keep controllers strictly focused on request handling.
- **Don't** use circular dependencies between modules; use `forwardRef()` only as an absolute last resort.
- **Don't** catch exceptions silently without rethrowing or logging through Nest's `Logger` service.

## Troubleshooting

| Error                                                             | Cause                                                                         | Solution                                                                          |
| :---------------------------------------------------------------- | :---------------------------------------------------------------------------- | :-------------------------------------------------------------------------------- |
| `Nest can't resolve dependencies of the ...`                      | Required service or repository not listed in module `providers` or `imports`. | Add the missing service to module `providers` or export it from its host module.  |
| `Cannot find module '...' or its corresponding type declarations` | Path alias in `tsconfig.json` not recognized by Nest CLI runner.              | Verify `baseUrl` and `paths` mapping in both `tsconfig.json` and `nest-cli.json`. |
| `Circular dependency detected in ...`                             | Two services directly injecting each other in constructor.                    | Use `forwardRef(() => OtherService)` in both `@Inject()` annotations.             |

## References

- [NestJS Documentation](https://docs.nestjs.com/)
