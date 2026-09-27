---
name: objective-c
description: Expert Objective-C assistance covering message passing, runtime dynamic method resolution, ARC, and Foundation/Cocoa. Use when maintaining Apple legacy codebases, developing native iOS/macOS frameworks, or C++ interop.
---

# Objective-C

Objective-C is in **maintenance mode**. New features are rare, but it powers the Apple ecosystem's foundation. It allows mixing C++ (`.mm`) loosely.

## When to Use

- **Legacy iOS and macOS Codebase Maintenance**: Maintaining established Apple applications built before Swift.
- **C/C++ and Swift Bridging (Objective-C++)**: Acting as a high-performance interoperability bridge between native C++ engines and modern Swift.
- **Dynamic Runtime Introspection**: Leveraging the dynamic Objective-C runtime for method swizzling and dynamic message forwarding.
- **High-Performance Audio & Core Audio Frameworks**: Interfacing with low-level Apple media frameworks where C pointer interop is required.

## Quick Start

```objc
#import <Foundation/Foundation.h>

@interface Person : NSObject
@property (nonatomic, copy) NSString *name;
@property (nonatomic, assign) NSInteger age;
- (void)sayHello;
@end

@implementation Person
- (void)sayHello {
    NSLog(@"Hello, my name is %@", self.name);
}
@end
```

## Core Concepts

#Dynamic Message Passing (`[receiver message]`)

Method calls in Objective-C are dynamic messages resolved at runtime via `objc_msgSend`:

```objc
#import <Foundation/Foundation.h>

@interface OrderService : NSObject
- (BOOL)processPayment:(double)amount forCustomer:(NSString *)customer;
@end

@implementation OrderService
- (BOOL)processPayment:(double)amount forCustomer:(NSString *)customer {
    NSLog(@"Charging %@: $%.2f", customer, amount);
    return amount > 0.0;
}
@end

// Invocation syntax
OrderService *service = [[OrderService alloc] init];
[service processPayment:150.0 forCustomer:@"Alice"];
```

#Automatic Reference Counting (ARC) & Nullability Annotations

Manages object memory automatically at compile time with strong/weak ownership semantics:

```objc
@property (nonatomic, strong) NSString *accountNumber;
@property (nonatomic, weak) id<OrderDelegate> delegate; // Prevents retain cycles
@property (nonatomic, copy) void (^completionHandler)(BOOL success);
```

#Objective-C++ (`.mm`) Bridging

Seamlessly mixes C++ standard library types with Cocoa objects in the same file:

```objc
// ProcessorBridge.mm (Objective-C++)
#include <vector>
#import "ProcessorBridge.h"

@implementation ProcessorBridge {
    std::vector<double> _signalBuffer;
}
- (void)addSample:(double)sample {
    _signalBuffer.push_back(sample);
}
@end
```

## Common Patterns

### Safe Block Self-Capture to Prevent Retain Cycles

**Problem**: Strong reference cycles in asynchronous blocks cause permanent memory leaks under ARC.

**Solution**:
Use the `weakSelf / strongSelf` dance in completion blocks:

```objc
__weak typeof(self) weakSelf = self;
[self.networkClient fetchProfileWithCompletion:^(NSDictionary *data) {
    __strong typeof(weakSelf) strongSelf = weakSelf;
    if (!strongSelf) return;
    [strongSelf updateUIWithData:data];
}];
```

## Best Practices (2026)

**Do**:

- **Add Nullability Annotations (`_Nonnull`, `_Nullable`)**: Ensure smooth, idiomatic bridging into modern Swift codebases.
- **Use Weak References for Delegates**: Mark all delegate properties as `weak` to eliminate memory retain cycles.
- **Use Objective-C Generics**: Parameterize collections (`NSArray<NSString *> *`) for compile-time type safety.
- **Wrap Bridged Code with Modern Swift Interfaces**: Plan incremental migrations by creating Swift wrapper classes.

**Don't**:

- **Don't start new greenfield Apple applications in Objective-C**: Build all new iOS/macOS applications in Swift and SwiftUI.
- **Don't invoke methods on deallocated objects without weak-strong dancing**: Use `__weak typeof(self) weakSelf = self;` in asynchronous blocks.
- **Don't use manual retain/release (MRR)**: Ensure modern ARC (`-fobjc-arc`) is enabled across all targets.

## Troubleshooting

| Error                                          | Cause                                                      | Solution                                                                                             |
| :--------------------------------------------- | :--------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| `unrecognized selector sent to instance ...`   | Invoking a method not implemented by the receiving object. | Verify method name and colons (e.g. `doAction:` vs `doAction`), or check with `respondsToSelector:`. |
| `EXC_BAD_ACCESS (code=1, address=...)`         | Dereferencing deallocated memory or zombie object.         | Enable Zombie Objects in Xcode scheme diagnostics to locate deallocated reference.                   |
| `Property with 'copy' attribute is not copied` | Custom setter failed to call `[newValue copy]`.            | Implement custom setters using `_prop = [newValue copy];`.                                           |

## References

- [Apple Developer Documentation](https://developer.apple.com/)
