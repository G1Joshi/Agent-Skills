---
name: sentry
description: Expert Sentry error monitoring assistance covering exception tracking, performance tracing, source maps, releases, and breadcrumbs. Use when monitoring production errors and diagnosing stack traces.
---

# Sentry

Sentry provides real-time application performance monitoring, distributed tracing, and code-level error diagnostics across frontend, backend, and mobile stacks.

## When to Use

- **Real-Time Application Error Monitoring**: Capturing unhandled exceptions, stack traces, and runtime errors in production.
- **End-to-End Performance Tracing**: Measuring transaction durations, database queries, and distributed trace spans.
- **Source Map Processing & De-Minification**: Translating minified production bundle errors back to original TypeScript source lines.
- **Session Replay & User Crash Feedback**: Watching user sessions to reproduce difficult-to-catch client-side bugs.

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

### Node.js / Next.js SDK Initialization with Performance Tracing

Instrumenting application with trace sampling and error capture:

```typescript
import * as Sentry from "@sentry/node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV || "production",
  release: "api-service@2026.1.0",
  tracesSampleRate: 0.1, // Sample 10% of transactions for performance metrics

  // Filter sensitive data before transmitting to Sentry
  beforeSend(event, hint) {
    if (event.request?.headers) {
      delete event.request.headers["authorization"];
      delete event.request.headers["cookie"];
    }
    return event;
  },
});
```

### Manual Error Capture with Custom Context

Enriching errors with user context and custom tags:

```typescript
import * as Sentry from "@sentry/node";

async function processPayment(userId: string, amountCents: number) {
  try {
    // Simulated payment logic
    throw new Error("Payment gateway rejected authorization token");
  } catch (error) {
    Sentry.withScope((scope) => {
      scope.setUser({ id: userId });
      scope.setTag("payment.provider", "stripe");
      scope.setExtra("amount_cents", amountCents);
      scope.setLevel("error");

      Sentry.captureException(error);
    });
    throw error;
  }
}
```

### Custom Performance Spans

Measuring execution duration of critical code blocks:

```typescript
import * as Sentry from "@sentry/node";

async function calculateRiskScore(orderId: string): Promise<number> {
  return await Sentry.startSpan(
    { name: "calculateRiskScore", op: "fraud.evaluation" },
    async (span) => {
      span.setAttribute("order_id", orderId);
      // Run intensive risk calculation
      return 0.95;
    },
  );
}
```

## Common Patterns

### Node.js / Express Error Middleware with User Context

**Problem**: Production exceptions logged without user session context or breadcrumb history.

**Solution**:
Configure Sentry tracing and request isolation:

```javascript
import * as Sentry from "@sentry/node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.2, // Capture 20% of transactions
  environment: process.env.NODE_ENV,
});

// Attach user context in auth middleware
app.use((req, res, next) => {
  if (req.user) {
    Sentry.setUser({ id: req.user.id, email: req.user.email });
  }
  next();
});

// Sentry error handler must be before any other error middleware
Sentry.setupExpressErrorHandler(app);
```

## Best Practices

**Do**:

- Configure `release` tags to correlate error occurrences with specific Git commits and deployments.
- Upload source maps during CI/CD using `@sentry/cli` to get clear TypeScript line numbers in stack traces.
- Sanitize sensitive PII, credit card numbers, and authorization headers in `beforeSend`.
- Tune `tracesSampleRate` in high-throughput environments to prevent excessive ingestion costs.

**Don't**:

- Leave DSN keys exposed in public repositories without domain restriction rules.
- Catch exceptions silently without logging or passing to `Sentry.captureException()`.
- Log high-frequency expected user validation errors (e.g. invalid form fields) as Sentry exceptions.

## Troubleshooting

| Error                                     | Cause                                                                      | Solution                                                                           |
| :---------------------------------------- | :------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- |
| `Source maps not showing in stack traces` | Source maps not uploaded during build or release version mismatch.         | Upload source maps via `@sentry/webpack-plugin` with identical `release` tag.      |
| `Sentry DSN not capturing events`         | DSN variable missing in production runtime or rate limit exceeded.         | Verify `SENTRY_DSN` is set and inspect Sentry Organization Stats for quota spikes. |
| `Transactions flooded / quota exhausted`  | `tracesSampleRate` set to 1.0 (100%) on high-traffic production endpoints. | Reduce `tracesSampleRate` to 0.05 - 0.2 (5% - 20%).                                |

## References

- [Sentry Documentation](https://docs.sentry.io/)
