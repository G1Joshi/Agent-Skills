---
name: javascript
description: Expert modern JavaScript (ES2024+) assistance covering closures, async/await, promises, modules, event loop concurrency, and DOM manipulation. Use when writing frontend or Node.js code, designing clean asynchronous flows, or modernizing legacy JavaScript.
---

# JavaScript

Modern JavaScript development with ES6+ features, async patterns, and best practices.

## When to Use

- **Universal Full-Stack Web Development**: The foundational language of the web, executing across browsers, Node.js, Bun, Deno, and Edge workers.
- **Event-Driven Asynchronous Backends**: Serving high-concurrency microservices, real-time WebSockets, and serverless functions.
- **Interactive Browser User Interfaces**: Manipulating the DOM, capturing browser events, and orchestrating client-side component state.
- **Cross-Platform Scripting & Tooling**: Building developer tools, CLI scripts, and build plugins with npm/npx.

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

#Event Loop & Microtask Concurrency

JavaScript is single-threaded; asynchronous operations queue callbacks across Macrotasks and Microtasks:

```javascript
console.log("1: Synchronous start");

setTimeout(() => console.log("4: Macrotask (setTimeout)"), 0);

Promise.resolve().then(() => console.log("3: Microtask (Promise)"));

console.log("2: Synchronous end");
// Output Order: 1 -> 2 -> 3 -> 4
```

#Modern ECMAScript (ES2024+) Features

Leverages modern language primitives for concise, safe data handling:

```javascript
// Structured Clone for deep copying
const original = { user: { name: "Alice" }, tags: new Set(["admin"]) };
const deepCopy = structuredClone(original);

// Array grouping (Object.groupBy)
const inventory = [
  { name: "Apples", category: "Fruit" },
  { name: "Carrots", category: "Vegetable" },
  { name: "Bananas", category: "Fruit" },
];
const grouped = Object.groupBy(inventory, (item) => item.category);

// Safe Object hasOwn
if (Object.hasOwn(original, "user")) {
  console.log("User property exists safely");
}
```

#Async / Await with Concurrent `Promise.allSettled`

Handles batch asynchronous requests safely without failing fast on single errors:

```javascript
async function fetchUserDashboard(userId) {
  const results = await Promise.allSettled([
    fetch(`/api/users/${userId}`).then((r) => r.json()),
    fetch(`/api/users/${userId}/notifications`).then((r) => r.json()),
  ]);

  const user = results[0].status === "fulfilled" ? results[0].value : null;
  const notifications =
    results[1].status === "fulfilled" ? results[1].value : [];
  return { user, notifications };
}
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

## Best Practices (2026)

**Do**:

- **Always Use Strict Equality (`===`)**: Avoid implicit type coercion bugs by using `===` and `!==`.
- **Use `const` by Default and `let` for Reassignment**: Never use legacy function-scoped `var`.
- **Adopt Native ESM Modules**: Use `import` and `export` statements; deprecate CommonJS `require()` in modern projects.
- **Handle Rejected Promises with `try...catch`**: Always wrap `await` calls in error handling blocks to avoid unhandled rejection crashes.

**Don't**:

- **Don't block the Event Loop**: Never execute heavy synchronous loops or CPU-intensive math on the main thread; offload to Web Workers.
- **Don't pollute global prototypes**: Never modify `Array.prototype` or `Object.prototype`.
- **Don't use `eval()` or `new Function()`**: Dynamic code evaluation opens critical remote code execution (RCE) vectors.

## Troubleshooting

| Error                               | Cause                                       | Solution                              |
| ----------------------------------- | ------------------------------------------- | ------------------------------------- |
| `Cannot read property of undefined` | Accessing nested property on null/undefined | Use optional chaining `?.`            |
| `Uncaught (in promise)`             | Unhandled promise rejection                 | Add `.catch()` or try/catch           |
| `X is not a function`               | Calling undefined method                    | Check if method exists before calling |

## References

- [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
- [JavaScript.info](https://javascript.info/)
