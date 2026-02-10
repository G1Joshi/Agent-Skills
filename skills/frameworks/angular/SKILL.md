---
name: angular
description: Angular TypeScript framework with dependency injection and RxJS. Use for enterprise SPAs.
---

# Angular

Angular is a platform for building mobile and desktop web applications. Angular 19 (2025) has completely reinvented itself with Signals, Standalone Components, and optional Zone.js.

## When to Use

- **Enterprise Applications**: Strict structure, opinionated, and "batteries-included" (Router, Forms, HTTP).
- **Large Teams**: TypeScript and strict patterns make it easier for large teams to collaborate.
- **Long-term Maintenance**: Angular's update story is excellent (CLI automates migrations).

## Quick Start (Signals)

```typescript
import { Component, signal, computed } from "@angular/core";

@Component({
  selector: "app-counter",
  standalone: true,
  template: `
    <p>Count: {{ count() }}</p>
    <p>Double: {{ double() }}</p>
    <button (click)="increment()">Increment</button>
  `,
})
export class CounterComponent {
  count = signal(0);
  double = computed(() => this.count() * 2);

  increment() {
    this.count.update((c) => c + 1);
  }
}
```

## Core Concepts

### Signals

The new reactivity primitive. Fine-grained reactivity that allows Angular to drop `Zone.js` and only update the exact text node that changed.

### Standalone Components

No more `NgModule`. Components import their dependencies directly.

### Deferrable Views (`@defer`)

Built-in syntax to lazy-load parts of templates.

```html
@defer (on viewport) {
<heavy-chart />
} @placeholder {
<p>Loading...</p>
}
```

## Best Practices (2025)

**Do**:

- **Use Signals**: Prefer `signal()` over `BehaviorSubject` for component state.
- **Use `inject()`**: Prefer the `inject(Service)` function over constructor dependency injection.
- **Go Zoneless**: Enable `provideExperimentalZonelessChangeDetection()` for better performance.

**Don't**:

- **Don't use `NgModule`**: Unless maintaining legacy code.
- **Don't use `CommonModule`**: Use new control flow syntax (`@if`, `@for`) instead of `*ngIf`, `*ngFor`.

## References

- [Angular Documentation](https://angular.dev/)
