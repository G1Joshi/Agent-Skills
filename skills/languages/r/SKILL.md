---
name: r
description: Expert R language assistance covering tidyverse, data.table, ggplot2, statistical modeling, and vectorized dataframes. Use when analyzing datasets, building statistical models, or generating research visualizations.
---

# R

A language and environment for statistical computing and graphics.

## When to Use

- **Statistical Analysis & Econometrics**: Hypothesis testing, regression modeling, survival analysis, and statistical research.
- **Publication-Ready Data Visualization (ggplot2)**: Creating high-fidelity, publication-quality statistical charts and graphics.
- **Data Wrangling with the Tidyverse**: Transforming and aggregating complex datasets using `dplyr`, `tidyr`, and pipes (`|>`).
- **Interactive Dashboards & Reports (Shiny / Quarto)**: Publishing dynamic web dashboards and reproducible scientific documents.

## Quick Start

```r
print("Hello, World!")

# Vector
x <- c(1, 2, 3, 4, 5)

# Mean
mean(x)

# Data Frame
df <- data.frame(
  Name = c("Alice", "Bob"),
  Age = c(25, 30)
)
```

## Core Concepts

#The Grammar of Graphics (ggplot2)

Composes statistical visualizations by layering data, aesthetic mappings, geometries, and facets:

```r
library(ggplot2)

# Compose visual layers declaratively
ggplot(mpg, aes(x = displ, y = hwy, color = class)) +
  geom_point(size = 3, alpha = 0.8) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "Engine Displacement vs Highway Fuel Economy",
    x = "Displacement (Liters)",
    y = "Highway MPG"
  ) +
  theme_minimal()
```

#Tidy Data Transformations with `dplyr` and Native Pipe (`|>`)

Transforms tables using standardized verbs and R 4.1+ native forward pipes:

```r
library(dplyr)

summary_stats <- starwars |>
  filter(!is.na(height), !is.na(mass)) |>
  group_by(species) |>
  summarise(
    count = n(),
    avg_height = mean(height),
    median_mass = median(mass)
  ) |>
  filter(count >= 2) |>
  arrange(desc(avg_height))
```

#Fast Columnar In-Memory Processing with `data.table`

Blazing fast processing of multi-gigabyte datasets:

```r
library(data.table)
dt <- data.table(iris)
dt[Species == "setosa", .(Avg_Petal_Length = mean(Petal.Length)), by = Species]
```

## Common Patterns

### Tidyverse Data Transformation Pipeline

**Problem**: Multiple intermediate dataframe copies cluttering memory during analysis.

**Solution**:
Use dplyr pipe operator (`%>%` or `|>`) for stream processing:

```r
library(dplyr)

summary_stats <- mtcars %>%
  filter(mpg > 15) %>%
  group_by(cyl) %>%
  summarise(
    mean_mpg = mean(mpg),
    mean_hp = mean(hp),
    count = n()
  ) %>%
  arrange(desc(mean_mpg))

print(summary_stats)
```

## Best Practices (2026)

**Do**:

- **Use the Native Pipe (`|>`)**: Standardize on R 4.1+ native pipe (`|>`) over legacy `magrittr` (`%>%`).
- **Use `renv` for Reproducible Environments**: Lock exact package versions in `renv.lock` to ensure reproducible research.
- **Adopt `data.table` or `arrow` for Big Data**: Avoid out-of-memory crashes on multi-million row datasets.
- **Publish with Quarto**: Author reproducible reports, slides, and websites using modern Quarto (`.qmd`).

**Don't**:

- **Don't use `attach()`**: `attach()` pollutes search namespaces and causes silent variable masking bugs.
- **Don't grow arrays inside iterative loops**: Pre-allocate vector sizes or use vectorized vectorized functions (`lapply`, `purrr::map`).
- **Don't use `1:length(x)`**: If `x` is empty, `1:0` creates an invalid 2-element vector; use `seq_along(x)` instead.

## Troubleshooting

| Error                                                | Cause                                                            | Solution                                                          |
| :--------------------------------------------------- | :--------------------------------------------------------------- | :---------------------------------------------------------------- |
| `Error in ... : could not find function "%>%"`       | Pipe operator used without loading `magrittr` or `dplyr`.        | Add `library(dplyr)` or use native R 4.1+ pipe `                  | >`. |
| `cannot allocate vector of size ... (Out of memory)` | Dataset exceeds available RAM.                                   | Use `data.table` or chunk analysis with the `arrow` package.      |
| `object '...' not found`                             | Variable evaluated before declaration or misspelled column name. | Verify spelling and check active environment objects with `ls()`. |

## References

- [R Project](https://www.r-project.org/)
- [R for Data Science](https://r4ds.had.co.nz/)
