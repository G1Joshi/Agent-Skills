---
name: angular
description: Angular TypeScript framework with dependency injection, RxJS, and components. Use for enterprise SPAs.
---

# Angular

Full-featured TypeScript framework for enterprise applications.

## When to Use

- Enterprise single-page applications
- Complex forms and validation
- Large team projects
- Applications requiring strong typing

## Quick Start

```typescript
import { Component } from "@angular/core";

@Component({
  selector: "app-root",
  standalone: true,
  template: `
    <h1>{{ title }}</h1>
    <button (click)="increment()">Count: {{ count }}</button>
  `,
})
export class AppComponent {
  title = "My App";
  count = 0;

  increment() {
    this.count++;
  }
}
```

## Core Concepts

### Components & Signals

```typescript
import { Component, signal, computed, effect } from "@angular/core";

@Component({
  selector: "app-counter",
  standalone: true,
  template: `
    <p>Count: {{ count() }}</p>
    <p>Double: {{ double() }}</p>
    <button (click)="increment()">+</button>
  `,
})
export class CounterComponent {
  count = signal(0);
  double = computed(() => this.count() * 2);

  constructor() {
    effect(() => console.log("Count changed:", this.count()));
  }

  increment() {
    this.count.update((c) => c + 1);
  }
}
```

### Services & DI

```typescript
import { Injectable, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Injectable({ providedIn: "root" })
export class UserService {
  private http = inject(HttpClient);

  getUsers() {
    return this.http.get<User[]>("/api/users");
  }

  getUser(id: string) {
    return this.http.get<User>(`/api/users/${id}`);
  }
}
```

## Common Patterns

### Reactive Forms

```typescript
import { ReactiveFormsModule, FormBuilder, Validators } from "@angular/forms";

@Component({
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="email" />
      <input formControlName="password" type="password" />
      <button [disabled]="form.invalid">Submit</button>
    </form>
  `,
})
export class LoginComponent {
  private fb = inject(FormBuilder);

  form = this.fb.group({
    email: ["", [Validators.required, Validators.email]],
    password: ["", [Validators.required, Validators.minLength(8)]],
  });

  onSubmit() {
    if (this.form.valid) {
      console.log(this.form.value);
    }
  }
}
```

## Best Practices

**Do**:

- Use standalone components
- Use signals for state
- Use inject() function
- Implement OnPush change detection

**Don't**:

- Subscribe without unsubscribing
- Use any type
- Mutate inputs directly
- Put logic in templates

## Troubleshooting

| Issue               | Cause                   | Solution                    |
| ------------------- | ----------------------- | --------------------------- |
| Change not detected | OnPush with mutation    | Use signals or markForCheck |
| Memory leak         | Unsubscribed observable | Use takeUntilDestroyed      |
| Circular dependency | Service circular ref    | Use forwardRef              |

## References

- [Angular Documentation](https://angular.dev/)
- [Angular Blog](https://blog.angular.io/)
