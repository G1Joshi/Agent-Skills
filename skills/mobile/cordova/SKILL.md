---
name: cordova
description: Apache Cordova hybrid mobile framework. Use for hybrid apps.
---

# Cordova

Apache Cordova (formerly PhoneGap) wraps HTML/CSS/JS apps in a native WebView container. While largely superseded by Capacitor and React Native, it remains active (CLI 13.x) for specific legacy use cases.

## When to Use

- Maintaining long-standing legacy hybrid applications.
- Need an extremely thin wrapper around a pure web app with minimal native plugin interaction.
- **Recommendation**: New projects should use **Capacitor** (which is backward compatible with many Cordova plugins).

## Quick Start

```bash
npm install -g cordova
cordova create hello com.example.hello HelloWorld
cd hello
cordova platform add android
cordova platform add ios
cordova run android
```

## Core Concepts

### Deviceready Event

The most critical event. You cannot call any native plugins until this fires.

```javascript
document.addEventListener("deviceready", onDeviceReady, false);
function onDeviceReady() {
  console.log("Running cordova-" + cordova.platformId);
}
```

### config.xml

The central configuration file for build settings, permissions, and plugin declarations.

### Plugins

Interfaces to native code.

- `cordova-plugin-camera`, `cordova-plugin-device`, etc.

## Common Patterns

### Migration to Capacitor

Many teams use Capacitor as a drop-in replacement runner for Cordova apps to modernize the buildstack while keeping the frontend code.

```bash
npm install @capacitor/cli @capacitor/core
npx cap init
# Capacitor automatically reads config.xml and supports most Cordova plugins
```

## Best Practices

**Do**:

- Use **Capacitor** if possible, even for Cordova projects.
- Keep the `www` folder stateless (build artifacts).
- Use `Content-Security-Policy` meta tags strictly to prevent XSS.

**Don't**:

- Don't edit `platforms/` directory directly (it gets overwritten).
- Don't assume WebView performance matches native; optimize DOM manipulation.

## Troubleshooting

| Error                    | Cause                                        | Solution                                                      |
| :----------------------- | :------------------------------------------- | :------------------------------------------------------------ |
| `deviceready not firing` | JS error before event or missing cordova.js. | Check console; ensure `cordova.js` is included in index.html. |
| `White Screen`           | CSP blocking scripts or syntax error.        | Check `Content-Security-Policy` and remote debugging.         |
| `Gradle build failed`    | Java/Gradle version mismatch.                | Check `cordova requirements android` output.                  |

## References

- [Apache Cordova Docs](https://cordova.apache.org/docs/en/latest/)
- [Migrating from Cordova to Capacitor](https://capacitorjs.com/docs/cordova/migrating)
