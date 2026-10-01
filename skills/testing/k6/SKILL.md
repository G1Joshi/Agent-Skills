---
name: k6
description: Expert k6 load and performance testing assistance covering virtual users, thresholds, metrics, and scenario scripting. Use when benchmarking APIs, performing stress testing, or integrating load tests into CI/CD.
---

# k6

k6 is a developer-centric, open-source load testing tool suitable for testing APIs, microservices, and websites. It is written in Go but you script tests in JavaScript.

## When to Use

- **Developer-Centric Load Testing**: Writing high-performance load tests in modern JavaScript / TypeScript with CLI execution.
- **CI/CD Performance Regression Gates**: Defining thresholds (`http_req_duration: ['p(95)<200']`) that automatically fail build pipelines on regressions.
- **Spike, Stress & Soak Testing**: Simulating traffic surges, system breaking points, and prolonged sustained load over hours.
- **Cloud Distributed Load Generation**: Running distributed tests across global regions via Grafana Cloud k6.

## Quick Start

```javascript
import http from "k6/http";
import { sleep, check } from "k6";

export const options = {
  vus: 10,
  duration: "30s",
};

export default function () {
  const res = http.get("http://test.k6.io");
  check(res, {
    "status was 200": (r) => r.status == 200,
  });
  sleep(1);
}
```

Run with `k6 run script.js`.

## Core Concepts

### Go-Powered Virtual Users (VUs) with JS Runtimes

Tests are written in JavaScript, but executed by a multi-threaded Go engine with zero NodeJS overhead:

```javascript
// load-test.js
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "30s", target: 50 }, // Ramp up to 50 users
    { duration: "1m", target: 50 }, // Stay at 50 users
    { duration: "20s", target: 0 }, // Ramp down
  ],
  thresholds: {
    http_req_duration: ["p(95)<300"], // 95% of requests must complete below 300ms
    http_req_failed: ["rate<0.01"], // Error rate must be less than 1%
  },
};

export default function () {
  const res = http.get("https://api.staging.example.com/v1/items");
  check(res, {
    "status is 200": (r) => r.status === 200,
    "transaction time OK": (r) => r.timings.duration < 300,
  });
  sleep(1);
}
```

### Custom Metrics (Counters, Gauges, Trends)

Tracks domain-specific operational metrics alongside standard HTTP timings:

```javascript
import { Trend, Counter } from "k6/metrics";

const checkoutLatency = new Trend("checkout_duration");
const completedOrders = new Counter("successful_checkouts");

export default function () {
  const start = Date.now();
  const res = http.post(
    "https://api.example.com/checkout",
    JSON.stringify({ cartId: 415 }),
    {
      headers: { "Content-Type": "application/json" },
    },
  );

  if (res.status === 201) {
    completedOrders.add(1);
    checkoutLatency.add(Date.now() - start);
  }
}
```

### Tagging & Scenarios

Isolates different user behaviors (e.g. 80% readers, 20% writers) in a single test run:

```javascript
export const options = {
  scenarios: {
    readers: {
      executor: "constant-vus",
      vus: 100,
      duration: "5m",
      exec: "browseCatalog",
    },
  },
};
```

## Common Patterns

### Staged Load Test with Strict SLA Thresholds

**Problem**: Performance regressions slip into production when build pipelines lack automated latency gatechecks.

**Solution**:
Define ramp-up stages and SLO thresholds in k6 script options:

```javascript
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "30s", target: 50 },
    { duration: "1m", target: 50 },
    { duration: "20s", target: 0 },
  ],
  thresholds: {
    http_req_duration: ["p(95)<300"],
    http_req_failed: ["rate<0.01"],
  },
};

export default function () {
  const res = http.get("https://test-api.k6.io/public/crocodiles/");
  check(res, { "status is 200": (r) => r.status === 200 });
  sleep(1);
}
```

## Best Practices

**Do**:

- Always Define Explicit `thresholds`: Let CI/CD pipelines fail automatically if latency percentiles or error rates degrade.
- Ramp Virtual Users Incrementally: Avoid instant spikes unless specifically conducting a spike/break test.
- Parameterize Test Data: Feed unique data using `SharedArray` from JSON/CSV files to prevent caching artifacts.
- Export Metrics to Prometheus / InfluxDB: Use `k6 run --out statsd` or Grafana Cloud k6 for real-time visualization.

**Don't**:

- Import heavy NPM packages directly: Use k6-compatible polyfills; k6 does not run inside standard Node.js.
- Print logs inside default test functions: `console.log()` inside virtual user loops degrades test runner performance.
- Omit think time (`sleep`): Zero sleep simulations hammer servers unrealistically and skew load profiles.

## Troubleshooting

| Error                                             | Cause                                                             | Solution                                                                  |
| :------------------------------------------------ | :---------------------------------------------------------------- | :------------------------------------------------------------------------ |
| `dial tcp: lookup ...: no such host`              | DNS resolution failure or target URL incorrect.                   | Verify endpoint connectivity and ensure VPN or internal DNS is reachable. |
| `Threshold failed: p(95)<300 [current: 450ms]`    | Target service latency exceeded predefined performance threshold. | Profile database query latency, server CPU/memory, and caching layers.    |
| `warn: Request Failed: context deadline exceeded` | Target server timing out under load.                              | Increase request timeout in k6 or scale upstream application workers.     |

## References

- [k6 Documentation](https://k6.io/docs/)
