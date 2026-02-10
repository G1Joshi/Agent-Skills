---
name: ruby
description: Ruby programming with blocks, metaprogramming, gems, and Rails conventions. Use for .rb files.
---

# Ruby

A dynamic, interpreted language known for its elegant syntax.

## When to Use

- Web Development (Ruby on Rails)
- Scripting / Automation
- DevOps tools (Chef, Puppet)
- Prototyping

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

### Everything is an Object

Numbers, strings, even nil are objects.

```ruby
1.odd? # => true
```

### Blocks & Iterators

Functional-style constructs for iteration.

```ruby
[1, 2, 3].each do |n|
  puts n * 2
end
```

### Metaprogramming

Writing code that writes code (used heavily in Rails).

## Best Practices

**Do**:

- Optimize for developer happiness (readability)
- Use standard style guide (RuboCop)
- Use blocks for resource management (`File.open`)

**Don't**:

- Overuse monkey patching (modifying core classes)
- Write "Perl-ish" Ruby (keep it clean)

## References

- [Ruby-Lang](https://www.ruby-lang.org/en/)
- [Ruby Style Guide](https://rubystyle.guide/)
