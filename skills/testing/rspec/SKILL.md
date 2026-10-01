---
name: rspec
description: Expert RSpec testing assistance covering Ruby BDD testing, mocks, expectations, and let/subject helpers. Use when writing Rails/Ruby tests, testing controllers/models, or running `bundle exec rspec`.
---

# RSpec

RSpec is the primary testing tool for Ruby (especially Rails). It focuses on "Behavior Driven Development" (BDD), making tests read like documentation specifications.

## When to Use

- **Ruby on Rails BDD Testing**: The standard Behavior-Driven Development testing framework for Ruby and Rails applications.
- **Expressive Specification Design**: Writing readable, self-documenting specifications using `describe`, `context`, and `it`.
- **Database & Model Validation**: Testing ActiveRecord validations, scopes, and associations with `shoulda-matchers`.
- **Comprehensive Mocking & Stubbing**: Isolating dependencies using `instance_double` and `allow().to receive()`.

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

### Hierarchical Contexts & Readable Specifications

Structures tests to match human-readable business expectations:

```ruby
# spec/models/order_spec.rb
RSpec.describe Order, type: :model do
  describe "#apply_coupon" do
    context "when coupon is valid" do
      let(:coupon) { create(:coupon, discount_percentage: 20) }
      let(:order) { create(:order, total: 100) }

      it "deducts percentage from order total" do
        order.apply_coupon(coupon)
        expect(order.total).to eq(80)
      end
    end

    context "when coupon has expired" do
      let(:expired_coupon) { create(:coupon, expires_at: 1.day.ago) }
      let(:order) { create(:order, total: 100) }

      it "raises an expired coupon error" do
        expect { order.apply_coupon(expired_coupon) }
          .to raise_error(CouponExpiredError)
      end
    end
  end
end
```

### Verified Mocks (`instance_double`)

Prevents stale mocks by validating that mocked methods actually exist on the target class:

```ruby
it "calls external payment gateway" do
  gateway = instance_double(PaymentGateway)
  expect(gateway).to receive(:charge).with(100).and_return(true)

  service = CheckoutService.new(gateway: gateway)
  service.process(100)
end
```

### FactoryBot Integration for Test Fixtures

Generates flexible model test records without brittle fixtures:

```ruby
# spec/factories/users.rb
FactoryBot.define do
  factory :user do
    sequence(:email) { |n| "user#{n}@example.com" }
    password { "Password123!" }
    role { "member" }

    trait :admin do
      role { "admin" }
    end
  end
end
```

## Common Patterns

### Expressive Contexts with Let and Subject

**Problem**: Monolithic test cases testing both valid and invalid states together with hard-to-read assertions.

**Solution**:
Use nested `context` blocks with lazy-evaluated `let`:

```ruby
RSpec.describe Order do
  let(:order) { described_class.new(amount: amount) }

  context "when amount is positive" do
    let(:amount) { 50 }

    it "is valid and processes successfully" do
      expect(order).to be_valid
      expect(order.process).to be true
    end
  end

  context "when amount is zero or negative" do
    let(:amount) { 0 }

    it "is invalid with an error message" do
      expect(order).not_to be_valid
      expect(order.errors[:amount]).to include("must be greater than 0")
    end
  end
end
```

## Best Practices

**Do**:

- Use `instance_double` Instead of `double`: Catch renamed or deleted methods immediately during test execution.
- Use `build_stubbed` in FactoryBot for Unit Tests: Avoid touching the database when testing pure model logic.
- Keep `it` Blocks to a Single Expectation: Isolate failures clearly; one assertion per specification.
- Use `context` Blocks Starting with "when" or "with": Clarify environmental preconditions and business states.

**Don't**:

- Overuse `let!` (bang): Eager loading on every test slows down test suites; prefer lazy `let` unless eager creation is required.
- Test framework features: Test custom business logic; avoid testing standard Rails ActiveRecord functionality directly.
- Leave mysterious instance variables (`@user`): Use explicit `let` bindings for predictable memoization.

## Troubleshooting

| Error                                              | Cause                                                     | Solution                                                            |
| :------------------------------------------------- | :-------------------------------------------------------- | :------------------------------------------------------------------ |
| `LoadError: cannot load such file -- rails_helper` | Running RSpec in a Rails app without loading helper.      | Ensure `require 'rails_helper'` is at the top of the spec file.     |
| `Double received unexpected message`               | Test double received a method call that was not declared. | Allow or expect method with `allow(mock).to receive(:method_name)`. |
| `RSpec::Expectations::ExpectationNotMetError`      | Expected return value or predicate failed.                | Check diff in terminal output and verify matcher syntax.            |

## References

- [RSpec Documentation](https://rspec.info/)
