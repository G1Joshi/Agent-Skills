---
name: prometheus
description: Expert Prometheus monitoring assistance covering PromQL, metric types (Counter, Gauge, Histogram), scrape configs, and Alertmanager. Use when collecting and querying operational metrics across microservices.
---

# Prometheus

Prometheus is the CNCF graduated monitoring and alerting toolkit, featuring a multi-dimensional data model with time-series metrics, PromQL, and native OpenTelemetry ingestion.

## When to Use

- **Cloud-Native Time-Series Monitoring**: Scraping, storing, and querying numerical metrics from infrastructure and applications.
- **PromQL Quantitative Querying**: Computing request rates, 99th percentile latencies, error ratios, and saturations.
- **Automated Service Discovery**: Dynamically discovering Kubernetes pods, EC2 instances, and Consul nodes to scrape.
- **Alerting Rules & Alertmanager Integration**: Evaluating threshold rules and dispatching alerts to on-call engineers.

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

### Prometheus Scrape Configuration (prometheus.yml)

Configuring scrape jobs with relabeling:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "api-microservices"
    scrape_interval: 10s
    metrics_path: "/metrics"
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: ["production"]
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: "true"
      - source_labels: [__meta_kubernetes_pod_container_port_number]
        action: keep
        regex: "8080"
```

### Production Alerting Rules (alert_rules.yml)

Defining SLO-based alert thresholds:

```yaml
groups:
  - name: API_SLO_Alerts
    rules:
      - alert: HighHttpErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) * 100 > 5
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High HTTP 5xx error rate on {{ $labels.service }}"
          description: 'Service {{ $labels.service }} error rate is {{ $value | printf "%.2f" }}% (> 5% SLO threshold).'
```

### Exposing Custom Metrics in Python

Instrumentation using official Prometheus Python client:

```python
from prometheus_client import start_http_server, Counter, Histogram
import time

REQUEST_COUNTER = Counter(
    'http_requests_total',
    'Total count of HTTP requests processed',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'Histogram of HTTP request latency in seconds',
    ['endpoint'],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
)

@REQUEST_DURATION.labels(endpoint='/api/orders').time()
def process_order():
    time.sleep(0.08)
    REQUEST_COUNTER.labels(method='POST', endpoint='/api/orders', status='200').inc()

# Start metrics endpoint server on port 8000
start_http_server(8000)
```

## Common Patterns

### High-Throughput Scrape Config with Kubernetes Service Discovery

**Problem**: Static IP scraping configurations fail as pods scale dynamically in Kubernetes.

**Solution**:
Use `kubernetes_sd_configs` with metric path annotations:

```yaml
scrape_configs:
  - job_name: "kubernetes-pods"
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels:
          [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
```

## Best Practices

**Do**:

- Adhere strictly to the Four Golden Signals (Latency, Traffic, Errors, Saturation) when building PromQL alert rules.
- Configure appropriate histogram buckets around your service SLO targets (e.g. 100ms, 200ms, 500ms).
- Use recording rules (`record: job:metric:rate5m`) for complex PromQL expressions queried by dashboards.
- Store long-term historical metrics using remote-write storage (Thanos, Cortex, or VictoriaMetrics).

**Don't**:

- Introduce high-cardinality label values (user IDs, email addresses, order IDs) into metric labels.
- Set scrape intervals too low (< 5s) across large fleets; it overloads target scrapers and storage.
- Alert on simple transient spikes; always use `for: 2m` or `for: 5m` to filter temporary noise.

## Troubleshooting

| Error                                        | Cause                                                                             | Solution                                                               |
| :------------------------------------------- | :-------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `Target shows DOWN in Prometheus Targets UI` | Scrape target port firewalled or application metrics path crashing.               | Test target endpoint manually: `curl http://<pod-ip>:<port>/metrics`.  |
| `High memory usage / Prometheus OOM`         | High churn in metric series (high cardinality tags like UUIDs or user emails).    | Audit and drop unbounded labels using `metric_relabel_configs`.        |
| `PromQL: many-to-many matching not allowed`  | Vector matching join (`on(...)`) without `group_left` or `group_right` modifiers. | Add `group_left` or `group_right` to specify many-to-one relationship. |

## References

- [Prometheus Documentation](https://prometheus.io/)
