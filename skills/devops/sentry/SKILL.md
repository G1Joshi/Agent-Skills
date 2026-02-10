---
name: sentry
description: Sentry error tracking and performance monitoring. Use for error tracking.
---

# Sentry

Sentry provides self-hosted and cloud-based error monitoring. In 2025, it excels at **Performance Monitoring** and identifying **AI Model** hallucinations or errors.

## When to Use

- **Error Tracking**: "My app crashed, what is the stack trace?"
- **Frontend Performance**: Web Vitals monitoring (LCP, FID).
- **Release Tracking**: Associate errors with specific git commits/releases.

## Quick Start

```javascript
import * as Sentry from "@sentry/node";

Sentry.init({
  dsn: "https://examplePublicKey@o0.ingest.sentry.io/0",
  tracesSampleRate: 1.0,
});

try {
  myFunction();
} catch (e) {
  Sentry.captureException(e);
}
```

## Core Concepts

### Issues

Aggregated groups of events. Sentry expects 1000 events of "NullPointerException" to be grouped into 1 Issue.

### Releases

Tying code versions to errors. Sentry can tell you "This error started in Release v3.4".

### Distributed Tracing

Connects frontend errors to backend bottlenecks.

## Best Practices (2025)

**Do**:

- **Upload Source Maps**: Essential for JS/TS debugging.
- **Use `ignoreErrors`**: Filter out noise (like "Network Error" when user is offline) in the SDK config.
- **Use Session Replay**: Video-like reproduction of user actions leading up to an error.

**Don't**:

- **Don't log PII**: Sanitize data before sending. Sentry has scrubbers, but do it client-side too.

## References

- [Sentry Documentation](https://docs.sentry.io/)
