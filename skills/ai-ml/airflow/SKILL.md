---
name: airflow
description: Apache Airflow workflow orchestration. Use for data pipelines.
---

# Airflow

Apache Airflow is the standard for data engineering pipelines. v3.0 (2025) introduces **Event-driven Triggers** and a modern React UI.

## When to Use

- **ETL/ELT**: Scheduling nightly data warehouse loads.
- **ML Ops**: Retraining models when new data arrives.
- **Dependency Management**: "Run Task B only if Task A succeeds".

## Core Concepts

### DAGs (Directed Acyclic Graphs)

Defined in Python.

### Task SDK

New in v3.0. Allows writing tasks in any language, not just Python.

### Edge Executor

Run tasks on remote edge devices.

## Best Practices (2025)

**Do**:

- **Use the TaskFlow API**: `@task` decorators are cleaner than `PythonOperator`.
- **Use Datasets**: Define data-aware scheduling (`schedule=[Dataset("s3://bucket/file")]`).

**Don't**:

- **Don't put top-level code in DAG files**: It runs every scheduler heartbeat.

## References

- [Airflow Documentation](https://airflow.apache.org/)
