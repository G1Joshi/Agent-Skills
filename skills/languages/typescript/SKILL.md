---
name: typescript
description: Expert TypeScript assistance covering advanced type gymnastics, generic constraints, conditional types, mapped types, declaration merging, and tsconfig optimization. Use when building type-safe applications, designing strict library typings, or refactoring JavaScript to TypeScript.
---

# TypeScript

Static typing for JavaScript with advanced type features for safer, more maintainable code.

## When to Use

- **Enterprise Full-Stack Web Development**: Building large-scale React, Next.js, Vue, Angular, or Svelte web apps.
- **Node.js & Edge Server Backends**: Developing robust APIs with NestJS, Fastify, Express, or Hono.
- **Type-Safe Domain Modeling & SDKs**: Publishing npm libraries and SDKs with rich IntelliSense and compile-time contract safety.
- **End-to-End Type Safety (tRPC / Prisma)**: Sharing database schema and API route types across frontend and backend without codegen.

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

### Advanced Type-Level Programming: Conditional & Mapped Types

Type transformations using conditional logic, `infer`, and template literal types:

```typescript
// Deep Readonly utility type
type DeepReadonly<T> = T extends
  Function | boolean | number | string | symbol | null | undefined
  ? T
  : T extends Array<infer U>
    ? ReadonlyArray<DeepReadonly<U>>
    : { readonly [K in keyof T]: DeepReadonly<T[K]> };

// Extract event names from route path template literal
type ExtractRouteParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<Rest>
    : T extends `${string}:${infer Param}`
      ? Param
      : never;

type ApiParams = ExtractRouteParams<"/users/:userId/posts/:postId">;
// Equivalent to: "userId" | "postId"
```

### Discriminated Unions & Exhaustive Type Narrowing

Modeling finite domain states with compiler-verified completeness:

```typescript
interface LoadingState {
  status: "loading";
}

interface SuccessState<T> {
  status: "success";
  data: T;
  receivedAt: Date;
}

interface ErrorState {
  status: "error";
  error: Error;
}

type AsyncData<T> = LoadingState | SuccessState<T> | ErrorState;

function renderState<T>(state: AsyncData<T>): string {
  switch (state.status) {
    case "loading":
      return "Loading...";
    case "success":
      return `Loaded data at ${state.receivedAt.toISOString()}`;
    case "error":
      return `Failed: ${state.error.message}`;
    default: {
      // Exhaustiveness check: compile error if any union case is unhandled
      const _unhandled: never = state;
      throw new Error(`Unhandled state: ${_unhandled}`);
    }
  }
}
```

### Satisfies Operator & Exact Literal Inference

Validating structure conformance without losing precise literal types:

```typescript
type RouteConfig = {
  path: string;
  method: "GET" | "POST" | "PUT" | "DELETE";
  rateLimit?: number;
};

// The satisfies operator validates types while retaining exact literal properties
const routes = {
  getUser: { path: "/users/:id", method: "GET" },
  createPost: { path: "/posts", method: "POST", rateLimit: 60 },
} satisfies Record<string, RouteConfig>;

// Exact string literal is preserved: "GET", not widened to "GET" | "POST" | ...
const method = routes.getUser.method;
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

**Problem**: Manually recreating duplicate interfaces for partial, selected, or read-only subsets of domain models.

**Solution**:

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

- Enable `"strict": true` and `"noUncheckedIndexedAccess": true` in `tsconfig.json` for bulletproof type safety.
- Use runtime validation libraries like `Zod` or `Valibot` at API boundaries to parse untrusted JSON into verified types.
- Leverage the `satisfies` operator to validate types without widening literal types or losing autocomplete.
- Favor `type` over `interface` for complex unions and tuples; use `interface` when public declaration merging is desired.

**Don't**:

- Use `any`; use `unknown` and narrow types using type guards, `instanceof`, or discriminated unions.
- Use non-null assertions (`foo!.bar`); handle null/undefined explicitly with optional chaining (`?.`) and nullish coalescing (`??`).
- Perform double-casting (`foo as unknown as Bar`) to bypass compile-time type errors.

## Troubleshooting

| Error                                    | Cause                     | Solution                           |
| ---------------------------------------- | ------------------------- | ---------------------------------- |
| `Type 'X' is not assignable to type 'Y'` | Type mismatch             | Check types, use type guards       |
| `Object is possibly undefined`           | Nullable value access     | Use optional chaining or narrowing |
| `Cannot find module`                     | Missing type declarations | Install `@types/package`           |

## References

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
