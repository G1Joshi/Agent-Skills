---
name: mvc
description: Model-View-Controller architecture pattern for separating concerns. Use for traditional web apps.
---

# MVC (Model-View-Controller)

Architectural pattern separating data, presentation, and logic.

## When to Use

- Traditional web applications
- Server-rendered pages
- Clear separation of concerns
- Team role separation

## Quick Start

```typescript
// Model
class UserModel {
  constructor(
    public id: string,
    public name: string,
    public email: string,
  ) {}
}

// Controller
class UserController {
  async getUser(req: Request, res: Response) {
    const user = await UserService.findById(req.params.id);
    res.render("user/show", { user });
  }
}

// View (EJS/Pug template)
// views/user/show.ejs
// <h1><%= user.name %></h1>
```

## Core Concepts

### Model

```typescript
// Domain model with validation
class User {
  constructor(
    private _name: string,
    private _email: string,
  ) {
    this.validate();
  }

  private validate() {
    if (!this._email.includes("@")) {
      throw new Error("Invalid email");
    }
  }

  get name() {
    return this._name;
  }
  get email() {
    return this._email;
  }
}
```

### Controller

```typescript
class ProductController {
  constructor(private productService: ProductService) {}

  async index(req: Request, res: Response) {
    const products = await this.productService.findAll();
    res.render("products/index", { products });
  }

  async create(req: Request, res: Response) {
    await this.productService.create(req.body);
    res.redirect("/products");
  }
}
```

## Common Patterns

### RESTful Routes

```typescript
// routes/products.ts
router.get("/products", controller.index);
router.get("/products/new", controller.new);
router.post("/products", controller.create);
router.get("/products/:id", controller.show);
router.get("/products/:id/edit", controller.edit);
router.put("/products/:id", controller.update);
router.delete("/products/:id", controller.destroy);
```

## Best Practices

**Do**: Keep controllers thin, models fat with business logic
**Don't**: Put business logic in controllers or views

## References

- [MVC Pattern](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)
