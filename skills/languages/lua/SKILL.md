---
name: lua
description: Expert Lua programming assistance covering tables, metatables, closures, coroutines, and C embedding. Use when writing game scripts, Neovim plugins, Nginx OpenResty modules, or embedded device logic.
---

# Lua

A powerful, efficient, lightweight, embeddable scripting language.

## When to Use

- **Game Engine Scripting & Modding**: Scripting gameplay logic, AI behavior, and UI in Roblox, World of Warcraft, and LÖVE2D.
- **High-Performance Web Gateways (Nginx / OpenResty)**: Executing microsecond request routing, auth token checks, and WAF rules in Nginx.
- **Redis Server-Side Scripting**: Running atomic transactions and complex data manipulations directly inside Redis instances.
- **Extensible Editor Configurations (Neovim)**: Writing custom editor plugins, keymaps, and LSP hooks in modern Neovim.

## Quick Start

```lua
print("Hello, World!")

function factorial(n)
  if n == 0 then
    return 1
  else
    return n * factorial(n - 1)
  end
end
```

## Core Concepts

#Tables as Universal Data Structures

Lua represents arrays, hashes, objects, modules, and namespaces using a single unified primitive: the Table:

```lua
-- Array style (1-indexed!)
local fruits = {"Apple", "Banana", "Cherry"}
print("First item:", fruits[1])

-- Hash / Dictionary style
local config = {
  host = "127.0.0.1",
  port = 8080,
  ["max-connections"] = 100
}

-- Iterating key-value pairs
for key, value in pairs(config) do
  print(key .. " = " .. tostring(value))
end
```

#Metatables & Object-Oriented Inheritance

Overloads table behaviors (operators, indexing, custom methods) via metamethods:

```lua
local Account = {}
Account.__index = Account

function Account.new(balance)
  local self = setmetatable({}, Account)
  self.balance = balance or 0
  return self
end

function Account:deposit(amount)
  self.balance = self.balance + amount
  return self.balance
end

local acc = Account.new(100)
acc:deposit(50)
print("Account balance:", acc.balance) -- 150
```

#Coroutines for Cooperative Concurrency

Fibers with manual yield and resume control:

```lua
local co = coroutine.create(function()
  for i = 1, 3 do
    print("Coroutine yield:", i)
    coroutine.yield()
  end
end)

coroutine.resume(co) -- "Coroutine yield: 1"
coroutine.resume(co) -- "Coroutine yield: 2"
```

## Common Patterns

### Object-Oriented Class via Metatables

**Problem**: Lua lacks a native `class` keyword; object models must be built from first principles.

**Solution**:
Use metatables with the `__index` metamethod:

```lua
local Vector2 = {}
Vector2.__index = Vector2

function Vector2.new(x, y)
    local self = setmetatable({}, Vector2)
    self.x = x or 0
    self.y = y or 0
    return self
end

function Vector2:magnitude()
    return math.sqrt(self.x * self.x + self.y * self.y)
end

local v = Vector2.new(3, 4)
print("Magnitude:", v:magnitude()) -- Output: 5
```

## Best Practices (2026)

**Do**:

- **Always Declare Variables as `local`**: Global variables by default pollute `_G` and degrade performance; use `local var = ...`.
- **Remember Lua Arrays are 1-Indexed**: Arrays start at index `1`, not `0`.
- **Use LuaJIT where Supported**: Leverage the LuaJIT compiler for near C-speed execution in OpenResty and games.
- **Cache Global Function Lookups**: Localize hot functions (`local sub = string.sub`) in tight loops to eliminate global table lookups.

**Don't**:

- **Don't store `nil` values in arrays**: Storing `nil` inside sequential tables breaks length operator (`#`) calculations.
- **Don't create circular metatable references**: Infinite recursion during index lookups causes stack overflow errors.
- **Don't concatenate strings repeatedly in loops**: Use `table.insert` and `table.concat` to avoid O(N^2) memory reallocations.

## Troubleshooting

| Error                                                           | Cause                                                           | Solution                                                                  |
| :-------------------------------------------------------------- | :-------------------------------------------------------------- | :------------------------------------------------------------------------ |
| `attempt to index a nil value`                                  | Accessing key on a variable that evaluated to `nil`.            | Guard access with `if tbl and tbl.key then` or assign default table `{}`. |
| `attempt to call a nil value (method call with . instead of :)` | Calling method with `v.magnitude()` instead of `v:magnitude()`. | Use colon syntax `:` to automatically pass `self` as the first argument.  |
| `1-based indexing confusion`                                    | Treating first index in Lua array tables as `0`.                | Access first element with `tbl[1]` and iterate with `ipairs`.             |

## References

- [Lua 5.4 Reference Manual](https://www.lua.org/manual/5.4/)
