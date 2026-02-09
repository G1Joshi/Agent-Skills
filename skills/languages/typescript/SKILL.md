---
name: typescript
description: TypeScript best practices including advanced types, generics, type guards, utility types, and patterns for type-safe applications. Use for .ts files.
---

# TypeScript

Static typing for JavaScript with advanced type features for safer, more maintainable code.

## When to Use

- Working with `.ts` or `.tsx` files
- Building type-safe APIs and applications
- Defining complex data models with validation
- Creating reusable generic utilities

## Quick Start

```typescript
// Define a typed interface
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

// Type-safe function
async function fetchUser(id: string): Promise<User | undefined> {
  const response = await fetch(`/api/users/${id}`);
  return response.ok ? response.json() : undefined;
}
```

## Core Concepts

### Interfaces and Types

```typescript
// Interface for object shapes (extendable)
interface User {
  id: string;
  name: string;
  email: string;
}

// Type for unions, intersections, mapped types
type Status = "pending" | "active" | "inactive";
type UserWithStatus = User & { status: Status };
```

### Generics

```typescript
// Generic functions
function first<T>(items: T[]): T | undefined {
  return items[0];
}

// Generic constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Generic interfaces
interface Repository<T extends { id: string }> {
  findById(id: string): Promise<T | null>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<void>;
}
```

## Common Patterns

### Type Guards

**Problem**: Narrowing unknown types at runtime.

**Solution**:

```typescript
// Type predicates
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value
  );
}

// Discriminated unions
type Result<T> = { success: true; data: T } | { success: false; error: string };

function handleResult<T>(result: Result<T>) {
  if (result.success) {
    console.log(result.data); // Type: T
  } else {
    console.error(result.error); // Type: string
  }
}
```

### Utility Types

```typescript
// Make all properties optional
type Partial<T> = { [P in keyof T]?: T[P] };

// Pick specific properties
type UserPreview = Pick<User, "id" | "name">;

// Omit specific properties
type UserCreate = Omit<User, "id" | "createdAt">;

// Brand types for nominal typing
type UserId = string & { readonly brand: unique symbol };
```

## Best Practices

**Do**:

- Enable `strict` mode in `tsconfig.json`
- Use `unknown` instead of `any` for truly unknown types
- Use discriminated unions for state management
- Export types alongside implementations

**Don't**:

- Use `any` to bypass type checking
- Use type assertions (`as`) when narrowing works
- Ignore TypeScript errors with `// @ts-ignore`
- Mix `interface` and `type` inconsistently

## Troubleshooting

| Error                                    | Cause                     | Solution                           |
| ---------------------------------------- | ------------------------- | ---------------------------------- |
| `Type 'X' is not assignable to type 'Y'` | Type mismatch             | Check types, use type guards       |
| `Object is possibly undefined`           | Nullable value access     | Use optional chaining or narrowing |
| `Cannot find module`                     | Missing type declarations | Install `@types/package`           |

## References

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
