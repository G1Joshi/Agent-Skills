---
name: vaex
description: Expert Vaex out-of-core data analytics assistance covering lazy evaluation, memory mapping (mmap), and billion-row DataFrame visualizations. Use when analyzing huge tabular datasets without loading them into RAM.
---

# Vaex

Vaex is a hidden gem. It uses **Memory Mapping** to open 100GB files instantly on a laptop and visualize them.

## When to Use

- **Billion-Row Tabular Analytics on a Single Laptop**: Interactive exploration and statistics on 100M-1B+ rows without cloud clusters.
- **Zero-Copy Memory-Mapped Files (HDF5 / Arrow)**: Opening 100GB+ files in milliseconds without loading data into RAM.
- **Virtual Columns & Lazy Evaluation**: Computing derived features and statistical transforms without allocating additional memory.
- **Ultra-Fast 2D Heatmaps & Visualizations**: Generating histograms, binned heatmaps, and scatter visualizations instantly.

## Quick Start

```python
import vaex

# Instantly memory-map 100M+ row HDF5/Arrow dataset without loading into RAM
df = vaex.open('billion_records.hdf5')

# Instant computation across billions of rows
mean_val = df.mean(df.amount)
print("Dataset row count:", len(df))
print("Mean amount:", mean_val)
```

## Core Concepts

#Opening & Querying Billion-Row Datasets Lazily

Memory-mapping huge datasets without RAM exhaustion:

```python
import vaex

# Open 100GB+ dataset instantaneously (zero memory allocation)
df = vaex.open('s3://massive-analytics/yellow_tripdata.arrow')

print(f"Total rows in dataset: {len(df):,}")

# Virtual column: computed lazily on-the-fly without memory consumption
df['trip_duration_min'] = (df.dropoff_datetime - df.pickup_datetime) / 60.0
df['speed_mph'] = df.trip_distance / (df.trip_duration_min / 60.0)

# Filter rows lazily
filtered_df = df[(df.trip_distance > 0) & (df.trip_distance < 100) & (df.speed_mph < 80)]

# Compute summary statistics across 1 billion rows in sub-seconds
mean_speed = filtered_df.speed_mph.mean()
total_passengers = filtered_df.passenger_count.sum()

print(f"Mean Speed: {mean_speed:.2f} mph, Total Passengers: {total_passengers:,}")
```

#High-Speed Binned Aggregations & Heatmaps

Computing 2D binned histograms across millions of points:

```python
import matplotlib.pyplot as plt

# Compute 2D binned aggregation directly in Vaex
heatmap_counts = filtered_df.count(binby=[filtered_df.pickup_longitude, filtered_df.pickup_latitude], shape=256)

plt.figure(figsize=(8, 8))
plt.imshow(heatmap_counts, cmap='hot', origin='lower')
plt.title("Pickup Density Heatmap (Computed in 150ms)")
plt.savefig("pickup_density.png")
```

#Exporting and Converting Large Datasets

Converting CSV files to fast memory-mapped Apache Arrow format:

```python
# Convert giant CSV to chunked memory-mapped Arrow
vaex.from_csv('giant_raw_data.csv', convert='giant_data.arrow', chunk_size=5_000_000)
```

## Common Patterns

### Virtual Columns and Fast Heatmap Binning

**Problem**: Creating derived columns duplicates memory when working with 100GB+ datasets.

**Solution**:
Use Vaex zero-memory virtual columns:

```python
# Virtual column: stored as an expression formula, zero memory allocated
df['tax'] = df.amount * 0.2

# Fast 2D histogram binning across 100 million points in under 1 second
heatmap = df.count(binby=[df.x, df.y], shape=128)
```

## Best Practices (2026)

- **Do** convert raw CSV or JSON files to Apache Arrow (`.arrow`) or HDF5 format to enable memory-mapping.
- **Do** leverage virtual columns (`df['col'] = ...`) rather than materializing copies to minimize RAM usage.
- **Do** use Vaex binned statistics (`df.count(binby=...)`) for large-scale data visualization rather than raw scatter plots.
- **Do** keep calculations within Vaex expressions to maintain multi-threaded C++ execution speeds.
- **Don't** convert massive Vaex DataFrames to Pandas (`df.to_pandas_df()`) if the dataset exceeds system RAM.
- **Don't** iterate over rows with Python loops; use Vaex aggregation expressions.
- **Don't** write intermediate datasets to uncompressed CSV; use Arrow or Parquet.

## Troubleshooting

| Error                                               | Cause                                                            | Solution                                                             |
| :-------------------------------------------------- | :--------------------------------------------------------------- | :------------------------------------------------------------------- |
| `FileNotFoundError / Unable to open file`           | Target file format not HDF5, Arrow, or Parquet.                  | Convert CSV to HDF5 once: `vaex.from_csv('file.csv', convert=True)`. |
| `AttributeError: DataFrame has no attribute 'iloc'` | Vaex is not pandas; row-based integer indexing is not supported. | Use boolean filtering `df[df.col > 0]` instead of iloc.              |
| `Memory spikes during export`                       | Exporting to uncompressed format without chunking.               | Export in chunks or write directly to Parquet/Arrow format.          |

## References

- [Vaex Documentation](https://vaex.io/docs/index.html)
