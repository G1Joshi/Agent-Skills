---
name: angular
description: Expert Angular assistance covering Signals, Standalone Components, dependency injection, RxJS, and SSR. Use when building enterprise Single Page Applications with modern Angular.
---

# Angular

Angular is an enterprise application framework featuring fine-grained reactivity via Signals, Standalone Components, built-in routing, and form validation.

## When to Use

- **Enterprise-Scale Single Page Applications (SPAs)**: Large multidisciplinary teams needing strict conventions, DI, and end-to-end tooling.
- **Modern Reactive Frontend Architecture**: Utilizing modern Angular Signals, computed values, and Zoneless change detection.
- **Progressive Web Apps & Hybrid Mobile**: Building performant, accessible mobile-ready web apps with Angular Material.
- **Complex Form & Validation Workflows**: Utilizing typed Reactive Forms with deep nested controls and custom async validators.

## Quick Start

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

### Angular Signals & Fine-Grained Reactivity

State management using reactive primitives without Zone.js change detection overhead:

```typescript
import { Component, signal, computed, effect } from "@angular/core";

@Component({
  selector: "app-cart-summary",
  standalone: true,
  template: `
    <div class="cart-box">
      <h3>Items in Cart: {{ itemCount() }}</h3>
      <p>Subtotal: {{ total() | currency }}</p>
      <button (click)="addItem('Item', 29.99)">Add Product</button>
    </div>
  `,
})
export class CartSummaryComponent {
  items = signal<{ name: string; price: number }[]>([
    { name: "Initial License", price: 99.0 },
  ]);

  itemCount = computed(() => this.items().length);
  total = computed(() =>
    this.items().reduce((sum, item) => sum + item.price, 0),
  );

  constructor() {
    effect(() => {
      console.log(`Cart total changed: $${this.total()}`);
    });
  }

  addItem(name: string, price: number): void {
    this.items.update((list) => [...list, { name, price }]);
  }
}
```

### Dependency Injection & Typed HTTP Client

Consuming APIs with injected services and modern interceptors:

```typescript
import { Injectable, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

export interface User {
  id: string;
  name: string;
  email: string;
}

@Injectable({ providedIn: "root" })
export class UserService {
  private http = inject(HttpClient);
  private apiUrl = "/api/v1/users";

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl);
  }

  createUser(user: Omit<User, "id">): Observable<User> {
    return this.http.post<User>(this.apiUrl, user);
  }
}
```

### Typed Reactive Forms with Custom Async Validators

Robust form state handling with full type safety:

```typescript
import { Component, inject } from "@angular/core";
import { FormBuilder, Validators, ReactiveFormsModule } from "@angular/forms";

@Component({
  selector: "app-signup-form",
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="email" type="email" placeholder="Email" />
      <input
        formControlName="password"
        type="password"
        placeholder="Password"
      />
      <button type="submit" [disabled]="form.invalid">Register</button>
    </form>
  `,
})
export class SignupFormComponent {
  private fb = inject(FormBuilder);

  form = this.fb.nonNullable.group({
    email: ["", [Validators.required, Validators.email]],
    password: ["", [Validators.required, Validators.minLength(8)]],
  });

  onSubmit(): void {
    if (this.form.valid) {
      console.log("Submitted values:", this.form.getRawValue());
    }
  }
}
```

## Common Patterns

### Reactive State with Angular Signals

**Problem**: Zone.js change detection triggers full-tree re-evaluation on every async event.

**Solution**:
Use modern Angular Signals for fine-grained reactivity:

```typescript
import { Component, signal, computed } from "@angular/core";

@Component({
  selector: "app-counter",
  standalone: true,
  template: `
    <p>Count: {{ count() }}</p>
    <p>Double: {{ doubleCount() }}</p>
    <button (click)="increment()">Increment</button>
  `,
})
export class CounterComponent {
  count = signal(0);
  doubleCount = computed(() => this.count() * 2);

  increment() {
    this.count.update((n) => n + 1);
  }
}
```

## Best Practices

**Do**:

- Build with standalone components (`standalone: true`), eliminating legacy `NgModule` boilerplate.
- Use modern Angular Signals (`signal()`, `computed()`, `input()`, `output()`) for declarative state.
- Configure `provideHttpClient(withFetch())` to enable high-performance browser fetch API.
- Enforce `ChangeDetectionStrategy.OnPush` across all components to prevent redundant render cycles.

**Don't**:

- Rely on Zone.js for new applications; migrate toward Zoneless change detection for lower bundle sizes.
- Mutate signal values directly; always use `.update()` or `.set()`.
- Forget to unsubscribe from RxJS observables or use `takeUntilDestroyed()` in component constructors.

## Troubleshooting

| Error                                                       | Cause                                                           | Solution                                                                    |
| :---------------------------------------------------------- | :-------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `NG0100: ExpressionChangedAfterItHasBeenCheckedError`       | Property mutated in lifecycle hook after change detection pass. | Move state mutation to `ngOnInit` or wrap in `Promise.resolve().then(...)`. |
| `NG0203: inject() must be called from an injection context` | Calling `inject()` outside of constructor or field initializer. | Move `inject(Service)` to component constructor or property declaration.    |
| `NG0300: Multiple components match tag`                     | Component selector collision or duplicate declarations.         | Ensure unique selector tags across standalone components.                   |

## References

- [Angular Documentation](https://angular.dev/)
