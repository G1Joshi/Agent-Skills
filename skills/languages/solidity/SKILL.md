---
name: solidity
description: Expert Solidity smart contract assistance covering EVM, OpenZeppelin, ERC-20/721/1155, and reentrancy guards. Use when developing Ethereum contracts, DeFi protocols, NFT systems, or Web3 dApps.
---

# Solidity

Solidity is an object-oriented, high-level language for implementing smart contracts on the Ethereum Virtual Machine (EVM), featuring strict typing and gas-optimized storage patterns.

## When to Use

- **Ethereum & EVM Smart Contract Development**: Building decentralized protocols on Ethereum, Arbitrum, Optimism, Polygon, and Base.
- **DeFi Financial Protocols**: Automated market makers (AMMs), lending pools, yield aggregators, and staking vaults.
- **Token Standards & Digital Assets**: Implementing ERC-20 fungible tokens, ERC-721/ERC-1155 non-fungible tokens, and ERC-4337 smart accounts.
- **On-Chain Governance & DAOs**: Implementing multisigs, timelocks, and decentralized voting mechanisms.

## Quick Start

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleStorage {
    uint256 private storedData;
    event DataChanged(uint256 newValue);

    function set(uint256 x) public {
        storedData = x;
        emit DataChanged(x);
    }

    function get() public view returns (uint256) {
        return storedData;
    }
}
```

## Core Concepts

### Secure ERC-20 Vault with OpenZeppelin & Custom Errors

Gas-optimized token vault with reentrancy protection and custom error revert reasons:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable2Step.sol";

error ZeroDepositAmount();
error InsufficientBalance(uint256 available, uint256 requested);

contract TokenVault is ReentrancyGuard, Ownable2Step {
    using SafeERC20 for IERC20;

    IERC20 public immutable token;
    mapping(address => uint256) public userBalances;

    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);

    constructor(IERC20 _token) Ownable2Step(msg.sender) {
        token = _token;
    }

    function deposit(uint256 amount) external nonReentrant {
        if (amount == 0) revert ZeroDepositAmount();
        userBalances[msg.sender] += amount;
        token.safeTransferFrom(msg.sender, address(this), amount);
        emit Deposited(msg.sender, amount);
    }

    function withdraw(uint256 amount) external nonReentrant {
        uint256 balance = userBalances[msg.sender];
        if (amount > balance) revert InsufficientBalance(balance, amount);
        userBalances[msg.sender] = balance - amount;
        token.safeTransfer(msg.sender, amount);
        emit Withdrawn(msg.sender, amount);
    }
}
```

### Storage, Memory & Calldata Gas Layout

Understanding the EVM data locations to minimize transaction execution costs:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract StorageLayout {
    // Storage variables packed into 32-byte slots
    struct UserProfile {
        uint128 balance; // slot 0 (16 bytes)
        uint64 lastLogin; // slot 0 (8 bytes)
        uint64 flags;     // slot 0 (8 bytes) - total 32 bytes packed
        address owner;    // slot 1 (20 bytes)
    }

    mapping(uint256 => UserProfile) public profiles;

    // Use 'calldata' for read-only external array arguments to avoid memory copying
    function batchCheckFlags(bytes32[] calldata hashes) external view returns (bool) {
        for (uint256 i = 0; i < hashes.length; ++i) {
            if (hashes[i] == bytes32(0)) return false;
        }
        return true;
    }
}
```

### Checks-Effects-Interactions & Upgradeability (UUPS)

Preventing reentrancy vulnerabilities and managing proxy upgrades:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract VaultV1 is Initializable, OwnableUpgradeable, UUPSUpgradeable {
    uint256 public totalYield;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize(address initialOwner) public initializer {
        __Ownable_init(initialOwner);
        __UUPSUpgradeable_init();
    }

    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}
```

## Common Patterns

### Checks-Effects-Interactions Pattern (Reentrancy Prevention)

**Problem**: External calls made before internal state updates allow recursive reentrancy attacks draining contract funds.

**Solution**:
Update contract state before making external ether transfers:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Vault {
    mapping(address => uint256) public balances;

    function withdraw() external {
        // 1. Checks
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Insufficient balance");

        // 2. Effects
        balances[msg.sender] = 0;

        // 3. Interactions
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

## Best Practices

**Do**:

- Use Solidity `^0.8.24` or higher with native arithmetic overflow protection and custom errors (`error MyError()`) instead of string `require` messages.
- Always adhere to the Checks-Effects-Interactions (CEI) pattern and apply `ReentrancyGuard` to all state-changing transfer functions.
- Test smart contracts rigorously with Foundry (`forge test`, fuzzing, and invariant testing) and formal verification tools.
- Use OpenZeppelin's `SafeERC20` wrapper to prevent silent transfer failures from non-standard ERC-20 tokens.

**Don't**:

- Use `tx.origin` for authorization; always use `msg.sender` to defend against phishing and proxy attacks.
- Rely on `block.timestamp` or `block.number` for random number generation; integrate Chainlink VRF.
- Deploy unverified or unaudited contracts to production mainnets.

## Troubleshooting

| Error                                        | Cause                                                               | Solution                                                                       |
| :------------------------------------------- | :------------------------------------------------------------------ | :----------------------------------------------------------------------------- |
| `Transaction reverted: function call failed` | `require` condition evaluated to false or gas limit exceeded.       | Check revert reason in block explorer or run test with Hardhat/Foundry traces. |
| `Error: Gas estimation failed`               | Transaction will inevitably revert under current contract state.    | Verify caller account permissions, allowance, and input parameters.            |
| `Compiler version mismatch`                  | `pragma solidity` declaration incompatible with local solc version. | Update compiler version in `hardhat.config.js` or `foundry.toml`.              |

## References

- [Solidity Documentation](https://docs.soliditylang.org/)
