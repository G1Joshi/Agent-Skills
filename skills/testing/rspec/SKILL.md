---
name: rspec
description: RSpec Ruby testing framework. Use for Ruby testing.
---

# RSpec

RSpec is the primary testing tool for Ruby (especially Rails). It focuses on "Behavior Driven Development" (BDD), making tests read like documentation specifications.

## When to Use

- **Ruby/Rails Projects**: The community standard (over Minitest) for complex apps.
- **Documentation**: You want tests that generate readable specs.

## Quick Start

```ruby
# user_spec.rb
RSpec.describe User, type: :model do
  context "when newly created" do
    it "has no name" do
      user = User.new
      expect(user.name).to be_nil
    end
  end
end
```

## Core Concepts

### `describe` vs `context`

- `describe`: Describes the thing being tested (Class, Method).
- `context`: Describes the condition ("when user is logged in").

### Let and Let!

Lazy-loaded variables.

- `let(:user) { User.create }`: Created only when referenced.
- `let!(:user) { User.create }`: Created before each test (eager).

### Matchers

`expect(x).to eq(y)`, `be_valid`, `change { User.count }.by(1)`.

## Best Practices (2025)

**Do**:

- **Use `subject`**: Define the subject of the test explicitly.
- **Keep `it` blocks short**: One expectation per block ideally.
- **Use FactoryBot**: Don't use Fixtures (YAML). Use Factories to build test data.

**Don't**:

- **Don't overuse `before(:all)`**: It introduces shared state between examples. Use `before(:each)` (default).
- **Don't put logic in specs**: Specs should verify behavior, not calculate it.

## References

- [RSpec Documentation](https://rspec.info/)
