---
name: spark
description: Expert Apache Spark assistance covering PySpark, Spark SQL, DataFrame transformations, broadcast joins, and cluster optimization. Use when processing petabyte distributed data and running big data ETL pipelines.
---

# Apache Spark

Spark is the king of Big Data. v4.0 (2024/2025) makes **Spark Connect** the default, allowing thin clients (like VS Code) to connect to massive clusters easily.

## When to Use

- **Petabyte-Scale Distributed Data Processing**: Transforming massive datasets across cloud clusters with Apache Spark 3.5+.
- **Real-Time Streaming Pipelines**: Low-latency stream processing with Spark Structured Streaming.
- **Enterprise Lakehouse Architectures**: Querying and updating Delta Lake, Apache Iceberg, and Apache Hudi tables.
- **Distributed SQL & Complex Analytical Aggregations**: Distributed joins, window functions, and analytics with Catalyst Optimizer.

## Quick Start

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

spark = SparkSession.builder \
    .appName("AnalyticsETL") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

df = spark.read.parquet("s3a://data-lake/sales/")
summary = df.groupBy("country").agg(avg("amount").alias("avg_spent"))
summary.write.mode("overwrite").parquet("s3a://data-lake/reports/summary/")
```

## Core Concepts

#Structured DataFrame Transformations & Window Functions

Distributed analytical querying with PySpark:

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("CustomerAnalytics2026") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

# Read partitioned Parquet from cloud storage
df = spark.read.parquet("s3a://data-lake/transactions/")

# Define window partitioned by customer ordered by timestamp
customer_window = Window.partitionBy("customer_id").orderBy("transaction_time")

# Compute cumulative spend and previous transaction date
enhanced_df = df.filter(F.col("status") == "COMPLETED") \
    .withColumn("running_total", F.sum("amount").over(customer_window)) \
    .withColumn("prev_transaction_time", F.lag("transaction_time", 1).over(customer_window)) \
    .withColumn("days_since_last", F.datediff(F.col("transaction_time"), F.col("prev_transaction_time")))

enhanced_df.write \
    .mode("overwrite") \
    .partitionBy("region") \
    .parquet("s3a://data-lake/marts/customer_summary/")
```

#Broadcast Joins for Skewed Dimensions

Optimizing distributed joins between large fact tables and small dimension lookup tables:

```python
# Broadcast small dimension table to all executors, eliminating expensive shuffles
dimension_df = spark.read.parquet("s3a://data-lake/dimensions/merchant_tiers/")

joined_df = df.join(
    F.broadcast(dimension_df),
    on="merchant_id",
    how="inner"
)
```

#Spark Structured Streaming from Kafka

Continuous stream processing with checkpointing:

```python
stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "telemetry-events") \
    .load()

parsed_stream = stream_df.selectExpr("CAST(value AS STRING) as json_payload")

query = parsed_stream.writeStream \
    .format("parquet") \
    .option("path", "s3a://data-lake/raw_stream/") \
    .option("checkpointLocation", "s3a://data-lake/checkpoints/telemetry/") \
    .trigger(processingTime="1 minute") \
    .start()
```

## Common Patterns

### Broadcast Join for Skewed Dimensions

**Problem**: Joining a small lookup table with a massive distributed fact table causes slow shuffle exchanges across executors.

**Solution**:
Broadcast the small table to all worker nodes:

```python
from pyspark.sql.functions import broadcast

large_fact_df = spark.read.parquet("events/")
small_dim_df = spark.read.csv("country_codes.csv", header=True)

# Broadcast join eliminates shuffle network overhead
result_df = large_fact_df.join(broadcast(small_dim_df), "country_id")
```

## Best Practices (2026)

- **Do** enable Adaptive Query Execution (`spark.sql.adaptive.enabled=true`) for automatic partition coalescing and join optimization.
- **Do** use `F.broadcast()` when joining a large DataFrame with a small table (< 100MB) to eliminate shuffle overhead.
- **Do** always specify an explicit `checkpointLocation` on durable cloud storage for Structured Streaming jobs.
- **Do** cache or persist (`df.persist()`) intermediate DataFrames only when reused multiple times in the same job.
- **Don't** collect massive DataFrames to the driver node (`df.collect()`); write directly to cloud storage.
- **Don't** use Python UDFs (`@udf`) if native `pyspark.sql.functions` exist; native functions avoid JVM-Python serialization overhead.
- **Don't** leave small file problems unaddressed; use Delta Lake `OPTIMIZE` or coalesce partitions before writing.

## Troubleshooting

| Error                                                                        | Cause                                                           | Solution                                                                       |
| :--------------------------------------------------------------------------- | :-------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| `java.lang.OutOfMemoryError: Java heap space on Executor`                    | Data skew or partition sizes too large for executor memory.     | Increase `spark.executor.memory` or salt skewed keys before grouping.          |
| `Container killed by YARN for exceeding memory limits`                       | Off-heap overhead or Python process exceeding memory threshold. | Increase `spark.yarn.executor.memoryOverhead` to 1GB+.                         |
| `Total size of serialized results is bigger than spark.driver.maxResultSize` | Calling `.collect()` on massive distributed DataFrame.          | Write output to disk or use `.take(100)` instead of collecting entire dataset. |

## References

- [Apache Spark](https://spark.apache.org/)
