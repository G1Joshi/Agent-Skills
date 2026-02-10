---
name: solidity
description: Solidity smart contract development for Ethereum and EVM chains. Use for .sol files.
---

# Solidity

Solidity is the primary language for the **Ethereum Virtual Machine (EVM)**. v0.8.28 (2025) focuses on transient storage (`tstore`) and gas optimization via IR.

## When to Use

- **Ethereum/L2s**: Developing for Optimism, Arbitrum, Base.
- **DeFi**: Writing logic for tokens, AMMs, and lending.
- **NFTs**: ERC-721 and ERC-1155 contracts.

## Core Concepts

### Gas

Every operation costs ETH. Optimization is critical.

### Modifiers

Reusable checks. `modifier onlyOwner { ... }`.

### Events

Logging on the blockchain. `emit Transfer(from, to, value)`.

## Best Practices (2025)

**Do**:

- **Use Foundry**: The 2025 standard for testing (Solidity-based tests).
- **Use Custom Errors**: `error InsufficientBalance();` is cheaper than string requires.
- **Use OpenZeppelin**: Don't roll your own crypto/auth logic.

**Don't**:

- **Don't ignore reentrancy**: Use `ReentrancyGuard` or Checks-Effects-Interactions pattern.

## References

- [Solidity Documentation](https://docs.soliditylang.org/)
