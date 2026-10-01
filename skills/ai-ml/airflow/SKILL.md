---
name: airflow
description: Expert Apache Airflow assistance covering DAG authoring, TaskFlow API (@task), operators, sensors, and Celery/Kubernetes executors. Use when orchestrating complex data engineering and ML pipelines.
---

# Airflow

Apache Airflow is the industry standard for programmatic data pipeline orchestration, featuring dynamic DAG generation, event-driven triggers, and robust task scheduling.

## When to Use

- **Enterprise Data Pipeline Orchestration**: Scheduling, monitoring, and authoring complex DAGs across cloud and on-premise systems.
- **Modern TaskFlow API Workloads**: Writing clean, Pythonic DAGs using `@task` and `@dag` decorators with automated XCom serialization.
- **Dynamic Task Mapping**: Fan-out and fan-in workflows processing variable numbers of files, partitions, or microservices.
- **Event-Driven & Deferrable Operators**: Minimizing worker slot utilization during long-running external jobs with async triggers.

## Quick Start

```python
from datetime import datetime
from airflow.decorators import dag, task

@dag(
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["pipeline"]
)
def etl_pipeline():
    @task
    def extract() -> list[dict]:
        return [{"id": 1, "val": 100}, {"id": 2, "val": 200}]

    @task
    def transform(data: list[dict]) -> list[dict]:
        return [{**d, "val": d["val"] * 2} for d in data]

    @task
    def load(data: list[dict]):
        print(f"Loaded {len(data)} transformed records.")

    raw = extract()
    transformed = transform(raw)
    load(transformed)

etl_pipeline()
```

## Core Concepts

### TaskFlow API & Functional DAG Authoring

Pythonic DAG definition with automatic XCom data passing:

```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task

default_args = {
    'owner': 'data-platform',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='customer_metrics_pipeline',
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['analytics', 'production']
)
def customer_metrics_dag():

    @task
    def extract_raw_records() -> list[dict]:
        return [
            {'user_id': 101, 'spend': 120.50},
            {'user_id': 102, 'spend': 450.00},
            {'user_id': 103, 'spend': 89.20},
        ]

    @task
    def compute_summary(records: list[dict]) -> dict:
        total = sum(r['spend'] for r in records)
        count = len(records)
        return {'total_spend': total, 'avg_spend': total / count, 'count': count}

    @task
    def publish_metrics(summary: dict):
        print(f"Published KPI: Total=${summary['total_spend']}, Avg=${summary['avg_spend']:.2f}")

    raw = extract_raw_records()
    summary = compute_summary(raw)
    publish_metrics(summary)

customer_pipeline = customer_metrics_dag()
```

### Dynamic Task Mapping with expand()

Fanning out tasks concurrently based on upstream output:

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(start_date=datetime(2026, 1, 1), schedule=None, catchup=False)
def dynamic_fanout_dag():

    @task
    def get_file_partitions() -> list[str]:
        return ['part-001.parquet', 'part-002.parquet', 'part-003.parquet']

    @task
    def process_file(partition_name: str) -> int:
        print(f"Processing partition: {partition_name}")
        return len(partition_name)

    @task
    def aggregate_results(counts: list[int]):
        print(f"Total processed characters: {sum(counts)}")

    files = get_file_partitions()
    # expand() spawns dynamic worker tasks per element
    processed = process_file.expand(partition_name=files)
    aggregate_results(processed)

fanout_dag = dynamic_fanout_dag()
```

### Deferrable Operators for Efficient Resource Utilization

Freeing worker slots while awaiting remote cluster jobs:

```python
from airflow.sensors.base import BaseSensorOperator
from airflow.triggers.temporal import TimeDeltaTrigger
from datetime import timedelta

# Example pattern using deferrable trigger
# Releases the worker slot to the triggerer service
class CustomAsyncClusterSensor(BaseSensorOperator):
    def execute(self, context):
        self.defer(
            trigger=TimeDeltaTrigger(timedelta(minutes=10)),
            method_name='execute_complete'
        )

    def execute_complete(self, context, event=None):
        self.log.info("Cluster job completed successfully!")
```

## Common Patterns

### Dynamic Task Mapping with Expanding

**Problem**: Processing a variable number of partition files without hardcoding task instances.

**Solution**:
Use `.expand()` on TaskFlow tasks:

```python
@task
def get_files():
    return ["file_a.csv", "file_b.csv", "file_c.csv"]

@task
def process_file(filename: str):
    print(f"Processing {filename}")

files = get_files()
process_file.expand(filename=files)
```

## Best Practices

**Do**:

- Write new DAGs using the TaskFlow API (`@task`, `@dag`) instead of legacy PythonOperator boilerplate.
- Set `catchup=False` on DAGs unless historically backfilling missing time intervals intentionally.
- Use Deferrable Operators and Sensors to prevent worker slot exhaustion during long external waits.
- Test DAGs for parse errors and syntax issues in CI using `pytest` and `dag.test()`.

**Don't**:

- Perform heavy compute or database queries in top-level DAG script code; execute them only inside tasks.
- Store large binary payloads or massive DataFrames in XCom; store metadata/S3 pointers instead.
- Hardcode credentials in DAG files; use Airflow Connections and Secrets Backends (HashiCorp Vault, AWS Secrets Manager).

## Troubleshooting

| Error                                       | Cause                                                                       | Solution                                                                |
| :------------------------------------------ | :-------------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `DagBag parsing timeout (DAG taking > 30s)` | Heavy imports, database queries, or network calls at top level of DAG file. | Move heavy imports and I/O operations inside task functions.            |
| `Task marked as failed without error log`   | Airflow worker process killed by OOM killer or host shutdown.               | Increase worker container memory limits or use `KubernetesPodOperator`. |
| `XCom payload size limit exceeded`          | Passing massive dataframes (>48KB in SQLite/MySQL) between tasks via XCom.  | Store data in S3/GCS object storage and pass only URI paths via XCom.   |

## References

- [Airflow Documentation](https://airflow.apache.org/)
