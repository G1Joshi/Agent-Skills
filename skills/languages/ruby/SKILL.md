---
name: ruby
description: Expert Ruby programming assistance covering blocks, metaprogramming, Bundler, gems, and modern Ruby 3.x features. Use when developing Rails web apps, writing CLI utilities, or managing Ruby gems.
---

# Ruby

A dynamic, interpreted language known for its elegant syntax.

## When to Use

- **Rapid Web Application Development (Ruby on Rails)**: Building full-stack web applications, startups, and MVPs with unmatched developer velocity.
- **E-Commerce & Digital Storefronts**: Powering platforms like Shopify, Spree Commerce, and custom checkout flows.
- **Developer Tooling & Automation**: Authoring automated DevOps scripts, Homebrew formulas, and Fastlane mobile deployment pipelines.
- **Background Processing & Queues**: Executing asynchronous jobs using Sidekiq backed by Redis.

## Quick Start

```ruby
puts "Hello, World!"

class Greeter
  def initialize(name)
    @name = name
  end

  def say_hi
    puts "Hi #{@name}!"
  end
end

g = Greeter.new("Alice")
g.say_hi
```

## Core Concepts

#Object-Oriented Everything & Dynamic Metaprogramming

Every value in Ruby is a full-fledged object; classes can be modified dynamically at runtime:

```ruby
class Integer
  def to_usd
    "$#{format('%.2f', self)}"
  end
end

puts 100.to_usd # "$100.00"
```

#Blocks, Procs & Enumerable Power

Passes executable code blocks to methods for clean data manipulation:

```ruby
orders = [
  { id: 1, total: 45.0, status: :completed },
  { id: 2, total: 120.0, status: :pending },
  { id: 3, total: 85.0, status: :completed }
]

completed_revenue = orders
  .select { |o| o[:status] == :completed }
  .sum { |o| o[:total] }

puts "Completed Revenue: $#{completed_revenue}" # 130.0
```

#Modern Concurrency (Fibers & Ractor)

Runs true parallel execution without Global VM Lock (GVL) contention using Ractors (Ruby 3+):

```ruby
# Parallel computation across multiple CPU cores
r = Ractor.new do
  # Completely isolated memory space
  1_000_000.times.reduce(:+)
end

puts "Ractor Result: #{r.take}"
```

## Common Patterns

### Pattern Matching with Value Extraction (Ruby 3+)

**Problem**: Verbose nested `if/elsif` conditionals when handling structured JSON API responses.

**Solution**:
Use Ruby 3 native pattern matching:

```ruby
def handle_response(response)
  case response
  in { status: 200, data: { user: { name:, email: } } }
    puts "User found: #{name} <#{email}>"
  in { status: 404, error: msg }
    warn "Not found: #{msg}"
  in { status: (500..) }
    raise "Server error occurred"
  else
    puts "Unknown response format"
  end
end
```

## Best Practices (2026)

**Do**:

- **Enable YJIT in Production**: Launch Ruby with `--yjit` to enable the native Just-in-Time compiler, boosting performance 20-40%.
- **Use RuboCop with Modern Presets**: Enforce style consistency and detect security pitfalls with automated RuboCop linting.
- **Freeze String Literals**: Add `# frozen_string_literal: true` at the top of files to reduce heap string allocations.
- **Use `Sorbet` or RBS for Type Checking**: Add static typing to mission-critical business modules.

**Don't**:

- **Don't use monkey-patching in application code**: Overriding core methods globally creates fragile, untraceable bugs across gems.
- **Don't query the database inside loops (N+1)**: Use `.includes()` or `.preload()` in ActiveRecord to eager-load associations.
- **Don't rescue `Exception`**: Always rescue `StandardError` (`rescue => e`); rescuing `Exception` catches system exit and termination signals.

## Troubleshooting

| Error                                                    | Cause                                               | Solution                                                                      |
| :------------------------------------------------------- | :-------------------------------------------------- | :---------------------------------------------------------------------------- |
| `NoMethodError: undefined method '...' for nil:NilClass` | Calling method on a nil object.                     | Use safe navigation operator `object&.method_name`.                           |
| `LoadError: cannot load such file -- ...`                | Gem not installed or missing in Gemfile.            | Run `bundle install` and execute script via `bundle exec ruby script.rb`.     |
| `NameError: uninitialized constant`                      | Constant/Class not required or module nesting typo. | Check file require paths and ensure file naming matches Zeitwerk conventions. |

## References

- [Ruby-Lang](https://www.ruby-lang.org/en/)
- [Ruby Style Guide](https://rubystyle.guide/)
