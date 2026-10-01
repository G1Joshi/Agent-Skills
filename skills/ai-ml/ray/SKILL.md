---
name: ray
description: Expert Ray distributed computing assistance covering Ray Core (actors, tasks), Ray Train, Ray Tune, and Ray Serve. Use when scaling Python compute and ML training across multi-node clusters.
---

# Ray

Ray is an open-source unified compute framework that makes it easy to scale AI and Python workloads across distributed clusters with Ray Train, Ray Data, and Ray Serve.

## When to Use

- **Distributed Python Applications**: Scaling compute-heavy Python tasks seamlessly from a single laptop to large cloud clusters.
- **Distributed ML Training with Ray Train**: Orchestrating multi-node PyTorch, XGBoost, and LightGBM training jobs.
- **Production Model Serving with Ray Serve**: Serving LLMs and multi-model microservice pipelines with dynamic autoscaling.
- **Hyperparameter Optimization with Ray Tune**: Running Bayesian, Optuna, and population-based training sweeps across hundreds of workers.

## Quick Start

```python
import ray

ray.init()

# Remote distributed task
@ray.remote
def square(x):
    return x * x

# Launch tasks in parallel across cluster
futures = [square.remote(i) for i in range(10)]
results = ray.get(futures)
print("Computed squares:", results)
```

## Core Concepts

### Distributed Tasks & Stateful Actors

Scaling functions and classes across cluster workers:

```python
import ray
import time

# Initialize local or connect to remote Ray cluster
ray.init(ignore_reinit_error=True)

# 1. Stateless Remote Function (Distributed Task)
@ray.remote
def process_data_chunk(chunk_id: int) -> dict:
    time.sleep(0.5) # Simulating CPU/IO bound computation
    return {"chunk_id": chunk_id, "processed_items": 1000 * chunk_id}

# Launch tasks concurrently across cluster
futures = [process_data_chunk.remote(i) for i in range(8)]
results = ray.get(futures) # Gather results
print("Processed Chunks:", results)

# 2. Stateful Remote Class (Distributed Actor)
@ray.remote
class GlobalCounter:
    def __init__(self):
        self.count = 0

    def increment(self) -> int:
        self.count += 1
        return self.count

counter_actor = GlobalCounter.remote()
inc_futures = [counter_actor.increment.remote() for _ in range(5)]
print("Final actor count:", ray.get(inc_futures[-1]))
```

### Production Model Serving with Ray Serve

Deploying scalable REST endpoints with dynamic request batching:

```python
from ray import serve
import torch
from transformers import pipeline

@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class SentimentClassifier:
    def __init__(self):
        self.classifier = pipeline("sentiment-analysis")

    async def __call__(self, request):
        json_data = await request.json()
        text = json_data.get("text", "")
        return self.classifier(text)

app = SentimentClassifier.bind()
# serve.run(app)
```

### Distributed Hyperparameter Tuning with Ray Tune

Running parallel hyperparameter trials:

```python
from ray import tune

def training_function(config):
    # Simulated model training
    for step in range(10):
        intermediate_score = config["alpha"] * step + config["beta"]
        tune.report(loss=1.0 / (intermediate_score + 0.1))

search_space = {
    "alpha": tune.uniform(0.1, 1.0),
    "beta": tune.choice([1, 2, 5])
}

tuner = tune.Tuner(
    training_function,
    param_space=search_space,
    tune_config=tune.TuneConfig(num_samples=10, metric="loss", mode="min")
)
results = tuner.fit()
print("Best hyperparameters:", results.get_best_result().config)
```

## Common Patterns

### Stateful Distributed Actors for Model Serving

**Problem**: Re-loading large model weights into memory on every function invocation.

**Solution**:
Use Ray Actors to hold in-memory state across requests:

```python
@ray.remote(num_gpus=1)
class ModelServer:
    def __init__(self):
        # Load weights once into GPU VRAM
        self.model = load_large_model()

    def predict(self, sample):
        return self.model(sample)

server_actor = ModelServer.remote()
prediction = ray.get(server_actor.predict.remote(sample_data))
```

## Best Practices

**Do**:

- Check the Ray Dashboard (port 8265) to monitor node CPU/GPU utilization, actor placement, and object store memory.
- Pass large read-only datasets via the Ray plasma object store (`ray.put(data)`) to prevent repetitive serializations.
- Specify resource requirements explicitly in decorators (`@ray.remote(num_cpus=2, num_gpus=1)`).
- Use Ray Serve for production multi-model microservices with built-in auto-batching.

**Don't**:

- Call `ray.get()` inside remote tasks; pass ObjectRefs directly to other remote tasks to preserve pipelining.
- Create millions of micro-tasks; batch fine-grained tasks together to minimize scheduler overhead.
- Pass large stateful objects (like database connections or open files) inside remote arguments.

## Troubleshooting

| Error                                                     | Cause                                                                | Solution                                                                       |
| :-------------------------------------------------------- | :------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| `RaySystemError: Object store full`                       | Tasks producing more data than allocated shared memory plasma store. | Use `ray.get()` to consume results, or store large arrays in disk storage.     |
| `Actor died unexpectedly`                                 | Worker process crashed due to unhandled exception or OOM.            | Check logs in Ray dashboard (`http://localhost:8265`) and increase worker RAM. |
| `Task failed to schedule: Unsatisfiable resource request` | Requested more CPUs/GPUs (`num_gpus=2`) than available on cluster.   | Verify available resources via `ray.cluster_resources()`.                      |

## References

- [Ray Documentation](https://docs.ray.io/)
