---
name: dbt
description: Expert dbt (data build tool) assistance covering SQL modeling, Jinja macros, tests, documentation, and semantic layer. Use when building analytics engineering pipelines on BigQuery, Snowflake, or PostgreSQL.
---

# dbt (Data Build Tool)

dbt manages data transformation in the warehouse using SQL. v2.0 introduces the **Fusion Engine** (Rust) for performance.

## When to Use

- **Analytics Engineering & Data Transformations**: Transforming raw data inside modern cloud warehouses (Snowflake, BigQuery, Databricks, Redshift).
- **Modular SQL with Jinja & Version Control**: Building reusable SQL models with DAG dependencies and macros.
- **Data Quality & Schema Testing**: Enforcing `unique`, `not_null`, referential integrity, and custom singular tests.
- **Automated Data Documentation & Lineage**: Generating interactive dependency lineage graphs directly from codebase schemas.

## Quick Start

```sql
-- models/marts/fct_orders.sql
{{ config(materialized='table') }}

with orders as (
    select * from {{ ref('stg_orders') }}
),
payments as (
    select * from {{ ref('stg_payments') }}
)

select
    orders.order_id,
    orders.customer_id,
    orders.order_date,
    coalesce(payments.amount, 0) as total_amount
from orders
left join payments using (order_id)
```

## Core Concepts

#Declarative SQL Modeling with ref() & source()

Building transformation models with dependency resolution:

```sql
-- models/marts/core/fct_customer_orders.sql
{{
  config(
    materialized = 'incremental',
    unique_key = 'order_id',
    on_schema_change = 'fail'
  )
}}

with orders as (
    select * from {{ ref('stg_orders') }}
    {% if is_incremental() %}
      where order_date >= (select coalesce(max(order_date), '1970-01-01') from {{ this }})
    {% endif %}
),

customers as (
    select * from {{ ref('stg_customers') }}
)

select
    o.order_id,
    o.customer_id,
    c.full_name as customer_name,
    o.order_date,
    o.total_amount_usd
from orders o
inner join customers c on o.customer_id = c.customer_id
```

#Schema Testing & Documentation in YAML

Enforcing column constraints and documentation:

```yaml
# models/marts/core/schema.yml
version: 2

models:
  - name: fct_customer_orders
    description: "Daily customer order fact table combining staged orders and customer dimensions."
    columns:
      - name: order_id
        description: "Primary key for orders."
        tests:
          - unique
          - not_null

      - name: customer_id
        description: "Foreign key referencing staging customers."
        tests:
          - not_null
          - relationships:
              to: ref('stg_customers')
              field: customer_id

      - name: total_amount_usd
        description: "Total transaction value in USD."
        tests:
          - not_null
```

#Jinja Macros for DRY Reusable Logic

Creating custom reusable SQL utilities:

```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, decimal_places=2) -%}
    round(cast(({{ column_name }} / 100.0) as numeric), {{ decimal_places }})
{%- endmacro %}

-- Usage in model:
select
    id,
    {{ cents_to_dollars('amount_in_cents') }} as amount_usd
from {{ ref('stg_payments') }}
```

## Common Patterns

### Incremental Models with Timestamp Filtering

**Problem**: Rebuilding multi-billion-row tables from scratch on every dbt run is slow and expensive.

**Solution**:
Use `incremental` materialization with `is_incremental()`:

```sql
{{ config(
    materialized='incremental',
    unique_key='event_id'
) }}

select * from {{ source('raw', 'events') }}

{% if is_incremental() %}
  -- Only query rows created after the most recent event in the target table
  where event_timestamp > (select max(event_timestamp) from {{ this }})
{% endif %}
```

## Best Practices (2026)

- **Do** organize projects into standard layers: `staging` (1-to-1 with raw sources), `intermediate`, and `marts`.
- **Do** always use `{{ ref('model_name') }}` and `{{ source('source_name', 'table_name') }}` to maintain DAG lineage.
- **Do** implement incremental models (`materialized='incremental'`) for multi-million row fact tables.
- **Do** run `dbt test` in CI pipelines on every pull request to catch data schema regressions.
- **Don't** write raw database table references (e.g. `analytics.raw.users`); always use `source()` or `ref()`.
- **Don't** perform business logic inside staging models; staging should only clean, cast, and rename columns.
- **Don't** hardcode environments (dev vs prod); use `target.name` conditionals in profiles.yml.

## Troubleshooting

| Error                                                                              | Cause                                                                     | Solution                                                                    |
| :--------------------------------------------------------------------------------- | :------------------------------------------------------------------------ | :-------------------------------------------------------------------------- |
| `Compilation Error: Model '...' depends on a node named '...' which was not found` | Typo in `{{ ref('model_name') }}` or model file missing.                  | Check model filename matches referenced string exactly.                     |
| `dbt test failed: unique constraint violated`                                      | Duplicate keys generated by non-unique join condition.                    | Inspect duplicate keys in compiled SQL in `target/compiled/`.               |
| `Schema change error during incremental run`                                       | Upstream model added/removed columns breaking existing incremental table. | Run with `--full-refresh` once to rebuild schema: `dbt run --full-refresh`. |

## References

- [dbt Documentation](https://docs.getdbt.com/)
