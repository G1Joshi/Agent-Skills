---
name: grafana
description: Expert Grafana assistance covering dashboards, PromQL/LogQL panels, alerting rules, data sources, and Grafana Loki/Tempo. Use when visualizing system metrics, application logs, and building monitoring dashboards.
---

# Grafana

Grafana is an open-source analytics and interactive visualization web application, providing flexible dashboarding, Scenes composability, and unified correlation across metrics, logs, and distributed traces.

## When to Use

- **Unified Observability Dashboards**: Visualizing time-series metrics from Prometheus, Datadog, CloudWatch, and InfluxDB.
- **Log Exploration with Grafana Loki**: Querying streaming logs using LogQL with zero-indexing overhead.
- **Distributed Trace Visualization with Grafana Tempo**: Inspecting traces, span latencies, and service dependency graphs.
- **Alerting & Incident Management**: Routing alerts via Grafana Alerting to PagerDuty, Slack, OpsGenie, and Webhooks.

## Quick Start

Run via Docker:
`docker run -d -p 3000:3000 grafana/grafana`

Or Provision as Code (YAML):

```yaml
apiVersion: 1
providers:
  - name: "default"
    folder: ""
    type: file
    options:
      path: /var/lib/grafana/dashboards
```

## Core Concepts

### Prometheus Metrics Visualization with PromQL

Configuring time-series queries for dashboard panels:

```promql
# Rate of HTTP 5xx errors per second across microservices
sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)

# 99th percentile request latency in seconds
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))

# CPU Utilization percentage per container
sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (pod) * 100
```

### Log Exploration with LogQL (Grafana Loki)

Filtering and parsing streaming application logs:

```logql
# Filter production API logs for errors and extract JSON fields
{env="production", service="billing"}
  |= "error"
  | json
  | latency_ms > 500
  | line_format "[{{.status}}] {{.error_message}} ({{.latency_ms}}ms)"
```

### Declarative Dashboard as Code (JSON Model)

Managing dashboard definitions in Git for automated provisioning:

```json
{
  "title": "Platform Health KPI",
  "panels": [
    {
      "id": 1,
      "title": "API Request Rate (req/s)",
      "type": "timeseries",
      "datasource": { "type": "prometheus", "uid": "prom-primary" },
      "targets": [
        {
          "expr": "sum(rate(http_requests_total[2m]))",
          "legendFormat": "Total Requests"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "reqps",
          "color": { "mode": "palette-classic" }
        }
      }
    }
  ]
}
```

## Common Patterns

### Dynamic Dashboard Variables with PromQL Label Values

**Problem**: Creating separate dashboard panels for every server instance or Kubernetes pod.

**Solution**:
Define template variables with dynamic queries:

```text
# Dashboard Variable: $instance
Query: label_values(node_cpu_seconds_total, instance)

# PromQL panel query utilizing variable:
sum(rate(node_cpu_seconds_total{mode!="idle", instance=~"$instance"}[5m]))
  by (instance) * 100
```

## Best Practices

**Do**:

- Provision dashboards and datasources declaratively using Grafana Provisioning (`/etc/grafana/provisioning`).
- Use Dashboard Template Variables (`$service`, `$environment`) to create dynamic, reusable panels.
- Set standard units (`reqps`, `bytes`, `seconds`, `percent`) on panel field configs for human-readable axes.
- Correlate metrics, logs, and traces using Grafana Explore cross-linking (Data Links).

**Don't**:

- Write high-cardinality PromQL queries that query raw unaggregated metrics over long timeframes (e.g. 30 days).
- Edit production dashboards directly in the UI without exporting and committing the JSON model to Git.
- Configure un-muted alerts that spam communication channels; group alerts by symptom and severity.

## Troubleshooting

| Error                                              | Cause                                                                      | Solution                                                                 |
| :------------------------------------------------- | :------------------------------------------------------------------------- | :----------------------------------------------------------------------- |
| `Data source connection failed: Bad Gateway (502)` | Grafana cannot reach Prometheus or database endpoint URL.                  | Verify internal network URL (e.g. `http://prometheus:9090`).             |
| `Panel showing 'No Data'`                          | Query filter labels do not match incoming metrics, or time range is empty. | Expand time range to "Last 24 hours" and test query in Explore view.     |
| `Alerting rule constantly flapping`                | Alert threshold evaluated without duration window.                         | Set evaluation interval: `for: 5m` before triggering alert notification. |

## References

- [Grafana Documentation](https://grafana.com/docs/)
