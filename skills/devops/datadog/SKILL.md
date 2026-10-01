---
name: datadog
description: Expert Datadog monitoring assistance covering APM tracing, custom metrics, log collection, dashboards, and monitors. Use when instrumenting production infrastructure and observability.
---

# Datadog

Datadog is a unified SaaS observability and security platform providing full-stack APM tracing, infrastructure monitoring, log aggregation, and real-time anomaly detection.

## When to Use

- **Enterprise Full-Stack Observability**: Unified APM tracing, infrastructure metrics, log aggregation, and real-user monitoring (RUM).
- **Distributed Microservice Tracing (APM)**: Visualizing request flow, latency bottlenecks, and database query timings across services.
- **Automated Anomaly Detection & Alerting**: Machine learning-powered alert monitors detecting traffic spikes, errors, and memory leaks.
- **Cloud Cost & Security Posture Management**: Tracking cloud resource misconfigurations, compliance, and container security.

## Quick Start

### 1. Install Datadog Agent (Linux/macOS)

```bash
DD_API_KEY="<YOUR_DATADOG_API_KEY>" DD_SITE="datadoghq.com" \
  bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
```

### 2. Auto-Instrument Node.js Application

```bash
npm install dd-trace --save
```

```javascript
// At the absolute top of your entrypoint file (index.js)
import tracer from "dd-trace";
tracer.init({
  service: "order-service",
  env: "production",
  logInjection: true,
  runtimeMetrics: true,
});
```

## Core Concepts

### Auto-Instrumenting Applications with dd-trace

Adding distributed tracing to a Node.js microservice:

```javascript
// Must be initialized before any other module imports!
import tracer from "dd-trace";

tracer.init({
  env: "production",
  service: "order-processing-service",
  version: "2026.1.0",
  logInjection: true, // Automatically inject trace IDs into logs
  runtimeMetrics: true, // Collect GC and event loop latency metrics
});

export default tracer;
```

### Custom Business Metrics & StatsD

Submitting custom business KPIs with high performance over UDP:

```python
from datadog import initialize, statsd

initialize(statsd_host="127.0.0.1", statsd_port=8125)

# Increment transaction counter with tags
statsd.increment(
    'ecommerce.checkout.success',
    tags=['payment_method:apple_pay', 'region:us_east']
)

# Record latency histogram
statsd.histogram(
    'ecommerce.checkout.duration_ms',
    value=245.5,
    tags=['tier:premium']
)
```

### Correlating Logs with Distributed Traces

Formatting structured logs with active Datadog trace context:

```json
{
  "timestamp": "2026-03-27T10:15:30.123Z",
  "level": "error",
  "message": "Payment authorization timed out with gateway",
  "dd": {
    "trace_id": "847291038472918374",
    "span_id": "1928374650192834",
    "service": "order-processing-service",
    "version": "2026.1.0",
    "env": "production"
  }
}
```

## Common Patterns

### Distributed APM Tracing with Custom Spans

**Problem**: Pinpointing exact latency bottlenecks within deeply nested asynchronous service methods.

**Solution**:
Wrap business logic in custom Datadog tracer spans:

```javascript
import tracer from "dd-trace";
tracer.init(); // Initialize tracer before importing other packages

async function processOrder(orderId) {
  return tracer.trace(
    "order.process",
    { resource: "checkout" },
    async (span) => {
      span.setTag("order.id", orderId);

      const inventory = await checkInventory(orderId);
      span.setTag("inventory.status", inventory.status);

      const charge = await chargeCard(orderId);
      return { inventory, charge };
    },
  );
}
```

## Best Practices

**Do**:

- Enforce Unified Service Tagging across all systems: `env`, `service`, and `version` tags must match everywhere.
- Enable `logInjection: true` in APM tracers to link logs and traces together automatically in the UI.
- Use DogStatsD over local UDP to submit high-frequency metrics without blocking application request threads.
- Configure log sampling and exclusion filters in `datadog.yaml` to control ingestion costs.

**Don't**:

- Initialize APM tracers after importing HTTP or database modules; tracer must load first to patch libraries.
- Emit high-cardinality tags (e.g. user IDs, order UUIDs, timestamps) as custom metric tag dimensions; use logs/spans.
- Log sensitive PII or credentials; configure Datadog log scrub rules (`log_processing_rules`).

## Troubleshooting

| Error                                                   | Cause                                                                        | Solution                                                                                         |
| :------------------------------------------------------ | :--------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------- |
| `Datadog Agent: API Key invalid`                        | `DD_API_KEY` contains typo or belongs to wrong Datadog site (e.g. EU vs US). | Verify API key and ensure `DD_SITE` is configured correctly (`datadoghq.com` vs `datadoghq.eu`). |
| `Traces not showing in APM dashboard`                   | Application tracer unable to reach Datadog agent on port 8126.               | Set `DD_AGENT_HOST=127.0.0.1` and verify agent container port mapping.                           |
| `Too many metrics: Custom metric cardinality explosion` | Using dynamic UUIDs or timestamps as custom metric tag values.               | Move high-cardinality values from metric tags to log attributes.                                 |

## References

- [Datadog Documentation](https://docs.datadoghq.com/)
