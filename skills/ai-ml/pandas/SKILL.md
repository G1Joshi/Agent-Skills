---
name: pandas
description: Expert pandas assistance covering DataFrames, indexing, grouping, merging, time series, and vectorized transformations. Use when cleaning, transforming, and analyzing tabular datasets in Python.
---

# Pandas

Pandas provides expressive, flexible data structures for tabular data manipulation and analysis in Python, featuring optimized Copy-on-Write (CoW) memory management.

## When to Use

- **In-Memory Tabular Data Manipulation**: Cleaning, transforming, merging, and reshaping tabular business data.
- **Time-Series Analysis & Resampling**: Date-range indexing, rolling window calculations, and financial resampling.
- **Modern PyArrow Backend (Pandas 2.0+)**: Leveraging Arrow string types for 2x-5x memory savings and instant parsing.
- **Exploratory Data Prep & Feature Engineering**: Computing group statistics, one-hot encodings, and pivot tables.

## Quick Start

```python
import pandas as pd

# Load CSV and compute group summaries
df = pd.DataFrame({
    'category': ['Tech', 'Health', 'Tech', 'Finance', 'Health'],
    'revenue': [1200, 800, 1500, 2200, 950],
    'units': [12, 8, 15, 20, 9]
})

summary = df.groupby('category').agg(
    total_rev=('revenue', 'sum'),
    avg_price=('revenue', lambda x: (x / df.loc[x.index, 'units']).mean())
).reset_index()

print(summary)
```

## Core Concepts

### Method Chaining with Modern PyArrow Backend

Clean, functional data transformation pipelines without intermediate variables:

```python
import pandas as pd
import numpy as np

# Load dataset using high-performance PyArrow backend
df = pd.read_csv(
    'orders.csv',
    dtype_backend='pyarrow',
    parse_dates=['order_date']
)

# Declarative pipeline using method chaining
kpi_summary = (
    df
    .query('status == "delivered" and total_amount > 0')
    .assign(
        margin_usd=lambda x: x['total_amount'] * 0.22,
        order_month=lambda x: x['order_date'].dt.to_period('M')
    )
    .groupby(['order_month', 'region'])
    .agg(
        total_revenue=('total_amount', 'sum'),
        total_margin=('margin_usd', 'sum'),
        avg_order_value=('total_amount', 'mean'),
        order_count=('order_id', 'count')
    )
    .reset_index()
    .sort_values(by='total_revenue', ascending=False)
)

print(kpi_summary.head(10))
```

### Time-Series Resampling & Rolling Windows

Computing moving averages and periodic intervals:

```python
# Create time-indexed financial series
dates = pd.date_range(start='2026-01-01', periods=100, freq='D')
stock_prices = pd.Series(np.random.normal(loc=150, scale=5, size=100), index=dates)

# Rolling 7-day moving average and 30-day volatility
rolling_metrics = pd.DataFrame({
    'price': stock_prices,
    'ma_7d': stock_prices.rolling(window=7, min_periods=1).mean(),
    'volatility_30d': stock_prices.rolling(window=30, min_periods=1).std()
})

# Weekly resampled summary
weekly_summary = stock_prices.resample('W').agg(['first', 'max', 'min', 'last'])
print(weekly_summary.head())
```

### Safe Data Mutation Avoiding SettingWithCopyWarning

Modifying slices explicitly:

```python
# Anti-pattern: df[df['age'] > 18]['status'] = 'adult'  # SettingWithCopyWarning!

# Idiomatic Pattern: Use .loc directly or .copy()
adults_df = df.loc[df['age'] > 18].copy()
adults_df['status'] = 'adult'
```

## Common Patterns

### Method Chaining with Assign and Query

**Problem**: Creating dozens of temporary intermediate DataFrame variables clutters script memory.

**Solution**:
Use readable method chaining pipelines:

```python
clean_df = (
    pd.read_csv("sales.csv")
    .dropna(subset=["customer_id"])
    .query("amount > 0 and status == 'COMPLETED'")
    .assign(
        amount_usd=lambda x: x["amount"] * x["exchange_rate"],
        order_month=lambda x: pd.to_datetime(x["order_date"]).dt.to_period("M")
    )
    .sort_values("amount_usd", ascending=False)
)
```

## Best Practices

**Do**:

- Target Pandas 2.2+ with `dtype_backend="pyarrow"` to eliminate string object overhead and boost performance.
- Use method chaining (`.pipe()`, `.assign()`, `.query()`) for clear, readable, and reproducible data workflows.
- Use `.loc[row_indexer, col_indexer]` for assignments to prevent `SettingWithCopyWarning`.
- Downcast integer and float types (`float32`, `int16`) or use categorical types to slash memory on large tables.

**Don't**:

- Iterate over DataFrame rows using `iterrows()` or `itertuples()` if vectorized operations can do the work.
- Use `inplace=True`; it is deprecated across modern Pandas methods.
- Concatenate DataFrames inside a loop; collect records into a list and call `pd.concat(list_of_dfs)` once.

## Troubleshooting

| Error                                          | Cause                                                                         | Solution                                                        |
| :--------------------------------------------- | :---------------------------------------------------------------------------- | :-------------------------------------------------------------- |
| `SettingWithCopyWarning`                       | Modifying a slice of a DataFrame rather than an explicit copy.                | Use `.loc[row_indexer, col_indexer] = value` or call `.copy()`. |
| `KeyError: '...'`                              | Column name does not exist, or column names have leading/trailing whitespace. | Strip column names: `df.columns = df.columns.str.strip()`.      |
| `DtypeWarning: Columns (...) have mixed types` | Large CSV contains inconsistent data types across chunks.                     | Specify explicit `dtype={'col_name': str}` in `pd.read_csv()`.  |

## References

- [Pandas Documentation](https://pandas.pydata.org/)
