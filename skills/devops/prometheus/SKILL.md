---
name: prometheus
description: Prometheus monitoring and alerting with PromQL. Use for metrics collection.
---

# Prometheus

Prometheus is the cloud-native standard for metric collection. Prometheus 3.0 (2025) features a modern UI, Native Histograms, and direct OpenTelemetry (OTLP) ingestion.

## When to Use

- **Kubernetes**: Standard monitoring stack (Prometheus Operator).
- **White-box Monitoring**: Measuring internal state (heap usage, request count) via endpoints.
- **Alerting**: Alertmanager handles de-duplication and routing to Slack/PagerDuty.

## Quick Start

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "node"
    static_configs:
      - targets: ["localhost:9100"]
```

## Core Concepts

### Time Series Format

Metrics are identified by name and label pairs.
`http_requests_total{method="POST", handler="/api"}`

### PromQL

Powerful query language.
`rate(http_requests_total[5m])`

### Pull Model

Prometheus scrapes targets. Apps do not push to Prometheus (usually).

## Best Practices (2025)

**Do**:

- **Use High-Cardinality wisely**: Native Histograms in v3.0 help, but keep labels bounded.
- **Use Service Monitors**: In K8s, use the Operator's `ServiceMonitor` CRD instead of manual config.
- **Use OTLP**: Ingest OTel metrics directly if you are transitioning standards.

**Don't**:

- **Don't use for logs**: It is for metrics only. Use Loki for logs.

## References

- [Prometheus Documentation](https://prometheus.io/)
