---
name: rails
description: Expert Ruby on Rails assistance covering ActiveRecord, MVC architecture, migrations, background jobs (Sidekiq/SolidQueue), and Hotwire. Use when building full-stack web apps with convention over configuration.
---

# Ruby on Rails

Rails is a web application framework that includes everything needed to create web applications. Rails 8 (2025) simplifies deployment (Kamal) and reduces dependencies (Solid Cache/Queue).

## When to Use

- **High-Velocity Full-Stack Web Development**: Building robust SaaS products with convention over configuration.
- **Modern Monoliths with Hotwire / Turbo**: Delivering reactive, SPA-like user experiences without heavy frontend frameworks.
- **Database-Driven Business Applications**: Leveraging Active Record associations, scopes, and validations.
- **Background Jobs & Real-Time WebSockets**: Utilizing Solid Queue, Solid Cache, and Action Cable in Rails 7.2 / 8.

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

#Active Record Models with Scopes & Validations

Defining business logic and relational constraints:

```ruby
class Order < ApplicationRecord
  belongs_to :customer
  has_many :line_items, dependent: :destroy

  validates :total_amount, presence: true, numericality: { greater_than: 0 }
  validates :status, inclusion: { in: %w[pending paid shipped canceled] }

  scope :recent, -> { order(created_at: :desc) }
  scope :paid, -> { where(status: 'paid') }

  after_commit :enqueue_fulfillment, on: :create

  private

  def enqueue_fulfillment
    FulfillmentJob.perform_later(id)
  end
end
```

#Hotwire & Turbo Streams for Real-Time Updates

Server-rendered partials pushed over WebSockets or response streams:

```ruby
# app/controllers/messages_controller.rb
class MessagesController < ApplicationController
  def create
    @message = Message.create!(message_params)

    respond_to do |format|
      format.turbo_stream do
        render turbo_stream: turbo_stream.append(
          'messages_list',
          partial: 'messages/message',
          locals: { message: @message }
        )
      end
      format.html { redirect_to @message.room }
    end
  end
end
```

#Background Processing with Active Job

Asynchronous queue job execution:

```ruby
class FulfillmentJob < ApplicationJob
  queue_as :default

  retry_on Net::OpenTimeout, wait: :exponentially_longer, attempts: 3

  def perform(order_id)
    order = Order.find(order_id)
    OrderFulfillmentService.new(order).process!
  end
end
```

## Common Patterns

### Turbo Stream Real-Time Dom Updates (Hotwire)

**Problem**: Needing single-page app reactivity without complex React/Vue frontend builds.

**Solution**:
Broadcast model updates via Turbo Streams:

```ruby
# app/models/message.rb
class Message < ApplicationRecord
  belongs_to :room
  after_create_commit -> {
    broadcast_append_to room, target: "messages", partial: "messages/message", locals: { message: self }
  }
end
```

## Best Practices (2026)

- **Do** target Rails 7.2 / 8 with Propshaft asset pipeline and built-in Solid Queue / Solid Cache.
- **Do** always use strong parameters (`params.require(:order).permit(...)`) in controllers.
- **Do** use `includes` or `strict_loading` to prevent N+1 query performance degradation.
- **Do** encapsulate complex multi-model business logic inside Plain Old Ruby Object (PORO) service objects.
- **Don't** put business logic or complex database queries inside view templates or controllers.
- **Don't** run long-running tasks synchronously inside HTTP controller actions; offload to Active Job.
- **Don't** skip database indexes on foreign keys; declare them explicitly in migrations.

## Troubleshooting

| Error                                           | Cause                                                 | Solution                                                          |
| :---------------------------------------------- | :---------------------------------------------------- | :---------------------------------------------------------------- |
| `ActiveRecord::RecordNotFound`                  | `find(id)` called with non-existent primary key.      | Use `find_by(id: ...)` or handle rescue in ApplicationController. |
| `ActionController::InvalidAuthenticityToken`    | CSRF token missing or mismatch in POST/PATCH request. | Include `<%= csrf_meta_tags %>` in layout or verify headers.      |
| `PendingMigrationError: Migrations are pending` | Database schema out of date with migration files.     | Run `bin/rails db:migrate`.                                       |

## References

- [Ruby on Rails Guides](https://guides.rubyonrails.org/)
