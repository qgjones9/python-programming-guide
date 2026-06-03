# [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html)

The [`statistics`](https://docs.python.org/3/library/statistics.html) module (3.4+) provides **calculator-grade descriptive statistics** on numeric (`Real`) data — means, medians, spread, quantiles, covariance, correlation, and simple linear regression. It supports `int`, `float`, [`Decimal`](../decimal-decimal-fixed-point-and-floating-point-arithmetic/index.md), and [`Fraction`](../fractions-rational-numbers/index.md) but is **not** a NumPy/SciPy replacement. Functions that sort data behave poorly with **`NaN`** unless stripped first. Full formulas and edge cases are on [docs.python.org](https://docs.python.org/3/library/statistics.html).

---

## Averages and central tendency

| Function | Measures |
|----------|----------|
| `mean(data)` | Arithmetic average (any numeric type in tower) |
| `fmean(data, weights=None)` | Fast float mean; optional weights |
| `geometric_mean(data)` | nth root of product |
| `harmonic_mean(data)` | Reciprocal average |
| `median`, `median_low`, `median_high` | Middle order statistics |
| `median_grouped(data, interval=1)` | Median of histogram-style grouped data |
| `mode`, `multimode(data)` | Most common discrete/nominal values |
| `quantiles(data, n=4, method='exclusive')` | Equal-probability cut points |

```python
# Goal: weighted course grade and robust median
import statistics

grades = [85, 92, 83, 91]
weights = [0.20, 0.20, 0.30, 0.30]
assert statistics.fmean(grades, weights) == 87.6
sample = [14.4, 18.3, 19.2, 20.7]
assert statistics.median(sample) == 18.75
```

---

## Spread (variance and standard deviation)

| Function | Population vs sample |
|----------|----------------------|
| `pvariance(data, mu=None)` | Population variance σ² |
| `pstdev(data, mu=None)` | Population std dev σ |
| `variance(data, xbar=None)` | Sample variance s² (Bessel correction) |
| `stdev(data, xbar=None)` | Sample std dev s |

```python
# Goal: sample vs population spread on same tiny dataset
import statistics
import math

data = [2, 4, 4, 4, 5, 5, 7, 9]
assert statistics.mean(data) == 5.0
assert statistics.pstdev(data) == math.sqrt(statistics.pvariance(data))
assert statistics.stdev(data) > statistics.pstdev(data)
```

---

## Relations between two variables

| Function | Output |
|----------|--------|
| `covariance(x, y)` | Sample covariance |
| `correlation(x, y, method='linear')` | Pearson r (or Spearman with `method='ranked'`) |
| `linear_regression(x, y)` | `LinearRegression(slope, intercept)` named tuple |

```python
# Goal: fit a simple linear trend
import statistics

xs = [1, 2, 3, 4, 5]
ys = [2, 4, 5, 4, 5]
reg = statistics.linear_regression(xs, ys)
assert reg.slope > 0
predict = reg.slope * 6 + reg.intercept
assert 4.0 < predict < 7.0
assert -1.0 <= statistics.correlation(xs, ys) <= 1.0
```

---

## Density estimation (3.13+)

| Function | Role |
|----------|------|
| `kde(data, h=None, kernel='normal')` | Kernel density estimate callable |
| `kde_random(data, h=None, kernel='normal')` | Random draws from KDE |

Useful for lightweight simulation when NumPy is unavailable.

```python
# Goal: mode of discrete data and multimodal list
import statistics

values = ["red", "blue", "red", "green", "red", "blue"]
assert statistics.mode(values) == "red"
assert statistics.multimode([1, 1, 2, 2, 3]) == [1, 2]
```

---

## Handling missing `NaN` values

| Affected functions | Issue |
|--------------------|-------|
| `median*`, `mode`, `multimode`, `quantiles` | NaN distorts sort order |

Strip NaNs before calling order-sensitive APIs.

```python
# Goal: strip NaN before median
import math
import statistics
from itertools import filterfalse

raw = [20.7, float("nan"), 19.2, 18.3, float("nan"), 14.4]
clean = list(filterfalse(math.isnan, raw))
assert statistics.median(clean) == 18.75
assert sum(map(math.isnan, raw)) == 2
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Strip **`NaN`** before median/quantiles | Sort semantics put NaN first unpredictably |
| Use **`fmean`** for large float datasets | Faster and always returns float |
| Pass **`weights`** to `fmean` for aggregated stats | Correct weighted averages |
| Choose **`pstdev` vs `stdev`** deliberately | Population vs sample inference |
| Normalize mixed types with **`map(float, data)`** | Mixed input is undefined |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `mean([])` | `StatisticsError` | Guard empty inputs |
| `harmonic_mean` with zero | `StatisticsError` | Filter non-positive values |
| `median` with NaN present | Unexpected middle value | Pre-filter NaN |
| Expecting **`statistics`** to handle dates/strings | Type errors or nonsense | Convert to numeric first |
| Using sample **`stdev`** on full population | Under-estimates dispersion | Use **`pstdev`** when data is complete population |
