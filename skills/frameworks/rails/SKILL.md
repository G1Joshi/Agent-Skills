---
name: rails
description: Ruby on Rails MVC framework with Active Record and conventions. Use for rapid development.
---

# Ruby on Rails

Rails is a web application framework that includes everything needed to create web applications. Rails 8 (2025) simplifies deployment (Kamal) and reduces dependencies (Solid Cache/Queue).

## When to Use

- **Startups**: The "One Person Framework". Build a full SaaS alone.
- **Rapid Development**: Convention over Configuration makes you move fast.
- **No-Build**: Rails 8 pushes hard for "no-build" setups with Propshaft and import maps.

## Quick Start

```ruby
# app/controllers/posts_controller.rb
class PostsController < ApplicationController
  def index
    @posts = Post.all
  end
end
```

## Core Concepts

### The "Solid" Stack (Rails 8)

- **Solid Cache**: DB-backed caching (replacing Redis for simple cases).
- **Solid Queue**: DB-backed background jobs.
- **Solid Cable**: DB-backed WebSocket handling.
  Rails 8 aims to let you deploy with _just_ a SQLite/Postgres DB, no Redis required.

### Hotwire

Build SAP-like responsiveness with HTML over the wire.

- **Turbo**: Fast navigation and partial page updates.
- **Stimulus**: Modest JavaScript frameworks for the remaining 10% of interactivity.

### Kamal

The new default deploy tool. `kamal deploy` puts your app on any server using Docker.

## Best Practices (2025)

**Do**:

- **Use `Solid` libraries**: Start with the default DB-backed queue/cache. Scale to Redis only if needed.
- **Use Hotwire**: Avoid React/Vue complexity unless the UI is extremely interactive.
- **Use SQLite in Production**: For small to medium apps, Rails 8 + optimized SQLite is a valid production stack.

**Don't**:

- **Don't bloat models**: Use Concerns or Service Objects (`app/services`) for heavy business logic.

## References

- [Ruby on Rails Guides](https://guides.rubyonrails.org/)
