---
name: dask
description: Expert Dask distributed computing assistance covering Dask DataFrames, Arrays, Futures, and cluster scaling. Use when analyzing datasets too large for pandas on a single machine or multi-node cluster.
---

# Dask

Dask scales Python. It looks like Pandas/NumPy but runs on clusters. 2025 updates focus on **High Performance Shuffle** and GPU integration.

## When to Use

- **Larger-than-Memory Tabular Computation**: Processing 10GB-1TB CSV/Parquet datasets on a single machine or multi-node cluster.
- **Parallelizing Custom Python Workflows**: Using `dask.delayed` to parallelize arbitrary Python loops and task graphs.
- **Distributed Machine Learning**: Integrating with Scikit-learn, XGBoost, and LightGBM across distributed worker nodes.
- **NumPy & Pandas Scaling**: Drop-in familiar APIs for out-of-core array and DataFrame calculations.

## Quick Start

```python
import dask.dataframe as dd

# Read multi-gigabyte partitioned CSV files lazily
df = dd.read_csv('data/transactions_*.csv')

# Compute aggregated statistics in parallel across all CPU cores
result = df.groupby('category').amount.mean().compute()
print(result)
```

## Core Concepts

#Out-of-Core Processing with Dask DataFrame

Loading partitioned Parquet files and computing aggregations lazily:

```python
import dask.dataframe as dd
from dask.distributed import Client

# Initialize local distributed cluster
client = Client(n_workers=4, threads_per_worker=2, memory_limit='4GB')
print(f"Dask Dashboard running at: {client.dashboard_link}")

# Lazy load multi-file dataset
df = dd.read_parquet(
    's3://analytics-bucket/transactions/*.parquet',
    columns=['customer_id', 'amount', 'status', 'country'],
    engine='pyarrow'
)

# Build computational graph lazily
filtered = df[df['status'] == 'completed']
metrics = filtered.groupby('country')['amount'].agg(['mean', 'sum', 'count'])

# Execute graph and return concrete Pandas DataFrame
result_df = metrics.compute()
print(result_df)
```

#Custom Task Graphs with dask.delayed

Parallelizing independent function executions:

```python
from dask import delayed, compute
import time

@delayed
def fetch_api_data(endpoint: str) -> dict:
    time.sleep(0.5) # Simulating I/O
    return {'endpoint': endpoint, 'status': 200, 'items': [1, 2, 3]}

@delayed
def transform_payload(data: dict) -> int:
    return sum(data['items'])

@delayed
def aggregate_totals(totals: list[int]) -> int:
    return sum(totals)

# Construct dependency DAG
endpoints = ['users', 'orders', 'inventory', 'payments']
fetched = [fetch_api_data(ep) for ep in endpoints]
transformed = [transform_payload(f) for f in fetched]
final_total = aggregate_totals(transformed)

# Execute all tasks in parallel across the cluster
total_result = final_total.compute()
print("Grand Total:", total_result)
```

#Dask Array for Distributed Linear Algebra

Manipulating massive multi-dimensional arrays:

```python
import dask.array as da

# Create a 50,000 x 50,000 array split into 5,000 x 5,000 chunks
x = da.random.normal(10, 0.1, size=(50000, 50000), chunks=(5000, 5000))

# Perform calculations lazily
y = x + x.T
z = y[::2, ::2].mean(axis=0)

# Compute result
result = z.compute()
print("Computed array mean shape:", result.shape)
```

## Common Patterns

### Distributed Futures for Irregular Parallel Task Graphs

**Problem**: Custom parallel computations that don't fit neatly into DataFrame/Array row/column structures.

**Solution**:
Use the Dask Distributed Client with asynchronous futures:

```python
from dask.distributed import Client

client = Client(n_workers=4, threads_per_worker=2)

def train_partition(part_id: int):
    # Train local sub-model
    return f"Model {part_id} trained"

futures = [client.submit(train_partition, i) for i in range(10)]
results = client.gather(futures)
print(results)
```

## Best Practices (2026)

- **Do** check the Dask Web Dashboard (typically on port 8787) to monitor memory pressure, task streams, and bottlenecks.
- **Do** choose chunk sizes between 100MB and 300MB in memory for optimal parallel efficiency.
- **Do** persist intermediate DataFrames (`df = df.persist()`) when querying the same transformed data repeatedly.
- **Do** filter columns and rows early using column projections and predicate pushdown.
- **Don't** call `.compute()` inside loops; build the complete task graph and call `compute()` once.
- **Don't** use Dask if data fits comfortably in RAM; native Pandas and Polars are significantly faster for in-memory tasks.
- **Don't** create millions of tiny delayed tasks; excessive task overhead degrades scheduler performance.

## Troubleshooting

| Error                                             | Cause                                                              | Solution                                                               |
| :------------------------------------------------ | :----------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `KilledWorker: Worker exceeded 95% memory budget` | Task partition too large to fit in worker RAM during compute.      | Increase number of partitions: `df.repartition(npartitions=100)`.      |
| `UserWarning: Sending large object to workers`    | Large NumPy array or DataFrame passed as direct function argument. | Scatter data once with `client.scatter(data)` before submitting tasks. |
| `Slow compute: Too many tiny tasks`               | Thousands of micro-partitions causing task scheduling overhead.    | Merge small partitions using `repartition(partition_size="100MB")`.    |

## References

- [Dask Documentation](https://graph.dask.org/)
