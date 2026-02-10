---
name: javascript
description: JavaScript ES6+ programming including async/await, DOM manipulation, modules, and Node.js. Use for .js files and web development.
---

# JavaScript

Modern JavaScript development with ES6+ features, async patterns, and best practices.

## When to Use

- Working with `.js` files in web or Node.js projects
- Implementing async/await patterns and promises
- DOM manipulation and event handling
- Building frontend applications

## Quick Start

```javascript
// Modern async function with error handling
async function fetchData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Fetch failed:", error);
    throw error;
  }
}
```

## Core Concepts

### Destructuring & Spread

```javascript
// Object destructuring with defaults
const { name, age = 18, ...rest } = user;

// Array destructuring
const [first, second, ...remaining] = items;

// Spread for immutable updates
const updated = { ...user, name: "New Name" };
const combined = [...array1, ...array2];
```

### Optional Chaining & Nullish Coalescing

```javascript
// Safe property access
const city = user?.address?.city;
const firstItem = items?.[0];
const result = callback?.();

// Nullish coalescing (null/undefined only)
const value = input ?? defaultValue;

// Logical assignment
user.name ??= "Anonymous";
user.permissions ||= [];
```

## Common Patterns

### Async/Await Best Practices

**Problem**: Managing multiple async operations efficiently.

**Solution**:

```javascript
// Parallel execution
async function fetchAllData(ids) {
  const promises = ids.map((id) => fetchData(id));
  return Promise.all(promises);
}

// Sequential with error handling
async function processItems(items) {
  const results = [];
  for (const item of items) {
    try {
      results.push(await processItem(item));
    } catch (error) {
      results.push({ error: error.message, item });
    }
  }
  return results;
}

// AbortController for cancellation
async function fetchWithTimeout(url, ms = 5000) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), ms);

  try {
    return await fetch(url, { signal: controller.signal });
  } finally {
    clearTimeout(timeout);
  }
}
```

### Modules

```javascript
// Named exports (preferred)
export const API_URL = "https://api.example.com";
export function fetchUser(id) {
  /* ... */
}
export class UserService {
  /* ... */
}

// Re-exports
export { default as Button } from "./Button.js";
export * from "./utils.js";

// Dynamic imports
const module = await import(`./features/${feature}.js`);
```

## Best Practices

**Do**:

- Use `const` by default, `let` when reassignment needed
- Use optional chaining (`?.`) for safe property access
- Use `Promise.allSettled()` for independent async operations
- Use named exports for better tree-shaking

**Don't**:

- Use `var` (prefer `const`/`let`)
- Use `== ` for comparison (use `===`)
- Nest callbacks deeply (use async/await)
- Mutate arrays/objects directly (use spread/map/filter)

## Troubleshooting

| Error                               | Cause                                       | Solution                              |
| ----------------------------------- | ------------------------------------------- | ------------------------------------- |
| `Cannot read property of undefined` | Accessing nested property on null/undefined | Use optional chaining `?.`            |
| `Uncaught (in promise)`             | Unhandled promise rejection                 | Add `.catch()` or try/catch           |
| `X is not a function`               | Calling undefined method                    | Check if method exists before calling |

## References

- [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
- [JavaScript.info](https://javascript.info/)
