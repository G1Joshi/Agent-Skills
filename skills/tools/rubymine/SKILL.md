---
name: rubymine
description: Expert RubyMine assistance covering Ruby on Rails development, gem management via Bundler, RSpec/minitest test runners, and remote container debugging. Use when configuring Ruby SDKs/rbenv/asdf, running Rails migrations, debugging RSpec specs, or profiling Ruby applications.
---

# RubyMine

RubyMine provides specialized tooling for **Ruby** and **Rails**. It excels at navigating the "Magic" of Rails (views to controllers, routes to actions).

## When to Use

- **Full-Stack Ruby on Rails Development**: Navigation between controllers, views, models, routes, and database migrations.
- **Interactive Step Debugging with Ruby Debug**: Setting conditional breakpoints, inspecting active threads, and evaluating IRB expressions.
- **RuboCop Code Style Enforcement**: Real-time linting, formatting, and auto-correcting Ruby style guide violations.
- **RSpec & Minitest Test Running**: Running individual test cases with visual pass/fail graphs and test coverage metrics.

## Quick Start

#1. Launch via Terminal

```bash
# Open Rails project in RubyMine
rubymine .
```

#2. Configure Bundler & Run Tests

```bash
# Install bundle dependencies and verify SDK
bundle install
bundle exec rspec spec/models/user_spec.rb
```

## Core Concepts

### Remote Docker Compose Interpreter Configuration

Configuring RubyMine to run Rails 7/8 inside Docker with fast code synchronization:

```yaml
# docker-compose.yml
services:
  web:
    build: .
    command: bundle exec rails s -p 3000 -b '0.0.0.0'
    volumes:
      - .:/app:cached
      - bundle_cache:/usr/local/bundle
    ports:
      - "3000:3000"
      - "1234:1234" # Remote debug port
    environment:
      RAILS_ENV: development
      RUBY_DEBUG_PORT: 1234
volumes:
  bundle_cache:
```

### RuboCop Integration & Custom Config (`.rubocop.yml`)

Configuring automated real-time linting in RubyMine:

```yaml
# .rubocop.yml
require:
  - rubocop-rails
  - rubocop-rspec
  - rubocop-performance

AllCops:
  NewCops: enable
  TargetRubyVersion: 3.3
  Exclude:
    - "bin/**/*"
    - "db/schema.rb"
    - "node_modules/**/*"
    - "vendor/**/*"

Style/Documentation:
  Enabled: false

Layout/LineLength:
  Max: 120
```

### RSpec Visual Test Execution

Running fast RSpec tests with visual assertions:

```ruby
# spec/models/user_spec.rb
require 'rails_helper'

RSpec.describe User, type: :model do
  describe 'validations' do
    subject(:user) { build(:user) }

    it { is_expected.to validate_presence_of(:email) }
    it { is_expected.to validate_uniqueness_of(:email).case_insensitive }
  end

  describe '#generate_auth_token' do
    let(:user) { create(:user) }

    it 'generates a signed 64-character token' do
      token = user.generate_auth_token
      expect(token).to be_a(String)
      expect(token.length).to eq(64)
    end
  end
end
```

## Common Patterns

#Docker Compose Remote Debugging
**Problem**: Run Rails server inside Docker Compose while hitting breakpoints in RubyMine.  
**Solution**: Configure remote Ruby SDK via Docker Compose.

```yaml
# docker-compose.yml
services:
  web:
    build: .
    command: bundle exec rails s -b '0.0.0.0' -p 3000
    volumes:
      - .:/rails
    ports:
      - "3000:3000"
    environment:
      - RUBY_DEBUG_PORT=1234
```

#Database Console Active Record Integration
**Problem**: Inspect database records and verify schema migrations directly.  
**Solution**: Execute SQL scratchpad queries against development database.

```sql
-- Scratchpad query in RubyMine Database window
SELECT id, email, created_at FROM users WHERE active = true ORDER BY created_at DESC LIMIT 10;
```

## Best Practices (2026)

- **Do** configure **RuboCop** under **Settings -> Tools -> RuboCop** with "Run on the fly" for instant linting feedback.
- **Do** use **Go to Model/Controller/View** (`Ctrl+Alt+Home` or `Cmd+Option+Up`) to jump across Rails MVC boundaries.
- **Do** leverage **Database View** to run interactive SQL migrations and inspect schema indices.
- **Do** use `debug` gem with Visual Debugger for seamless step debugging in modern Ruby 3.x.
- **Don't** commit `.idea/` workspace files or personal deployment settings to git.
- **Don't** leave Spring application preloader running when gems or C-extensions are updated; run `bin/spring stop`.
- **Don't** run test suites without Spring or parallel test execution configured on large repositories.

## Troubleshooting

| Error / Symptom                                                           | Cause                                                                  | Solution                                                                         |
| ------------------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `Gem not found` in RubyMine despite bundle install succeeding in terminal | RubyMine pointing to different Ruby version than shell `.ruby-version` | Check SDK setting in RubyMine matches `ruby -v` in project root directory.       |
| Slow indexing or freeze during Rails load                                 | Indexing `log/`, `tmp/`, or asset compilation directories              | Right-click `log/` and `tmp/` folders > **Mark Directory as > Excluded**.        |
| Breakpoints not triggering in Puma multi-worker mode                      | Puma running in cluster mode forks workers away from debug listener    | Run server with single worker in dev: `bundle exec puma -w 0` or `rails s -w 0`. |

## References

- [RubyMine Documentation](https://www.jetbrains.com/ruby/documentation/)
