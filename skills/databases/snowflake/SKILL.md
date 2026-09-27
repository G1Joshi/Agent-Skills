---
name: snowflake
description: Expert Snowflake cloud data warehouse assistance covering Virtual Warehouses, Snowpipe, zero-copy cloning, time travel, and Streamlit. Use when building enterprise analytical data warehouses or running big data analytics.
---

# Snowflake

Snowflake is a cloud-native data warehouse. It separates compute ("Virtual Warehouses") from storage, allowing them to scale independently.

## When to Use

- **Cloud Data Warehousing & Data Lakes**: Consolidating enterprise data across AWS, Azure, and GCP into a single analytical platform.
- **Separation of Compute and Storage (Virtual Warehouses)**: Scaling compute clusters up, down, or suspending instantly without copying data.
- **Zero-Copy Data Cloning & Time Travel**: Cloning multi-terabyte production databases in seconds for dev/test without storage cost duplication.
- **Secure Cross-Company Data Sharing**: Sharing live, governed datasets with external partners without ETL replication.

## Quick Start

```sql
-- Create warehouse (Compute)
CREATE WAREHOUSE my_wh WITH WAREHOUSE_SIZE = 'X-SMALL';

-- Query JSON directly (Variant type)
SELECT src:sales.order_id::integer
FROM raw_data;
```

## Core Concepts

#Multi-Cluster Shared Data Architecture

Decouples centralized cloud storage from independent, autoscaling virtual compute warehouses:

```
[ Central Cloud Storage (AWS S3 / Azure Blob / GCS) ]
         ├── [ Virtual Warehouse: ETL (Size: X-Large) ]
         ├── [ Virtual Warehouse: BI Reports (Size: Medium, Autoscale) ]
         └── [ Virtual Warehouse: Data Science (Size: Large) ]
```

#Time Travel & Zero-Copy Cloning

Restores historical data and creates instant instant clones without data duplication:

```sql
-- Query data as it existed 2 hours ago
SELECT * FROM analytics.orders
AT(OFFSET => -60*120)
WHERE status = 'FAILED';

-- Instant zero-copy clone for testing (takes 2 seconds, zero storage added)
CREATE OR REPLACE DATABASE dev_clone_2026 CLONE production;
```

#Native Semi-Structured VARIANT Querying

Ingests and queries nested JSON, Avro, and Parquet data directly:

```sql
SELECT
  raw_payload:user_id::string AS user_id,
  raw_payload:event_name::string AS event_name,
  raw_payload:metadata.device.os::string AS os_system
FROM raw_logs.event_stream
WHERE raw_payload:event_name = 'checkout_completed';
```

## Common Patterns

### Zero-Copy Cloning with Time Travel Recovery

**Problem**: Creating staging replicas of terabyte datasets for testing consumes massive storage and time.

**Solution**:
Use metadata-only Zero-Copy Cloning with Time Travel:

```sql
-- Instantly clone production database without duplicating underlying micro-partitions
CREATE OR REPLACE DATABASE dev_db CLONE prod_db;

-- Recover accidentally dropped or updated table state from 2 hours ago
CREATE OR REPLACE TABLE orders_restored CLONE prod_db.public.orders
  AT (OFFSET => -60*120);
```

## Best Practices (2026)

**Do**:

- **Enable Auto-Suspend and Auto-Resume**: Set warehouses to auto-suspend after 60 seconds of inactivity (`AUTO_SUSPEND = 60`) to stop billing.
- **Cluster by Primary Query Dimensions**: Apply cluster keys (`CLUSTER BY (event_date, customer_id)`) on multi-terabyte tables to optimize micro-partition pruning.
- **Leverage Transient Tables for Staging**: Use `CREATE TRANSIENT TABLE` for intermediate ETL steps to eliminate Time Travel storage costs.
- **Use Dynamic Data Masking**: Protect sensitive PII columns using role-based masking policies.

**Don't**:

- **Don't leave oversized virtual warehouses running 24/7**: Size warehouses appropriately; scale down when batch jobs complete.
- **Don't use Snowflake for single-row transactional OLTP**: High latency per single insert makes Snowflake unsuitable for low-latency operational backends.
- **Don't ignore micro-partition pruning**: Always filter queries by date or clustered keys to avoid full table scans.

## Troubleshooting

| Error                                               | Cause                                                        | Solution                                                              |
| :-------------------------------------------------- | :----------------------------------------------------------- | :-------------------------------------------------------------------- |
| `Warehouse '...' has exceeded maximum credit limit` | Long-running queries keeping large virtual warehouse active. | Configure `AUTO_SUSPEND = 60` and `AUTO_RESUME = TRUE` on warehouses. |
| `Query compilation error: ambiguous column name`    | Joins referencing shared column names without table aliases. | Qualify all column references with explicit table aliases.            |
| `Snowpipe load error: File size exceeds maximum`    | Staged file too large for streaming ingestion.               | Split input files into optimal 100MB-250MB compressed chunks.         |

## References

- [Snowflake Documentation](https://docs.snowflake.com/)
