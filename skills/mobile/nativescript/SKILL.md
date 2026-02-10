---
name: nativescript
description: NativeScript native mobile with JS. Use for native mobile.
---

# NativeScript

NativeScript allows you to write native mobile apps using JavaScript/TypeScript, Angular, Vue, or Svelte. Unlike hybrid apps (WebView), it renders **native UI components** and provides **direct access** to all iOS and Android APIs without boilerplate wrappers.

## When to Use

- You need 100% native performance and API access but want to share logic in JS/TS.
- You want to use Angular or Vue architecture for mobile.
- You need to access a new native API (e.g., latest iOS SDK) immediately without waiting for a plugin wrapper.

## Quick Start

```bash
npm install -g nativescript
ns create my-app
# Choose flavor: Angular, Vue, React, Svelte, or TypeScript
cd my-app
ns run android
```

```typescript
// Accessing Native APIs directly (Android)
const time = new android.text.format.Time();
time.setToNow();
console.log(time.format("%d.%m.%Y"));
```

## Core Concepts

### Runtime Marshalling

The V8 (Android) and JavaScriptCore (iOS) engines are modified to inject native APIs into the JS global scope.

- `new android.widget.Button(context)` creates a real Android Button.
- `UILabel.alloc().init()` creates a real iOS Label.

### Layouts

NativeScript uses its own layout system that maps to native structures.

- `StackLayout`, `GridLayout`, `FlexboxLayout`.

### Plugins

While you _can_ call native APIs directly, plugins are used to simplify complex tasks (Camera, Map) and provide a unified JS API.

## Best Practices

**Do**:

- Use **TypeScript** strictly. Direct native access without types is error-prone.
- Offload heavy CPU tasks to **Worker Threads** (JS runs on the main UI thread).
- Use `Webpack` optimizations provided by the CLI.

**Don't**:

- Don't block the main thread.
- Don't assume CSS works exactly like the web (it's a subset/mapping).

## Troubleshooting

| Error               | Cause                                     | Solution                                                     |
| :------------------ | :---------------------------------------- | :----------------------------------------------------------- |
| `Marshalling Error` | Passing wrong type to native interaction. | Check native docs and cast types if needed.                  |
| `Out of Memory`     | Large images or memory leaks.             | Use `image-cache-it` or proper GC disposal management.       |
| `Build Failed`      | Native dependency issues.                 | `ns clean`, remove `platforms/` and `node_modules/`, re-run. |

## References

- [NativeScript Docs](https://docs.nativescript.org/)
- [NativeScript Plugins](https://market.nativescript.org/)
