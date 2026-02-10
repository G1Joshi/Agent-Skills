---
name: datadog
description: Datadog monitoring and APM platform. Use for observability.
---

# Datadog

Datadog is a leading SaaS observability platform. In 2025, it focuses on **AI Observability** (monitoring LLMs) and automated remediation with **Watchdog**.

## When to Use

- **SaaS Convenience**: You want a complete solution (APM, Logs, Infra) without managing storage.
- **Full Stack Visibility**: Frontend RUM (Real User Monitoring) connected to Backend Traces connected to DB Metrics.
- **AI Apps**: Monitor token usage, latency, and costs of LLM calls.

## Quick Start

Install Agent:
`DD_API_KEY=... bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"`

Enable APM (e.g. Node.js):
`DD_TRACE_AGENT_URL=http://localhost:8126 node --require dd-trace/init app.js`

## Core Concepts

### Tags

The most important concept. `env:prod`, `service:login`, `team:core`. Filter everything by tags.

### Watchdog

AI-driven anomaly detection. "Redis latency is 30% higher than normal".

### APM (Application Performance Monitoring)

Automatic instrumentation of code to find slow SQL queries or API calls.

## Best Practices (2025)

**Do**:

- **Tag Everything**: Use `DD_TAGS` to standard metadata across all hosts.
- **Use Sampling**: For high-volume services, sample traces to keep costs down.
- **Set Budgets**: Datadog is expensive. Use cost alerts.

**Don't**:

- **Don't ignore the bill**: Custom Metrics and high-volume logs can spike costs unexpectedly.

## References

- [Datadog Documentation](https://docs.datadoghq.com/)
