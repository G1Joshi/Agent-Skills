---
name: pandas
description: Pandas data analysis library with DataFrames and data manipulation. Use for data processing.
---

# Pandas

Data analysis and manipulation library for Python.

## When to Use

- Data cleaning and preprocessing
- Exploratory data analysis
- CSV/Excel file processing
- Data transformation pipelines

## Quick Start

```python
import pandas as pd

# Read data
df = pd.read_csv('data.csv')

# Basic operations
df.head()
df.info()
df.describe()

# Filtering
active_users = df[df['status'] == 'active']
```

## Core Concepts

### DataFrame Operations

```python
# Create DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NYC', 'LA', 'Chicago']
})

# Selection
df['name']                    # Single column
df[['name', 'age']]          # Multiple columns
df.loc[0]                     # Row by label
df.iloc[0:2]                  # Rows by position

# Filtering
df[df['age'] > 25]
df.query('age > 25 and city == "NYC"')
```

### Data Manipulation

```python
# Add/modify columns
df['age_group'] = df['age'].apply(lambda x: 'young' if x < 30 else 'adult')
df['full_name'] = df['first_name'] + ' ' + df['last_name']

# Grouping
df.groupby('city')['sales'].sum()
df.groupby(['city', 'year']).agg({
    'sales': 'sum',
    'orders': 'count',
    'price': 'mean'
})

# Pivot tables
pd.pivot_table(df, values='sales', index='city', columns='year', aggfunc='sum')
```

## Common Patterns

### Data Cleaning

```python
# Handle missing values
df.dropna()
df.fillna(0)
df['column'].fillna(df['column'].median(), inplace=True)

# Remove duplicates
df.drop_duplicates(subset=['email'])

# Type conversion
df['date'] = pd.to_datetime(df['date'])
df['price'] = pd.to_numeric(df['price'], errors='coerce')
```

### Merging DataFrames

```python
# Merge (SQL-like join)
merged = pd.merge(orders, customers, on='customer_id', how='left')

# Concat
combined = pd.concat([df1, df2], ignore_index=True)
```

## Best Practices

**Do**:

- Use vectorized operations
- Chain methods for readability
- Use `query()` for complex filters
- Set appropriate dtypes

**Don't**:

- Iterate with for loops
- Modify during iteration
- Use `inplace=True` in chains
- Ignore memory usage

## Troubleshooting

| Issue           | Cause              | Solution           |
| --------------- | ------------------ | ------------------ |
| Memory error    | Large dataset      | Use chunks or dask |
| SettingWithCopy | Chained assignment | Use .loc[]         |
| Slow operation  | Not vectorized     | Use apply or numpy |

## References

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
