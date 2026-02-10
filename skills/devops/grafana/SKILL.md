---
name: grafana
description: Grafana dashboards and visualization for metrics. Use for observability.
---

# Grafana

Grafana is the visualization layer for Observability. Grafana 11 (2025) introduces **Scenes** (dynamic dashboards) and deeper correlation between Metrics, Logs, and Traces.

## When to Use

- **Dashboards**: Visualize data from Prometheus, InfluxDB, CloudWatch, SQL, etc.
- **Single Pane of Glass**: Combine metrics (Prometheus), logs (Loki), and traces (Tempo) in one UI.
- **Alerting**: Unified alerting UI regardless of the data source.

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

### Data Sources

Plugins that connect to storage backends.

### Panels

Individual visualizations (Time Series, Gauge, Bar Chart).

### Variables

Dropdowns at the top of dashboards (e.g., Select `Cluster` or `Namespace`) to make dashboards dynamic.

## Best Practices (2025)

**Do**:

- **Provision as Code**: Store dashboards as JSON files in Git.
- **Use Explore metrics**: The new v11 UI for ad-hoc querying.
- **Standardize Labels**: Ensure "env" and "service" labels match across Metrics and Logs for seamless correlation links.

**Don't**:

- **Don't hardcode queries**: Use Variables so one dashboard serves all environments.

## References

- [Grafana Documentation](https://grafana.com/docs/)
