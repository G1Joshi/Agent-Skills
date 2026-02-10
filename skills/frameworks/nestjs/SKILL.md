---
name: nestjs
description: NestJS TypeScript backend framework with decorators and modules. Use for Node.js APIs.
---

# NestJS

NestJS is a structured, opinionated framework for Node.js, heavily inspired by Angular. NestJS 10 (2025) focuses on performance with SWC integration and refined standalone modules.

## When to Use

- **Enterprise Monorepos**: Strict architecture (Controllers, Services, Modules) scales well.
- **TypeScript First**: Best-in-class TS support and decorators.
- **Microservices**: Built-in support for gRPC, MQTT, Redis transport layers.

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

### Modules

Logic is organized into Modules (`UserModule`, `AuthModule`). Dependency Injection wires them together.

### Decorators

`@Controller`, `@Get`, `@Injectable`. Declarative metadata programming.

### Guards & Interceptors

A refined pipeline for Authentication (`@UseGuards`) and Response transformation (`@UseInterceptors`).

## Best Practices (2025)

**Do**:

- **Use SWC**: Speed up builds significantly by using the SWC compiler.
- **Use Fastify adapter**: Switch from Express to Fastify for 2x performance gains if compatibility allows.
- **Use `zod` or `class-validator`**: Validate all inputs using DTOs.

**Don't**:

- **Don't allow circular dependencies**: They are a pain in NestJS. Design your modules as acyclic graphs.

## References

- [NestJS Documentation](https://docs.nestjs.com/)
